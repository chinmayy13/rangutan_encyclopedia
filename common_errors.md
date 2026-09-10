# Common Errors

*Orangutan Encyclopedia*

These are some common mistakes that we see when auditing tasks in the project, along with suggestions for a better approach.

---

## Soft configs become hard rubrics

**Description:**
Prompt requests that are open-ended (i.e. where more than one answer/layout/visual representation can be equally valid) are allowed, as long as the correct responses can be specified somehow, but quite often, these are transformed into hard rubric criteria that only allow for the exact solution in the GTF.

**Examples:**
Prompt: *"Create slides with summaries of topics A, B, and C from starter_article.pdf."*
GTF: Has one slide per topic
Model: Has 2 slides for topic A (because topic A has more information in the starter article), and 1 each for B and C.
Rubric: *"Create 1 slide each for topics A, B, and C, matching the corresponding expected file."*

**Why is it a problem?**
The prompt did not specify how many slides per topic, so the rubric can't demand this.

This is different from the more reasonable implicit request that the slides show A, B, and C in that order, since they are mentioned in that order (especially if the original paper has them in that order as well).

The end result of this error is that the agent run percentage might not reflect actual model errors, just differences in interpretation.

**How to do it instead:**
Define the parameters of the correct response and allow for variations within these parameters. In this case, the rubric item should be *"at least one slide per topic"*.

---

## No significant prompt changes

**Description:**
Prompts that have no significant changes from the seed prompt, with the core structure of the prompt being unchanged.

**Examples:**
The prompt has the addition of "save to desktop", and specified file names, and perhaps some surface-level adjustments in phrasing to make it more natural.

**Why is it a problem?**
If the seed prompt is great, this is not a problem. But the seed prompt is never great. A majority of the seed prompts are unnatural, extremely wide in scope, and somehow both overprescriptive and underdefined - some parts describe step-by-step calculations and detailed layout instructions, whereas in another part there are fluffy instructions like "In slide 3, include a discussion about the possible effects of topic A" (effects on what? based on what - the starter file content or an online search? or is the model supposed to independently draw a logical conclusion?), things that are very wide in scope and hard to pin down with rubric items.

**How to do it instead:**
Assume that the seed prompt is bad. The starter files are the important stuff: if they are good, you can rebuild the task on them (although they might need editing and/or the addition of more files), and use the seed prompt as loose inspiration.

Don't be afraid to do drastic changes. Not sure you understand all the intricacies of the files and the seed prompt? Then create a prompt from the parts you do understand!

---

## Changes in the prompt/starter files/gold files with no corresponding rubric changes

**Description:**
The prompt has been edited to be more natural, the scope is narrowed, misspelled file names have been corrected, etc, but the rubric has not been updated to reflect the changes.

**Examples:**
Seed prompt asks for a computation of value X by method A, something that the contributor determines to be too complex, unnatural, or non-deterministic, so they change it to method B. Rubric item is still phrased as "Computes X through method A".

**Why is it a problem?**
The rubric now tests for something that the prompt did not ask for, so the agent run will be low despite no actual model failure.

**How to do it instead:**
Make sure that all changes you make to the prompt (and/or gold/starter files) are reflected in the rubric.

---

## Agent run is < 65%, but the model artifacts should score higher

**Description:**
Agent run gives a falsely low percentage, and this has not been discovered by the contributors.

**Examples:**
The agent has scored against a faulty rubric that doesn't reflect the actual prompt request, or the agent judge has hallucinated errors that aren't there.

**Why is it a problem?**
The prompt is not, in fact, difficult enough for the model, so the task can't be approved.

**How to do it instead:**
Always inspect the generated model artifacts!

---

## Agent run is 0% and no sanity check has been done

**Description:**
The agent run scores 0% but no inspection has been done to verify that this is due to an actual model failure.

**Examples:**
The score is caused by the agent not finding the file, or by the Verifier not being formatted correctly, or by some other environmental failure.

**Why is it a problem?**
There is no actual test of the model's capabilities here. When the environmental issues are taken care of during audit, there is a risk that the agent score is > 65%.

**How to do it instead:**
Always look at the actual detailed result of the agent run, not just the score.

---

## Quantity over quality

**Description:**
The prompt asks for big artifacts, or processing of large amounts of data, or for the model to follow a loooong multi-step instruction, but there is no actual model challenge.

**Examples:**
The gold file is a 50-page pdf, but each page is created in the same way (like presenting statistics for 50 different countries in the exact same way) so there is no added difficulty compared to creating just one single page.

**Why is it a problem?**
This type of bloat slows down processing, requires a larger rubric, is tedious to audit, and provided no additional model challenge or quality to the task.

**How to do it instead:**
Focus on quality - it is better to ask for a complex pdf where the model has to use reasoning in order to construct it than one with 50 pages with just easily extracted data.

---

## No GUI action

**Description:**
The prompt only asks for things than can be achieved with code alone, no need for visual inspection.

**Examples:**
Asking for specific colors, font size etc - this does not require visual inspection. Asking the model to inspect the output files to make sure they don't cut off tables between pages or similar things - this would require GUI, but there is no way to know if the model actually did the inspection or if the tables just happened to come out correct anyway.

**Why is it a problem?**
This is essential for the kind of challenge we want to create for the model.

**How to do it instead:**
Make sure the prompt asks for a GUI action that can be assessed by a rubric item, i.e. something that you know would look different if the model failed to inspect.

---

## Hardcoding values in the rubric criteria

**Description:**
The rubric item provides the correct answer instead of referring to the GTF.

**Examples:**
"The document states that the correct value is X, matching the value in the corresponding expected document."

**Why is it a problem?**
The rubric items should always refer to the GTF as the source of truth. Even if the criterion in the example also refers to the GTF, it gives away the correct value as well.

**How to do it instead:**
Make sure the rubric item is phrased in a way that requires comparison to the GTF: "The document states the correct value of X, matching the value of X in the corresponding expected file."
