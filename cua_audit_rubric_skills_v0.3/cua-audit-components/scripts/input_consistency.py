#!/usr/bin/env python3
"""Input-file consistency pass: one opus call per unit over the supplied material.

The 28 components each grade one artifact against the review form. None grades
the input files in their own right, and none asks whether two supplied sources
contradict each other — a methodology PDF and a dataset's own reference sheet
stating different thresholds, a cutoff that selects nothing from the column it
governs, an answer key resolving the conflict silently. This pass does only
that, and it is never scored: it cannot move a component score or the verdict.

It needs `bundle.json` and the extracted views, so it runs any time after
`audit_prepare.py` — before, during or after `run_review.py`.

    python3 input_consistency.py <unit_id> [...]
    python3 input_consistency.py                 # every prepared unit
    python3 input_consistency.py <unit_id> --redo
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_common as ac  # noqa: E402
from run_review import AUDIT, SKILL, rendered_pages  # noqa: E402

PROMPT = SKILL / "components" / "_input_consistency.md"
MODEL = "claude-opus-5"
EFFORT = "max"
TIMEOUT = 1800

KINDS = ["rule-conflict", "rule-unusable", "value-conflict", "scope-conflict",
         "missing-referent", "self-contradiction", "naming-drift",
         "gold-resolves-silently", "prompt-conflict", "criterion-conflict"]

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["unit", "verdict", "summary", "files_checked",
                 "rules_compared", "findings"],
    "properties": {
        "unit": {"type": "string"},
        "verdict": {"type": "string", "enum": ["major", "minor", "none"]},
        "summary": {"type": "string"},
        "files_checked": {"type": "array", "items": {"type": "string"}},
        "rules_compared": {"type": "array", "items": {"type": "string"}},
        "findings": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["severity", "kind", "files", "statement_a",
                         "statement_b", "why_conflict", "graded_impact", "fix"],
            "properties": {
                "severity": {"type": "string", "enum": ["major", "minor"]},
                "kind": {"type": "string", "enum": KINDS},
                "files": {"type": "array", "items": {"type": "string"}},
                "statement_a": {"type": "string"},
                "statement_b": {"type": "string"},
                "why_conflict": {"type": "string"},
                "graded_impact": {"type": "string"},
                "component": {"type": ["string", "null"]},
                "fix": {"type": "string"}}}},
        "blocked_on": {"type": ["string", "null"]},
    },
}


def inventory(b: dict) -> str:
    """The supplied set, named up front so nothing is quietly skipped."""
    lines = []
    for side, key in (("input", "input_files"), ("expected", "expected_files")):
        for f in b.get(key) or []:
            lines.append(f"  {side:8} {f.get('path') or f.get('dest')}")
    return "\n".join(lines) or "  (none listed in bundle.json)"


def run_one(unit: str) -> dict:
    d = AUDIT / unit
    out = d / "input_consistency.json"
    b = json.loads((d / "bundle.json").read_text(encoding="utf-8"))
    prompt = (
        f"UNIT UNDER REVIEW: {unit}\n"
        f"EVIDENCE DIRECTORY: {d}\n"
        f"  bundle.json            {d / 'bundle.json'}\n"
        f"  inputs_extracted.md    {d / 'inputs_extracted.md'}\n"
        f"  expected_extracted.md  {d / 'expected_extracted.md'}\n"
        f"  files/inputs/          {d / 'files' / 'inputs'}\n"
        f"  files/expected/        {d / 'files' / 'expected'}\n"
        f"  render_index.json      {d / 'render_index.json'}\n\n"
        f"THE SUPPLIED SET — every one of these must be opened:\n"
        f"{inventory(b)}\n\n"
        + rendered_pages(d)
        + "=" * 78 + "\n\n" + PROMPT.read_text(encoding="utf-8")
    )
    (d / "input_consistency.prompt.md").write_text(prompt, encoding="utf-8")

    t0 = time.time()
    cmd = ["claude", "--print", "--model", MODEL, "--effort", EFFORT,
           "--permission-mode", "bypassPermissions",
           "--output-format", "stream-json", "--verbose",
           "--json-schema", json.dumps(SCHEMA)]
    final, n_ev = None, 0
    with subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
                          bufsize=1, cwd=str(d)) as p, \
            (d / "input_consistency.stream.jsonl").open("w", encoding="utf-8") as sf:
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
            if time.time() - beat > 60:
                print(f"    [{unit[:8]} inputs] {int(time.time()-t0)}s {n_ev} ev",
                      flush=True)
                beat = time.time()
            if time.time() - t0 > TIMEOUT:
                p.kill()
                return {"unit": unit, "status": "timeout"}
        p.wait()

    rec = {"unit": unit, "elapsed_s": round(time.time() - t0, 1), "events": n_ev}
    if final is None:
        rec["status"] = "no_result_event"
        return rec
    try:
        txt = final.get("result")
        obj = txt if isinstance(txt, dict) else json.loads(txt)
        obj.setdefault("unit", unit)
        # The verdict is mechanical, so derive it rather than trusting it: a
        # model that lists a major finding and then reports "minor" would
        # quietly downgrade the one thing this pass exists to surface.
        sev = {f.get("severity") for f in obj.get("findings") or []}
        obj["verdict"] = ("major" if "major" in sev
                          else "minor" if "minor" in sev else "none")
        out.write_text(ac.dumps(obj), encoding="utf-8")
        rec.update(status="ok", verdict=obj["verdict"],
                   n_major=sum(1 for f in obj.get("findings") or []
                               if f.get("severity") == "major"),
                   n_minor=sum(1 for f in obj.get("findings") or []
                               if f.get("severity") == "minor"))
    except Exception as e:                                   # noqa: BLE001
        rec["status"] = "invalid_output"
        rec["error"] = f"{type(e).__name__}: {e}"
    return rec


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Check the supplied files against each other and against "
                    "the prompt, the answer key and the criteria. Never scored.")
    ap.add_argument("units", nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--redo", action="store_true")
    a = ap.parse_args()

    ready = [p.name for p in (sorted(AUDIT.iterdir()) if AUDIT.exists() else [])
             if (p / "bundle.json").exists()]
    units = [u for u in (a.units or ready) if u in ready]
    for u in (a.units or []):
        if u not in ready:
            print(f"  {u}: no bundle.json — run audit_prepare.py first, skipped")
    units = ac.admit(units, "input_consistency.py", named=bool(a.units),
                     replaces=lambda u: a.redo
                     and (AUDIT / u / "input_consistency.json").exists())
    if units is None:
        return 3
    if not a.redo:
        units = [u for u in units
                 if not (AUDIT / u / "input_consistency.json").exists()]
    if not units:
        print("nothing to do")
        return 0

    print(f"input consistency on {len(units)} unit(s), {MODEL} effort={EFFORT}")
    for rec in ThreadPoolExecutor(max_workers=a.workers).map(run_one, units):
        print(f"  {rec['unit'][:12]}: {rec.get('status')} "
              f"({rec.get('elapsed_s')}s) verdict={rec.get('verdict')} "
              f"major={rec.get('n_major')} minor={rec.get('n_minor')}"
              + (f"  {rec.get('error','')}" if rec.get("status") != "ok" else ""),
              flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
