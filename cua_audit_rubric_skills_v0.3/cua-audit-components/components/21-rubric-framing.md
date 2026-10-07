# 21. Rubric - Framing

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `de6f8f1c-3701-4af6-b54d-40645afe9f54` |
| title | Rubric - Framing |
| allowed scores | 2, 5 |
| required | true |
| evidence class | `rubric` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Framing of the Rubric dimension.

## Description (verbatim from the CSV)

```
Criteria should be positively framed, UNLESS the prompt explicitly asks to omit something.

GOOD: "The model does X"
BAD: "The model does not do X".
```

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- **Judge the criterion's main requirement**, not incidental wording, and count each offending criterion once. A criterion is positively framed when it states what the output does, includes, provides, displays or contains; negatively framed when its main requirement is what the output does *not* do.
- **Do not flag** a legitimate constraint, comparison, tolerance or condition merely because a "no" or a "without" appears inside it. "…fits within the page margins **without overflow**, and remains legible at normal zoom" is positive — and it is also the construction component 26 asks for, so flagging it would leave the author no compliant wording. "…reports the variance **without exceeding 10%**" states the acceptable result.
- **Genuinely negative**, both with positive rewrites available: "Body text and list items are **free of** formatting artifacts — no overlapping text, no truncation, no mixed list markers", where the only concrete content is a set of things that must not appear; and "**No slide** covers material outside the operations review".
- **Sweep the siblings.** This defect is copied more often than any other — one audited rubric had a negatively framed criterion caught and its structurally identical twin two rows down missed; another had three legibility criteria sharing one absence-framed construction, of which one was reported. Having found one, search for the same shape before you score.

### Score 2  — **justification REQUIRED**

```
[Fail - Framing]
At least 1 criterion is negatively framed—e.g., "Does not include...", "Fails to create..."—and this is not due to an omission request in the prompt
```

### Score 5  — justification not required

```
All criteria are positively framed.
| Negatively framed criteria stem from an omission request in the prompt.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Framing]`

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
  "component_id": "de6f8f1c-3701-4af6-b54d-40645afe9f54",
  "title": "Rubric - Framing",
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
