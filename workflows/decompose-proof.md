---
description: Invoke when the user asks to build a claim graph for a theorem/paper — e.g. "decompose this proof", "make a proof map for arXiv:XXXX", "claim-graph this theorem". Produces THEOREM + PROOF-MAP + LEMMA artifacts with honest statuses.
---

# Workflow: decompose-proof

## Inputs

- A paper (PDF/arXiv ID) and the target theorem within it.

## Steps

1. **Create the THEOREM artifact** from `artifacts/THEOREM/template.md`. Statement must match the source exactly; run reference-audit on the Source section.
2. **Extract the proof's own structure first.** Many papers state their decomposition (proof-map paragraphs, appendix structure). Follow the authors' decomposition; do not invent a better proof (PROOF-MAP rules.md rule 1).
3. **Split into lemma nodes** until each has a single verification route (tier A exact / tier B symbolic / tier C Lean / cited / expert). Create a LEMMA artifact per node.
4. **Assign statuses honestly.** Everything starts `open` or `cited`. **NEVER assign `machine-checked` or `formalized` at decomposition time — those statuses are earned by artifacts, not by reading.** For `cited` nodes: quote the exact external statement and verify the reference resolves.
5. **Build the PROOF-MAP**: dependency table/DAG, then the Load-Bearing Nodes section (test: delete a node — does the theorem survive?).
6. **Write the Trust Summary** in the THEOREM: the single weakest load-bearing link, named.
7. **Gate.** `python3 {scripts}/graph_gate.py <artifacts-root>` must PASS (it will catch unresolved node IDs and status inflation).
8. **Propose the upgrade plan**: for each `open` node, the cheapest route to `machine-checked` (usually tier A for finite arithmetic), presented to the user as next steps.

## Hard rules

- The claim graph documents the *published* proof; gaps found during decomposition are recorded as `open` nodes with a note, not silently patched.
- Every node ID follows `cpt-{system}-lem-{slug}`; every citation resolves or the node cannot be `cited`.
