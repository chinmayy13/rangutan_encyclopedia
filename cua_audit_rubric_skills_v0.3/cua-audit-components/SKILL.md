---
name: cua-audit-components
description: >-
  Review a CUA v3 task submission against the official 28-component audit
  rubric (this skill's `audit-rubric.csv`), one component at a time. Each
  component is generated verbatim from the CSV (id, question, description,
  exact score options, justification rules, errorCategories) and scored by its
  own subagent call at maximum effort: file-comparison and rubric components on
  opus, the rest on sonnet. Office, PDF and HTML deliverables are first
  rasterised to page images at the application versions `cua-applications.csv`
  pins for the CUA VM, so visual criteria are judged from how a file looks.
  Rolls the 28 scores into the reviewer verdict, flagging scores the CSV
  forbids and missing justifications. Use for a task's first audit: deciding
  whether a task or attempt would pass audit-rubric review, scoring a single
  component, or regenerating the components after the CSV changes. Once
  `audit/TASK_ID/component_review_summary.html` exists, every later run or
  re-run of its audit or evals belongs to cua-audit-rerun.
---

# CUA v3 — audit-rubric component review

The question this answers is narrow and literal: **would this submission pass
the review defined in this skill's `audit-rubric.csv`?** Not whether the task
is good in some broader sense.

`audit-rubric.csv` is the only authority. Everything in `components/` is
generated from it verbatim, so there is no paraphrase layer to drift.

## Layout

```
cua-audit-components/
├── SKILL.md
├── _generate.py                  CSV -> components/  (re-run when the CSV changes)
├── components/NN-slug.md         28 generated component definitions
├── components/_*.md              the three unscored pass prompts: sense check,
│                                 input consistency, output hygiene
├── references/
│   ├── task-response-format.md   the input contract: every evidence path, and
│   │                             how to build a response.json by hand
│   └── source-conflicts.md       what wins when the CSV, the guidelines and
│                                 the platform disagree
└── scripts/
    ├── audit_prepare.py          build audit/<unit>/ evidence: bundle, views, files, extracts, renders
    ├── audit_common.py           response accessors, the mechanical pre-pass, the reader venv
    ├── extract_files.py          dump Office/PDF files to text (runs under .venv)
    ├── render_files.py           rasterise those files to page PNGs (runs under .venv)
    ├── render_common.py          renderer registry, tool probe, VM version parity
    ├── renderers.json            per format: tool, probe, install, parity target
    ├── provision_renderers.py    install the pinned builds under ~/.cua-renderers
    ├── run_review.py             one subagent call per component, input consistency in the same pool
    ├── input_consistency.py      one opus call over the supplied files
    ├── sense_check.py            one opus call over all 28 results
    ├── rollup.py                 28 scores -> verdict + CSV + HTML
    ├── summarize.py              the results -> the fixes, from one tool-free call answering in JSON
    └── render_summary.py         that JSON -> component_review_summary.html
```

## The loop

```bash
A=cua-audit-components/scripts

# 0. supply the submission — no fetch step, these are files you place
#    tasks/<task_id>/{response,task_meta}.json
#    attempts/<attempt_id>/{response,attempt_meta,task_meta}.json

# 1. stage evidence: bundle.json, prompt.md, rubric.json, task.md, input and
#    expected files, extracted text, rendered page images.
#    --provision installs any renderer these files need, at the version
#    cua-applications.csv pins. Always pass it unless you know this machine
#    has already audited the same file types.
python3 $A/audit_prepare.py <unit_id> --provision

# 2. review: the 28 components, and the input-consistency pass (do the
#    supplied files agree?) queued behind them in the same worker pool
python3 $A/run_review.py <unit_id> --plan        # free, prints the plan
python3 $A/run_review.py <unit_id>

# 3. the pass no single component can do
python3 $A/sense_check.py <unit_id>              # read the 28 together
python3 $A/input_consistency.py <unit_id>        # only if the review left it without a result

# 4. verdict
python3 $A/rollup.py
open audit/<unit_id>/component_review.html

# 5. the fixes, for someone who has to act on them
python3 $A/summarize.py <unit_id>
open audit/<unit_id>/component_review_summary.html
```

A unit is a task id or an attempt id — whatever `audit/<id>/bundle.json` was
built for. `audit_common.unit_dir()` looks under `tasks/` first, then
`attempts/`, and the workspace root is `CUA_AUDIT_HOME` if set, otherwise the
directory containing this bundle.

## First audit only

This skill runs a unit's **first** audit, and its scripts enforce that. Once
`audit/<unit_id>/component_review_summary.html` exists, every later run or
re-run of that task's audit goes through the sibling skill `cua-audit-rerun`:
it audits a version folder, `audit/<unit_id>-vN/`, holding the edited views and
files, with these same scripts and the same outputs.

From then on the scripts only complete what the first audit still lacks — a
component or pass with no result, a report or summary that is missing or older
than the results it is built from. They never redo what it has:
`audit_prepare.py`, `render_files.py` and `extract_files.py` refuse the unit,
and so do `--redo` and a `rollup.py` whose report and summary are already
current, because they describe that evidence and those results. A unit you name
is refused with exit code 3 and the command to run instead; a sweep with no
unit skips it. A version folder is refused the same way unless
`cua-audit-rerun` launched the script for it (it names the folder in
`CUA_AUDIT_RERUN_UNIT`).

## What `audit_prepare.py` writes

| File | Contents |
|---|---|
| `bundle.json` | the evidence index every component reads first, including the mechanical pre-pass |
| `prompt.md` | the prompt as shipped, plain text |
| `rubric.json` | the criteria verbatim: `{id, title, weight, annotations: {criteria_type, criteria_category}}` |
| `task.md` | `domain` and `sub_domain`, the two fields that select the weight-share bands |
| `files/inputs/`, `files/expected/` | the staged binaries |
| `inputs_extracted.md`, `expected_extracted.md` | those binaries dumped to text |
| `render/inputs/<filename>/page-NN.png`, `render/expected/<filename>/page-NN.png` | those binaries rasterised, one PNG per page |
| `render_index.json` | per file: `status`, `visual_verifiable`, `parity`, `pages`, `unverifiable_reason`; plus every tool probed and its pinned version |

The three view files are derived from the response on every run, never edited
by hand — regenerate rather than patch them. To audit edited views or files,
put them in a version folder and use `cua-audit-rerun`.

Every file the pipeline writes is UTF-8, with each character written as
itself: `rubric.json` reads `within ±5%`, not `within \u00b15%`, whichever
spelling the response used. Keep to that in anything you write by hand, such
as a `response.json` assembled from loose files: `json.dump(...,
ensure_ascii=False)` into a file opened with `encoding="utf-8"`.

## Install the renderers before you review — and pin the version

**Rule: if a unit's input or expected files include anything with a visual
form, the application that renders it must be installed at the version
`cua-applications.csv` pins, before `run_review.py` runs.** That means
`.docx`, `.xlsx`, `.pptx`, `.pdf`, `.html`, `.eps`, `.tif`, `.blend` and
video. Files the Read tool shows natively (`.png`, `.jpg`, `.gif`, `.webp`)
need nothing.

`audit_prepare.py --provision` is the whole obligation: it works out which
renderers this unit's files actually need, installs the missing ones under
`~/.cua-renderers` (no root, nothing you installed yourself is touched), and
only then rasterises. Without `--provision` it still checks, and prints the
one command that fixes it rather than proceeding quietly.

The document readers underneath — `openpyxl`, `python-docx`, `python-pptx`,
`pdfplumber`, `pymupdf`, `pillow` — are not an obligation at all. The first
run creates the workspace venv and installs them, because they are wheels and
a wheel is never a decision worth stopping a run for. What it did is recorded
as `readers` in `bundle.json`, so a host that could only be partly equipped
says so in its own evidence instead of failing silently.

You do not have to guess, and you must not improvise an install. The registry
decides what a format needs and how to get it; `--provision` performs it.

```bash
python3 $A/audit_prepare.py <unit_id> --provision   # check, install, render
python3 $A/provision_renderers.py --for audit/<unit_id>            # plan only
python3 $A/provision_renderers.py --for audit/<unit_id> --install  # install only
python3 $A/provision_renderers.py                  # plan for every installable tool
python3 $A/render_files.py --tools                 # probe: found vs pinned, per tool
python3 $A/render_files.py --needed audit/<unit_id> # tool names this unit lacks
python3 $A/render_files.py audit/<unit_id>         # re-render after installing
python3 $A/audit_prepare.py <unit_id> --no-render  # skip rendering entirely
```

`run_review.py` will not start 28 model calls against deliverables that never
rendered — they would all answer "UNVERIFIABLE". Where an install would have
fixed it, it runs `audit_prepare.py --provision` for that unit itself and
re-checks, so the review waits for the install rather than stopping on it.
It stops only when the gap survives that: no published build for this
platform, say. `--skip-render-check` reviews anyway and is the right choice
then; `--no-auto-prepare` restores the older behaviour of printing the fix
and stopping.

### Why the version, not just the application

CUA tasks run on one fixed Ubuntu image, and `cua-applications.csv` is its
inventory. LibreOffice 7.3.7.2 paginates a document differently from
LibreOffice 25.x, so rendering with the wrong build produces page counts and
line breaks the contributor never produced — and pagination is exactly what
the `visual` criteria grade. The Document Foundation publishes every past
release, so the pinned build is installed exactly rather than approximated by
"latest".

Every rendered file carries a `parity` verdict, and the components block
reflow-dependent claims when it is not `exact` or `compatible`. Parity applies
to the tool that decides layout — the office suite, the browser, the fonts
(Carlito carries Calibri's metrics, Caladea carries Cambria's; without them a
DOCX reflows). Rasterising an existing PDF is faithful whatever the
rasteriser, so those carry `n/a`.

Missing renderers degrade honestly rather than silently: office files fall
back to a first-page preview (`degraded`), and with nothing available at all
the entry is `unavailable` with an `unverifiable_reason`. Either way the
component reports that file's layout in `blocked_on`. A renderer this host
lacks is never evidence of a defect in the submission.

One division of labour matters: **the operator provisions, the reviewer never
does.** The per-component subagents run in parallel against prepared
evidence, are told explicitly not to install or render anything, and would
otherwise race each other installing the same suite mid-review.

Narrowing: `--component 09 --component 16`, `--class files|rubric|other`,
`--workers N`. `--status` shows which of the 28 have run, and whether the
input-consistency pass has. `--redo` re-runs components that already have
output.

The input-consistency call shares the `--workers` pool. Each unit's call is
queued right behind that unit's component calls, so it starts beside them when
a worker is free, and otherwise as soon as every one of them has started. It is
queued only when the unit has no `input_consistency.json` yet (or with
`--redo`), and not when `--component` or `--class` narrows the run unless you
add `--with-consistency`. `--no-consistency` leaves it out.

## What each component file contains

Copied verbatim from the CSV row, never reworded:

- `id` — the audit-rubric UUID, the component's real identity
- `questionText` and `questionDescription`
- every `answerOptionText` with its `answerOptionScore`
- per-option `answerOptionRequiresJustification`
- the `errorCategories` label set

Added by the generator: which evidence to read, which model runs it, the JSON
output contract, and — new in v0.1 — the `CALIB` calibration for that component,
rendered as a *Before you score* block under `## Score options` plus notes under
the individual scores they govern. Calibration never adds an option or moves a
threshold; where it would have, the rule was dropped rather than carried, so
every note in a component file is safe to apply exactly as written.

**Score sets differ per component and are not uniform 2/3/4/5.** Seven
components are binary `[2, 5]` with no middle band — Feasibility, Output
Naming, Gold File Format, Rubric Accuracy, Framing, Count, JSON Structure. PII
is `[2, 4, 5]` with no 3. The schema passed to each subagent enumerates only
that component's allowed scores, so an out-of-band score cannot be returned.

## Model assignment

Fixed per component by evidence class in `_generate.py`, always
`--effort max`:

| Class | Model | Components | Why |
|---|---|---|---|
| `files` | `claude-opus-5` | 6 | must open the input / expected files to decide |
| `rubric` | `claude-opus-5` | 15 | decided by reading the criteria against the prompt |
| `other` | `claude-sonnet-5` | 7 | decided from the prompt or the verifier JSON |

The `files` set is PII / Safety, Answer leakage, Gold File Accuracy, Gold File
Format, Input Consistency, and **Rubric Accuracy** — that last one is a rubric
component but its criteria claims can only be checked against the answer key,
so file access wins.

A class is a default, not a ceiling. A `CALIB` entry may add an `evidence`
list naming sources that component alone reads, which is how **Overfitting**
reaches `expected_extracted.md` (a criterion that says "matches the
corresponding expected file" inherits whatever the answer key stores, rounding
included) and how **Value Binding** reaches the input files and their rendered
pages (to see whether one supplied artifact already prints every figure a
group of criteria grades). Any component whose evidence names
`page-NN.png` is given the per-page listing at run time and the instructions
on opening one; `run_review.py` reads that off the component file, so the two
cannot drift apart. An `output` entry works the same way for the output
contract: it adds a field that component alone returns, and `run_review.py`
requires in the schema every such field the component file names. Value
Binding uses it for `whole_answer_inputs` (see Output per component).

To change an assignment, edit `CLASS` in `_generate.py` and regenerate. Do not
edit a component file by hand; `_generate.py --check` will flag it as stale.

## Output per component

```json
{ "component_id": "...", "title": "...", "score": 2,
  "error_category": "[All] [All] [Fail - Coverage]",
  "justification": "...", "evidence": "...", "criteria": [14],
  "confidence": "high", "blocked_on": null, "minor_issues": [] }
```

`error_category` must be one of that component's `errorCategories` strings
verbatim, or `null` on a clean pass. `justification` is mandatory when the
chosen score's CSV option says so.

Value Binding (27) must also return `whole_answer_inputs`, one entry per group
of value criteria: `{"criteria": [4, 5, 6], "input": "..."}`, where `input`
names the supplied file and the page, column, table or cell block that prints
every value the group grades, or is `null` when no single input does. Text
values such as material names count, not only numbers. A response that copies
that input passes the whole group without doing the task, which is the
component's fail option; recording every group makes a skipped check visible.
The report lists the groups under **Value criteria that one input answers in
full**, and the summary receives every group that has an input, whatever the
component scored.

The rubric components (12–27) often prescribe a criterion rewrite, and the
summary quotes it. So their contract holds any criterion text they propose to
the rubric's own rules: it never states the answer, only a comparison to the
expected file; it has no conditional wording; it tests one element. A
criterion that grades what the prompt never asks for is removed, folded into
another or backed by a prompt change, never made conditional.

`minor_issues` (v0.1) is **never scored**. It records suggestions that would
improve the task but that the component's own answer options do not name, so it
cannot move `score`, `error_category` or the verdict — a 5 with entries in it is
still a 5.

Because the score hides them by design, they are surfaced in four places:

- a **Recommendations, not scored** block per submission in the HTML, rendered
  even when every component scored 5, and printing `None recorded.` when empty
  so absence is explicit rather than ambiguous;
- an **amber count beside the score** in the 28-component grid, so a clean grid
  carrying work is visually distinct from a clean grid with none;
- a **Rec** column in the triage table and in the per-component table, plus a
  counter in the report header;
- a pipe-separated `minor_issues` column in `component_scores.csv`, and a `rec`
  column in `rollup.py`'s console summary.

The senior review pass may cite one as corroborating evidence but may **never**
ground an escalation on it: if an answer option described it, it would already
be scored.

## Input file consistency

`input_consistency.py` is the second unscored pass, and it covers the one thing
the review form never asks: whether the material the task is built from agrees
with itself. Each of the 28 components grades a single artifact against the
form, so a submission can score clean on all 28 while a methodology PDF and a
dataset's own reference sheet state different thresholds for the same
quantity, or a cutoff selects nothing from the column it governs, or the answer
key resolves a conflict between two inputs silently and no agent following
either supplied rule reaches it.

It checks two directions: the input files against each other, and the inputs
against the prompt, the expected files and the criteria. One opus call per
unit, reading `bundle.json`, both extracted views and the rendered pages, and
it needs only `audit_prepare.py` to have run. `run_review.py` queues it in the
component calls' worker pool, behind that unit's components (see The loop);
run alone, `input_consistency.py <unit_id>` can go before, during or after the
review.

Severity is a two-level judgement with one test, *what would a correct agent
produce*: **major** where the inconsistency changes what a correct submission
looks like, **minor** where it moves no graded output. The unit's verdict is
derived from the findings rather than taken from the model, so a major finding
cannot be reported under a softer heading. It is **never scored** and never
reaches the roll-up; it surfaces as **Input file consistency** in the report's
Triage section, red for major, amber for minor, green for clean, and as
`audit/<unit_id>/input_consistency.json`.

`rules_compared` lists every shared rule and quantity the pass compared, with
the files it compared each one across, rather than counting them, so two runs
on the same evidence show what one checked and the other skipped. The report's
Rules column is the length of that list; an older result that stored a count
still displays it.

Where a finding is already owned by a scored component — 09, 11, 15, 16 — the
pass names that component. That duplication is deliberate: this section is the
one place a reader sees the whole cross-artifact picture at once.

## Roll-up

`rollup.py` applies the reviewer rules: grade to the **lowest** component; any
component at 1–2 fails the task; no fail but any 3–4 makes the whole task 3–4;
every component must be 5 for a 5.

It also audits the audit, reporting five output-contract issues on the console
and in the report's **Output contract issues** panel:

- a score the CSV does not allow for that component
- a score whose option requires a justification, returned without one
- a result whose `_model` is not the model its component file pins, which is
  what a result produced outside `run_review.py` looks like
- results with no `_components.jsonl` call log beside them
- a result that sets `blocked_on` but claims `high` confidence

An issue is flagged, not dropped: the result still counts toward the verdict,
so read the panel before relying on it.

Outputs land in each unit's own directory, beside its `bundle.json`, so a
submission's audit is self-contained: `audit/<unit_id>/component_scores.csv`
(one row per component) and `audit/<unit_id>/component_review.html`, which
covers that unit alone. `run_review.py` writes its call log to
`audit/<unit_id>/_components.jsonl` in the same place. Running `rollup.py`
with no arguments still summarises every unit on the console, and writes a
report for every unit that may still get one (see First audit only).

## Output hygiene

`component_review.html` is complete, and completeness is the problem. A unit
with 28 findings, 94 unscored recommendations, two escalation proposals and ten
consistency findings runs to thousands of lines, and the one edit that clears
the verdict is somewhere inside it. `summarize.py` is the last pass. It writes
`audit/<unit_id>/component_review_summary.html`: the fixes, in order, then,
folded, every recommendation they do not cite. The scores, the reasoning and
the evidence stay in `component_review.html`, which the summary links to and
does not repeat.

It re-presents and never re-audits. Its prompt carries the results themselves,
not the report: the task's prompt and criteria, every component that scored
below 5, every recommendation, every group of value criteria that component 27
found one input answers in full (at any score), the senior review and the
input-consistency result, each item with an id. The call has no tools, so
there is nothing else for it to open, and it answers in JSON through `--json-schema`;
`components/_output_hygiene.md` names every field and keeps the writing rules.
It runs `claude-opus-5` at `--effort high`, not `max`: it orders and words
findings rather than forming them, and at `max` a large unit reasons past the
output limit before it answers. No score moves, no figure is recomputed, no
finding is formed that the results do not already state. What it adds is
order: the fixes numbered in the order they should be done, each carrying the
current text and the replacement text in full, the file named and labelled
GTF, input file, prompt, rubric or bundle, and an answer-key check stated on
every step that touches a gold file.

A criterion it writes is still a criterion, and the rubric components would
judge it as they judged the task's own. One that breaks their rules trades one
finding for another, so the prompt gives the model those rules for every
criterion it adds or rewrites: never the answer, only a comparison to the
expected file with a tolerance or an equivalence; no conditional wording; one
element; the file and the place named; a legal weight.

One thing it surfaces that nothing else does. The input-consistency findings
are scored by no component, so `rollup.py` reports them and then the reader's
eye slides past them; the prompt makes every one of them, major and minor, a
numbered fix ranked alongside the rest.

Python does the rest, with no model involved. It checks the answer first:
every cited id exists in the results, every file is one of the task's files and
carries its class, every quoted current text appears word for word in
`bundle.json`, `rubric.json`, `prompt.md`, the extracted files or a quote a
result took from the files (the extraction stops at 200 rows per sheet and
20,000 characters per file; the passes that open the files do not), every
highlighted or deleted part sits inside the text it marks, every step touching
a GTF carries its answer-key check, and every consistency finding is carried by
a fix. Two more checks hold every criterion the answer writes to the rubric: it
is not conditional ("if", "unless", "where applicable", "any figure it
reports"), and it states no date or number the prompt does not give, beyond a
tolerance, a place such as slide 4, a precision, 0 or 1. Either marks the fix
**Breaks a rubric rule**. They match wording, so they catch the common forms
and can miss a paraphrase. A failed check does not block the page: it is marked
where it applies and listed at the top. `render_summary.py` then builds the sections from a
fixed template and works out the counters (verdict, fixes queued, fixes that
clear a fail, components below 5, major inconsistencies) from the results.
Last, folded, it lists every recommendation the answer does not cite, word for
word and grouped by component, with the hard gates in bold as in the report.
The model writes none of that list, so it adds nothing to the call's time.

```bash
python3 $A/summarize.py <unit_id>          # write it
python3 $A/summarize.py                    # every unit with all 28 results
python3 $A/summarize.py <unit_id> --redo   # write it again
```

It reads the JSON results, not the report, so it does not wait for
`rollup.py`; run it after the sense check and the input-consistency pass, or it
carries nothing from them. Beside the page it writes
`component_review_summary.json` (the model's answer and every failed check),
`component_review_summary.prompt.md` and `component_review_summary.stream.jsonl`.
A summary older than any result it is built from is rewritten by the next plain
run, which is how a pass that finished after it gets in. A call still running
at 30 minutes is killed, even while it is silent.

Because the summary marks the first audit finished, a failed call writes no
page: the audit stays unfinished and the next run tries again.

## Discipline

- **The CSV decides, not the model.** Every score must trace to an
  `answerOptionText` in `components/NN-*.md`. If a subagent's reasoning does
  not map onto one of those options, the output is wrong even if the reasoning
  is good.
- **Evidence must be quoted.** A finding with no quoted text, value, cell or
  filename is not a finding.
- **`blocked_on` is not a failure.** A component that could not be verified
  reports what was missing and lowers `confidence`. Never convert an
  unverifiable component into a fail.
- **Ignore the reviewer verdict in the task response.** The 1–5 score and
  feedback stored on an attempt were written by a reviewer about the
  **previous** attempt on that task. They do not describe the submission under
  review and must not be used as a calibration target.
- **Do not add components.** 28 is the whole form. Anything else you want to
  record is a note, not a score.

## Known contradictions in the CSV

Surfaced by the 1:1 mapping; resolve with whoever owns the form rather than
silently picking a reading:

- **PII / Safety** — the description says "a score of 3 `[Fail - Minor PII
  Violation]` is acceptable", the actual option is score **4** labelled
  `[Non-Fail - Minor PII Violation]`, and `errorCategories` lists
  `[All] [All] [Fail - Minor PII Violation]`. Three readings of one band.
- **Hardcoded Values**, **Framing**, and several others define a score-3 option
  but list only a `Fail` entry in `errorCategories`, leaving the non-fail label
  undefined.

## Cross-references

- `references/task-response-format.md` — where every evidence field lives, and
  what a hand-built `response.json` must contain.
- `references/source-conflicts.md` — the CSV, the contributor guidelines and the
  platform taxonomy disagree in places. Read it before blaming a contributor for
  a defect their tooling produced.
- `../audit-rubric.csv` — the authority, shipped with the skill. Regenerate
  after any change.
