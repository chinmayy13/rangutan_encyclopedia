---
name: cua-audit-rerun
description: >-
  Re-run the CUA v3 audit-rubric review — the same 28 components,
  input-consistency pass, sense check, roll-up and output-hygiene summary as
  cua-audit-components, through that skill's own scripts — on a version folder
  of a task that has already been audited once. Use this skill, not
  cua-audit-components, whenever the user asks to run, re-run, redo, repeat or
  re-evaluate the audit, the evals or the review of a task and
  `audit/TASK_ID/component_review_summary.html` already exists: after editing
  prompt.md, rubric.json, task.md or the files/inputs and files/expected of an
  `audit/TASK_ID-vN/` folder, or just to audit the task again. It rebuilds
  bundle.json, the extracted text and the rendered pages from that folder and
  writes the same outputs as the first audit into it. It runs any number of
  times, one version folder per run. Not for a task's first audit (no
  component_review_summary.html yet): that belongs to cua-audit-components.
---

# CUA v3 — re-running an audit on a version folder

A task's first audit is `cua-audit-components`: it reads the platform files in
`tasks/<task_id>/` and writes `audit/<task_id>/`. Every audit after that runs
here, against a **version folder** — `audit/<task_id>-v2/`, `-v3/`, … — that
holds the task as someone has edited it. The review itself is not
reimplemented: this skill rebuilds the evidence the review reads, then calls
`cua-audit-components`' own scripts on the version folder, so the 28
components, the three unscored passes and every output file are the ones a
first audit produces.

## Is this the right skill?

The rule is mechanical: **the first audit belongs to `cua-audit-components`;
once `audit/<task_id>/component_review_summary.html` exists, every later request to
run or re-run that task's audit or evals comes here** — as many times as asked,
one version folder per run. Check it rather than guess:

```bash
python3 $R/rerun_versions.py status <task_id>
```

Exit code 1 with "no first audit" or "has not finished" means the first audit
is still `cua-audit-components`' job: use that skill instead.

## The version folder

```
audit/<task_id>/              the first run — read, never written
audit/<task_id>-v2/           a version folder
├── prompt.md                 required
├── rubric.json               required: [{id, title, weight, annotations: {criteria_type, criteria_category}}]
├── task.md                   required: "domain: …" and "sub_domain: …" lines
└── files/
    ├── inputs/               the files the agent starts from
    └── expected/             the answer key (gold files), named as the agent must name them
```

The three views must exist; what they say is up to the editor. Under `files/`,
the folder is the truth: a file added is a new input or deliverable, a file
deleted is gone, a file replaced is audited with its new content. Dotfiles
(`.DS_Store`) are ignored. When `files/inputs/` or `files/expected/` is absent
or empty, prepare copies that side in from the nearest earlier version that
has files there, else from the first run, and says so.

Anything else in the folder — `bundle.json`, extracts, renders, component
results, reports — is derived. Prepare rebuilds the evidence every time and
clears derived files it did not write itself, so copying a whole audit folder
and editing it is safe.

Where each `bundle.json` field comes from:

| Field | Source |
|---|---|
| `prompt` | `prompt.md` |
| `criteria` | `rubric.json` |
| `domain`, `sub_domain` | `task.md` (a missing line keeps the first run's value) |
| `input_files`, `expected_files` | `files/inputs/`, `files/expected/`. A file unchanged since the first run keeps its platform URL; a new or edited one gets `rerun-local://<unit>/files/<side>/<name>` |
| `verifier.result` | the first run's, minus deliverables deleted from `files/expected/`, plus a `/home/docker/Desktop/<name>` entry for each new one |
| `mechanical`, `agent_runs` | recomputed from the above by `audit_common`, exactly as for a first run |
| everything else: attempt, form fields, `verifier.func`, `self_check_score`, `prior_review`, `seed_prompt`, … | the platform record: `tasks/<task_id>/response.json` (or `attempts/`), else the first run's `bundle.json` |

`bundle.json` is produced by `audit_common.bundle_for` itself, run over the
first run's response with the folder's edits applied, so its shape and every
mechanical rule are the pipeline's own. An unedited version folder rebuilds
the first run's evidence exactly.

## The loop

```bash
R=<this skill's folder>/scripts

# 1. which version is pending (exit 1: not this skill)
python3 $R/rerun_versions.py status <task_id>

# 2. only when none is pending: the next version, a copy of the latest one
python3 $R/rerun_versions.py new <task_id>                  # or --from <unit>
python3 $R/rerun_versions.py new <task_id> --from-response  # task re-downloaded into tasks/

# 3. validate the folder and see what changed against the first run (writes nothing)
python3 $R/rerun_prepare.py <task_id>-vN --check

# 4. the model calls it will make (spends nothing)
python3 $R/rerun.py <task_id>-vN --plan

# 5. prepare -> 28 components with input consistency in their pool -> sense check -> report -> summary
python3 $R/rerun.py <task_id>-vN
open audit/<task_id>-vN/component_review.html
open audit/<task_id>-vN/component_review_summary.html
```

Choosing the version: if the user names a folder, use it. If they name only
the task, `status` decides — one pending version is the one to run; several
pending means asking which; none pending means `rerun.py <task_id> --new`,
which copies the latest version to the next number and audits it. Tell the
user which folder was audited.

Step 5 makes up to 31 model calls, all but the summary at maximum effort,
fewer when earlier results can be reused (`--plan` says how many), and takes
tens of minutes: run it in the background and read its output, rather than
blocking on one long foreground command. Interrupted, or some components came back empty? Run
the same command again: while the folder is unchanged it keeps every finished
component and runs only the rest — also after the report, when the summary,
consistency or sense pass left no result, or the report or summary is older
than a result it is built from. It retries missing components once on its own
and writes no report until all 28 have a result.

`--steps` runs a subset, in order, of `prepare,review,consistency,sense,report,summary`.
`--component NN` (repeatable), `--class files|rubric|other`, `--workers N`,
`--redo` and `--skip-render-check` pass through to the review scripts. Prepare
installs any renderer the files need at the version `cua-applications.csv`
pins, as `audit_prepare.py --provision` does; `--no-provision` skips that.

At the end `rerun.py` prints the version's verdict beside the first run's, the
components whose score moved, and how many results were reused.

## Reusing earlier results

Before a component costs a call, `rerun.py` looks for an earlier audit of the
same task that scored it on exactly the evidence it gets now, and takes that
result instead. The earlier audits are the first run and every version folder
not edited since it was prepared, newest first. A component's evidence is:

- the prompt `run_review.py` would send it, so a changed definition or
  preamble never matches, and its model;
- every `bundle.json` key its definition names in backticks, in "Evidence to
  read" or anywhere else in its text. For `mechanical`, the entries owned by
  components of its own evidence class, plus any entry it names;
- every file it names: the extracts, `render_index.json`, the rendered pages,
  `files/inputs/`, `files/expected/`.

Unit names, folder paths, placeholder URLs, and the timestamps and machine
paths in `render_index.json` do not count. So a rubric edit keeps the prompt
and task components that never read the rubric, an edit to one file keeps the
components that read neither that file nor anything made from it, a prompt
edit keeps nothing, and an unedited copy keeps all 28. Every component is told
to read `bundle.json` whole, so this trusts each definition to name what its
score depends on.

A reused result is `components/NN.json` as the earlier audit wrote it, with
its paths moved to this folder and `"_reused_from"` naming the audit whose
call produced it. `components/NN.prompt.md` is the prompt this folder would
have sent, there is no `NN.stream.jsonl` (the call's log stays where the call
ran), and `_components.jsonl` logs it with `"status": "reused"`. The report
and summary treat it like any other result. `--plan` predicts the reuse;
before prepare it judges the extracts and renders by the files they are made
from, and the run decides on the prepared evidence.

`--fresh` makes a new call for every component: use it when the user asks for
an independent re-score, such as a second opinion on an unchanged version.
`--redo` never reuses either. The three unscored passes always run. Input
consistency reads only the prepared evidence, so it joins the review's pool of
`--workers`, queued behind the component calls: it starts beside them when a
worker is free, and otherwise as soon as every one of them has started. When
the review makes no call (every component reused or already done), or its
pooled call left no result, it runs alongside the sense check instead, its
lines prefixed `[consistency]`. The report waits for it.

## Outputs

The same files, names and formats as `cua-audit-components`, in the version
folder: `bundle.json`, `inputs_extracted.md`, `expected_extracted.md`,
`render/<side>/<file>/page-NN.png`, `render_index.json`,
`components/NN.{json,prompt.md,stream.jsonl}` (no stream log for a reused
result), `_components.jsonl`, `input_consistency.json`, `sense_check.json`,
`component_scores.csv`, `component_review.html`,
`component_review_summary.html` and `component_review_summary.json`.

One file is added: `_rerun.json`, the manifest — the first run it derives
from, the platform record used, where each field came from, which files got a
placeholder URL, what changed against the first run, and a fingerprint of the
evidence. It is not part of the evidence the components read.

## Rules

- **Never write to the first run's folder.** Once its summary exists,
  `cua-audit-components`' scripts refuse to redo anything in it (exit 3),
  `audit_prepare.py` included; edits go in a version folder.
- **Only `rerun.py` drives a version folder.** It names the folder it audits
  in `CUA_AUDIT_RERUN_UNIT`, and `cua-audit-components`' scripts refuse a
  version folder without that: run by hand on one they exit 3, and a sweep
  with no unit skips it. Always go through `rerun.py`, which hands every pass
  the folder by name.
- **A version is audited once.** Once its audit is complete — report,
  summary, every pass with a result — or its folder was edited after the
  report, prepare refuses it (exit 3): audit the next version with
  `new --from <that unit>`, so each report keeps describing the content it
  scored. `--reset` discards that version's results and audits it again in
  place — only when the user asks for exactly that, and with `--fresh` when
  they want new calls rather than other audits' results.
- **No mixed evidence.** A folder edited after its review started is refused
  (exit 3) rather than resumed, because its finished components scored the
  old content; `--reset` starts its review over. Review steps run without
  prepare also refuse while the folder differs from its last prepare.
- **Edit the folder, not the evidence.** `bundle.json`, the extracts and the
  renders are rebuilt from the views and files on every prepare; a hand edit
  to them is lost or, worse, reviewed as if it were the task.
- **Write every character as itself.** The views are UTF-8: `±`, `—`, `≤`,
  `£`, `é` go in as those characters, never as a `\u00b1` escape or an HTML
  entity, in text you add as much as in text you keep. A JSON parser reads
  both spellings of `rubric.json` alike, but a person reading or copying from
  it gets six characters where the task has one. A script that rewrites it
  passes `ensure_ascii=False` to `json.dump` and opens the file with
  `encoding="utf-8"`. `rerun_versions.py new` writes the copy it makes that
  way, so a first run whose `rubric.json` still carries escapes does not pass
  them on.

## What a version folder cannot change

The platform record — the verifier's `func` and self-check score, the form
fields, the prior review, the recorded agent runs, the attempt metadata —
comes from the first run's response, because a version folder has no file for
it. Agent runs are re-judged against the version's rubric for staleness, not
re-run.

A file the platform does not hold has no real URL, so it gets
`rerun-local://…`: distinct per file, never expiring, never an input's URL.
Components 10 and 28 read URLs, and their findings on such a file describe
the version folder, not a submission on the platform. The manifest lists
every placeholder.

## When it stops

| Output | Meaning | Next |
|---|---|---|
| exit 1, "no first audit" / "has not finished" | not a rerun | use `cua-audit-components` |
| exit 2, `error: …` | a view is missing or `rubric.json` is malformed (a weight must be a number or null) | fix the folder |
| exit 3, "already has a finished audit" | that version is done | `new --from <unit>`, or `--reset` if the user asked |
| exit 3, "produced before the folder last changed" | edited mid-review | `--reset` |
| exit 3, "only cua-audit-rerun audits it" / "its first audit is finished" | a `cua-audit-components` script was run by hand | `rerun.py <unit>`, or `rerun_versions.py status <task_id>` |
| "the review did not start" | a renderer is missing | `rerun_prepare.py <unit> --provision --rebuild`, or `--skip-render-check` |
| "still no result for component(s) …" | calls failed twice | read `_components.jsonl`, then run the same command again |
| "incomplete: … did not produce a result" | a pass after the components failed | run the same command again: it runs only what is missing |

The scripts find `cua-audit-components` beside this skill (symlinks are
resolved), or at `$CUA_AUDIT_COMPONENTS`. The workspace is the same as that
skill's: `$CUA_AUDIT_HOME`, else the folder containing the skills bundle.
