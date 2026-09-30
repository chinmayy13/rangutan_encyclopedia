# 08. Component: Prompt - Answer leakage

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `8c2ae7e1-6bcb-411e-a3f1-fdedb7fa0687` |
| title | Component: Prompt - Answer leakage |
| allowed scores | 2, 3, 5 |
| required | true |
| evidence class | `files` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Answer Leakage of the Prompt dimension.

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- Check this on every prompt. Leakage is among the most common prompt defects and the one most often missed — ask directly whether the agent could lift a graded value, the conclusion, or a required sentence straight out of the prompt and earn credit without doing the work.
- Decide against what is actually graded. Read `expected_extracted.md` and `criteria[]` first: leakage is defined by what the scored criteria look for, not by whatever the prompt happens to restate.

### Score 2  — **justification REQUIRED**

```
[Fail - Answer Leakage]
The prompt itself contains the answer content that scored criteria look for (specific values, the conclusion, or full sentences the deliverable must contain), so an agent could copy the prompt into its output and earn meaningful credit without doing the work.
```

### Score 3  — **justification REQUIRED**

```
[Non-Fail - Minor Leakage]
The prompt restates one or two secondary facts that also appear in the answer, but the core graded deliverable still requires work the prompt does not contain.
```

**Applies to this score.**

- One or two secondary facts restated, with the core graded deliverable still requiring work the prompt does not contain.

### Score 5  — justification not required

```
The prompt gives the task and context but none of the graded answer content; the agent must derive it from the inputs.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[Prompt] [All] [Non-Fail - Answer Leakage]`
- `[Prompt] [All] [Fail - Answer Leakage]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Multiple valid interpretations

An ambiguity matters when it changes the graded output. For each element of the request that could be read more than one way, list the defensible readings, then decide whether they produce *different* artifacts that `criteria[]` would score differently. If two competent submissions following different valid readings would be graded differently, the ambiguity is consequential and belongs in your score; if every valid reading converges on the same graded content, it does not. Where a method, statistic or convention is left unspecified and several standard choices give different numbers, that is consequential by definition.

Judge the request as the agent receives it. A supplied template or example file may narrow a reading, but only if it is unambiguous on the point in question; do not treat an attachment as curing an ambiguity it does not actually settle.

## Evidence to read

- `bundle.json` -> `prompt`, `criteria[]`, `input_files[]`, `expected_files[]`
- `inputs_extracted.md` — every input file dumped to text
- `expected_extracted.md` — every expected (answer-key) file dumped to text
- `render/inputs/<filename>/page-NN.png` and `render/expected/<filename>/page-NN.png` — each non-image file rasterised page by page: what it LOOKS like, as opposed to what the extraction says it contains
- `render_index.json` — per file: `status`, `visual_verifiable`, `parity`, `pages`, `unverifiable_reason`. Consult it before making any claim about appearance
- `files/inputs/` and `files/expected/` — the originals, for images
- `bundle.json` -> `staged_files` — any value starting `FAILED` did not download; say so rather than guessing

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
  "component_id": "8c2ae7e1-6bcb-411e-a3f1-fdedb7fa0687",
  "title": "Component: Prompt - Answer leakage",
  "score": <one of: 2, 3, 5>,
  "error_category": "<verbatim from the list above, or null>",
  "justification": "<required when the chosen score says so>",
  "evidence": "<quote the exact text, value, cell or filename>",
  "criteria": [<rubric criterion numbers, if applicable>],
  "confidence": "high|medium|low",
  "blocked_on": "<what you could not verify, or null>",
  "minor_issues": ["<non-scoring suggestion>", "..."]
}
```

Rules:

- Score **only** from the options above. The clean-pass score is `5`.
- A score whose option is marked **justification REQUIRED** must carry a non-empty `justification` naming the threshold it crosses and the evidence it rests on.
- Quote evidence. A finding with no quoted text, value or filename is not a finding — score the clean pass instead.
- If you could not verify something (a file would not open, an artifact is unavailable), set `blocked_on` and lower `confidence`; do not guess.
- Judge **this** submission only. Any reviewer score or feedback in the task response was written about the PREVIOUS attempt and does not apply here — ignore it.
- `minor_issues` is **never scored**. It carries suggestions that would improve the task but that this component's answer options do not name, so nothing you put there may change `score`, `error_category` or the verdict — and a clean pass stays a clean pass with entries in it. Use `[]` when there is nothing to record.
