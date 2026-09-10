# Orangutan Encyclopedia Prompt Writing Handbook

**Domain and Application Examples for Attempters**

## Purpose

This guide shows how to write realistic prompts that naturally require meaningful application work. The goal is not to tell the model to use a GUI. The goal is to request final artifacts whose visual, spatial, temporal, or application-native requirements are extremely difficult to satisfy well without using the intended application and GUI actions

The applications listed in each domain are what we have available at the moment in the virtual machine. Let's make sure to make the most of these apps!

**Core requirements in every example:** at least three named inputs; exact output filenames; all outputs saved to the Desktop; application work tied to verifiable final artifacts.

---

## Contents

1. Non-negotiable prompt rules
2. How to create indirect GUI pressure
3. Input, output, and source requirements
4. A reusable prompt structure
5. Domain and application examples
6. Final attempter checklist

---

## 1. Non-negotiable prompt rules

**Create indirect GUI pressure**

Describe an output that is hard to produce correctly without visually working in the relevant application. Examples include matching a supplied template, laying out a diagram, fitting a chart without clipping, arranging a PCB, segmenting anatomy, timing video overlays, or preserving comments and tracked changes. Do not write instructions such as 'use the GUI' or 'do this manually.'

**Use at least three named inputs**

Every prompt must reference at least three input files by filename. Mention them in natural prose and explain what each contributes. Filenames make the task and its sources verifiable.

**Name every output**

Every deliverable needs an exact filename and extension. The primary deliverable must never be described only as 'the report,' 'the deck,' or 'the analysis.'

**Save all outputs to the Desktop**

End the deliverable request by stating that all final output files must be saved to the Desktop.

**Design for output-only verification**

Only the final output files are verified. Any browsing, visual inspection, playback, rendering, or application interaction should improve a result that is visible in an output. A temporary UI state is not evidence unless the prompt asks for a meaningful screenshot or exported artifact as a deliverable.

**Use Chrome for stable sources**

Browser research should target stable, versioned sources: a specific SEC filing, a dated government report, a standards edition, a tagged software release, a DOI, or a versioned arXiv paper. Avoid live dashboards, changing homepages, current prices, rolling rankings, or anything described only as 'latest.'

**Keep the request natural**

Write like a colleague asking for work. State the decision, audience, source materials, constraints, and deliverables. Avoid artificial personas, evaluator language, hype, answer-key values, or a line-by-line rubric disguised as a prompt.

---

## 2. How to create indirect GUI pressure

### The design principle

Do not instruct the model to "use the GUI." Instead, make the output depend on visual judgment, spatial arrangement, application-native behavior, or interpretation of a visual source. The GUI interaction is a means to a better final artifact, not necessarily the deliverable by itself.

### Strong ways to create GUI pressure

**Template matching**
Supply an image, board, schematic, or visual reference and require the final artifact to preserve its hierarchy, spacing, styles, or structure.

**Diagram construction**
Require a flowchart, system diagram, logic circuit, process map, network, or annotated image whose layout and relationships are visible in the final output.

**Chart and figure layout**
Require readable legends, non-overlapping labels, meaningful axes, visible thresholds, correct ordering, or a multi-panel arrangement matched to a reference.

**Visual interpretation**
Provide screenshots, scans, maps, medical images, drawings, footage, or reference renders that must be interpreted to produce the final artifact.

**Rendered media**
Require a finished image, video, audio mix, score, 3D render, CAD drawing, board export, or presentation where visual or temporal quality is part of correctness.

### Weak or unverifiable GUI hooks

- 'Open the file and look at it' without requiring any visible change in an output.
- 'Use Excel/PowerPoint/Blender' when the same deliverable could be produced without any application-specific visual work.
- A screenshot used only as proof that an application was opened.
- A vague instruction to 'make it professional' with no reference, audience, hierarchy, or observable layout requirement.
- A visual check whose result is not reflected in a saved output.

---

## 3. Input, output, and source requirements

### Inputs

Every prompt must mention at least three input files by filename. Describe them naturally: "Use the audited statements in FY2023_10K.pdf, the maturity schedule in Debt_Maturities.xlsx, and the memo structure in Treasury_Memo_Template.docx." Do not hide the filenames behind vague phrases such as "the attached files."

### Outputs

- Give every output an exact filename and extension.
- Name the primary output explicitly; do not rely on metadata or task setup to identify it.
- Save every final output to the Desktop.
- Choose outputs that preserve the work being evaluated: a formatted DOCX, a PPTX with the required layout, a workbook with formulas and chart objects, a PDF drawing, a rendered PNG, an MP4, an audio master, or a ZIP containing native project files.
- When temporary application work matters, make its result visible in a final output. For example, a Blender scene can be verified through a render set or annotated PDF; an MPV review can be verified through a timestamped QC log and contact sheet.

### Chrome and stable web sources

- Use exact, stable sources: a versioned arXiv URL, DOI page, dated government PDF, fixed SEC filing accession, tagged software documentation, standards edition, or archived public record.
- State which fixed source should be consulted and what information should be carried into the output.
- Avoid "current," "latest," live dashboards, changing prices, rolling leaderboards, mutable wiki pages, and undated homepages.
- The browser lookup should add data, evidence, citations, or reference material to a final deliverable; browsing alone is not the task.

---

## 4. A reusable prompt structure

1. **Context and decision** — Explain what is happening, who needs the work, and what decision or outcome it supports.
2. **Named source files** — Mention at least three filenames in natural prose and explain the role of each source.
3. **Core work** — Describe the analysis, design, synthesis, editing, or modeling goal without revealing the answer or dictating every step.
4. **Application-shaped artifact requirements** — Add visual, spatial, temporal, or native-format requirements that are visible in the final output.
5. **Named deliverables and Desktop save** — Specify every filename, extension, and the requirement to save all outputs to the Desktop.

### Compact example

> "Use the operating data in Weekly_Demand.xlsx, the staffing rules in Staffing_Constraints.pdf, and the dashboard structure in Capacity_Template.xlsx to build a weekly capacity plan. Show the Base and Surge scenarios, keep the gap chart labels readable, and make the summary print on one landscape page. Save the model as Q4_Capacity_Plan.xlsx and the summary as Q4_Capacity_Summary.pdf. Save both outputs to the Desktop."

---

## 5. Domain and application examples

Each example below follows the same baseline: three or more named inputs, output requirements that create indirect GUI pressure, exact output filenames, and a Desktop save requirement. The examples are starting points; task authors should adapt the facts, filenames, and complexity to the actual source package.

### 5.1. Finance & Accounting

*Treasury, financial reporting, audit support, budgeting, forecasting, controls, and executive decision support.*

| Application and prompt design | Example ideas |
|---|---|
| **Chrome**<br>Best for: Researching fixed-period financial facts from authoritative, stable records.<br>GUI pressure: Require source reconciliation and citations in the final memo, using a specific filing accession or dated publication. | I'm reviewing how several companies disclosed their debt positions before a portfolio risk meeting. The companies, target fiscal years, and CIK numbers are listed in Issuer_Review_List.xlsx. Use the calculation definitions in Debt_Review_Guide.pdf and record your findings in the structure provided by Debt_Review_Template.xlsx.<br><br>For each company, locate the specified Form 10-K on SEC EDGAR. Work through the filing and its filing-detail page to identify the accession number, reporting period, auditor, debt carrying value, current portion of long-term debt, future maturity schedule, and the principal interest-rate terms disclosed in the debt note.<br><br>Review the linked exhibit list as well and identify whether the filing includes the credit agreement or an amendment relevant to the reported debt.<br><br>Reconcile the EDGAR findings with any figures already included in the issuer list and clearly flag differences rather than silently replacing them. Include the filing accession number, document name, relevant section or note, and source page link for every company.<br><br>Save the completed tracker as Debt_Disclosure_Review.xlsx and a concise portfolio summary as Debt_Disclosure_Findings.docx. Save both files to the Desktop. |
| **Excel/Sheets**<br>Best for: Financial models, reconciliations, scenario analysis, print layout, pivots, and editable charts.<br>GUI pressure: Use a supplied workbook structure and require formulas, print areas, chart labels, and visible scenario controls in the final workbook. | Build the FY2027 operating forecast from FY2024_Actuals.xlsx, Department_Assumptions.xlsx, and Forecast_Model_Template.xlsx. Preserve the template's sheet order and input-cell conventions, add Base, Downside, and Upside scenarios, and create an executive dashboard with revenue, EBITDA, cash runway, and headcount. The dashboard must print on one landscape page, with no clipped columns, and its variance chart must keep every data label readable. Save the model as FY2027_Operating_Forecast.xlsx and export the dashboard as FY2027_Forecast_Dashboard.pdf. Save both files to the Desktop. |
| **Word/Docs**<br>Best for: Audit memos, accounting-policy analyses, control narratives, and board-ready written conclusions.<br>GUI pressure: Supply a document template and require page-level formatting, comments, cross-references, or tracked revisions that remain in the output. | Use Revenue_Recognition_Policy.pdf, Contract_Sample_Set.xlsx, and Accounting_Memo_Template.docx to assess whether the sampled contracts follow the company's revenue-recognition policy. Complete the template as Revenue_Recognition_Assessment.docx, keeping the conclusion section on the first page and adding a resolved comment to each item that needs controller review. Include a concise exception table and cross-reference each exception to the source contract ID. Also save a clean PDF as Revenue_Recognition_Assessment.pdf. Save both outputs to the Desktop. |
| **PowerPoint**<br>Best for: Board and committee presentations that translate financial analysis into a clear visual story.<br>GUI pressure: Use a supplied deck or brand template and require charts, tables, callouts, and alignment that are visible in the final presentation. | Create a four-slide covenant briefing using Covenant_Calculations.xlsx, Credit_Agreement.pdf, and Board_Deck_Template.pptx. Keep the supplied theme and slide master, show the covenant headroom trend as an editable chart, and build a maturity timeline that clearly separates fixed-rate and floating-rate debt. The key-metrics table must use at least 14-point text and fit without overflow. Save the finished deck as Covenant_Risk_Briefing.pptx and a presentation-ready PDF as Covenant_Risk_Briefing.pdf. Save both files to the Desktop. |

**Things to avoid in this domain**

- Do not provide the ratios, totals, or recommendations the agent is supposed to derive.
- Do not rely on live market prices or an undated "current" filing; identify a specific filing or reporting period.
- Do not make the spreadsheet the only output when the task also requires interpretation for decision-makers.

---

### 5.2. Software & Data

*Software engineering, API and database work, data analysis, system integration, cloud architecture, and technical reporting.*

| Application and prompt design | Example ideas |
|---|---|
| **Chrome**<br>Best for: Consulting versioned API documentation, standards, tagged releases, and archived technical references.<br>GUI pressure: Tie browsing to a fixed release or version and require the findings to appear in a migration matrix or technical specification. | We are documenting whether several assumptions in our legacy HTTP gateway are still supported by the current protocol standards. The assumptions and affected gateway behaviors are in Legacy_HTTP_Assumptions.xlsx, the production issues are summarized in Gateway_Defect_Log.docx, and the review format is provided in Protocol_Review_Template.xlsx.<br><br>Use the RFC Editor website to investigate RFC 9110, RFC 9111, and RFC 9112. For each document, review its publication information, status, relationships to earlier RFCs, and any linked errata. Determine which gateway assumptions remain supported, which rely on an obsolete specification, and which need qualification because of a verified or held-for-update erratum.<br><br>Each conclusion should identify the applicable RFC and section, the relevant erratum when one exists, and the gateway behavior affected. Do not treat every reported erratum as authoritative without checking its status.<br><br>Save the completed standards matrix as HTTP_Standards_Review.xlsx and the remediation brief as HTTP_Gateway_Standards_Brief.docx. Save both outputs to the Desktop. |
| **VSCode**<br>Best for: Editing and testing codebases, debugging UI behavior, and packaging reproducible fixes.<br>GUI pressure: Pair code changes with a rendered application result or test report that exposes whether the implementation is visually and functionally correct. | Repair the dashboard project in Analytics_Dashboard_Source.zip using Test_Defect_Report.txt and Dashboard_Reference.png. Fix the data-loading and responsive-layout defects without changing the public API, add or update tests for the reported defects, and make the rendered dashboard match the reference hierarchy at desktop and tablet widths. Save the corrected project as Analytics_Dashboard_Fixed.zip, the test results as Analytics_Dashboard_Test_Report.pdf, and the final tablet render as Analytics_Dashboard_Tablet.png. Save all three outputs to the Desktop. |
| **pgAdmin**<br>Best for: Database inspection, SQL validation, data-quality analysis, and relationship visualization.<br>GUI pressure: Require an ERD, query result reconciliation, or schema comparison whose relationships and layout are visible in exported outputs. | Review the customer-order schema using commerce_schema.sql, Data_Dictionary.xlsx, and ERD_Layout_Reference.png. Identify orphaned records, inconsistent foreign keys, and indexes needed for the three slow queries documented in slow_queries.txt, then prepare a corrected migration script. Arrange the final entity-relationship diagram to match the reference grouping and keep all relationship labels readable. Save the diagram as Commerce_ERD.png, the findings as Commerce_Database_Audit.pdf, and the migration package as Commerce_Schema_Fixes.zip. Save all outputs to the Desktop. |
| **R Studio**<br>Best for: Statistical modeling, reproducible analysis, diagnostics, and publication-quality reports.<br>GUI pressure: Use a report template and reference plots; require faceting, annotations, diagnostics, and output formatting visible in the final report. | Analyze churn using Customer_Churn.csv, Analysis_Plan.pdf, and Churn_Report_Template.docx. Compare at least two defensible classification approaches, document preprocessing choices, and evaluate calibration as well as discrimination. Recreate the diagnostic layout shown in Churn_Plot_Reference.png, with readable facet labels and no overlapping annotations. Save the report as Churn_Model_Assessment.docx, the scored records as Churn_Scored_Customers.csv, and the diagnostic figure as Churn_Diagnostics.png. Save all three outputs to the Desktop. |
| **LabPlot**<br>Best for: Layered scientific or technical plotting from structured data.<br>GUI pressure: Require a specific multi-layer composition, legend placement, annotations, or reference match in the exported figure. | Create a performance figure from api_latency.csv, deployment_events.csv, and Plot_Style_Reference.png. Show p50, p95, and p99 latency on aligned panels, annotate the two deployment windows, and include the error-rate series on a clearly labeled secondary view without obscuring the latency data. Match the reference's typography and panel spacing. Save the final figure as API_Performance_Timeline.png and a one-page interpretation as API_Performance_Notes.pdf. Save both outputs to the Desktop. |
| **Octave**<br>Best for: Numerical analysis, simulation, signal processing, and technical figure generation.<br>GUI pressure: Require a simulation result with visually checked axes, threshold crossings, annotations, and comparison against a supplied reference. | Evaluate the queue-control model using arrival_rates.csv, controller_parameters.xlsx, and Queue_Model_Equations.pdf. Simulate the baseline and two alternative control settings, identify the stability boundary, and compare the response to Target_Response_Reference.png. The final figure must show the threshold crossing, settling time, and overshoot with non-overlapping annotations. Save the analysis as Queue_Control_Assessment.pdf, the simulation outputs as Queue_Control_Results.csv, and the figure as Queue_Control_Response.png. Save all outputs to the Desktop. |

**Things to avoid in this domain**

- Do not assign a persona such as "act as a senior engineer." State the system problem directly.
- Do not turn a technical-writing task into Software & Data unless code, queries, a database, or analytical tooling is genuinely required.
- Do not specify the exact implementation when several sound solutions are possible; specify compatibility, behavior, and constraints.

---

### 5.3. STEM Research

*Scientific literature review, quantitative analysis, modeling, visualization, citation management, circuits, geometry, and medical-image research.*

| Application and prompt design | Example Ideas |
|---|---|
| **Chrome**<br>Best for: Finding stable scientific sources such as DOI records, versioned arXiv papers, or archived datasets.<br>GUI pressure: Require exact source versions and integrate evidence into a final literature table or synthesis. | I'm preparing a research-history briefing on three influential machine-learning papers. The target arXiv identifiers and the versions we are interested in are listed in Paper_Version_Targets.xlsx. Use Evidence_Coding_Guide.pdf to classify changes and build the final visual in Literature_Map_Template.pptx.<br><br>On arXiv, locate each target paper and work through its abstract page, submission history, earlier versions, author information, subject classifications, and journal-reference or DOI information where available. Compare the first submitted version with the version named in the target workbook and identify meaningful changes in the paper's title, abstract framing, stated scope, authorship, or publication information.<br><br>Distinguish substantive research-framing changes from minor metadata or wording updates. For each paper, state which version should be cited for the purpose described in the coding guide and preserve the exact arXiv version identifier.<br><br>Save the version comparison as Arxiv_Version_Review.xlsx and the completed visual research map as Research_Evolution_Map.pptx. The map should clearly connect each paper's versions without overcrowding the timeline. Save both files to the Desktop. |
| **Octave**<br>Best for: Mathematical simulation, numerical methods, and model comparison.<br>GUI pressure: Require an annotated technical figure and a reproducible results table, with visible agreement or deviation from a reference solution. | Model the damped oscillator using experiment_run.csv, Oscillator_Parameters.xlsx, and Numerical_Methods_Notes.pdf. Compare two suitable integration methods across the supplied step sizes, quantify numerical error, and explain where the methods diverge. Match the plot arrangement in Figure_Layout_Reference.png and label the region where error growth becomes material. Save the report as Oscillator_Numerical_Study.pdf, the results as Oscillator_Error_Table.csv, and the figure as Oscillator_Method_Comparison.png. Save all outputs to the Desktop. |
| **R Studio**<br>Best for: Experimental analysis, ecological and biomedical statistics, and reproducible reporting.<br>GUI pressure: Use a protocol and report template; require a publication-style figure with visible uncertainty and grouping choices. | Analyze the field experiment using Growth_Measurements.csv, Study_Protocol.pdf, and Manuscript_Results_Template.docx. Apply the protocol's exclusion and grouping rules, compare treatment effects with an appropriate model, and report effect sizes with uncertainty. Build the main figure to match Journal_Figure_Reference.png, including panel labels, confidence intervals, and readable species names. Save the completed section as Growth_Study_Results.docx, the analysis table as Growth_Model_Results.csv, and the figure as Growth_Treatment_Effects.png. Save all outputs to the Desktop. |
| **GeoGebra**<br>Best for: Geometric construction, proof support, coordinate relationships, and visually constrained diagrams.<br>GUI pressure: Require a precise construction whose incidences, labels, and measurements are visible in an exported diagram. | Reconstruct the mechanism geometry from Linkage_Dimensions.pdf, Constraint_Table.xlsx, and Linkage_Reference_Diagram.png. Build the constrained four-bar linkage, identify the reachable range of the coupler point, and mark the two limiting configurations. The exported diagram must show all named points, key dimensions, and the traced coupler path without label collisions. Save the construction summary as Four_Bar_Linkage_Analysis.pdf and the final diagram as Four_Bar_Linkage_Geometry.png. Save both outputs to the Desktop. |
| **LabPlot**<br>Best for: Publication-quality plots for spectra, time series, and multi-condition experiments.<br>GUI pressure: Use a reference figure and require careful panel alignment, scales, peak labels, legends, and uncertainty bands. | Prepare the spectroscopy figure using sample_spectra.csv, Peak_Assignments.xlsx, and Figure_Style_Guide.pdf. Plot the three treatment spectra on aligned panels, label only the assigned peaks, and include the baseline-corrected inset shown in Spectra_Reference.png. Keep the legend outside the data region and make every wavelength label readable. Save the figure as Treatment_Spectra.png and a one-page caption and interpretation as Treatment_Spectra_Notes.pdf. Save both outputs to the Desktop. |
| **Zotero**<br>Best for: Organizing references, deduplicating sources, and producing consistent citations and bibliographies.<br>GUI pressure: Require a final document whose in-text citations and bibliography follow a supplied style and whose evidence table traces claims to sources. | Consolidate the review from Reference_Library.ris, Draft_Background.docx, and Citation_Style_Guide.pdf. Deduplicate the library, correct incomplete metadata using the DOI information already recorded in DOI_Checklist.xlsx, and revise the background so each scientific claim has an appropriate citation. Save the revised document as Background_With_Citations.docx and a clean PDF as Background_With_Citations.pdf. The bibliography must follow the supplied style exactly and remain consistent with the in-text citations. Save both outputs to the Desktop. |
| **Logism**<br>Best for: Digital-logic design, truth-table verification, and circuit visualization.<br>GUI pressure: Require a labeled circuit schematic and a truth-table comparison that can be checked in exported outputs. | Design the controller from Controller_Truth_Table.xlsx, Timing_Constraints.pdf, and Circuit_Layout_Reference.png. Implement the minimized combinational logic, add the required enable and fault behavior, and verify every input combination against the truth table. Arrange the schematic so signal flow is left to right, buses are labeled, and no wires or gate labels overlap. Save the circuit package as Controller_Logic_Design.zip, the schematic as Controller_Logic_Schematic.png, and the verification report as Controller_Truth_Table_Check.pdf. Save all outputs to the Desktop. |
| **3D Slicer**<br>Best for: Medical-image segmentation, volumetric measurement, and 3D visualization for research.<br>GUI pressure: Require segmentation decisions, measurements, and standardized render views that are visible in final images and reports. | Segment the lesion in Patient_014_CT.zip using Segmentation_Protocol.pdf and Radiology_Reference_Views.png. Separate the lesion from adjacent vessels, calculate its volume and longest diameter, and create axial, coronal, sagittal, and 3D views with the same orientation and label placement as the reference. Save the segmentation package as Patient_014_Segmentation.zip, the measurement report as Patient_014_Measurements.pdf, and the composite render as Patient_014_Views.png. Save all outputs to the Desktop. |

**Things to avoid in this domain**

- Do not use live or changing web data when a versioned paper, archived dataset, or dated report can be used.
- Do not supply expected scientific results as targets; provide methods, source files, and classification rules instead.
- Do not request a figure without defining the scientific comparison and the visible elements needed to interpret it.

---

### 5.4. Design & Creative

*Brand systems, image editing, 3D design, video editing, music notation, presentation design, and creative production.*

| Application and prompt design | Example ideas |
|---|---|
| **Chrome**<br>Best for: Researching stable visual references, archived style guides, and fixed museum or design-system pages.<br>GUI pressure: Use a dated or versioned reference source and require the research to shape a visible design system in the output. | I'm developing an exhibition concept around how similar functional objects were interpreted through different materials and periods. The seed accession numbers are listed in Met_Seed_Objects.xlsx, the exhibition argument is described in Exhibition_Concept.docx, and the board structure is provided in Collection_Board_Template.pptx.<br><br>Search for each accession number in The Met's online collection and review its full object record. Capture the verified title, date, culture or maker, medium, dimensions, department, credit line, and any rights or open-access information shown for the object.<br><br>Then use the collection's categories, department links, related-object suggestions, or search filters to find one defensible companion object for each seed object. Each companion should serve a similar function or share a clear visual motif while differing meaningfully in material, culture, or period. Explain the relationship using information available in the collection records rather than visual resemblance alone.<br><br>Save the source and object comparison table as Met_Object_Research.xlsx and complete the visual board as Material_Across_Time.pptx. Include accession numbers beneath every image and keep all captions readable. Save both outputs to the Desktop. |
| **GIMP**<br>Best for: Image compositing, retouching, masking, color correction, and reference matching.<br>GUI pressure: Supply source images, a layout reference, and brand constraints; require clean masks, typography, and export dimensions visible in the final image. | Create the campaign hero from Product_Cutout.png, Lifestyle_Background.jpg, and Campaign_Copy.docx, following the composition in Hero_Reference.png and the colors in Brand_Guide.pdf. Preserve realistic shadows around the product, remove the background halo, and keep the headline readable at both full size and mobile crop. Save the final image as Summer_Campaign_Hero.png and a side-by-side review sheet as Summer_Campaign_Hero_Review.pdf. Save both outputs to the Desktop. |
| **Blender**<br>Best for: 3D modeling, lighting, materials, scene composition, and rendering.<br>GUI pressure: Provide orthographic references and material cues; require multiple consistent render views or an annotated contact sheet. | Create a presentation render of the kiosk concept using Kiosk_Dimensions.pdf, Kiosk_Reference_Front.png, and Material_Palette.jpg. Model the visible structure accurately, match the supplied proportions, and light the scene so the display, counter, and material transitions remain readable. Produce front, three-quarter, and side views with consistent camera height and no cropped geometry. Save the renders as Kiosk_Front.png, Kiosk_ThreeQuarter.png, and Kiosk_Side.png, plus an annotated contact sheet as Kiosk_Render_Set.pdf. Save all outputs to the Desktop. |
| **Shotcut**<br>Best for: Editing narrative, promotional, instructional, and social video.<br>GUI pressure: Use a storyboard, timing sheet, and visual reference; require pacing, text-safe areas, transitions, and audio synchronization visible in the final video. | Edit the launch video from Product_Demo.mp4, Customer_Quote.mp4, and Voiceover.wav using Launch_Storyboard.pdf and Caption_Copy.docx. Follow the storyboard's sequence, synchronize the voiceover, keep captions inside the safe area, and match the reference pacing without abrupt cuts. Save the final video as Product_Launch_60s.mp4 and the selected thumbnail as Product_Launch_Thumbnail.png. The last frame must hold long enough for the call to action to be readable. Save both outputs to the Desktop. |
| **MuseScore**<br>Best for: Music notation, arrangement, engraving, and score preparation.<br>GUI pressure: Supply musical source material and an engraving reference; require readable parts, spacing, dynamics, and page turns in the final score. | Arrange the theme from Lead_Melody.mid, Chord_Sketch.pdf, and Instrumentation_Notes.docx in the style shown by Engraving_Reference.pdf. Write a two-minute chamber arrangement, keep articulations and dynamics consistent, and ensure no system or rehearsal mark collides with staff content. Save the full score as Chamber_Theme_Score.pdf, the editable score as Chamber_Theme.mscz, and an audio preview as Chamber_Theme_Preview.wav. Save all outputs to the Desktop. |
| **Office Suite**<br>Best for: Coordinated brand packages across documents, spreadsheets, and presentations.<br>GUI pressure: Use related templates and require consistent visual language across multiple final files. | Turn Campaign_Strategy.docx, Performance_Data.xlsx, and Brand_Template.pptx into a coordinated client package. Create Campaign_Recommendation.docx, Campaign_Budget.xlsx, and Campaign_Pitch.pptx using the same terminology, colors, and hierarchy. The budget summary must print on one page, the recommendation table must not split across pages, and the pitch deck must use the supplied slide master with readable charts. Save all three outputs to the Desktop. |

**Things to avoid in this domain**

- Do not rely on subjective wording such as "make it beautiful" without a reference, audience, or communication goal.
- Do not prescribe every coordinate unless the task is deliberate reference matching.
- Do not ask for a design application merely to open an asset; the final output must show meaningful composition or editing.

---

### 5.5. Engineering

*Mechanical, electrical, process, manufacturing, validation, circuit, numerical, and systems engineering.*

| Application and prompt design | Example ideas |
|---|---|
| **Chrome**<br>Best for: Consulting fixed standards editions, archived datasheets, and versioned technical references.<br>GUI pressure: Name the exact edition or revision and require traceable application of it in an engineering decision artifact. | We are screening several aircraft configurations for a survey mission before beginning a more detailed engineering study. The candidate models and Type Certificate Data Sheet numbers are listed in Candidate_Aircraft.xlsx, the mission loads and operating conditions are in Survey_Mission_Profile.pdf, and the assessment structure is provided in Airworthiness_Review_Template.docx.<br><br>Use the FAA Dynamic Regulatory System to locate the specified revision of each Type Certificate Data Sheet. Review both the DRS record and its attached certificate document to determine which model variants are covered and identify the certificate limitations relevant to the proposed mission, including approved engines, maximum weight, center-of-gravity restrictions, fuel requirements, operating categories, or model-specific notes where applicable.<br><br>Compare the certified configurations with the mission profile and identify which candidates appear compatible, which are clearly unsuitable, and which require additional configuration information before a conclusion can be reached. Preserve the TCDS number, revision, model designation, and page or note reference supporting each finding.<br><br>Save the comparison as Survey_Aircraft_Certification_Matrix.xlsx and the engineering review as Survey_Aircraft_Screening.docx. Save both files to the Desktop. |
| **KiCAD**<br>Best for: Schematic capture, PCB layout, net verification, and fabrication outputs.<br>GUI pressure: Require component placement, routing, labels, board constraints, and exported schematic/PCB views that are visible in final artifacts. | Design the sensor interface board from Sensor_Interface_Spec.pdf, Component_Pinout_Pack.pdf, and Board_Outline.dxf, following Placement_Reference.png. Include protection, filtering, test points, and the specified connector mapping; keep analog and digital return paths separated and respect the board outline. Save the editable design package as Sensor_Interface_KiCAD.zip, the schematic as Sensor_Interface_Schematic.pdf, the board views as Sensor_Interface_PCB.png, and fabrication files as Sensor_Interface_Gerbers.zip. Save all outputs to the Desktop. |
| **FreeCAD**<br>Best for: Parametric mechanical modeling, assemblies, and technical drawings.<br>GUI pressure: Use dimensioned drawings and reference views; require a model plus an exported drawing whose dimensions and views are legible. | Model the mounting bracket using Bracket_Dimensions.pdf, Interface_Geometry.step, and Bracket_Reference.png. Preserve the hole pattern and keep the design parametric so thickness and flange height can be changed independently. Produce a drawing with front, side, isometric, and section views, including the critical dimensions and tolerances without overlapping annotations. Save the model package as Mounting_Bracket_Model.zip, the drawing as Mounting_Bracket_Drawing.pdf, and the isometric render as Mounting_Bracket_Render.png. Save all outputs to the Desktop. |
| **SolveSpace**<br>Best for: Constraint-based part design and dimension-driven mechanisms.<br>GUI pressure: Require a fully constrained sketch and a clean dimensional export that exposes geometric relationships. | Create the sensor plate from Sensor_Plate_Sketch.pdf, Hole_Locations.xlsx, and Datum_Reference.png. Build the profile from constraints rather than freehand placement, verify that the mounting pattern remains symmetric when the width parameter changes, and show the final datum scheme clearly. Save the editable model as Sensor_Plate_SolveSpace.zip, the dimensioned drawing as Sensor_Plate_Drawing.pdf, and the constraint overview as Sensor_Plate_Constraints.png. Save all outputs to the Desktop. |
| **Logism**<br>Best for: Control logic, state-machine circuits, and digital verification.<br>GUI pressure: Require a readable circuit layout and state/truth-table evidence in the final outputs. | Implement the safety interlock from Interlock_State_Table.xlsx, Sensor_Logic_Spec.pdf, and State_Diagram_Reference.png. Build the state logic, include reset and fault-latch behavior, and verify normal, maintenance, and fault sequences. Arrange the circuit so each state block and transition signal is clearly labeled and wires do not cross labels. Save the circuit as Safety_Interlock_Logic.zip, the schematic as Safety_Interlock_Schematic.png, and the verification matrix as Safety_Interlock_Verification.pdf. Save all outputs to the Desktop. |
| **Octave**<br>Best for: Engineering calculations, regression, control analysis, and simulation.<br>GUI pressure: Require an engineering decision from calculated results plus an annotated figure with visible limits and fit quality. | Evaluate the replacement pump using Pump_Test_Data.csv, Pipe_Flow_Reference.pdf, and Fluid_Properties.xlsx. Fit an appropriate pressure-loss model, assess fit quality and flow regime, and define the operating envelope below the process limit in Design_Limit_Spec.pdf. Save the report as Pump_Replacement_Assessment.pdf, the calculated envelope as Pump_Operating_Envelope.csv, and the annotated figure as Pump_Pressure_Loss.png. The figure must label the limit crossing and keep the legend clear of the data. Save all outputs to the Desktop. |
| **Office Suite**<br>Best for: Validation protocols, design reviews, calculation packages, and stakeholder presentations.<br>GUI pressure: Use supplied templates across multiple applications and require consistent traceability, page layout, and visual summaries. | Prepare the validation package from Functional_Specification.pdf, Test_Run_Data.xlsx, and VV_Report_Template.docx, using System_Configuration.png as the visual source for the installed settings. Save the protocol and traceability report as System_VV_Report.docx, the test matrix as System_VV_Matrix.xlsx, and the review deck as System_VV_Summary.pptx. The report tables must not split across pages, the matrix summary must print on one landscape page, and the deck must use the supplied review layout. Save all outputs to the Desktop. |

**Things to avoid in this domain**

- Do not place the expected calculated values or verification answers in the prompt.
- Do not use broad praise or hype in place of measurable engineering requirements.
- Do not request native engineering work without a final drawing, image, report, or package that captures the result.

---

### 5.6. Legal & Compliance

*Regulatory analysis, policy application, contract review, evidence organization, disclosure, and compliance communication.*

| Application and prompt design | Example Ideas |
|---|---|
| **Chrome**<br>Best for: Researching fixed statutes, regulations, agency guidance, and archived decisions.<br>GUI pressure: Identify the exact edition, docket, or dated guidance and require precise citations in the final output. | Our compliance group is reviewing completed CFPB enforcement matters to improve the controls used by our payments and collections teams. The matters to review are listed in CFPB_Case_List.xlsx, the internal issue categories are defined in Compliance_Issue_Taxonomy.pdf, and the final format is provided in Enforcement_Review_Template.docx.<br><br>Locate each matter on the CFPB Enforcement Actions website. Review the case page together with the linked complaint, consent order, judgment, or related case documents needed to understand the outcome. Identify the respondent, action date, conduct at issue, laws or regulations cited, consumer redress, civil money penalty, business restrictions, and required corrective actions.<br><br>Do not rely only on the short case-page description when the underlying order provides a more precise obligation or amount. Classify each matter using the internal taxonomy and explain which operational control could have prevented or detected the conduct.<br><br>Save the structured case tracker as CFPB_Enforcement_Tracker.xlsx and the control lessons as CFPB_Compliance_Lessons.docx. Save both outputs to the Desktop. |
| **Excel/Sheets**<br>Best for: Compliance calculations, sampling, exception tracking, and evidence matrices.<br>GUI pressure: Use formulas, validation, conditional formatting, and printable summaries that remain visible in the final workbook. | Review the compliance sample using Transaction_Sample.xlsx, Monitoring_Rules.pdf, and Findings_Template.xlsx. Apply the rules to each transaction, preserve source IDs, and build an exceptions dashboard grouped by rule, owner, and severity. Use formulas rather than typed totals, add data validation for disposition status, and make the dashboard print on one landscape page without clipped columns. Save the workbook as Transaction_Compliance_Review.xlsx and export the dashboard as Transaction_Compliance_Summary.pdf. Save both outputs to the Desktop. |
| **Word/Docs**<br>Best for: Contract redlines, legal memoranda, policies, notices, and review comments.<br>GUI pressure: Require tracked changes, resolved comments, clause comparison, and stable pagination in the saved document. | Revise Vendor_Agreement_Draft.docx using Approved_Clause_Library.docx and Security_Requirements.pdf. Preserve the commercial terms, use tracked changes for every substantive edit, and add comments explaining deviations from the approved clauses. Save the redline as Vendor_Agreement_Redline.docx and a clean execution copy as Vendor_Agreement_Clean.docx. The signature blocks and clause headings must not be split awkwardly across pages. Save both outputs to the Desktop. |
| **PowerPoint**<br>Best for: Compliance briefings, hearing decks, issue timelines, and decision trees.<br>GUI pressure: Use a template and require visually clear chronology, authority hierarchy, or decision flow in the final deck. | Create the committee briefing from Investigation_Timeline.xlsx, Key_Evidence_Summary.docx, and Hearing_Deck_Template.pptx. Build a chronology, an evidence-to-obligation map, and a decision flow that separates confirmed facts from open issues. Keep every citation readable and use the supplied slide master. Save the deck as Compliance_Committee_Briefing.pptx and a PDF copy as Compliance_Committee_Briefing.pdf. Save both outputs to the Desktop. |
| **Zotero**<br>Best for: Managing authorities, citation consistency, and source metadata for legal research.<br>GUI pressure: Require a final memo with correct citation style and a source table that maps propositions to authorities. | Consolidate the authorities in Case_Authorities.ris, Draft_Legal_Analysis.docx, and Citation_Manual_Excerpt.pdf. Correct duplicate and incomplete records using Authority_Metadata_Check.xlsx, then revise the analysis so every legal proposition is supported by the appropriate authority. Save the revised memo as Legal_Analysis_With_Authorities.docx and the authority table as Legal_Authority_Map.csv. Keep the bibliography and in-text citations consistent with the supplied citation rules. Save both outputs to the Desktop. |
| **Obsidian**<br>Best for: Evidence maps, issue trees, matter chronologies, and linked policy knowledge.<br>GUI pressure: Require a linked knowledge structure plus an exported map or report that preserves the relationships for verification. | Organize the investigation from Interview_Notes.docx, Evidence_Register.xlsx, and Policy_Requirements.pdf. Build a linked matter map that connects each allegation, supporting evidence, policy obligation, and unresolved gap. Save the vault as Investigation_Evidence_Vault.zip, export the relationship map as Investigation_Evidence_Map.png, and summarize the open issues in Investigation_Issue_Summary.pdf. The map must use a consistent legend and keep node labels readable. Save all outputs to the Desktop. |
| **GIMP**<br>Best for: Sketches of crime scenes, traffic accident diagrams/sketches, property layouts, insurance claim diagrams.<br>GUI pressure: Require a sketch of a vehicle collision based on a witness statement and a street template, using color codes to distinguish each vehicle. | Using the witness's account of how the vehicle collision in witness.docx, the claim details in claimdraft.pdf, and the street template with color codes for each vehicle in template.png, create a sketch of the collision and save it as sketch.png. Additionally, create a report containing the details of the vehicles involved and save it as collision.docx |

**Things to avoid in this domain**

- Do not ask for analysis under a vague "current law" when a dated rule, contract version, or policy edition should be named.
- Do not request legal conclusions without supplying the governing sources and relevant facts.
- Do not rely on visual actions such as comments or highlighting unless those features remain in the saved output.

---

### 5.7. Operations & Management

*Process design, operating reviews, capacity planning, project coordination, knowledge management, and executive communication.*

| Application and prompt design | Example prompt |
|---|---|
| **Chrome**<br>Best for: Finding stable benchmarks, archived vendor documentation, and dated operating standards.<br>GUI pressure: Use fixed-source research to support a decision and require a cited comparison in the final output. | I'm preparing a workshop on why operational-improvement recommendations remain open, become implemented, or are closed without full implementation. The GAO report numbers and recommendations to review are listed in GAO_Recommendation_Targets.xlsx. Use the interpretation rules in Recommendation_Status_Guide.pdf and record the results in Followup_Review_Template.xlsx.<br><br>Search for each report number on the GAO website and work through the report page, recommendation section, status information, and agency-response details. For each target recommendation, capture the responsible agency, recommendation language, current status, actions reported by the agency, and GAO's explanation for closing it or keeping it open.<br><br>Compare the cases and identify recurring implementation patterns, such as formal policy changes, improved monitoring, incomplete evidence, responsibility gaps, or actions that addressed only part of the recommendation. Keep GAO's stated rationale separate from your interpretation.<br><br>Save the completed analysis as GAO_Recommendation_Followup.xlsx and the workshop brief as Recommendation_Implementation_Patterns.docx. Save both files to the Desktop. |
| **Obsidian**<br>Best for: Linked operating knowledge, process dependencies, risks, and decision logs.<br>GUI pressure: Require a linked vault plus an exported dependency map or knowledge guide that exposes relationships. | Build the launch knowledge base from Launch_Plan.docx, Risk_Register.xlsx, and Team_Dependencies.csv. Link milestones to owners, decisions, risks, and source documents, then create a dependency map that highlights the critical path and unresolved decisions. Save the vault as Product_Launch_Vault.zip, the map as Product_Launch_Dependency_Map.png, and the operating guide as Product_Launch_Guide.pdf. Keep map labels readable and use a consistent status legend. Save all outputs to the Desktop. |
| **OpenBoard**<br>Best for: Workshops, process mapping, retrospectives, and collaborative planning boards.<br>GUI pressure: Require a structured board export with lanes, clusters, arrows, and readable labels that feed a final action plan. | Turn Workshop_Notes.docx, Current_Process.png, and Issue_Backlog.xlsx into a process-improvement workshop board. Create separate pages for the current state, root causes, future state, and action owners; use arrows and swimlanes so handoffs are unambiguous. Export the board as Process_Improvement_Workshop.pdf and save the resulting action plan as Process_Improvement_Actions.xlsx. The PDF pages must remain legible at normal viewing size. Save both outputs to the Desktop. |
| **Excel/Sheets**<br>Best for: Capacity models, schedules, staffing plans, trackers, and operational dashboards.<br>GUI pressure: Use formulas, constraints, conditional formatting, and print-ready summaries in the output workbook. | Create the capacity plan from Weekly_Demand.xlsx, Team_Productivity.xlsx, and Staffing_Constraints.pdf. Model weekly demand, productive capacity, shrinkage, and backlog under Base and Surge scenarios, then produce a staffing recommendation by team. Save the model as Q4_Capacity_Plan.xlsx and the executive summary as Q4_Capacity_Summary.pdf. The dashboard must show capacity gaps by week, use readable conditional formatting, and print on one landscape page. Save both outputs to the Desktop. |
| **Word/Docs**<br>Best for: SOPs, operating plans, postmortems, and decision documents.<br>GUI pressure: Use a supplied template and require process diagrams, controlled headings, comments, and stable pagination. | Draft the incident-management SOP using Incident_History.xlsx, Escalation_Policy.pdf, and SOP_Template.docx. Convert the policy into a practical workflow, include a RACI table and escalation decision tree, and add resolved comments where policy owners must confirm a choice. Save the completed document as Incident_Management_SOP.docx and a clean PDF as Incident_Management_SOP.pdf. Keep the decision tree on one page and prevent the RACI table from splitting. Save both outputs to the Desktop. |
| **PowerPoint**<br>Best for: Operating reviews, project kickoffs, executive updates, and action-oriented storytelling.<br>GUI pressure: Use a deck template and require scorecards, timelines, risk visuals, and consistent status communication. | Prepare the monthly operating review from KPI_Results.xlsx, Initiative_Status.docx, and Operating_Review_Template.pptx. Build a scorecard, explain the largest variances, show the next eight weeks of milestones, and visualize the top risks with owners and mitigations. Save the deck as July_Operating_Review.pptx and a PDF copy as July_Operating_Review.pdf. Use the supplied slide master, keep chart labels readable, and avoid overcrowding the action slide. Save both outputs to the Desktop. |

**Things to avoid in this domain**

- Do not ask for generic "best practices" when internal process files and operating constraints should drive the work.
- Do not create a whiteboard or map that is disconnected from the final plan or decision.
- Do not list every expected conclusion; provide the source rules and ask the agent to synthesize the operating implications.

---

### 5.8. Government & Public Sector

*Policy analysis, program evaluation, public communication, grants, service planning, and civic decision support.*

| Application and prompt design | Example prompt |
|---|---|
| **Chrome**<br>Best for: Researching dated government reports, archived datasets, official code editions, and fixed public records.<br>GUI pressure: Require exact publication dates and source references in the final policy artifact. | I'm building a legislative-process reference for three major laws enacted during the 117th Congress: H.R. 3684, H.R. 5376, and H.R. 4346. Use the tracking fields in Legislative_Targets.xlsx, the milestone definitions in Legislative_Process_Guide.pdf, and the visual structure in Bill_Timeline_Template.pptx.<br><br>Use Congress.gov to locate each bill in the correct Congress and trace its path from introduction through enactment. Review the bill's official titles, sponsors, committees, major actions, summaries, related or companion bills, recorded votes where available, public-law designation, and enactment date.<br><br>Identify the most consequential procedural milestones for each bill rather than copying every action. Where a related bill or amendment became the vehicle for the final law, make that relationship clear and support it with the information shown in the legislative record.<br><br>Save the structured research as Enacted_Bill_Pathways.xlsx and the completed comparative timeline as Major_Laws_Legislative_Pathways.pptx. Keep the three pathways visually distinct and all milestone dates readable. Save both outputs to the Desktop. |
| **OpenBoard**<br>Best for: Public workshops, service-blueprint mapping, stakeholder sessions, and community feedback synthesis.<br>GUI pressure: Require a multi-page board export with clear categories, relationships, and a resulting action artifact. | Synthesize the engagement session from Resident_Comments.docx, Service_Process.png, and Workshop_Agenda.pdf. Create board pages for stakeholder groups, recurring barriers, service touchpoints, and proposed improvements, using a legend that distinguishes direct comments from facilitator synthesis. Export the board as Community_Service_Workshop.pdf and save the prioritized actions as Community_Service_Actions.xlsx. Ensure every board page remains legible when exported. Save both outputs to the Desktop. |
| **Obsidian**<br>Best for: Policy evidence maps, program knowledge bases, cross-agency dependencies, and decision records.<br>GUI pressure: Require linked notes plus an exported policy map or implementation guide that makes relationships visible. | Organize the policy package from Agency_Mandates.pdf, Program_Inventory.xlsx, and Interagency_Notes.docx. Link each statutory duty to the responsible program, shared dependency, evidence source, and unresolved implementation question. Save the vault as Interagency_Policy_Vault.zip, export the relationship map as Interagency_Policy_Map.png, and write the implementation summary as Interagency_Implementation_Guide.pdf. Use readable labels and a clear agency legend. Save all outputs to the Desktop. |
| **Excel/Sheets**<br>Best for: Grant allocation, program metrics, budget scenarios, and transparent scoring models.<br>GUI pressure: Require formula-based scoring, protected assumptions, visible audit trails, and a print-ready decision summary. | Score the grant applications using Grant_Applications.xlsx, Scoring_Rubric.pdf, and Allocation_Model_Template.xlsx. Apply the rubric consistently, show each criterion calculation, and model allocations under the approved budget and a 10% reduction scenario. Save the model as Community_Grant_Allocation.xlsx and the decision summary as Community_Grant_Recommendations.pdf. The summary sheet must print on one landscape page and clearly flag tie-break decisions. Save both outputs to the Desktop. |
| **Word/Docs**<br>Best for: Policy briefs, staff reports, public notices, program evaluations, and implementation plans.<br>GUI pressure: Use a government template and require accessible headings, tables, callouts, and source notes in the output. | Draft the council staff report using Pilot_Results.xlsx, Public_Comments.docx, and Staff_Report_Template.docx. Summarize the pilot outcomes, explain the major public concerns, and present three implementation options with fiscal and operational tradeoffs. Save the report as Transit_Pilot_Staff_Report.docx and a public PDF as Transit_Pilot_Staff_Report.pdf. Follow the template, add descriptive headings, keep option tables intact across pages, and include a plain-language summary box. Save both outputs to the Desktop. |
| **PowerPoint**<br>Best for: Council briefings, public-meeting decks, program updates, and budget presentations.<br>GUI pressure: Require accessible visual hierarchy, cited charts, maps, and clear decision points in the final deck. | Create the public briefing from Budget_Scenarios.xlsx, Program_Map.png, and Public_Deck_Template.pptx. Explain the service issue, compare the three funding scenarios, and show the geographic impact using the supplied map. Save the deck as Library_Service_Options.pptx and a PDF as Library_Service_Options.pdf. Use the supplied theme, keep all text at presentation-readable size, add source notes to every data slide, and make the final decision slide visually distinct. Save both outputs to the Desktop. |

**Things to avoid in this domain**

- Do not use live public dashboards when a dated release or archived dataset is available.
- Do not make recommendations without connecting them to the supplied mandate, budget, and affected population.
- Do not create public-facing visuals without accessibility, readability, and source attribution requirements.

---

### 5.9. Sales & Marketing

*Market research, campaign design, account planning, sales enablement, creative production, and performance communication.*

| Application and prompt design | Example prompt |
|---|---|
| **Chrome**<br>Best for: Researching dated company filings, archived product pages, fixed analyst reports, and stable market sources.<br>GUI pressure: Use a fixed source list and require cited findings to appear in a market map, account brief, or campaign strategy. | We are reviewing several discontinued competitor brand names before naming a new workflow-automation product. The trademark serial numbers and proposed product categories are listed in Competitor_Marks.xlsx, the category boundaries are defined in Brand_Category_Map.pdf, and the review format is provided in Trademark_Review_Template.xlsx.<br><br>Use the USPTO trademark search system to locate each serial number, then review its detailed TSDR record. Confirm the mark wording, owner, filing basis, international classes, goods or services, filing and registration dates, and final status.<br><br>For records that were abandoned, cancelled, or expired before the cutoff date in the workbook, review the prosecution history and the final relevant document to determine what happened. Distinguish an application abandoned during examination from a registration later cancelled because maintenance filings were not submitted.<br><br>Use the findings to identify naming patterns that appear crowded, categories where similar marks failed for procedural rather than substantive reasons, and records that warrant separate legal review.<br><br>Save the research as Competitor_Trademark_Review.xlsx and the naming-risk summary as Trademark_Landscape_Brief.docx. Save both outputs to the Desktop. |
| **GIMP**<br>Best for: Campaign imagery, ad variants, product composites, thumbnails, and branded visual assets.<br>GUI pressure: Supply source assets and reference layouts; require multiple channel crops with consistent hierarchy and clean masking. | Create the paid-social visual set from Product_Render.png, Customer_Photo.jpg, and Campaign_Copy.docx using Brand_Guide.pdf and Ad_Reference.png. Produce square and vertical variants with consistent hierarchy, realistic product integration, and readable copy inside each platform's safe area. Save the final images as Campaign_Ad_Square.png and Campaign_Ad_Vertical.png, plus a comparison sheet as Campaign_Ad_Review.pdf. Save all outputs to the Desktop. |
| **Office Suite**<br>Best for: Integrated account plans, pipeline models, campaign reports, and sales presentations.<br>GUI pressure: Coordinate data, narrative, and visuals across workbook, document, and deck outputs. | Build the quarterly sales package from Pipeline_Export.xlsx, Win_Loss_Notes.docx, and QBR_Template.pptx. Save the cleaned forecast as Q3_Sales_Forecast.xlsx, the account-priority memo as Q3_Account_Priorities.docx, and the review deck as Q3_Sales_QBR.pptx. Keep stage probabilities formula-driven, make the forecast summary print on one page, and use the supplied slide master for a readable funnel and regional performance chart. Save all three outputs to the Desktop. |
| **Shotcut**<br>Best for: Product demos, testimonial edits, campaign videos, and social cutdowns.<br>GUI pressure: Use a storyboard, caption copy, and reference pacing; require synchronized, platform-ready video outputs. | Edit the customer story from Interview_A.mp4, Product_Broll.mp4, and Narration.wav using Customer_Story_Storyboard.pdf and Caption_Copy.docx. Build a 45-second narrative, synchronize the narration, use lower thirds consistently, and keep captions within the mobile safe area. Save the final video as Customer_Story_45s.mp4 and the thumbnail as Customer_Story_Thumbnail.png. Ensure the product proof point is visible when it is mentioned and the final call to action remains on screen long enough to read. Save both outputs to the Desktop. |

**Things to avoid in this domain**

- Do not use live social trends, prices, or rankings as evidence unless the prompt fixes a date and source snapshot.
- Do not request generic promotional copy without audience, offer, channel, and brand constraints.
- Do not create attractive visuals that are disconnected from the campaign objective or performance data.

---

### 5.10. Healthcare

*Clinical evidence synthesis, imaging analysis, quality improvement, patient-safety review, and clinical operations.*

| Application and prompt design | Example prompt |
|---|---|
| **Chrome**<br>Best for: Consulting stable clinical guidelines, drug labels, trial records, and versioned evidence.<br>GUI pressure: Name the guideline edition, publication, or archived trial record and require exact citations in the final evidence artifact. | Our clinical-evidence team is reviewing whether several completed trials changed their registered outcomes or enrollment information during the study. The NCT numbers and historical record dates are listed in Trial_Version_Targets.xlsx, the outcome-classification rules are in Endpoint_Review_Guide.pdf, and the evidence structure is provided in Clinical_Evidence_Template.xlsx.<br><br>Locate each study on ClinicalTrials.gov and review its study details, posted results, and record history. Use the historical version specified in the target workbook as the comparison point.<br><br>For each trial, document the study design, enrollment, arms, primary and secondary outcomes, completion dates, posted result values, and limitations or caveats. Compare the selected historical record with the final posted record and identify meaningful changes to enrollment, outcome wording, outcome timing, study status, or analysis populations.<br><br>Do not characterize a change as outcome switching unless it meets the definition in the review guide.<br><br>Save the evidence table as Clinical_Trial_Record_Review.xlsx and the findings memo as Clinical_Trial_Registration_Findings.docx. Save both files to the Desktop. |
| **3D Slicer**<br>Best for: Clinical and research imaging, segmentation, measurements, and 3D rendering.<br>GUI pressure: Require standardized views, quantitative measurements, and exported segmentation packages that can be verified independently. | Analyze the preoperative scan in Case_022_MRI.zip using Tumor_Segmentation_Protocol.pdf and Surgical_View_Reference.png. Segment the lesion and edema separately, record volume and maximum dimensions, and create axial, coronal, sagittal, and 3D views matching the reference orientation. Save the segmentation data as Case_022_Segmentation.zip, the measurement summary as Case_022_Imaging_Report.pdf, and the composite image as Case_022_Imaging_Views.png. Keep labels outside the anatomy and use a consistent color legend. Save all outputs to the Desktop. |

**Things to avoid in this domain**

- Do not rely on a changing clinical webpage when a dated guideline, label, or peer-reviewed publication can be named.
- Do not ask for diagnostic conclusions beyond what the supplied data and task scope support.
- Do not make a medical-image task depend only on a screenshot; preserve measurements and segmentation results in final outputs.

---

### 5.11. Multimedia & A/V

*Video editing, audio production, scoring, motion graphics, media review, and audiovisual delivery.*

| Application and prompt design | Example prompt |
|---|---|
| **Chrome**<br>Best for: Finding fixed archive media, documented licenses, and versioned production references.<br>GUI pressure: Use a stable archive or license page and require source and rights information in the final deliverable. | I'm selecting historically appropriate recordings for three scenes in a documentary about American public life before 1923. The candidate Library of Congress item IDs are listed in Candidate_Recordings.xlsx, the scenes and emotional beats are described in Documentary_Scene_Map.xlsx, and the usage rules are provided in Archive_Rights_Guide.pdf.<br><br>Use the Library of Congress National Jukebox to locate each candidate recording. Review the item record, contributor and performer information, recording date, label and catalog details, genre, source institution, citation information, and the item-specific Rights and Access statement.<br><br>Listen to enough of each recording to assess its pacing, instrumentation, vocal presence, and suitability for the scenes in the scene map. Recommend one primary and one backup recording for each scene, noting any rights or attribution concern that would need to be resolved before use.<br><br>Save the completed cue sheet as Documentary_Archive_Cue_Sheet.xlsx and the selection rationale as Documentary_Music_Selections.docx. Include the Library of Congress item ID and source link for every recommendation. Save both outputs to the Desktop. |
| **Shotcut**<br>Best for: Editing video, captions, transitions, color balance, and timed graphics.<br>GUI pressure: Require a final video whose pacing, safe areas, overlays, and sequence can be checked, plus a meaningful still or cue sheet if useful. | Edit the tutorial from Screen_Record.mp4, Presenter_Camera.mp4, and Voiceover.wav using Tutorial_Edit_Plan.pdf and Onscreen_Text.docx. Synchronize the sources, remove dead time, emphasize the three key interface steps with restrained callouts, and keep captions inside the safe area. Save the finished video as Setup_Tutorial.mp4 and the selected cover frame as Setup_Tutorial_Cover.png. Keep cursor actions visible when referenced and avoid covering important interface controls. Save both outputs to the Desktop. |
| **Reaper**<br>Best for: Audio editing, mixing, restoration, dialogue cleanup, and mastering.<br>GUI pressure: Use reference audio and delivery specifications; require audible edits plus measurable loudness and stem outputs. | Mix the interview episode from Host_Raw.wav, Guest_Raw.wav, and Music_Bed.wav using Mix_Reference.wav and Delivery_Spec.pdf. Remove distracting noise without damaging speech, balance the two voices, automate the music under dialogue, and meet the supplied loudness and peak targets. Save the final mix as Interview_Episode_Master.wav, the dialogue stem as Interview_Episode_Dialogue.wav, and the mix report as Interview_Episode_Mix_Report.pdf. Save all outputs to the Desktop. |
| **MuseScore**<br>Best for: Score preparation, arrangement, transcription, and engraved parts.<br>GUI pressure: Require notation that is musically correct and visually readable, with page turns, dynamics, and instrument ranges reflected in outputs. | Create the performance score from Piano_Demo.wav, Chord_Chart.pdf, and Ensemble_Ranges.docx using Score_Style_Reference.pdf. Transcribe the theme, arrange it for the listed ensemble, and prepare readable parts with consistent rehearsal marks and practical page turns. Save the full score as Theme_Arrangement_Score.pdf, the editable score as Theme_Arrangement.mscz, and the audio mockup as Theme_Arrangement.wav. Save all outputs to the Desktop. |
| **Blender**<br>Best for: 3D motion graphics, animated visualizers, compositing, and rendered sequences.<br>GUI pressure: Provide visual references and timing; require rendered frames or video with consistent composition, materials, and camera movement. | Create a looping visualizer using Album_Artwork.png, Visualizer_Storyboard.pdf, and Track_Edit.wav, matching the lighting cues in Render_Reference.png. Build a 15-second seamless loop with subtle camera movement, readable artwork, and motion that responds to the track without rapid flashing. Save the final video as Album_Visualizer_Loop.mp4 and three representative frames as Album_Visualizer_Frames.pdf. Save both outputs to the Desktop. |
| **MPV**<br>Best for: Detailed playback review, frame inspection, subtitle timing, and media quality control.<br>GUI pressure: Turn playback observations into timestamped output artifacts such as a QC log and contact sheet. | Review Final_Cut_v3.mp4 against Edit_Decisions.pdf and Subtitle_File.srt, using Audio_Delivery_Spec.pdf for the technical checks. Record every visible edit issue, subtitle timing problem, frozen frame, and audio discontinuity with exact timestamps. Save the findings as Final_Cut_QC_Log.csv and create a contact sheet of the most important visual issues as Final_Cut_QC_Frames.pdf. The contact sheet must show the timestamp and issue ID under each frame. Save both outputs to the Desktop. |

**Things to avoid in this domain**

- Do not ask merely for playback or inspection; the observation must drive a saved edit, timestamp log, contact sheet, or report.
- Do not use unstable online media when a fixed release, archive item, or supplied source file can be used.
- Do not define quality only as "sounds good" or "looks cinematic"; give reference material and observable delivery requirements.

---

### 5.12. Real Estate

*Property research, valuation support, listing assets, walkthrough media, investment analysis, and client presentation.*

| Application and prompt design | Example prompt |
|---|---|
| **Chrome**<br>Best for: Researching fixed parcel records, recorded deeds, archived planning documents, and dated market reports.<br>GUI pressure: Use dated public records or archived reports and require exact source references in the final analysis. | We are performing a preliminary title-history review for several New York City properties before deciding which ones should move to full diligence. The borough, block, lot, and review cutoff date for each property are listed in Property_Targets.xlsx. Use the issue definitions in Title_Exception_Guide.pdf and record the results in Property_Diligence_Template.xlsx.<br><br>Search each property in NYC ACRIS using its borough-block-lot information. Review the recorded documents dated on or before the specified cutoff, including the document-detail records and document images needed to understand the transaction history.<br><br>Identify the most recent deed, grantor and grantee, recorded consideration, execution and recording dates, document ID or CRFN, and any mortgages, assignments, satisfactions, or other instruments that materially affect the preliminary chain. Where a satisfaction appears to correspond to an earlier mortgage, confirm the relationship using the parties, amounts, dates, and referenced document information rather than assuming the match.<br><br>Save the completed tracker as NYC_Preliminary_Title_Review.xlsx and the properties requiring further investigation as NYC_Title_Diligence_Flags.docx. Include the ACRIS identifiers supporting every flagged issue. Save both outputs to the Desktop. |
| **GIMP**<br>Best for: Listing-photo correction, floor-plan cleanup, brochure images, and compliant visual enhancement.<br>GUI pressure: Provide originals, a style reference, and factual constraints; require consistent crops and truthful edits visible in outputs. | Prepare the listing images from Living_Room_RAW.jpg, Kitchen_RAW.jpg, and Exterior_RAW.jpg using Listing_Image_Reference.pdf and Property_Features.docx. Correct exposure and perspective, remove temporary clutter only where it does not alter permanent features, and create consistent landscape crops. Save the final images as Living_Room_Final.png, Kitchen_Final.png, and Exterior_Final.png, plus a contact sheet as Listing_Image_Set.pdf. Save all outputs to the Desktop. |
| **Shotcut**<br>Best for: Property walkthroughs, neighborhood videos, agent introductions, and social cutdowns.<br>GUI pressure: Use floor plans and a shot order; require coherent spatial sequence, labels, pacing, and compliant text in final video. | Edit the property walkthrough from Interior_Walkthrough.mp4, Exterior_Drone.mp4, and Agent_Voiceover.wav using Floor_Plan.pdf and Walkthrough_Storyboard.docx. Order the rooms so the route matches the floor plan, add restrained room labels, and keep required brokerage text readable at the end. Save the finished video as 214_Oak_Walkthrough.mp4 and the thumbnail as 214_Oak_Thumbnail.png. Avoid transitions that imply connections between rooms that do not exist. Save both outputs to the Desktop. |
| **Office Suite**<br>Best for: Comparable analyses, investment packages, listing brochures, and client presentations.<br>GUI pressure: Require consistent property facts across workbook, document, and deck, with print and presentation layout checks. | Create the investment package from Comparable_Sales.xlsx, Property_Condition_Report.pdf, and Offering_Memorandum_Template.pptx. Save the valuation model as 214_Oak_Valuation.xlsx, the investment memo as 214_Oak_Investment_Memo.docx, and the offering deck as 214_Oak_Offering_Deck.pptx. The valuation summary must print on one page, the memo's risk table must not split, and the deck must use the supplied template with readable maps and charts. Save all three outputs to the Desktop. |

**Things to avoid in this domain**

- Do not use changing listing prices or live market pages unless a fixed snapshot or dated record is identified.
- Do not enhance property images in a way that materially misrepresents the property.
- Do not produce attractive marketing collateral without preserving factual consistency across the source documents.

---

## 6. Final attempter checklist

☐ The prompt fits the selected domain and uses an application available for that domain.
☐ The prompt mentions and utilizes at least three input files by exact filename.
☐ The filenames are introduced naturally and the role of each source is understandable.
☐ Any Chrome research uses a stable, versioned, dated, or archived source.
☐ The prompt does not directly tell the model to use a GUI.
☐ The final artifact has visual, spatial, temporal, or application-native requirements that make GUI work valuable.
☐ The GUI-related work is reflected in a final output, not only in a temporary application state.
☐ The prompt does not reveal the expected calculations, classifications, or conclusions.
☐ The prompt sounds like a realistic workplace request rather than an evaluator rubric.
☐ Every output has an exact filename and extension.
☐ The primary output is named explicitly.
☐ Every final output is required to be saved to the Desktop.
☐ The output set is sufficient to verify the requested work.

### Final test

Ask: "Could the final outputs be produced convincingly without visually working in the intended application?" If the answer is yes, strengthen the artifact requirements—not by naming the GUI, but by adding a template, reference, diagram, layout, media, or native-format requirement that matters to the final result.
