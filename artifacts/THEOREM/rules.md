# THEOREM — Generation & Validation Rules

1. **A theorem tracks a source.** THEOREM artifacts verify *published* (or preprint) results; the statement must match the source up to notation, and any deviation must be flagged. New conjectures are CLAIMs, not THEOREMs.
2. **Status is computed, not asserted.** `verified` ⟺ every load-bearing node of the proof map has status ≥ machine-checked. `in-verification` ⟺ a proof map exists. Enforced by `scripts/graph_gate.py`.
3. **Trust Summary names the weakest link.** Not a list — the single weakest load-bearing node and its status. If the weakest link is `expert-verified`, name the expert.
4. **One proof map per theorem** (alternative proofs = alternative PROOF-MAP artifacts, the theorem references all; trust is the max over maps).
