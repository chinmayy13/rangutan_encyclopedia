# 20. Rubric - Objectivity

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `635195ed-1833-49a5-bd7e-c1b45fa1fff4` |
| title | Rubric - Objectivity |
| allowed scores | 2, 3, 5 |
| required | true |
| evidence class | `rubric` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Objectivity of the Rubric dimension.

## Description (verbatim from the CSV)

```
Criteria evaluation should not revolve around subjectivity or cannot be objectively evaluated —e.g., "good", "nice", "appropriate", etc.

 An important caveat to this is that "Visual" criteria are allowed to use subjective phrasing, such as "professional comparable/appropriate".
```

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- The denominator is the **non-visual criteria only**, since visual criteria are expressly permitted subjective phrasing. Worked count: with 20 non-visual criteria, 10% is exactly 2, so 3 or more takes the fail option.
- Permitted and **not** subjective: "professionally comparable / appropriate" on a visual criterion, and "similar to / semantically comparable to the expected file" on a correctness criterion.

### Score 2  — **justification REQUIRED**

```
[Fail - Objectivity]
More than 10% of the rubric's criteria are subjective or cannot be objectively evaluated (non-visual).
```

### Score 3  — **justification REQUIRED**

```
[Non-Fail - Objectivity]
Up to 10% of the rubric's criteria are subjective or loosely worded but still reasonably gradable (non-visual).
```

### Score 5  — justification not required

```
All criteria are reasonably objective.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Objectivity]`
- `[All] [All] [Non-Fail - Objectivity]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Counting instances

This component's threshold is a share of the criteria, so the verdict turns on the count. Walk **every** criterion in `criteria[]` and record a verdict for each: does it exhibit the defect, yes or no. Report the count, the denominator and the resulting percentage, and list the criterion numbers on both sides of the line. Do not report only the ones you decided count.

One criterion moves the share by three to five points on a typical rubric, which is enough to cross the threshold on its own. When a criterion is borderline, say so explicitly and say which way you resolved it. If including the borderline cases would cross the threshold, report both figures and take the stricter band; a defect the form names is not excused by being one instance short.

## Evidence to read

- `bundle.json` -> `criteria[]` — each `{n, id, title, weight, category, type}`
- `bundle.json` -> `prompt` — for coverage and framing only
- `bundle.json` -> `mechanical` — precomputed counts and weight shares; trust them, do not recompute

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Output contract

Return exactly one JSON object:

```json
{
  "component_id": "635195ed-1833-49a5-bd7e-c1b45fa1fff4",
  "title": "Rubric - Objectivity",
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
  - **Criterion hygiene** — malformed markup (a filename with a missing opening backtick, a mismatched delimiter, a rubric where no filename is backticked at all), missing terminal punctuation, a doubled space, a stray character left from an edit, or ungrammatical wording that survived a rewrite. These cost nothing to fix and distort no grading, so they **do not affect the score**. Record them as **one grouped entry** naming the criteria affected, not one entry per criterion. The exception is already scored: where the wording is so broken that the criterion cannot be graded as written, it is no longer hygiene — it is not objectively evaluable, and it counts toward this component's bands.
  - **Conditional wording** — a criterion whose requirement holds only in some case: "if …", "unless …", "where applicable", "when present", "if any", "depending on …". The grader must settle the condition before it can grade, often from input files it never sees, and a response that avoids the case passes without doing the work. The task's inputs and expected file already fix which case holds, so the fix grades that case's outcome against the expected file: "If the starting total includes the transfers, it subtracts them" becomes "The adjusted total in `report.xlsx` matches the corresponding value in the expected file within ±1%". A condition copied from the prompt resolves the same way. Record every conditional criterion in **one grouped entry**, quoting each condition; this **does not affect the score**.
