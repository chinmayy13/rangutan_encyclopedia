# Run the CUA audit on task_10 (local)

Needs: Python 3.10+, the `claude` CLI logged in, and the audit folder `cua_audit_rubric_skills_v0.3` (on `main`).
The audit calls Claude about 30 times (maximum effort, tens of minutes). Treat the result as leads, not a verdict: the tool's own calibration report says it catches about 1 in 5 of the fails human auditors record and over-flags.

## 1. Get the files
```bash
cd rangutan_encyclopedia
git fetch origin claude/focused-lamport-gv6r74 && git checkout claude/focused-lamport-gv6r74
git pull origin claude/focused-lamport-gv6r74
```
You now have `task_10/local_audit/` (this folder).

## 2. Build the audit workspace
Pick any empty folder. It holds the task, the 9 input files and the 3 expected files.
```bash
python3 task_10/local_audit/build_workspace.py --out ~/cua_audit_workspace
```
Expect: `30 criteria, total weight 324` and `staged 9 inputs + 3 expected files`.

## 3. Point the audit tool at it (every new terminal)
```bash
export CUA_AUDIT_HOME=~/cua_audit_workspace
cd /path/to/cua_audit_rubric_skills_v0.3
A=cua-audit-components/scripts
```
Without `CUA_AUDIT_HOME` the tool looks in the folder above `cua_audit_rubric_skills_v0.3`, so it will not find task_10.

## 4. Prepare the evidence
Mac, once (renders the `.xcf` and PDFs): `brew install imagemagick poppler`
```bash
python3 $A/audit_prepare.py task_10 --provision
```
`--provision` installs LibreOffice 7.3.7.2, the version the task VM runs, under `~/.cua-renderers` (large download, no admin rights needed). It makes the `.docx` page count match the VM. Leave the flag off to skip it; the docx layout claims are then marked unverifiable.
A line saying `fitz API is deprecated` is harmless.
Expect: `30 criteria ... mech fails=- minors=- ... files=12 (0 failed)`.

## 5. Run the review
```bash
python3 $A/run_review.py task_10 --plan     # free, lists the calls
python3 $A/run_review.py task_10            # 28 components + input consistency
```
If it stops or some components come back empty, run the same command again; it only runs what is missing.

## 6. Read the result
```bash
python3 $A/sense_check.py task_10
python3 $A/rollup.py
open $CUA_AUDIT_HOME/audit/task_10/component_review.html
python3 $A/summarize.py task_10
open $CUA_AUDIT_HOME/audit/task_10/component_review_summary.html
```
The summary page is the one to act on: numbered fixes with the current text and the replacement text. Any component scoring 1 or 2 fails the task. A 3 or 4 means non-fail. All 5s is a clean pass.

## 7. After you change something
The first audit locks once the summary exists. Re-audit with the rerun skill:
```bash
RR=cua-audit-rerun/scripts
python3 $RR/rerun_versions.py new task_10        # makes audit/task_10-v2/
# edit in $CUA_AUDIT_HOME/audit/task_10-v2/: prompt.md, rubric.json, files/inputs, files/expected
python3 $RR/rerun.py task_10-v2
```
To start from scratch instead, edit `source/prompt.md`, `source/rubric.txt` or `source/form.json` here, delete `$CUA_AUDIT_HOME`, and repeat from step 2.

## What is in `source/`
- `prompt.md`: your final prompt, exactly as pasted.
- `rubric.txt`: your 30 criteria exactly as on the platform, one per line (`weight | type | category | text`). Criterion 16 still has the platform typos (`absorbents`, `withing`, `Cost($/kg)`); the audit will list them as an unscored recommendation. Fix them on the platform, then here.
- `form.json`: domain (Engineering / Chemical Engineering), `applications_used`, the reviewer note.
