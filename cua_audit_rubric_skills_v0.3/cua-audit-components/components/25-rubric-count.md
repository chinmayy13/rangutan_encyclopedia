# 25. Rubric - Count

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `4f4f7cfc-1c98-46fb-b779-b61820061c90` |
| title | Rubric - Count |
| allowed scores | 2, 5 |
| required | true |
| evidence class | `rubric` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Count of the Rubric dimension.

## Description (verbatim from the CSV)

```
The rubric should contain between 10–30 criteria.
```

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- Trust `mechanical.25_rubric_count` for `n_criteria`.
- Check any fix another component prescribes against this band: a split that would push the rubric past 30, or a merge or deletion that would drop it below 10, is not a legal remedy.
- An over-30 rubric is usually a tooling defect — the generator's `criteriaCount` is 50 — and a sub-10 rubric submits cleanly because `minCriteria` is 0. See `references/source-conflicts.md`.

### Score 2  — **justification REQUIRED**

```
[Fail - Count]
The rubric contains fewer than 10 criteria
| The rubric contains more than 30 criteria
```

### Score 5  — justification not required

```
The rubric contains between 10–30 criteria.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Count]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Evidence to read

- `bundle.json` -> `criteria[]` — each `{n, id, title, weight, category, type}`
- `bundle.json` -> `prompt` — for coverage and framing only
- `bundle.json` -> `mechanical` — precomputed counts and weight shares; trust them, do not recompute

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Output contract

Return exactly one JSON object:

```json
{
  "component_id": "4f4f7cfc-1c98-46fb-b779-b61820061c90",
  "title": "Rubric - Count",
  "score": <one of: 2, 5>,
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
  - **A rubric of 10–14 criteria** is allowed — the CSV's range is 10–30 and this scores a clean 5 — but it sits below the 15–30 target the project aims for. Record it as a warning with the suggestion to add criteria up to 15; it **does not affect the score**.
