# 12. Rubric - Categorization

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `7c7c74f0-5299-482d-8a5d-eeaea4e03068` |
| title | Rubric - Categorization |
| allowed scores | 2, 3, 5 |
| required | true |
| evidence class | `rubric` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Categorization of the Rubric dimension.

## Description (verbatim from the CSV)

```
See "Examples & Notes" tab in spec sheet for reference table.
```

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- **Category definitions.** `format_gate`: the required file was produced, or has the required file / organisational shape — filenames, file types and extensions, page count, slide count, word count, document length, folder and ZIP structure, and which worksheets a workbook contains. `correctness`: the agent got the content right — computed values, transformations, reasoning, classifications, recommendations, conclusions, heading names, column names, chart data values. `visual`: the output looks right — chart rendering, axes, scales, legibility, layout, typography, style, slide presentation, document section / page / template structure, and ordering where reasoning is not involved.
- **Disambiguation, most-missed first.** A *value* inside a visual element is `correctness` — the axis label text, the KPI number on a tile, the figure in a callout, the total in a rendered table; only its rendering, spacing and legibility are `visual`. Display rounding is `visual`, computational precision is `correctness`. Chart rendering is `visual`, chart plotted values are `correctness`. Folder, ZIP and worksheet arrangement is `format_gate`; document layout *within* a file is `visual`. Named column headers and heading names are `correctness` — the names are content even though they sit in a layout. A conclusion the agent drew by inspecting a supplied image is `correctness`; the word "visual" appearing in the criterion text is not the signal.
- **Ordering** is `visual` by default and `correctness` only when the order is itself the output of a reasoning step. The test: could the agent produce the required order without doing any of the task's analysis? "in the order China, USA, India" → handed down, `visual`. "in ascending order of 2025 GDP per capita" → derived, `correctness`.
- **Being mandated by the prompt does not decide the category.** A property the prompt required is still `visual` if what it tests is a rendering property.
- **Group same-shape criteria and judge them as a unit.** Miscategorisations come in pairs and triples, because a contributor writes one criterion and copies it to its siblings and the copies inherit the category. Catching one of a pair and leaving its twin makes the survivor read as a deliberate choice.
- **Your own uncertainty is not a miscategorisation.** Where the rules above do not settle a call, leave the criterion as filed and do not count it toward the share.
- **Not defects, all three confirmed over-flags.** Page, slide and word counts **are** `format_gate` and **are** `REGULAR`. An unordered set of required topic areas is `correctness` — "numbered sections" is not automatically document structure; an *ordered* section skeleton is `visual`. Which worksheets a workbook contains is `format_gate`, not `visual`.

### Score 2  — **justification REQUIRED**

```
[Fail - Categorization]
15%+ criteria are incorrectly categorized ("Format Gates", "Correctness", "Visual")
```

**Applies to this score.**

- **Gating impact takes this option on its own, whatever the share.** `MUST-PASS` assigned to a criterion that is not a file-existence or file-type/extension gate — including one that bundles such a check in alongside the gate — silently gates the whole task on formatting, so it fails here even when the misfiled share is under the threshold. The mirror case, a genuine file gate left `REGULAR`, has no gating impact and belongs in the band below. Component 24 scores the same tag under the weighting protocol; both readings stand, and each scores its own question.

### Score 3  — **justification REQUIRED**

```
[Non-Fail - Categorization]
<15% an isolated category or type slip with no gating impact.
```

**Applies to this score.**

- Under the threshold and with no gating impact — an isolated category or type slip. Every criterion in this band must still be named, with the pair it currently carries and the pair it should.

### Score 5  — justification not required

```
All criteria are correctly categorized.
| All criteria have correct type classifications.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Categorization]`
- `[All] [All] [Non-Fail - Categorization]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Counting instances

This component's threshold is a share of the criteria, so the verdict turns on the count. Walk **every** criterion in `criteria[]` and record a verdict for each: does it exhibit the defect, yes or no. Report the count, the denominator and the resulting percentage, and list the criterion numbers on both sides of the line. Do not report only the ones you decided count.

One criterion moves the share by three to five points on a typical rubric, which is enough to cross the threshold on its own. When a criterion is borderline, say so explicitly and say which way you resolved it. If including the borderline cases would cross the threshold, report both figures and take the stricter band; a defect the form names is not excused by being one instance short.

## Scope, not just presence

A guard or a label is not enough on its own; it has to cover the thing at risk. For each criterion in scope, name the specific element that could be degraded or mis-handled, then check whether the guard or category actually covers **that element**. A guard scoped to one element leaves every other element unprotected, and a criterion that spans two categories is mis-categorised even when the category it carries is defensible for part of it. Report the element and the coverage, not the existence of the clause.

## Evidence to read

- `bundle.json` -> `criteria[]` — each `{n, id, title, weight, category, type}`
- `bundle.json` -> `prompt` — for coverage and framing only
- `bundle.json` -> `mechanical` — precomputed counts and weight shares; trust them, do not recompute

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Output contract

Return exactly one JSON object:

```json
{
  "component_id": "7c7c74f0-5299-482d-8a5d-eeaea4e03068",
  "title": "Rubric - Categorization",
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
  - **A criterion that tests both correctness and visual properties**, so that no single filing is correct for it — a presentation wrapper carrying a required content list, for example. The fix is a split, not a refiling: name **both** target `criteria_category` / `criteria_type` pairs. Keep the opening phrase as written: this defect is a hard gate elsewhere in the project, so the report prints the whole entry in bold. It still does not affect your score.
