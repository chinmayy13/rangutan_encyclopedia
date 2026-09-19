# Draft Recommendation: Agent Canvas Library Stack

## Background
Agents that operate on a node-based canvas (react-flow) need to autonomously answer three questions without a human in the loop: where should a new node go, which page/view should be opened, and what does a given node depend on. That means the agent needs reliable, structured access to node bounding boxes, z-order, page membership, and dependency edges — not just a pretty rendered canvas. The open question for this evidence pack is whether the current base stack (`react-flow + roughjs + dagre`) already exposes enough of that structure, or whether we need to add `elkjs` and/or `d3-hierarchy` on top.

## Reconciled benchmark findings
TODO: insert reconciled benchmark findings here (pull from `library_delta_table.md` / the annotated chart — where do the two runs agree, where do they diverge by more than 15 points, and what does that imply about the reliability of each stack).

## Conclusion
TODO: is the base stack (`react-flow + roughjs + dagre`) sufficient on its own, or are `elkjs` and `d3-hierarchy` necessary additions? No verdict written yet — pending the reconciled evidence above.
