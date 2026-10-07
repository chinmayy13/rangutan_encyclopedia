# CTSAgn task: rebuilt version (v2)

Original (`../task_10/`) is untouched. This folder is a full redesign following `../task_10/feedback.md` (reviewer: "must be redone from scratch, adding more complexity"; agent run scored 96%).

## Why the old task scored 96%, and what changed
Every rule the agent needed was spelled out, so it was data processing, not judgment (`stump.md`: "method hides in the files", "thresholds live in the source"; `model_stumping_prompts.md`: "if you write the criteria into the request you have removed the judgment call"). Three levers were moved from the prompt into the source files, each changing a large share of the deliverable:

| Lever (guide) | Where it now lives | Default-agent failure | Effect |
|---|---|---|---|
| Method hides in the files / specialist convention | `Thermal_Screening_Note.pdf` "Rate basis": rates are per cent of the **150 °C mass** | Reads the instrument's %/°C column as is (it is per cent of *initial* mass) | Table rates, post-adsorption ratios and the headline finding all change: post/as-made peak rate is **0.86 raw but 1.006 dry**, so the "peak rate falls after adsorption" story disappears |
| Source precedence / exclusion rule | `Stage_Gate_Policy.pdf` §1–2: cash cost = all lines **except equipment depreciation**; released batches only; loss sensitivity separate | Uses the CSV's `Total_Production_Cost_$`/`Cost_per_kg_$` | CTSAgn $42.92/kg not $45.42; efficiency +16.5% not +10.1%; headroom $354 not $229; loss case −19.2% not −23.5% |
| Thresholds in the source / stop rule | `Stage_Gate_Policy.pdf` §3: ceiling must be ≥25 °C above the benchmark regen temperature; external guidance counts only if measured on the candidate; cycles must be demonstrated | Says "195 °C is above 175 °C, proceed" | Ceiling 195.4 − 175 = 20.4 °C fails → **Hold for validation**, plus loss-case efficiency fails and cycle data are absent |
| Visual template (kept) | `plot_template.xcf` → updated copy; axis must be extended because the dry-basis post-adsorption water step reaches ≈0.32 vs the template's 0.28 | Copies template axis, clips data | Visual + xcf criteria |

Four levers, as the guide recommends ("three or four is enough; nine is dense, not hard").

## Feedback → fix
| Review point | Fix |
|---|---|
| Prompt: year missing | "September 2018 campaign" |
| Prompt prescriptive / leading ("whether it really shows", "how much … trusting") | Rewritten in four short paragraphs; neutral wording |
| Prompt reveals released-product basis | Removed; basis now in the policy file |
| GUI pressure | Template-matching plot (xcf), colour edit, render checks stated as outcomes (no "use page view") per FAQ |
| "10-minute meeting" not covered by rubric | Phrase removed (nothing scoreable); "one page" is covered by criterion 4 |
| Note says "Alignate", "The The"; water-tail wording | Fixed in `initial_files/Thermal_Screening_Note.pdf` (tail-to-185 °C wording kept) |
| Agn.txt Sig1–Sig6 removed | Column-definition block restored (data rows byte-identical; checked) |
| Initializer missing Regeneration bulletin, missing bracket, stale golden links | `verifier_initializer.md`: nine-file list, validated structure, URL rules |
| GTF font colours vs template, decimals, 9.5 pt, headings | To apply when rebuilding the GTFs: peak labels and axis text in #15295d (only the two traces change colour), temperatures to one decimal, all docx text ≥10 pt including the table, one heading style per level |
| Rubric: C3/C30 categorisation, C12/C13 overfit/mixed, C14 subjective, C16 overloaded, C18 inaccurate, C19 location, C21/C24 overlap, C23 negative framing, C26/27 redundant, missing colour coverage | New rubric: 30 criteria; font/margin thresholds are the prompt's own 10 pt / 2.5 cm and categorised visual; no negative framing; hex colours covered in two criteria; no "immediately under the table"; one criterion per element |

## Guideline cross-check (`attempter_guidelines.md`, `pre_submission.md`, `prompt_writing.md`)
- Filenames + Desktop save + deliverable types stated; ≥3 named inputs (nine); not all CSV/XLSX; GUI is outcome-shaped. Prompt names no application, mirrors `prompt_writing.md` "indirect GUI pressure".
- Rubric: 30 criteria (limit 10–30), weights integers 1–50, MUST-PASS only on the three file gates, format 5.0% / correctness 71.9% / visual 23.1%, values never written into criteria, positive framing, expected-file anchoring (visual anchored only for the template, the allowed exception).
- Every graded value reproduces from the inputs: `answer_key/compute_answer_key.py` (asserts the CSV line items sum to each stated batch total).

## What I could not do (needs you, in the platform/VM)
1. Upload the new/changed inputs, run the initializer, rebuild the three GTFs in the VM from the new inputs (numbers in `answer_key/answer_key.json`), upload to Asset section.
2. Paste the rubric, run Copilot checks and the rubric generator, fix flags, run the verifier (expect 1.0).
3. **Click Run twice for the agent run.** The 96% was measured on the old task; the new difficulty is my estimate (`rubric.md` footer: ~51% for an agent that misses both conventions) and is unverified. If it still averages >80%, the next lever is a second precision trap in the data (e.g. an off-side note in the CSV that re-grades a batch).
4. Confirm CC0/PII on the TGA files: `CTS.txt` and the xlsx headers carry a lab server path with a first name ("Abner") and operator initials. Standalone names are tolerated by `pre_submission.md`, but strip them if you prefer.

## Files
`prompt.md` · `prompt_change_description.md` · `rubric.md` · `verifier_initializer.md` · `answer_key/` · `initial_files/` (changed: Agn.txt, CTSAgn_batch_economics.csv, Thermal_Screening_Note.pdf; new: Stage_Gate_Policy.pdf).
