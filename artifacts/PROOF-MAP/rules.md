# PROOF-MAP — Generation & Validation Rules

**Dependencies**:
- `{principles}` — cross-cutting invariants P1–P13; load before these rules
- `{proof_map_template}` — structural reference

---

1. **Faithful to the source proof.** The DAG decomposes the *published* proof, not an imagined better one. Alternative decompositions are separate maps.
2. **Nodes are checkable units.** Split until each node has a single natural verification route (tier A exact / tier B symbolic / tier C Lean / cited / expert). A node needing two routes is two nodes.
3. **Statuses on nodes, from the closed vocabulary:** `formalized > machine-checked > expert-verified > cited > open`. A status may only be set by reference to the artifact that establishes it (CHECK-RUN, Lean build, named review, resolved citation).
4. **Load-bearing is explicit.** Redundant/alternative branches marked as such; everything else is load-bearing and must appear in the Load-Bearing Nodes section.
5. **Cited nodes cite theorems, not papers.** "GGK Prop. 1" with a resolvable reference and the exact statement used — not "see [28]".

## Where the principles land in a PROOF-MAP

| Section | Principles |
|---------|------------|
| Dependency Graph | P9 cited nodes quote theorems with exact statements; P8 statuses only by reference to the establishing artifact; P1 each node's tier names its evidence kind |
| Load-Bearing Nodes | P8 the set that drives the theorem's computed trust; P10 a refuted node stays visible |
