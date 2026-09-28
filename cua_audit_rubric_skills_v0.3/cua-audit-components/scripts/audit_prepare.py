#!/usr/bin/env python3
"""Stage the evidence bundle every audit component reads.

Reads the task files supplied under tasks/<task_id>/ (or attempts/<attempt_id>/)
and writes, per unit, under audit/<unit_id>/:
    bundle.json             evidence index (incl. the mechanical pre-pass)
    prompt.md               the prompt as shipped
    rubric.json             the rubric criteria, verbatim
    task.md                 domain / sub_domain
    files/inputs/*          downloaded input files
    files/expected/*        downloaded expected files (the answer key)
    inputs_extracted.md     input files dumped to text
    expected_extracted.md   expected files dumped to text
    render/inputs/*         input files rasterised to page images
    render/expected/*       expected files rasterised to page images
    render_index.json       what rendered, with which application and version

Usage:
    python3 audit_prepare.py <task_id> [<task_id> ...]
    python3 audit_prepare.py --all              # every task under tasks/
    python3 audit_prepare.py <task_id> --provision   # install missing renderers first
    python3 audit_prepare.py <task_id> --no-files
    python3 audit_prepare.py <task_id> --no-render

Run it with `--provision` on a machine that has not audited an office or PDF
deliverable before: the renderers are installed at the versions pinned in
cua-applications.csv, which is what makes the rendered pagination the
contributor's rather than this host's.

The document readers are not a choice and are never asked about — the
workspace venv is created and stocked on first run (audit_common.reader_python),
so this step never stops for a wheel it could have installed itself.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_common as ac  # noqa: E402
import render_common as rc  # noqa: E402
import render_files as rf  # noqa: E402




def download(url: str, dest: Path) -> str:
    if dest.exists() and dest.stat().st_size > 0:
        return "cached"
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=90) as r:
            dest.write_bytes(r.read())
        return "ok"
    except Exception as e:                                   # noqa: BLE001
        return f"FAILED {type(e).__name__}"


def stage_files(bundle: dict, out: Path) -> dict:
    report = {"inputs": {}, "expected": {}}
    for kind, key, namer in (
        ("inputs", "input_files", lambda f: Path(f["path"]).name),
        ("expected", "expected_files", lambda f: f["dest"]),
    ):
        for f in bundle.get(key) or []:
            name = namer(f)
            if not name or not f.get("url", "").startswith("http"):
                continue
            report[kind][name] = download(f["url"], out / "files" / kind / name)
    return report


EXTRACTOR = Path(__file__).resolve().parent / "extract_files.py"
RENDERER = Path(__file__).resolve().parent / "render_files.py"
PROVISIONER = Path(__file__).resolve().parent / "provision_renderers.py"


def extract(python: Path, out: Path) -> dict:
    """Dump staged binaries to text so subagents never open Office files."""
    res = {}
    for kind in ("inputs", "expected"):
        src, dest = out / "files" / kind, out / f"{kind}_extracted.md"
        p = subprocess.run([str(python), str(EXTRACTOR), str(src), str(dest)],
                           capture_output=True, text=True, timeout=600)
        res[kind] = "ok" if p.returncode == 0 else f"FAILED {p.stderr[-200:]}"
    return res


def preflight(out: Path, provision: bool) -> dict:
    """Make sure the renderers this unit's files need are actually here.

    Rendering already degrades honestly when a tool is missing, but a degraded
    render costs a full review pass to discover: 28 model calls that report
    the deliverable's layout UNVERIFIABLE. Checking first, and naming the one
    command that fixes it, is the difference between "the eval ran" and "the
    eval ran and saw the artifacts".
    """
    needs = rf.unit_needs(out)
    if not (needs["install"] or needs["off_version"]):
        return needs

    what = ", ".join(needs["kinds"]) or "none"
    print(f"  renderers missing for this unit (file kinds: {what}):")
    for tool in needs["install"]:
        print(f"    {tool:<10} absent — {rc.tool_spec(tool).get('unlocks')}")
    for tool in needs["off_version"]:
        print(f"    {tool:<10} {rc.probe(tool).get('parity_gap')}")

    if not provision:
        print("  install them at the version the CUA VM runs, then re-run this:")
        print(f"    python3 {PROVISIONER} --for {out} --install")
        print(f"    python3 {Path(__file__).name} {out.name}")
        needs["provision_command"] = (
            f"python3 {PROVISIONER} --for {out} --install")
        return needs

    print(f"  installing at the pinned versions from {rc.APPLICATIONS_CSV.name} ...")
    p = subprocess.run([sys.executable, str(PROVISIONER), "--for", str(out),
                        "--install"], text=True, timeout=3600)
    rc.forget_tools()
    after = rf.unit_needs(out)
    after["provisioned"] = {"exit_code": p.returncode,
                            "before": needs["install"] + needs["off_version"],
                            "still_missing": after["install"] + after["off_version"]}
    return after


def render(python: Path, out: Path, provision: bool = False) -> dict:
    """Rasterise the staged files so appearance can be judged, not just content.

    The extraction above says what a file contains; this says what it looks
    like. Runs under the reader venv for PyMuPDF, and summarises
    render_index.json — the full per-file record, including which renderer
    produced each page and whether it matches the CUA VM's build, stays in
    that file.
    """
    needs = preflight(out, provision)
    p = subprocess.run([str(python), str(RENDERER), str(out)],
                       capture_output=True, text=True, timeout=1800)
    if p.returncode != 0:
        return {"status": f"FAILED {(p.stderr or p.stdout)[-300:]}"}
    index = out / "render_index.json"
    if not index.exists():
        return {"status": "FAILED no render_index.json"}
    idx = json.loads(index.read_text(encoding="utf-8"))
    return {"status": "ok", "index": index.name,
            **idx["summary"], "parity_warnings": idx["parity_warnings"],
            "needs": needs}


def write_views(tid: str, out: Path) -> list[str]:
    """The submission in readable form, beside bundle.json.

    prompt.md / rubric.json / task.md are the same three files a delivery
    folder ships, regenerated from the response on every run.
    """
    b, meta, _ = ac.load(tid)
    md = meta.get("metadata") or {}

    prompt = ((ac.step(b, "PromptInput") or {}).get("output") or {}).get("content") or ""
    (out / "prompt.md").write_text(prompt.strip() + "\n", encoding="utf-8")

    crits = ((ac.step(b, "RubricCriteriaBuilder") or {}).get("output") or {}).get("criteria") or []
    rubric = [{"id": c.get("id"),
               "title": c.get("title"),
               "weight": c.get("weight"),
               "annotations": {
                   "criteria_type": (c.get("annotations") or {}).get("criteria_type"),
                   "criteria_category": (c.get("annotations") or {}).get("criteria_category"),
               }} for c in crits]
    (out / "rubric.json").write_text(ac.dumps(rubric, indent=2) + "\n", encoding="utf-8")

    (out / "task.md").write_text(
        f"domain: {md.get('domain') or ''}\n"
        f"sub_domain: {md.get('sub_domain') or ''}\n", encoding="utf-8")

    return ["prompt.md", "rubric.json", "task.md"]




def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task_ids", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--no-files", action="store_true",
                    help="skip downloading input/expected files (file-class components will be blocked)")
    ap.add_argument("--no-render", action="store_true",
                    help="skip rasterising to PNG (visual findings will be UNVERIFIABLE)")
    ap.add_argument("--provision", action="store_true",
                    help="install any renderer this unit's files need, at the version "
                         "pinned in cua-applications.csv, before rendering")
    a = ap.parse_args()

    if not a.task_ids and not a.all:
        ap.error("give at least one task_id / attempt_id, or --all")
    ids = ac.admit(list(dict.fromkeys(a.task_ids)), "audit_prepare.py", named=True)
    if ids is None:
        return 3
    if a.all:
        ids += ac.admit([u for u in ac.all_units() if u not in ids],
                        "audit_prepare.py", named=False)
    if not ids:
        print("nothing to prepare")
        return 0

    # Before anything is staged: the readers. Nothing below should ever fail
    # for want of a wheel, because the review that follows cannot see a file
    # this step did not extract or render.
    python, pyrec = (Path(sys.executable), {"status": "skipped (--no-files)"}) \
        if a.no_files else ac.reader_python()
    if pyrec.get("created") or pyrec.get("installed"):
        print(f"  readers ready: {pyrec['python']}")
    if not pyrec["status"].startswith(("ok", "skipped")):
        print(f"  readers {pyrec['status']}")

    for tid in dict.fromkeys(ids):
        out = ac.AUDIT / tid
        out.mkdir(parents=True, exist_ok=True)
        try:
            bundle = ac.bundle_for(tid)
        except FileNotFoundError as e:
            print(f"  {e}")
            continue

        bundle["readers"] = pyrec
        if not a.no_files:
            bundle["staged_files"] = stage_files(bundle, out)
            bundle["extracted"] = extract(python, out)
            if not a.no_render:
                bundle["renders"] = render(python, out, a.provision)
        (out / "bundle.json").write_text(ac.dumps(bundle), encoding="utf-8")
        views = write_views(tid, out)

        mech = bundle["mechanical"]
        fails = [k for k, v in mech.items() if v["score"] == 2]
        minors = [k for k, v in mech.items() if v["score"] in (3, 4)]
        sf = bundle.get("staged_files") or {}
        nbad = sum(1 for d in sf.values() for v in d.values() if v.startswith("FAILED"))
        att = bundle.get("attempt") or {}
        tag = (f"attempt[{att.get('role')}] on {att.get('on_task')}"
               if att.get("is_attempt_unit") else "task")
        print(f"{tid} ({tag}): {len(bundle['criteria'])} criteria, "
              f"domain={bundle['domain']!r}, "
              f"mech fails={fails or '-'} minors={minors or '-'}, "
              f"files={sum(len(d) for d in sf.values())} ({nbad} failed), "
              f"wrote bundle.json + {', '.join(views)}")
        r = bundle.get("renders") or {}
        if r.get("status") == "ok":
            print(f"  render: {r['pages_rendered']} page(s), "
                  f"{r['visual_verifiable']} visual-verifiable, "
                  f"{r['degraded']} degraded, {r['unavailable']} unavailable"
                  + ("" if r["parity_ok"] else "  ⚠ renderer parity gap"))
            for w in r.get("parity_warnings") or []:
                print(f"    parity: {w}")
        elif r:
            print(f"  render: {r.get('status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
