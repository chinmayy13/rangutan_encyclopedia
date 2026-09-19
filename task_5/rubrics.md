Write criteria that encompass all requirements needed to fulfill this prompt.

Edit raw criteria

Table view
(19/19 completed)

Criterion
Weight
Criteria Type
Category

1
An output file named `benchmark_comparison_annotated.png` exists and is a valid PNG image.
5
MUST-PASS
format_gate

2
An output file named `library_delta_table.md` exists and is a valid Markdown file.
5
MUST-PASS
format_gate

3
An output file named `canvas_agent_evidence_pack.md` exists and is a valid Markdown file.
5
MUST-PASS
format_gate

4
The chart in `benchmark_comparison_annotated.png` compares Run 1 vs Run 2 across all four stacks and all four metrics, with data values semantically equivalent to the corresponding expected file.
20
REGULAR
correctness

5
The chart in `benchmark_comparison_annotated.png` annotates the same stack-metric pairs flagged as divergent in the corresponding expected file, with delta values matching within ±.5 points.
20
REGULAR
correctness

6
`library_delta_table.md` contains a reconciliation table covering the same conflict areas addressed in the corresponding expected file (`roughjs` bounding-box exposure, `dagre` dependency-resolution sufficiency, `elkjs` necessity, `d3-hierarchy` for page/content context).
20
REGULAR
correctness

7
For each conflict area in `library_delta_table.md`, the reconciliation conclusion is semantically equivalent to the corresponding expected file.
35
REGULAR
correctness

8
Each reconciliation conclusion in `library_delta_table.md` is justified by referencing benchmark evidence consistent with the evidence cited in the corresponding expected file.
15
REGULAR
correctness

9
`canvas_agent_evidence_pack.md` embeds the benchmark chart image (`benchmark_comparison_annotated.png`), as shown in the corresponding expected file.
5
REGULAR
correctness

10
`canvas_agent_evidence_pack.md` embeds the delta table's reconciliation content from `library_delta_table.md` directly, rather than only referencing or summarizing it, matching the corresponding expected file.
8
REGULAR
correctness

11
The benchmark evidence section in `canvas_agent_evidence_pack.md` conveys the same key methodology and divergence findings as the corresponding expected file.
10
REGULAR
correctness

12
The reconciled capability-notes summary in `canvas_agent_evidence_pack.md` is consistent with the conclusions reached for each conflict area in `library_delta_table.md`, with no contradictions between the two files.
10
REGULAR
correctness

13
The recommendation in `canvas_agent_evidence_pack.md` reaches the same overall conclusion on stack sufficiency, the primary library addition, any complementary addition, and the final recommended configuration as the corresponding expected file.
40
REGULAR
correctness

14
The recommendation in `canvas_agent_evidence_pack.md` addresses autonomous node placement, page/view navigation, and dependency reasoning, consistent with the corresponding expected file.
10
REGULAR
correctness

15
`canvas_agent_evidence_pack.md` includes a background section framing the agent-canvas problem, consistent with the corresponding expected file.
5
REGULAR
correctness

16
The chart in `benchmark_comparison_annotated.png` uses a grouped bar layout faceted by metric, with distinguishable Run 1 and Run 2 bar colors and a legend identifying the runs, comparable to the corresponding expected file.
30
REGULAR
visual

17
All text in `benchmark_comparison_annotated.png` including axis labels, stack names, metric titles, divergence annotations, and the legend is legible, with no overlapping, truncation, or clipping.
25
REGULAR
visual

18
The chart in `benchmark_comparison_annotated.png` has a descriptive title and appropriate axis labels, comparable to the corresponding expected file.
20
REGULAR
visual

19
The recommendation in `canvas_agent_evidence_pack.md` acknowledges the layout-latency cost of the recommended configuration, consistent with the corresponding expected file.
10
REGULAR
correctness
