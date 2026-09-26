#!/usr/bin/env python3
"""Rebuild a version folder's evidence so cua-audit-components can review it.

A version folder is audit/<task_id>-vN/, beside the task's first run, and
holds what an editor changes:

    prompt.md, rubric.json, task.md    required, whatever they say
    files/inputs/*, files/expected/*   the input files and the answer key

From it, plus the first run's platform record for everything a folder cannot
express, this writes the evidence audit_prepare.py writes for a first run,
under the same names and in the same shapes:

    bundle.json                        built by audit_common.bundle_for itself
    inputs_extracted.md, expected_extracted.md
    render/<side>/<file>/page-NN.png, render_index.json

and _rerun.json, which records where each field came from and what changed
against the first run. The three views and files/ are only read; the first
run's folder is never written.

Usage:
    python3 rerun_prepare.py <task_id>-v2 --provision
    python3 rerun_prepare.py <task_id>-v2 --check      # validate and diff, write nothing
    python3 rerun_prepare.py <task_id>-v2 --no-render
    python3 rerun_prepare.py <task_id>-v2 --rebuild    # even when up to date
    python3 rerun_prepare.py <task_id>-v2 --reset      # discard this version's review outputs

Exit codes: 0 ready, 2 not a valid version folder, 3 refused because the
folder's review outputs were produced from different evidence.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rerun_common as rr  # noqa: E402
from rerun_common import ac  # noqa: E402
import audit_prepare as ap  # noqa: E402

VERSIONS = Path(__file__).resolve().with_name("rerun_versions.py")
DESKTOP = "/home/docker/Desktop/"
# Records of the prepare run itself, not evidence about the task.
RUN_KEYS = ("readers", "staged_files", "extracted", "renders")
# What a version folder can move. Every other bundle.json field is the
# platform's record of the task, read from the first run's response.
FOLDER_KEYS = ("domain", "sub_domain", "prompt", "criteria", "input_files",
               "expected_files", "verifier")
DERIVED_KEYS = ("mechanical", "agent_runs")
CATEGORIES = ("format_gate", "correctness", "visual")
TYPES = ("MUST-PASS", "REGULAR")
CRIT_FIELDS = ("title", "weight", "category", "type")


# ------------------------------------------------------------ the folder
def read_views(d: Path, plan: dict) -> dict:
    err, warn = plan["errors"].append, plan["warnings"].append
    missing = [v for v in rr.VIEWS if not (d / v).is_file()]
    if missing:
        err(f"missing {', '.join(missing)}: a version folder must hold "
            f"prompt.md, rubric.json and task.md, whatever they contain")
        return {}

    prompt = (d / "prompt.md").read_text(encoding="utf-8")
    if not prompt.strip():
        warn("prompt.md is empty")

    try:
        rub = json.loads((d / "rubric.json").read_text(encoding="utf-8"))
    except ValueError as e:
        err(f"rubric.json is not valid JSON: {e}")
        rub = []
    if isinstance(rub, dict) and isinstance(rub.get("criteria"), list):
        rub = rub["criteria"]
    if not isinstance(rub, list):
        err('rubric.json must be a list of criteria, or {"criteria": [...]}')
        rub = []
    crits, seen = [], set()
    for i, c in enumerate(rub, 1):
        if not isinstance(c, dict):
            err(f"rubric.json criterion {i} is not an object")
            continue
        w, t, a = c.get("weight"), c.get("title"), c.get("annotations")
        if isinstance(w, bool) or not (w is None or isinstance(w, (int, float))):
            err(f"rubric.json criterion {i}: weight {w!r} must be a number or null")
        if t is not None and not isinstance(t, str):
            err(f"rubric.json criterion {i}: title must be text")
        if a is not None and not isinstance(a, dict):
            err(f"rubric.json criterion {i}: annotations must be an object or null")
            a = None
        a = a or {}
        if a.get("criteria_category") not in (None,) + CATEGORIES:
            warn(f"criterion {i}: criteria_category {a['criteria_category']!r} is "
                 f"not one of {', '.join(CATEGORIES)}, so the weight-share check "
                 f"will not count it")
        if a.get("criteria_type") not in (None,) + TYPES:
            warn(f"criterion {i}: criteria_type {a['criteria_type']!r} is not "
                 f"MUST-PASS or REGULAR")
        if c.get("id") and c["id"] in seen:
            warn(f"criterion {i}: id {c['id']} is used twice")
        seen.add(c.get("id"))
        # rubric.json spells an absent field as null; the response omits it.
        crits.append({k: v for k, v in c.items() if v is not None})
    if not crits and not plan["errors"]:
        warn("rubric.json has no criteria")

    task = {}
    for line in (d / "task.md").read_text(encoding="utf-8").splitlines():
        k, sep, v = line.partition(":")
        if sep and k.strip() in ("domain", "sub_domain"):
            task[k.strip()] = v.strip()
    for k in ("domain", "sub_domain"):
        if k not in task:
            plan["notes"].append(f"task.md has no {k} line: keeping the first run's")
    return {"prompt": prompt, "criteria": crits, "task": task}


def inherit_from(base: str, unit: str, side: str) -> Path:
    """Where a version folder with no files on one side takes them from: the
    nearest earlier version that has some, else the first run."""
    me = rr.version_of(unit[len(base) + 1:])
    best = None
    if me is not None:
        for p in rr.versions(base):
            n = rr.version_of(p.name[len(base) + 1:])
            if n is not None and n < me and rr.visible(p / "files" / side):
                best = p
    return best or rr.AUDIT / base


def collect_sides(d: Path, plan: dict) -> dict:
    sides = {}
    for side in rr.SIDES:
        own = d / "files" / side
        root, files, came = own, rr.visible(own), None
        if not files:
            src = inherit_from(plan["base"], d.name, side)
            theirs = rr.visible(src / "files" / side)
            if theirs:
                root, files, came = src / "files" / side, theirs, src.name
                plan["notes"].append(
                    f"files/{side}/ is {'empty' if own.is_dir() else 'absent'}: "
                    f"taking its {len(files)} file(s) from {src.name}")
        sides[side] = {"root": root, "inherited_from": came,
                       "files": {rr.rel(root, f): f for f in files}}
        empty = [n for n, f in sides[side]["files"].items() if f.stat().st_size == 0]
        if empty:
            plan["warnings"].append(f"files/{side}/: {', '.join(empty)} is 0 bytes")
    return sides


def staged_in_first_run(plan: dict, side: str) -> set:
    """Names the first run had on disk. Only these can have been deleted by an
    editor; an entry the first run never staged is carried as it was."""
    root = plan["base_dir"] / "files" / side
    names = {rr.rel(root, f) for f in rr.visible(root)}
    sf = ((plan["base_bundle"].get("staged_files") or {}).get(side) or {})
    return names | {n for n, s in sf.items() if not str(s).startswith("FAILED")}


def differs(plan: dict, side: str, name: str, path: Path):
    """True / False against the first run's copy; None when it has none."""
    ref = plan["base_dir"] / "files" / side / name
    if not ref.is_file():
        return None
    if ref.stat().st_size != path.stat().st_size:
        return True
    return rr.sha256(ref) != rr.sha256(path)


# ------------------------------------------------------------ the response
def placeholder(unit: str, side: str, name: str) -> str:
    """The source URL of a file the platform does not hold. Distinct per file,
    so component 10's answer-key-points-at-an-input check cannot collide."""
    return f"rerun-local://{unit}/files/{side}/{name}"


def _out(b: dict, t: str) -> dict:
    s = ac.step(b, t)
    if s is None:
        s = b[f"step-{t}-rerun"] = {"type": t}
    if not isinstance(s.get("output"), dict):
        s["output"] = {}
    return s["output"]


def _sub(d: dict, key: str) -> dict:
    if not isinstance(d.get(key), dict):
        d[key] = {}
    return d[key]


def _shared(entries: list, key: str):
    vals = {e.get(key) for e in entries if isinstance(e, dict)}
    return vals.pop() if len(vals) == 1 else None


def patch(b: dict, meta: dict, views: dict, sides: dict, plan: dict) -> tuple[dict, dict]:
    """The first run's response with the version folder applied, in the
    response's own shape, so bundle_for reads it exactly as it read the first."""
    unit, prov = plan["unit"], plan["provenance"]
    b, meta = copy.deepcopy(b), copy.deepcopy(meta)

    out = _out(b, "PromptInput")
    if views["prompt"].strip() != (out.get("content") or "").strip():
        out["content"] = views["prompt"].strip()
    _out(b, "RubricCriteriaBuilder")["criteria"] = views["criteria"]

    md = _sub(meta, "metadata")
    for k, v in views["task"].items():
        if v != (md.get(k) or ""):
            md[k] = v or None

    cuo = _out(b, "ComputerUse")

    # inputs: the task initializer's file list
    tii = _sub(cuo, "taskInitializerInput")
    if not isinstance(tii.get("config"), list):
        tii["config"] = []
    local, staged = sides["inputs"]["files"], staged_in_first_run(plan, "inputs")
    kept, lists = set(), []
    for c in tii["config"]:
        params = c.get("parameters") if isinstance(c, dict) else None
        if not isinstance(params, dict) or not isinstance(params.get("files"), list):
            continue
        lists.append(params)
        keep = []
        for f in params["files"]:
            name = Path(f.get("path") or "").name
            if name in local:
                kept.add(name)
                if differs(plan, "inputs", name, local[name]):
                    f = {**f, "url": placeholder(unit, "inputs", name)}
                    prov["placeholders"].append({"side": "inputs", "file": name,
                                                 "why": "content differs from the first run"})
                keep.append(f)
            elif name in staged:
                prov["removed"]["inputs"].append(name)
            else:
                keep.append(f)
        params["files"] = keep
    added = [n for n in local if n not in kept]
    if added and not lists:
        tii["config"].append({"type": "download", "parameters": {"files": []}})
        lists.append(tii["config"][-1]["parameters"])
    for n in added:
        lists[0]["files"].append({"path": DESKTOP + n,
                                  "url": placeholder(unit, "inputs", n)})
        prov["placeholders"].append({"side": "inputs", "file": n, "why": "new file"})
    prov["added"]["inputs"] = added

    # expected: the verifier's answer key, and the result entries mirroring it
    ev = _sub(_sub(cuo, "verifierInput"), "evaluator")
    local, staged = sides["expected"]["files"], staged_in_first_run(plan, "expected")
    kept, keep, removed = set(), [], []
    for e in ac.as_list(ev.get("expected")):
        name = e.get("dest")
        if name in local:
            kept.add(name)
            if differs(plan, "expected", name, local[name]):
                e = {**e, "path": placeholder(unit, "expected", name)}
                prov["placeholders"].append({"side": "expected", "file": name,
                                             "why": "content differs from the first run"})
            keep.append(e)
        elif name in staged:
            removed.append(name)
        else:
            keep.append(e)
    added = [n for n in local if n not in kept]
    etype = _shared(keep, "type")
    for n in added:
        keep.append({"dest": n, "path": placeholder(unit, "expected", n),
                     **({"type": etype} if etype else {})})
        prov["placeholders"].append({"side": "expected", "file": n, "why": "new file"})
    ev["expected"] = keep
    prov["removed"]["expected"], prov["added"]["expected"] = removed, added

    # A deliverable the answer key gains or loses is one the agent must write
    # or no longer writes; keeping `result` in step is what the platform does.
    results = ac.as_list(ev.get("result"))
    res = [r for r in results if r.get("dest") not in removed]
    have, rtype = {r.get("dest") for r in res}, _shared(results, "type")
    for n in added:
        if n not in have:
            res.append({"dest": n, "path": DESKTOP + n,
                        **({"type": rtype} if rtype else {})})
            prov["verifier_result"]["added"].append(n)
    prov["verifier_result"]["removed"] = [r.get("dest") for r in results
                                          if r.get("dest") in removed]
    ev["result"] = res
    return b, meta


def synthetic(bb: dict) -> tuple[dict, dict, dict]:
    """A response rebuilt from the first run's bundle.json, for when its
    response.json is gone. Only the fields a version folder moves need to
    survive the trip; everything else is carried from the bundle as it is."""
    ver = bb.get("verifier") or {}
    crits = [{k: v for k, v in (
        ("id", c.get("id")), ("title", c.get("title")), ("weight", c.get("weight")),
        ("annotations", {"criteria_type": c.get("type"),
                         "criteria_category": c.get("category")})) if v is not None}
        for c in bb.get("criteria") or []]
    b = {
        "step-PromptInput": {"type": "PromptInput",
                             "output": {"content": bb.get("prompt")}},
        "step-RubricCriteriaBuilder": {"type": "RubricCriteriaBuilder",
                                       "output": {"criteria": crits}},
        "step-ComputerUse": {"type": "ComputerUse", "output": {
            "taskInitializerInput": {"config": [{"type": "download", "parameters": {
                "files": [{"path": f.get("path"), "url": f.get("url")}
                          for f in bb.get("input_files") or []]}}]},
            "verifierInput": {"evaluator": {
                "func": ver.get("func"),
                "expected": [{"dest": e.get("dest"), "path": e.get("url")}
                             for e in bb.get("expected_files") or []],
                "result": [dict(r) for r in ver.get("result") or []]}},
            "verifierOutput": {"evaluationScore": ver.get("self_check_score")}}},
    }
    os_on = ((bb.get("mechanical") or {}).get("10_gold_file_format") or {}).get("os_enabled") or []
    meta = {"metadata": {"domain": bb.get("domain"), "sub_domain": bb.get("sub_domain"),
                         **{k: "true" for k in os_on}}}
    return b, meta, {}


def bundle_from(b: dict, meta: dict, amet: dict, uid: str) -> dict:
    """audit_common.bundle_for over a response held in memory."""
    real = ac.load
    ac.load = lambda _uid: (b, meta, amet)
    try:
        return ac.bundle_for(uid)
    finally:
        ac.load = real


# ------------------------------------------------------------ the plan
def _name_in(f: dict) -> str:
    return Path(f.get("path") or "").name


def _name_exp(f: dict):
    return f.get("dest")


def crit_diff(old: list, new: list) -> dict:
    def key(c):
        return c.get("id") or ("title", c.get("title"))
    o, n = {key(c): c for c in old}, {key(c): c for c in new}
    changed = []
    for k, c in n.items():
        if k in o:
            f = {x: [o[k].get(x), c.get(x)] for x in CRIT_FIELDS if o[k].get(x) != c.get(x)}
            if f:
                changed.append({"n": c.get("n"), **f})
    same_set = set(o) == set(n)
    return {"criteria": [len(old), len(new)],
            "weight": [sum(c.get("weight") or 0 for c in old),
                       sum(c.get("weight") or 0 for c in new)],
            "added": [c.get("n") for k, c in n.items() if k not in o],
            "removed_first_run_n": [c.get("n") for k, c in o.items() if k not in n],
            "changed": changed,
            "reordered": same_set and [key(c) for c in old] != [key(c) for c in new]}


def changes(plan: dict, nb: dict) -> dict:
    bb, sides = plan["base_bundle"], plan["sides"]
    ch = {"prompt": ("changed" if (nb.get("prompt") or "").strip()
                     != (bb.get("prompt") or "").strip() else "unchanged"),
          "task": {k: [bb.get(k), nb.get(k)] for k in ("domain", "sub_domain")
                   if bb.get(k) != nb.get(k)},
          "rubric": crit_diff(bb.get("criteria") or [], nb.get("criteria") or [])}
    for side, key, name_of in (("inputs", "input_files", _name_in),
                               ("expected", "expected_files", _name_exp)):
        before = [name_of(f) for f in bb.get(key) or []]
        after = [name_of(f) for f in nb.get(key) or []]
        ch[side] = {"files": len(after),
                    "added": [n for n in after if n not in before],
                    "removed": [n for n in before if n not in after],
                    "modified": [n for n, p in sides[side]["files"].items()
                                 if n in before and differs(plan, side, n, p)]}
    bm = bb.get("mechanical") or {}
    ch["mechanical"] = {k: [(bm.get(k) or {}).get("score"), v.get("score")]
                        for k, v in (nb.get("mechanical") or {}).items()
                        if (bm.get(k) or {}).get("score") != v.get("score")}
    was = (bb.get("agent_runs") or {}).get("rubric_stale")
    now = (nb.get("agent_runs") or {}).get("rubric_stale")
    if was != now:
        ch["agent_runs_rubric_stale"] = [was, now]
    return ch


def fingerprint(core: dict, sides: dict) -> str:
    """Everything the components will be shown: the bundle minus the prepare
    run's own records, and the bytes of every staged file."""
    h = hashlib.sha256(json.dumps(core, sort_keys=True, default=str).encode())
    for side in rr.SIDES:
        for name, p in sorted(sides[side]["files"].items()):
            h.update(f"\0{side}/{name}\0{rr.sha256(p)}".encode())
    return h.hexdigest()


def build(d: Path, base: str | None = None) -> dict:
    """Everything prepare would write, worked out without writing anything."""
    plan = {"unit": d.name, "dir": d, "errors": [], "warnings": [], "notes": [],
            "provenance": {"placeholders": [],
                           "added": {"inputs": [], "expected": []},
                           "removed": {"inputs": [], "expected": []},
                           "verifier_result": {"added": [], "removed": []}}}
    err, warn = plan["errors"].append, plan["warnings"].append
    if not d.is_dir():
        err(f"{d}: no such folder")
        return plan
    if base is None:
        s = rr.split_unit(d.name)
        if s is None and rr.is_first_run(d):
            err(f"{d.name} is a first run. A rerun goes in a version folder "
                f"beside it: python3 {VERSIONS} new {d.name}")
            return plan
        if s is None:
            err(f"{d.name}: no first run to rerun from. A version folder is "
                f"named <task_id>-v<N>, and audit/<task_id>/ must hold that "
                f"task's first audit (cua-audit-components), bundle.json included.")
            return plan
        base = s[0]
    if base == d.name:
        err(f"{d.name} is the first run itself. A rerun goes in a version "
            f"folder beside it: python3 {VERSIONS} new {d.name}")
        return plan
    base_dir = rr.AUDIT / base
    bb = rr.read_json(base_dir / "bundle.json")
    if not isinstance(bb, dict):
        err(f"{base}: no readable bundle.json in {base_dir}. The first audit "
            f"(cua-audit-components) has to run before any rerun.")
        return plan
    if not rr.is_first_run(base_dir):
        warn(f"{base} is itself a rerun; the fields it carried came from its own first run")
    if not (base_dir / rr.SUMMARY).exists():
        warn(f"{base} has no {rr.SUMMARY}: its first audit never finished. That "
             f"run belongs to cua-audit-components; this one proceeds from its bundle.json.")
    suffix = d.name[len(base) + 1:] if d.name.startswith(base + "-") else ""
    plan.update(base=base, base_dir=base_dir, base_bundle=bb,
                version=rr.version_of(suffix))

    views = read_views(d, plan)
    if plan["errors"]:
        return plan
    sides = plan["sides"] = collect_sides(d, plan)

    try:
        raw = ac.load(base)
        plan["source"] = str(ac.unit_dir(base) / "response.json")
    except FileNotFoundError:
        raw = None
    except Exception as e:                                   # noqa: BLE001
        raw = None
        warn(f"{base}: its response.json could not be read ({type(e).__name__}: "
             f"{e}); falling back to the first run's bundle.json")

    if raw is not None:
        b, meta, amet = raw
        nb = bundle_from(*patch(b, meta, views, sides, plan), amet, base)
        drift = [k for k, v in bundle_from(b, meta, amet, base).items()
                 if k not in RUN_KEYS and bb.get(k) != v]
        if drift:
            warn(f"the first run's bundle.json differs from what the current "
                 f"pipeline builds from {plan['source']} ({', '.join(drift)}): "
                 f"the response or the pipeline changed since the first run. "
                 f"The rerun uses the current build.")
        plan["agent_runs"] = "re-judged against this version's rubric"
    else:
        sb, smeta, samet = synthetic(bb)
        s = bundle_from(*patch(sb, smeta, views, sides, plan), samet, base)
        nb = {k: v for k, v in bb.items() if k not in RUN_KEYS}
        for k in FOLDER_KEYS + ("mechanical",):
            nb[k] = s[k]
        plan["source"] = (f"{base_dir / 'bundle.json'} (no response.json under "
                          f"{ac.TASKS} or {ac.ATTEMPTS})")
        plan["agent_runs"] = "the first run's record, as it was"
        plan["notes"].append("agent_runs is the first run's record: without "
                             "its response.json it cannot be re-judged against this rubric")

    core = {k: v for k, v in nb.items() if k not in RUN_KEYS}
    plan["core"] = core
    plan["changes"] = changes(plan, core)
    plan["fingerprint"] = fingerprint(core, sides)
    return plan


def _w(x) -> str:
    return str(int(x)) if float(x).is_integer() else f"{x:g}"


def describe(plan: dict) -> list[str]:
    ch = plan["changes"]
    out = [f"changes vs {plan['base']} (first run):",
           f"  prompt      {ch['prompt']}",
           "  task        " + ("; ".join(f"{k} {v[0]!r} -> {v[1]!r}"
                                       for k, v in ch["task"].items()) or "unchanged")]
    r = ch["rubric"]
    (n0, n1), (w0, w1) = r["criteria"], r["weight"]
    head = (f"{n0} -> {n1} criteria, weight {_w(w0)} -> {_w(w1)}"
            if (n0, w0) != (n1, w1) else f"{n1} criteria, weight {_w(w1)}")
    parts = []
    if r["added"]:
        parts.append("added #" + ", #".join(map(str, r["added"])))
    if r["removed_first_run_n"]:
        parts.append("removed first-run #" + ", #".join(map(str, r["removed_first_run_n"])))
    for c in r["changed"][:6]:
        parts.append(f"#{c['n']} " + ", ".join(
            "title reworded" if k == "title" else f"{k} {v[0]!r} -> {v[1]!r}"
            for k, v in c.items() if k != "n"))
    if len(r["changed"]) > 6:
        parts.append(f"{len(r['changed']) - 6} more changed")
    if r["reordered"]:
        parts.append("reordered")
    out.append(f"  rubric      {head}" + (": " + "; ".join(parts) if parts else ", unchanged"))
    for side in rr.SIDES:
        s = ch[side]
        parts = [f"{k} {', '.join(s[k])}" for k in ("added", "removed", "modified") if s[k]]
        out.append(f"  {side:<11} {s['files']} file(s)"
                   + (": " + "; ".join(parts) if parts else ", unchanged"))
    m = ch["mechanical"]
    out.append("  mechanical  " + (", ".join(f"{k[:2]} {v[0]} -> {v[1]}" for k, v in m.items())
                                   or "unchanged"))
    return out


def show(plan: dict) -> None:
    if plan["errors"]:
        for e in plan["errors"]:
            print(f"  error: {e}")
        return
    v = plan["version"]
    print(f"{plan['unit']}: rerun{' v' + str(v) if v else ''} of {plan['base']}, "
          f"platform record from {plan['source']}")
    for n in plan["notes"]:
        print(f"  note: {n}")
    for w in plan["warnings"]:
        print(f"  warning: {w}")
    for line in describe(plan):
        print("  " + line)
    ph = plan["provenance"]["placeholders"]
    if ph:
        print(f"  {len(ph)} file(s) not on the platform get a rerun-local:// source "
              f"URL: " + ", ".join(f"{p['side']}/{p['file']} ({p['why']})" for p in ph))


# ------------------------------------------------------------ writing
def extract(python: Path, d: Path) -> dict:
    """audit_prepare.extract minus dotfiles: extract_files.py reads every file
    under a side folder, and a .DS_Store is not part of the submission."""
    res = {}
    for side in rr.SIDES:
        src, dest = d / "files" / side, d / f"{side}_extracted.md"
        files = rr.visible(src)
        with tempfile.TemporaryDirectory(prefix="cua-rerun-") as tmp:
            arg = src
            if src.is_dir() and len(files) != sum(1 for p in src.rglob("*") if p.is_file()):
                arg = Path(tmp) / side
                arg.mkdir()
                for f in files:
                    t = arg / rr.rel(src, f)
                    t.parent.mkdir(parents=True, exist_ok=True)
                    os.symlink(f.resolve(), t)
            try:
                p = subprocess.run([str(python), str(ap.EXTRACTOR), str(arg), str(dest)],
                                   capture_output=True, text=True, timeout=600)
                res[side] = "ok" if p.returncode == 0 else f"FAILED {p.stderr[-200:]}"
            except subprocess.TimeoutExpired:
                res[side] = "FAILED timeout"
    return res


def staged(bundle: dict, d: Path, files: dict | None = None) -> dict:
    """audit_prepare's staged_files record, for files already on disk: in d,
    or where files ({side: {name: path}}) says, before prepare copies them in."""
    rep = {"inputs": {}, "expected": {}}
    for side, key, name_of in (("inputs", "input_files", _name_in),
                               ("expected", "expected_files", _name_exp)):
        for f in bundle.get(key) or []:
            name = name_of(f)
            if not name:
                continue
            p = d / "files" / side / name if files is None else files[side].get(name)
            if p is not None and p.is_file() and p.stat().st_size > 0:
                rep[side][name] = "cached"
            elif p is not None and p.is_file():
                rep[side][name] = "FAILED empty file (0 bytes)"
            elif str(f.get("url") or "").startswith("http"):
                rep[side][name] = "FAILED not in the version folder"
    return rep


def write_manifest(plan: dict, bundle: dict, rendered: bool) -> None:
    r = bundle.get("renders") or {}
    needs = r.get("needs") or {}
    carried = [k for k in bundle if k not in FOLDER_KEYS + DERIVED_KEYS + RUN_KEYS]
    man = {
        "unit": plan["unit"],
        "first_run": plan["base"],
        "version": plan["version"],
        "task_id": bundle.get("task_id"),
        "prepared_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "fingerprint": plan["fingerprint"],
        "rendered": bool(rendered and r.get("status") == "ok"),
        "renderers_missing": (needs.get("install") or []) + (needs.get("off_version") or []),
        "platform_record": plan["source"],
        "from_this_folder": {
            "prompt.md": "prompt",
            "rubric.json": "criteria",
            "task.md": "domain, sub_domain",
            "files/inputs/": "input_files",
            "files/expected/": "expected_files, verifier.result",
        },
        "recomputed": {"mechanical": "from this folder, by audit_common.mechanical",
                       "agent_runs": plan["agent_runs"]},
        "carried_from_platform_record": carried + ["verifier.func",
                                                   "verifier.self_check_score"],
        "files": {side: {"from": (f"copied from {s['inherited_from']}"
                                  if s["inherited_from"] else "this folder"),
                         "names": sorted(s["files"])}
                  for side, s in plan["sides"].items()},
        "placeholders": plan["provenance"]["placeholders"],
        "removed_vs_first_run": plan["provenance"]["removed"],
        "verifier_result": plan["provenance"]["verifier_result"],
        "changes_vs_first_run": plan["changes"],
        "notes": plan["notes"],
        "warnings": plan["warnings"],
    }
    tmp = plan["dir"] / (rr.MANIFEST + ".tmp")
    tmp.write_text(ac.dumps(man) + "\n", encoding="utf-8")
    os.replace(tmp, plan["dir"] / rr.MANIFEST)


def summarise(plan: dict, bundle: dict) -> None:
    """The line audit_prepare prints, for the version folder."""
    mech = bundle["mechanical"]
    fails = [k for k, v in mech.items() if v["score"] == 2]
    minors = [k for k, v in mech.items() if v["score"] in (3, 4)]
    sf = bundle.get("staged_files") or {}
    nbad = sum(1 for x in sf.values() for v in x.values() if v.startswith("FAILED"))
    v = plan["version"]
    print(f"{plan['unit']} (rerun{' v' + str(v) if v else ''} of {plan['base']}): "
          f"{len(bundle['criteria'])} criteria, domain={bundle['domain']!r}, "
          f"mech fails={fails or '-'} minors={minors or '-'}, "
          f"files={sum(len(x) for x in sf.values())} ({nbad} failed), "
          f"wrote bundle.json, the extracts"
          + (", the renders" if "renders" in bundle else "") + f" and {rr.MANIFEST}")
    r = bundle.get("renders") or {}
    if r.get("status") == "ok":
        print(f"  render: {r['pages_rendered']} page(s), "
              f"{r['visual_verifiable']} visual-verifiable, "
              f"{r['degraded']} degraded, {r['unavailable']} unavailable"
              + ("" if r["parity_ok"] else "  ⚠ renderer parity gap"))
        for w in r.get("parity_warnings") or []:
            print(f"    parity: {w}")
        if (r.get("needs") or {}).get("provision_command"):
            print(f"  for this version folder, install and re-render with:\n"
                  f"    python3 {Path(__file__).resolve()} {plan['unit']} --provision --rebuild")
    elif r:
        print(f"  render: {r.get('status')}")


def prepare(plan: dict, provision: bool = False, render: bool = True,
            rebuild: bool = False, reset: bool = False) -> int:
    d, unit, fp = plan["dir"], plan["unit"], plan["fingerprint"]
    # extract_files.py and render_files.py refuse a version folder unless this names it.
    os.environ[ac.RERUN_ENV] = unit
    man = rr.own_manifest(d)
    review = rr.present(d, rr.REVIEW)
    if man is None:
        foreign = rr.present(d, rr.EVIDENCE + rr.REVIEW)
        if foreign:
            rr.remove(d, foreign)
            print(f"  cleared {', '.join(foreign)}: {unit} was never prepared by "
                  f"cua-audit-rerun, so these came with a copy of another run and "
                  f"describe that run's evidence, not this folder's")
    else:
        if (d / rr.SUMMARY).exists() and not reset:
            print(f"  {unit} already has a finished audit ({rr.SUMMARY}), and a "
                  f"version is audited once so its report keeps describing it.\n"
                  f"    audit the next version (a copy of this one's views and files):\n"
                  f"      python3 {VERSIONS} new {plan['base']} --from {unit}\n"
                  f"    or discard this version's results and audit it again: add --reset")
            return 3
        if review and man.get("fingerprint") != fp and not reset:
            print(f"  {unit} holds review outputs ({', '.join(review)}) produced "
                  f"before the folder last changed. Resuming would score this "
                  f"version partly on another version's evidence.\n"
                  f"    add --reset to discard them and start its review over")
            return 3
        if reset and review:
            rr.remove(d, review)
            print(f"  discarded this version's review outputs: {', '.join(review)}")
        current = (man.get("fingerprint") == fp
                   and all((d / n).is_file() for n in
                           ("bundle.json", "inputs_extracted.md", "expected_extracted.md"))
                   and (not render or (man.get("rendered")
                                       and (d / "render_index.json").is_file()))
                   and not (provision and man.get("renderers_missing")))
        if current and not rebuild:
            print(f"{unit}: evidence up to date (prepared {man.get('prepared_at')}); "
                  f"--rebuild redoes it")
            return 0

    for side in rr.SIDES:
        s, dest = plan["sides"][side], d / "files" / side
        dest.mkdir(parents=True, exist_ok=True)
        if s["inherited_from"]:
            for name, src in s["files"].items():
                t = dest / name
                t.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, t)
            print(f"  files/{side}/: copied {len(s['files'])} file(s) in from "
                  f"{s['inherited_from']}")
            s["root"], s["files"] = dest, {n: dest / n for n in s["files"]}

    python, pyrec = ac.reader_python()
    if pyrec.get("created") or pyrec.get("installed"):
        print(f"  readers ready: {pyrec['python']}")
    if not pyrec["status"].startswith("ok"):
        print(f"  readers {pyrec['status']}")

    bundle = dict(plan["core"])
    bundle["readers"] = pyrec
    bundle["staged_files"] = staged(bundle, d)
    bundle["extracted"] = extract(python, d)
    # Pages of a file the folder no longer holds must not outlive it, and an
    # index without its pages would pass run_review's render gate.
    rr.remove(d, ["render", "render_index.json"])
    if render:
        bundle["renders"] = ap.render(python, d, provision)
    (d / "bundle.json").write_text(ac.dumps(bundle), encoding="utf-8")
    write_manifest(plan, bundle, render)
    summarise(plan, bundle)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Rebuild a version folder's evidence for cua-audit-components.")
    p.add_argument("unit", help="version folder: <task_id>-vN, audit/<task_id>-vN or a path")
    p.add_argument("--base", help="first-run unit to rerun from "
                                  "(default: the folder name's <task_id> prefix)")
    p.add_argument("--provision", action="store_true",
                   help="install any renderer these files need, at the version "
                        "cua-applications.csv pins, before rendering")
    p.add_argument("--no-render", action="store_true",
                   help="skip rasterising (visual findings will be UNVERIFIABLE)")
    p.add_argument("--rebuild", action="store_true",
                   help="rebuild the evidence even when it is up to date")
    p.add_argument("--reset", action="store_true",
                   help="discard this version's review outputs first")
    p.add_argument("--check", action="store_true",
                   help="validate the folder and show what changed; write nothing")
    a = p.parse_args(argv)

    plan = build(rr.resolve_dir(a.unit), a.base)
    show(plan)
    if plan["errors"]:
        return 2
    if a.check:
        return 0
    return prepare(plan, a.provision, not a.no_render, a.rebuild, a.reset)


if __name__ == "__main__":
    raise SystemExit(main())
