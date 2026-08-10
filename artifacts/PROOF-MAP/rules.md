# PROOF-MAP — Generation & Validation Rules

1. **Faithful to the source proof.** The DAG decomposes the *published* proof, not an imagined better one. Alternative decompositions are separate maps.
2. **Nodes are checkable units.** Split until each node has a single natural verification route (tier A exact / tier B symbolic / tier C Lean / cited / expert). A node needing two routes is two nodes.
3. **Statuses on nodes, from the closed vocabulary:** `formalized > machine-checked > expert-verified > cited > open`. A status may only be set by reference to the artifact that establishes it (CHECK-RUN, Lean build, named review, resolved citation).
4. **Load-bearing is explicit.** Redundant/alternative branches marked as such; everything else is load-bearing and must appear in the Load-Bearing Nodes section.
5. **Cited nodes cite theorems, not papers.** "GGK Prop. 1" with a resolvable reference and the exact statement used — not "see [28]".
