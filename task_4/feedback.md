Improve the task per the following feedback:

Round 1 feedback (resolved)

Quality: Overall Task

4

Quality: Instruction Following

yes

Overall Task Feedback

Overall, excellent work. The prompt, verifier and GTF are all correct. I only found a few issues with the rubric.
C12 is vague/unbound: "present and consistent" does not specify a comparison mode or tolerance.
C14/C15/C29 and C30 are not GT-anchored: Make sure every correctness criterion should be anchored to the expected file. Also, "clearly communicates", or "technically supported" relies on the grader judgement.
C21 is unbound: "the other principal shortcut result values" is not explicitly enumerated or tied to a specific slide, table or callout. This means the values could potentially appear anywhere in the deck.
One more thing- Do not explicitly instructs the agent not to use seeded input files. You can just remove them from the initializer.

All four rubric items and the initializer note were fixed and verified, plus the follow-up copilot passes on overfitting, coverage, and atomicity. The rubric reached a Verifier score of 1.00 across all 30 criteria.

Round 3 feedback (current, needs action)

Quality: Overall Task

3

Quality: Instruction Following

yes

Overall Task Feedback

The overall task is good and there are only minor fixes needed in the rubric like C15 is not GTF anchored and some weightage inaccuracies. Every correctness criterion should be anchored to the GTF and visual criteria should be weighted properly - their weights should not be greater than the main core correctness criteria.

The main reason for sending this task back is the difficulty and complexity. The task is quite simple and easy for the model. The agent scores 81.66% across the three runs. Please increase the overall complexity and difficulty of the prompt and revise the GTF and rubric accordingly.
