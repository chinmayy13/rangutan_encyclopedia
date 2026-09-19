# Capability Notes — Source A

**Reviewer:** Assessor A 
**Scope:** Can an agent reading only the canvas library's exposed data determine node bounding boxes, z-order, page membership, and dependency edges?

## roughjs

`roughjs` exposes the rendered shape's bounding box directly through its generated SVG/canvas element attributes (`width`, `height`, `x`, `y` on the returned drawable). No extra tooling is needed — the agent can read this straight out of the DOM/canvas node after render. This means node position and size are natively available to any agent inspecting the canvas.

## dagre

`dagre` alone is sufficient for dependency traversal. It computes a directed graph layout and stores parent/child and edge relationships in its internal graph object, which is queryable via `graph.predecessors()` / `graph.successors()`. For the stack sizes we tested, this fully covers "what depends on what."

## elkjs

Recommend **against** adding `elkjs`. It roughly doubles bundle size and adds a WASM layout step that is not required once `dagre` is already resolving edges. The added complexity isn't justified for our use case.

## Summary verdict

`react-flow + roughjs + dagre` is enough. No need for `elkjs`.

