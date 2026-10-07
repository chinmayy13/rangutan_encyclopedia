# ORANGUTAN ENCYCLOPEDIA | CUA v3

# What Makes a Prompt Stump the Agent

**Prompt writing guide · Read time: ~10 min**

---

> **Confidentiality notice**
>
> This document is for internal use by authorized Orangutan_Encyclopedia contributors only. Do not share externally or post in public forums.

---

## Table of Contents

- General Guidance
  - 1\. Stumpers at a glance
  - 2\. Requests that Work and Requests that don't
  - 3\. Before → after: rewrites that bring difficulty back
  - 4\. Prompt examples: real prompts that stumped the agent
- Domain Specific Guidance
  - Finance and Accounting
  - Software and Data
  - Design and Creative
  - Engineering
  - Legal and Compliance
  - Healthcare
  - Sales and Marketing
  - STEM Research
  - Multimedia and Audiovisual
  - Operations and Management
  - Real Estate
  - Government and Public Sector

---

## General Guidance

### 1. Stumpers at a glance

A strong task has at least two, and one of them decides the answer.

| # | Stumper | Description |
|---|--------|-------------|
| 1 | **The method hides in the files** | The rule lives in an attached document and differs from the textbook default. |
| 2 | **Judgment at the boundary** | Tens of items, each tested against a rule, with near-misses on both sides. |
| 3 | **Knowing when to stop** | The right answer is to flag an unsupported step, not to finish with an estimate. |
| 4 | **The key fact is off to the side** | A correction, footnote or defined term that changes the answer. |
| 5 | **Visual Template or 3D visual judgment** | Something must be measured or identified by eye, among look-alikes. |
| 6 | **One early decision cascades** | A single upstream choice sets most of the deliverables. |
| 7 | **Real specialist conventions** | Close-but-wrong is easy for a generalist; right needs the expert rule. |

---

### 2. Requests that Work and Requests that don't

#### Top Request Types that stumped the model

| # | Request type | Pattern and example | Model Stumping rate |
|---|-------------|---------------------|-------------------|
| 1 | **Apply source-specific definitions and exceptions** | The model applies a familiar approach instead of the supplied source's exact rule. Example: exclude a particular securitization obligation from covenant debt, or recognize that a measurement is not evaluable under the manual. | 40.5% — 15/37 attempts, 8 tasks |
| 2 | **Provide precise and comprehensive source traceability** | A plausible answer is easier than tracing every value and substantive claim to the correct page, line item, period, or clause. Example: produce a calculation package and a source register for every number. | 51.9% — 40/77 attempts, 17 tasks |
| 3 | **Identify the complete analytical scope before calculating** | The model selects an incomplete or incorrect set of observations, undermining later calculations. Example: identify both fluorescence peaks per condition, cover all 64 array elements, or include exactly the days in a monitoring episode. | 72.2% — 65/90 attempts, 19 tasks |
| 4 | **Identify technical objects from images or 3D evidence** | Broad recognition can succeed while precise identification fails. Example: recognize a hand but name the wrong missing bones, or misidentify a specimen and assign incorrect anatomical character states. | 66.1% — 39/59 attempts, 12 tasks |
| 5 | **Reconcile multiple sources through dependent calculations** | Values must be selected, classified, reconciled, and carried through several formulas. An early interpretation error spreads. Example: reconstruct debt, net debt, EBITDA, and covenant ratios from an agreement and financial filings. | 46.8% — 51/109 attempts, 25 tasks |
| 6 | **Recognize when evidence does not support a unique answer** | The model sometimes supplies a precise answer when the sources support only a range or unresolved conclusion. Example: give an exact cohort headcount despite overlapping categories that prevent a unique count. | 56.7% — 34/60 attempts, 13 tasks |
| 7 | **Apply conditional rules while distinguishing facts from assumptions** | The challenge is deciding which rule applies, what prerequisites are established, and what remains conditional. Example: classify environmental obligations using substance identity, quantity, release status, and missing facts. | 36.4% — 12/33 attempts, 7 tasks |
| 8 | **Support a recommendation with complete comparative evidence** | The recommendation can be correct while comparison rows, measurements, or constraint checks are wrong or missing. Example: compare cryptographic candidates' timings, sizes, and field-limit compliance. This rate covers one task only. | 0.0% — 0/6 attempts, 1 task |
| 9 | **Make a targeted change while preserving an existing technical contract** | The model introduces a feature but changes unrelated definitions or behavior. Example: add a Waitlist class while preserving existing enums, defaults, relationships, and class attributes. | 68.6% — 24/35 attempts, 7 tasks |
| 10 | **Keep analytical content consistent across multiple outputs** | A finding must remain identical in a dataset, chart, report, and presentation. Errors can spread into several outputs. However, the high full-credit rate means consistency alone is a weak standalone stumping request. | 89.3% — 67/75 attempts, 18 tasks |

#### Top Request Types that the model solves easily

| # | Request type | Pattern and example | Full credit |
|---|-------------|---------------------|------------|
| 1 | **Make content readable and prevent visual collisions** | Legible labels, readable text, and avoiding clipping or overlap usually pass even when analysis is wrong. Example: ensure chart labels and legends do not overlap plotted data. | 87.6% — 687/784 attempts, 169 tasks |
| 2 | **Organize content into explicitly named sections** | The model generally follows a clear structural outline. Example: include mapping, findings, methodology, results, and recommendations in the requested order. | 95.9% — 94/98 attempts, 24 tasks |
| 3 | **Keep tables and result blocks together across pages** | Basic pagination requirements are usually handled successfully. Example: prevent a calculation block from splitting across pages or a heading from being stranded. | 95.6% — 174/182 attempts, 40 tasks |
| 4 | **Apply conventional chart styling** | Standard presentation instructions are easier than determining what the chart should contain. Example: use distinct line colors, labeled axes, a legend, and matching translucent standard-deviation bands. | 79.0% — 241/305 attempts, 68 tasks |
| 5 | **Produce basic structured-data syntax and organization** | Syntax can be valid while semantics are wrong. Example: create valid YAML or a table with the requested fields. Exact headers and keys are less reliable. | 66.4% — 91/137 attempts, 29 tasks |
| 6 | **Perform calculations with clear inputs and explicit rules** | Arithmetic often succeeds with unambiguous inputs and rules. Example: calculate a daily reserve, standard deviation, or lifting index. | 85.4% — 76/89 attempts, 20 tasks |
| 7 | **Filter join and sort data using explicit criteria** | Deterministic selection and ordering can succeed across sources. Example: identify eligible teachers using loan, school, and shortage-subject records; sort factories by ranking. | 100.0% — 38/38 attempts, 7 tasks |
| 8 | **Draw a workflow from an explicitly described process** | The model usually communicates a supplied sequence effectively. Example: diagram key generation, encapsulation, encryption, and API fields, or render an entity relationship diagram. | 93.5% — 29/31 attempts, 6 tasks |
| 9 | **State a high-level recommendation or overall verdict** | The headline decision can pass before supporting evidence does. Example: recommend a cryptographic pairing or defer a release while missing benchmark details or policy thresholds. | 73.4% — 69/94 attempts, 20 tasks |
| 10 | **Follow explicit instructions for handling missing information** | Directly specified missing-data behavior is easier than independently recognizing underdetermination. Example: report "Not calculable from provided excerpts" and leave a deficit null when unit-cost data are absent. This rate covers two tasks only. | 100.0% — 9/9 attempts, 2 tasks |

---

### Additional Tips

#### The method hides in the files

| | |
|---|---|
| **What it is** | The rule, definition or formula that decides the answer sits in an attached SOP, lab notebook, manual or contract, and it differs from what a professional would do by default. |
| **Why it works** | The agent knows the textbook method very well and reaches for it first. It applies the familiar default even when the notes define something else. |
| **How to build it** | Ask the business question only ("determine the detection limit"). Put the convention in the document as a normal part of it, not highlighted. Make sure the default and the defined rule give clearly different results. |
| **Example** | Lab notes define the detection limit with their own blank-based rule. The agent used the textbook formula, and every downstream value missed. |
| **Keep it fair** | The document must state the convention clearly. If a reasonable expert could argue for the default, the task is ambiguous, not hard. |

#### Judgment at the boundary

| | |
|---|---|
| **What it is** | Roughly 10 to 60 different items (defects, claims, measures, tasks, clauses), each classified against a written rule, with near-misses on both sides. |
| **Why it works** | The agent tends to classify by label or keyword instead of testing each item against the rule itself. Hundreds of rows don't work the same way: it scripts those. |
| **How to build it** | Put the rule in the inputs. Include items whose name suggests one category but whose substance meets the other. Ask for the classification plus a total that depends on it. |
| **Example** | Hospital price-file defects: some look like "encoding" issues but actually break a disclosure requirement. The agent sorted them by label and got the severity tiers wrong. |
| **Keep it fair** | Every boundary item must be decidable from the rule text. Grade those items explicitly. |

#### Knowing when to stop

| | |
|---|---|
| **What it is** | Part of the task can't be completed from the documents (an undisclosed input, or a defined term that excludes an item), so the correct response is to stop and flag it. |
| **Why it works** | The agent is very completion-driven. It fills gaps with proxies and "indicative" estimates rather than stopping. |
| **How to build it** | Ask for the full deliverable anyway, so stopping is a judgment the agent has to make. Let the documents, not the prompt, show why the step is unsupported. |
| **Example** | A covenant leverage test where one required input is undisclosed. The right answer is to stop and flag it; the agent produced an indicative ratio using estimates. |
| **Keep it fair** | The stop point must follow from the documents. Grade the stop and the stated reason. Never make it depend on a file that isn't attached. |

#### The key fact is off to the side

| | |
|---|---|
| **What it is** | A fact that changes the answer sits somewhere the agent treats as background: a side log, a footnote, a correction table, a manifest remark, a relabeled duplicate. |
| **Why it works** | Obvious traps (visible duplicates, plain mismatches) now get caught. Facts in secondary places, and quiet changes to the population, still slip by. |
| **How to build it** | Place the fact in a document the main task doesn't obviously need. Make it change a count, a value or a classification. Don't hint at it anywhere. |
| **Example** | An air-quality log where one day was duplicated under a new date. Missing it changed the row count, the number of activation days and which chart was right. |
| **Keep it fair** | An expert reading all the inputs must be able to find it. The expected file must show the resolution. |

#### Fine or 3D visual judgment

| | |
|---|---|
| **What it is** | The answer must be measured or identified by eye with precision: unlabeled 3D parts, a rotation angle, morphological features, picks on a scientific image, subtle errors in photos. |
| **Why it works** | Reading a clear chart or photo is easy for the agent now. Fine spatial judgment and look-alike identification are not, especially when later steps depend on them. |
| **How to build it** | Require a precise visual quantity or identification. Add plausible distractors (similar structures, faint features). Make downstream deliverables depend on it. |
| **Example** | Assemble unlabeled 3D bone models and name the missing ones. The agent couldn't identify parts by shape, so every downstream label was wrong. |
| **Keep it fair** | Use tolerances (e.g. +/-5 degrees) and evidence that experts would agree on. |

#### One early decision cascades

| | |
|---|---|
| **What it is** | A single early step (a filter, a join, an identification, an assembled parameter) determines most of the downstream values and files. |
| **Why it works** | The agent does each step well but rarely revisits an early choice once it builds on it. One plausible-but-wrong call costs most of the rubric. |
| **How to build it** | Make the early step one of stumpers 1-5, and make the charts, totals and recommendations all flow from it. |
| **Example** | A valuation where the discount rate must be assembled from three documents. One different choice there wiped out most of the numeric criteria. |
| **Keep it fair** | Grade the early decision once as its own criterion, then weight downstream values by importance, without over-penalising the same error. |

#### Real specialist conventions

| | |
|---|---|
| **What it is** | Correctness depends on niche conventions (statute subsections, covenant mechanics, lab and spectroscopy conventions, engineering standards) rather than general professional knowledge. |
| **Why it works** | The agent's general knowledge is broad, but it applies niche conventions approximately. Close-but-wrong is its typical failure. |
| **How to build it** | Choose the specialist variant where the generalist answer is close but wrong, and provide the governing source in the inputs. |
| **Example** | Identifying a fossil genus from limb characters in specimen photos. The agent's answer was plausible but named the wrong genus. |
| **Keep it fair** | The expert answer must be checkable from the provided sources or a standard reference. |

---

### 3. Before → after: rewrites that bring difficulty back

Real tasks the agent now solves, with fair changes that make them hard again.

| Before (agent solves it) | After (difficulty restored) |
|--------------------------|---------------------------|
| "I'd rather have the AKT premise checked than assumed." | State the premise as the team's working view. The pathway map in the inputs shows it's wrong. |
| Output columns ask for "the containment level its requirements were drawn from". | Ask only for each lab's compliance rate. The level mismatch must be noticed in the documents. |
| The prompt lists the formula, cuts, windows and rounding. | The rules live in the manual, including one non-obvious convention. |
| The prompt lists every element of the legal test to check. | Ask only whether the payment is permitted. The agreement reveals which tests apply. |
| The prompt lists every driver each slide must cover. | Ask for the drivers. Grade against the full set in the sources, including one found only in a table note. |
| Match 3 images to 3 structure files. | Six candidate files, including near-identical look-alikes. |

---

### 4. Prompt examples: real prompts that stumped the agent

Seven real prompts from our project where the agent scored well under the bar, and the low score comes from how the task was set up, not from an unusually complex output file. Read the highlighted phrases first; they show where the trap is set.

> **How these were chosen**
>
> Low agent average, consistent across 3-6 runs, judged genuine (no rubric tricks), and most lost points come from a few decisive correctness criteria, not formatting or file complexity.

---

#### E1: Wildfire smoke: which days hit Smoke Emergency?

**30% agent avg · 5 runs**

**Healthcare** — Inputs: rooftop_pm25_export.csv, activation_levels.pdf, indoor_air_filtration_report.pdf, episode_chart_drafts.png — Outputs: daily_activation.csv, smoke_episode_review.pdf, smoke_activation_briefing.pptx

Stumpers: **#4 Key fact off to the side** · **#6 One early decision cascades**

**THE PROMPT** *(highlighted = where the stumper is set up)*

> I handle emergency management for Canyon Vista Medical Center, a small community hospital in Sacramento. We just came through a multi-day wildfire smoke episode, and I need to brief our leadership on how bad each day got and which days would have put us at our highest response level.
>
> I have attached the export from our rooftop air monitor for the episode, a one-page sheet that lists our smoke activation levels, a background report on indoor air filtration, and a set of draft charts one of our analysts sketched.
>
> For each day in the episode, work out the day's air quality and the activation level it falls under, then determine which day or days reached Smoke Emergency. Prepare three files for the leadership review and save them to the Desktop.
>
> Make a short PDF named smoke_episode_review.pdf that lays out the day-by-day activation levels, states which day or days reached Smoke Emergency, and includes the one draft chart that correctly represents the episode. Close it with a short set of protective steps for the next episode, drawing on the attached filtration report.
>
> Make a brief slide deck named smoke_activation_briefing.pptx for the board that carries the same finding, the same chart, and the protective steps.
>
> Make a data table named daily_activation.csv with one row for each day covered in the review, and the numbers behind each day's level.
>
> Keep the files plain and easy to read, and return only the three files.

| | |
|---|---|
| **Hidden in the files** | The rooftop monitor export repeats one day's readings under a new date. Among the analyst's draft charts, one has 7 bars and one has 6. |
| **What the agent did** | In all 5 runs it counted the duplicate as a real 7th day. That gave two Smoke Emergency days instead of one and the wrong row count, and it picked the 7-bar chart. Every run scored exactly 30%. |
| **Why it works** | The prompt never mentions data quality. A quiet "how many days are there?" decision drives the finding, the table and the chart choice. |

---

#### E2: GPR35: reconcile a potency review package

**44% agent avg · 3 runs**

**STEM Research** — Inputs: GPR35_Multipathway_Data_Package.pdf, GPR35_Cross_Functional_Review_Brief.pptx, GPR35_Methods_Buffer_Reagent_Log.docx, GPR35_Literature_Extraction_Matrix.docx, gpr35_potency_panels.png — Outputs: gpr35_claim_audit_memo.pdf, gpr35_review_deck.pptx

Stumpers: **#4 Key fact off to the side** · **#1 The method hides in the files**

**THE PROMPT** *(highlighted = where the stumper is set up)*

> We have the GPR35 cross-functional review tomorrow, and I need the package reconciled before it is circulated. The attached files include the main data package, `GPR35_Multipathway_Data_Package.pdf`, the methods and buffer log, `GPR35_Methods_Buffer_Reagent_Log.docx`, the literature extraction matrix, `GPR35_Literature_Extraction_Matrix.docx`, the review brief, `GPR35_Cross_Functional_Review_Brief.pptx`, and a sheet of candidate potency panels, `gpr35_potency_panels.png`.
>
> Based on these files, I want you to prepare the two deliverables requested in the review brief, saving both to the Desktop. Name the PDF `gpr35_claim_audit_memo.pdf` and the presentation `gpr35_review_deck.pptx`.
>
> In the deck, present the corrected Gi-proximal potency comparison as a chart. The potencies run across several orders of magnitude, so scale the value axis so every bar stays legible and the rank order reads at a glance, and keep the chart clear of the reconstruction table.
>
> The panel sheet shows four versions of the Gi-proximal comparison. Only one of them is consistent with the reconstruction the source data actually support. Work out which one that is, crop that panel out of the sheet, and include it in the memo as Figure 1 with a short caption.
>
> Use the evidence standards in the brief when assessing each claim. A claim should be treated as supported only when the quantitative result is interpretable and not materially weakened by assay quality, comparability or source conflicts. Use conditional status where the direction of the finding is useful, but the magnitude or generalizability is limited by assay context or technical caveats. Treat claims as not decision-grade where the evidence relies on non-comparable readouts, unresolved conflicts, failed assay acceptance, or missing validation needed for attribution.
>
> It would be great if you could use the highlight tool to add two removable text highlights on the passages where your reconciliation documents a potency rank-order reversal, using standard annotations that can be cleared later rather than flattened or permanent markup.

| | |
|---|---|
| **Hidden in the files** | The free-drug (buffer/BSA) correction is documented only in the methods & reagent log, a file that looks like background. The four candidate panels are nearly identical. |
| **What the agent did** | All 3 runs used uncorrected potencies. So it picked the wrong panel, gave several claims the wrong status, and found 8 of the 11 source conflicts. |
| **Why it works** | "Corrected" points nowhere specific. The correction lives in the least important-looking file, and everything downstream depends on it. |

---

#### E3: Fv/Fm: compare fluorescence peaks under two light conditions

**51% agent avg · 6 runs**

**STEM Research** — Inputs: Data Fvfm bands high light.xlsx, Data Fvfm bands low light.xlsx, Fvfm formula.pptx — Outputs: fluorescence_plot.png, Fvfm_results.pptx, fluorescence_report.pdf

Stumpers: **#1 The method hides in the files** · **#6 One early decision cascades**

**THE PROMPT** *(highlighted = where the stumper is set up)*

> I am writing a report on an experiment comparing chlorophyll fluorescence recovery in Arabidopsis under high-light versus low-light conditions. Compute and compare the Fv/Fm peak values between both conditions and evaluate the underlying physiological implications of the results. Use the method and formulae from the provided presentation file and the raw values in the spreadsheets for data analysis.
>
> Create a PNG plot showing changes in Fv/Fm against the records. Plot both conditions' mean curves on the same axes with each condition's standard deviation shown as a lighter, semi-transparent band in the matching color. Label the axes, indicate the peak values and the difference between the two conditions at each peak (high-light minus low-light) for both conditions. Save the plot to the Desktop as `fluorescence_plot.png`
>
> Also, provide a PDF document named `fluorescence_report.pdf` that describes the experimental procedures and data analysis in a "methodology" section in a research-article style. Also, report the results, including the maximum peak values for each condition and their differences, under a "results and discussion" section. Summarise the Fv/Fm of low-light, high-light, the differences, and the aligned peak position of each peak in a table. Evaluate the underlying physiological implications of the results. Save this PDF file to the Desktop.
>
> Lastly, add the PNG figure and the summary table to the attached PPTX presentation, each on a separate slide. Save the presentation file to the Desktop as `Fvfm_results.pptx`
>
> Open the pdf and pptx files and verify they render correctly. Check that the PNG figure includes peak values and indicates the values between peaks for both conditions. Ensure there are no overlapping elements or clipped text in all output files. If there are any formatting issues, adjust the layout and save the corrected versions.

| | |
|---|---|
| **Hidden in the files** | The method deck defines a peak-alignment procedure in which each condition has two fluorescence peaks. |
| **What the agent did** | All 6 runs took one global maximum per condition, the obvious default. Half the summary table and half the plot annotations were missing. Every run scored exactly 51%. |
| **Why it works** | The prompt points to the method instead of restating it. The method differs from what anyone would do by default. |

---

#### E4: IQVIA: is a $1.03B buyback a permitted Restricted Payment?

**54% agent avg · 5 runs**

**Finance & Accounting** — Inputs: IQVIA_CREDIT_AGREEMENT_trimmed_relevant_restr_payments.txt, IQVIA_FORM_10-K_trimmed_relevant_restr_payments.txt, IQVIA_FORM10-Q_JUNE_2025_trimmed_relevant_24pages.pdf — Outputs: Memorandum.pdf, Support_Calc.pdf, Trace_Reg.pdf

Stumpers: **#3 Knowing when to stop** · **#7 Real specialist conventions**

**THE PROMPT** *(highlighted = where the stumper is set up)*

> We're finalizing the Board materials covering our capital allocation activity through June 30, 2025, and I'd like an independent review before the package goes out.
>
> Please use the attached documents to look into whether the $1.032 billion of common stock repurchases disclosed for the six months ended June 30, 2025 can be supported as a Restricted Payment permitted under the Credit Agreement as of that date.
>
> I'm particularly interested in Sections 7.06(a)(iii) and 7.06(b)(xvii) as possible routes, but walk me through whatever the documents actually support — if one route gets you there and the other doesn't, or if neither fully closes the loop, I want to understand why and see your reasoning laid out so the Board can follow it.
>
> Please prepare three PDF documents and save them to the Desktop.
>
> Prepare a board memorandum saved as `Memorandum.pdf` that explains your approach, your analysis, and your overall conclusion. Once it's generated, open it and check that no heading is left stranded at the bottom of a page with its content pushed to the next page — adjust the breaks so each heading stays with the text that follows it.
>
> Prepare a supporting calculation package saved as `Support_Calc.pdf` containing the legal and financial analysis, covenant calculations, intermediate results, and supporting citations used to reach your conclusions. After generating it, check that no individual step or result block gets split across a page break — if one does, adjust the layout so each step reads as a continuous block.
>
> Prepare a trace register saved as `Trace_Reg.pdf` listing every numerical value used in the analysis together with its source. For Credit Agreement references, identify the relevant section or defined term. For SEC filings, identify the applicable table, line item, reporting period, and page where available. Before saving, review it to make sure each value stays together with its source description on the same page, so the register can be checked without flipping back and forth.

| | |
|---|---|
| **Hidden in the files** | The credit agreement's definition of Consolidated Total Debt excludes the receivables securitization, and the agreement-defined EBITDA is not disclosed in the filings. |
| **What the agent did** | It kept the $550M securitization in debt and used SEC-filing EBITDA as a stand-in, then concluded the leverage basket was clearly met. The right answer was to flag that defined EBITDA is unavailable and stop. |
| **Why it works** | Defined terms override reported numbers, and the honest answer is "we can't fully support this." The agent is strongly pulled toward finishing with a proxy. |

---

#### E5: Vantara: H-model DCF valuation memo

**57% agent avg · 4 runs**

**Finance & Accounting** — Inputs: Vantara_Systems_CIM.pdf, Precedent_Transactions_Comps.pptx, Macro_Assumptions_WACC_Build.docx — Outputs: Precedent_Transactions_Bridge.pdf, Vantara_Valuation_Memo.pdf

Stumpers: **#1 The method hides in the files** · **#6 One early decision cascades**

**THE PROMPT** *(highlighted = where the stumper is set up)*

> Hi, we need two valuation PDFs prepared for Vantara Systems Inc. ahead of Monday's sell-side M&A partner review for Vantara Systems Inc. Meridian Capital Advisors LLC has been exclusively retained by Vantara's Board of Directors to run a structured sale process targeting a Q3 2026 close. The partner review is an internal Transaction Committee meeting at which Meridian's deal team presents its valuation analysis and earnings quality assessment before engaging with prospective acquirers in the first round of the process.
>
> In order to conduct the valuation analysis and prepare the deliverables, you must use the following source files: Vantara_Systems_CIM.pdf, Precedent_Transactions_Comps.pptx, and Macro_Assumptions_WACC_Build.docx.
>
> The deliverables prepared here will serve as the analytical foundation for that meeting, anchoring the price expectation range the team will defend in negotiations with bidders and informing how management's reported financials should be presented and qualified to prospective buyers.
>
> Please prepare two downloadable pdf files:
>
> Vantara_Valuation_Memo.pdf should be a formal valuation memorandum addressed to the Transaction Committee. It should cover a full DCF analysis using the H-Model terminal value formulation, including the cost of capital build, the explicit three-year free cash flow forecast, and the terminal value calculation with both the Gordon Growth and transition premium components shown separately. It should also include a quality of earnings assessment of management's Adjusted EBITDA, reviewing each of the Tier 3 adjustments and reaching an analyst-recommended EBITDA figure. Present the document with a formal memo header, clear numbered sections, and use tables rather than prose to display all financial figures and calculations. Highlight key output rows and caption each table.
>
> Precedent_Transactions_Bridge.pdf should present all twelve precedent transactions in a single-page landscape table showing, for each deal, the reported multiple, the calendarization adjustment to a December 31 reference date, the resulting calendarized multiple, and the leverage-normalized multiple. Include a notes column with a brief explanation per transaction, summary statistic rows at the bottom, and a final highlighted row positioning Vantara's implied entry multiple against the comparable set. Use color-coded row formatting to visually distinguish December fiscal year-end targets from non-December ones, and add a color legend and methodology footnotes below the table.
>
> Please save the pdf files at the Desktop.

| | |
|---|---|
| **Hidden in the files** | The WACC build document specifies how to relever beta and which discount rate to adopt. |
| **What the agent did** | It built its own cost of capital (11.2% vs 9.33%). That carried into terminal value, enterprise value ($329M vs $442M), equity value and every scenario. |
| **Why it works** | One parameter assembled from the files sets almost every number in both deliverables. The agent's own sensible approach isn't the firm's. |

---

#### E6: PAT: project cost estimate from a task sheet

**61% agent avg · 4 runs**

**Software & Data** — Inputs: Ca.png, US.pdf, Estimates.xlsx — Outputs: PAT_Cost_Estimate.pdf, Angular_Arch.png

Stumpers: **#2 Judgment at the boundary** · **#6 One early decision cascades**

**THE PROMPT** *(highlighted = where the stumper is set up)*

> Hey, I need to send the cost estimate and the initial project scaffolding for the PAT project to the client ASAP. Could you generate two files and leave them on my Desktop? Let's call them `PAT_Cost_Estimate.pdf` and `Angular_Arch.png`.
>
> When you look at `Estimates.xlsx`, completely ignore the "Dead lines" sheet since it is outdated. For estimating the tasks, our standard senior pace is 8 hours for an easy task, 24 for a medium one, and 40 for a hard one. Juniors always take twice as long. Please calculate the real hours based on who is actually doing the work. Usually, we give the medium and hard tasks to the senior developer of that area, and the easy ones to the junior. Also, do not worry about sizing the design tasks; just leave their hours blank. For the timeline, we are planning a 28-week run starting on January 1, 2026, working in standard two-week sprints. Just map the user stories sequentially based on the PDF, so US-01 goes in the first sprint, US-02 in the second one, and so on. For the rest of the team billing, the PO, QA, designer, and manager are full-time at 40 hours a week for the whole project. The architect is part-time at 20 hours a week for the full duration. We also need DevOps full-time, but only for the first month. You can find their hourly rates in the "Cost rates" sheet. Once you tally everything up, please add our standard 15 percent margin to the final number. Put all this in `PAT_Cost_Estimate.pdf`; I just need a table breaking down the tasks grouped by user story showing who does what and the sprint. Then, add a summary table showing the costs per role and the grand total before and after the margin.
>
> To make it look nice, use a color picker in `Ca.png` to grab that dark teal from the outer circle to use as the background color for the table headers.
>
> For `Angular_Arch.png`, I need a visual folder tree for Angular 19 that matches the six architectural layers shown in `Ca.png`. To keep it on brand, please extract the exact hex colors used for the six layer names at the bottom of the image and apply them to the corresponding folder text in your diagram. Add a tiny color legend in the corner too. Thanks!

| | |
|---|---|
| **Hidden in the files** | Design tasks are scattered among the developer tasks in the spreadsheet under different names ("Design landing", "Create the design for profile", ...). |
| **What the agent did** | In every run it treated several design tasks as developer work. Hours, role costs and both totals came out wrong. |
| **Why it works** | A simple rule plus messily named items is a boundary judgment on tens of rows, and every cost criterion depends on getting it right. |

---

#### E7: Fairlife: how much of the purchase price can we trace?

**64% agent avg · 6 runs**

**Finance & Accounting** — Inputs: Cola_FORM_10-K_trimmed_143k.txt, Cola_FORM_10-Q_March_2020_trimmed_35pages.pdf, Cola_FORM_10-Q_Sept_2020_trimmed_66k.txt — Outputs: Fairlife_Memorandum.pdf, Fairlife_Supporting_Calculations.pdf, Fairlife_Trace_Register.pdf

Stumpers: **#3 Knowing when to stop** · **#4 Key fact off to the side**

**THE PROMPT** *(highlighted = where the stumper is set up)*

> I'm putting together a board prep package on Coca-Cola's fairlife acquisition (closed January 2020) and could use your help with the purchase price allocation piece. The three filings we're working from are attached — the 2021 10-K plus the March and September 2020 10-Qs. Everything needs to trace back to those three documents only; audit will be checking figures against the filings, so no outside sources and no estimating around gaps.
>
> The question I'm really trying to answer for the board is: how much of the fairlife PPA can we rebuild ourselves from the public disclosures, and where are we just relying on management's numbers? Walk the consideration through from the top — cash at close, the remeasured existing stake, anything settled at closing, the earnout — and see how far the disclosures actually get you before they collapse into netted totals. Wherever that happens, don't force it; just be upfront in the memo about which figures we traced and which ones are Coca-Cola's as-reported values, including goodwill and the final allocation.
>
> Three PDFs, saved to the Desktop with these names (our indexing script is picky about filenames):
>
> Fairlife_Memorandum.pdf — the memo, including a summary table (title it "Classification Integrity Check") laying out each component, the amount, and traced vs. as-reported.
>
> Fairlife_Supporting_Calculations.pdf — the schedules behind it.
>
> Fairlife_Trace_Register.pdf — every figure mapped to its filing, note, and table (page numbers where the source format has them).
>
> And do me a favor — open the memo when you're done and eyeball the table before finalizing. The last package we sent up had it split across a page break and it looked bad. If it's doing that, fix the spacing and re-export so it fits on one page.

| | |
|---|---|
| **Hidden in the files** | The very first component, cash paid at close, is only disclosed net of cash acquired, so the independent rebuild should stop right there. |
| **What the agent did** | It kept tracing past the stop point and labelled netted or as-reported figures as "traced". Runs scored 53-75%. |
| **Why it works** | Stating the principle ("don't force it") is fine. The agent still has to find exactly where the record runs out, and it pushes on. |

---

> **Notice the pattern**
>
> None of these prompts is long or tricky. They read like normal workplace requests. The difficulty is a single decision, set up by the prompt and hidden in the files, that a smart generalist gets wrong and that the whole deliverable depends on.

---

## Domain Specific Guidance

Use these sections to choose a professional request that tests the model's reasoning, evidence handling or native application work. Keep the result useful for a real colleague. Formatting and extra outputs support the job; the decisive challenge should sit in the underlying work.

### How to use the guide

- **Choose the dependency.** Start with one source selection, interpretation or identification that materially changes the result.
- **Build a fair evidence set.** Keep every required fact and convention recoverable from the supplied files. A hard task still needs to be solvable by a domain expert.
- **Adapt and pilot.** The example briefs illustrate candidate designs, not guaranteed stumps. Their difficulty depends on the actual input files. Sections marked *Pattern to pilot* need particular care before reuse.

### Find your domain

| Domain | Start with this challenge |
|--------|--------------------------|
| Finance and Accounting | Apply the agreement before building the model |
| Software and Data | Test preservation and complete evidence |
| Design and Creative | Require visual relationships and useful editable structure |
| Engineering | Make validity and acquisition rules decide the result |
| Legal and Compliance | Test applicability rather than the presence of citations |
| Healthcare | Control the cohort and the evidence behind each status |
| Sales and Marketing | Combine brand fidelity with real campaign adaptation |
| STEM Research | Require identification before transformation |
| Multimedia and Audiovisual | Make inspection of the actual media necessary |
| Operations and Management | Make the operating basis and uncertainty matter |
| Real Estate | Use property evidence to control the underwriting |
| Government and Public Sector | Make every priority traceable to the right evidence |

> Use the current project requirements for artifact counts, allowed applications, rubric categories and weight bands. Do not copy older scoring conventions into a new task.

---

### Finance and Accounting

**Apply the agreement before building the model**

Make a financial conclusion depend on the exact definitions and documentary support in the supplied agreement or filings. A credible memo and correct arithmetic can still rest on the wrong debt population.

**Requests most worth trying**

- **Source specific carve outs.** Require debt, net debt, EBITDA and permission tests under a supplied agreement. A narrow exclusion or prerequisite should materially change the calculation, rather than merely add a footnote.
- **Reconstruction with an evidence boundary.** Ask the agent to distinguish reported amounts from reconstructed amounts and identify where the record no longer supports a calculation. Require the period, units and source locator for every material figure.
- **Dependent reconciliations.** Carry one inclusion decision through the calculation bridge and committee conclusion. The challenge is choosing and justifying the inputs, not multiplying the number of schedules.

**Requests that usually pass on their own**

- **Routine schedules.** Clean sources and uses, straightforward accretion, margin comparisons and arithmetic with explicit inputs are weak standalone challenges.
- **A familiar permission review.** Even multi filing covenant reviews can succeed when definitions and prerequisites are clear. More PDFs, polished tables and matching totals do not create difficulty on their own.

**Rubric and task guidance**

Independently verify the reference calculations. Grade the debt treatment, reconciliation and documentary sufficiency separately. Accept another well supported calculation route; do not require a particular stop location or five step framework unless the task materials establish it.

**Example prompt**

> Our treasury team needs a repurchase review. Use credit_agreement.pdf, annual_filing.pdf, interim_filing.pdf and calculation_template.xlsx to assess the available permission routes. Complete the working calculation package in LibreOffice Calc and prepare treasury_review.pdf in LibreOffice Writer. Show the components behind each material total, link figures and conclusions to their source pages or clauses, and state what the available record establishes for each route. Keep the committee conclusion tied to the completed calculation package. Save the workbook and PDF to the Desktop.

**Build the inputs this way.** Include a consequential exclusion in the agreement and enough filing detail to resolve it. The exception must be discoverable and the reference must use the same reporting period.

---

### Software and Data

**Test preservation and complete evidence**

A correct headline recommendation or a working new feature can conceal omitted evidence, changed defaults or broken behavior elsewhere. Make the existing implementation and source contract central to the job.

**Requests most worth trying**

- **Minimal changes to an existing system.** Add a feature while preserving existing enums, defaults, relationships and unrelated behavior. The recurring weakness is a broader rewrite that silently changes the original contract.
- **Complete comparative evidence.** Require all candidate benchmark rows, units, sizes, timings and constraint checks before a recommendation. A sensible winner should not substitute for an accurate comparison.
- **Evidence driven audits and builds.** Use source defined release gates or a diagram that must become an exact data model. For an interface build, test approved copy, required components and actual behavior across relevant states.

**Requests that usually pass on their own**

- **Explicit bounded repairs.** Ordinary coding fixes and deterministic filters, joins or sorts often pass. Framework choice, folder scaffolding and valid data syntax are supporting requirements.
- **A correct verdict or readable diagram.** An agent may reach DEFER or draw a clear workflow while using the wrong threshold or date. Some full coordinate and registry audits also succeed.

**Rubric and task guidance**

Check executable behavior, not just code appearance. Use regression checks for the preservation contract and inspect the requested UI states. Allow equivalent implementations when their behavior matches. A missing screenshot from evaluation is not evidence of a bad interface.

**Example prompt**

> We need waitlist support added to our booking prototype. Use booking_prototype.py, booking_model.png and change_request.docx to make the targeted update in VSCode and revise the UML diagram. Preserve the existing enum values, default attributes and current booking behavior while implementing the new entity and relationships described in the request. Save booking_updated.py, booking_model_updated.png and a short verification record to the Desktop. The record should demonstrate the new flow and confirm the existing scenarios in the change request still behave as specified.

**Build the inputs this way.** Supply a real prototype with distinctive defaults and enum values. Define the preservation contract in the change request and make every behavioral check runnable.

---

### Design and Creative

**Require visual relationships and useful editable structure**

*Pattern to pilot* — Test the exact files and failure mechanism before reuse.

Prefer precise composition, material behavior and layered editing over a generic request for attractive artwork. Fine visual work is worth piloting, but reference based scene construction can still score highly.

**Requests most worth trying**

- **Layered composition.** Combine photography, masks, transparency and overlapping elements. Require clean subject edges, intentional depth and the specified relationship between foreground, typography and background.
- **View dependent fidelity.** Distinguish elevated frontal from overhead views, preserve grain direction and camera framing, and keep those properties through compositing. A plausible render may depict the wrong geometry.
- **Native editability.** Ask for text, subjects, backgrounds and treatments to remain independently editable. A flattened image can look acceptable while being unusable for the client revision.

**Requests that usually pass on their own**

- **Simple design treatments.** Basic geometric shapes plus text, recoloring, ordinary frontal renders and readable client summaries are weak standalone challenges.
- **From scratch as the only difficulty.** Removing a starting model or textures is not sufficient. Even scenes built from reference renders can pass; focus on the details the agent actually misses.

**Rubric and task guidance**

Define the target with clear supplied references. Grade camera relationships, masks, material appearance and editability directly. Do not demand a hidden node graph or exact transforms from an approximate brief. Use objective dimensions where specified and allow reasonable visual tolerances elsewhere.

**Example prompt**

> Please finish our lounge chair presentation using lounge_scene.blend, client_revision_notes.txt, approved_views.png and wood_texture.png. In Blender, apply the client revisions and produce the frontal, elevated frontal and low frontal views shown in the approved reference. Preserve the visible wood grain direction and full scene framing in each view. Save the revised scene and transparent renders to the Desktop. Use GIMP to assemble the client comparison sheet, keeping each render and its labels editable, and export client_views.pdf from that project.

**Build the inputs this way.** Make the elevated view genuinely distinct from overhead, and show the important material and silhouette details clearly. Supply enough reference information for an expert to reproduce the result.

---

### Engineering

**Make validity and acquisition rules decide the result**

Textbook calculations, dimensioned drawings and chart styling often work well. Stronger tasks require the agent to interpret the acquisition chain, distinguish equipment values or recognize when a requested metric is not valid.

**Requests most worth trying**

- **Manual specific measurement interpretation.** Require source defined signs, timing alignment, conformance checks and action codes. A correct formula can still use the wrong lag or measurement basis.
- **Not evaluable conditions.** Use a documented adjacency, acquisition or scope rule that determines whether a metric may be calculated. Require full asset coverage, including passing records, rather than only a failure list.
- **Rendered evidence with technical precedence.** A legible nameplate image and nearby operating text can supply different values. Make the engineering context determine which governs sizing, with that choice carried into the recommendation.

**Requests that usually pass on their own**

- **Conventional numerical analysis.** Explicit fatigue, process and lifting risk calculations can succeed, even with several dependent formulas and drawings.
- **Routine presentation.** Familiar formulas, orderly reports, chart labels and readable risk plots usually pass. Adding nondefault settings without a meaningful engineering consequence is insufficient.

**Rubric and task guidance**

Verify the sign convention, units and reference timing independently. Separate acquisition validity, numerical result and action. Keep mixed PDF evidence readable to a human. A live interface idea needs a supported environment and recorded state evidence before it becomes a usable task.

**Example prompt**

> Our QA team needs to decide which RF array findings require action. Use array_measurements.csv, acquisition_manual.pdf and array_review_template.xlsx to complete the review in LibreOffice Calc. Apply the manual to the measurements and report the required results and conformance status for every array element. Prepare array_actions.pdf in LibreOffice Writer with the basis for each recommended action and the applicable manual references. Save the completed workbook and PDF to the Desktop, with the report using the same reviewed results as the workbook.

**Build the inputs this way.** Include the manual defined scope condition that governs phase coherence, with sufficient acquisition evidence to resolve it. Do not place the exception answer in the prompt.

---

### Legal and Compliance

**Test applicability rather than the presence of citations**

Make the agent apply a controlling provision to specific facts. The meaningful distinction is between an established obligation, a conditional obligation and a conclusion the available evidence cannot support.

**Requests most worth trying**

- **Conditional legal applicability.** Require issue level decisions under supplied provisions, including the factual predicate, relevant exception and missing information. General legal principles may be close but still produce the wrong classification.
- **Finding to operational action.** Carry each classification into notification, investigation, hold or other action. A chart or checklist should derive from those classifications rather than a separate generic summary.
- **Legal reasoning with visual evidence.** As a pattern to pilot, reconstruct a witness based scene or relevant evidence extract using a supplied visual template. Spatial direction and placement must follow the case record.

**Requests that usually pass on their own**

- **Authorities and checklist structure.** Listing the right family of statutes, populating named headers and sorting records do not establish correct applicability.
- **Routine drafting and clear eligibility joins.** Conventional claims, evidence summaries and explicit multi source eligibility checks can succeed. Legal vocabulary and extra sources are not enough.

**Rubric and task guidance**

Validate the legal outcome against the supplied authorities. Grade applicability separately from citation accuracy and presentation. Accept defensible conditional wording. Ensure the expected workbook follows explicit requests such as filters; do not reject them because a reference omitted them.

**Example prompt**

> Prepare a compliance triage package for the property described in hazards.docx using the supplied regulatory_extracts.pdf and checklist_template.xlsx. In LibreOffice Writer, assess each issue under the attached provisions and explain the supporting facts, controlling section and resulting action. Complete the linked checklist in LibreOffice Calc so the status fields and summary chart reflect the memo findings. Keep established conclusions distinct from those that depend on further facts. Save property_memo.docx and property_checklist.xlsx to the Desktop.

**Build the inputs this way.** Use realistic differences in substance identity, quantity or release status that change applicability. The reference must justify each classification; a preferred memo is not proof that alternatives are wrong.

---

### Healthcare

**Control the cohort and the evidence behind each status**

Build difficulty around data coverage, response thresholds and evidence mapping. A clean leadership deck or well formed evidence file can still communicate an incorrect population or unsupported finding.

**Requests most worth trying**

- **Daily scope and escalation.** Require the correct monitoring episode, day boundaries and aggregation rules before classifying an emergency. One extra day or a wrong threshold can change every communication artifact.
- **Semantic mapping and query evidence.** Map source clinical data to the requested model at a consistent grain. Require evidence for each orphan link or grain mismatch check, with counts reconciled to the governance memo.
- **Rendered corrections and evidence qualification.** As a pattern to pilot, use a visible approved correction or withdrawal convention that changes which records apply. For synthesis, preserve conditions on each relationship rather than inventing conflicts between different exposures.

**Requests that usually pass on their own**

- **Clear descriptive analysis.** Well specified counts, pooled trends, epidemiological charts and image derived data extraction can succeed together.
- **Communication structure.** Section order, legible diagrams, clean pagination and generic cautions are weaker challenges than cohort definition or evidence transformation.

**Rubric and task guidance**

Keep a single reviewed table behind the charts and summaries, then check that table against the sources. For mapping tasks, allow equivalent valid SQL and inspect results at the required grain. Visible status conventions must be unambiguous and defined in the supplied workflow.

**Example prompt**

> Hospital leadership needs a wildfire smoke activation review. Use monitor_export.csv, activation_policy.pdf and incident_review_template.xlsx to assess the episode recorded in the export. Complete the daily analysis and activation findings in LibreOffice Calc, then prepare leadership_smoke_review.pptx in LibreOffice Impress using the reviewed table and chart. Explain the basis for each activation finding under the policy and preserve the episode dates across both files. Save smoke_review.xlsx and the presentation to the Desktop.

**Build the inputs this way.** Give the episode a documented coverage boundary and a consequential threshold case. Every day and classification in the reference must follow the export and policy.

---

### Sales and Marketing

**Combine brand fidelity with real campaign adaptation**

*Pattern to pilot* — Test the exact files and failure mechanism before reuse.

Use a campaign task that must preserve approved content and adapt it to different placements. Routine sales writing and small identifier traps are weak starting points for the stronger model.

**Requests most worth trying**

- **Brand system versus layout reference.** Require the agent to apply the controlling palette and typography while using a separate image for composition. It must preserve the brand rules without copying the reference placeholder content.
- **Exact approved copy across placements.** Adapt the design for feed and Story formats while retaining the approved wording, audience action and destination. Merely resizing or cropping the first output should not satisfy the brief.
- **Editable campaign elements.** Keep logos, subjects, text and decorative treatments individually editable. Check the native project; a flattened zone composite does not provide the same revision capability.

**Requests that usually pass on their own**

- **Conventional commercial follow up.** Supported product to need connections, freight emphasis, qualified messaging and clear next steps can pass, even in a long sales package.
- **Basic campaign packaging.** Readable text, canvas dimensions, recognizable subjects and a visible call to action are supporting checks. Simple missing fields or punctuation differences are not reliable hardening.

**Rubric and task guidance**

Keep the approved copy and brand hierarchy unambiguous. Score visual fidelity, placement adaptation and element editability separately. Avoid subjective labels such as retro as the only acceptance condition, and do not invent a preferred campaign style in the expected file.

**Example prompt**

> Create our launch feed and Story artwork in GIMP using campaign_brief.pdf, approved_copy.docx, brand_kit.zip, brand_guide.pdf and layout_reference.png. Follow the brand guide and use the reference for composition. Keep the approved wording intact and recompose for each placement described in the brief. Retain the logo, subjects, individual text elements and decorative treatments as meaningful editable layers. Save launch_feed.xcf, launch_story.xcf and their PNG exports to the Desktop.

**Build the inputs this way.** Show the brand rules in usable references and include enough source artwork to build both placements. Make the adaptation require a genuine composition change, not a canvas size change.

---

### STEM Research

**Require identification before transformation**

Precise scientific identity and analytical scope are stronger challenges than sophisticated terminology. The model can make an excellent looking plot or scene while identifying the wrong structure or omitting a relevant observation.

**Requests most worth trying**

- **Anatomical identity and spatial assembly.** Ask for missing or foreign bones, specimen identity and coherent placement from unlabeled geometry. Carry those identities into the editable scene, labels and structured record.
- **Complete analytical scope.** Require all relevant peaks, characters or observations under a supplied definition. A missed second peak should have a visible effect on the signed differences, summary and scientific interpretation.
- **Identity across representations.** Resolve similar sequences or structures across source files, then preserve the correct identity in character states, tables and figures. Require claims to stay within what the source paper reports.

**Requests that usually pass on their own**

- **Explicit numerical and plotting workflows.** Calibration audits, standard data processing, ordinary plot construction and routine rounding often pass.
- **3D work with clear interpretation.** Some protein reconstructions match the supplied views perfectly. Readable scientific figures, color systems and model screenshots do not prove the underlying identification is hard.

**Rubric and task guidance**

Define peak and character conventions in the inputs, not through an unseen answer key. Grade identity, spatial placement and downstream calculations separately. For editable scenes, avoid arbitrary mesh counts; for live workbooks, change an input and confirm the calculation updates.

**Example prompt**

> Please recatalog the hand scans in collection_1.zip, collection_2.zip and collection_3.zip using the conventions in archive_notes.pdf. In Blender, assemble the supplied bones into an anatomically coherent hand and determine which bones are missing. Add clearly distinguished placeholders where needed. Save hand_archive.blend and a labeled anterior and posterior overview PDF to the Desktop, along with missing_bones.csv. Keep the identities and placements in the scene consistent with the labels and archive record.

**Build the inputs this way.** Use distinguishable unlabeled scans and enough geometry to establish which bones are absent. Neutral filenames should not give away the answer, but the shapes must support an expert identification.

---

### Multimedia and Audiovisual

**Make inspection of the actual media necessary**

*Pattern to pilot* — Test the exact files and failure mechanism before reuse.

Build an editorial or production task, not a research summary with a video filename attached. Stronger candidates require checking the timeline, fitting source media into a supplied graphic and carrying verified facts into the finished segment.

**Requests most worth trying**

- **Timeline defects.** Use source footage with realistic flash or black frames, timing problems or inherited edit defects. Require a broadcast ready result that depends on frame level inspection.
- **Template fit and source style.** Place an image inside the intended graphic region without covering banners or other content. Use a clear visual charter where matching the palette, hierarchy and fit requires inspection.
- **Source based editorial corrections.** Compare an as aired script with the authoritative release, establish the broadcast date from the record and carry corrections into the script, graphics and edit log.

**Requests that usually pass on their own**

- **Research and extraction alone.** Reading a PDF, explaining a topic or creating several independent summaries is weak and may not require audiovisual expertise.
- **Clean graphics without semantic checks.** A map can have a consistent legend and recognizable geography while shading the wrong data bucket. Routine visual packaging is not a substitute for editorial correctness.

**Rubric and task guidance**

Check the rendered segment at relevant frame boundaries and compare the saved project with the export. Grade graphic fit, factual corrections and timeline defects separately. Use defined safe areas and source dates; do not impose an unstated font or pixel exact layout from the expected file.

**Example prompt**

> We need a corrected version of the recorded science bulletin. Use aired_segment.mp4, aired_script.docx, official_release.pdf, bulletin_graphic.png and broadcast_style.pdf to prepare the correction in Shotcut. Reconcile the segment with the release, update the script and graphics to the supplied style, and deliver a broadcast ready edit. Save corrected_bulletin.mp4, its editable project and corrections_log.docx to the Desktop. The log should identify each correction, its source and where it appears in the revised segment, using the broadcast date from the record.

**Build the inputs this way.** Provide a discoverable source discrepancy and genuine timeline defects. The files must contain enough source media and graphic information to repair them without guessing.

---

### Operations and Management

**Make the operating basis and uncertainty matter**

A polished plan can contain an unjustified exact figure. Make the requested allocation or schedule depend on whether the source records support a unique answer and on the organization rules that govern the work.

**Requests most worth trying**

- **Underdetermined cohorts.** Use overlapping source categories that do not establish a unique headcount. Ask for the operational baseline and let the evidence determine whether the answer is a point value, range or unresolved item.
- **Rule order and working calendars.** As patterns to pilot, combine exclusions, ordering dependencies or a holiday calendar with a scheduling or enumeration task. One rule must be applied before the next calculation is meaningful.
- **Plans versus execution.** Compare a proposed process with evidence of what actually occurred. Preserve unconfirmed actions and unresolved gaps rather than treating a plan as proof of completion.

**Requests that usually pass on their own**

- **Explicit operational arithmetic.** Daily reserves, percentage calculations, ordinary lot disposition and replenishment calculations can succeed.
- **Direct instructions about missing inputs.** An explicit instruction to leave a deficit uncalculated is often followed. Generic plans, filled forms and readable kickoff slides are also weak standalone challenges.

**Rubric and task guidance**

Verify the source of uncertainty before requiring a range. Grade the supported population separately from the derived per capita allocation. For scheduling, define calendar and date conventions in the inputs. If preserving comments or native document structure matters, ask for it and inspect it directly.

**Example prompt**

> We need the contingency baseline for our service team. Use service_population.pdf, allocation_rules.docx and reserve_tracker.xlsx to establish the supported caller headcount and per caller allocation. Complete the working baseline in LibreOffice Calc and prepare contingency_brief.pdf in LibreOffice Writer with the basis for the figures, the applicable look back period and the implications for coverage. Follow the allocation rules and retain the tracker structure. Save the updated workbook and brief to the Desktop.

**Build the inputs this way.** Include overlapping categories with documented totals but no record that resolves their overlap. The reference should derive the valid bounds rather than invent an exact cohort.

---

### Real Estate

**Use property evidence to control the underwriting**

*Pattern to pilot* — Test the exact files and failure mechanism before reuse.

Start with a property specific reconciliation, then pilot it. Transfer the stronger financial and evidence boundary patterns to leases, rent rolls and plans rather than assuming a familiar underwriting model will be difficult.

**Requests most worth trying**

- **Lease hierarchy and effective periods.** Reconcile a rent roll with leases and amendments. A concession, start date or superseding term should change recognized rent and the investment conclusion.
- **Area and unit identity.** Resolve rentable versus usable area and unit identifiers from a supplied plan and measurement policy. Carry the selected area basis into normalized rents and comparable metrics.
- **A supportable investment conclusion.** Separate documented income and expenses from assumptions. Make the evidence determine whether an exact valuation is supported or a range and open diligence item are appropriate.

**Requests that usually pass on their own**

- **Routine underwriting candidates.** Clean rent roll arithmetic, explicit cap rate formulas, tidy comparable tables and generic property summaries are weak standalone choices.
- **More documents without a decisive dependency.** Several brochures or a long investment memo do not create difficulty if the values are already resolved. Keep the challenge in a lease, area or evidence decision.

**Rubric and task guidance**

Choose one consequential property interpretation and verify it independently. Make amendment precedence, area definitions and valuation conventions recoverable from the inputs. Grade the source selection, income bridge and conclusion separately; accept a defensible range where the evidence permits one.

**Example prompt**

> Please prepare the acquisition review for our small office property. Use rent_roll.xlsx, lease_and_amendment_pack.pdf, floor_plan.png and underwriting_policy.docx to complete the rental income and area analysis in LibreOffice Calc. Prepare acquisition_review.pdf in LibreOffice Writer with an auditable bridge from the property records to the underwriting and investment conclusion. Include the source locators for material lease terms and area measurements. Save property_underwriting.xlsx and the PDF to the Desktop.

**Build the inputs this way.** Build a realistic amendment and area basis that materially affect the underwriting. This is a pattern to pilot; do not treat it as a proven recipe or remove information needed to resolve the property facts.

---

### Government and Public Sector

**Make every priority traceable to the right evidence**

Use decision relevant synthesis with the correct population, construct and denominator. A readable committee briefing can still substitute a plausible general recommendation for the findings the source record actually supports.

**Requests most worth trying**

- **Claims with exact supporting evidence.** Require each material finding and proposed action to carry the correct source and page. Distinguish what a report found from what the briefing recommends.
- **Subgroups and measurement constructs.** As a pattern to pilot, require age, usage or geographic breakdowns that affect resource priorities. The outcome coding and denominator must remain consistent across calculations.
- **Unresolved rule exceptions.** Require an exception ledger where a policy hierarchy depends on missing facts. A mostly correct allocation or seating audit can still omit the unresolvable case.

**Requests that usually pass on their own**

- **Headline facts and conventional caveats.** Straightforward counts, selected correlations and ordinary limitations often pass. A generic timeless recommendation is weak difficulty.
- **Basic briefing and rule audit structure.** Slide counts, checklist organization, readable tables and much of an explicit hierarchy audit can succeed. Multiple sources alone do not make synthesis hard.

**Rubric and task guidance**

Grade source fidelity and action support, not one preferred wording or list. Permit alternative priorities justified by the evidence. Do not demand an unannounced source order, tagline or subtitle. Define the decision horizon in the brief if immediate response and long term prevention must be distinguished.

**Example prompt**

> Our education committee needs a learning recovery briefing. Use district_findings.pdf, program_review.pdf, committee_request.docx and action_checklist.xlsx to prepare the requested deck in LibreOffice Impress and complete the checklist in LibreOffice Calc. Organize the findings around the committee questions and connect each proposed action to the supporting finding and page. Keep source findings distinct from recommendations and carry the same evidence into both deliverables. Save learning_recovery.pptx and action_checklist_completed.xlsx to the Desktop.

**Build the inputs this way.** Select sources with related but distinct populations and findings. The request should define the policy questions, while leaving room for more than one well supported action list.
