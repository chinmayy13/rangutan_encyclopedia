#!/usr/bin/env python3
"""Audit a version folder end to end with cua-audit-components' own passes.

    prepare      rerun_prepare.py      bundle.json, extracts and renders, from the folder
    review       run_review.py         the 28 components; any left without a result retried once
    consistency  input_consistency.py  do the supplied files agree?
    sense        sense_check.py        the 28 results read together
    report       rollup.py             component_scores.csv + component_review.html
    summary      summarize.py          component_review_summary.html, the fixes to make

Before the review calls the model, a component whose evidence is exactly what
an earlier audit of the task scored takes that audit's result instead
(rerun_reuse.py; --fresh turns this off). Input consistency reads only the
prepared evidence, so it shares the review's worker pool, queued behind the
component calls: it starts beside them when a worker is free, and otherwise as
soon as every one has started. When the review makes no call, it runs
alongside the sense check instead. The report waits for it.

Each pass is handed the unit by name. Their no-argument forms sweep every unit
under audit/, the first run included, and a rerun leaves the first run alone.

Usage:
    python3 rerun.py <task_id>-v2                  # every step, in order
    python3 rerun.py <task_id>                     # the task's one pending version
    python3 rerun.py <task_id> --new               # copy the latest version to -v<N+1>, audit it
    python3 rerun.py <task_id>-v2 --plan           # what would run; spends nothing
    python3 rerun.py <task_id>-v2 --fresh          # a new call for every component
    python3 rerun.py <task_id>-v2 --steps review,sense,report,summary --component 18 --redo
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rerun_common as rr  # noqa: E402
import rerun_prepare as rp  # noqa: E402
import rerun_reuse as rz  # noqa: E402
import rerun_versions as rv  # noqa: E402

A = rr.PIPELINE
ME = Path(__file__).resolve()
PREPARE = ME.with_name("rerun_prepare.py")
STEPS = ("prepare", "review", "consistency", "sense", "report", "summary")
PY = sys.executable


def run(cmd: list, tag: str | None = None) -> int:
    """tag: the pass is running alongside another, so its lines are labelled."""
    cmd = [str(c) for c in cmd]
    lead = f"[{tag}] " if tag else ""
    print(f"\n{lead}$ {Path(cmd[1]).name} {' '.join(cmd[2:])}", flush=True)
    if not tag:
        return subprocess.run(cmd).returncode
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, bufsize=1,
                          env={**os.environ, "PYTHONUNBUFFERED": "1"}) as p:
        for line in p.stdout:
            print(lead + line.rstrip("\n"), flush=True)
    return p.returncode


# ------------------------------------------------------------ which folder
def pick(target: str, new: bool, src: str | None, from_response: bool) -> Path | None:
    """The version folder a request means."""
    name = Path(target).name
    if rr.split_unit(name):
        return rr.resolve_dir(target)
    if not rv.first_run_ready(name):
        return None
    waiting = rv.pending(name)
    if new:
        if waiting:
            print(f"{waiting[0].name} is still pending: audit it first "
                  f"(python3 {ME} {waiting[0].name}), or create another version "
                  f"by hand with rerun_versions.py new")
            return None
        return rv.new(name, src, from_response)
    if len(waiting) == 1:
        print(f"{name}: auditing its pending version {waiting[0].name}")
        return waiting[0]
    if waiting:
        print(f"{name} has {len(waiting)} pending versions "
              f"({', '.join(d.name for d in waiting)}); name the one to audit")
        return None
    print(f"{name}: every version is audited. To audit it again:\n"
          f"  python3 {ME} {name} --new    (copies {rv.latest(name).name} to "
          f"{name}-v{rr.next_version(name)})")
    return None


def evidence_problem(d: Path, base: str | None) -> str | None:
    man = rr.own_manifest(d)
    if not man or not (d / "bundle.json").is_file():
        return "it has not been prepared"
    plan = rp.build(d, base)
    if plan["errors"]:
        return "; ".join(plan["errors"])
    if plan["fingerprint"] != man.get("fingerprint"):
        return "the folder changed after it was prepared"
    return None


# ------------------------------------------------------------ the passes
def _log(d: Path) -> list[dict]:
    p = d / "_components.jsonl"
    out = []
    # A record ends at "\n" alone: splitlines() would also cut one at a U+2028
    # or U+0085 inside one of its strings.
    for line in (p.read_text(encoding="utf-8").split("\n") if p.exists() else []):
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def _review_once(d: Path, a, only: list[str] | None,
                 consistency: bool = False) -> tuple[int, list[str], list[dict]]:
    """-> (exit code, components this call left without a result, its log records).
    consistency: queue input_consistency.py in the same pool, behind the components."""
    cmd = [PY, A / "run_review.py", d.name, "--no-auto-prepare", "--workers", a.workers,
           "--with-consistency" if consistency else "--no-consistency"]
    for c in (only if only is not None else a.component):
        cmd += ["--component", c]
    if a.cls and only is None:
        cmd += ["--class", a.cls]
    if a.redo:
        cmd.append("--redo")
    if a.skip_render_check:
        cmd.append("--skip-render-check")
    seen = len(_log(d))
    code = run(cmd)
    fresh = _log(d)[seen:]
    return code, sorted({r.get("component") for r in fresh if r.get("status") != "ok"}), fresh


def reuse(d: Path, base: str, comps: list[dict]) -> None:
    """Give d the result of every component an earlier audit scored on the
    same evidence, so that only the rest cost a call."""
    found = rz.find(d, base, comps)
    if not found:
        return
    rz.carry(d, found, comps)
    by = collections.defaultdict(list)
    for n, (src, _) in sorted(found.items()):
        by[src.name].append(n)
    print(f"\nreusing {len(found)} component result(s) whose evidence is unchanged "
          f"(--fresh scores them anew):")
    for src, nums in by.items():
        print(f"  from {src}: {' '.join(nums)}")


def review(d: Path, a, base: str, consistency: bool) -> bool:
    """consistency: input consistency is due, so it joins the review's pool."""
    import run_review
    wanted = {c.zfill(2) for c in a.component}
    comps = [c for c in run_review.components()
             if (not wanted or c["num"] in wanted) and (not a.cls or c["cls"] == a.cls)]
    want = [c["num"] for c in comps]
    if not (a.fresh or a.redo):
        reuse(d, base, [c for c in comps if c["num"] not in rr.done_components(d)])
        if set(want) <= set(rr.done_components(d)):
            return True
    code, failed, fresh = _review_once(d, a, None, consistency)
    if code == 2:
        print(f"\nthe review did not start (see above). If a renderer is missing:\n"
              f"  python3 {PREPARE} {d.name} --provision --rebuild\n"
              f"then run this again, or add --skip-render-check to score layout "
              f"UNVERIFIABLE.")
        return False
    failed = sorted(set(failed) | {n for n in want if n not in rr.done_components(d)})
    if failed and any(r.get("status") == "claude_not_found" for r in fresh):
        print("\nthe claude CLI is not on PATH, so no component could run")
        return False
    if failed:
        why = collections.Counter(r.get("status") for r in fresh
                                  if r.get("component") in failed)
        print(f"\n{len(failed)} component(s) came back without a result ("
              + (", ".join(f"{k} x{v}" for k, v in why.items()) or "not run")
              + "): retrying them once")
        code, failed, fresh = _review_once(d, a, failed)
        failed = sorted(set(failed) | {n for n in want if n not in rr.done_components(d)})
    if failed:
        print(f"\nstill no result for component(s) {', '.join(failed)}; the call log "
              f"is {d / '_components.jsonl'}. Nothing was rolled up.\n"
              f"  resume: python3 {ME} {d.name}")
        return False
    return True


def single(d: Path, script: str, out: str, redo: bool, tag: str | None = None) -> bool:
    """One unscored pass; retried once when it leaves no result."""
    lead = f"[{tag}] " if tag else ""
    p = d / out
    if p.exists() and not redo:
        print(f"\n{lead}{out} already present, kept")
        return True
    before = p.stat().st_mtime_ns if p.exists() else None
    for attempt in (1, 2):
        run([PY, A / script, d.name] + (["--redo"] if p.exists() else []), tag)
        if p.exists() and p.stat().st_mtime_ns != before:
            return True
        if attempt == 1:
            print(f"{lead}  {script} left no fresh {out}: retrying once")
    print(f"{lead}  still no {out}; the report will show this pass as not run")
    return False


def alongside(d: Path, redo: bool):
    """Start input consistency beside the sense check, when the review's pool
    did not run it: the report is the first step to read its result."""
    pool = ThreadPoolExecutor(max_workers=1)
    job = pool.submit(single, d, "input_consistency.py", "input_consistency.json",
                      redo, "consistency")
    pool.shutdown(wait=False)
    return job


def sense(d: Path, a) -> bool:
    n = len(rr.done_components(d))
    if n < 28:
        print(f"\nsense check needs all 28 component results and {d.name} has {n}; skipped")
        return False
    return single(d, "sense_check.py", "sense_check.json", a.redo)


def report(d: Path) -> bool:
    run([PY, A / "rollup.py", d.name])
    return (d / rr.REPORT).is_file()


def summary(d: Path, a) -> bool:
    if rr.summary_ok(d) and not a.redo:
        print(f"\n{rr.SUMMARY} already describes these results, kept")
        return True
    code = run([PY, A / "summarize.py", d.name] + (["--redo"] if a.redo else []))
    if code != 0 or not rr.summary_ok(d):
        print(f"  summarize.py wrote no {rr.SUMMARY}")
        return False
    return True


def finish(d: Path, base: str) -> None:
    v, n = rr.verdict(d)
    bv, _ = rr.verdict(rr.AUDIT / base)
    print(f"\n{d.name}: verdict {v} {rr.band(v)} over {n}/28 components "
          f"(first run {base}: {bv} {rr.band(bv)})")
    moved = []
    for c in rr.done_components(d):
        now = (rr.read_json(d / "components" / f"{c}.json") or {}).get("score")
        was = (rr.read_json(rr.AUDIT / base / "components" / f"{c}.json") or {}).get("score")
        if now != was:
            moved.append(f"{c} {was} -> {now}")
    print("  components that moved since the first run: " + (", ".join(moved) or "none"))
    carried = [c for c in rr.done_components(d)
               if (rr.read_json(d / "components" / f"{c}.json") or {}).get("_reused_from")]
    if carried:
        print(f"  results reused from an earlier audit (same evidence): {len(carried)} of {n}")
    for f in (rr.REPORT, rr.SUMMARY, "component_scores.csv"):
        if (d / f).exists():
            print(f"  {d / f}")


# ------------------------------------------------------------ the plan
def show_plan(a, steps: list[str]) -> int:
    import input_consistency
    import run_review
    import sense_check
    import summarize

    name = Path(a.target).name
    d = plan = man = None
    if rr.split_unit(name):
        d = rr.resolve_dir(a.target)
    else:
        if not rv.first_run_ready(name):
            return 1
        waiting = rv.pending(name)
        if len(waiting) > 1 and not a.new:
            print(f"{name} has {len(waiting)} pending versions "
                  f"({', '.join(x.name for x in waiting)}); name the one to plan")
            return 1
        if waiting and not a.new:
            d = waiting[0]
        elif waiting:
            print(f"{waiting[0].name} is still pending; --new would refuse")
            return 1
        else:
            src = a.src or ("tasks/ response.json" if a.from_response else rv.latest(name).name)
            print(f"{name}: would create {name}-v{rr.next_version(name)} from {src}, "
                  f"then audit it")
    if d is not None:
        plan = rp.build(d, a.base)
        rp.show(plan)
        if plan["errors"]:
            return 2
        man = rr.own_manifest(d)
        if man and rr.reported(d) and not a.reset and "prepare" in steps:
            rest = (rr.unfinished(d) if plan["fingerprint"] == man.get("fingerprint")
                    else [])
            if not rest:
                print(f"\n{d.name} already has a finished audit, so prepare will refuse: "
                      f"--new audits a copy of it, --reset audits it again in place")
                return 3
            print(f"\n{d.name}: its audit stopped before {', '.join(rest)} finished; "
                  f"the run finishes it")
            steps = [s for s in steps if s in rest]
        elif (man and "prepare" in steps and not a.reset and rr.present(d, rr.REVIEW)
                and plan["fingerprint"] != man.get("fingerprint")):
            print(f"\n{d.name} holds review outputs produced before the folder last "
                  f"changed, so prepare will refuse: --reset starts its review over")
            return 3

    fresh = a.redo or a.reset or d is None or (
        "prepare" in steps and not man and bool(rr.present(d, rr.REVIEW)))
    if fresh and d is not None and not (a.redo or a.reset):
        print(f"\n{d.name} holds review outputs copied from another run; prepare "
              f"clears them, so every pass runs")
    wanted = {c.zfill(2) for c in a.component}
    comps = [c for c in run_review.components()
             if (not wanted or c["num"] in wanted) and (not a.cls or c["cls"] == a.cls)]
    todo = [c for c in comps if fresh
            or not (d / "components" / f"{c['num']}.json").exists()]
    reused, exact = {}, True
    if "review" in steps and d is not None and todo and not (a.redo or a.fresh):
        exact = (man is not None and man.get("fingerprint") == plan["fingerprint"]
                 and (d / "bundle.json").is_file())
        reused = rz.find(d, plan["base"], todo, None if exact else plan)
        todo = [c for c in todo if c["num"] not in reused]

    def kept(out: str) -> bool:
        return not fresh and (d / out).exists()

    print()
    if "prepare" in steps:
        current = (plan is not None and man is not None
                   and man.get("fingerprint") == plan["fingerprint"]
                   and (d / "bundle.json").exists())
        print("  prepare      " + ("evidence up to date" if current else
                                   "build bundle.json, the extracts and the renders")
              + ("" if a.no_provision else "; installs any renderer the files need"))
    if "review" in steps:
        by = collections.Counter(c["model"] for c in todo)
        print(f"  review       {len(todo)} component call(s) at effort {run_review.EFFORT}"
              + (": " + ", ".join(f"{m} x{k}" for m, k in sorted(by.items())) if by else ""))
        if reused:
            srcs = ", ".join(sorted({s.name for s, _ in reused.values()}))
            print(f"               {len(reused)} result(s) reused from {srcs}, which scored "
                  f"the same evidence"
                  + ("" if exact else " as far as the folder shows before prepare")
                  + "; --fresh calls them too")
        elif d is None and not (a.redo or a.fresh):
            print("               fewer if an earlier audit scored the same evidence: "
                  "decided once the copy is prepared")
    for step, mod, out in (("consistency", input_consistency, "input_consistency.json"),
                           ("sense", sense_check, "sense_check.json")):
        if step in steps:
            where = ""
            if step == "consistency":
                where = (f", in the review's pool of {a.workers} workers, behind the "
                         f"component calls" if "review" in steps and todo
                         else ", alongside the sense check" if "sense" in steps else "")
            print(f"  {step:<12} " + ("already done" if kept(out) else
                                      f"1 call, {mod.MODEL}{where}"))
    if "report" in steps:
        print("  report       rollup.py, no model call")
    if "summary" in steps:
        done = (not fresh
                and not any(s in steps for s in ("review", "consistency", "sense", "report"))
                and rr.summary_ok(d))
        print("  summary      " + ("already done" if done else f"1 call, {summarize.MODEL}"))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Audit a version folder with the cua-audit-components passes.")
    p.add_argument("target", help="version folder (<task_id>-vN), or a task id to "
                                  "audit its pending version")
    p.add_argument("--new", action="store_true",
                   help="for a task id: create the next version (a copy of the "
                        "latest) and audit it")
    p.add_argument("--from", dest="src", metavar="UNIT",
                   help="with --new: copy this folder instead of the latest version")
    p.add_argument("--from-response", action="store_true",
                   help="with --new: take the views and files from the task's response.json")
    p.add_argument("--steps", help=f"comma-separated subset of {','.join(STEPS)}")
    p.add_argument("--base", help="first-run unit, when the folder name does not start with it")
    p.add_argument("--no-provision", action="store_true",
                   help="do not install missing renderers during prepare")
    p.add_argument("--no-render", action="store_true")
    p.add_argument("--rebuild", action="store_true", help="rebuild evidence even when up to date")
    p.add_argument("--reset", action="store_true",
                   help="discard this version's earlier review outputs before preparing")
    p.add_argument("--workers", type=int, default=12)
    p.add_argument("--component", action="append", default=[],
                   help="two-digit component number (repeatable)")
    p.add_argument("--class", dest="cls", choices=["files", "rubric", "other"])
    p.add_argument("--redo", action="store_true",
                   help="re-run passes that already have output")
    p.add_argument("--fresh", action="store_true",
                   help="a new call for every component, even one an earlier audit "
                        "of the task scored on the same evidence")
    p.add_argument("--skip-render-check", action="store_true")
    p.add_argument("--plan", action="store_true", help="print what would run; spend nothing")
    a = p.parse_args()

    steps = [s.strip() for s in a.steps.split(",")] if a.steps else list(STEPS)
    bad = [s for s in steps if s not in STEPS]
    if bad:
        p.error(f"unknown step(s) {', '.join(bad)}; choose from {', '.join(STEPS)}")
    steps = [s for s in STEPS if s in steps]

    if a.plan:
        return show_plan(a, steps)

    d = pick(a.target, a.new, a.src, a.from_response)
    if d is None:
        return 1
    # cua-audit-components' scripts refuse a version folder unless this names it.
    os.environ[rr.ac.RERUN_ENV] = d.name
    split = rr.split_unit(d.name)
    base = a.base or (split[0] if split else None)
    if base is None:
        print(f"{d.name}: cannot tell which first run it belongs to; pass --base")
        return 2

    if ("prepare" in steps and not a.reset and rr.own_manifest(d)
            and rr.reported(d) and not evidence_problem(d, a.base)):
        rest = rr.unfinished(d)
        if rest:
            print(f"{d.name}: its audit stopped before {', '.join(rest)} finished and "
                  f"its folder is unchanged since: finishing it")
            steps = [s for s in steps if s in rest]

    if "prepare" in steps:
        code = run([PY, PREPARE, d.name]
                   + (["--base", a.base] if a.base else [])
                   + ([] if a.no_provision else ["--provision"])
                   + (["--no-render"] if a.no_render else [])
                   + (["--rebuild"] if a.rebuild else [])
                   + (["--reset"] if a.reset else []))
        if code != 0:
            return code
    elif any(s in steps for s in ("review", "consistency", "sense")):
        why = evidence_problem(d, a.base)
        if why:
            print(f"{d.name}: its evidence is not current ({why}). "
                  f"Run the prepare step first.")
            return 3

    ok = {}
    ic = d / "input_consistency.json"
    ic_was = ic.stat().st_mtime_ns if ic.exists() else None
    pooled = "review" in steps and "consistency" in steps and (a.redo or ic_was is None)
    if "review" in steps:
        if not review(d, a, base, pooled):
            return 1
        ok["review"] = True
    side = None
    if "consistency" in steps:
        if pooled and ic.exists() and ic.stat().st_mtime_ns != ic_was:
            ok["consistency"] = True
        elif "sense" in steps:
            side = alongside(d, a.redo)
        else:
            ok["consistency"] = single(d, "input_consistency.py", "input_consistency.json",
                                       a.redo)
    try:
        if "sense" in steps:
            ok["sense"] = sense(d, a)
    finally:
        if side is not None:
            if not side.done():
                print("\nwaiting for the input consistency pass to finish", flush=True)
            ok["consistency"] = side.result()
    if "report" in steps:
        if not report(d):
            print(f"\nrollup.py wrote no {rr.REPORT}")
            return 1
        ok["report"] = True
    if "summary" in steps:
        ok["summary"] = summary(d, a)

    if any(s in steps for s in ("review", "report", "summary")):
        finish(d, base)
    failed = [k for k, v in ok.items() if not v]
    if failed:
        print(f"\nincomplete: {', '.join(failed)} did not produce a result")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
