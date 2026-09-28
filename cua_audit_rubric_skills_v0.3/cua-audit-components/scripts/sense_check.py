#!/usr/bin/env python3
"""Final cross-component sense check: one opus call per unit over all 28 results.

Reads components/NN.json + bundle.json. Cannot change scores — it reports
contradictions, escalation proposals, unverified components and a fix order.

    python3 sense_check.py <unit_id> [...]
    python3 sense_check.py                 # every unit with 28 results
    python3 sense_check.py <unit_id> --redo
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
from run_review import AUDIT, SKILL, components  # noqa: E402

PROMPT = SKILL / "components" / "_sense_check.md"
MODEL = "claude-opus-5"
EFFORT = "max"
TIMEOUT = 1800

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["unit", "mechanical_verdict", "verdict_driver", "fragility",
                 "contradictions", "escalations", "unverified", "fix_order",
                 "summary"],
    "properties": {
        "unit": {"type": "string"},
        "mechanical_verdict": {"type": "integer"},
        "verdict_driver": {"type": "array", "items": {"type": "string"}},
        "fragility": {"type": "string"},
        "contradictions": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["components", "claim_a", "claim_b", "why_conflict"],
            "properties": {"components": {"type": "array", "items": {"type": "string"}},
                           "claim_a": {"type": "string"}, "claim_b": {"type": "string"},
                           "why_conflict": {"type": "string"}}}},
        "escalations": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["component", "current_score", "proposed_score",
                         "evidence", "reasoning"],
            "properties": {"component": {"type": "string"},
                           "current_score": {"type": "integer"},
                           "proposed_score": {"type": "integer"},
                           "evidence": {"type": "string"},
                           "reasoning": {"type": "string"}}}},
        "unverified": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["component", "unexamined"],
            "properties": {"component": {"type": "string"},
                           "blocked_on": {"type": ["string", "null"]},
                           "unexamined": {"type": "string"}}}},
        "fix_order": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["rank", "component", "fix"],
            "properties": {"rank": {"type": "integer"},
                           "component": {"type": "string"},
                           "fix": {"type": "string"}}}},
        "summary": {"type": "string"},
    },
}


def scoreboard(unit: str) -> str:
    lines = []
    for c in components():
        p = AUDIT / unit / "components" / f"{c['num']}.json"
        if not p.exists():
            lines.append(f"  {c['num']}  {c['title']:44} NOT RUN")
            continue
        o = json.loads(p.read_text(encoding="utf-8"))
        lines.append(f"  {c['num']}  {c['title']:44} score={o.get('score')} "
                     f"conf={o.get('confidence')} "
                     f"cat={o.get('error_category') or '-'}"
                     + ("  BLOCKED" if o.get("blocked_on") else ""))
    return "\n".join(lines)


def run_one(unit: str) -> dict:
    d = AUDIT / unit
    out = d / "sense_check.json"
    prompt = (
        f"UNIT UNDER REVIEW: {unit}\n"
        f"EVIDENCE DIRECTORY: {d}\n"
        f"  the 28 results   {d / 'components'}/NN.json\n"
        f"  bundle.json      {d / 'bundle.json'}\n"
        f"  inputs           {d / 'inputs_extracted.md'}\n"
        f"  expected         {d / 'expected_extracted.md'}\n\n"
        f"Scores as reported by the 28:\n{scoreboard(unit)}\n\n"
        + "=" * 78 + "\n\n" + PROMPT.read_text(encoding="utf-8")
    )
    (d / "sense_check.prompt.md").write_text(prompt, encoding="utf-8")

    t0 = time.time()
    cmd = ["claude", "--print", "--model", MODEL, "--effort", EFFORT,
           "--permission-mode", "bypassPermissions",
           "--output-format", "stream-json", "--verbose",
           "--json-schema", json.dumps(SCHEMA)]
    final, n_ev = None, 0
    with subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
                          bufsize=1, cwd=str(d)) as p, \
            (d / "sense_check.stream.jsonl").open("w", encoding="utf-8") as sf:
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
                print(f"    [{unit[:8]} sense] {int(time.time()-t0)}s {n_ev} ev",
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
        out.write_text(ac.dumps(obj), encoding="utf-8")
        rec.update(status="ok", verdict=obj.get("mechanical_verdict"),
                   n_contradictions=len(obj.get("contradictions") or []),
                   n_escalations=len(obj.get("escalations") or []))
    except Exception as e:                                   # noqa: BLE001
        rec["status"] = "invalid_output"
        rec["error"] = f"{type(e).__name__}: {e}"
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("units", nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--redo", action="store_true")
    a = ap.parse_args()

    ready = []
    for p in (sorted(AUDIT.iterdir()) if AUDIT.exists() else []):
        cd = p / "components"
        if cd.exists() and len(list(cd.glob("[0-9][0-9].json"))) == 28:
            ready.append(p.name)
    units = [u for u in (a.units or ready) if u in ready]
    skipped = [u for u in (a.units or []) if u not in ready]
    for u in skipped:
        print(f"  {u}: fewer than 28 component results — skipped")
    units = ac.admit(units, "sense_check.py", named=bool(a.units),
                     replaces=lambda u: a.redo and (AUDIT / u / "sense_check.json").exists())
    if units is None:
        return 3
    if not a.redo:
        units = [u for u in units if not (AUDIT / u / "sense_check.json").exists()]
    if not units:
        print("nothing to do")
        return 0

    print(f"sense check on {len(units)} unit(s), {MODEL} effort={EFFORT}")
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for rec in ex.map(run_one, units):
            print(f"  {rec['unit'][:12]}: {rec.get('status')} "
                  f"({rec.get('elapsed_s')}s) verdict={rec.get('verdict')} "
                  f"contradictions={rec.get('n_contradictions')} "
                  f"escalations={rec.get('n_escalations')}"
                  + (f"  {rec.get('error','')}" if rec.get("status") != "ok" else ""),
                  flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
