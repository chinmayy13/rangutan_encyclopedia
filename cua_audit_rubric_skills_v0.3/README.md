# CUA v3 audit skill — v0.2

One skill that scores a CUA v3 task submission against the 28 components of the
audit rubric (`audit-rubric.csv`), the same form a human reviewer fills in.

The question it answers is narrow: **would this submission pass audit-rubric
review?** Not whether the task is good in some broader sense.

## What v0.2 changes

**No warehouse access anywhere.** v0.1 pulled the submission from Snowflake via
the external `redash` skill. That path is gone: the `cua-audit-task-browsing`
skill, its `fetch_task.py` and every credential-bearing dependency have been
removed, and the task files are supplied on disk instead.

```
tasks/<task_id>/response.json      the task response  (required)
tasks/<task_id>/task_meta.json     domain / sub_domain / OS flags
```

Attempt-level audits use `attempts/<attempt_id>/` with the same
`response.json` plus `attempt_meta.json`. Both locations are resolved exactly
as before, so nothing downstream changed shape.

**`audit_prepare.py` now also writes the submission in readable form.**
Alongside `bundle.json` it emits `prompt.md`, `rubric.json` and `task.md`, so
the prompt and the rubric can be read, diffed and version-controlled without
opening the response. `rubric.json` round-trips the criteria verbatim —
`{id, title, weight, annotations: {criteria_type, criteria_category}}`.

**`CUA_AUDIT_HOME` is now honoured by every script.** In v0.1 the fetcher and
`run_review.py` derived the workspace independently, so setting it split the
tree in half.

**Visual criteria are now actually visual.** Office and PDF deliverables are
rasterised to one PNG per page under `audit/<unit_id>/render/`, by the same
LibreOffice version the CUA VM runs. See
[Seeing the artifacts, not just reading them](#seeing-the-artifacts-not-just-reading-them).

**The evidence map survives as a reference.** Everything the browsing skill
documented that still applies — the JSON path for every field of
`response.json`, the four places that name the same files, the judge-breakdown
parse, and the minimum response to assemble when a submission arrives as loose
files — is now
`cua-audit-components/references/task-response-format.md`.

## What v0.1 added

Calibration ported from the deployed reference evals: the
worked examples, denominators, restraint cases and confirmed over-flags that the
CSV rows state a threshold for but never explain. It lives in `_generate.py`'s
`CALIB` map and renders into each component's **existing** sections — a *Before
you score* block under `## Score options`, and per-band notes under the score
they govern. No component gained a section, an answer option or a threshold.

Two consequences worth knowing:

- **`minor_issues` is a new output field, and it is never scored.** It carries
  defects the reference evals catch that no component's answer options name — format
  corruption, placeholder residue, criterion hygiene, conditional wording in a
  criterion, a rubric of 10–14 criteria.
  A clean pass stays a clean pass with entries in it. Because the score hides
  them by design, `component_review.html` renders a **Recommendations, not
  scored** block per submission even when every component scored 5, marks each
  affected component with an amber count in the score grid, and counts them in
  the header and triage table. `component_scores.csv` carries them too.
- **Five of those recommendations print in bold.** A recommendation is bolded
  when **both** halves hold: it is unscored here, because `audit-rubric.csv` has
  no answer option for it, **and** the reference eval fails a task on the same
  defect. Bold changes no score — it stops a reader skimming past a hard defect
  on a component showing 5.

  | Entry | Component | Reference severity |
  |---|---|---|
  | Domain fit and expertise level | 01 | FAIL |
  | Thin complexity | 01 | FAIL |
  | Spreadsheet-only deliverables | 06 | FAIL |
  | Prompt-constrained style not followed | 10 | `fail` — *"the prompt constrained the style and the file does not comply"* |
  | A criterion that tests both correctness and visual properties | 12 | *"a FAIL on its own, because the fix is a split rather than a refiling"* |

  Both halves are required, and that is what keeps the set at five. *Format /
  extension integrity* and *archive integrity* are `fail` in the reference eval,
  but component 10 already escalates them to score 2 when the file will not
  open, so bolding the leftover recommendation would double-signal.
  *Self-inconsistent typography*, *placeholder residue* and *mojibake* are
  `non_fail` — the reference visual zone calls self-inconsistency "the normal
  band" — so they stay plain even sitting beside a bolded sibling on the same
  component. The set lives in `_generate.py`'s `HARD_GATE`, mirrored in
  `scripts/render_html.py`.

```
skills/
└── cua-audit-components/        score a submission against the 28 components
```

## What's in the box

**`cua-audit-components`** holds one generated definition per rubric component
and the scripts that run them. Each component is scored by its own model call
reading only that component's definition and the evidence it needs.

Two references sit beside them. `references/task-response-format.md` is the
input contract: the exact JSON path for every field of a submission, and how
to assemble a `response.json` by hand. Read it first if you have never looked
at this project's data. `references/source-conflicts.md` says what wins when
the CSV, the contributor guidelines and the platform disagree.

## Everything derives from the CSV

`cua-audit-components/_generate.py` reads `audit-rubric.csv` and writes 28
component files. Each carries, verbatim, that row's id, question text,
description, every answer option with its score, the per-option justification
requirement, and the errorCategories label set.

Nothing the CSV says is paraphrased. What v0.1 adds alongside it — the `CALIB`
map — is guidance on *applying* those options, never a restatement of them, and
it is regenerated from the same script. Re-run the generator when either
changes:

```bash
python3 _generate.py            # regenerate
python3 _generate.py --check    # exit 1 if any file has drifted
```

Do not hand-edit a component file. Edit the CSV, or edit the generator's
`CLASS` / `EVIDENCE` / `CALIB` maps, and regenerate.

Two properties of the form that are easy to get wrong: score sets differ per
component, and seven components allow only 2 or 5 with no middle band. The JSON
schema handed to each model call enumerates only that component's legal scores,
so an out-of-band score cannot come back.

## Running it

```bash
A=cua-audit-components/scripts

# place tasks/<task_id>/{response,task_meta}.json first
python3 $A/audit_prepare.py <unit_id> --provision   # renderers + bundle + views + files
python3 $A/run_review.py <unit_id> --plan       # free: shows the plan
python3 $A/run_review.py <unit_id>              # 28 model calls + input consistency, one pool
python3 $A/sense_check.py <unit_id>             # read the 28 together
python3 $A/rollup.py                            # verdict + CSV + HTML
open audit/<unit_id>/component_review.html
python3 $A/summarize.py <unit_id>               # the results -> the fixes to make
open audit/<unit_id>/component_review_summary.html
```

Everything a run produces stays under `audit/<unit_id>/`, so one submission's
audit is one directory you can zip and send.

`audit_prepare.py` creates `audit/<unit_id>/` and writes:

```
audit/<unit_id>/
├── bundle.json             evidence index (incl. the mechanical pre-pass)
├── prompt.md               the prompt as shipped
├── rubric.json             the criteria, verbatim
├── task.md                 domain / sub_domain
├── files/inputs/*          downloaded input files
├── files/expected/*        downloaded expected files (the answer key)
├── inputs_extracted.md     input files dumped to text
├── expected_extracted.md   expected files dumped to text
├── render/inputs/<file>/page-NN.png      input files rasterised
├── render/expected/<file>/page-NN.png    expected files rasterised
└── render_index.json       what rendered, by which application and version
```

The review passes, `rollup.py` and `summarize.py` then add, in the same directory:

```
audit/<unit_id>/
├── components/NN.json      one result per component
├── sense_check.json        the senior review pass
├── input_consistency.json  do the supplied files agree with each other?
├── _components.jsonl       one line per component call: status, model, elapsed
├── component_scores.csv    one row per component
├── component_review.html   the report
├── component_review_summary.html   the fixes to make, in order; marks the audit finished
└── component_review_summary.json   the model's answer behind it, and every check it failed
```

If the file URLs in the response have expired, place the binaries in
`files/inputs/` and `files/expected/` yourself before running it: anything
already there and non-empty is left alone. Input files take the basename of
the VM path, expected files the verifier's `dest` string.

## Checking that the supplied files agree with each other

The review form grades one artifact at a time: the prompt, the expected files,
the rubric, the verifier JSON. Nothing on it grades the **input files** in
their own right, and nothing asks whether two supplied sources contradict each
other. Real tasks fail exactly there. A methodology PDF selects a cohort on
`BMI > 29.9 and glucose > 127.5`; the dataset's own `Reference` sheet defines
diabetic as `> 200`; the largest glucose value in the file is `199`, so that
second rule selects nobody while an outcome column already marks 268 positive
rows; and the answer key quietly uses neither. Every one of the 28 components
can score clean on that task.

`input_consistency.py` is one unscored opus call per unit that does only this,
in both directions — inputs against each other, and inputs against the prompt,
the expected files and the criteria. Findings are **major** when the
inconsistency changes what a correct submission looks like and **minor** when
it moves no graded output. It cannot touch a score or the verdict; it appears
as **Input file consistency** in the report's Triage section, in the same red /
amber / green the scores use.

`run_review.py` queues it in the same worker pool as the component calls,
right behind that unit's components: it starts beside them when a worker is
free, and otherwise as soon as every component call has started.
`--no-consistency` leaves it out; `input_consistency.py <unit_id>` runs it alone.

## Seeing the artifacts, not just reading them

`*_extracted.md` says what a file **contains**. It cannot show what it **looks
like**, and roughly a fifth of a CUA rubric's criteria are `visual` — chart
legibility, pagination, a table fitting on one page, overlapping shapes, an
empty section. v0.1 could only open files the Read tool displays natively
(`.png`, `.jpg`, `.gif`, `.webp`), so every visual criterion on a `.docx`,
`.xlsx`, `.pptx` or `.pdf` was scored from text or not at all.

v0.2 rasterises them. `audit_prepare.py` runs `render_files.py`, which turns
each staged non-image file into one PNG per page under
`render/<inputs|expected>/<filename>/`, and records in `render_index.json` what
produced each page and how far it can be trusted. The components' `files`
class is told to open those pages, and to put a file's layout in `blocked_on`
when the index says it is not visually verifiable — a renderer this host lacks
is never evidence of a defect in the submission.

**The renderer has to be the VM's application.** These tasks run on one fixed
Ubuntu image, whose applications and versions are pinned in
`cua-applications.csv`. LibreOffice 7.3.7.2 paginates a DOCX differently from
LibreOffice 25.x, so rendering with the wrong build produces page counts and
line breaks that were never the contributor's. `render_common.py` probes this
machine, compares each layout tool against its pinned row in that CSV, and
stamps every rendered file with `parity: exact | compatible | mismatch |
unknown`. On a mismatch, reflow-dependent claims are blocked; what is visible
regardless of reflow still counts.

`provision_renderers.py` installs the pinned build rather than the latest one
— the Document Foundation publishes every past release, so the CSV's version
is installable exactly. Everything lands under `~/.cua-renderers`, so it needs
no root and does not disturb an application you installed for yourself.

**You should not have to think about any of this.** `audit_prepare.py
--provision` works out which renderers a unit's files need, installs the
missing ones at the pinned version, and then renders. Without `--provision` it
still checks and prints the one command that fixes it. The document readers
below it are not even a prompt: the first run creates the venv and installs
them. And when an expected deliverable did not render but an install would
have fixed it, `run_review.py` performs that install itself and re-checks
rather than sending 28 model calls at evidence that is not there — it stops
only if the gap survives the fix.

```bash
python3 $A/audit_prepare.py <unit_id> --provision      # check, install, render
python3 $A/provision_renderers.py --for audit/<unit>   # plan for just that unit
python3 $A/provision_renderers.py                      # plan for every installable tool
python3 $A/render_files.py --tools                     # probe: found vs pinned, per tool
python3 $A/render_files.py --needed audit/<unit>       # tool names this unit lacks
python3 $A/render_files.py audit/<unit_id>             # re-render one unit
python3 $A/audit_prepare.py <unit_id> --no-render      # skip rendering entirely
python3 $A/run_review.py <unit_id> --skip-render-check # review unrendered anyway
python3 $A/run_review.py <unit_id> --no-auto-prepare   # print the fix, do not run it
```

Which tool each format needs, how to probe it, how to install it and which CSV
row it stands in for all live in `scripts/renderers.json`. A new file type is
an entry there, not a code change. Without LibreOffice the office formats fall
back to a first-page preview marked `degraded`; without any renderer they are
`unavailable`. Both are reported, never silently scored.

Narrowing: `--component 09 --component 16`, `--class files|rubric|other`,
`--workers N`. `--status` shows which components have run. A narrowed run
leaves input consistency out unless you add `--with-consistency`.

Optional final pass, worth running when you want a reviewer-shaped read rather
than 28 separate scores:

```bash
python3 $A/sense_check.py <unit_id>
```

It reads the 28 results together and reports what no single component can see:
contradictions between two components' claims, escalation proposals, which
component the verdict rests on, and a fix order. It cannot change a score and
can only propose moving one toward a fail, never away.

## Turning the report into something you can act on

`component_review.html` holds everything, which is why the one edit that clears
the verdict is hard to find in it. `summarize.py` is a last pass that pulls
those edits out:

```bash
python3 $A/summarize.py <unit_id>
```

It writes `component_review_summary.html` beside the report: the fixes numbered
in the order to do them, each with the text as it stands and the text to
replace it with, the file named and labelled GTF / input / prompt / rubric /
bundle, and an answer-key check on every step that edits a gold file. Every
input-consistency finding becomes a numbered fix too — nothing scores them, so
otherwise they are read and forgotten. After those fix sections, folded, it
lists every recommendation they do not cite, as its component wrote it; Python
adds that list, so it costs the model call nothing. It links to the report for
the scores and evidence rather than copying them.

It re-presents and never re-audits: no score moves and no finding is formed
that the results do not already state. The model gets the results themselves,
not the report — the components that scored below 5, every recommendation,
every group of value criteria that one input answers in full, the senior
review, the input-consistency result, the prompt and the criteria, each with
an id — in one call at `--effort high` with no tools, and answers in
JSON. A criterion it writes must pass the rubric components the way the task's
own criteria must: the prompt gives it their rules (no stated answer, no
conditional wording, one element, compared to the expected file), and the
rubric components are held to the same rules when they propose a rewrite,
since the summary quotes them. Python checks
that answer (every cited id exists, every quoted current text appears word for
word in the task's own files or in a quote the results took from them, every
GTF step has its answer-key check, no criterion it writes is conditional or
states a date or number the prompt does not give) and renders the page from a
fixed template, marking anything that failed a check.
A summary older than the results it is built from is rewritten by the next run.

## Requirements

- `claude` CLI, logged in. `run_review.py` runs a preflight that fails in
  seconds if the token is stale, rather than burning the per-call timeout.
- Python 3. The document readers used at prepare time, so the model calls
  never open binaries, are installed for you on the first run — `.venv/` in
  the workspace root, carrying `openpyxl`, `python-docx`, `python-pptx`,
  `pdfplumber`, `pymupdf` and `pillow`. Build it yourself if you would rather:
  ```bash
  python3 -m venv .venv
  .venv/bin/pip install openpyxl python-docx python-pptx pdfplumber pymupdf pillow
  ```
- The task files themselves, under `tasks/<task_id>/` or
  `attempts/<attempt_id>/`. No network service, credential or API key is
  involved. `audit_prepare.py` makes plain HTTPS requests to the public
  `scale-cds-*` buckets to stage the input and expected files, and `--no-files`
  skips even that.

Set `CUA_AUDIT_HOME` if `tasks/`, `attempts/` and `audit/` should live outside
this repo. Every script reads it, so the whole tree moves together.

## Models

Fixed per component by evidence class, always at `--effort max`. Pinned to exact
names rather than aliases, so results stay reproducible as the CLI updates.

| Class | Model | N |
|---|---|---|
| needs the input or expected files | `claude-opus-5` | 7 |
| judged from the rubric criteria | `claude-opus-5` | 14 |
| judged from the prompt or verifier JSON | `claude-sonnet-5` | 7 |

Change an assignment in `_generate.py`'s `CLASS` map and regenerate.

## Two ways to use this

**A contributor, on one task.** Run the whole thing once before submitting. The
`sense_check.py` output is the useful artifact: a verdict plus an ordered fix
list. For a faster loop mid-task, `--class rubric` covers the 14 components most
likely to be wrong.

**Calibration, on many tasks.** The 28 per-component JSON results are the data.
Each unit writes its own `audit/<unit_id>/component_scores.csv`, one row per
component, with the unit id in the first column so the set concatenates into
one table for comparison against human audit records.

## How well does it work

See `CALIBRATION_REPORT.md`. Measured on 27 submissions and 707 component
scores against human auditors: **precision 0.43, recall 0.21** treating score 1
or 2 as a fail.

Read that honestly. It over-flags roughly three times for every two agreed
fails, and it misses about four fifths of the fails a human records. Most of the
misses are a banding problem rather than a detection problem: the tool finds the
defect and scores it 3 where the auditor scored 2, because six components define
their fail condition as a share of the criteria and one to four real defects
cannot reach a 15% threshold on a 20 to 30 criterion rubric.

The report also documents two things that flatter the human side of the
comparison: 12 of 89 sampled disagreements are the auditor scoring against a
rule the CSV contradicts in writing, and 14 are correct tool findings the
auditor did not record.

**Treat the output as leads, not verdicts.** Every finding quotes its evidence
so you can check it.

## Known limits

- The tool reads a JSON bundle plus text extractions. It has no VM, no rendered
  artifacts and no platform UI, so some human findings are unreachable from its
  evidence. Expiring URLs are a confirmed case: the bundle builder strips the
  tokens upstream.
- Agent output artifacts sit in a private bucket and are not downloaded.
- A component that could not verify something reports `blocked_on` and lowers
  its confidence. That is not a pass. Check those before trusting a clean score.
- The whole bundle runs offline once the task files and their binaries are on
  disk, so it works in a sandbox with no warehouse and no network.
