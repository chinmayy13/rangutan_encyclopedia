# 07. Prompt - Timelessness

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `a1d00c99-1e0e-43c8-b7d9-b74e99319e9d` |
| title | Prompt - Timelessness |
| allowed scores | 2, 3, 5 |
| required | true |
| evidence class | `other` |
| subagent model | `claude-sonnet-5` at `--effort max` |

## Question

Rate the Timelessness of the Prompt dimension.

## Description (verbatim from the CSV)

```
All tasks must use historical or static data.

Time-sensitive framing that could mislead the model's trajectory is failing.

For arXiv content, a fixed historic version (e.g., https://arxiv.org/abs/<arxivID>v1) must be used.
```

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- Mild time framing over static inputs is the middle band, not the fail option. "It is March 2026 … the current cycle" does not change the correct answer when that answer derives from the attached files.

### Score 2  — **justification REQUIRED**

```
[Fail - Time-dependent Prompt]
The correct solution varies with time, e.g., live stock prices, real-time scores, current weather, etc.
| The prompt contains a time-sensitive count/claim—framed as trajectory confirmation—that may mislead the model, e.g., "There should be 113 results..."
```

**Applies to this score.**

- Reserve for a correct solution that genuinely varies with time — live prices, real-time scores, current weather, live inventory, an "as of today" page — or a time-sensitive count framed as trajectory confirmation. An unpinned arXiv reference is time-dependent because the paper it resolves to can change; a version-pinned one is not.

### Score 3  — **justification REQUIRED**

```
[Non-Fail - Minor Time-sensitivity]
The prompt contains some time-sensitive statements, but they don't affect the correct solution and won't mislead the model, i.e., they're only "background noise".
```

### Score 5  — justification not required

```
There are no time-sensitive references; data sources are verifiably static/archived.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Time-dependent Prompt]`
- `[All] [All] [Non-Fail - Minor Time-sensitivity]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Evidence to read

- `bundle.json` -> `prompt`, `seed_prompt`, `applications_used`
- `bundle.json` -> `input_files[]`, `verifier`, `mechanical`
- `bundle.json` -> `agent_issue_details` — often records a real environment failure

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Output contract

Return exactly one JSON object:

```json
{
  "component_id": "a1d00c99-1e0e-43c8-b7d9-b74e99319e9d",
  "title": "Prompt - Timelessness",
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
