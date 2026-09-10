# Glossary

## General terms

**Model**
*What it means:* The AI system itself; the thing that reads text and images and produces an answer.
*In this project:* "Model" and "AI" are used interchangeably.
*Be careful with:* The model is what we are testing. Our goal is to build tasks it cannot do well.

**Agent**
*What it means:* A model that can also act: open files, click things, run programs, save documents. A plain model only writes text back to you; an agent can operate a computer.
*In this project:* "The agent" and "the model" are used for the same thing, because the model we test is working as an agent inside the VM. If you see "agent run", it means the automated attempt where the model tries to complete your task.

**Prompt**
*What it means:* The instruction given to a model. In everyday use, anything you type into a chat window to an AI.
*In this project:* The prompt is the request that the agent receives, written as if a real person were asking. It is one of the things you create, and it must read naturally (see natural).

**Stump / model-stumping**
*What it means:* To defeat the model: to build a task it cannot complete correctly.
*In this project:* A task is generally considered successful when the agent's average score is below 65%. A task the model solves easily does not give useful training data.

---

## The task and its parts

**Task**
*What it means:* The whole unit of work you claim, complete, and submit. It contains the prompt, the files, the rubric, the VM, and the agent run.
*In this project:* One task ID identifies all of it, but the ID visible to you inside the task is unique to this particular attempt.

**Virtual machine (VM)**
*What it means:* A computer running inside another computer. It gives a separate environment where files can be opened, edited, and saved without affecting your own system.
*In this project:* The VM is a section inside the task. It runs Ubuntu, and it is where the agent does its work with the prompt and the files. It is also where you build and save your own output files.

**Ubuntu**
*What it means:* A free operating system, in the same family as Windows and macOS but built on Linux. It looks a little different, but it has the same familiar pieces: a desktop, a file manager, folders.
*In this project:* The VM runs Ubuntu, so the software inside it is the Linux equivalent of what you may be used to — LibreOffice rather than Microsoft Office, for example. Files saved to the Desktop are what the verifier looks for.

**Graphical user interface (GUI)**
*What it means:* A visual way to interact with a computer. Instead of typing text commands, you click or tap on pictures, icons, and buttons.
*In this project:* "GUI actions" means real manipulation of a program's interface — cropping an image, changing a slide background, formatting cells, building a chart. This is the heart of the project.
*Be careful with:* Simply reading text off an image is not a GUI action. Basic OCR (a computer recognizing letters in a picture) does not count.

**Initializer**
*What it means:* The tool that sets the task up and loads the starting files into the VM.

**Verifier**
*What it means:* The part of the system that checks your task is internally consistent before the agent ever runs.
*In this project:* It does two jobs. First, it maps each expected file to the path it should appear at on the VM and confirms the file is actually there. Second, it loads your rubric and checks that your expected files satisfy every criterion. The second job is your safety net: a criterion your own expected file cannot pass is a broken criterion, and the verifier catches it here rather than at audit or after a wasted agent run.
*Be careful with:* The verifier checks your files against your rubric. It says nothing about how well the agent performed — that is the judge.

**Agent run**
*What it means:* The automated attempt in which the model tries to complete your task.
*In this project:* Afterwards, you get a score and a per-criterion breakdown.

**Judge**
*What it means:* The automated system that compares the agent's output files against your expected files, criterion by criterion, and awards the points.
*Be careful with:* The judge is not perfect. It sometimes marks a correct answer wrong, or a wrong answer correct. If a result looks strange, inspect the actual output files before accepting the score.

**PII (personally identifiable information)**
*What it means:* Any information that could identify a real person: names, addresses, emails, phone numbers, ID numbers, faces.
*In this project:* Never put real PII into a task — not in prompts, files, or screenshots. Invent fictional people and data instead.

**Open source / CC-compliant**
*What it means:* Material that is licensed for reuse. CC stands for Creative Commons, a family of licenses with different conditions attached.
*In this project:* Only CC0 material may be used. CC0 means the creator has waived all rights, so the work can be used freely and no credit is required. Most other Creative Commons licenses (CC-BY and its relatives) require you to credit the creator, and once material is used in training there is no way to attribute anything — so a file can be genuinely free, openly published, and still not usable here.
*Be careful with:* "Freely available on the internet" is not the same as CC0, and neither is "free to download". Check the license before you use anything, and record where it came from.

---

## Files

**Input files / starting files / starter files**
*What it means:* The files that are given to the agent at the start. The raw material it works from.

**Output files**
*What it means:* The files the prompt asks the agent to create.

**Ground truth file (GTF) / expected file**
*What it means:* The output file created by you, the contributor. It is the answer key: the correct version against which the agent's attempt is compared.
*In this project:* Write "expected file" in rubric criteria, not "GTF" or "ground truth". They mean the same thing; "expected file" is the wording we use.
*Be careful with:* Expected files must never be given to the agent as starting files. That would hand it the answers.

**Initial Output files**
*What it means:* A pre-filled output file that came with a seeded task, before you did anything.
*Be careful with:* These were previously called "gold files", and you might see "gold" written here and there. Because "gold" has meant different things at different times, prefer the precise names: Initial Output file for the pre-seeded one, expected file or GTF for the one you made.

**Artifact**
*What it means:* A general word for any file produced as part of the work.
*In this project:* When someone says "the artifacts", they usually mean the output and expected files together.

**Rendered**
*What it means:* How a file actually looks when opened and displayed, as opposed to the raw data inside it.
*Be careful with:* A PDF can contain text that looks perfect on screen but extracts as nonsense, and the reverse is also possible. When checking visual quality, open or render the file — do not judge it from extracted text.

**Backticks**
*What it means:* The ` character, used to wrap a filename so it stands out as a filename.
*In this project:* Always put filenames in backticks in the rubric.
*Be careful with:* It is a small thing, but it saves auditors a lot of tedious editing later.

---

## The rubric

**Rubric**
*What it means:* A scoring guide: the standard against which work is judged.
*In this project:* The rubric is one thing — the whole scoring guide for your task. Inside it are items, also called criteria (one of them is a criterion).
*Be careful with:* You have one rubric containing many criteria. There is no such thing as "a list of rubrics" for a single task. Say "the rubric has 24 criteria", not "the task has 24 rubrics". Rubric formats vary a lot between projects, so if you have worked elsewhere, expect ours to differ.

**Criterion / item**
*What it means:* One single check inside the rubric. It describes one thing the judge should look for in the output.

**Weight**
*What it means:* How many points a criterion is worth.
*In this project:* Heavier criteria matter more to the final score.

**Category / scoring area**
*What it means:* Which kind of thing a criterion is checking.
*In this project:* We use three. format_gate: structural requirements — the required filenames and file types, and non-visual structural counts such as slide count or page count. correctness: is the content right? Values, findings, classifications, headings and labels. visual: does it look right? Layout, legibility, colors, images, charts.

**Criteria type**
*What it means:* MUST-PASS or REGULAR. A must-pass criterion is a gate: fail it and the whole attempt fails.
*In this project:* Must-pass is reserved for the file-name and file-type gates. Not every format_gate criterion is must-pass.

**Atomic**
*What it means:* Testing one thing at a time, so that a pass or a fail has a single clear meaning.
*In this project:* This is the clearest example of a word that shifts between projects. On some projects, "atomic" means as small as a single spreadsheet cell. Here it is looser: one element, one category. A whole table, or a set of values belonging to the same dimension, can be one atomic criterion. You do not need to split every value into its own item.
*Be careful with:* The opposite problem is a stacked criterion — one item bundling two unrelated checks. That becomes unfair because the agent can do one of them correctly and would still score zero.

**Anchored / GT-anchored**
*What it means:* A criterion that tells the judge what dimension to compare and leaves the actual answer in the expected file.
*In this project:* Write "reports the cleaning counts matching the values in the expected file", not "reports that 4 rows were removed, leaving 600".
*Be careful with:* The judge already has the expected file. Writing the answer into the criterion is leakage.

**Leakage / hard-coding**
*What it means:* Writing answers taken from your expected files into the rubric: counts, dates, colors, names, values — even helpfully, in brackets.
*In this project:* Not allowed. The only exceptions are output filenames and prompt-specified structural counts such as "exactly 5 slides".

**Weight** *(tolerance)*
*What it means:* How much difference is still acceptable ("within ±1%", "within 0.5 percentage points").
*In this project:* Tolerances belong in the rubric, not in the prompt. The exact margin of error depends on the original value and how the request is phrased in the prompt.
*Be careful with:* A real person asking for a report does not specify a percentage tolerance, so putting one in the prompt makes the request sound artificial. The rubric generator occasionally creates items with margins that require editing - remember that the margin of error has to be realistic: if the rubric item is "includes 4 slides", you can't set a tolerance level of "+/- 4%".

---

## Words that turn up in feedback

**Granular**
*What it means:* Broken down into small, separate pieces. It comes from the same Latin word as "grain," as in "grains of sand". The more granular, the smaller the grains.
*In this project:* "More granular" means split this into smaller parts. "Too granular" means you have split it too far.

**Scope**
*What it means:* How much ground something covers.
*In this project:* "Out of scope" means outside what was asked. "Scope creep" means the rubric demands more than the prompt actually requested.

**Natural / naturalness**
*What it means:* Whether the prompt reads like a genuine request from a real person, rather than a test written for a machine.
*Be careful with:* Mentions of rubrics, tolerances, or scoring make a prompt sound unnatural. Asking the model to take on a persona is unnatural, but assigning a persona to yourself is fine.

**Deterministic**
*What it means:* Having exactly one correct answer that can be computed or checked. The opposite is open-ended, where several answers are equally valid.
*In this project:* Open-ended requests are allowed, but the rubric must then define the acceptable parameters rather than demand the exact solution in the expected file.

**Sanity check**
*What it means:* A quick, common-sense look to see whether a result is plausible before trusting it.
*In this project:* "No sanity check was performed" means someone accepted a number without asking whether it made sense.

**Edge case**
*What it means:* An unusual situation at the boundary of the rules, which the normal instructions do not clearly cover.

**Overflag**
*What it means:* When an automated checker reports a problem that is not actually a problem.
*In this project:* The linter overflags fairly often. You may push back rather than rewriting good work.

**Linter / eval**
*What it means:* Automated checkers that inspect your prompt or rubric and report suspected problems.
*Be careful with:* They are advisory, not authoritative. They sometimes contradict each other, and they lag behind policy changes. If a flag is wrong, say so and explain why.

**Trajectory**
*What it means:* The path the model took to its answer, rather than the final files.
*In this project:* The rubric grades only the final files, not the trajectory. This is why the output has to be rich enough that different kinds of failure look different in it.
*Be careful with:* When an error in reasoning and an error in visual inspection lead to the exact same mistake in the output files, the task becomes less useful as training data for the model.

---

## People and working with the team

**CB**
*What it means:* Contributor, i.e. you!
*In this project:* This project has several different domains, and therefore has contributors with different types of specialized domain knowledge.
*Be careful with:* If you get a task that is outside your domain - skip it. If you keep getting tasks from the wrong domain, tag a QM in the chat, or write a dm.

**QM**
*What it means:* Queue Manager. They do many things on the project, such as conducting audits, hosting webinars, assisting in the war room, and updating instructions. They are your point of contact with the team and the ones you turn to with questions and issues. Don't worry about finding the "correct" QM just because you belong to a specific domain speciality - general tasking questions can be handled by any of the QMs, and if it's a domain-specific question, they'll pass it along to the right person.
*In this project:* If something in a task is unclear, these are the people to ask.

**Review**
*What it means:* A reviewer auditing a completed task in detail and giving it a score of 1-5.

**SBQ ("send back to queue")**
*What it means:* A task that is not approved and instead sent back to be reworked.
*In this project:* These tasks are returned to the general task pool. If you receive such a task, read the feedback carefully!
*Be careful with:* An SBQ is not a judgment of you; it means that the task requires more edits than a reviewer has time for.

**Task limit**
*What it means:* A cap on how many tasks you can hold at one time.
*In this project:* New contributors start with a limit, which lifts as you build up completed, audited work. If you have reached your limit and are not sure why, ask a QM.

**Downtime/EQ (empty queue)**
*What it means:* A period when there are no tasks available to claim.
*In this project:* This happens from time to time and does not mean anything is wrong with your account.

**Outlier Community (OC)**
*What it means:* The forum where contributors and the wider team talk. It has channels for individual projects, and you can also send direct messages to people, including QMs.
*In this project:* This is where to ask questions, report problems, and check whether others are running into the same issue.
*Be careful with:* If you are stuck, asking in the project channel is usually faster than working around the problem on your own.

**War room / WR**
*What it means:* A live help session on Zoom to get guidance while you are working on a task.
*In this project:* The war room is open 24 hours a day, with a new link each day. You find the link in your dashboard, and it is usually posted in the OC channel as well. It is often easier to help out in the war room than in the OC chat, since our tasks are so complex.
*Be careful with:* We strive to have QMs in the war room at all times, but some time slots are difficult to cover. If someone is there but it's quiet, it is better to unmute and say hello than just write in the chat. If nobody is there, try tagging a QM in the OC channel; whoever is online can meet you in the war room and guide you through most issues.
