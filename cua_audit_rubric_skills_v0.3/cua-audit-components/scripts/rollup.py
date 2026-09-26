#!/usr/bin/env python3
"""Roll 28 component scores into the audit-rubric verdict for each unit.

Implements the reviewer roll-up: grade to the lowest component; any component
at 1-2 fails the task; no fail but any 3-4 makes the task 3-4; all must be 5
for a 5. Flags components that returned a score the CSV does not allow,
components whose chosen score required a justification but gave none, results
whose `_model` is not the component's pinned model, results that set
`blocked_on` but claim high confidence, and results with no `_components.jsonl`
call log beside them.

    python3 rollup.py                # every unit under audit/
    python3 rollup.py <unit_id> ...
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_common as ac  # noqa: E402
from run_review import AUDIT, components  # noqa: E402

SKILL = Path(__file__).resolve().parents[1]
# Same search order as _generate.py: the copy shipped inside this bundle first,
# then a `project_docs/` copy outside the skill as a fallback. The bundled CSV
# has to win, or the justification map is read from a different form than the
# one the components were generated from.
_CSV = [SKILL.parent / "audit-rubric.csv",
        SKILL.parents[1] / "project_docs" / "audit-rubric.csv"]
CSVPATH = next((c for c in _CSV if c.exists()), _CSV[0])


def justification_map() -> dict[str, dict[str, bool]]:
    """component_id -> {score: requires_justification}"""
    out, cur = {}, None
    for r in csv.DictReader(CSVPATH.open(encoding="utf-8")):
        if r["id"]:
            cur = r["id"]
            out[cur] = {}
        if r["answerOptionText"] and cur:
            out[cur][r["answerOptionScore"]] = \
                str(r["answerOptionRequiresJustification"]).lower() == "true"
    return out


def report_current(d: Path) -> bool:
    """The summary, which marks the audit finished, and the report are both at
    least as new as everything they are built from."""
    return ac.current(d, ac.SUMMARY) and ac.current(d, ac.REPORT)


def collect(unit: str, comps: list[dict], need: dict) -> dict:
    d = AUDIT / unit / "components"
    rows, problems = [], []
    if any(d.glob("[0-9][0-9].json")) and not (AUDIT / unit / "_components.jsonl").exists():
        problems.append("no _components.jsonl: nothing records that run_review.py "
                        "produced these results, or on which model")
    for c in comps:
        p = d / f"{c['num']}.json"
        if not p.exists():
            rows.append({**c, "score": None, "status": "not run"})
            continue
        o = json.loads(p.read_text(encoding="utf-8"))
        s = o.get("score")
        allowed = [int(x) for x in c["scores"] if x.isdigit()]
        if s not in allowed:
            problems.append(f"{c['num']} returned score {s}, CSV allows {allowed}")
        if need.get(c["id"], {}).get(str(s)) and not (o.get("justification") or "").strip():
            problems.append(f"{c['num']} score {s} requires a justification "
                            f"but none was given")
        if o.get("_model") != c["model"]:
            problems.append(f"{c['num']} records model {o.get('_model')!r}, "
                            f"pinned model is {c['model']}")
        if str(o.get("blocked_on") or "").strip() and o.get("confidence") == "high":
            problems.append(f"{c['num']} sets blocked_on but claims high confidence")
        rows.append({**c, "score": s, "status": "ok",
                     "error_category": o.get("error_category"),
                     "justification": o.get("justification"),
                     "evidence": o.get("evidence"),
                     "confidence": o.get("confidence"),
                     "blocked_on": o.get("blocked_on"),
                     "minor_issues": o.get("minor_issues") or [],
                     "whole_answer_inputs": o.get("whole_answer_inputs")})
    scored = [r["score"] for r in rows if isinstance(r["score"], int)]
    verdict = min(scored) if scored else None
    band = ("FAIL" if verdict is not None and verdict <= 2
            else "NON-FAIL" if verdict in (3, 4)
            else "PASS" if verdict == 5 else "INCOMPLETE")
    b = json.loads((AUDIT / unit / "bundle.json").read_text(encoding="utf-8"))
    sc_path = AUDIT / unit / "sense_check.json"
    sc = json.loads(sc_path.read_text(encoding="utf-8")) if sc_path.exists() else {}
    ic_path = AUDIT / unit / "input_consistency.json"
    ic = json.loads(ic_path.read_text(encoding="utf-8")) if ic_path.exists() else {}
    n_minor = sum(len(r.get("minor_issues") or []) for r in rows)
    return {"unit": unit, "domain": b.get("domain"), "sense": sc,
            "n_run": len(scored), "verdict": verdict, "band": band,
            "rows": rows, "problems": problems, "n_minor": n_minor,
            "renders": b.get("renders") or {}, "inputs": ic}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("units", nargs="*")
    a = ap.parse_args()

    comps, need = components(), justification_map()
    units = a.units or (sorted(p.name for p in AUDIT.iterdir()
                               if (p / "components").exists()) if AUDIT.exists() else [])
    writable = ac.admit(units, "rollup.py", named=bool(a.units),
                        replaces=lambda u: report_current(AUDIT / u))
    if writable is None:
        return 3
    res = [collect(u, comps, need) for u in units]
    if not res:
        print("no reviewed units found under audit/")
        return 1

    print(f"{'unit':26} {'domain':16} {'run':>5} {'verdict':>7}  {'band':9} {'rec':>5} sense")
    for r in res:
        print(f"{r['unit']:26} {(r['domain'] or '?')[:16]:16} "
              f"{r['n_run']:>2}/28 {str(r['verdict']):>7}  {r['band']:9} "
              f"{r['n_minor']:>5} "
              f"{('esc=' + str(len((r.get('sense') or {}).get('escalations') or [])) + ' contra=' + str(len((r.get('sense') or {}).get('contradictions') or []))) if r.get('sense') else '-'}"
              + (f"   ⚠ {len(r['problems'])} contract issue(s)" if r["problems"] else ""))
    # A unit whose deliverables never rendered was scored without ever seeing
    # them. That is a limit of this host, not a verdict — but it must be said.
    for r in res:
        rd = r["renders"]
        if rd.get("status") != "ok":
            if rd:
                print(f"\n  {r['unit'][:12]} render: {rd.get('status')} — visual "
                      f"criteria were judged without page images")
            continue
        if rd.get("unavailable") or rd.get("degraded") or not rd.get("parity_ok"):
            print(f"\n  {r['unit'][:12]} render: {rd.get('visual_verifiable')} "
                  f"file(s) visually verifiable, {rd.get('degraded')} degraded, "
                  f"{rd.get('unavailable')} unavailable")
            for w in rd.get("parity_warnings") or []:
                print(f"    parity: {w}")

    # Input consistency is not scored and never reaches the verdict, so it has
    # to be said out loud or it is invisible beside a clean grid.
    if any(r["inputs"] for r in res):
        print()
        for r in res:
            ic = r["inputs"]
            if not ic:
                print(f"  {r['unit'][:12]} inputs: not run — "
                      f"python3 input_consistency.py {r['unit']}")
                continue
            f = ic.get("findings") or []
            nmaj = sum(1 for x in f if x.get("severity") == "major")
            rc = ic.get("rules_compared") or 0
            print(f"  {r['unit'][:12]} inputs: {ic.get('verdict', '?').upper():5} "
                  f"{nmaj} major, {len(f) - nmaj} minor "
                  f"over {len(rc) if isinstance(rc, list) else rc} shared rule(s)")

    tot_minor = sum(r["n_minor"] for r in res)
    if tot_minor:
        print(f"\n{tot_minor} unscored recommendation(s) across {len(res)} unit(s). "
              f"These never move a verdict — see 'Recommendations, not scored' "
              f"per submission in the HTML.")

    # Both outputs are written per unit, beside that unit's bundle.json, so a
    # submission's whole audit travels as one directory.
    cols = ["unit", "component", "title", "model", "score", "error_category",
            "confidence", "blocked_on", "justification", "evidence",
            "minor_issues"]
    import render_html
    print()
    for r in res:
        if r["unit"] not in writable:
            continue
        d = AUDIT / r["unit"]
        d.mkdir(parents=True, exist_ok=True)
        with (d / "component_scores.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            for row in r["rows"]:
                w.writerow({"unit": r["unit"], "component": row["num"],
                            "title": row["title"], "model": row.get("model"),
                            "score": row["score"],
                            "error_category": row.get("error_category") or "",
                            "confidence": row.get("confidence") or "",
                            "blocked_on": row.get("blocked_on") or "",
                            "justification": (row.get("justification") or "")[:4000],
                            "evidence": (row.get("evidence") or "")[:4000],
                            "minor_issues": " | ".join(
                                row.get("minor_issues") or [])[:4000]})
        (d / "component_review.html").write_text(render_html.render([r], AUDIT),
                                                 encoding="utf-8")
        print(f"  {d / 'component_scores.csv'}")
        print(f"  {d / 'component_review.html'}")
    allp = [(r["unit"], p) for r in res for p in r["problems"]]
    if allp:
        print(f"\n{len(allp)} output-contract issue(s):")
        for u, p in allp[:20]:
            print(f"  {u[:12]} {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
