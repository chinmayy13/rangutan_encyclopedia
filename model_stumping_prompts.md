# CUA V3 · Model-Stumping Quick Reference

*Internal · for CB reference*
*QUALITY MANAGEMENT · AUGUST 2026 · 7-PAGE VERSION*

What makes a CUA task stump the model — the part that holds across domains, then the part that does not. Worked prompts for all twelve domains are in the appendix. The full 18-page playbook has the evidence behind each pattern.

---

## APPLIES TO EVERY DOMAIN

### Six things that hold everywhere

These are the patterns that showed up across all twelve domains, and the ones worth getting right before anything domain-specific.

- **An early judgment has to control everything after it.** Length is not the variable. A long task whose steps are independent is easy; a short task where one interpretation feeds every later number is hard. Build the task the way the profession works, so that getting the first call wrong naturally corrupts the rest.
- **The conflict belongs in the files, not the prompt.** The strongest tasks supply documents that disagree — on a figure, a date, a definition — and a rule for which one wins. Weak tasks are rarely weak because of phrasing. They are weak because there is no tension in the source material and the agent can fall back on straightforward data processing.
- **Leave the thresholds in the source.** If you write the qualifying criteria, bands or deadline windows into the request, you have removed the only judgment call. A brokerage compliance audit with every ingredient of a hard task scored 96% for exactly this reason.
- **Run the task yourself before you write the rubric.** If an intermediate result comes out zero, comes out identical across scenarios, or can be derived without the earlier stages, the dependency is decorative. An embankment task scored 83% because its settlement variance came out to zero and there was nothing left to get wrong.
- **Make the model look at what it produced.** Reading information off a source image, matching a supplied reference, and inspecting a rendered result are consistently the hardest steps. Asking for a screenshot of a page the agent just built is not one of them.
- **Three or four levers is enough.** Nine is dense, not hard. Pick the ones the workflow genuinely calls for.

### Visual and GUI work, specifically

The most under-used source of difficulty in the sample, and usually the hardest part for the model.

- **An image template beats a Word template.** A .docx template will usually be filled in with the layout preserved. Supply the same thing as a .png or a tightly formatted PDF and it becomes far harder. Works for compliance spreadsheet layouts, accident-report sketches, chart skeletons whose axis titles and legend must be retained.
- **Prefer "match the supplied reference" over a pixel count.** Exact match to a supplied mockup is the strongest form of the lever. Naming precise pixel dimensions is weaker — it is only sometimes natural for a developer to work that way, and attempters copying the pattern will use it where it does not fit.
- **Make the visual check an acceptance criterion.** Overlapping labels, bars running off the plot area, clipped columns, text outside safe areas and split rows count as failures even when the numbers are right.

### A caveat on what this data can tell you

- Some of these patterns describe what is easy to grade, not what is hard to do. Deterministic item-level outputs score cleanly with a rubric, so they read as stumping. Interpretive outputs allow semantic equivalence and are hard to score, so they read as non-stumping. Part of the observed gap is a measurement artifact.
- Watch for the same idea on both sides. "Governance framework" as a stumping trait and "rule hierarchies" as a non-stumping one are the same mechanism phrased twice. Where a contrast reads as a near-mirror of itself, lean on the source-material guidance instead.
- A high score does not always mean the task was easy. Some complex tasks score high because the verifier cannot compare two long texts and decide whether they mean the same thing.

---

## The four levers that carry most of the weight

Every worked prompt in the appendix is marked with these letters. The right-hand column counts how many of the twelve domains the lever applies to.

| Lever | What you write into the prompt | The failure it triggers | Seen in |
|---|---|---|---|
| **A** Source precedence | Name which document controls when two sources disagree, and make them actually disagree. | Averages the sources, or silently picks the more prominent one. | 11 of 12 |
| **B** Item-level work before totals | Every record matched, classified or dispositioned before any aggregate is computed. | Jumps to the summary and back-fills, so exceptions never get applied. | 9 of 12 |
| **F** Rendered format gate | Page limits, chart legibility, no overlapping labels, no clipped rows — checked after rendering. | Produces valid content inside an unusable artifact and never looks at it. | 12 of 12 |
| **H** Cross-artifact reconciliation | The same totals, counts and dates must agree across the workbook, the memo and the deck. | Recomputes per artifact, so the three deliverables disagree with each other. | 12 of 12 |

### And five to reach for when the workflow calls for them

| Lever | What you write into the prompt | The failure it triggers | Seen in |
|---|---|---|---|
| **C** Thresholds live in the source | Qualifying criteria, bands and deadline windows sit in the manual or spec, not in the prompt. | Uses conventional industry defaults instead of the ones in your file. | 7 of 12 |
| **D** Convention-bound calculation | Specify the counting rule: banking days, business days, measurement period, rounding, cut-off. | Uses calendar days or its own rounding, so every derived figure drifts. | 6 of 12 |
| **E** Exclusion rule | A named status keeps records out of the financial or operational totals. | Includes the excluded rows, inflating every downstream number. | 8 of 12 |
| **I** Stop rule | If the source does not resolve a case, list it separately and keep it out of the totals. | Guesses to complete the table rather than declaring the gap. | 7 of 12 |
| **G** Fixed-count traceable findings | Exactly three findings or actions, each tied to a specific figure, with an owner and a date. | Writes generic recommendations not anchored to any computed value. | 3 of 12 |

*Three or four levers is enough. Nine is dense, not hard.*

---

## DOES NOT GENERALIZE

### What is different about each domain

Everything above applies here too. These are only the things that do not carry over — the specific move that makes a task hard in that profession. Four domains have no stumping examples in the data; their entries are labeled and should be treated as hypotheses.

### 1. Finance & Accounting
**High — 34 vs. 46**

- A gating waterfall: do not proceed to a later covenant or accounting test unless an earlier condition is satisfied by permitted evidence.
- Figures must be derived, not copied — standalone-quarter values pulled out of year-to-date disclosures, pro forma ratios, capacity tests.
- Every material number traceable to a table, line item, clause or definition.

**Levers:** A D F H I

*Not hard here.* Trend summaries, margin analysis and growth comparisons where the method is already obvious, and formatting that is not tied to an eligibility determination.

### 2. Software & Data
**High — 53 vs. 74**

- Functional and visual correctness at once. Correct code alone is not sufficient.
- Edits inside an existing repository, with protected behavior that must not regress.
- Actual execution: run the tests, build, then compare the rendered interface against the supplied mockups and fix the differences.

**Levers:** A E F

*Not hard here.* One script correction or data transformation, validated by output values rather than UI fidelity. Asking for a screenshot of the page just built.

### 3. STEM Research
**High — 55 vs. 61**

- Classification that cannot be resolved by picking the best number — physical admissibility and uncertainty conditions come first.
- Sources that disagree: use the uncertainties from one file, the parameter definitions from another.
- Conclusions demonstrated by the data kept separate from mechanisms that are only plausible.

**Levers:** A B C D F H I

*Not hard here.* Standard analysis with a known formula or statistical test, and descriptive interpretation of trends. Prompt length here is high on both sides.

### 4. Engineering
**Strong pattern, small set — 27 vs. 5**

- An approved spec supplies the formulas, status bands, rounding and corrective-action triggers, by section number.
- Per machine, per shift, per supplier — not overall averages. Many independently checkable results.
- Raw measurement → metric → normalized deviation and status → dominant failure mode → corrective action.

**Levers:** A B C D E F G H

*Not hard here.* A clean regression, fluid or thermal model with few policy or status layers stacked after the computation.

### 5. Healthcare
**Medium — 14 vs. 7**

- One row per unit, exhaustively — every date in the season, every trial, every record — even when nothing escalates.
- The approved internal protocol controls; external guidance is context and must not override it.
- Privacy constraints: IDs only, no PHI, or reasoning restricted to schema level.

**Levers:** A B C F H I

*Not hard here.* Interpreting a case or summarizing quality metrics, where several readings are defensible and no traceable classification ledger is required.

*"Governance framework" on the stumping side and "rule hierarchies" on the non-stumping side are the same thing. Trust the source documents here, not the contrast.*

### 6. Legal & Compliance
**Medium — 9 vs. 7**

- Chronology is substantive: attachment, commencement, filing or notice dates decide priority.
- Apply the provision to facts. Asking for excerpts or citations involves no legal reasoning and will not stump the model.
- Supply the template as an image. A .docx template gets filled in without trouble; a .png does not.

**Levers:** A B D H I

*Not hard here.* Auditing against a clear checklist or finalizing a redline. A .docx template to fill in. Extracting clauses without applying them.

Put the enactment or effective date inside the input file, and state the date on which the request is being made inside the prompt, or QC will flag the task as time sensitive. Example: the prompt says the current date is March 2025; the input file is a law enacted March 2024 waiving certain requirements for two years. In that task universe the model should conclude the requirements are waived, and the answer does not change with the calendar.

### 7. Operations & Management
**Small sample, consistent — 4 vs. 16**

- Status first, work second. The agent classifies something, and that classification determines what it is allowed to do next.
- Operational numbers become money or dates — a staffing, replacement or procurement figure.
- A short management artifact plus the detailed backup it must be traceable to.

**Levers:** All nine

*Not hard here.* One review reported section by section, with deliverables that sit side by side rather than as stages of one calculation. These prompts are often the longest.

Two failures seen here: a dependency chain whose intermediate result came out zero and voided the deliverable, and a board review asking for "important trends" and "areas needing attention" while giving two layout rules that could not both be satisfied.

### 8. Government & Public Sector
**Low confidence, small set — 4 vs. 8**

- Suppressed values are not zero. Complete ranking and subgroup analysis must respect them.
- Subgroup behavior may contradict the headline, and the model has to notice.
- Official methodology defines population, geographic scope and comparability.

**Levers:** A F

*Not hard here.* Straightforward aggregation, ranked lists or source-by-source synthesis off a public dataset, with recommendations not tied to specific figures.

### 9. Sales & Marketing
**Extrapolated — no examples — 0 vs. 25**

- Every transaction, account or campaign classified under a controlling policy, with no skipped records.
- A memo or playbook may only make the corporate rule stricter, never relax it.
- Compliance status drives revenue at risk, which drives the manager action.

**Levers:** A B C E F H I

*Not hard here.* A standard policy audit, refund analysis or demand trend run off one dataset, with the recommendation generated straight from the aggregate.

### 10. Multimedia & A/V
**Extrapolated — no examples — 0 vs. 17**

- Scored editorial inclusion, with time-window or value-based exceptions that override the score.
- Timing arithmetic: segment durations must sum to an exact runtime after open, close and transitions.
- The same names, numbers and ordering across ledger, rundown, script and graphics brief.

**Levers:** B C D E F H

*Not hard here.* A ranked story list, memo and deck that are parallel views of the same findings, with no cascading runtime or asset dependency.

### 11. Design & Creative
**Illustrative only — no data**

- Layouts that adapt across sizes rather than scale, so variants must stay consistent without being identical.
- Objective visual QA: contrast thresholds, exact dimensions, bleed, no clipping, verified on the exported files.
- Stated precedence when the mockup, the brand guide and the accessibility rule conflict.

**Levers:** A B C F H

*Not hard here.* One canvas size, one artifact, judged on overall visual quality rather than exact reproduction against a reference.

### 12. Real Estate
**Observed, not validated — L1 pipeline**

- Tenant-level reconciliation before any property-level metric. Every suite first, then occupancy, NOI, rollover, valuation.
- Contractual facts kept separate from analyst assumptions — no filling in missing lease terms.
- One misread lease expiry moves the rollover schedule, the NOI and the cap-rate value.

**Levers:** All nine

*Not hard here.* File-by-file summaries off clean data, with the thresholds handed over in the prompt. Often the longest prompts in the domain.

Three failures seen here: overlapping geography tiers with no rule for which to use, a source image described as something it was not, and a compliance audit that gave away its thresholds and scored 96%.

---

## What does not stump the model

- ✗ Length on its own. Several of the longest prompts in the sample are among the easiest.
- ✗ Asking for a screenshot of a page the agent just built or fixed.
- ✗ Extracting sections, clauses or citations from a law. There is no legal reasoning in retrieval.
- ✗ Filling in a Word template while preserving its layout.
- ✗ Ten unrelated things in one prompt. Unrelated is not the same as dependent.
- ✗ Handing over the qualifying thresholds when they could have stayed in the source.
- ✗ Broad prose asks such as "important trends" or "areas needing attention". Not scoreable.
- ✗ Contradictory format instructions that are not the point of the task.

---

## Before you submit

| Check | Detail |
|---|---|
| Is there a real conflict in the source files? | Two documents disagreeing on a figure, a date or a definition, with a stated rule for which wins. |
| Are the thresholds in the source rather than the prompt? | If you wrote the criteria into the request, you removed the judgment call. |
| Did you run the task end to end yourself? | Check that no intermediate result comes out zero, identical across scenarios, or derivable without the earlier stages. |
| Does a wrong early call actually break something later? | If the later steps still produce a defensible answer, the dependency is decorative. |
| Is there a genuine exception or stop rule? | More diagnostic than adding prose. Include an instruction to list unresolvable cases rather than guess. |
| Do at least two outputs have to reconcile? | Workbook and memo, data table and deck, code and test report — where the profession would expect it. |
| Is there a meaningful visual or GUI requirement? | Reading a source image, matching a reference, or inspecting and correcting a rendered result. |
| Is every requirement scoreable, and non-contradictory? | Remove "important trends" and check that no two format instructions conflict. |
| Are the dates anchored? | Effective date in the file, request date in the prompt. |
| Have you kept it to three or four levers? | Nine is dense, not hard. |

**Method note.** Drawn from a comparative analysis of model-stumping and non-stumping CUA tasks across three supplied CSVs, plus Real Estate tasks reviewed in the L1 pipeline, revised with review comments from the domain QM teams. No single feature causes model failure on its own; the signal is the interaction of constraints within a task. Four domains have no stumping examples in the data and are labeled accordingly.

---

## APPENDIX

### Worked prompts, one per domain

Marker letters map to the lever tables. Domains 9 to 12 have no stumping examples in the data, so those prompts are proposals to test rather than validated patterns.

---

#### 1. Finance & Accounting — Example stumping prompt

You are preparing the quarter-end financing review for a fictional manufacturer. Use Q2_2026_10Q.pdf, Credit_Agreement_Excerpt.pdf, and Covenant_Calculation_Workbook.xlsx. The agreement excerpt is the controlling source for definitions and permitted-payment tests. If a management metric conflicts with an agreement-defined metric, use the agreement definition and document the difference. **[A]**

Determine whether the $42.6 million shareholder distribution disclosed for the six months ended June 30, 2026 is supportable under the permitted-payment waterfall. Test Clause 6.04(c) first. If the permitted capacity cannot be independently established from the supplied evidence, stop the substantive eligibility analysis there and do not calculate later baskets. **[I]** Only if the payment clears that gate, calculate the agreement-defined leverage test under Clause 6.04(f), pro forma for the distribution, using the most recently ended measurement period. **[D]** Do not reverse-engineer missing inputs or treat liquidity commentary, board authorization, or management-adjusted leverage as proof of compliance.

Create Distribution_Analysis.docx, Distribution_Calculation.xlsx, and Distribution_Trace_Register.csv. The memo must state the earliest binding stop point, the workbook must contain only tests the analysis legitimately reached, and the trace register must identify the source location for every number used. The amount, classification, leverage result, and conclusion must agree across all three files. **[H]** Open the memo and workbook before finishing and correct any clipped tables, broken number formats, or inconsistent values. **[F]**

**Levers:** [A] Source precedence · [D] Convention-bound calculation · [F] Rendered format gate · [H] Cross-artifact reconciliation · [I] Stop rule

---

#### 2. Software & Data — Example stumping prompt

The starter Vue project is in support_console.zip. desktop_mockup.png and tablet_mockup.png show the required page at desktop and tablet widths. interaction_spec.pdf defines button states, keyboard behavior, validation rules, and animation timing. known_exceptions.csv lists the only approved deviations from the spec. **[A]**

Implement the page inside the existing project. Keep each major section as its own component under src/components, and do not replace the routing or state-management setup already in the repository. Every visible label must match the mockups exactly. Apply the interaction rules from the specification, including disabled, loading, error, and success states; when a case appears in known_exceptions.csv, follow that exception and no others. **[E]**

Run the provided test suite and fix all failures. Then open the app in a browser at the two widths shown in the mockups and compare it with the supplied files. **[F]** Correct obvious differences in spacing, alignment, text wrapping, element dimensions, and responsive behavior; there must be no horizontal overflow. Save the finished project as support_console_final.zip without node_modules, and create verification_results.pdf listing each test scenario, expected result, actual result, and pass/fail status. The PDF must include a pass/fail summary and render without clipped rows or overlapping chart labels. **[F]**

**Levers:** [A] Source precedence · [E] Exclusion rule · [F] Rendered format gate

---

#### 3. STEM Research — Example stumping prompt

Use orbital_measurements.csv, compact_object_reference.docx, and classification_rules.pdf to classify the six priority compact-object candidates. Work in natural units and use the mass in the CSV as fixed. The reference appendix and CSV disagree on several measurement uncertainties; use the CSV uncertainties as final while using the reference document for the equations and parameter definitions. **[A]**

For each object, apply the classification rules in order. **[B]** Do not select a class solely because it has the lowest chi-squared value: first check the physical admissibility and uncertainty conditions stated in the rules. **[C]** Once the class is fixed, calculate the required derived quantities, including the normalized spin or charge parameter, horizon radius where applicable, temperature/entropy quantities, and the orbital-frequency residual relative to the measured value. **[D]** Flag any object whose absolute residual exceeds 5%. If a quantity does not apply to the selected class, enter 0 rather than inventing an estimate. **[I]**

Create classification_results.csv, classification_report.docx, and collaboration_summary.pptx. Use the same object order in all three files, and make every classification, parameter, residual, and flag agree exactly. **[H]** The deck must distinguish conclusions demonstrated by the supplied measurements from physical explanations that are only hypotheses. Open the report and presentation and fix any clipped equations, unreadable figure labels, or inconsistent numbers before saving. **[F]**

**Levers:** [A] Source precedence · [B] Item-level work before totals · [C] Thresholds live in the source · [D] Convention-bound calculation · [F] Rendered format gate · [H] Cross-artifact reconciliation · [I] Stop rule

---

#### 4. Engineering — Example stumping prompt

The October injection-molding review uses shot_logs.zip, process_spec.pdf, and maintenance_events.xlsx. The process specification is the governing source for acceptance limits, Cpk formulas, fail-rate rounding, status bands, and corrective-action triggers. **[A][C]** The ZIP contains one CSV for each of four machines and includes DAY and NIGHT shift records.

For every machine and shift, calculate fail rate and Cpk for all three critical dimensions using only that shift's accepted measurement rows and the formulas in Section 5. **[B][D]** Then calculate each machine's monthly status using Section 7.1. For machines at Caution or worse, identify the shift with the higher fail rate and the dominant KPI using the Appendix A normalized-deviation method. Do not choose the dominant KPI from raw magnitude alone. Use Section 11 to count only qualifying corrective maintenance events from the most recent 60 days. **[E]**

Create oct_quality_review.pptx, oct_machine_metrics.csv, and a one-page corrective_action_memo.docx. The deck must contain the monthly table, per-shift table, grouped fail-rate chart, and failure-mode summary. The memo must cover only machines whose computed status triggers action. **[G]** All metric values and status labels must match across the three files. **[H]** Open the deck and memo before finishing; fix cut-off columns, overlapping labels, row splits, or unit/rounding inconsistencies. **[F]**

**Levers:** [A] Source precedence · [B] Item-level work before totals · [C] Thresholds live in the source · [D] Convention-bound calculation · [E] Exclusion rule · [F] Rendered format gate · [G] Fixed-count traceable findings · [H] Cross-artifact reconciliation

---

#### 5. Healthcare — Example stumping prompt

Riverbend Medical Center is preparing its summer heat-readiness review. Use heat_log_2026.csv, activation_protocol.pdf, and federal_heat_guidance.pdf. The hospital protocol is already approved and is the controlling source for activation levels; the federal guidance is context only and must not override the hospital thresholds. **[A][C]**

For every date in the declared heat season, classify the day into the protocol's activation level using the recorded measurements and the exact threshold/exception rules. Create one row per date even when no escalation occurs. **[B]** If a measurement is missing, apply only the protocol's stated missing-data rule and flag the row; do not infer a value. **[I]** Then summarize the number of days in each level, longest consecutive escalation period, dates that crossed into the highest level, and the operational actions that the protocol requires for those dates.

Save heat_activation_daily.csv, summer_heat_board_brief.docx, and summer_heat_summary.pptx. The daily CSV is the source of truth for all counts in the brief and deck. **[H]** Do not include patient names or other PHI. The brief must distinguish actions required by the hospital protocol from optional practices mentioned only in the federal guidance. Open the Word document and presentation and correct any table overflow, unreadable chart labels, or mismatched counts before finishing. **[F]**

**Levers:** [A] Source precedence · [B] Item-level work before totals · [C] Thresholds live in the source · [F] Rendered format gate · [H] Cross-artifact reconciliation · [I] Stop rule

---

#### 6. Legal & Compliance — Example stumping prompt

A fictional company is in liquidation. Use claims_register.xlsx, Insolvency_Code.pdf, Tax_Act.pdf, and property_attachment_log.csv. The insolvency statute controls the distribution waterfall. Use the tax statute only to determine the legal character and timing of the tax authority's claims; do not assume that a tax lien automatically outranks the insolvency waterfall. **[A]** The commencement date is 20 February 2026. **[D]**

For every tax attachment in the log, determine whether it occurred before or after commencement and identify the insolvency provision that controls its treatment. **[B]** Then place each creditor class from the claims register into the statutory waterfall. Where priority depends on a fact that is not established by the supplied record, state that the priority cannot be independently concluded and do not fill the gap with an assumption. **[I]** Cite the controlling section for each material conclusion.

Complete Priority_Memo_Template.docx without changing its section order or color scheme, and also create distribution_priority_register.xlsx. The memo must explain the chronology, treatment of the tax authority, and final ranking; the workbook must list each claim, amount, class, relevant date, statutory basis, and priority position. The claim amounts and ranking must agree between the files. **[H]** Add a final unresolved-evidence section only if the supplied record leaves a legal condition open.

**Levers:** [A] Source precedence · [B] Item-level work before totals · [D] Convention-bound calculation · [H] Cross-artifact reconciliation · [I] Stop rule

---

#### 7. Operations & Management — Annotated example prompt

We're six weeks out from the recall response, and I need the numbers pinned down before Thursday's leadership sync.

Everything you need is on the Desktop. The lot-level data is in affected_inventory.csv, supplier windows in supplier_lead_times.xlsx, and unit pricing in replacement_costs.xlsx. The recall_policy.pdf is what governs disposition and escalation, so treat it as the final word. If the lead time file suggests a delivery window that contradicts the policy, go with the policy. **[A]**

Start by working through every lot and assigning it a disposition per the policy, making sure you apply the lot and date exceptions in Section 4 before you land on a final status. **[B]** Only lots that end up as Recall or Hold-for-Review are replaceable at all. Once that's settled, take the lots that reach replaceable status and work out units needing replacement by site, the earliest realistic replenishment date off the supplier windows (business days only please), **[C]** and the direct replacement cost.

From there I need to know whether any site drops below the four-week safety-stock floor before its replenishment lands. For the ones that do, tell me the transfer quantity and cost needed to get them back over the floor, though nothing above 500 units in a single move — anything larger needs to come to me first. **[D]** Anything still sitting in Hold-for-Review stays out of replacement and transfer cost totals. **[E]**

Save the model as recall_response_model.xlsx and the writeup as leadership_action_memo.docx, both on the Desktop. Build the coverage-by-site comparison as a chart in the workbook, then drop a picture of it into the memo under the actions **[F]** — leadership won't open the spreadsheet, so whatever's in the memo has to stand on its own. Size it to the page width and make sure both series are actually visible in the shot, **[F]** the last version we sent had the post-transfer bars running off the top of the plot area. The memo should land on three actions, each tied back to a figure in the workbook, with an owner and a deadline, **[G]** and the whole thing needs to fit on two pages. **[F]** Site totals, dates and costs need to match between the two files. **[H]**

If the policy just doesn't resolve a lot cleanly, park it in its own list and keep it out of the financial totals rather than guessing. **[I]**

**Levers:** [A] Source precedence · [B] Item-level work before totals · [C] Thresholds live in the source · [D] Convention-bound calculation · [E] Exclusion rule · [F] Rendered format gate · [G] Fixed-count traceable findings · [H] Cross-artifact reconciliation · [I] Stop rule

---

#### 8. Government & Public Sector — Example stumping prompt

Prepare an overview on the electrification of cars, from the perspective of labor and power grid impact: the workforce impact and effects on the power grid that would be experienced if America were to match China in terms of sales of new EVs by market share.

Use transition to electric vehicles.pdf, Effects of Electric Vehicles on Power Networks.pdf, and GlobalEVOutlook2026.pdf to prepare a presentation deck containing bar charts that present the labor scenario from the perspective of design and development, manufacturing, and charging infrastructure. Where the three sources disagree on a projection, the GlobalEVOutlook figures control and the difference must be noted on the slide. **[A]**

For the power grid impact, present the grid's sensitivity to the additional load as a grounded illustration rather than a precise model. Use template_labor_impact.png when developing the bar charts: retain the axis title and legend exactly as shown, and populate all other aspects with the respective content. **[F]** Before finalizing, make sure everything in the deck is legible at presentation scale in a small meeting room and nothing is truncated or clipped. **[F]** Save the finalized deck as Matching_China_EV_Electrification_Costs.pptx to the Desktop.

**Levers:** [A] Source precedence · [F] Rendered format gate

---

#### 9. Sales & Marketing — Proposed stumping prompt (untested)

A national retailer is reviewing unusual return activity before the holiday campaign. Use returns_transactions.csv, Corporate_Return_Policy.pdf, Brand_Exception_Memo.docx, and store_roster.xlsx. The corporate return policy is controlling whenever the brand memo would relax a requirement; the brand memo may only add stricter rules. **[A]**

Audit every transaction. For each one, determine whether it is Compliant, Non-Compliant, or Requires Escalation and cite the specific policy rule. **[B]** Apply the high-value-customer exception only when all conditions in Section 6 are met. **[E]** Then calculate, by store and employee, non-compliant transaction count, affected sales value, escalation count, and repeat-offender status using the threshold in Section 8. **[C]** An employee may be placed on the coaching list only if the transaction-level audit supports the threshold; do not infer intent from the transaction notes. **[I]**

Create returns_audit.xlsx, manager_action_plan.docx, and executive_summary.pptx. The action plan must include only employees and stores that meet the policy-defined trigger, and every count and dollar value must reconcile to the audit workbook. **[H]** The deck must show the top compliance risks without exposing individual customer names. Open the deck and workbook and correct any cut-off labels, unreadable charts, or inconsistent totals. **[F]**

**Levers:** [A] Source precedence · [B] Item-level work before totals · [C] Thresholds live in the source · [E] Exclusion rule · [F] Rendered format gate · [H] Cross-artifact reconciliation · [I] Stop rule

---

#### 10. Multimedia & A/V — Proposed stumping prompt (untested)

You are producing a 4:00 evening-news segment on port disruptions. Use port_intelligence.pdf, active_manifest.csv, editorial_scoring_guide.pdf, and graphics_style_guide.pdf. Score every disruption using the five-level framework in the editorial guide. **[C]** Feature only shipments arriving within seven days of the intelligence report date that face a Level 4 or 5 disruption, except that cargo valued at $5 million or more must also be included at Level 3. **[E]** Do not upgrade a disruption based on dramatic wording alone.

Create a research ledger listing every candidate shipment, score, source evidence, arrival date, cargo value, inclusion decision, and reason. **[B]** From the included set, build a rundown whose total on-air time is exactly 4:00 including a 0:12 open and 0:08 close. **[D]** Then write the anchor script and a graphics brief with one lower-third and one data graphic per featured shipment. All vessel names, ports, dates, values, scores, and ordering must match the ledger and rundown. **[H]**

Save segment_research.xlsx, shipping_rundown.docx, anchor_script.docx, and graphics_brief.pptx. Keep verified facts distinct from editorial framing. Open the deck and documents before finishing and correct any text outside safe areas, clipped graphics, or runtime totals that do not equal exactly 4:00. **[F]**

**Levers:** [B] Item-level work before totals · [C] Thresholds live in the source · [D] Convention-bound calculation · [E] Exclusion rule · [F] Rendered format gate · [H] Cross-artifact reconciliation

---

#### 11. Design & Creative — Proposed stumping prompt (untested)

Create a launch campaign from brand_guide.pdf, desktop_key_visual.png, campaign_copy.docx, and approved_assets.zip. The brand guide controls logo clear space, color use, typography, and accessibility. The key visual controls composition and relative spacing. If the reference visual conflicts with an accessibility requirement, preserve the composition as closely as possible but satisfy the accessibility rule and document the deviation. **[A]**

Produce a presentation hero, a social post, and a story variant at the sizes given in the brand guide. **[C]** All three must use the exact approved campaign copy, logo, product image, and legal line. Adapt the layout for each aspect ratio without stretching assets. **[B]** Maintain the same visual hierarchy, preserve logo clear space, keep required text inside safe areas, and ensure text/background contrast meets the brand guide.

Save an editable source file plus campaign_16x9.png, campaign_4x5.png, and campaign_9x16.png. Inspect each export at full size and correct clipping, unintended text reflow, inconsistent copy, incorrect dimensions, or asset distortion. **[F]** Include a short design_QA.docx listing dimensions, contrast checks, and any justified deviation from the reference visual. **[H]**

**Levers:** [A] Source precedence · [B] Item-level work before totals · [C] Thresholds live in the source · [F] Rendered format gate · [H] Cross-artifact reconciliation

---

#### 12. Real Estate — Annotated example prompt

Compliance is reviewing Q3 before the broker sign-off next Friday and I need the escrow exposure nailed down.

Everything's on the Desktop. Closed transactions are in mls_transactions.csv, the escrow side in escrow_ledger.xlsx, and compliance_manual.pdf is the policy. The manual sets the qualifying thresholds and the deadline windows, so pull them from there rather than assuming the usual ones. **[C]** Where the ledger and the MLS feed disagree on a closing amount or date, the ledger controls — it's the funded record. **[A]**

Match every closed transaction to its escrow record before you calculate anything. **[B]** Then work out earnest money held, commission earned and days-to-disbursement per transaction, counting banking days from the recorded closing date as the manual defines it. **[D]** Anything flagged Under Review in the ledger stays out of the exposure totals. **[E]**

Save the model as Q3_escrow_exposure.xlsx, the writeup as Broker_Notice.docx and the deck as Q3_Brokerage_Audit.pptx, all on the Desktop. Build the disbursement-aging chart in the workbook, then put it on the exposure slide — the broker works off the deck, so it has to read on its own. Keep it clear of the title placeholder and check the bucket labels aren't stacked on each other, the last one we sent had them overlapping and it went out like that. **[F]** The notice should land on three findings, each tied to a transaction in the workbook, with an owner and a cure date. **[G]** Exposure totals, transaction counts and dates need to match across all three files. **[H]**

If a transaction can't be matched to an escrow record, or the manual doesn't cleanly cover it, list it separately and keep it out of the totals rather than guessing. **[I]**

**Levers:** [A] Source precedence · [B] Item-level work before totals · [C] Thresholds live in the source · [D] Convention-bound calculation · [E] Exclusion rule · [F] Rendered format gate · [G] Fixed-count traceable findings · [H] Cross-artifact reconciliation · [I] Stop rule
