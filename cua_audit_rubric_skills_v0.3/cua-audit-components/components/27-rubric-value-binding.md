# 27. Component: Rubric - Value Binding

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `d77b518d-fd8c-467d-8717-d5e7b05327c4` |
| title | Component: Rubric - Value Binding |
| allowed scores | 2, 3, 5 |
| required | true |
| evidence class | `rubric` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Value Binding of the Rubric dimension.

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- **Anchoring to a whole file instead of the element inside it is the same defect in another costume.** "The basket language quoted in `leverage_memo.docx` is semantically equivalent to the corresponding expected file" compares a quotation to an entire document. Where the comparison target is a section, a table row, a slide, a cell or a quoted passage, the anchor must name it.
- This is **distinct from atomicity**: a criterion can test exactly one value (atomic) and still fail to bind it to a location. Score it here, not there, and do not charge the same criterion to both.
- **A tolerance band on a transcribed figure unbinds the value.** Classify every numeric criterion's value first: *transcribed* — copied off a supplied page, cell or table, so exactly one answer is right and no method variance exists — or *derived*, computed from the inputs, where rounding and step order legitimately move the last digits. A band on a derived value is sound construction and is never a finding. A band on a transcribed one turns a single correct answer into a range of accepted ones, which is the score-5 conjunct "guard against extraneous candidate values appearing as correct" failing: the extraneous candidates are every number inside the band. Do the arithmetic and put it in evidence — "`±1%` of the `$15,481,203` income tax line is `±$154,812`, so a figure off by six figures passes" — because the band reads harmless until it is priced. Uneven bands across the rubric are not the issue and must not be reported as one.
- **Look for one supplied artifact that already contains the whole answer.** Before clearing a group of value criteria, open the inputs and ask whether a single page, column, table or cell block prints every figure that group grades. Where it does, a response that reproduces that artifact verbatim and unlabelled carries every graded value and passes them all without performing the task — which is this component's fail option in its own words, "cannot tell a correctly placed answer from a dump of every candidate". Name the source artifact and list the criteria it satisfies at once. Derived values are the defence: a group is safe when at least one of its figures must be computed and so appears in no input. Check that fund by fund, entity by entity — a rubric is often safe on the entity whose figures are computed and wide open on the one whose figures are transcribed.

### Score 2  — **justification REQUIRED**

```
[Fail - Unbound Value]
A value criterion only requires the value to appear somewhere in the file, with no binding to its correct row, column, or label and no guard against other candidate values also appearing, so it cannot tell a correctly placed answer from a dump of every candidate.
```

### Score 3  — **justification REQUIRED**

```
[Non-Fail - Somewhat Unbound Value]
The criterion requires the value in labeled context but does not explicitly rule out other candidate values also appearing.
```

### Score 5  — justification not required

```
Value criteria bind each value to its correct label, row, or column, and guard against extraneous candidate values appearing as correct.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Unbound Value]`
- `[All] [All] [Non-Fail - Somewhat Unbound Value]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Binding is a pairing, not co-occurrence

A criterion naming a value and a label in one sentence does not bind them. Ask the CSV's own question: could a submission carry every correct label and every correct value, paired wrongly, and still pass? If yes, the value is unbound. Binding needs an explicit pairing (each value associated with its own row, column or label) plus a guard against extra candidate values.

## Evidence to read

- `bundle.json` -> `criteria[]` — each `{n, id, title, weight, category, type}`
- `bundle.json` -> `prompt` — for coverage and framing only
- `bundle.json` -> `mechanical` — precomputed counts and weight shares; trust them, do not recompute
- `inputs_extracted.md` and `render/inputs/<filename>/page-NN.png` — needed to see whether one supplied artifact already prints every figure a group of criteria grades
- `expected_extracted.md` — the labels, rows and columns a criterion would have to name to bind its value

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Looking at the artifacts

You can read images directly. Use the Read tool on any `.png`, `.jpg`, `.gif` or `.webp` under `files/inputs/` or `files/expected/` and judge what it actually shows: axis labels, series, legends, value labels, what the picture depicts, whether it matches its filename and what the prompt says about it. The text extraction lists these files as `IMAGE` with dimensions only; that is a limit of the extraction, not of you. Never score a component clean on an artifact you did not look at. If a file genuinely will not open, set `blocked_on` and lower `confidence`.

Everything else that has a visual form — `.docx`, `.xlsx`, `.pptx`, `.pdf`, `.html`, and the rest — has already been rasterised for you, one PNG per page, under `render/<side>/<filename>/page-NN.png`. The prompt lists the exact page files.

**Open them with the Read tool before you score, and do it first.** Not `cat`, not `head`, not a Python one-liner: a PNG carries no text for Bash to print, and the `text.txt` beside the pages is text, not appearance. Reading the chart XML out of an `.xlsx`, or the slide XML out of a `.pptx`, tells you a chart was declared — it cannot tell you the axis labels are legible, the series fit, the columns are not clipped or the table did not spill onto a second page.

The pages are the only evidence that shows pagination, clipping, column overflow, overlapping shapes, blank pages, chart legibility and whether something fits on one page. So: any statement you make about appearance must name the page file you opened to see it. An appearance claim you did not look at is not a finding, and it is not a clean pass either.

Never render anything yourself and never attempt a `pip install` or an application install. Extraction and rendering are both already done. Open an original only when it is an image.

### What the render is worth — check `render_index.json` first

The entry for a file states how far its appearance can honestly be judged. Respect it literally.

- `visual_verifiable: true` — the pages are a faithful render. Judge appearance from them.
- `visual_verifiable: false` (`status` `degraded` or `unavailable`) — the renderer for that format is missing or only a first-page preview was produced. Its `unverifiable_reason` says which. Every ask about that file's layout goes in `blocked_on` with that reason. A renderer this audit host lacks is never evidence of a defect in the submission.
- `truncated: true` — pages beyond the ones listed were not rendered. Say nothing about them.
- `parity` — whether the application that laid these pages out is the version the CUA VM runs (`cua-applications.csv`). `exact` or `compatible`: pagination claims are sound. `mismatch` or `unknown`: what you see may be this host's LibreOffice rather than the VM's, so claims that depend on exact reflow — total page count, a table fitting on one page, a specific line break — go in `blocked_on`. What is visible on the page regardless of reflow (a missing chart, an empty section, a wrong label, overlapping shapes) stands as a finding.

## Required method — reproducibility of the expected artifact

Do this before you score. The question is not whether the expected files agree with one another; it is whether a competent agent could arrive at them from what it is actually given.

1. Inventory what the agent has. List the input files. For every input that is a script, template, schema or config, state the outputs it can generate and the vocabulary, labels and ranges it can emit.
2. For each graded value in the expected files, name the specific input it derives from and the operation that produces it. Recompute it where it is computable.
3. Mark every value you cannot reach, and say why — absent from all inputs; requires a label, constant or category the provided code cannot emit; requires data the agent never receives; requires a step the inputs do not support.
4. Report both halves in `justification`: what you reconstructed, and what you could not reach.

**Reachable is not the same as correct.** Step 3 establishes only that a value can be derived from the inputs. It says nothing about whether the value is right. Both must hold, and correctness is the more important of the two. Separately check: is the arithmetic right; does the artifact satisfy every request the prompt and any supplied template make, including sections or fields left blank; do the inputs actually contain what their filenames and the prompt claim they contain; and is the content true against the domain rather than merely internally consistent. A traceable value that is wrong, and an artifact that is accurate but incomplete against the template, are both defects. State the correctness check you ran, not only the derivation.

A label or wording is a presentation choice **only if no criterion grades it**. Check `criteria[]`: once a criterion compares that cell, field or label to the expected file, it is a graded value, and "the agent could have phrased it differently" is not available as a defence — the criterion demands the expected file's version specifically.

A graded value the agent cannot reach is **not** cosmetic and **not** a disagreement between expected files. It is unreachable, every criterion anchored to it is unsatisfiable. Report it. But score **only** against this component's own answer options: if none of them describes unreachability, this finding does not change your score, and it belongs in `justification` as context. Never stretch an option's wording to fit a defect it does not name.

## Output contract

Return exactly one JSON object:

```json
{
  "component_id": "d77b518d-fd8c-467d-8717-d5e7b05327c4",
  "title": "Component: Rubric - Value Binding",
  "score": <one of: 2, 3, 5>,
  "error_category": "<verbatim from the list above, or null>",
  "justification": "<required when the chosen score says so>",
  "evidence": "<quote the exact text, value, cell or filename>",
  "criteria": [<rubric criterion numbers, if applicable>],
  "confidence": "high|medium|low",
  "blocked_on": "<what you could not verify, or null>",
  "whole_answer_inputs": [{"criteria": [<one group's value criteria>], "input": "<file and page, column, table or cell block that prints all their values, or null>"}, "..."],
  "minor_issues": ["<non-scoring suggestion>", "..."]
}
```

Rules:

- Score **only** from the options above. The clean-pass score is `5`.
- A score whose option is marked **justification REQUIRED** must carry a non-empty `justification` naming the threshold it crosses and the evidence it rests on.
- Quote evidence. A finding with no quoted text, value or filename is not a finding — score the clean pass instead.
- If you could not verify something (a file would not open, an artifact is unavailable), set `blocked_on` and lower `confidence`; do not guess.
- Judge **this** submission only. Any reviewer score or feedback in the task response was written about the PREVIOUS attempt and does not apply here — ignore it.
- **`whole_answer_inputs` is required.** It records the check above for one supplied artifact that already contains the whole answer: one entry per group of value criteria, giving the group's criterion numbers and the input that prints every value the group grades — the file plus the page, column, table or cell block — or `null` when no single input does. Text values such as material names count, not only numbers: a column that lists every material name a group grades prints that group's whole answer. Use `[]` only when the rubric has no value criteria.
- **A criterion you propose must pass the rubric itself.** Replacement or new criterion text you write, in `justification` or `minor_issues`, is judged by the rubric components the way the task's own criteria are. It never states the value, name, date, count or conclusion the agent has to produce: it names the expected file and a comparison — a tolerance on a derived number, semantic equivalence on prose — and only a value the prompt itself gives may appear. It has no conditional wording ("if …", "unless …", "where applicable", "when present", "if any", "any X it reports"): the task's inputs already fix which case holds, so it grades that case's outcome. It tests one element. A criterion that grades what the prompt never asks for is removed, folded into another, or backed by a prompt change, never made conditional.
- `minor_issues` is **never scored**. It carries suggestions that would improve the task but that this component's answer options do not name, so nothing you put there may change `score`, `error_category` or the verdict — and a clean pass stays a clean pass with entries in it. Use `[]` when there is nothing to record.
