# Canvas Agent Evidence Pack: Do We Need elkjs and d3-hierarchy?

## Background
Agents that operate on a node-based canvas (react-flow) need to autonomously answer three questions
without a human in the loop: where should a new node go, which page/view should be opened, and what
does a given node depend on. That means the agent needs reliable, structured access to node bounding
boxes, z-order, page membership, and dependency edges — not just a pretty rendered canvas. This pack
resolves the open question of whether the base stack (`react-flow + roughjs + dagre`) already exposes
enough of that structure, or whether `elkjs` and/or `d3-hierarchy` are necessary additions.

## Benchmark evidence

![Benchmark comparison, run 1 vs run 2, annotated where divergence exceeds 15 points](benchmark_comparison_annotated.png)

Two independent benchmark runs were compared across four stacks and four metrics, with each stack's
score averaged across 6 individual trials per run (24 trial-level rows per run file) rather than a
single reading — so the pattern below reflects repeated-trial behavior, not one-off noise. Two bars
diverge by more than 15 points between the run averages: `S1` (base stack) on spatial accuracy (Δ17),
and `S3` (`+d3-hierarchy`, no `elkjs`) on page-navigation success (Δ22). Every stack that includes
`elkjs` (`S2`, `S4`) stays comfortably under that 15-point threshold on every metric, typically within
single digits.

Latency moves in the opposite direction from the accuracy metrics. Average layout latency rises
consistently with each addition — ~420 ms for `S1`, ~455 ms for `S3`, ~610 ms for `S2`, and ~690 ms
for `S4` — with run-to-run agreement inside 8 ms everywhere. Adding `elkjs` accounts for most of it:
roughly 190 ms on the base stack (`S1` → `S2`) and ~235 ms alongside `d3-hierarchy` (`S3` → `S4`).
The full stack is the slowest tested configuration by roughly 65% over the base stack, and unlike the
accuracy metrics this ordering is stable across both runs.

## Reconciled capability-notes findings

The two assessor sources disagreed on two points: whether `roughjs` exposes bounding-box metadata
natively, and whether `elkjs` is necessary. The full reconciliation is in `library_delta_table.md`;
the short version:

- **`roughjs` bounding boxes:** Source A said this works natively; Source B said it needs a custom
  serializer. The base stack's 17-point spatial-accuracy swing between otherwise-identical runs
  matches Source B's account — a library that natively and reliably exposed bounding boxes shouldn't
  produce that much run-to-run noise.
- **`dagre` for dependency resolution:** Source A said `dagre` alone is sufficient. This one holds up:
  `dep_resolution_hit_rate_pct` is the most stable metric in the whole dataset (1–2 point deltas
  everywhere), including in the stack with no `elkjs`. Source A is correct on this specific point.
- **`elkjs` necessity:** Source A recommended against it; Source B said it's required for multi-page
  graphs. The evidence favors Source B — the two stacks with `elkjs` are the most stable across every
  metric, and the worst divergence in the whole dataset (S3, page-nav, Δ22) happens specifically in a
  stack that has `d3-hierarchy` but not `elkjs`.
- **`d3-hierarchy` for page context:** Source B recommended it for page/content positioning. It does
  help, but only alongside `elkjs` — the best and most stable stack overall is `S4`
  (`elkjs + d3-hierarchy` together); `d3-hierarchy` alone (`S3`) does not fix page-navigation
  reliability on its own.

## Recommendation

**`react-flow + roughjs + dagre` alone is not enough.** It gets dependency resolution right, but its
spatial-accuracy numbers are too unstable to trust for autonomous node placement — an agent using this
stack could not reliably determine where to insert a new node.

**Add `elkjs`.** It is the single change most correlated with run-to-run stability across every metric,
including the two metrics agents most need for autonomous operation: spatial accuracy (positioning) and
page-navigation success (knowing which page to open). It is also the largest latency addition in the
set — roughly 190 ms on the base stack — which is the trade worth taking here, since an unstable
position signal fails the task at any speed.

**Also add `d3-hierarchy`, as a complement to `elkjs` rather than a substitute for it.** It provides the
page/parent-container context an agent needs to reason about "which page does this belong to," but the
data shows it only delivers that benefit once `elkjs` is already handling layout — on its own it does
not stabilize page navigation.

**Bottom line:** the full stack, `react-flow + roughjs + dagre + elkjs + d3-hierarchy` (`S4` in the
benchmark), is the only configuration tested that gives an agent reliably stable answers on node
position, page context, and dependencies at once.
