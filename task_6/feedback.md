Improve the task per the following feedback:

Quality: Overall Task

3

Quality: Instruction Following

yes

Overall Task Feedback

Dear contributor, good work overall. There are some minor fixes needed before sending the task forward. Some sentences from the prompt are removed which are making it overly prescriptive like the explanation after the sentence to match the layout of figure.
Rubric:
C8, C9, C14, C15: These are numeric-match criteria with no stated tolerance.
C28 - miscategorized: Page count should be categorized as "format_gate".
C23 - somewhat brittle: The requirement that the content be "clear of traces/other labels" can be satisfied by multiple valid layouts, so requiring it to match the expected file may incorrectly penalize a differently arranged but equally clear placement.
Coverage gap: There is no criterion testing the explicit requirement that no heading should be stranded at the foot of a page.

GTF:
The template comment and the prompt require the figure to be "sized to the text width". The image is currently inserted at 7 inches wide, but the document was changed to landscape orientation to accommodate the wide performance table. As a result, the text column is now approximately 9.6 inches wide, meaning the figure occupies only around three-quarters of the available width and appears undersized. The 7 inches width appears to be the original portrait layout value and was not updated after switching to landscape.
Minor: The conclusion asks "How much more modelled height the reduced sulfur carries than the oxidised sulfur". The response gives this as a ratio. This is arithmetically correct, however in everyday usage, "how much more" can also imply a difference. Both interpretations are defensible, so the prompt should clarify to explicitly request either the ratio or absolute difference to avoid ambiguity.

Quality: Overall Task

3

Quality: Instruction Following

no

Overall Task Feedback

Dear contributor, thanks for the work you put into this one. The overall quality score is 3/5, so it does not pass in its current state.

Some of us reviewers received the assignment to grade tasks exactly how QC would, based on QC specs, so scores will likely be more severe and less tolerant of mistakes. I am sorry about this situation, but these are the instructions we must follow to reach the QC stage with the best possible quality.

What went wrong
There are coverage gap in the rubric. The prompt closes the figure paragraph with "Then place the finished figure in the record where the template marks it", and your own artifacts back that up. Analysis_Record_Template.docx has a paragraph reading "Place the finished figure in here." sitting right above the caption "Figure 1. Sulfur 2p region and column performance.", and the GTF XPS_Analysis_Record.docx embeds the figure exactly there, filling a full page out of three. No criterion tests it. I swept all 30 titles and not one contains the words figure, image or embed. So an agent that builds a perfect XPS_Sulfur_Region.pdf and never inserts it, leaving that placeholder line under a numbered caption, still passes every criterion you wrote. C4 is the closest miss, but it only asks that the document "opens with no tracked change left pending and no review comment left in the document", so deleting the comment that reads "Drop the finished figure in here." satisfies it without the work being done.

There is a trap in fixing that. C25 and C26 say the same thing about two different tables and merge cleanly into "Every table in XPS_Analysis_Record.docx shows every column in full on the page with all cell text legible at normal viewing size, matching the corresponding expected file", which leaves room for the figure criterion.

The second fail is framing. C22 reads "In XPS_Analysis_Record.docx, no section heading is left stranded at the foot of a page as in the corresponding expected file". A criterion has to state what the output does rather than what it avoids, and the exemption for absence wording only applies when the prompt asks to omit something. Your prompt asks for a layout fix, not an omission, so the exemption does not reach it.

Answer leakage, scored 3. The prompt asks for "how much more modelled height the reduced sulfur carries than the oxidised sulfur (as a ratio)", which presupposes that reduced is the larger of the two. That is one of the four findings C10 grades, and your GTF states it as a conclusion, "Reduced sulfur dominates the surface". The magnitude is not given away, so this stays minor, but phrase it neutrally as "the ratio of reduced to oxidised modelled peak height". The same pattern shows up in "pick out any negative removal in red", which quietly tells the agent that negatives exist.

Robustness, scored 3. C28 reads "The peak assignment and column performance sheets of Speciation_Summary.xlsx are set to print on a single page" and carries neither a legibility clause nor an expected-file anchor, unlike its siblings. An agent can force nine fields onto one page by dropping the print scaling and pass the check while producing an unreadable printout. Add "with all cell text legible at normal viewing size".

Realism, scored 3. The prompt pins the numeric method from end to end: window, polynomial order, boundary handling, the tie break, the not-resolved fallback, the half-limit convention and the rounding for every quantity. Each one is defensible alone, and your notes explain why you added them. Together they read more like a procedure than a request from a colleague. This is the hardest of the five to act on, because the pinned window is load-bearing by your own account and it is also what keeps the task clear, so trim it carefully and leave it for last.

What went well
The analysis is genuinely well built and the GTF is accurate. I re-derived every graded number from the raw inputs independently and it all reproduces: the Savitzky-Golay column to thirteen decimals, all six peak assignments with their offsets and amplitudes, the failure day at 458, and every value in the performance table including the half-limit substitutions and the dropped incomplete days. That is rare, and it is the strongest part of this submission.

The design choices behind it hold up too. Choosing a five point window so all six references resolve was the right call, and two of those six assignments land on genuine equal-distance ties, which means your "take the taller one" rule is actually exercised rather than decorative. The failure day is unambiguous, with the treated effluent at pH 4.39 on day 452 and below 4 for every sample from 458 onward. The two panel figure is clean, the species labels are moved clear of the traces with leader lines, both twin axes carry their own labels and ticks, and the failure-day callout is readable. The Read Me tells the agent which column is feed and which is treated effluent instead of leaving it to guesswork. On the rubric, weight shares are in band, the three must-pass gates are proper file checks, and the category tagging is clean across all 30.

Closing
You asked for tips on making tasks harder. One signal from this attempt: the single run that got scored reached 95.3 per cent, so the difficulty is probably not yet where you want it, although one run is thin evidence. Difficulty tends to come from visual and layout work rather than from more pinned arithmetic, so the label decrowding and the page setup are the right places to lean, not the numeric spec.

Consider also offloading the requirement charge of the prompt to an auxiliary input file; that way you would have a better prompt and still complex enough.

Fix the two rubric items, disambiguate that one background sentence, and this becomes a strong task. The hard part is already done, and done well.
