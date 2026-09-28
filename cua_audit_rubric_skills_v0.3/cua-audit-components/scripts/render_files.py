#!/usr/bin/env python3
"""Turn a unit's staged files into page images an auditor can actually look at.

Text extraction (`extract_files.py`) says what a file CONTAINS. This says what
it LOOKS LIKE — pagination, clipping, overlap, fit-on-one-page, legibility —
which is what the rubric's `visual` criteria are written about.

Reads   audit/<unit>/files/{inputs,expected}/
Writes  audit/<unit>/render/{inputs,expected}/<filename>/page-NN.png
        audit/<unit>/render_index.json

Must run under the workspace venv, which carries PyMuPDF:
    <repo>/.venv/bin/python render_files.py <audit_unit_dir>

Honesty rule, carried over from the reference evals: when the renderer for a
format is missing, the entry is `visual_verifiable: false` and the component
must report that file's layout asks UNVERIFIABLE. A missing renderer is never
evidence of a defect in the submission.

Parity rule: converting a DOCX to pages is a LAYOUT decision and must be made
by the same application the CUA VM runs (see cua-applications.csv).
Rasterising an existing PDF is not — the layout is already fixed in the file —
so any rasteriser will do. Each entry carries the `parity` verdict for the
tool that decided its layout.

Usage:
    python3 render_files.py <audit_unit_dir> [--page-cap N] [--dpi N]
    python3 render_files.py --tools            # probe this machine, render nothing
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_common as ac  # noqa: E402
import render_common as rc  # noqa: E402

PAGE_CAP_DEFAULT = 1000        # rendered pages per unit, across both sides
MIN_PAGES_PER_FILE = 4
DPI_DEFAULT = 150
TIMEOUT = 300
PROVISIONER = Path(__file__).resolve().parent / "provision_renderers.py"

# Which tool decides the LAYOUT of each kind. `None` means the layout was
# already fixed before we saw the file, so no parity target applies.
LAYOUT_TOOL = {"office": "soffice", "html": "chrome",
               "blender": "blender", "media": "ffmpeg"}

DPI = DPI_DEFAULT


# ---------------------------------------------------------------- renderers
def render_pdf(pdf: Path, out_dir: Path, max_pages: int) -> dict:
    """PyMuPDF first (a venv wheel, no system package), then poppler, then Quick Look."""
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        import fitz
    except ImportError:
        fitz = None

    if fitz is not None:
        try:
            doc = fitz.open(str(pdf))
            total = doc.page_count
            text_path = out_dir / "text.txt"
            text_path.write_text(
                "\n\n".join(f"--- page {i + 1} ---\n{doc[i].get_text()}"
                            for i in range(total)), encoding="utf-8")
            pages = []
            for i in range(min(total, max_pages)):
                img = out_dir / f"page-{i + 1:02d}.png"
                doc[i].get_pixmap(dpi=DPI).save(str(img))
                pages.append(img.name)
            doc.close()
            return {"status": "full", "mode": "pymupdf", "visual_verifiable": True,
                    "pages": pages, "pages_rendered": len(pages),
                    "page_count": total, "page_cap": max_pages,
                    "truncated": total > len(pages), "text": text_path.name,
                    "renderer": f"PyMuPDF {getattr(fitz, '__version__', '?')}"}
        except Exception as exc:                                # noqa: BLE001
            print(f"    pymupdf failed on {pdf.name}: {exc}", file=sys.stderr)

    text_path = None
    if rc.which("pdftotext"):
        text_path = out_dir / "text.txt"
        code, _, _ = rc.run([rc.which("pdftotext"), "-layout", str(pdf), str(text_path)],
                            timeout=TIMEOUT)
        if code != 0:
            text_path = None

    if rc.which("pdftoppm"):
        code, _, err = rc.run([rc.which("pdftoppm"), "-png", "-r", str(DPI),
                               "-l", str(max_pages), str(pdf), str(out_dir / "page")],
                              timeout=TIMEOUT)
        pages = sorted(p.name for p in out_dir.glob("page*.png"))
        if pages:
            return {"status": "full", "mode": "pdftoppm", "visual_verifiable": True,
                    "pages": pages, "pages_rendered": len(pages),
                    "page_cap": max_pages, "truncated": len(pages) >= max_pages,
                    "text": text_path.name if text_path else None,
                    "renderer": rc.tool_version("pdftoppm")}
        return {"status": "unavailable", "mode": "pdftoppm-failed",
                "visual_verifiable": False, "pages": [],
                "text": text_path.name if text_path else None,
                "error": err.strip()[:300],
                "unverifiable_reason": "pdftoppm produced no pages"}

    return _quicklook(pdf, out_dir, text_path,
                      f"no PDF rasteriser ({rc.install_hint('pymupdf')})")


def render_office(src: Path, out_dir: Path, max_pages: int) -> dict:
    """LibreOffice is the parity renderer: the CUA Ubuntu VM's office suite."""
    out_dir.mkdir(parents=True, exist_ok=True)
    soffice = rc.which("soffice")
    if not soffice:
        return _quicklook(
            src, out_dir, None,
            f"LibreOffice is not installed ({rc.install_hint('soffice')}); it is "
            f"the parity renderer for these Ubuntu-only tasks")

    profile = (rc.tool_spec("soffice").get("wrapper") or {}).get("prepend_args") or []
    rc.STATE_DIR.mkdir(parents=True, exist_ok=True)
    prepend = [a.replace("{state}", str(rc.STATE_DIR)) for a in profile]

    with tempfile.TemporaryDirectory() as tmp:
        code, _, err = rc.run([soffice, *prepend, "--headless", "--convert-to", "pdf",
                               "--outdir", tmp, str(src)], timeout=TIMEOUT)
        produced = list(Path(tmp).glob("*.pdf"))
        if code != 0 or not produced:
            return {"status": "unavailable", "mode": "soffice-failed",
                    "visual_verifiable": False, "pages": [],
                    "error": (err or "no pdf produced").strip()[:300],
                    "unverifiable_reason": "LibreOffice could not convert this file"}
        staged = out_dir / "converted.pdf"
        shutil.copy2(produced[0], staged)

    result = render_pdf(staged, out_dir, max_pages)
    result["mode"] = f"soffice->{result.get('mode')}"
    result["converted_pdf"] = staged.name
    result["renderer"] = f"{rc.tool_version('soffice')} -> {result.get('renderer')}"
    return result


def render_html(src: Path, out_dir: Path) -> dict:
    """HTML has real layout. Screenshot it with headless Chrome."""
    out_dir.mkdir(parents=True, exist_ok=True)
    chrome = rc.which("chrome")
    if not chrome:
        return {"status": "unavailable", "mode": "none", "visual_verifiable": False,
                "pages": [], "read_directly": str(src),
                "unverifiable_reason": f"no Chrome/Chromium found "
                                       f"({rc.install_hint('chrome')}), so this file's "
                                       f"rendered appearance is UNVERIFIABLE. Its "
                                       f"markup is still readable as text."}
    shot = out_dir / "page-01.png"
    extra = (rc.format_spec("html").get("extra_args") or {}).get(rc.platform_key()) or []
    _, _, err = rc.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                        *extra, f"--screenshot={shot}", "--window-size=1440,2400",
                        "--default-background-color=FFFFFFFF",
                        src.resolve().as_uri()], timeout=120)
    if not shot.exists():
        return {"status": "unavailable", "mode": "chrome-failed",
                "visual_verifiable": False, "pages": [], "read_directly": str(src),
                "error": (err or "").strip()[:300],
                "unverifiable_reason": "Chrome could not screenshot this file"}
    return {"status": "full", "mode": "chrome", "visual_verifiable": True,
            "pages": [shot.name], "pages_rendered": 1, "read_directly": str(src),
            "renderer": rc.tool_version("chrome"),
            "note": "Viewport screenshot at 1440x2400. Content below that height is "
                    "not captured — treat page-length asks as UNVERIFIABLE."}


def _quicklook(src: Path, out_dir: Path, text_path: Path | None, why: str) -> dict:
    """macOS Quick Look gives page/slide 1 only. Enough to see, not to judge."""
    out_dir.mkdir(parents=True, exist_ok=True)
    ql = rc.which("qlmanage")
    if not ql:
        return {"status": "unavailable", "mode": "none", "visual_verifiable": False,
                "pages": [], "text": text_path.name if text_path else None,
                "unverifiable_reason": why}
    _, _, err = rc.run([ql, "-t", "-s", "1600", "-o", str(out_dir), str(src)],
                       timeout=TIMEOUT)
    thumb = next(iter(sorted(out_dir.glob("*.png"))), None)
    if thumb is None:
        return {"status": "unavailable", "mode": "qlmanage-failed",
                "visual_verifiable": False, "pages": [],
                "text": text_path.name if text_path else None,
                "error": err.strip()[:300], "unverifiable_reason": why}
    page1 = out_dir / "page-01.png"
    if thumb != page1:
        thumb.replace(page1)
    return {
        "status": "degraded", "mode": "qlmanage", "visual_verifiable": False,
        "pages": [page1.name], "pages_rendered": 1, "truncated": True,
        "text": text_path.name if text_path else None,
        "renderer": "qlmanage (macOS Quick Look)",
        "unverifiable_reason":
            f"{why}. Only page/slide 1 was rendered, by a previewer that is not the "
            f"VM's application — asks about any later page, about total page count, "
            f"and about exact layout are UNVERIFIABLE.",
    }


def inspect_archive(src: Path, out_dir: Path) -> dict:
    unzip = rc.which("unzip")
    if not unzip:
        return {"status": "unavailable", "mode": "none", "visual_verifiable": False,
                "pages": [], "unverifiable_reason": "unzip not available"}
    out_dir.mkdir(parents=True, exist_ok=True)
    code_t, out_t, err_t = rc.run([unzip, "-t", str(src)], timeout=TIMEOUT)
    _, out_l, _ = rc.run([unzip, "-l", str(src)], timeout=TIMEOUT)
    listing = [ln for ln in out_l.splitlines()
               if ln.strip() and "__MACOSX" not in ln and ".DS_Store" not in ln]
    return {"status": "full" if code_t == 0 else "corrupt", "mode": "unzip",
            "visual_verifiable": False, "pages": [],
            "integrity_ok": code_t == 0,
            "integrity_error": (err_t or out_t).strip()[:300] if code_t != 0 else None,
            "listing": listing[-40:], "renderer": "unzip"}


def render_recipe(src: Path, out_dir: Path, max_pages: int, spec: dict) -> dict:
    """A format whose renderer is declared in renderers.json rather than coded here.

    Two shapes cover everything so far: `via: pdf` converts and hands off to
    the PDF renderer, `via: png` writes page images directly.
    """
    recipe = spec["render"]
    tool = recipe.get("tool") or recipe["cmd"][0]
    if src.suffix.lower() in (recipe.get("skip_exts") or []):
        return {"status": "unavailable", "mode": "none", "visual_verifiable": False,
                "pages": [], "read_directly": str(src),
                "unverifiable_reason": recipe.get("skip_note")
                or f"{src.suffix} carries no visual layout"}
    exe = rc.which(tool)
    if not exe:
        return {"status": "unavailable", "mode": "none", "visual_verifiable": False,
                "pages": [],
                "unverifiable_reason": f"{tool} not installed ({rc.install_hint(tool)})"}

    out_dir.mkdir(parents=True, exist_ok=True)
    fill = {"src": str(src), "out": str(out_dir),
            "max_pages": str(max_pages), "dpi": str(DPI)}
    cmd = [exe] + [_fill(arg, fill) for arg in recipe["cmd"][1:]]
    code, _, err = rc.run(cmd, timeout=TIMEOUT)

    if recipe.get("via") == "pdf":
        pdf = out_dir / "converted.pdf"
        if code != 0 or not pdf.exists():
            return {"status": "unavailable", "mode": f"{tool}-failed",
                    "visual_verifiable": False, "pages": [],
                    "error": (err or "no pdf produced").strip()[:300],
                    "unverifiable_reason": f"{tool} could not convert this file"}
        result = render_pdf(pdf, out_dir, max_pages)
        result["mode"] = f"{tool}->{result.get('mode')}"
        result["converted_pdf"] = pdf.name
        result["renderer"] = f"{rc.tool_version(tool)} -> {result.get('renderer')}"
        if recipe.get("note"):
            result["note"] = recipe["note"]
        return result

    pages = sorted(p.name for p in out_dir.glob("page*.png"))
    if not pages:
        return {"status": "unavailable", "mode": f"{tool}-failed",
                "visual_verifiable": False, "pages": [],
                "error": (err or "no page images produced").strip()[:300],
                "unverifiable_reason": f"{tool} produced no page images from this file"}
    return {"status": "full", "mode": tool, "visual_verifiable": True,
            "pages": pages[:max_pages], "pages_rendered": min(len(pages), max_pages),
            "truncated": len(pages) > max_pages,
            "renderer": rc.tool_version(tool), "note": recipe.get("note")}


def _fill(arg: str, values: dict) -> str:
    for key, value in values.items():
        arg = arg.replace("{" + key + "}", value)
    return arg


# ---------------------------------------------------------------- per file
def render_file(src: Path, out_root: Path, max_pages: int, rel: Path) -> dict:
    """Render one file. `rel` is its path within the side, so a nested
    `sub/report.pdf` renders to `render/<side>/sub/report.pdf/` and cannot
    collide with a `report.pdf` staged at the top level."""
    kind = rc.kind_for(src)
    spec = rc.format_spec(kind)
    out_dir = out_root / rel
    magic = rc.sniff_magic(src)
    base = {"name": src.name, "path": str(rel), "kind": kind,
            "source": str(src),
            "bytes": src.stat().st_size if src.exists() else None,
            "magic": magic}
    if rc.ext_matches_magic(src.name, magic) is False:
        base["ext_magic_mismatch"] = (
            f"the extension says {src.suffix} but the bytes are {magic} — a page "
            f"rendered from this file is not evidence that the file is a valid "
            f"{src.suffix.lstrip('.')}")

    if kind == "pdf":
        r = render_pdf(src, out_dir, max_pages)
    elif kind == "office":
        r = render_office(src, out_dir, max_pages)
    elif kind == "html":
        r = render_html(src, out_dir)
    elif kind == "archive":
        r = inspect_archive(src, out_dir)
    elif kind == "image":
        r = {"status": "full", "mode": "native", "visual_verifiable": True,
             "pages": [src.name], "pages_rendered": 1, "read_directly": str(src),
             "renderer": "read-tool-native",
             "note": "Already an image — open the original, it needs no render."}
    elif kind == "text" or (kind == "unknown" and magic in ("text", "empty")):
        # An extensionless or oddly-named file whose bytes are text is text.
        # Calling it unrenderable would imply a layout nobody can see.
        r = {"status": "full", "mode": "native", "visual_verifiable": False,
             "pages": [], "read_directly": str(src), "renderer": "plain-text",
             "note": "Plain text has no visual layout — read it as text."}
    elif spec.get("render"):
        r = render_recipe(src, out_dir, max_pages, spec)
    else:
        r = {"status": "unavailable", "mode": "none", "visual_verifiable": False,
             "pages": [], "unverifiable_reason":
             f"no renderer for extension {src.suffix or '(none)'}"}

    layout_tool = LAYOUT_TOOL.get(kind)
    if layout_tool and r.get("visual_verifiable"):
        p = rc.probe(layout_tool)
        r["layout_tool"] = layout_tool
        r["parity"] = p.get("parity")
        if p.get("parity_gap"):
            r["parity_gap"] = p["parity_gap"]
    elif r.get("visual_verifiable"):
        r["parity"] = "n/a"
        r["parity_note"] = ("the layout was fixed in the file before we saw it; "
                            "rasterising it is faithful whatever the rasteriser")

    if r.get("pages") and r.get("mode") != "native":
        r["page_dir"] = str(out_dir)
    return {**base, **r}


def _renderable(files: list[Path]) -> int:
    return sum(1 for f in files if rc.is_paged(rc.kind_for(f)))


def _staged(side_dir: Path) -> list[Path]:
    """Every staged file, minus dotfiles and the tool caches that ride along.

    `.pytest_cache/` and friends arrive inside an inputs archive and are not
    part of the submission; rendering them only adds noise to the index.
    """
    if not side_dir.is_dir():
        return []
    return sorted(p for p in side_dir.rglob("*")
                  if p.is_file()
                  and not any(part.startswith(".")
                              for part in p.relative_to(side_dir).parts))


def unit_needs(unit_dir: Path) -> dict:
    """What must be installed for THIS unit's files to render faithfully.

    Scoped to the unit rather than the machine on purpose: a host with no
    ffmpeg is fully equipped for a unit whose deliverables are a workbook and
    a deck, and telling an operator to install a video renderer they do not
    need is how a preflight gets ignored.
    """
    kinds = set()
    for side in ("inputs", "expected"):
        for f in _staged(unit_dir / "files" / side):
            kind = rc.kind_for(f)
            if rc.is_paged(kind):
                kinds.add(kind)
    out = rc.needs(kinds)
    out["kinds"] = sorted(kinds)
    out["install_commands"] = rc.install_commands(
        out["install"] + out["off_version"], script=str(PROVISIONER))
    return out


def render_unit(unit_dir: Path, page_cap: int = PAGE_CAP_DEFAULT) -> dict:
    """Render both sides of one audit unit and write render_index.json."""
    roots = {side: unit_dir / "files" / side for side in ("inputs", "expected")}
    sides = {side: _staged(root) for side, root in roots.items()}

    total_renderable = sum(_renderable(f) for f in sides.values())
    per_file = (max(MIN_PAGES_PER_FILE, page_cap // total_renderable)
                if total_renderable else page_cap)

    index = {
        "unit": unit_dir.name,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dpi": DPI,
        "page_cap": page_cap,
        "pages_per_file_cap": per_file,
        "applications_csv": str(rc.APPLICATIONS_CSV),
        "needs": unit_needs(unit_dir),
        "tools": rc.probe_all(),
    }
    for side, files in sides.items():
        index[side] = [render_file(f, unit_dir / "render" / side, per_file,
                                   f.relative_to(roots[side])) for f in files]

    # Only warn about the tools this unit actually leaned on: a Chrome version
    # gap is noise for a unit with no HTML in it. Fonts ride with LibreOffice.
    entries = index["inputs"] + index["expected"]
    used = {e["layout_tool"] for e in entries if e.get("layout_tool")}
    if "soffice" in used:
        used.add("fonts-parity")
    gaps = sorted({index["tools"][t]["parity_gap"] for t in used
                   if index["tools"].get(t, {}).get("parity_gap")})
    index["parity_warnings"] = gaps
    index["summary"] = {
        "files": len(entries),
        "visual_verifiable": sum(1 for e in entries if e.get("visual_verifiable")),
        "degraded": sum(1 for e in entries if e.get("status") == "degraded"),
        "unavailable": sum(1 for e in entries if e.get("status") == "unavailable"),
        "pages_rendered": sum(e.get("pages_rendered") or 0 for e in entries),
        "parity_ok": not gaps,
    }
    (unit_dir / "render_index.json").write_text(
        ac.dumps(index, indent=2) + "\n", encoding="utf-8")
    return index


def main() -> int:
    global DPI
    ap = argparse.ArgumentParser()
    ap.add_argument("unit_dir", nargs="?", help="audit/<unit_id> directory")
    ap.add_argument("--page-cap", type=int, default=PAGE_CAP_DEFAULT)
    ap.add_argument("--dpi", type=int, default=DPI_DEFAULT)
    ap.add_argument("--tools", action="store_true",
                    help="probe this machine against cua-applications.csv, render nothing")
    ap.add_argument("--needed", action="store_true",
                    help="print the tools this unit needs installed, one per line, "
                         "and render nothing")
    a = ap.parse_args()

    if a.tools:
        return rc.main()
    if not a.unit_dir:
        ap.error("give an audit/<unit_id> directory, or --tools")

    if a.needed:
        n = unit_needs(Path(a.unit_dir).resolve())
        for tool in n["install"] + n["off_version"]:
            print(tool)
        return 0

    DPI = a.dpi
    unit = Path(a.unit_dir).resolve()
    if not unit.is_dir():
        print(f"{unit}: not a directory")
        return 2
    if unit.parent == ac.AUDIT.resolve():
        why = ac.locked(unit.name, "render_files.py")
        if why:
            print(why)
            return 3

    index = render_unit(unit, a.page_cap)
    s = index["summary"]
    print(f"  rendered {s['pages_rendered']} page(s) from {s['files']} file(s): "
          f"{s['visual_verifiable']} visual-verifiable, {s['degraded']} degraded, "
          f"{s['unavailable']} unavailable")
    for side in ("inputs", "expected"):
        for e in index[side]:
            if e.get("status") not in ("full", None) or not e.get("visual_verifiable"):
                if e["kind"] in ("text", "archive"):
                    continue
                print(f"    {e['status']:<11} {side}/{e['path']}: "
                      f"{(e.get('unverifiable_reason') or '')[:88]}")
    for w in index["parity_warnings"]:
        print(f"    parity: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
