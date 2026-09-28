# 05. Prompt - GUI Integration

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `a45a178b-8e59-4e45-9163-794bcb395b60` |
| title | Prompt - GUI Integration |
| allowed scores | 2, 3, 5 |
| required | true |
| evidence class | `other` |
| subagent model | `claude-sonnet-5` at `--effort max` |

## Question

Rate the GUI Integration of the Prompt dimension.

## Description (verbatim from the CSV)

```
GUI interaction is a defining requirement of CUA v3.

Reward UI work that affects the observable output (e.g., "adjust the translated German text so it fits the text box without overlapping the chart, then preview the slide").

Do not reward GUI-for-its-own-sake ("open the file and click around").
The GUI action must be verifiable in the output artifact.
```

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- **Apply the GUI evidence test before scoring.** Do not judge GUI by vibes or by the presence of a verb like "open", "review" or "check". Write down two things: **(1) the action** — the specific thing the agent must do in the interface, quoted from the prompt; and **(2) the artifact change** — what would look different in the deliverable if the agent skipped it. Both must be nameable from the prompt's own words.
- Worked contrasts. "adjust the translated German text so it fits the text box without overlapping the chart, then preview the slide" → action and artifact change both nameable, **meaningful**. "use print-preview to make sure the sheet prints on one page" → **meaningful**. "open the workbook and review the data before summarising" → no artifact change; the summary is identical either way. "keep the existing template's formatting" → nothing the agent must observe.
- Restraint — a supplied visual reference is **not** minimal GUI. Where the agent must read a layout out of an image to know what to produce, and a readability requirement lands on the rendered output, both are real GUI work with nameable artifact changes.

### Score 2  — **justification REQUIRED**

```
[Fail - Lacking GUI Action]
The prompt lacks any meaningful GUI interaction where the deliverable plainly calls for it.

e.g., A layout/print/visual/animation/browser task solvable entirely via script with no observable UI decision.
```

**Applies to this score.**

- Take this option only when you **cannot name the artifact change** — skipping the interface work would leave the graded output identical. State the action you found and the artifact change you could not.

### Score 3  — **justification REQUIRED**

```
[Non-Fail - Minimal GUI Action]
The prompt contains a GUI interaction, but it's minimal or only loosely tied to the deliverable.
```

**Applies to this score.**

- You can name both the action and the artifact change, but the change is cosmetic or only loosely tied to the deliverable. Report it rather than escalating: the observed problem on this component is this band going **unreported**, not the fail option being too loose.

### Score 5  — justification not required

```
The prompt contains a meaningful GUI interaction that changes what the agent must observe or do.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Lacking GUI Action]`
- `[All] [All] [Non-Fail - Minimal GUI Action]`

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
  "component_id": "a45a178b-8e59-4e45-9163-794bcb395b60",
  "title": "Prompt - GUI Integration",
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
