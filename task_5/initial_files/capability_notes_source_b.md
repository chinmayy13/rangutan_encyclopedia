# Capability Notes — Source B

**Reviewer:** Assessor B 
**Scope:** Can an agent reading only the canvas library's exposed data determine node bounding boxes, z-order, page membership, and dependency edges?

## roughjs

`roughjs` is a rendering/sketch-style drawing library, not a layout library. It draws shapes but does **not** expose bounding-box metadata to the surrounding application context on its own — the geometry it computes internally is discarded after the draw call. To get bounding boxes into agent-readable context, you need a **custom serializer** that captures the shape's computed path data at draw time and writes it back out as structured metadata. Without that extra layer, an agent has no reliable way to read node bounds.

## dagre

`dagre` is fine for small graphs, but its layout quality and its edge-resolution APIs degrade past roughly 40 nodes across multiple pages. For multi-page dependency graphs above that size, **`elkjs` is required** — it supports constrained, incremental layout across sub-graphs (pages) in a way `dagre` doesn't.

## d3-hierarchy

Recommend adding `d3-hierarchy` specifically for **content-position context** — i.e., letting the agent understand "which page/parent container does this node belong to" via `d3.hierarchy()` tree structures, which `dagre` and `elkjs` don't model well on their own.

## Summary verdict

`react-flow + roughjs + dagre` is **not** enough on its own. Needs a custom roughjs serializer at minimum, plus `elkjs` for graphs over \~40 nodes across pages, plus `d3-hierarchy` for page/content positioning.

*Directly conflicts with Source A on the roughjs bounding-box claim and the elkjs necessity claim.*

