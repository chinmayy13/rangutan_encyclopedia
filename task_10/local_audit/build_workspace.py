#!/usr/bin/env python3
"""Assemble task_10 for the CUA audit tool (cua_audit_rubric_skills_v0.3).

Writes, inside a workspace folder of your choice:
    tasks/task_10/response.json    prompt, rubric, initializer and verifier JSON
    tasks/task_10/task_meta.json   domain / sub_domain
    audit/task_10/files/inputs/    the nine input files   (from ../initial_files)
    audit/task_10/files/expected/  the three expected files (from ../gtf_files)

Usage (from anywhere):
    python3 build_workspace.py --out ~/cua_audit_workspace
    export CUA_AUDIT_HOME=~/cua_audit_workspace     # tells the audit scripts to use it

Edit source/prompt.md, source/rubric.txt or source/form.json and rerun to
audit a changed prompt or rubric. Safe to rerun: it overwrites what it wrote.
"""
import argparse
import json
import re
import shutil
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASK = HERE.parent
INPUTS = ["CTS.txt", "Agn.txt", "CTSAgn.xlsx", "CTSAgn_After.xlsx",
          "CTSAgn_batch_economics.csv", "Thermal_Screening_Note.pdf",
          "Stage_Gate_Policy.pdf", "Regeneration_Guidance_Bulletin.pdf",
          "plot_template.xcf"]
EXPECTED = ["Thermal_Stability_Assessment.pdf", "Adsorbent_Cost_Comparison.docx",
            "plot_template_updated.xcf"]
BUCKET = "https://scale-cds-public-us-west-2.s3.amazonaws.com/local-audit"
DESKTOP = "/home/docker/Desktop"


def read_rubric():
    crits = []
    for line in (HERE / "source" / "rubric.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        w, typ, cat, title = [p.strip() for p in line.split("|", 3)]
        crits.append({
            "id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"task_10/{len(crits) + 1}")),
            "title": title,
            "weight": int(w),
            "annotations": {"criteria_type": typ, "criteria_category": cat},
        })
    return crits


def prompt_changes():
    text = (TASK / "prompt_change_description.md").read_text(encoding="utf-8")
    return text.split("\n", 2)[2].strip() if text.startswith("Paste into") else text.strip()


def build_response(prompt, crits, form):
    evaluator = {
        "func": "agent_judge_multi",
        "expected": [{"dest": n, "path": f"{BUCKET}/expected/{n}", "type": "cloud_file"}
                     for n in EXPECTED],
        "result": [{"dest": n, "path": f"{DESKTOP}/{n}", "type": "vm_file"}
                   for n in EXPECTED],
        "rubric": {"criteria": crits},
    }
    initializer = {"config": [{"type": "download", "parameters": {"files": [
        {"path": f"{DESKTOP}/{n}", "url": f"{BUCKET}/inputs/{n}"} for n in INPUTS]}}]}
    return {"before": {
        "step_prompt": {"type": "PromptInput", "output": {"content": prompt}},
        "step_rubric": {"type": "RubricCriteriaBuilder", "output": {"criteria": crits}},
        "step_cu": {"type": "ComputerUse", "output": {
            "taskInitializerInput": initializer,
            "verifierInput": {"evaluator": evaluator},
            "inputRubricCriteria": crits,
            "verifierOutput": {"evaluationScore": "1"}}},
        "step_t1": {"type": "TextCollection", "output": {
            "prompt_changed": "true", "prompt_changes_made": prompt_changes()}},
        "step_t2": {"type": "TextCollection", "output": {
            "applications_used": form["applications_used"],
            "notes_for_reviewer": form["notes_for_reviewer"]}},
    }, "turns": [], "after": {}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path,
                    help="workspace folder; use the same path for CUA_AUDIT_HOME")
    out = ap.parse_args().out.expanduser().resolve()

    prompt = (HERE / "source" / "prompt.md").read_text(encoding="utf-8").strip()
    form = json.loads((HERE / "source" / "form.json").read_text(encoding="utf-8"))
    crits = read_rubric()
    for n in INPUTS:
        assert (TASK / "initial_files" / n).is_file(), f"missing initial_files/{n}"
    for n in EXPECTED:
        assert (TASK / "gtf_files" / n).is_file(), f"missing gtf_files/{n}"
    assert re.search(r"\bdesktop\b", prompt, re.I)

    tdir = out / "tasks" / "task_10"
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / "response.json").write_text(
        json.dumps(build_response(prompt, crits, form), indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (tdir / "task_meta.json").write_text(json.dumps({
        "TASK_ID": "task_10", "STATUS": "pending", "BATCH": None,
        "metadata": {"domain": form["domain"], "sub_domain": form["sub_domain"],
                     "WORKER_SKILL_NAME": form["sub_domain"], "ubuntu": "true"},
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    for sub, names, src in (("inputs", INPUTS, TASK / "initial_files"),
                            ("expected", EXPECTED, TASK / "gtf_files")):
        dest = out / "audit" / "task_10" / "files" / sub
        dest.mkdir(parents=True, exist_ok=True)
        for n in names:
            shutil.copy2(src / n, dest / n)

    total = sum(c["weight"] for c in crits)
    print(f"wrote {tdir}/response.json  ({len(crits)} criteria, total weight {total})")
    print(f"staged {len(INPUTS)} inputs + {len(EXPECTED)} expected files under {out / 'audit' / 'task_10' / 'files'}")


if __name__ == "__main__":
    main()
