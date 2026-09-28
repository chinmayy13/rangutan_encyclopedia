#!/usr/bin/env python3
"""Renderer registry, tool discovery, and VM parity.

Two data files drive everything here and nothing is hard-coded:

    renderers.json        which tool each format needs, how to probe it, how to
                          install it, and which VM application it stands in for
    cua-applications.csv  the CUA Ubuntu VM's application list — the parity
                          target, because a file laid out by a different build
                          paginates differently, and pagination is exactly what
                          the visual rubric criteria grade

Parity applies to the tool that decides LAYOUT (the office suite, the browser,
the 3D renderer, the fonts). A rasteriser turns an already-laid-out PDF into
pixels and has no VM counterpart, so it is never a parity target.
"""
from __future__ import annotations

import csv
import os
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_common as ac  # noqa: E402

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parents[1]

RENDERERS_FILE = HERE / "renderers.json"
APPLICATIONS_CSV = Path(os.environ.get("CUA_APPLICATIONS_CSV")
                        or BUNDLE / "cua-applications.csv")

# Where provision_renderers.py installs pinned builds. Everything lands under
# $HOME so provisioning never needs root and never disturbs an application the
# operator installed for themselves.
TOOLS_ROOT = Path(os.environ.get("CUA_RENDER_TOOLS")
                  or Path.home() / ".cua-renderers").expanduser()
APPS_DIR = TOOLS_ROOT / "apps"
STATE_DIR = TOOLS_ROOT / "state"       # writable profile for LibreOffice
PROVISION_FILE = TOOLS_ROOT / "provision.json"

PROBE_TIMEOUT = 30


# ---------------------------------------------------------------- the registry
_REGISTRY: dict | None = None


def registry() -> dict:
    """renderers.json, or {} when it is missing or unreadable.

    Empty is a working state, not an error: every consumer then reports its
    formats unavailable, which is the honest outcome rather than a broken run.
    """
    global _REGISTRY
    if _REGISTRY is None:
        import json
        try:
            _REGISTRY = json.loads(RENDERERS_FILE.read_text(encoding="utf-8"))
        except Exception:                                       # noqa: BLE001
            _REGISTRY = {}
    return _REGISTRY


def tool_spec(tool: str) -> dict:
    return (registry().get("tools") or {}).get(tool) or {}


def format_spec(kind: str) -> dict:
    return (registry().get("formats") or {}).get(kind) or {}


def platform_key() -> str:
    if sys.platform == "darwin":
        return "darwin"
    return "linux" if sys.platform.startswith("linux") else "default"


def install_hint(tool: str) -> str:
    hint = tool_spec(tool).get("hint") or {}
    if isinstance(hint, str):
        return hint
    return hint.get(platform_key()) or hint.get("default") or f"install {tool}"


# ---------------------------------------------------------------- file typing
KIND_BY_EXT = {
    ".pdf": "pdf",
    ".docx": "office", ".doc": "office", ".rtf": "office",
    ".pptx": "office", ".ppt": "office",
    ".xlsx": "office", ".xls": "office", ".xlsm": "office",
    ".odt": "office", ".odp": "office", ".ods": "office",
    ".png": "image", ".jpg": "image", ".jpeg": "image",
    ".gif": "image", ".webp": "image", ".bmp": "image",
    ".zip": "archive",
    ".csv": "text", ".tsv": "text", ".md": "text", ".txt": "text",
    ".py": "text", ".js": "text", ".json": "text", ".xml": "text",
    ".yaml": "text", ".yml": "text", ".sql": "text", ".sh": "text",
    ".r": "text", ".rmd": "text", ".tex": "text", ".log": "text",
    ".ipynb": "text",
    ".html": "html", ".htm": "html", ".svg": "html",
    ".mp4": "media", ".mov": "media", ".avi": "media", ".webm": "media",
    ".mkv": "media", ".mp3": "media", ".wav": "media", ".m4a": "media",
    ".blend": "blender",
}

# A format declaring `exts` in the registry claims them, so a new file type
# becomes renderable by editing JSON rather than this table.
for _kind, _spec in (registry().get("formats") or {}).items():
    for _ext in _spec.get("exts") or []:
        KIND_BY_EXT[_ext.lower()] = _kind


def kind_for(name: str | Path) -> str:
    return KIND_BY_EXT.get(Path(name).suffix.lower(), "unknown")


# Magic-byte signatures, containers last so OOXML resolves as the zip it is.
MAGIC = [
    (b"%PDF-", "pdf"),
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"\xff\xd8\xff", "jpeg"),
    (b"GIF87a", "gif"), (b"GIF89a", "gif"),
    (b"RIFF", "riff"),
    (b"BLENDER", "blend"),
    (b"PK\x03\x04", "zip"),          # also docx/pptx/xlsx: OOXML is a zip
    (b"\xd0\xcf\x11\xe0", "ole2"),   # legacy doc/xls/ppt
    (b"\x1f\x8b", "gzip"),
]

# What the bytes must be for a given extension. Anything absent has no rule.
MAGIC_OK = {
    ".pdf": {"pdf"},
    ".png": {"png"}, ".jpg": {"jpeg"}, ".jpeg": {"jpeg"}, ".gif": {"gif"},
    ".webp": {"riff"},
    ".docx": {"zip"}, ".pptx": {"zip"}, ".xlsx": {"zip"}, ".xlsm": {"zip"},
    ".odt": {"zip"}, ".ods": {"zip"}, ".odp": {"zip"}, ".zip": {"zip"},
    ".doc": {"ole2"}, ".xls": {"ole2"}, ".ppt": {"ole2"},
    ".blend": {"blend", "gzip"},
}


def sniff_magic(path: Path) -> str:
    """A magic-byte type, or 'text' / 'empty' / 'unknown' / 'unreadable'."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(16)
    except OSError:
        return "unreadable"
    if not head:
        return "empty"
    for sig, name in MAGIC:
        if head.startswith(sig):
            return name
    printable = sum(1 for b in head if 9 <= b <= 13 or 32 <= b <= 126)
    return "text" if printable >= len(head) - 1 else "unknown"


def ext_matches_magic(name: str | Path, magic: str) -> bool | None:
    """True/False where there is a rule for the extension, else None.

    Worth recording next to a render: LibreOffice will cheerfully import a
    text file named `.docx` and produce a page from it, so a render that
    succeeded is not on its own proof that the file is the format it claims.
    """
    ext = Path(name).suffix.lower()
    if ext in MAGIC_OK:
        return magic in MAGIC_OK[ext]
    if KIND_BY_EXT.get(ext) in ("text", "html"):
        return magic in ("text", "empty")
    return None


def is_paged(kind: str) -> bool:
    """Kinds that can yield more than one page, so the page budget is split."""
    return kind in ("pdf", "office", "html") or bool(format_spec(kind).get("render"))


# ---------------------------------------------------------------- tool lookup
def tool_bins(tool: str) -> list[str]:
    return list(tool_spec(tool).get("bins") or [tool])


def _candidates(tool: str) -> list[str]:
    """Absolute paths the registry declares for this tool, globs expanded.

    A pinned build we provisioned is searched BEFORE the system one: parity is
    the point of installing it, so it must win over whatever else is around.
    """
    spec = tool_spec(tool)
    out: list[str] = []
    for pattern in [*(spec.get("provisioned_paths") or []), *(spec.get("paths") or [])]:
        pattern = pattern.replace("{tools}", str(TOOLS_ROOT))
        out.extend(sorted(str(p) for p in Path("/").glob(pattern.lstrip("/")))
                   if any(c in pattern for c in "*?[") else [pattern])
    return out


@lru_cache(maxsize=None)
def which(tool: str) -> str | None:
    """Provisioned build first, then PATH, then the app bundles.

    A GUI app installed from a .dmg is not on PATH; without that last pass a
    working LibreOffice reads as missing.
    """
    from shutil import which as _which
    for candidate in _candidates(tool):
        if Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return candidate
    for name in tool_bins(tool):
        found = _which(name)
        if found:
            return found
    return None


def run(cmd: list[str], timeout: int = PROBE_TIMEOUT):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s"
    except OSError as exc:
        return 127, "", str(exc)


def _reader_venv_version(module: str) -> str | None:
    """Ask the reader venv, which is where a wheel renderer is installed.

    audit_prepare.py probes under the system interpreter but extracts and
    renders under the venv. Probing only this process would report a working
    PyMuPDF as missing, reinstall it on every run, and then call the install
    a failure — an installation problem invented by the probe.
    """
    if not ac.VENV_PY.is_file():
        return None
    code, out, _ = run([str(ac.VENV_PY), "-c",
                        f"import {module} as m; "
                        f"print(getattr(m, '__version__', '?'))"])
    return f"{module} {out.strip()}" if code == 0 else None


@lru_cache(maxsize=None)
def tool_version(tool: str) -> str | None:
    """The tool's own version banner, first line, or None when absent.

    Cached: a unit with seventeen office files must not shell out to
    `soffice --version` seventeen times. `forget_tools()` after installing.
    """
    spec = tool_spec(tool)
    if spec.get("probe") == "python":
        module = spec.get("module") or tool
        try:
            mod = __import__(module)
        except ImportError:
            return _reader_venv_version(module)
        return f"{module} {getattr(mod, '__version__', '?')}"
    exe = which(tool)
    if not exe:
        return None
    args = spec.get("version_args")
    if args is None:
        return "present"
    _, out, err = run([exe, *args])
    text = (out or err).strip()
    return text.splitlines()[0][:120] if text else "present"


def font_roots() -> list[Path]:
    """Font directories worth searching, including LibreOffice's own.

    LibreOffice ships Carlito, Caladea, Liberation and DejaVu inside its
    installation and uses them whether or not the OS has registered them, so
    its bundle counts: install the pinned suite and font parity comes with it.
    """
    roots = [Path("/Library/Fonts"), Path("/System/Library/Fonts"),
             Path.home() / "Library" / "Fonts",
             Path("/usr/share/fonts"), Path.home() / ".fonts"]
    soffice = which("soffice")
    if soffice:
        home = Path(soffice).resolve().parent.parent      # .../Contents or .../libreoffice
        roots += [home / "Resources" / "fonts", home / "share" / "fonts"]
    return roots


def installed_fonts() -> list[str]:
    """Font family names visible on this machine, best effort.

    fc-list where it exists, else the font directories. Best effort is the
    right standard here: a font we cannot see is reported as a parity gap to
    be checked, never as proof that the file itself is wrong.
    """
    names: set[str] = set()
    if which("fc-list"):
        _, out, _ = run(["fc-list", ":", "family"])
        for line in out.splitlines():
            for fam in line.split(","):
                if fam.strip():
                    names.add(fam.strip())
    for root in font_roots():
        if root.is_dir():
            for f in root.rglob("*"):
                if f.suffix.lower() in (".ttf", ".otf", ".ttc"):
                    names.add(f.stem)
    return sorted(names)


# ---------------------------------------------- the VM application list (CSV)
_APPS: list[dict] | None = None


def applications() -> list[dict]:
    """cua-applications.csv as a list of rows, or [] when it is not there."""
    global _APPS
    if _APPS is None:
        try:
            with APPLICATIONS_CSV.open(encoding="utf-8") as fh:
                _APPS = [r for r in csv.DictReader(fh) if (r.get("name") or "").strip()]
        except Exception:                                       # noqa: BLE001
            _APPS = []
    return _APPS


def application(name: str) -> dict | None:
    for row in applications():
        if (row.get("name") or "").strip() == name:
            return row
    return None


_VERSION = re.compile(r"(\d+(?:\.\d+)+)")


def normalise_version(text: str | None) -> str | None:
    """The first dotted numeric run in a version string.

    Both sides need this. The CSV writes `7.3.7.2 (1:7.3.7-0ubuntu0.22.04.12)`
    and LibreOffice answers `LibreOffice 7.3.7.2 30(Build:2)`; the comparable
    part is `7.3.7.2`.
    """
    m = _VERSION.search(text or "")
    return m.group(1) if m else None


def _series(version: str | None, depth: int = 2) -> str | None:
    return ".".join(version.split(".")[:depth]) if version else None


def compare_versions(pinned: str | None, found: str | None) -> str:
    """exact | compatible | mismatch | unknown.

    `compatible` means the same major.minor series. LibreOffice 7.3.7.2 and
    7.3.7.1 lay a document out identically; 7.3 and 25.2 do not.
    """
    p, f = normalise_version(pinned), normalise_version(found)
    if not p or not f:
        return "unknown"
    if p == f:
        return "exact"
    return "compatible" if _series(p) == _series(f) else "mismatch"


def forget_tools() -> None:
    """Drop the discovery caches. Call after installing something."""
    which.cache_clear()
    tool_version.cache_clear()
    probe.cache_clear()


@lru_cache(maxsize=None)
def probe(tool: str) -> dict:
    """One tool: is it here, which version, and does it match the VM's build."""
    spec = tool_spec(tool)
    found = tool_version(tool)
    rec = {
        "tool": tool,
        "present": found is not None,
        "path": which(tool),
        "found_version": found,
        "unlocks": spec.get("unlocks"),
        "hint": install_hint(tool),
    }

    if spec.get("probe") == "fonts":
        have = installed_fonts()
        wanted = spec.get("fonts") or []
        missing = [w for w in wanted
                   if not any(w.lower() in h.lower() for h in have)]
        rec.update(present=not missing,
                   found_version=f"{len(wanted) - len(missing)}/{len(wanted)} "
                                 f"families present",
                   fonts_required=wanted, fonts_missing=missing,
                   parity="exact" if not missing else "mismatch",
                   parity_note=spec.get("parity_note"))
        if missing:
            rec["parity_gap"] = (
                f"missing font families {', '.join(missing)} — an office file "
                f"using them reflows, so pagination is not the contributor's")
        return rec

    app_name = spec.get("parity_app")
    if not app_name:
        rec["parity"] = "n/a"
        return rec

    row = application(app_name) or {}
    pinned = (row.get("version") or "").strip() or None
    rec.update(parity_app=app_name, pinned_version=pinned,
               parity=compare_versions(pinned, found) if found else "unknown",
               parity_note=spec.get("parity_note"))
    if rec["parity"] == "mismatch":
        rec["parity_gap"] = (
            f"the VM runs {app_name} {normalise_version(pinned)}, this machine has "
            f"{normalise_version(found)} — layout and pagination may differ")
    return rec


def probe_all(tools: list[str] | None = None) -> dict[str, dict]:
    """Every tool probed, as copies — `probe` is cached, callers may edit."""
    names = tools if tools is not None else sorted((registry().get("tools") or {}))
    return {t: dict(probe(t)) for t in names}


def tools_for(kind: str) -> tuple[list[str], list[str]]:
    """(hard requirements, interchangeable set) for a format kind."""
    spec = format_spec(kind)
    return list(spec.get("requires") or []), list(spec.get("one_of") or [])


def kind_satisfied(kind: str) -> tuple[bool, list[str]]:
    """Can this format render faithfully here, and if not, what to install.

    Faithful means the render is the file's real layout. The degraded
    fallbacks never count: a Quick Look thumbnail of slide 1 is not a render
    of a deck, which is why a missing tool has to be reported as something to
    install rather than absorbed silently.
    """
    required, interchangeable = tools_for(kind)
    missing = [t for t in required if not probe(t)["present"]]
    if interchangeable and not any(probe(t)["present"] for t in interchangeable):
        missing.append(interchangeable[0])   # the cheapest of an equal set
    return not missing, missing


def needs(kinds) -> dict:
    """What this host must install before these formats render faithfully.

    Two separate answers, because they are different problems. `install` is
    "there is no renderer at all" — the pages would not exist. `off_version`
    is "the renderer is here but is not the build the CUA VM runs" — the pages
    exist and are worth looking at, but their pagination is this host's, so
    reflow-dependent findings have to be blocked instead of scored.
    """
    by_kind, install, off = {}, [], []
    for kind in sorted(set(kinds)):
        ok, missing = kind_satisfied(kind)
        by_kind[kind] = {"ok": ok, "missing": missing}
        install += missing
        for tool in tools_for(kind)[0]:
            p = probe(tool)
            if p["present"] and p.get("parity") == "mismatch":
                off.append(tool)
    return {"by_kind": by_kind, "install": sorted(set(install)),
            "off_version": sorted(set(off))}


def install_commands(tools: list[str], script: str = "provision_renderers.py") -> list[str]:
    """One command per tool, preferring this bundle's provisioner.

    A tool the provisioner can install at the pinned version is named as such;
    anything else falls back to the platform hint from the registry, so the
    answer is never "install it somehow".
    """
    out = []
    for tool in tools:
        if tool_spec(tool).get("acquire"):
            out.append(f"python3 {script} {tool} --install")
        else:
            out.append(install_hint(tool))
    return out


def main() -> int:
    """`python3 render_common.py` prints the parity report for this machine."""
    print(f"registry     {RENDERERS_FILE}")
    print(f"applications {APPLICATIONS_CSV} ({len(applications())} rows)\n")
    rows = probe_all()
    width = max(len(t) for t in rows) if rows else 8
    for tool, r in rows.items():
        mark = "ok " if r["present"] else "-- "
        ver = r.get("found_version") or "not installed"
        par = r.get("parity") or ""
        tail = f"  [parity {par}]" if par not in ("", "n/a") else ""
        print(f"  {mark}{tool:<{width}}  {ver[:60]}{tail}")
        if r.get("parity_gap"):
            print(f"      ! {r['parity_gap']}")
        if not r["present"]:
            print(f"      install: {r['hint']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
