#!/usr/bin/env python3
"""Shared helpers for the CUA task audit: task-response step access, the
mechanical pre-pass, and workspace paths."""
from __future__ import annotations

import json
import os
import re
import statistics
import subprocess
import sys
from pathlib import Path

# Portable: CUA_AUDIT_HOME wins, else the repo root above this skill, else cwd.
WORKSPACE = Path(os.environ.get("CUA_AUDIT_HOME")
                 or Path(__file__).resolve().parents[3]).expanduser()
TASKS = WORKSPACE / "tasks"
ATTEMPTS = WORKSPACE / "attempts"
AUDIT = WORKSPACE / "audit"


def dumps(obj, indent: int | None = 1) -> str:
    """JSON with every character written as itself: `±`, not `\\u00b1`.

    People read these files, copy criteria out of them and edit the views by
    hand, and an escape reaches all three as six characters. Besides what JSON
    itself must escape (quotes, backslashes, control characters), the one
    character left escaped is a lone surrogate, which UTF-8 cannot encode.
    Write the result with encoding="utf-8".
    """
    return json.dumps(obj, indent=indent, ensure_ascii=False).encode(
        "utf-8", "backslashreplace").decode("utf-8")


# ----------------------------------------------------------- the reader venv
# Extraction and rendering read Office and PDF files through five wheels and
# no system package at all, so the workspace venv is the entire dependency
# story. Import name -> distribution, because the two differ often enough.
VENV = WORKSPACE / ".venv"
VENV_PY = VENV / "bin" / "python"
READERS = {"openpyxl": "openpyxl", "docx": "python-docx", "pptx": "python-pptx",
           "pdfplumber": "pdfplumber", "fitz": "pymupdf", "PIL": "pillow"}

_READER: tuple[Path, dict] | None = None


def _sh(cmd: list[str], timeout: int) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stderr or p.stdout).strip()[-300:]
    except (OSError, subprocess.SubprocessError) as exc:        # noqa: BLE001
        return 127, f"{type(exc).__name__}: {exc}"[:300]


def unimportable(python: Path, modules=READERS) -> list[str]:
    """Which of `modules` that interpreter cannot import."""
    code = ("import importlib.util as u, sys; "
            "print(' '.join(m for m in sys.argv[1:] if u.find_spec(m) is None))")
    try:
        p = subprocess.run([str(python), "-c", code, *modules],
                           capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return list(modules)
    return p.stdout.split() if p.returncode == 0 else list(modules)


def _build_reader_python(log) -> tuple[Path, dict]:
    rec: dict = {"created": False, "installed": [], "missing": [], "status": "ok"}

    python = VENV_PY
    if not python.is_file():
        log(f"  no reader venv at {VENV} — creating it")
        _sh([sys.executable, "-m", "venv", str(VENV)], 600)
        if VENV_PY.is_file():
            rec["created"] = True
        else:
            # A host whose python3-venv is absent may still carry the wheels.
            python = Path(sys.executable)
            rec["venv_error"] = f"could not create {VENV}"
            log(f"  could not create it — falling back to {python}")
    rec["python"] = str(python)

    missing = unimportable(python)
    if missing:
        pkgs = sorted({READERS[m] for m in missing})
        log(f"  installing document readers: {', '.join(pkgs)}")
        code, err = _sh([str(python), "-m", "pip", "install", "--quiet",
                         "--disable-pip-version-check", *pkgs], 1800)
        rec["installed"] = pkgs
        if code != 0:
            rec["pip_error"] = err
        missing = unimportable(python)

    rec["missing"] = sorted(READERS[m] for m in missing)
    if missing:
        rec["status"] = (f"partial — {', '.join(rec['missing'])} still not "
                         f"importable under {python}; files needing them will "
                         f"report COULD NOT READ rather than be scored")
    return python, rec


def reader_python(log=print) -> tuple[Path, dict]:
    """An interpreter that can read Office and PDF files, built if absent.

    Everything the prepare step imports is a wheel, so a missing reader is not
    a decision for anyone to make — it is a venv and a pip install. Stopping
    to ask for one costs a round trip and leaves the review subagents with no
    extracted text and no rendered pages, which is the one failure this
    pipeline cannot absorb: they would score a deliverable they never saw.

    Always returns an interpreter, so a host that is only partly equipped
    still extracts and renders what it can. The record travels into
    `bundle.json`, which is where a half-equipped run has to be visible.
    """
    global _READER
    if _READER is None:
        _READER = _build_reader_python(log)
    return _READER


def unit_dir(uid: str) -> Path:
    """An audit unit is either a task (latest attempt) or a specific attempt."""
    for root in (TASKS, ATTEMPTS):
        if (root / uid / "response.json").exists():
            return root / uid
    raise FileNotFoundError(
        f"{uid}: no response.json under {TASKS} or {ATTEMPTS} — place the "
        f"task files in one of those directories (see "
        f"references/task-response-format.md for the expected shape)")


def all_units() -> list[str]:
    out = []
    for root in (TASKS, ATTEMPTS):
        if root.exists():
            out += sorted(p.name for p in root.iterdir()
                          if (p / "response.json").exists())
    return out


# ----------------------------------------------- the first audit, then reruns
# A unit's first audit is this skill's. Once audit/<unit>/component_review_summary.html
# exists, every later audit of that submission is a version folder,
# audit/<unit>-v2/ and on, that the sibling skill cua-audit-rerun drives
# through these same scripts, naming the folder it drives in RERUN_ENV.
REPORT = "component_review.html"
SUMMARY = "component_review_summary.html"
RERUN_MANIFEST = "_rerun.json"
RERUN_ENV = "CUA_AUDIT_RERUN_UNIT"
RERUN_SCRIPTS = Path(__file__).resolve().parents[2] / "cua-audit-rerun" / "scripts"


def version_base(unit: str) -> str | None:
    """The first run a cua-audit-rerun version folder belongs to, else None."""
    for i, ch in enumerate(unit):
        if ch == "-" and 0 < i < len(unit) - 1:
            base = AUDIT / unit[:i]
            if (base / "bundle.json").is_file() and not (base / RERUN_MANIFEST).exists():
                return unit[:i]
    manifest = AUDIT / unit / RERUN_MANIFEST
    if manifest.is_file():
        try:
            return json.loads(manifest.read_text(encoding="utf-8")).get("first_run") or "another unit"
        except ValueError:
            return "another unit"
    return None


def current(d: Path, name: str) -> bool:
    """`name` exists in d and is at least as new as every result it is built from."""
    out = d / name
    if not out.is_file():
        return False
    sources = [*(d / "components").glob("[0-9][0-9].json"), d / "bundle.json",
               d / "input_consistency.json", d / "sense_check.json"]
    newest = max((p.stat().st_mtime for p in sources if p.is_file()), default=0)
    return out.stat().st_mtime >= newest


def locked(unit: str, script: str, replaces: bool = True) -> str | None:
    """Why `script` must not write `unit`, or None when it may.

    A finished first audit can still be completed — a component, pass, report
    or summary it lacks — but nothing it already has is redone here, because
    its report describes that evidence and those results. `replaces` says
    whether this run would overwrite something the audit already has.
    """
    base = version_base(unit)
    if base is not None:
        if os.environ.get(RERUN_ENV) == unit:
            return None
        return (f"{unit} is a version folder of {base}, and only cua-audit-rerun "
                f"audits it:\n  python3 {RERUN_SCRIPTS / 'rerun.py'} {unit}")
    if replaces and (AUDIT / unit / SUMMARY).is_file():
        return (f"{unit}: its first audit is finished ({SUMMARY} exists), and "
                f"{script} would redo part of it. Every later audit of it runs "
                f"through cua-audit-rerun:\n"
                f"  python3 {RERUN_SCRIPTS / 'rerun_versions.py'} status {unit}")
    return None


def admit(units: list[str], script: str, named: bool,
          replaces=lambda unit: True) -> list[str] | None:
    """The units `script` may write. A locked unit the caller named stops the
    run (None, after saying why); a locked unit a sweep found is skipped."""
    refused = {}
    for u in units:
        why = locked(u, script, replaces(u))
        if why:
            refused[u] = why
    if refused and named:
        print("\n".join(refused.values()))
        return None
    if refused:
        print(f"  skipped (a finished first audit, or a cua-audit-rerun version "
              f"folder): {', '.join(refused)}")
    return [u for u in units if u not in refused]

BREAKDOWN = re.compile(
    r"\[(must-pass|regular)\]\s+(.*?):\s+score=([\d.]+)\s+weight=([\d.]+)\s+"
    r"contribution=([\d.]+)\s*(PASS|FAIL)?", re.S)

# Bands are (min, max) inclusive; None = unbounded on that side.
BANDS = {
    "default":          {"format_gate": (None, 20), "correctness": (50, None), "visual": (20, 30)},
    "Design & Creative": {"format_gate": (None, 20), "correctness": (20, 30), "visual": (50, None)},
}

# Lower bounds the CSV states strictly (">"), not inclusively (">="). Only the
# default correctness floor is strict: "Correctness > 50%". source-conflicts.md
# §1 rules that exactly 50.0% is off band by 0 points, so the +/-5-point rule
# makes it Non-Fail (3) rather than a clean 5. Do not escalate a boundary case.
STRICT_LO = {("default", "correctness")}


# ------------------------------------------------------- task-response access
def load(task_id: str) -> tuple[dict, dict, dict]:
    """-> (before, task_meta, attempt_meta). attempt_meta is {} for task units."""
    d = unit_dir(task_id)
    resp = json.loads((d / "response.json").read_text(encoding="utf-8"))
    meta, amet = {}, {}
    if (d / "task_meta.json").exists():
        meta = json.loads((d / "task_meta.json").read_text(encoding="utf-8"))
    if (d / "attempt_meta.json").exists():
        amet = json.loads((d / "attempt_meta.json").read_text(encoding="utf-8"))
    return resp["before"], meta, amet


def steps(b: dict, t: str) -> list[dict]:
    return [s for s in b.values() if s.get("type") == t]


def step(b: dict, t: str) -> dict | None:
    s = steps(b, t)
    return s[0] if s else None


def field(b: dict, name: str):
    for s in b.values():
        if s.get("type") == "TextCollection" and name in (s.get("output") or {}):
            return s["output"][name]
    return None


def agent_run(b: dict) -> dict | None:
    for s in steps(b, "ExternalApp"):
        items = (s.get("output") or {}).get("items") or []
        data = ((items[0].get("content") or {}).get("data") or {}) if items else {}
        if "instances" in data:
            return data
    return None


def generated_rubric(b: dict):
    for s in steps(b, "ExternalApp"):
        items = (s.get("output") or {}).get("items") or []
        data = ((items[0].get("content") or {}).get("data") or {}) if items else {}
        if "criteria" in data:
            return data["criteria"]
    return None


def cds_to_https(url: str) -> str:
    m = re.match(r"scale-cds://([^/]+)/([^#]+)#s3/(.+)", url or "")
    return f"https://{m.group(3)}.s3.amazonaws.com/{m.group(1)}/{m.group(2)}" if m else url


def as_list(v):
    return [] if v is None else (v if isinstance(v, list) else [v])


# ---------------------------------------------------------------- runs
def _norm_title(t: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", (t or "").lower()).split())


def run_summary(b: dict, shipped_n: int, shipped_w: float,
                shipped_titles: list[str] | None = None) -> dict:
    """Per-run scores plus the judged-rubric shape.

    Staleness is decided on the SET OF JUDGED CRITERION TITLES, not on count and
    total weight: swapping one criterion for a reworded one of the same weight
    and category preserves both aggregates and would otherwise read as clean.
    Runs spanning more than one verification_id are flagged separately, because
    that means the run set straddles two task versions and its pooled mean
    measures neither.
    """
    ar = agent_run(b)
    if not ar:
        return {"present": False}
    runs, shapes, by_vid = [], set(), {}
    for inst in ar.get("instances", []):
        ctx = inst.get("context") or {}
        for vid, v in ((ctx.get("metadata") or {}).get("verifications") or {}).items():
            if v.get("score") is None:
                continue
            msg = v["results"][0]["results"][0].get("message", "")
            rows = BREAKDOWN.findall(msg)
            jw = sum(float(r[3]) for r in rows)
            titles = frozenset(_norm_title(r[1]) for r in rows)
            shapes.add((len(rows), jw))
            by_vid.setdefault(vid, []).append(v["score"])
            runs.append({
                "instance_id": inst.get("instance_id"),
                "status": inst.get("status"),
                "verification_id": vid,
                "score": v["score"],
                "judged_criteria": len(rows),
                "judged_weight": jw,
                "judged_titles": sorted(titles),
                "missed": [{"type": r[0], "title": r[1].strip(), "score": float(r[2]),
                            "weight": float(r[3])} for r in rows if float(r[2]) < 1.0],
            })
    prompts = {pr.get("prompt_text") for inst in ar.get("instances", [])
               for pr in ((inst.get("context") or {}).get("prompt_responses") or [])}
    scores = [r["score"] for r in runs]

    shipped_set = frozenset(_norm_title(t) for t in (shipped_titles or []))
    judged_sets = {frozenset(r["judged_titles"]) for r in runs}
    reasons, unmatched = [], []
    if runs:
        if len(judged_sets) > 1:
            reasons.append(f"runs used {len(judged_sets)} different judged rubrics")
        if len(by_vid) > 1:
            reasons.append(f"runs span {len(by_vid)} verification_ids "
                           f"(two task versions)")
        if shipped_set:
            for js in judged_sets:
                missing = shipped_set - js
                extra = js - shipped_set
                if missing or extra:
                    unmatched.append({"judged_not_shipped": sorted(extra)[:8],
                                      "shipped_not_judged": sorted(missing)[:8]})
            if unmatched:
                reasons.append("judged criterion titles differ from the shipped "
                               "rubric")
        if runs[0]["judged_criteria"] != shipped_n or \
                abs(runs[0]["judged_weight"] - shipped_w) > 0.5:
            reasons.append(f"judged {runs[0]['judged_criteria']} criteria / "
                           f"weight {runs[0]['judged_weight']:.0f} vs shipped "
                           f"{shipped_n} / {shipped_w:.0f}")

    return {
        "present": True,
        "n_instances": len(ar.get("instances", [])),
        "n_scored": len(runs),
        "mean_score": statistics.mean(scores) if scores else None,
        "mean_by_verification": {k: round(statistics.mean(v), 4)
                                 for k, v in by_vid.items()},
        "runs": runs,
        "rubric_versions": sorted(shapes),
        "rubric_stale": bool(reasons),
        "stale_reasons": reasons,
        "title_diff": unmatched[:2],
        "run_prompts": sorted(p for p in prompts if p),
    }


# ---------------------------------------------------------------- mechanical
def mechanical(b: dict, meta: dict) -> dict:
    """The six mechanically decidable dimensions. Subagents receive these and
    must not re-derive them."""
    out: dict[str, dict] = {}
    md = meta.get("metadata") or {}
    domain = (md.get("domain") or "").strip()

    prompt = (step(b, "PromptInput") or {}).get("output", {}).get("content", "") or ""
    cu = step(b, "ComputerUse") or {}
    ev = ((cu.get("output") or {}).get("verifierInput") or {}).get("evaluator") or {}
    crits = ((step(b, "RubricCriteriaBuilder") or {}).get("output") or {}).get("criteria") or []

    results = as_list(ev.get("result"))
    expected = as_list(ev.get("expected"))
    init_files = [f for c in (((cu.get("output") or {}).get("taskInitializerInput") or {})
                              .get("config") or [])
                  for f in (c.get("parameters") or {}).get("files", []) or []]

    # component 06 — Prompt - Output Naming
    unnamed = [r.get("dest") for r in results
               if r.get("dest") and r["dest"].lower() not in prompt.lower()]
    desktop = bool(re.search(r"\bdesktop\b", prompt, re.I))
    out["06_prompt_output_naming"] = {
        "score": 2 if (unnamed or not desktop) else 5,
        "unnamed_outputs": unnamed,
        "states_desktop": desktop,
    }

    # component 10 — Gold File - Format (the ground-truth-URL clause)
    in_urls = {f.get("url") for f in init_files}
    points_at_input = [e.get("dest") for e in expected if e.get("path") in in_urls]
    os_enabled = [k for k in ("windows", "ubuntu", "mac") if str(md.get(k)).lower() == "true"]
    out["10_gold_file_format"] = {
        "score": 2 if points_at_input else 5,
        "gt_url_points_at_input": points_at_input,
        "expected_exts": sorted({(e.get("dest") or "").rsplit(".", 1)[-1].lower()
                                 for e in expected if e.get("dest")}),
        "os_enabled": os_enabled,
    }

    # component 25 — Rubric - Count
    n = len(crits)
    out["25_rubric_count"] = {"score": 2 if (n < 10 or n > 30) else 5, "n_criteria": n}

    # component 24 — Rubric - Individual Criteria Weights
    #
    # A field that is PRESENT and wrong is a contributor defect. A field absent
    # from every criterion means it was never handed to us, which is a bundle
    # defect: it suppresses the band rather than failing it, and is reported
    # under `bundle_defects`. A weight present and outside [1, 50] still fails.
    weights_absent = bool(crits) and all(c.get("weight") is None for c in crits)
    bad_range = [] if weights_absent else [
        i for i, c in enumerate(crits, 1)
        if not (isinstance(c.get("weight"), int) and 1 <= c["weight"] <= 50)]
    mistagged, missing_ann = [], []
    for i, c in enumerate(crits, 1):
        a = c.get("annotations") or {}
        cat, typ = a.get("criteria_category"), a.get("criteria_type")
        if cat is None or typ is None:
            missing_ann.append({"c": i, "missing": [k for k, v in
                                                    (("criteria_category", cat),
                                                     ("criteria_type", typ)) if v is None]})
        elif typ == "MUST-PASS" and cat != "format_gate":
            mistagged.append({"c": i, "why": f"MUST-PASS on {cat}"})
    n_bad = len(mistagged)          # missing_ann is a bundle defect, not scored
    bundle, not_run = [], []
    if weights_absent:
        bundle.append("no criterion carries a `weight` field")
        not_run += ["per-criterion weight", "category weight share"]
    if missing_ann:
        bundle.append(f"{len(missing_ann)} criteria arrived with no "
                      f"criteria_category / criteria_type")
        not_run.append("MUST-PASS / REGULAR tagging")
    out["24_rubric_individual_criteria_weights"] = {
        "score": 2 if bad_range else (5 if n_bad == 0 else 3),
        "weights_out_of_range": bad_range,
        "type_mistags": mistagged,
        "missing_annotations": missing_ann,
        "bundle_defects": bundle,
        "bands_not_run": sorted(set(not_run)),
        "n_must_pass": sum(1 for c in crits
                           if (c.get("annotations") or {}).get("criteria_type") == "MUST-PASS"),
        "note": "MUST-PASS legitimacy needs a human read of each gate's title "
                "(audit-rubric component 24): MUST-PASS is reserved for the file itself / correct extension. "
                "`bundle_defects` are NOT scored — an absent weight or annotation was never supplied, "
                "so the band did not run: report it in blocked_on and lower confidence.",
    }

    # component 23 — Rubric - Weight Share
    total = sum(c.get("weight", 0) for c in crits)
    by = {"format_gate": 0, "correctness": 0, "visual": 0}
    for c in crits:
        cat = (c.get("annotations") or {}).get("criteria_category")
        if cat in by:
            by[cat] += c.get("weight", 0)
    band_used = "Design & Creative" if domain in BANDS and domain != "default" else "default"
    band = BANDS.get(domain, BANDS["default"])
    shares, offs = {}, []
    for cat, w in by.items():
        pct = round(100 * w / total, 2) if total else 0.0
        shares[cat] = pct
        lo, hi = band[cat]
        off, at_edge = 0.0, False
        if lo is not None:
            if pct < lo:
                off = lo - pct
            elif pct == lo and (band_used, cat) in STRICT_LO:
                at_edge = True          # exactly on a ">" floor: off band by 0
        if hi is not None and pct > hi:
            off = pct - hi
        if off > 0 or at_edge:
            offs.append({"category": cat, "pct": pct, "band": [lo, hi],
                         "off_by": round(off, 2), "at_strict_edge": at_edge})
    worst = max((o["off_by"] for o in offs), default=0.0)
    out["23_rubric_weight_share"] = {
        # An off-band share of 0 points is still off band -> Non-Fail (3).
        "score": 2 if worst > 5 else (3 if offs else 5),
        "domain": domain or None,
        "band_used": band_used,
        "shares_pct": shares,
        "total_weight": total,
        "off_band": offs,
        "note": "Only 'Design & Creative' inverts; every other domain, including "
                "Multimedia & A/V, uses the default bands. Where a Multimedia & A/V "
                "task lands off band, flag rather than fail (source-conflicts.md §4).",
    }

    # component 28 — JSON - Structure / URL Integrity
    exp_d = {e.get("dest") for e in expected}
    res_d = {r.get("dest") for r in results}

    def _expiring(u):
        u = u or ""
        return "Expires=" in u or "X-Amz-Signature" in u

    # The component covers BOTH JSONs: the verifier and the task initializer.
    # An expiring link in either one fails it.
    signed = [e.get("path") for e in expected if _expiring(e.get("path"))]
    signed_init = [f.get("url") for f in init_files if _expiring(f.get("url"))]
    bad_paths = [r.get("path") for r in results
                 if not (r.get("path") or "").startswith("/home/docker/Desktop/")]
    out["28_json_structure_url_integrity"] = {
        "score": 2 if (ev.get("func") != "agent_judge_multi" or exp_d != res_d
                       or signed or signed_init or bad_paths) else 5,
        "func": ev.get("func"),
        "dest_mismatch": sorted(exp_d ^ res_d),
        "signed_urls_verifier": signed,
        "signed_urls_initializer": signed_init,
        "result_paths_off_desktop": bad_paths,
        "note": "The verifier SCORE is not graded by QC — a 0 is expected. An "
                "expiring URL may be added by the pipeline rather than the "
                "contributor; see references/source-conflicts.md.",
    }
    return out


def bundle_for(task_id: str) -> dict:
    """The evidence index every zone subagent reads first."""
    b, meta, amet = load(task_id)
    md = meta.get("metadata") or {}
    truthy = {"true", "True", True}
    attempt = {
        "is_attempt_unit": bool(amet),
        "attempt_id": amet.get("ATTEMPT_ID"),
        "on_task": amet.get("TASK"),
        "role": ("review fix" if amet.get("IS_REVIEW_FIX") in truthy
                 else "SBQ" if amet.get("IS_SEND_BACK_TO_QUEUE") in truthy
                 else "original" if amet else None),
        "attempt_version": amet.get("ATTEMPT_VERSION"),
        "attempted_by": amet.get("ATTEMPTED_BY"),
        "attempted_at": amet.get("ATTEMPTED_AT"),
        "review_status": amet.get("REVIEW_STATUS"),
        "reviewed_at": amet.get("REVIEWED_AT"),
        "review_comments": amet.get("REVIEW_COMMENTS"),
        "time_spent_secs": amet.get("TIME_SPENT_SECS"),
    } if amet else {"is_attempt_unit": False}
    cu = step(b, "ComputerUse") or {}
    cuo = cu.get("output") or {}
    ev = (cuo.get("verifierInput") or {}).get("evaluator") or {}
    crits = ((step(b, "RubricCriteriaBuilder") or {}).get("output") or {}).get("criteria") or []
    qm = ((step(b, "QualityMeasurement") or {}).get("output") or {}).get("content") or {}
    gen = generated_rubric(b)

    init_files = [f for c in ((cuo.get("taskInitializerInput") or {}).get("config") or [])
                  for f in (c.get("parameters") or {}).get("files", []) or []]

    return {
        "task_id": task_id,
        "attempt": attempt,
        "domain": md.get("domain"),
        "sub_domain": md.get("sub_domain"),
        "worker_skill": md.get("WORKER_SKILL_NAME"),
        "batch": meta.get("BATCH"),
        "prompt": (step(b, "PromptInput") or {}).get("output", {}).get("content"),
        "seed_prompt": md.get("seed_prompt"),
        "prompt_changed": field(b, "prompt_changed"),
        "prompt_changes_made": field(b, "prompt_changes_made"),
        "applications_used": field(b, "applications_used"),
        "notes_for_reviewer": field(b, "notes_for_reviewer"),
        "agent_issue_details": field(b, "agent_issue_details"),
        "criteria": [
            {"n": i, "id": c.get("id"), "title": c.get("title"), "weight": c.get("weight"),
             "category": (c.get("annotations") or {}).get("criteria_category"),
             "type": (c.get("annotations") or {}).get("criteria_type")}
            for i, c in enumerate(crits, 1)
        ],
        "n_generated_criteria": len(gen) if gen is not None else None,
        "input_files": [{"path": f.get("path"), "url": cds_to_https(f.get("url", ""))}
                        for f in init_files],
        "expected_files": [{"dest": e.get("dest"), "url": cds_to_https(e.get("path", ""))}
                           for e in as_list(ev.get("expected"))],
        "verifier": {"func": ev.get("func"),
                     "result": [{"dest": r.get("dest"), "path": r.get("path")}
                                for r in as_list(ev.get("result"))],
                     "self_check_score": (cuo.get("verifierOutput") or {}).get("evaluationScore")},
        # NOT about this attempt. A reviewer grades the PREVIOUS submission on the
        # task, then their own fix becomes this attempt — so this verdict belongs to
        # attempt N-1. Never use it to calibrate an audit of attempt N.
        "prior_review": {"applies_to": "the PREVIOUS attempt, not this one",
                         "score_1_5": qm.get("quality_task_overall"),
                         "instruction_following": qm.get("quality_instruction_following"),
                         "feedback": qm.get("feedback_overall")},
        "mechanical": mechanical(b, meta),
        "agent_runs": run_summary(
            b, len(crits), float(sum(c.get("weight", 0) for c in crits)),
            [c.get("title") or "" for c in crits]),
    }
