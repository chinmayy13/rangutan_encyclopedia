# Frequently Asked Questions

*Orangutan Encyclopedia*

This is a collection of some of the common questions we get from contributors.
Is your question not in the list? Please fill out the form **here** with any questions you have about the guidelines, workflow, task interface, or related topics.

---

**Topic:** GTF files
**Question:** When editing the starter files, is it ok to switch to other file formats than the originals? If the task originally has a pdf and a docx, can I change this so my new GTF files are a png and a pptx?
**Answer:** Yes, this is fine! As long as all links and references are edited as well (for example, referring to the correct, new file types in the prompt request), the file types can be changed.

---

**Topic:** GTF files
**Question:** What is the difference between Gold Files and Ground Truth files? Sometimes in the documentation, the terms are used interchangeably.
**Answer:** "Gold files" is a term that has been confusing, since it is used for both the initial input files and the GTF files. We are trying to remove this term from the instructions to make it less confusing, so if you encounter this term somewhere, please flag it to a QM so we can update the instructions.

---

**Topic:** Starter files
**Question:** Reviewer stated that CC-BY licensed papers are not acceptable. I don't see any such information in the instructions. CC-BY license specifically mentions that the unrestricted use is permitted if the original author and source are credited (not hidden).
**Answer:** The files used in the project need to be "open source CC compliant (free for use, fully public license - NO ATTRIBUTION)". This means that CC-BY files are not allowed, since they require attribution.

---

**Topic:** Prompt
**Question:** Are there hard rules for what can be included in a "natural" prompt, like bullet points, file names etc?
**Answer:** It is difficult to define a natural prompt, and we are working on a set of good prompts to provide as examples, to make this easier.
Generally, bullet point is not very natural, but having a short bullet point list in an otherwise natural prompt is not the end of the world.
Focus on the overall impression of the prompt: what would you write to an LLM in your day-to-day work? It is rare that people spend effort on neat formatting on a prompt in real life.

---

**Topic:** Prompt
**Question:** How descriptive/specific can I be in the prompt and still have it be considered "natural"?
**Answer:** This is also a difficult thing to pin down in an exact, always-valid way. But a couple of guidelines are:
- If you would spend so much time and effort specifying exactly how the model should carry out the work that it would almost be as fast doing the work yourselves, it is overprescriptive.
- If the model doesn't have to ever think "hmm, what is the best way to produce this result?" it is likely overprescriptive.
- In a real-world situation, you are likely most interested in the result, not the way the model creates it. That is kind of the point of using an AI, right? Try to write outcome-focused prompts where you nail down what you want in the end result, and leave it up to the model to figure out how to deliver this to you.
- Sometimes that means that you have to widen the rubric items to allow for several, equally valid solutions, and that is fine. Example: "Please make sure the chart is readable for people with colorblindness" - this can be solved with choosing appropriate hues, or adding textures, or choosing colors with contrasting values, or all of these combined. Make sure the rubric rewards all of the appropriate choices.

---

**Topic:** Rubric
**Question:** If the prompt asks for 30 things, how can I cover this with the rubric? Or should I limit the prompt?
**Answer:** This depends on what you mean by "30 things". If you ask for a spreadsheet with more than 30 values, this is fine (see the next question). If you ask it to do 30 separate things, all of which are individually visible in the result and not interdependent, then yes, you should limit the prompt!

---

**Topic:** Rubric
**Question:** How do I write atomic rubric criteria when the limit is 30?
**Answer:** It is important to distinguish between individual data points, and different dimensions. If you ask for the average patient mortality for 30 different diagnoses, these are 30 data points but only one dimension, and can be covered by just one rubric item.

---

**Topic:** Starter files
**Question:** My task includes files where the previous CB have used their own proprietary work, can I use this?
**Answer:** Save the task id, skip the task, and flag to a QM

---

**Topic:** General Outlier Questions
**Question:** Can I task from a different country?
**Answer:** In order to task from a different country, you need to submit a travel request beforehand. If you haven't done this, and task from abroad, this risks getting flagged as potential fraud.

---

**Topic:** Tasking Workflow
**Question:** I get "task limit reached", why?
**Answer:** In order to get unthrottled, you need to have three tasks audited and scored 3 or higher. Until then, you will be throttled to a limited number of tasks.

---

**Topic:** Prompt
**Question:** The seeded prompt in my task has a long list of items/large dataset, can I put these in a file and add this to the starter files, so the prompt is more concise and natural?
**Answer:** Yes, this is a great idea!

---

**Topic:** VM
**Question:** I have trouble with the VM - it won't connect/I get an error message
**Answer:** Make sure all upstream steps are saved properly, and try refreshing the page. If you still have issues, please visit the war room to get further guidance. You can also try pausing the task for a while and then refresh - the VM issues tend to fluctuate. If nothing works, and the time is running out: document everything (task id, time spent) and submit a ticket to support for the time worked.
It is also a good idea to save the work you've done to your personal notes - the task might end up in your hands again at some point.

---

**Topic:** Starter files
**Question:** I get "Access denied" when I click on the link for the starter/initial output files.
**Answer:** These links are connected together to one (non-functional) link, and have to be separated. Copy the entire link to Notes or some other text editor, and divide them up. They are structured like this: link%22,%22link%22,%22link - remove the "%22,%22" section and replace it with a space. This should give you separate, functional links.

---

**Topic:** Prompt
**Question:** Can a prompt ask for VS Code Settings or Extension changes and grade the resulting configuration files?
**Answer:** No, his is too simple, and difficult to verify in the outcome.

---

**Topic:** Tasking Workflow
**Question:** No one is present in the War Room.
**Answer:** We strive to have someone in the War Room at all times, but sometimes there are gaps in coverage

---

**Topic:** Tasking Workflow
**Question:** How does the pause time work in relation to the submission deadline?
**Answer:** When the task is paused, the deadline is pushed forward.

---

**Topic:** GTF files
**Question:** Should output files be renamed in the prompt because of unnatural-sounding names?
**Answer:** Yes, this is preferable, but make sure that this change is implemented everywhere: in the actual files, in the rubric items, in the prompt, and in the Initializer&Verifier.

---

**Topic:** Other
**Question:** What info should I include when I flag issues?
**Answer:** Always include the attempt id, and screenshots of the issue, with as much context included as possible.

---

**Topic:** Other
**Question:** The pre-seeded task domain is different from mine - can I still proceed?
**Answer:** If you feel comfortable with the domain, you can go ahead, but otherwise skip it. If you keep getting tasks from the wrong domain, please tag a QM about the issue.

---

**Topic:** Other
**Question:** My task has blocking issues that prevents me from submitting it, and it is about to expire, what can I do?
**Answer:** Take screenshots and save the task id, so you can submit a ticket to support for the time worked. It is a good idea to save the work you've done on the task in your own notes, in case the task ends up with you again at some point.

---

**Topic:** Prompt
**Question:** Must a prompt explicitly name every file contained inside a required ZIP archive?
**Answer:** No. Naming the final archive and clearly specifying its required contents or goal can be sufficient.

---

**Topic:** Prompt
**Question:** Should my prompt include a margin of error for visual spacing or layout?
**Answer:** No, this is not very natural, so reserve this for the rubric items.

---

**Topic:** Starter files
**Question:** What should happen when seeded or inherited artifacts are incorrect?
**Answer:** In this case, you can either edit the files or replace them. Note that it is fine to have synthetic/CB-created files as input files, but it becomes problematic if the content goes against known domain facts, since the model will have to choose between trusting the input file or trust its own training data, which is not a valid model challenge.

---

**Topic:** Rubric
**Question:** Is a rubric allowed to hard-code the real answers, even as clarification?
**Answer:** No. Counts, dates, colors, values, and enumerated answers should not be leaked into criteria even as parenthetical clarification. These criteria should anchor correctness to the expected file without revealing its answers.

---

**Topic:** Tasking Workflow
**Question:** I don't see the new GTF eval in my task(s), but I get the agent run. What should I do?
**Answer:** Flag the task to a QM. Skip the agent run, and use the external GTF eval.

---

**Topic:** Other
**Question:** I get tasks in a domain that is connected to a skill that I have, but it's not my main skill and I would prefer not to get these.
**Answer:** You can archive the skill (it can be restored at any time). Go to the Skills section in your dashboard and click Edit, and choose which skill to archive.

---

**Topic:** GTF files
**Question:** Which file formats can we ask the model for as output?
**Answer:** The currently supported formats are .docx .pptx .pdf .zip .blend .tscn .escn .tres .godot .gd .scn .res. Extensions which are not in this list, such as .txt files or videos, are evaluated on a best-effort basis by the agent judge. If you have ideas for other formats, please let us know!

---

**Topic:** Other
**Question:** I still get "task limit reached", when can I continue tasking?
**Answer:** You can read all about the task limit in the post "How to Become a Trusted Reviewer"

---

**Topic:** Starter files
**Question:** I am trying to download a starter file that is a .txt/.R/.Py/.md/other text-based file type, and it doesn't initiate a download, it just sends me to a webpage.
**Answer:** Right-click anywhere on the page and choose "Save as". Verify afterwards that it is saved with the correct file extension.

---

**Topic:** Other
**Question:** I accidentally chose "Save and Regenerate" after editing the prompt, and now everything after the prompt is gone.
**Answer:** Step one is to save your edited prompt in external notes. After that, you can choose "Abort changes". This will reset the task to its original state. If you have made edits to other sections of the task, like the rubrics etc, and then accidentally regenerate, those edits can't be restored.

---

**Topic:** Rubric
**Question:** It says Budget Exceeded in the rubric generator
**Answer:** Flag the issue to a QM and write the rubric manually.

---

**Topic:** VM
**Question:** The VM lost connection and all the work I did on my GTF files is gone.
**Answer:** This is very unfortunate, but it happens. Try to remember to save to an external app (like Limewire or Filebin) intermittently.
Working outside the VM is allowed, to keep the files from getting lost when it disconnects, but it is crucial that all files are constructed in a way that they look good in the VM, with no functions or file formats that the VM could not have created. Always open the files in the VM, inspect, edit, and save.

---

**Topic:** Other
**Question:** Will users with multiple skills (e.g., Law + CS) be assigned tasks across all domains or restricted to one?
**Answer:** If you have more than one relevant skill, you might get tasks from different domains. If you are not comfortable working in that domain, you can temporarily archive that skill from your dashboard.

---

**Topic:** Starter files
**Question:** Must all input files be in English?
**Answer:** Yes!

---

**Topic:** Prompt
**Question:** Do I have to name the starter files with exact file names in the prompt?
**Answer:** Yes, but try to integrate them in a way that is as natural as possible.

---

**Topic:** GUI
**Question:** How can GUI tasks be designed to ensure the model must use the UI (PG Admin/VS Code) rather than defaulting to command-line solutions? Most SQL tasks can be completed via CLI.
**Answer:** For pgAdmin, the GUI-forcing features are the ERD Tool (arrange tables, export the .pgerd project plus a PNG/SVG), graphical EXPLAIN plan exports, the Dashboard/Statistics charts, and the wizard-driven dialogs — Import/Export, Backup/Restore, Grant. For VS Code, it's the debugger (breakpoints, variable inspection, call stack), the merge-conflict three-way editor, Source Control diffs and hunk staging, the Problems panel, rename/refactor, and rendered notebook or Markdown preview output. In both cases, favour artifacts the tool serializes itself over free-form screenshots: a screenshot can be fabricated without ever opening the app. Phrase the requirement as observe-adjust-re-observe so it isn't scriptable, and pair every GUI ask with a rubric criterion that catches its absence.

---

**Topic:** GUI/starters
**Question:** I received a task where the starter files are only text-based, i.e. .txt, .md and similar - is this allowed, as long as a GUI action is included in the task as a whole, or do I need to add more starters?
**Answer:** The only limitation is that the input can't be only spreadsheets (CSV, xlxs, etc.), and you need at least 3 files as input. Text-only is fine as long as the task is good overall, and has a relevant GUI action. If you are able to achieve that using only text-based input, more power to you.

---

**Topic:** Prompt
**Question:** Is it ok to specifically instruct the model to open an application? For example Blender, PgAdmin.
**Answer:** Try to avoid this, and in general avoid step-by-step instructions to the model. If the thing you want the model to do can only be achieved by one specific application, try to stay output-focused. Instead of "open the document in LibreOffice, check the print view and ensure that nothing is split across pages" just ask "I am going to print this, so make sure nothing is split across pages" - the model can figure out how to achieve it.

---

**Topic:** Rubric
**Question:** I can't pass the rubric step to get to the initializer!
**Answer:** If the rubric is completely blank, you need to fill in a couple of items as placeholders so you can pass the step (and you can of course ignore all linters at this point).

---

**Topic:** Workflow
**Question:** I received a task where it says to improve on the previous contributors task, but there is no feedback.
**Answer:** The tasks in this project have mixed origins, and some have been worked on several times before ending up in your hands. When contributors leave the project, their tasks are sent back in the general task pool, and they appear as "improve this task", but they have never been audited. You need to look critically at the task; it is yours now, and you need to make sure that when you submit it, it is up to your standards, and that it follows all instructions. If the prompt looks unsalvageable in your eyes, feel free to scrap it, same goes for the starter files. Any edits you make need to also be reflected in the GTFs - sometimes there are decent GTFs provided with the files and all you need to do is make minor edits, and sometimes you need to rhrow them out and start over.

---

**Topic:** Verifier
**Question:** The Verifier doesn't have "func": "agent_judge_multi" in the JSON, and the path for expected is also wrong, should I include and change them respectively?
**Answer:** Yes, this needs to be included. See the instructions for how this should be formatted, and please visit the war room if you get stuck.

---

**Topic:** Starter files
**Question:** The initial file of my task does not align with the domain and sub-domain, can I use my own files?
**Answer:** You can always use your own files! But they need to comply with the instructions: CC0 license, at least three files, not only spreadsheet input, etc.

---

**Topic:** Rubric
**Question:** Is it still mandatory to have >=20% visual-criteria weight for code-centered tasks? It is hard to reach that minimum with mostly-code tasks.
**Answer:** Yeah, sorry, we know it's difficult, but that's why we only onboard the smartest contributors.

---

**Topic:** Starter files
**Question:** Where should we upload the initial files if they need to be modified for conciseness?
**Answer:** All initial files, whether they are edited or completely new, should be uploaded in the section right before the prompt, underneath the links to the initial starter files. The links to these uploaded files need to be used in the initializer.

---

**Topic:** GUI
**Question:** Does replicating UI from mockups count as enough GUI steps, or should we add a step like a screenshot on completion?
**Answer:** Yes, as long as the mockup is a visual mockup and not just text based.

---

**Topic:** Prompt
**Question:** Contradiction: docs say always mention input files by name, but recent posts allow implicit referencing - which is it?
**Answer:** The files should be referenced by name, but in a reasonably natural way.
