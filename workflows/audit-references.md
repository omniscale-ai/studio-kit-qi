---
description: Invoke when the user asks to audit citations/references of a claim graph or paper — e.g. "audit the references", "check the citations in this proof map". Verifies every `cited` node and Source section resolves to a real document.
---

# Workflow: audit-references

## Inputs

- A set of kit artifacts (THEOREM/PROOF-MAP/LEMMA) or a paper's bibliography.

## Steps

1. **Collect every external reference**: THEOREM Source sections, every `cited` LEMMA's Verification section, CERTIFICATE provenance links.
2. **Resolve each to exactly one real document** (arXiv ID, DOI, published venue). Vocabulary of outcomes: `resolved` (exactly one document, statement present), `none` (no such document — hallucination), `ambiguous` (multiple candidates), `unresolved` (lookup failed — outage is never "not found").
3. **For `cited` lemma nodes, go one level deeper:** confirm the *exact quoted statement* appears in the resolved document (page/section), not merely that the document exists. A resolving citation with a missing statement downgrades the node to `open` with a note.
4. **Record the audit** as a dated run record (which IDs checked, outcomes, tool versions); update artifact statuses only downward or laterally — an audit can revoke `cited`, never mint `machine-checked`.
5. **Gate.** graph_gate must PASS after status updates.

## Hard rules

- Outage ≠ absence: `unresolved` is a distinct outcome and must be retried, never silently dropped.
- Statement-level verification (step 3) is what makes this stronger than bibliography linting; do not skip it for load-bearing nodes.
