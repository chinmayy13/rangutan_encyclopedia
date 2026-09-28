# Source conflicts and their resolutions

Where the instruction sources disagree, this file records the rule that wins and
what was overridden. Cite `§12.x` from the parent skill in findings; cite this
file when a contributor appears to have followed a losing source.

**Sources.** `S1` the 7 annotator-guideline PDFs (master spec, prompt handbook,
rubric examples, pre-submission checklist, common errors, FAQ, glossary).
`S2` this skill's `audit-rubric.csv`, the 28-dimension grading form.
`S3` the platform workflow taxonomy — including the
rubric-generator system prompt at
`before[6].params.criteriaPrefiller.systemPrompt` and the widget constraints.

**The general precedence rule.** For *grading*, **S2 wins** — it is the
instrument reviewers score against. For *authoring guidance*, S1 wins. S3 is
neither authoritative nor harmless: it is what the contributor's tooling
actually did, so when S3 loses, the defect it produced is a **tooling defect**
and the contributor should not be penalised for it.


---

## 1. Correctness weight-share floor — `>50%` wins

| Source | Says |
|---|---|
| S1 master spec §5.2 | `>=50%` |
| S1 pre-submission checklist R12 | `>50%` |
| **S2 dimension 23** | **`> 50%`** |
| S3 generator "Constraints that MUST hold" | `≥ 50%` |

**Resolution.** Grade on `>50%`. A rubric at exactly 50.0% is off band, but by
0 points, so the ±5-point rule makes it **Non-Fail (3)**, not a Fail. Do not
escalate a boundary case.

---

## 2. MUST-PASS scope — the narrow rule wins

| Source | Says |
|---|---|
| S1 master spec §5.2 | "For Must pass. Use for **file existence and file type only**. Counts and non-visual structural checks … are Format Gate, **but not Must Pass**" |
| **S2 dimension 24** | **"MUST-PASS is reserved for format-gate criteria (the file itself / correct extension). Everything else is REGULAR."** |
| S3 generator weight table | "Format Gates ≤ 20% (**MUST-PASS only**)" |

**Resolution.** Grade on the narrow rule. A page-count or slide-count gate is
`format_gate` + `REGULAR`.

**Do not penalise the contributor** when the over-broad tagging matches what the
generator produced. Record it as a tooling defect against S3.

---

## 3. Agent stump threshold — `≤80%` wins

| Source | Says |
|---|---|
| S1 master spec §7, glossary | `≤65%` (and the master spec's section is titled *Removed from Attempts*) |
| Reviewer doc §1 Overview / Golden Rule | `≤65%` |
| **Reviewer doc §3 Step 4** (stated twice) | **`≤80%`** |
| **QC Spec Doc (designated SSOT)** | **`≤80%`** |
| S3 welcome node + agent-run node | `65%` / `0.65` |

**Resolution.** `≤80%`. The 65% wording is stale everywhere it appears,
including on every surface a contributor actually sees.

**Do not grade a contributor on the agent score at all** — the agent run was
removed from the attempter flow, so any responses already in a task are old.

---

## 4. Design & Creative bands — S2 wins, but the generator cannot comply

| Source | Says |
|---|---|
| S1 master spec §5.2, **S2 dimension 23** | D&C inverts: correctness 20–30%, visual ≥50% |
| S3 generator | hardcodes correctness ≥50% / visual 20–30%, with **no domain conditional**, and is never passed the domain |

**Resolution.** Grade on S2's inverted bands for D&C tasks.

A D&C task whose weight share matches the generator's output is a **tooling
defect**, not a contributor defect. Flag it and do not fail the contributor on
`§R12` alone.

Related ambiguity: S1 §5.2's prose note says "For **Design and Multimedia**
tasks" while its own table and S2 say **Design & Creative** only. "Design &
Creative" and "Multimedia & A/V" are two distinct domains. **Treat only
`Design & Creative` as inverted** until the spec is corrected; if a
Multimedia & A/V task is borderline on `§R12`, flag rather than fail.

---

## 5. Criteria count — 10–30 wins

S3's Rubric Criteria Builder node states the count four ways at once:

```
minCriteria                     = 0
maxCriteria                     = 30
criteriaPrefiller.criteriaCount = 50
criteriaPrefiller.systemPrompt  : "Total criteria count: 10-30."
```

**Resolution.** 10–30, per S1 and **S2 dimension 25**.

Two consequences for grading. `minCriteria = 0` means a sub-10 rubric submits
cleanly, so under-count is a real and un-warned failure mode. And
`criteriaCount = 50` is the likely cause of any over-30 rubric — treat an
over-count as a **tooling defect** unless the contributor clearly added criteria
by hand.

---

## 6. Permitted expected-file formats — the 24-application list wins

| Source | Says |
|---|---|
| **S2 dimension 10 (current)** | any format the **24 named applications** can generate |
| S2 dimension 10 (older vendored copy) | "the required Office format" |
| S1 FAQ | "currently supported formats are `.docx .pptx .pdf .zip .blend .tscn .escn .tres .godot .gd .scn .res`" |
| S3 Asset Upload `allowedMimeTypes` | pptx, xlsx, doc, docx, ppt, jpeg, png, json, `.ps1`, `.sh` — **no PDF, no zip, no blend** |

**Resolution.** Grade on the 24-application list.

S3's upload widget cannot accept most permitted formats — its own instruction
text documents the workaround ("select 'all files' on your PC … and upload the
PDF"), and the workflow's sample data has PDF expected files. **Never fail a
task on `§G2` for a format the widget blocked**; the contributor had no
compliant path.

---

## 7. Minor PII — Non-Fail wins

This skill's `audit-rubric.csv` scores minor PII as
`[Non-Fail - Minor PII Violation]` at **4**. The older copy vendored at
`current_quality_evals/definitions/audit_rubric.csv` scores it
`[Fail - Minor PII Violation]` at 2.

**Resolution.** Non-Fail (4). The bundled `audit-rubric.csv` is the newer
version. Re-check any task previously failed on minor PII.

---

## 8. Atomicity — a Non-Fail band exists

The current CSV adds `[Non-Fail - Minor Atomicity Issues]` at 3 for "15% or less
of the criteria are non-atomic". The older vendored copy has a hard fail only.

**Resolution.** The Non-Fail band applies. Re-check any task previously failed
on atomicity at or under 15%.

---

## 9. "Gold file" — two referents, term deprecated

| Source | Uses "gold file" to mean |
|---|---|
| S1 master spec §1.1, glossary; **S3 `templateVariables.golden_*`** | the **pre-seeded initial output files** |
| **S2 dimensions 9–11**; S1 pre-submission checklist "GOLD FILE CHECKLIST" | the contributor's **answer key** |
| S1 FAQ | "a term that has been confusing … **we are trying to remove this term**" |

**Resolution.** Use **"expected file"** for the answer key, per the glossary.
Read S2's three "Gold File" dimensions as "Expected File". When reading L1
`metadata`, remember `golden_names` / `golden_urls` are the *initial output*
files, not the answer key.

---

## 10. Prompt-change guidance — make substantial changes

| Source | Says |
|---|---|
| S3 prompt-input node | "**PRESERVE CORE REQUESTS:** Keep the same number and type of requests as the skeleton." |
| S3 next node's model GOOD answer | "Changed target from all slides to slides 2-5. **Removed infeasible Core Request** (insert watermark)…" |
| S1 common errors #2 | "the seed prompt is **never** great … don't be afraid of drastic changes" |

**Resolution.** Substantial rewriting is expected and correct; preserve
*coverage and feasibility*, not request count. "No significant prompt changes"
is the second most common audit finding, so do not reward a conservative rewrite.

---

## 11. Orphaned generator rules — not gradable

S3's generator states two rules that appear in **no** S2 dimension and nowhere
in S1: "Each gate 5-10" (per-gate weight) and "cap at 4 gates total".

**Resolution.** Not gradable. Do not raise findings against them. Report as
informational only.

---

## 12. `criteria_category` key name

S3's generator prompt instructs the model to emit `category`; production data
uses `annotations.criteria_category`.

**Resolution.** `criteria_category` is the real key. The generator prompt's
documented schema is wrong; this is informational unless generated rubrics are
actually arriving mis-keyed.

---

## 13. The sample rubric in the taxonomy is pre-v3

`S3 templateVariables.rubric` carries 111 criteria using
`criteria_category` values of `"must have criteria"` and `"critical criteria"`,
with no `criteria_type` at all.

**Resolution.** Dead schema. Never audit it as a rubric, and never treat it as
an example of correct authoring. L1 `metadata.rubric` (the seed rubric) uses the
same dead schema.

---

## 14. Input-file rules are unenforced, not optional

S1 states ≥3 files, not-all-spreadsheets, English, CC0, <30MB. S3 enforces none
of them — `maxFileSizeKB = 1073741824` (1 TB), no minimum count, and the Initial
Files widget blocks `text/plain`, `text/markdown` and `text/csv` even though the
FAQ permits text-only inputs.

**Resolution.** S1's rules apply. But do not fail a task for a missing input
format the widget blocked, and treat an oversize input set as a finding against
the pipeline rather than the contributor.

---

## 15. Multi-OS is live but undocumented

S3 ships Windows, Ubuntu and Mac `ComputerUse` nodes, and `templateVariables`
sets `windows`/`ubuntu`/`mac` all `"true"`. **S2 dimension 10** grades per-OS
expected files ("a separate gold file per OS when applicable"). S1 describes
Ubuntu exclusively and never defines "when applicable".

**Resolution.** Treat Ubuntu-only as correct unless the task's L1 metadata
enables another OS. Never fail `§G2`'s per-OS clause on an Ubuntu-only task.
