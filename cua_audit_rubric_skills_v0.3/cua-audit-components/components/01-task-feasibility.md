# 01. Task - Feasibility

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `58db686e-d16d-413e-8e83-e54feb9ca6de` |
| title | Task - Feasibility |
| allowed scores | 2, 5 |
| required | true |
| evidence class | `other` |
| subagent model | `claude-sonnet-5` at `--effort max` |

## Question

Rate the Feasibility of the Task dimension.

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- Infeasibility is concrete and nameable: software that is not installed on the VM, a login or credential the agent cannot hold, a captcha, or a step the VM physically cannot perform. Name which one, and name the application the task would have needed.
- A browser lookup to a **stable public authority** for a historical fact is ordinary CUA work and is feasible. Do not read it as an infeasible external dependency.

### Score 2  — **justification REQUIRED**

```
[Fail - Infeasible Prompt]
The task cannot be completed in the VM, e.g., needs software that's not installed
```

**Applies to this score.**

- Quote the step you say cannot run and the capability it needs. `agent_issue_details` recording a real environment failure is evidence; your own doubt about difficulty is not.

### Score 5  — justification not required

```
The task is fully feasible.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Infeasible Prompt]`

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
  "component_id": "58db686e-d16d-413e-8e83-e54feb9ca6de",
  "title": "Task - Feasibility",
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
- `minor_issues` is **never scored**. It carries suggestions that would improve the task but that this component's answer options do not name, so nothing you put there may change `score`, `error_category` or the verdict — and a clean pass stays a clean pass with entries in it. Use `[]` when there is nothing to record.
- Record in `minor_issues` any of the following you find. Each entry quotes its evidence, names the file or criterion, and states the fix:
  - **Domain fit and expertise level** — the task really tests a different profession than its `domain` / `sub_domain` claims, or someone with only basic subdomain knowledge could complete it. Fit is carried by who is asking and the work context, not by the deliverable's genre, so do not record this merely because the output format is unexpected. Keep the opening phrase as written: this defect is a hard gate elsewhere in the project, so the report prints the whole entry in bold. It still does not affect your score.
  - **Thin complexity** — the task is retrieval or reorganisation rather than professional judgment, multi-step execution, cross-file reasoning, calculation or transformation. Keep the opening phrase as written: this defect is a hard gate elsewhere in the project, so the report prints the whole entry in bold. It still does not affect your score.
