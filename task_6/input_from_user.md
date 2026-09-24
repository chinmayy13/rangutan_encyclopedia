**Original prompt**

- The seed prompt didn't pin the analysis, so I added the smoothing window, polynomial order, and end handling since that choice decides which references resolve.
- Pinned the background line and the peak-matching rule for the same reason, two references sit right between two peaks.
- Prompt now pulls from the whole workbook, not one sheet. Agent has to find the failure day itself, halve any below-detection reading, drop incomplete days, and read values out of the "value ± uncertainty" strings.
- Named the deliverables `XPS_Analysis_Record.docx`, `XPS_Sulfur_Region.pdf`, and `Speciation_Summary.xlsx`.

**After review**

- Fixed two lines that leaked the answer: the ratio question no longer implies which species is bigger, and the red-formatting line no longer hints that some removals come out negative.
- Moved non-essential method detail (background, search radius, tie-break, half-limit, rounding) out of the prompt into a new file, `XPS_Processing_Notes.pdf`. Kept the window and the failure-day rule in the prompt since those actually decide the answer.
- Added the missing line telling the agent to save outputs to the Desktop.
- Briefly added extra clarifying words to the conclusions line (absolute vs relative, summed vs averaged), then took them back out since they made the prompt read like a spec. Moved them into the notes file instead and kept the conclusions line plain.
- Cut repeated mentions of `XPS_Processing_Notes.pdf` from five down to one.
- Trimmed the red-formatting line to a single clause.
- Removed em-dashes.
