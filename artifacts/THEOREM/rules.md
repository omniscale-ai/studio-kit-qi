# THEOREM — Generation & Validation Rules

**Dependencies**:
- `{principles}` — cross-cutting invariants P1–P13; load before these rules
- `{theorem_template}` — structural reference

---

1. **A theorem tracks a source.** THEOREM artifacts verify *published* (or preprint) results; the statement must match the source up to notation, and any deviation must be flagged. New statements are CONJECTUREs (or CLAIMs when they are single finite exact statements), not THEOREMs; a proved conjecture becomes a THEOREM once it has a citable source.
2. **Status is computed, not asserted.** `verified` ⟺ every load-bearing node of the proof map has status ≥ machine-checked. `in-verification` ⟺ a proof map exists. Enforced by `scripts/graph_gate.py`.
3. **Trust Summary names the weakest link.** Not a list — the single weakest load-bearing node and its status. If the weakest link is `expert-verified`, name the expert.
4. **One proof map per theorem** (alternative proofs = alternative PROOF-MAP artifacts, the theorem references all; trust is the max over maps).

## Where the principles land in a THEOREM

| Section | Principles |
|---------|------------|
| Statement, Source | P9 the statement matches a resolved source; deviations flagged |
| Proof Map | P8 status computed from load-bearing nodes (`graph_gate` G1) |
| Trust Summary | P8 the single weakest link named; P12 an expert-verified link names the expert |
