#!/usr/bin/env python3
"""Run the 28-component audit-rubric review over one or more audit units.

One subagent call per component, per unit. Model is fixed per component by
`_generate.py` (files and rubric -> opus, other -> sonnet), always at
`--effort max`. The input-consistency pass (input_consistency.py) shares the
worker pool: each unit's call is queued behind that unit's component calls, so
it starts beside them when a worker is free, and otherwise as soon as every
one of them has started.

    python3 run_review.py <unit_id> [...]           # all 28 components + input consistency
    python3 run_review.py <unit_id> --component 09 --component 16
    python3 run_review.py <unit_id> --class files
    python3 run_review.py <unit_id> --no-consistency   # the components only
    python3 run_review.py --status
    python3 run_review.py <unit_id> --plan          # print the plan, spend nothing

Requires `audit/<unit_id>/bundle.json` — produce it with `audit_prepare.py` in this
skill.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_common as ac  # noqa: E402

SKILL = Path(__file__).resolve().parents[1]
COMPONENTS = SKILL / "components"
PROVISIONER = Path(__file__).resolve().parent / "provision_renderers.py"
PREPARE = Path(__file__).resolve().parent / "audit_prepare.py"
# One workspace for every script, so CUA_AUDIT_HOME moves the whole tree.
WORKSPACE = ac.WORKSPACE
AUDIT = ac.AUDIT
EFFORT = "max"
TIMEOUT = 1200

HDR = re.compile(r"\|\s*(audit-rubric id|allowed scores|evidence class|"
                 r"subagent model)\s*\|\s*(.+?)\s*\|")


def components() -> list[dict]:
    out = []
    for p in sorted(COMPONENTS.glob("[0-9][0-9]-*.md")):
        body = p.read_text(encoding="utf-8")
        meta = {k: v for k, v in HDR.findall(body)}
        model = (meta.get("subagent model") or "").split("`")[1] \
            if "`" in (meta.get("subagent model") or "") else ""
        out.append({
            "num": p.name[:2],
            "slug": p.stem,
            "path": p,
            "title": body.splitlines()[0].lstrip("# ").split(". ", 1)[-1],
            "id": (meta.get("audit-rubric id") or "").strip("`"),
            "scores": [s.strip() for s in (meta.get("allowed scores") or "").split(",")],
            "cls": (meta.get("evidence class") or "").strip("`"),
            "model": model,
        })
    return out


# Fields a single component adds to its output contract. `_generate.py` writes
# them into that component's file, and schema_for requires each one the file
# names, so the contract and the schema cannot drift apart.
EXTRA_FIELDS = {
    "whole_answer_inputs": {
        "type": "array",
        "items": {"type": "object", "additionalProperties": False,
                  "required": ["criteria", "input"],
                  "properties": {
                      "criteria": {"type": "array", "items": {"type": "integer"}},
                      "input": {"type": ["string", "null"]}}},
    },
}


def schema_for(comp: dict) -> dict:
    body = comp["path"].read_text(encoding="utf-8")
    extra = {k: v for k, v in EXTRA_FIELDS.items() if f'"{k}":' in body}
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["component_id", "title", "score", "evidence", "confidence",
                     *extra],
        "properties": {
            "component_id": {"type": "string"},
            "title": {"type": "string"},
            "score": {"type": "integer",
                      "enum": [int(s) for s in comp["scores"] if s.isdigit()]},
            "error_category": {"type": ["string", "null"]},
            "justification": {"type": ["string", "null"]},
            "evidence": {"type": "string"},
            "criteria": {"type": "array", "items": {"type": "integer"}},
            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            "blocked_on": {"type": ["string", "null"]},
            # v0.1: never scored. Suggestions the component's own answer options
            # do not name, so they cannot move `score` or the verdict.
            "minor_issues": {"type": "array", "items": {"type": "string"}},
            **extra,
        },
    }


def rendered_pages(d: Path) -> str:
    """Name every rendered page file in the prompt, not just the directory.

    Pointing at a folder was not enough: a reviewer given `render/` read the
    per-page *text* through Bash and then asserted that charts were legible
    and nothing was clipped — a visual claim made without looking. Listing the
    exact PNGs, and saying which tool can open them, removes that excuse.
    """
    try:
        idx = json.loads((d / "render_index.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""

    rows = []
    for side in ("inputs", "expected"):
        for e in idx.get(side) or []:
            pages = e.get("pages") or []
            if not pages or e.get("mode") == "native":
                continue
            base = f"render/{side}/{e['path']}"
            if not e.get("visual_verifiable"):
                rows.append(f"  {base}/{pages[0]}  — NOT VISUALLY VERIFIABLE: "
                            f"{e.get('unverifiable_reason', '')}")
                continue
            span = (f"{pages[0]} .. {pages[-1]}" if len(pages) > 1 else pages[0])
            note = f"parity {e.get('parity')}"
            if e.get("truncated"):
                note += f", TRUNCATED at {len(pages)} of {e.get('page_count')}"
            if e.get("ext_magic_mismatch"):
                note += ", EXTENSION/BYTES MISMATCH"
            rows.append(f"  {base}/{{{span}}}  {len(pages)} page(s), {note}")

    if not rows:
        return ""
    return ("RENDERED PAGES — open these with the **Read** tool. They are "
            "images; `cat`, `head` and every other Bash command are blind to "
            "them, and the `text.txt` beside them is text, not appearance. Do "
            "not assert that anything is legible, unclipped, aligned, "
            "paginated or fits on a page unless you have opened the page "
            "itself.\n" + "\n".join(rows) + "\n\n")


def render_prompt(unit: str, comp: dict) -> str:
    d = AUDIT / unit
    return (
        f"You are a QC REVIEWER for the CUA v3 project. You are scoring ONE "
        f"component of the official audit rubric against ONE task submission, "
        f"exactly as the review form defines it.\n\n"
        f"Your entire job is to decide: would this submission pass THIS "
        f"component of the audit rubric? Nothing else is in scope — not the "
        f"other 27 components, not your own sense of task quality.\n\n"
        f"The component definition below is generated verbatim from the "
        f"official `audit-rubric.csv`. Its score options are the only scores "
        f"that exist. Its thresholds are the only thresholds. Apply them "
        f"literally; do not substitute a stricter or looser standard.\n\n"
        f"UNIT UNDER REVIEW: {unit}\n"
        f"EVIDENCE DIRECTORY: {d}\n"
        f"  bundle.json            {d / 'bundle.json'}\n"
        f"  inputs_extracted.md    {d / 'inputs_extracted.md'}\n"
        f"  expected_extracted.md  {d / 'expected_extracted.md'}\n"
        f"  files/inputs/          {d / 'files' / 'inputs'}\n"
        f"  files/expected/        {d / 'files' / 'expected'}\n"
        f"  render/inputs/         {d / 'render' / 'inputs'}\n"
        f"  render/expected/       {d / 'render' / 'expected'}\n"
        f"  render_index.json      {d / 'render_index.json'}\n\n"
        f"`render/<side>/<filename>/page-NN.png` is what each non-image file "
        f"LOOKS like — open those with the Read tool to judge appearance. "
        f"`render_index.json` says which renderer produced each page and "
        f"whether it matches the version the CUA VM runs; when it reports a "
        f"file as not visually verifiable, that file's layout is UNVERIFIABLE "
        f"and belongs in `blocked_on`, never in a finding.\n\n"
        # Not every page-reading component is in the `files` class: a rubric
        # component can be widened to open the artifacts too. Its own evidence
        # list is the signal, so the two stay in step without a second map.
        + (rendered_pages(d) if "page-NN.png" in comp["path"].read_text(encoding="utf-8") else "")
        + f"Read `bundle.json` first. Then read only what this component needs.\n\n"
        f"{'=' * 78}\n\n" + comp["path"].read_text(encoding="utf-8")
    )


def render_gate(unit: str) -> list[str]:
    """Reasons this unit is not ready to be reviewed, each with its fix.

    Reviewing a unit whose deliverables never rendered costs 28 model calls
    and buys 28 UNVERIFIABLE layout findings. This stops only when the fix is
    an install we know how to perform — a platform with no published build is
    a limit to report, not a mistake to block on.
    """
    d = AUDIT / unit
    try:
        idx = json.loads((d / "render_index.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        if not (d / "files" / "expected").is_dir():
            return []
        return [f"{unit}: no render_index.json — the deliverables were never "
                f"rasterised, so every visual criterion would be scored blind.\n"
                f"    fix: python3 {PREPARE.name} {unit} --provision"]

    needs = idx.get("needs") or {}
    fixable = needs.get("install") or []
    if not fixable:
        return []
    blind = [e["path"] for e in idx.get("expected") or []
             if not e.get("visual_verifiable") and e.get("kind") != "text"]
    if not blind:
        return []
    return [f"{unit}: {', '.join(fixable)} not installed, so "
            f"{len(blind)} expected deliverable(s) did not render "
            f"({', '.join(blind[:3])}).\n"
            f"    fix: python3 {PROVISIONER.name} --for {d} --install "
            f"&& python3 {PREPARE.name} {unit}"]


def run_one(job: tuple[str, dict]) -> dict:
    unit, comp = job
    d = AUDIT / unit / "components"
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"{comp['num']}.json"
    prompt = render_prompt(unit, comp)
    (d / f"{comp['num']}.prompt.md").write_text(prompt, encoding="utf-8")

    t0 = time.time()
    cmd = ["claude", "--print", "--model", comp["model"], "--effort", EFFORT,
           "--permission-mode", "bypassPermissions", "--session-id", str(uuid.uuid4()),
           "--output-format", "stream-json", "--verbose",
           "--json-schema", json.dumps(schema_for(comp))]
    final, n_ev = None, 0
    child_env = {**os.environ, "IS_SANDBOX": "1"}
    try:
        with subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
                              bufsize=1, cwd=str(AUDIT / unit), env=child_env) as p, \
                (d / f"{comp['num']}.stream.jsonl").open("w", encoding="utf-8") as sf:
            p.stdin.write(prompt)
            p.stdin.close()
            beat = t0
            for line in p.stdout:
                sf.write(line)
                sf.flush()
                n_ev += 1
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if ev.get("type") == "result":
                    final = ev
                now = time.time()
                if now - beat > 60:
                    print(f"    [{unit[:8]} {comp['num']}] {int(now - t0)}s "
                          f"{n_ev} ev", flush=True)
                    beat = now
                if now - t0 > TIMEOUT:
                    p.kill()
                    return {"unit": unit, "component": comp["num"],
                            "model": comp["model"], "status": "timeout",
                            "elapsed_s": round(now - t0, 1)}
            p.wait()
    except FileNotFoundError:
        return {"unit": unit, "component": comp["num"], "status": "claude_not_found"}

    rec = {"unit": unit, "component": comp["num"], "title": comp["title"],
           "model": comp["model"], "elapsed_s": round(time.time() - t0, 1),
           "events": n_ev}
    if final is None:
        rec["status"] = "no_result_event"
        return rec
    try:
        txt = final.get("result")
        obj = txt if isinstance(txt, dict) else json.loads(txt)
        assert "score" in obj, "no score key"
        obj.setdefault("component_id", comp["id"])
        obj.setdefault("title", comp["title"])
        obj["_model"] = comp["model"]
        obj["_component"] = comp["num"]
        out.write_text(ac.dumps(obj), encoding="utf-8")
        rec.update(status="ok", score=obj["score"],
                   error_category=obj.get("error_category"))
    except Exception as e:                                   # noqa: BLE001
        rec["status"] = "invalid_output"
        rec["error"] = f"{type(e).__name__}: {e}"
        (d / f"{comp['num']}.raw.txt").write_text(str(final.get("result"))[:20000],
                                                  encoding="utf-8")
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("units", nargs="*")
    ap.add_argument("--component", action="append", default=[],
                    help="two-digit component number (repeatable)")
    ap.add_argument("--class", dest="cls", choices=["files", "rubric", "other"])
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument("--skip-render-check", action="store_true",
                    help="review even though a deliverable never rendered; its "
                         "layout will be scored UNVERIFIABLE")
    ap.add_argument("--no-auto-prepare", action="store_true",
                    help="do not run audit_prepare.py --provision for a unit "
                         "whose deliverables did not render; print the fix and "
                         "stop, as earlier versions did")
    ic = ap.add_mutually_exclusive_group()
    ic.add_argument("--with-consistency", action="store_true",
                    help="queue input_consistency.py behind the component calls "
                         "even when --component or --class narrows them")
    ic.add_argument("--no-consistency", action="store_true",
                    help="leave input_consistency.py out of the pool")
    a = ap.parse_args()

    comps = components()
    if len(comps) != 28:
        print(f"expected 28 components, found {len(comps)} — run _generate.py")
        return 2
    if a.component:
        want = {c.zfill(2) for c in a.component}
        comps = [c for c in comps if c["num"] in want]
    if a.cls:
        comps = [c for c in comps if c["cls"] == a.cls]

    units = a.units or sorted(p.name for p in AUDIT.iterdir()
                              if (p / "bundle.json").exists()) if AUDIT.exists() else []

    if a.status:
        for u in units:
            done = sorted(p.stem for p in (AUDIT / u / "components").glob("[0-9][0-9].json")) \
                if (AUDIT / u / "components").exists() else []
            ic_done = (AUDIT / u / "input_consistency.json").exists()
            print(f"  {u}  {len(done)}/28  missing="
                  f"{[c['num'] for c in components() if c['num'] not in done] or '-'}"
                  f"  consistency={'done' if ic_done else 'missing'}")
        return 0

    units = ac.admit(units, "run_review.py", named=bool(a.units),
                     replaces=lambda u: a.redo and any(
                         (AUDIT / u / "components" / f"{c['num']}.json").exists()
                         for c in comps))
    if units is None:
        return 3

    blocked = [] if a.skip_render_check else [m for u in units for m in render_gate(u)]
    if blocked and not (a.plan or a.no_auto_prepare):
        # The gate only fires when the fix is an install we know how to
        # perform, so performing it beats printing it: the operator's next
        # keystroke would be this command either way.
        print("artifacts not rendered — provisioning and re-preparing first:\n",
              flush=True)
        for u in sorted({m.split(":", 1)[0] for m in blocked}):
            print(f"  {u}", flush=True)
            subprocess.run([sys.executable, str(PREPARE), u, "--provision"],
                           timeout=5400)
        blocked = [m for u in units for m in render_gate(u)]
    if blocked:
        print("not ready to review — the artifacts have not been rendered:\n")
        for m in blocked:
            print(f"  {m}")
        print("\n  These components would report the deliverable's layout "
              "UNVERIFIABLE rather than score it.\n"
              "  Run the fix above, or pass --skip-render-check to review anyway.")
        return 2

    import input_consistency

    # Input consistency reads only the prepared evidence, so it shares the
    # component calls' pool. Each unit's call is queued right behind that
    # unit's components: the pool starts jobs in order, so it runs beside them
    # when a worker is free, and otherwise as soon as every one has started.
    def wants_consistency(u: str) -> bool:
        out = AUDIT / u / "input_consistency.json"
        if a.no_consistency or ((a.component or a.cls) and not a.with_consistency):
            return False
        if out.exists() and not a.redo:
            return False
        why = ac.locked(u, "input_consistency.py", replaces=out.exists())
        if why:
            print(f"  {u[:12]} input consistency not queued: {why.splitlines()[0]}")
        return why is None

    jobs = []
    for u in units:
        jobs += [("component", (u, c)) for c in comps
                 if a.redo or not (AUDIT / u / "components" / f"{c['num']}.json").exists()]
        if wants_consistency(u):
            jobs.append(("consistency", u))
    n_comp = sum(1 for kind, _ in jobs if kind == "component")
    n_ic = len(jobs) - n_comp
    if not jobs:
        print("nothing pending")
        return 0

    by_model = {}
    for kind, job in jobs:
        m = job[1]["model"] if kind == "component" else input_consistency.MODEL
        by_model[m] = by_model.get(m, 0) + 1
    print(f"{n_comp} component call(s)"
          + (f" + {n_ic} input-consistency call(s) queued behind them" if n_ic else "")
          + f" over {len(units)} unit(s), effort={EFFORT}, {a.workers} workers")
    for m, n in sorted(by_model.items()):
        print(f"  {m:22} {n} calls")
    if a.plan:
        for kind, job in jobs:
            if kind == "component":
                u, c = job
                print(f"  {u[:12]} {c['num']} {c['title'][:44]:44} {c['model']}")
            else:
                print(f"  {job[:12]} IC {'input file consistency':44} "
                      f"{input_consistency.MODEL}")
        return 0

    def consistency_one(unit: str) -> dict:
        try:
            return input_consistency.run_one(unit)
        except FileNotFoundError:
            return {"unit": unit, "status": "claude_not_found"}

    AUDIT.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futures = [(kind, ex.submit(run_one if kind == "component" else consistency_one, job))
                   for kind, job in jobs]
        for kind, fut in futures:
            rec = fut.result()
            if kind == "consistency":
                tail = (f"verdict={rec.get('verdict')} major={rec.get('n_major')} "
                        f"minor={rec.get('n_minor')}" if rec.get("status") == "ok"
                        else rec.get("error", ""))
                print(f"  {rec['unit'][:12]} IC "
                      f"[{input_consistency.MODEL.replace('claude-', '')}]: "
                      f"{rec.get('status')} ({rec.get('elapsed_s')}s) {tail}", flush=True)
                continue
            # The call log belongs to the unit it reviewed, beside its bundle.
            log = AUDIT / rec["unit"] / "_components.jsonl"
            log.parent.mkdir(parents=True, exist_ok=True)
            with log.open("a", encoding="utf-8") as fh:
                fh.write(ac.dumps(rec, indent=None) + "\n")
            tail = (f"score={rec.get('score')}" if rec.get("status") == "ok"
                    else rec.get("error", ""))
            print(f"  {rec['unit'][:12]} {rec['component']} "
                  f"[{(rec.get('model') or '?').replace('claude-', '')}]: "
                  f"{rec.get('status')} ({rec.get('elapsed_s')}s) {tail}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
