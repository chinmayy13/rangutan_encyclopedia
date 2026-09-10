# What a Well-Built Rubric Looks Like

The five tasks below were selected because their rubrics were good and all five also passed GTF instruction-following review with no issues, so these are clean end to end task, not just on one side of the pipeline. They span five different domains on purpose, to show the same underlying discipline applies everywhere.

---

## Example — 6a6a7461f858c2a3993d2e5c

**The prompt:**

> Hey, can you finish the LiberLingua schema and spaced-repetition analysis package?
>
> The database pieces are in liberlingua_schema_setup.zip, which has liberlingua_mvp_schema.sql for the tables and liberlingua_seed_words.sql for the 600 simulated vocab records. There's also a charting script in liberlingua_analysis_draft.zip that someone started and never finished, and chart_style_reference.png shows the visual style our figures are supposed to follow.
>
> The schema relationship map is the key visual. Create liberlingua_schema_erd.png for words, user_profiles, mastery_events, review_sessions, and etymology_links, showing the column names and data types, identifying primary- and foreign-key columns, and labeling every declared relationship with 1:N cardinality. Keep the tables, labels, and connector paths readable.
>
> On the numbers side, I need the mastery distribution from the seeded database exported as mastery_distribution_raw.csv, showing each mastery state with its word count, share of vocabulary, average ease factor, average frequency score, average reviews per word, and total review sessions, where the averages are per word rather than per review row. The interval picture goes in review_latency_raw.csv, listing each SM-2 interval with its session count, average ease factor, average frequency score, and cumulative share of review activity, this time averaged across the review rows in that interval. Keep the headers in the snake_case we use everywhere else, with share_pct and cumulative_share_pct for the two percentage columns and an avg_ prefix on the averages.
>
> Finish the draft as liberlingua_chart_analysis.R so it turns those two exports into the mastery-state pie chart saved as mastery_state_piechart.png and the bar chart of session counts per SM-2 interval saved as sm2_interval_histogram.png. Both figures should follow the reference's color scheme, title and axis-label treatment, and legend conventions, with nothing clipped or overlapping, and I'd like the completed script included with the deliverables.
>
> Save all the completed deliverables to the Desktop. Thanks!

**The rubric:**

| Category | Weight | Criterion |
|---|---|---|
| format_gate (MUST-PASS) | 5 | Output includes a valid `.csv` file named `mastery_distribution_raw.csv`. |
| format_gate (MUST-PASS) | 5 | Output includes a valid `.csv` file named `review_latency_raw.csv`. |
| format_gate (MUST-PASS) | 5 | Output includes a valid `.png` file named `liberlingua_schema_erd.png`. |
| format_gate (MUST-PASS) | 5 | Output includes a valid `.png` file named `mastery_state_piechart.png`. |
| format_gate (MUST-PASS) | 5 | Output includes a valid `.png` file named `sm2_interval_histogram.png`. |
| format_gate (MUST-PASS) | 5 | Output includes a valid `.R` file named `liberlingua_chart_analysis.R`. |
| correctness | 20 | The headers, mastery-state rows, word counts, vocabulary shares, average ease factors, average frequency scores, average reviews per word, and total review sessions in output file `mastery_distribution_raw.csv` match the corresponding expected file within +/-0.01 for decimal values. |
| correctness | 20 | The headers, complete set of SM-2 interval rows, session counts, average ease factors, average frequency scores, and cumulative review-activity shares in output file `review_latency_raw.csv` match the corresponding expected file within +/-0.01 for decimal values. |
| correctness | 10 | The entity names, column names, data types, primary- and foreign-key designations shown in `liberlingua_schema_erd.png` match the corresponding expected file. |
| correctness | 15 | The join columns and 1:N cardinality labels for every relationship shown in output file `liberlingua_schema_erd.png` match the corresponding expected file. |
| correctness | 10 | The segment proportions in output file `mastery_state_piechart.png` match the corresponding expected file within +/-1 percentage point per segment. |
| correctness | 10 | The session count plotted for every SM-2 interval in output file `sm2_interval_histogram.png` matches the corresponding expected file. |
| correctness | 5 | The data-loading logic in output file `liberlingua_chart_analysis.R` is semantically equivalent to the corresponding expected file, allowing different R functions or packages that read the same two CSV files. |
| correctness | 10 | The mastery-state pie-chart generation and export logic in output file `liberlingua_chart_analysis.R` is semantically equivalent to the corresponding expected file, allowing different R functions or packages that produce the same chart and output file. |
| correctness | 10 | The SM-2 interval bar-chart generation and export logic in output file `liberlingua_chart_analysis.R` is semantically equivalent to the corresponding expected file, allowing different R functions or packages that produce the same chart and output file. |
| visual | 20 | Output file `mastery_state_piechart.png` uses the color scheme, title treatment, axis-label handling, and legend conventions represented in the corresponding expected file, with clearly distinguishable segments and all content legible within the image bounds. |
| visual | 20 | Output file `sm2_interval_histogram.png` uses the color scheme, title treatment, axis-label handling, and legend conventions represented in the corresponding expected file, with clearly distinguishable bars and all content legible within the image bounds. |
| visual | 10 | Output file `liberlingua_schema_erd.png` keeps table text, relationship labels, connector paths, tables, and joins distinct and readable. |

**Why this rubric works:**

- The R-script logic is split into three separate, independently-scorable criteria (data loading, pie-chart generation, bar-chart generation) — each one explicitly written as "semantically equivalent... allowing different R functions or packages," so a valid alternative implementation can't be penalized for using different code than the reference.
- Both chart visual criteria pair the positive requirement ("clearly distinguishable... all content legible") with the style-matching requirement in the same sentence — no unpaired "no clipping" rule that a shrink-to-fit output could sneak past.
- Every numeric criterion states its own tolerance (±0.01, ±1 percentage point) instead of leaving "matches" ambiguous.

---

## Example — 6a62dc372071f153f642fc11

**Software & Data / Software Developers — cross-system data reconciliation + report**

**The prompt:**

> Our platform dashboard still shows a different per-model run count depending on when you look at it: the model registry and the runtime API each report their own figure, and nobody has ever reconciled the two. Data Operations has published the policy that governs the reconciled result in run_count_reconciliation_policy.pdf, and it is on the Desktop along with the two source extracts, model_registry_export.xlsx from the registry and api_run_snapshot_20240915.csv from the runtime API.
>
> Work through them and produce the reconciled dataset as corrected_model_runs.csv, using the fields and row order the policy defines. Save it on the Desktop.
>
> Then prepare reconciliation_report.pdf for the platform leads who approve the dashboard. It should present the reconciled count for every model, explain the basis of each outcome, show the registry and runtime API figures and the size of the gap alongside the final one, and call out the three models where the two systems disagree most. Include a chart of the reconciled counts with each bar labelled with its figure, and close with a concise recommendation for reducing future drift between the two systems. Save the report on the Desktop.
>
> Do the data work in VS Code and build the report in LibreOffice. The leads read this on screen, so review the rendered tables and chart in LibreOffice before you export it to PDF: they need to be fully legible, with no clipped labels, no overlapping elements, and no columns extending beyond the page.

**The rubric:**

| Category | Weight | Criterion |
|---|---|---|
| format_gate (MUST-PASS) | 5 | The output includes a file named `corrected_model_runs.csv` with a `.csv` extension. |
| format_gate (MUST-PASS) | 5 | The output includes a file named `reconciliation_report.pdf` with a `.pdf` extension. |
| correctness | 10 | The header row of `corrected_model_runs.csv` lists the same field names in the same order as the expected file. |
| correctness | 15 | `corrected_model_runs.csv` contains one data row per model present in the expected file, in the same order, with no additional and no missing rows. |
| correctness | 20 | For every row in `corrected_model_runs.csv`, the `registry_run_count` value matches the corresponding value in the expected file, and is left empty wherever the expected file leaves it empty. |
| correctness | 10 | For every row in `corrected_model_runs.csv`, the `api_run_count` value matches the corresponding value in the expected file, and is left empty wherever the expected file leaves it empty. |
| correctness | 20 | For every row in `corrected_model_runs.csv`, the `abs_delta_pct` value matches the corresponding value in the expected file within 0.01, and is left empty wherever the expected file leaves it empty. |
| correctness | 50 | For every row in `corrected_model_runs.csv`, the `corrected_run_count` value matches the corresponding value in the expected file exactly. |
| correctness | 40 | For every row in `corrected_model_runs.csv`, the `correction_reason` value is the same string as the corresponding value in the expected file, character for character. |
| correctness | 35 | The reconciliation table in `reconciliation_report.pdf` covers the same models as the corresponding table in the expected file and reports the same registry figure, runtime API figure, delta percentage, reconciled figure and basis for each of them. |
| correctness | 20 | `reconciliation_report.pdf` singles out the same models as the largest disagreements that the expected file singles out, and accounts for each of them in terms semantically equivalent to the expected file. |
| correctness | 15 | The chart in `reconciliation_report.pdf` plots the reconciled run count for the same models as the chart in the expected file, with the figure printed on each bar matching the corresponding value in the expected file. |
| correctness | 15 | `reconciliation_report.pdf` includes a recommendation for reducing future drift between the two systems that names at least one change to how the two systems are reconciled, monitored or refreshed. A recommendation that differs from the one in the expected file is accepted when it addresses the same causes of drift as the expected file. |
| visual | 35 | Every table in `reconciliation_report.pdf` is fully legible, with no clipped cell text, no overlapping text and no column extending beyond the page margin. |
| visual | 30 | In the chart in `reconciliation_report.pdf`, the model labels, the value axis labels and the figure on each bar are fully readable, with no label clipped, truncated or overlapping another element. |
| visual | 20 | The headings and body text of `reconciliation_report.pdf` render cleanly, with each section visually separated from the next and no overlapping text, clipped characters or stray formatting artifacts. |
| visual | 5 | `reconciliation_report.pdf` ends with the recommendation section, as the expected file does. |

**Why this rubric works:**

- The CSV output is scored per-field rather than per-row: registry count, API count, delta %, corrected count, and correction reason each get their own criterion with its own weight — so a mistake in one field doesn't hide inside (or wrongly sink) a bundled row-match check.
- The recommendation criterion explicitly states "a recommendation that differs from the one in the expected file is accepted when it addresses the same causes of drift" — a textbook example of the non-overfitting carve-out for open-ended reasoning tasks.
- All three visual criteria (tables, chart, headings/body) pair a positive legibility term with the no-clipping/no-overlap language in the same sentence, and the report is required to end with the recommendation section — a structural check that's easy to skip but catches real formatting bugs.

---

## Example — 694bace5d8a0b9cd5e364958

**Media & Entertainment — investor pitch sheet + comps chart**

**The prompt:**

> I have a final investor meeting for the new Yorkshire film tomorrow. I need to prove to them that localized stories can actually make money on a national level here in UK, so help me put together some comps.
>
> I've attached three files for you in the Desktop: indie_box_office_comps.xlsx, director_vision_notes.docx, and WYIFF_Historical_Attendance.csv.
>
> I'll need a one-page pitch sheet to hand out to the investors. My colleague said it's good to pull the logline and main themes from the director's notes to use as the intro, and I think is fine. Then, look at the comps spreadsheet and figure out which three films had the highest national box office return relative to their production budget (ROI). Also, my manager asked me to add a table to the sheet showing those three films, their budgets, and their net national ROI percentage. Then, help me analyze the film festival CSV and add a quick highlight stating the average percentage of non-Yorkshire attendees over the last five recorded years, just to prove people travel for these films. Just follow the rule in the director's notes about local and visiting press, and be sure to skip any projected, estimated, or cancelled rows (by the way you can ignore the column with the reported total in that CSV, the festival directors told me it's notoriously buggy, just sum up the actual attendance columns yourself to get the true total).
>
> Name this document as investor_pitch_sheet.pdf. Give the file a look in the print layout to check the tables, last batch had tables spilling across the pages and this is not what my manager wants.
>
> I'll also need you to take those top three ROI films you found and make a clean, professional bar chart comparing their local vs. total national box office gross, name the chart as national_appeal_comps.png, and see the image to make sure the legend is readable because my manager asked me to pay attention so it isn't covering any of the bars or data.
>
> Drop both files on the desktop when you are done.

**The rubric:**

| Category | Weight | Criterion |
|---|---|---|
| format_gate (MUST-PASS) | 10 | Provides an openable file named `investor_pitch_sheet.pdf` with the `.pdf` extension. |
| format_gate (MUST-PASS) | 10 | Provides an openable image named `national_appeal_comps.png` with the `.png` extension. |
| correctness | 10 | The logline presented in `investor_pitch_sheet.pdf` is semantically equivalent to the corresponding logline in the expected file. |
| correctness | 10 | The main themes presented in `investor_pitch_sheet.pdf` are semantically equivalent to the main themes in the expected file. |
| correctness | 15 | The table in `investor_pitch_sheet.pdf` identifies the same top three ROI films as the corresponding expected file. |
| correctness | 10 | The table in `investor_pitch_sheet.pdf` reports the production budgets for the top three films, matching the corresponding expected file within a ±1% tolerance. |
| correctness | 15 | The table in `investor_pitch_sheet.pdf` reports the net national ROI percentage for the top three films, matching the corresponding expected file within a ±1% tolerance. |
| correctness | 15 | The average percentage highlight value in `investor_pitch_sheet.pdf` about the number of non Yorkshire attendees over the last five recorded years matches the value in the corresponding expected file within a ±1% tolerance. |
| correctness | 10 | The bar chart in `national_appeal_comps.png` plots the local box office gross for the top three ROI films, matching the data in the corresponding expected file within a ±1% tolerance. |
| correctness | 10 | The bar chart in `national_appeal_comps.png` plots the national box office gross for the top three ROI films, matching the data in the corresponding expected file within a ±1% tolerance. |
| format_gate | 5 | The `investor_pitch_sheet.pdf` is formatted as one page, matching the number of pages in the corresponding expected file. |
| visual | 10 | The table in `investor_pitch_sheet.pdf` is fully contained within the page margins without spilling or splitting across pages, matching the layout in the corresponding expected file. |
| visual | 10 | The chart in `national_appeal_comps.png` includes a legend distinguishing local versus total national box office gross, matching the corresponding expected file. |
| visual | 10 | The legend in `national_appeal_comps.png` is clearly legible and positioned so that it does not overlap, cover, or obscure any of the data bars, matching the corresponding expected file. |
| visual | 5 | The content and layout of `investor_pitch_sheet.pdf` are presented in a professionally comparable handout format to the corresponding expected file. |
| visual | 5 | All text and table content in `investor_pitch_sheet.pdf` is fully visible and legible, with no truncated or unreadably small text, matching the corresponding expected file. |
| visual | 5 | The bar chart in `national_appeal_comps.png` includes clearly labeled axes, a title, and spacing comparable to the corresponding expected file. |
| correctness | 15 | The highlight support statement in `investor_pitch_sheet.pdf` to prove non-Yorkshire attendees travel for these films is semantically equivalent to the corresponding expected file. |
| correctness | 5 | The axes labels in `national_appeal_comps.png` identify the same three films as the corresponding expected file. |
| visual | 5 | The `investor_pitch_sheet.pdf` includes major labeled sections layout equivalent to an intro logline, main themes, audience reach highlight, and financial comps table, comparable to the corresponding expected file. |

**Why this rubric works:**

- The non-Yorkshire-attendee highlight is split into two criteria on purpose: one checks the computed number (±1% tolerance), the other checks the qualitative "support statement" text — two genuinely different failure modes, not a duplicate.
- The one-page and no-table-spilling requirements anchor to "the layout in the corresponding expected file" rather than inventing an arbitrary rule, which is the accepted way to satisfy the anti-hacking robustness check without a separate legibility clause.
- No criterion hardcodes a specific dollar figure or percentage in its own text — everything compares to the expected file, so the rubric can't go stale if the underlying data changes.

---

## Example — 697b044c5f8828abae7a0002

**Engineering / Product Design — two-phase QFD (House of Quality) package**

**The prompt:**

> I'm completing a two-phase QFD (House of Quality) for the Logitech M240 mouse. The attached files are the teardown file, named partss.pdf, the two-user interview data condensed into the file Customer Needs.xlsx, and the QFD template called QFD format.xlsx.
>
> For the customer requirements, use the consolidated need column, counting how many interview statements map to each consolidated need label, that would be the need's frequency. Then select the six highest-frequency needs, rank by frequency, breaking any tie alphabetically by the need's label. Then assign weights by rank this way: the top two needs get 9, the next two get 3, and the last two get 1.
>
> For the engineering side, use these six metrics: total mass in grams, overall length in mm, overall width in mm, peak click force in N, click sound level at 0.25 m in dBA, and scroll wheel torque in N·mm. For Product A, use values from the teardown. If something isn't available there, just mark it as "measurement required" and keep the target as TBD. For the relationship matrix, score each need-metric pair as 9 (dominant driver), 3 (moderate), 1 (weak), or 0 (none). For the roof, mark each metric-metric correlation as positive or negative only (no numbers) and leave pairs with no meaningful correlation blank.
>
> For phase two, please make sure to use the exact component names from the teardown and map each one to the metrics using the same scoring scale as phase one.
>
> I need two files as a result, saved on my Desktop: A PDF named M240_QFD_Package.pdf with the completed QFD. Open the completed document and visually ensure the phase one and phase two matrices fit cleanly within page margins without any overlapping text or clipped column titles, and a Word document named M240_QFD_Rationale.docx explaining the reasoning of these: why each need and metric was chosen, justifying every strong (9) relationship using actual customer quotes and relevant teardown references, a description of the roof correlations and how they influenced decisions, and exactly three examples of mistakes that could happen in this QFD, why they'd be wrong, and how to avoid them.
>
> Before finishing, it is essential that you open both files and make sure that the tables are not cut off at the page breaks. To be absolutely sure, I need you to do a print preview using letter size paper to double-check that.

**The rubric:**

| Category | Weight | Criterion |
|---|---|---|
| format_gate (MUST-PASS) | 5 | Includes a PDF file named `M240_QFD_Package.pdf`. |
| format_gate (MUST-PASS) | 5 | Includes a Word document named `M240_QFD_Rationale.docx`. |
| correctness | 20 | The Phase 1 relationship matrix in `M240_QFD_Package.pdf` lists the same six customer needs, in the same rank order, as the corresponding expected file. |
| correctness | 15 | The Phase 1 matrix in `M240_QFD_Package.pdf` assigns each of the six needs the rank-based customer weight that matches the corresponding expected file. |
| correctness | 20 | The Phase 1 matrix in `M240_QFD_Package.pdf` presents the six prescribed engineering metrics with semantically equivalent names and units as the corresponding expected file. |
| correctness | 10 | Every scored cell in the Phase 1 relationship matrix in `M240_QFD_Package.pdf` uses only the values 0, 1, 3, or 9 as scores, matching the corresponding expected file. |
| correctness | 10 | The Phase 1 relationship matrix in `M240_QFD_Package.pdf` includes a scored value in every need-metric cell, matching the corresponding expected file. |
| correctness | 25 | The Product A row in `M240_QFD_Package.pdf` reports the teardown-derived total mass and uses semantically equivalent labels for metrics unavailable in the teardown, matching the corresponding expected file. |
| correctness | 20 | The Technical Target row in `M240_QFD_Package.pdf` uses semantically equivalent target entries for each metric, matching the corresponding expected file. |
| correctness | 15 | The roof correlation matrix in `M240_QFD_Package.pdf` marks the same set of metric pairs as correlated, each with the same sign (positive/negative) and with no numeric correlation strengths recorded, as the corresponding expected file. |
| correctness | 20 | Phase 2 of `M240_QFD_Package.pdf` lists all ten teardown components using the exact part names shown in the corresponding expected file. |
| correctness | 10 | Every scored cell in the Phase 2 allocation matrix in `M240_QFD_Package.pdf` uses only the values 0, 1, 3, or 9 as scores, matching the corresponding expected file. |
| correctness | 10 | The Phase 2 allocation matrix in `M240_QFD_Package.pdf` includes a scored value for every listed component across all six metrics, matching the corresponding expected file. |
| correctness | 20 | `M240_QFD_Rationale.docx` explains the consolidated-need frequency counts, tie-break logic, and resulting top-six ranking, semantically matching the corresponding expected file. |
| correctness | 12 | `M240_QFD_Rationale.docx` explains why each of the six customer needs is included in the Phase 1 matrix, semantically matching the reasoning in the corresponding expected file. |
| correctness | 12 | `M240_QFD_Rationale.docx` explains why each of the six engineering metrics is included in the Phase 1 matrix, semantically matching the reasoning in the corresponding expected file. |
| correctness | 15 | `M240_QFD_Rationale.docx` justifies every strong (9 score) relationship in the Phase 1 matrix using customer quotes and teardown references that are semantically equivalent to those in the corresponding expected file. |
| correctness | 10 | `M240_QFD_Rationale.docx` describes the roof correlations and how they influence design decisions, semantically matching the corresponding expected file. |
| correctness | 10 | `M240_QFD_Rationale.docx` includes exactly three QFD error examples, each describing the mistake, why it is wrong, and how to avoid it, semantically comparable to the corresponding expected file. |
| visual | 20 | The Phase 1 matrix (roof, relationship matrix, and benchmarking rows) in `M240_QFD_Package.pdf` renders within the page margins with legible headers and no overlapping, clipped, or truncated text, comparable to the corresponding expected file. |
| visual | 20 | The Phase 2 allocation matrix in `M240_QFD_Package.pdf` renders within the page margins, with all ten component names and all metric and score/rank columns legible and free of overlap or clipping, comparable to the corresponding expected file. |
| visual | 20 | `M240_QFD_Rationale.docx` is organized with clear section headings, readable paragraph structure, and legible tables, with no overlapping text, truncation, or formatting artifacts, comparable to the corresponding expected file. |
| visual | 20 | `M240_QFD_Package.pdf` renders Phase 1 and Phase 2 tables without table content cut off at page breaks at letter size, comparable to the corresponding expected file. |

**Why this rubric works:**

- The roof-correlation criterion explicitly bans numeric correlation strengths ("with no numeric correlation strengths recorded") — directly encoding the prompt's own "positive or negative only, no numbers" rule instead of leaving it to a generic "matches expected file" check.
- "Exact part names" is required for Phase 2 components — normally a red flag for overfitting, but here it's justified because the prompt itself explicitly demands exact teardown names. Exact-match language is only ever appropriate when the prompt asks for exactness.
- Despite 24 criteria across two files and two phases, weight-share math still lands cleanly in band (correctness ~74%, visual ~23%), proving thoroughness and correct proportioning aren't in tension.

---

## Example — 6a6a7461f858c2a3993d2e7b

**Web / Docs tooling — restoring a broken doc-generation build to its approved design**

**The prompt:**

> Our developer docs ship with a "Language Samples" reference page that shows one annotated excerpt from each of the five sample files we maintain: classic.c, Main.java, coffeemaker.js, catalog.hs, and inventory.go. The page is generated by a small Python build script that reads each sample's header metadata and section markers, pulls out the designated excerpt, and writes a single static HTML page styled by its stylesheet. After last week's refactor, the rendered page drifted away from the approved design, and it needs to be brought back in line before the docs freeze.
>
> The project lives in code-samples-project.zip, which contains build_docs.py, docs_theme.css, and the samples folder. The approved design is captured in design-reference.png, a full-page mock showing the finished page and its card layout, and in card-detail-reference.png, a close-up of the first card showing the intended treatment of the points list, the filename bar, the "Demonstrates point" callout, and the code excerpt. The five sample files are correct as shipped, so whatever drifted did so in the generator or the stylesheet. Track down everything the refactor broke and rebuild until the rendered page matches the approved design, especially on typography, background treatment, color scheme, and column layout.
>
> Once the page matches, open it in the browser and capture a screenshot showing the top of the page with the first row of sample cards fully visible, saved as samples-preview.png. Deliver the fixed build_docs.py, the fixed docs_theme.css, the regenerated samples.html, and samples-preview.png, all saved to the Desktop.

**The rubric:**

| Category | Weight | Criterion |
|---|---|---|
| format_gate (MUST-PASS) | 5 | Output includes a valid `.html` file named `samples.html`. |
| format_gate (MUST-PASS) | 5 | Output includes a valid Python file named `build_docs.py`. |
| format_gate (MUST-PASS) | 5 | Output includes a valid CSS file named `docs_theme.css`. |
| format_gate (MUST-PASS) | 5 | Output includes a valid `.png` image named `samples-preview.png`. |
| correctness | 15 | Each card's points list content in `samples.html` matches the corresponding expected file. |
| correctness | 15 | Each code excerpt's content in `samples.html` matches the corresponding expected file. |
| correctness | 12 | `build_docs.py` reads every sample files' header metadata and section markers, extracting the designated excerpts from them, matching the corresponding expected file. |
| correctness | 12 | The style rules in `docs_theme.css` are applied to `samples.html`, matching the corresponding expected file. |
| correctness | 10 | Every required sample card is present in `samples.html`, matching the corresponding expected file. |
| correctness | 10 | The sample cards in `samples.html` appear in the same order as the corresponding expected file. |
| visual | 5 | In `samples-preview.png`, the column layout of the sample cards matches the corresponding expected file. |
| visual | 5 | In `samples-preview.png`, the overall color scheme matches the corresponding expected file. |
| visual | 5 | In `samples-preview.png`, the typography matches the corresponding expected file. |
| visual | 5 | In `samples-preview.png`, the code excerpts' style match the corresponding expected file. |
| visual | 5 | In `samples-preview.png`, the background matches the corresponding expected file. |
| visual | 5 | In `samples-preview.png`, the filename bar style matches the corresponding expected file. |
| visual | 5 | In `samples-preview.png`, the "Demonstrates point" callout style matches the corresponding expected file. |
| visual | 5 | `samples-preview.png` shows the top of the page with the first row of sample cards fully visible, matching the corresponding expected file. |

**Why this rubric works:**

- This is the best atomicity example in the whole audit: seven distinct visual sub-elements — column layout, color scheme, typography, code-excerpt style, background, filename-bar style, and callout style — each get their own dedicated criterion instead of being bundled into one vague "looks right" check. A grader (or reviewer) can pinpoint exactly which element broke.
- Correctness and visual are kept cleanly separate: content-correctness criteria (points list, code excerpt text, card presence/order) never mix with the purely visual criteria above them — no categorization drift.
- The final screenshot criterion ("shows the top of the page with the first row of sample cards fully visible") directly mirrors the prompt's own screenshot instruction, so nothing about the deliverable is invented by the rubric writer.
