# 18. Rubric - Overfitting

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `fed588c5-689e-495c-b522-71a8279ab740` |
| title | Rubric - Overfitting |
| allowed scores | 2, 3, 5 |
| required | true |
| evidence class | `rubric` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Overfitting of the Rubric dimension.

## Description (verbatim from the CSV)

```
Criteria should not penalize valid fulfillments of the prompt or hone in on overly specific implementations.

Examples of overfitting:
Mandating ground-truth specific output wording/attribution or an output filename the prompt never specifies
| - Demanding exact equality where the prompt permits variation
| - Penalizing valid rounding, semantically equivalent prose, defensible methods, or visually comparable layouts.
```

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- **Check the requirement's source before flagging.** A detail is overfit only when it is left open by the prompt **and** prescribed by no input file. The prompt plus the input files together are the decisive input, and every finding must be checked against both.
- A detail is an explicit requirement — and the criterion is **not** overfit — when it is: a section, heading, field or bracketed placeholder instruction contained in a supplied **template**; a calculation, formula, methodology or convention prescribed by a supplied **methodology, specification or runbook**; a column name, key, unit or structure fixed by a supplied **schema, data file or code file**; a visual convention fixed by a supplied **style reference**; or a specific value, date, rounding rule or prescribed field value stated in a supplied **SLA or briefing**. Each of these has been flagged as overfit and each flag was overturned.
- **Archetypes, once the source check comes back empty.** The *mirrored criterion* — the same constraint correctly grounded on one entity and invented on its neighbour, the single most reliable signal. *Placement is not cardinality* — apply the negation test to every "exactly N", "only", "no additional" and "and nothing else": does the prompt or an input actually forbid the extra thing? *A display form mandated where any form works* — the prompt named the content, not whether it is a table. *Semantic equivalence demanded on an element the prompt left open.* *A visual anchor governing a stylistic choice* rather than a legibility judgment.
- **Rounding imported from the answer key.** Open the expected file and read what a graded cell **stores**, not what it displays. Where the answer key stores a rounded derived value — a coverage share held as `0.303`, a rate held as `0.9031` — and the criterion says only "matches the corresponding expected file", the gold's rounding becomes the requirement: a response holding the exact quotient is marked wrong, and the exact quotient is usually the number the gold itself carried forward into its own downstream figures. That is a display artifact promoted to a graded constraint, and it is overfitting whether or not the author intended it. Quote the stored value and the exact value, and prescribe either a tolerance or an explicit rounding instruction. Screen every criterion whose graded value is *computed* rather than copied; a bare "match" is safe only on a value with one exact representation.
- **An anchor on an absence.** A criterion phrased as an exclusion — "excludes the transfer in and lapsed encumbrances", "omits the prior-year column", "does not count X" — that is then anchored with "matching the corresponding expected file" stops grading the exclusion and starts grading the gold's **depiction** of it: a reconciliation line, a struck row, a footnote naming what was left out. A response that simply never counted the excluded items, which is the behaviour the prompt asked for, has nothing to match and fails. Grade the consequence — the resulting figure, computed without the excluded items — not the display of the omission. Beware of reading such a criterion as a *guard*: an exclusion anchored to a file is a form requirement wearing a guard's clothes.
- **Restraint.** Anchoring a legibility or containment judgment to the expected file is sound construction, not overfitting. An inherited public API in a supplied codebase is a preserved interface, not a mandated construct. Grading a *function* without prescribing a heading, wording or position is not dictating a form. And a requirement the supplied **data** makes unavoidable is not overfit — ask whether a *correct* answer could omit it; if it could not, the criterion stands.
- Count criteria, not phrases: a criterion with several overfitting issues counts once. When uncertain, leave it unflagged. Whether a criterion restates a literal answer is a hardcoded-values question and belongs to component 13, not here.

### Score 2  — **justification REQUIRED**

```
[Fail - Overfitting]
At least 15% of the  criteria are overfit (i.e., valid alternate implementations would be penalized)
```

### Score 3  — **justification REQUIRED**

```
[Non-Fail - Overfitting]
<15% of the criterion are overfit (i.e., valid alternate implementations would be penalized)
```

### Score 5  — justification not required

```
The rubric does not contain any overfit criteria.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Overfitting]`
- `[All] [All] [Non-Fail - Overfitting]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Multiple valid interpretations

An ambiguity matters when it changes the graded output. For each element of the request that could be read more than one way, list the defensible readings, then decide whether they produce *different* artifacts that `criteria[]` would score differently. If two competent submissions following different valid readings would be graded differently, the ambiguity is consequential and belongs in your score; if every valid reading converges on the same graded content, it does not. Where a method, statistic or convention is left unspecified and several standard choices give different numbers, that is consequential by definition.

Judge the request as the agent receives it. A supplied template or example file may narrow a reading, but only if it is unambiguous on the point in question; do not treat an attachment as curing an ambiguity it does not actually settle.

## Counting instances

This component's threshold is a share of the criteria, so the verdict turns on the count. Walk **every** criterion in `criteria[]` and record a verdict for each: does it exhibit the defect, yes or no. Report the count, the denominator and the resulting percentage, and list the criterion numbers on both sides of the line. Do not report only the ones you decided count.

One criterion moves the share by three to five points on a typical rubric, which is enough to cross the threshold on its own. When a criterion is borderline, say so explicitly and say which way you resolved it. If including the borderline cases would cross the threshold, report both figures and take the stricter band; a defect the form names is not excused by being one instance short.

## Evidence to read

- `bundle.json` -> `criteria[]` — each `{n, id, title, weight, category, type}`
- `bundle.json` -> `prompt` — for coverage and framing only
- `bundle.json` -> `mechanical` — precomputed counts and weight shares; trust them, do not recompute
- `expected_extracted.md` — required for the rounding check: a criterion that says "matches the corresponding expected file" inherits whatever the answer key stores, so you cannot judge it without reading the stored values
- `inputs_extracted.md` — required for the source check: a detail is overfit only when no supplied template, schema, methodology or data file already prescribes it

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Output contract

Return exactly one JSON object:

```json
{
  "component_id": "fed588c5-689e-495c-b522-71a8279ab740",
  "title": "Rubric - Overfitting",
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
- **A criterion you propose must pass the rubric itself.** Replacement or new criterion text you write, in `justification` or `minor_issues`, is judged by the rubric components the way the task's own criteria are. It never states the value, name, date, count or conclusion the agent has to produce: it names the expected file and a comparison — a tolerance on a derived number, semantic equivalence on prose — and only a value the prompt itself gives may appear. It has no conditional wording ("if …", "unless …", "where applicable", "when present", "if any", "any X it reports"): the task's inputs already fix which case holds, so it grades that case's outcome. It tests one element. A criterion that grades what the prompt never asks for is removed, folded into another, or backed by a prompt change, never made conditional.
- `minor_issues` is **never scored**. It carries suggestions that would improve the task but that this component's answer options do not name, so nothing you put there may change `score`, `error_category` or the verdict — and a clean pass stays a clean pass with entries in it. Use `[]` when there is nothing to record.
- Record in `minor_issues` any of the following you find. Each entry quotes its evidence, names the file or criterion, and states the fix:
  - **A loosening must be bounded by the observable outcome.** A permission clause that shelters genuinely wrong answers is a worse defect than the overfitting it cures. Write the clause you would prescribe, then ask what a wrong answer could now slip past it — "any implementation that renders as a constant line at the same value across the full date range" is bounded; "citing other provisions does not detract" is not.
  - **Never recommend spreading an existing tolerance band across the rubric.** Uneven bands are not in themselves a defect, and "these six criteria carry `±1%` and those six do not" is not a finding. Before proposing a band anywhere, classify the value: *transcribed* (copied off a supplied page, cell or table, so exactly one answer is right) or *derived* (computed, so rounding and step order legitimately move the last digits). A band belongs only on a derived value. On a transcribed one it admits a wrong number and is itself the defect — which component 27 scores, not this one. If you record a tolerance observation here at all, state the classification and what the band is worth in the value's own units.
