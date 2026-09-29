Improve the task per the following feedback:

Quality: Overall Task

2

Quality: Instruction Following

no

Overall Task Feedback

Dear contributor, unfortunately, there are several issues that need to be fixed.

First, the task can be solved by three models, which score almost perfectly against the rubric.

Additionally, the prompt requires source_coin_token.png and scene_reference.png, but neither file is present in input_files.

The rubric weight distribution is also inverted compared to the required model (format_gate <20% / correctness >50% / visual 20–30%). The current distribution is approximately 7% / 30% / 63%, largely due to redundant visual criteria. Criteria 5, 6, 16, and 20 all re-test the 3D bomb, while criteria 7, 17, 18, 19, and 21 all re-test scene readability.

Criterion 1 (and likely criterion 2) should be MUST-PASS rather than REGULAR. Criterion 8 is also miscategorized as Visual instead of Correctness.

The prompt has a robotic file references, with three consecutive "Use X as Y" sentences. Several visual criteria also over-anchor to the specific layout choices in the GTF, even though the prompt allows multiple valid presentations.

Finally, the initializer was left with the placeholder, it was not modified to the currect input files as it is requested

Please address these issues and review the stumping guidelines for ideas on how to make the task more challenging while keeping the rubric aligned with the requirements.
