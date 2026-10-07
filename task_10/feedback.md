Improve the task per the following feedback:

Quality: Overall Task

3

Quality: Instruction Following

no

Overall Task Feedback

I would like to thank the attempter for this complex task. Clearly a lot of effort has been put into this. This is good work. The score of 3/5 (which seems harsh but these are the reviewer rules) is mainly due to initializer and rubric issues. There was also an issue with one of the input files. I have done the required fixes so there is no action required from you.
The agents returned 96/97%, i.e. the task was too easy (which doesn't affect the score). To make it harder, the following steps have been done:
-Removed Composite_DTG_Overlay.png deliverable (as a separate file) as this is a trivial step.
-Removed input image DTG_Thermogram.png, as all information in that can be found in the data.
-Adapted prompt, rubric, and Thermal_Screening_Note.pdf to adapt to these changes.
-Remove meta data from Agn.txt
-Added more explicit GUI pressure in separate paragraph (with stricter page margins, no image distortions etc.).
-Added a template for the required plot and added template modification requirement. This is in gimp format trying to force the agent to deal with gimp.

Prompt: 4/5

"September" is the prompt's only temporal reference and carries no year, while every input file refers contains the year 2018.
Change the second sentence of the prompt into:
"All we have is the TGA work from the September 2018 campaign..." to align the prompt with the input files.

The 3rd and 6th paragraph sound rather prescriptive (like an enumeration).
Also criterion 12 of the rubric checks for something which is not asked for in the prompt. Rather than changing the criterion, it is easier to add to change the prompt.
In total, this could be (for the 3rd paragraph)
"[..]Give me the primary degradation peak of each of the four materials, temperature and rate, in a small table, named the way the lab overlay names them so the committee can line the two up. Then read that table for the committee: how the composite's peak mass-loss rate stands against each precursor before and after an adsorption cycle, where the composite peak sits relative to the two precursors and which precursor its decomposition looks more like, and how far the peak moves after adsorption in degrees, what is driving that, and whether it really shows the material breaking down earlier. Close with the handling and regeneration ceiling for the material once we get it back, weighed against what the trade group's note claims, and how much that leaves you trusting our own reading.[...]"

GUI pressure is there, but could be more emphasized.

Input files:
In Thermal_Screening_Note.pdf:
It states the opening water-loss step is complete by 150 °C in all four runs. This is technically not the case: In CTSAgn_After.xlsx and Agn.txt the DTG is still descending at 150 °C until about 185 °C or so. The notes are therefore not quite correct and should be changed. For instance "The bulk of that step is over by 150 °C in all four runs, though a declining tail persists to roughly 185 °C in the alginate and post-adsorption composite runs; a primary degradation peak is nonetheless read above 150 °C and the opening step is left out of the selection."

Rubric: 3/5
C17:
The criterion does not check for the ($/g) values in the corresponding column (the corresponding values are completely unchecked). Change this, e.g., into:
"The CTSAgn row of Adsorbent_Cost_Comparison.docx reports its Cost ($/kg) cell and its Cost ($/g) cell each within ±0.5% of the corresponding expected file and takes its Capacity (mg/g) cell from the released-batch capacity, matching the corresponding expected file."

C19:
This one checks for presence only but not for the correct content of these cells. As there are already 30 criteria, the correctness check (which has to be somewhere) can be combined with this criterion, e.g.:
"The benchmark table in Adsorbent_Cost_Comparison.docx presents all five adsorbents, each on its own row, with all six column headers and units as shown in the corresponding expected file, and reports each of the four non-CTSAgn adsorbents' Cost ($/kg) and Capacity (mg/g) cells within ±1% of the corresponding expected file."
Note that this should normally be split into separate criteria but due to the criterion number constraint it is deemed ok in this case.

C13/C25:
The prompt says "Close with the handling and regeneration ceiling…" and "Finish with an adoption call." Criteria 13 and 25 check for content but not for placement.
and
C13/22:
Criteria 13 and 22 grade the same handling/regeneration threshold at ±2 °C and ±1 °C which is inconsistent.
C13 (and similar for C25) could be changed into
"Thermal_Stability_Assessment.pdf identifies the recovered composite's handling/regeneration screening threshold within ±1 °C of the corresponding expected file, stating its operational mass-loss definition, the limitations on what the threshold establishes, and how that threshold weighs against the trade-association note's regeneration figure, and places that passage as the final substantive text on the page, consistent with the corresponding expected file."

C20
This one has no anchor (i.e. is not compared to expected file).

Verifier\Initializer: 3/5
The new file (Regeneration_Guidance_Bulletin.pdf) was missing in the initializer (this seems trivial but can cause a lot of problems in later stages of the task pipeline).

Quality: Overall Task

2

Quality: Instruction Following

no

Overall Task Feedback

Dear reviewer, good effort in trying to fix this task. However, this task was already marked by QC as a Fail, and I also need to flag that it failed at stumping the model: the Agent Run scored 96%. Please make sure to click Run / Re-run Agent Run before submitting next time, especially after making major changes.

Prompt

Some parts are still too prescriptive and checklist-like, especially the thermal-analysis paragraph. Some wording is leading, such as whether it really shows... or how much that leaves you trusting....
The prompt directly reveals the released-product basis, removing a decision the agent could derive from the inputs and making the task easier.
GUI pressure was improved and is generally fine.
Input files
Thermal_Screening_Note.pdf says Alignate precursor, while the GTF uses Alginate precursor. Agn.txt had too much metadata removed. The Sig1–Sig6 headers are gone, so the column structure must now be inferred from the other files.

The previous water-loss-tail issue and missing Regeneration_Guidance_Bulletin.pdf appear to be fixed.
Although some previous input/prompt issues were corrected, some fixes were incomplete or introduced new issues.
GTF

The main issue is that the peak annotations in Thermal_Stability_Assessment.pdf use the trace colors, while plot_template.xcf requires the template font color #15295d. This creates a direct conflict between the prompt/template and the GTF. Peak labels use inconsistent decimal precision.
Adsorbent_Cost_Comparison.docx has inconsistent heading styles and number formatting.
The benchmark table uses 9.5 pt text while the prompt establishes a 10 pt floor.
Rubric

C3: wrong categorization. It mixes page count with font/margin requirements and overfits to the expected file instead of the prompt's 10 pt / 2.5 cm values.

C12: requires the operational mass-loss definition, which the prompt does not explicitly ask to restate. It also mixes correctness with placement.

C13: curve shapes and relative vertical scale faithful is too vague and lacks an objective comparison mode.

C14: any clear marker glyph is subjective.

C16: improved and now checks numerical values, but it is overloaded, checking five rows, six columns and all numerical cells in one criterion.

C19: immediately under the benchmark table does not match the actual GTF structure.

C21: overlaps with other handling/regeneration criteria and references the benchmark table's stated regeneration assumption, although that assumption comes from the input CSV.

C23: uses unnecessary negative framing with not rejected-batch capacity.

C24: bundles too many independent checks and overlaps with C21.

C26: major issue. It combines trace separation, legibility, distortion, font colors and trace colors. It also anchors font colors to the expected file, creating the conflict with the template.

C26/C27: redundant, since both grade plot legibility and distortion.

C30: wrong categorization. Typography and margins are being graded as a format_gate.

Some of your previous rubric fixes addressed the original issues, but several were incomplete or solved one problem while introducing another type of issue.

Agent Run

I ran the agent since a run was missing (please mark as 'No' next time you don't run the agent run), and I got 96%, which means the task is still too easy and does not stump the model. This task must be redone from scratch, adding more complexity. You can use our guidelines on how to stump the model and use examples from there.
Also I will share with you the previous QC feedback :

Rubric

Framing — FAIL
At least 1 criterion is negatively framed and does not fall under one of the 2 valid negative conditions.

Says "not rejected-batch capacity."
The rubric has already stated what should be used, so this negative framing is unnecessary.
Atomicity — NON-FAIL
15% or less of the criteria have minor atomicity issues.

Criteria 12 and 24 should each be split into two criteria.
Criterion 29 could be split into three criteria.
Coverage — FAIL
At least 1 explicit primary prompt request is not covered by the rubric, meaning a clearly wrong answer could still pass.

The prompt explicitly states that the plot template updated.xcf file must use amber and blue trace colors. This requirement is missing from the rubric.
The prompt also states that the materials must be appropriate for a 10-minute committee meeting. The rubric does not evaluate the length of the materials or their suitability for the intended audience/meeting duration.
Categorization — NON-FAIL
Less than 15% of the criteria have an isolated category/type issue with no gating impact.

Criterion 30 should be categorized as Visual.
The spec defines the format gate as: "Basic file characteristics and metadata (e.g. file names, file types, page/slide counts)."
JSON / Technical Structure

JSON Structure — FAIL
The verifier or task initializer JSON has an incorrect structure.

Both the verifier JSON and input JSON are missing a closing bracket.
The golden file links in the task do not match the final links in the spreadsheet.
Golden Files

Gold File Accuracy — NON-FAIL
The content and values are substantively correct, but there is a minor formatting inconsistency.

The prompt says to use plot_template.xcf as guidance, which uses blue and amber.
The chart in Thermal_stability_assessment instead uses green and red.
Rubric Accuracy

Rubric Accuracy — FAIL
At least 1 criterion contains an objective inaccuracy.

Criterion 18 is inaccurate because the prompt explicitly states that the colors are changing and therefore should not be taken from the old template.
Input Files

Input Consistency — NON-FAIL
One or two secondary gold values are not directly traceable to the inputs, although the core deliverable can still be derived correctly.

The CB states that Regeneration_Guidance_Bulletin.pdf "quotes a much higher blanket regeneration figure for this class of media."
This statement also needs clarification: "For the recovered material, 5% of the mass remaining at 150 °C has been lost by approximately 195 °C under the nitrogen ramp."
Prompt

Clarity / Specificity — NON-FAIL
The prompt is solvable with one valid interpretation, but it could be clearer.

The prompt should be written in a more concise and organized way.
Its current structure is distracting and requires multiple reads to fully understand.
Again, thanks for the effort, but learn from this feedback, and I recommend doing this task again from scratch. Keep it up
