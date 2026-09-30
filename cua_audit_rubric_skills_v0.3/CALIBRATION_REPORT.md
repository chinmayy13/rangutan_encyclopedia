# CUA audit tool — calibration report

An automated reviewer scores CUA v3 task submissions against the 28 components
of the audit rubric (this skill's `audit-rubric.csv`). This report measures it
against the human auditors who scored the same submissions.

## Method

- 27 submissions, each scored on all 28 components by its own model call
- 707 component scores compared against human audit records pulled from Snowflake
- FAIL = score 1 or 2. PASS = score 3, 4 or 5. Agreement measured on that binary
- The audit rubric CSV is the only authority. Component definitions are generated
  from it verbatim, so there is no paraphrase layer that can drift

## Outcome

| Scope | | Agreed fails | False positives | Missed fails | Precision | Recall |
|---|---|---:|---:|---:|---:|---:|
| All 28 components | before | 14 | 31 | 58 | 0.31 | 0.19 |
| All 28 components | after | 15 | 20 | 57 | 0.43 | 0.21 |
| The 11 revised components | before | 11 | 18 | 30 | 0.38 | 0.27 |
| The 11 revised components | after | 12 | 7 | 29 | 0.63 | 0.29 |

Precision rose from 0.31 to 0.43 overall, and from 0.38 to 0.63 on the components
that were revised. False positives fell from 31 to 20. Recall did not move: 57
missed fails against 58 before.

## What the revisions changed

Eleven components were revised after a root-cause review of 89 disagreements.
Five mechanisms were identified and corrected:

| Component | Change | Effect |
|---|---|---|
| Prompt - Realism | Stop treating prompt wording that matches criterion wording as evidence the prompt leaks the verifier. The rubric is written from the prompt, so overlap is expected. | 12 scores changed, mostly off the fail band. Largest single source of false positives removed. |
| Rubric - Coverage | Given the expected and input files, which it previously never saw, and required to construct the specific wrong submission that passes every criterion while omitting each request. | Now detects gaps it previously reported as fully covered. |
| Rubric - Self-Containment | "The expected file" is not an anchor by name. Where a task ships more than one expected file, a generic reference is not gradable. | 4 scores changed. |
| Rubric - Robustness | A legibility guard only counts when it sits in the same criterion as the mechanical check. | 5 scores changed. |
| Rubric - Value Binding | Naming a value and a label in one sentence does not bind them. | 3 scores changed. |
| Gold File - Format | Tool defect: a shared instruction block let this component fail a submission for a reason its own answer options do not name. | 2 false fails cleared. |

## Where it still misses

Recall is 0.21. The revisions fixed detection without fixing severity: roughly
20 scores moved from 5 to 3, meaning the defect is now found but banded as a
non-fail where the human recorded a fail.

The cause is the form's own thresholds. Six components define their fail
condition as a share of the criteria, typically 15%. On a 20 to 30 criterion
rubric that requires 3 to 5 flagged criteria, so one to four real defects land
in the non-fail band by arithmetic. Human auditors do not compute a share; they
fail on the existence of a defect that would change a grading outcome. In two
cases the tool flagged the identical criteria as the human, computed the same
percentage, and scored 3 against their 2.

Closing that gap means scoring against observed practice rather than the form as
written. That is a decision for the form's owner and has not been made.

## Two findings about the comparison itself

Of the 89 disagreements examined, 26 are not tool errors:

- **12 are spec divergence.** The human scored against a rule the CSV contradicts
  in writing. All four Weight Share disagreements are of this kind: one reads the
  correctness rule as a floor on each criterion rather than the category share,
  another invents a minimum weight for format gates where the CSV sets only a
  ceiling. Two PII disagreements fail on a document author name, which the CSV
  explicitly permits, metadata included. Two JSON disagreements fail on the
  verifier score, which the CSV says QC does not check.
- **14 are correct findings the human did not record.** An auditor records the
  labels that drove their score, not every issue present. Five of the 14 were
  recorded by the same auditor under a different component on the same
  submission, so the observation was agreed and only the filing differed.

Both inflate the apparent error rate. The measured numbers understate the tool.

## Per-component detail

| # | Component | Scored | Missed (before → after) | False pos. (before → after) | Revised |
|---|---|---:|---:|---:|:-:|
| 04 | Prompt - Realism | 27 | 1 → 1 | 8 → 2 | yes |
| 15 | Rubric - Accuracy | 27 | 3 → 3 | 6 → 3 | yes |
| 16 | Rubric - Coverage | 27 | 9 → 9 | 0 → 0 | yes |
| 09 | Gold File - Accuracy | 27 | 5 → 5 | 1 → 1 | yes |
| 02 | Task - PII / Safety | 27 | 3 → 3 | 0 → 0 | yes |
| 17 | Rubric - Self-Containment | 27 | 3 → 2 | 0 → 0 | yes |
| 26 | Component: Rubric - Robustness | 19 | 3 → 3 | 0 → 0 | yes |
| 10 | Gold File - Format | 27 | 0 → 0 | 2 → 0 | yes |
| 11 | Component: Gold File - Input Consistency | 19 | 1 → 1 | 1 → 1 | yes |
| 08 | Component: Prompt - Answer leakage | 19 | 1 → 1 | 0 → 0 | yes |
| 27 | Component: Rubric - Value Binding | 19 | 1 → 1 | 0 → 0 | yes |
| 01 | Task - Feasibility | 27 | 0 → 0 | 0 → 0 |  |
| 03 | Prompt - Clarity | 27 | 0 → 1 | 0 → 1 |  |
| 05 | Prompt - GUI Integration | 27 | 0 → 0 | 0 → 4 |  |
| 06 | Prompt - Output Naming | 27 | 0 → 0 | 0 → 0 |  |
| 07 | Prompt - Timelessness | 27 | 0 → 1 | 0 → 0 |  |
| 12 | Rubric - Categorization | 27 | 0 → 3 | 0 → 0 |  |
| 13 | Rubric - Hardcoded Values | 27 | 0 → 0 | 0 → 0 |  |
| 14 | Rubric - Content | 16 | 0 → 1 | 0 → 0 |  |
| 18 | Rubric - Overfitting | 27 | 0 → 7 | 0 → 4 |  |
| 19 | Rubric - Atomicity | 27 | 0 → 3 | 0 → 1 |  |
| 20 | Rubric - Objectivity | 27 | 0 → 0 | 0 → 0 |  |
| 21 | Rubric - Framing | 27 | 0 → 2 | 0 → 1 |  |
| 22 | Rubric - Redundancy | 27 | 0 → 2 | 0 → 2 |  |
| 23 | Rubric - Weight Share | 27 | 0 → 4 | 0 → 0 |  |
| 24 | Rubric - Individual Criteria Weights | 21 | 0 → 0 | 0 → 0 |  |
| 25 | Rubric - Count | 27 | 0 → 0 | 0 → 0 |  |
| 28 | JSON - Structure / URL Integrity | 27 | 0 → 4 | 0 → 0 |  |

Seven components have no human fail examples anywhere in the project, so recall
cannot be measured on them: Feasibility, Output Naming, Gold File Format,
Hardcoded Values, Objectivity, Individual Criteria Weights, Count.

## Caveats

- 27 submissions and 72 human-recorded fails is a small sample. Per-component
  figures rest on 1 to 10 examples each and should not be read as stable.
- The comparison ground truth has not been re-adjudicated for the 26 records
  above. Doing so would raise both measured figures.
- The tool reads a JSON bundle plus text extractions of the input and expected
  files. It does not have the VM, the rendered artifacts, or the platform UI.
  Some human findings are not reachable from its evidence; expiring URLs are one
  confirmed case, since the bundle builder strips the tokens upstream.