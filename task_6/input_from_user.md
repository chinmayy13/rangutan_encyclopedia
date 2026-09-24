**Original rewrite**

- The original prompt didn't pin down the analysis at all, so I added the smoothing window, polynomial order, and end handling. That choice matters: a 5-point window resolves all six references, a 9-point window only resolves four.
- Pinned the background line and the peak-matching rule too. Two references sit right between two peaks, so without a rule it's a coin flip.
- Task now uses the whole workbook, not one sheet. The agent has to find the failure day itself from the pH data, halve any below-detection reading, drop incomplete days, and pull values out of the "value ± uncertainty" strings. Two removals go negative after the failure day, that's the real finding.
- Swapped the deliverables to `XPS_Analysis_Record.docx`, `XPS_Sulfur_Region.pdf`, and `Speciation_Summary.xlsx`, since the originals were plain text with nothing to look at.
- Added interface difficulty: the template (`Analysis_Record_Template.docx`) has tracked changes, comments, stale numbers, and a table that overflows the page. `Figure_Layout_Reference.png` forces label decrowding. `Images_XPS.zip` only has peak heights as text printed on images.
- Removed a researcher's name, fixed the Read Me, stripped embedded text from the image archive.

**Second pass, after review**

- Merged two duplicate rubric criteria to free a slot. Added one for the figure actually being embedded, nothing tested that before.
- Reworded the stranded-heading criterion positively.
- Added a legibility clause to the print-on-one-page criterion.
- Fixed two prompt lines that leaked the answer (the ratio direction, the red-formatting hint).
- Moved non-essential method detail (background, search radius, tie-break, half-limit, rounding) into a new file, `XPS_Processing_Notes.pdf`. Kept the window and the failure-day rule in the prompt since those actually decide the answer.
- Still need to fix the figure's size in the docx, it's a leftover from the portrait layout.

**Third pass**

- Found a real bug in the new notes file: the matching step said "background-corrected trace," should be "smoothed trace."
- Rewrote the reflection and background-line rules precisely, and checked them against the raw data rather than trusting the review.
- Fixed real ambiguities: disagree-most is absolute not relative, the ratio is summed not averaged, removal comes from period means not daily averages, the difference is amplitude minus modelled height.
- Added the missing "save to Desktop" line.
- Cut repeated file citations from five down to a couple.
- Kept the panel description and the GUI instruction as written, they already match the guidelines.

**Fourth pass**

- Caught my own inconsistency: moved the processing rules to the notes file but left the reporting rules (subtraction order, absolute vs relative, sum vs average) sitting in the prompt. Moved those too.
- Reverted the prompt's conclusion line back to plain wording.
- Cut the file citations down to one blanket mention.
