# LEMMA — Generation & Validation Rules

**Dependencies**:
- `{principles}` — cross-cutting invariants P1–P13; load before these rules
- `{lemma_template}` — structural reference

---

1. **Status follows artifacts.** The frontmatter status equals the strongest verification artifact present in the Verification section — never stronger. `machine-checked` requires a passing CHECK-RUN or equivalent script output; `formalized` requires a building Lean/Coq/Isabelle development containing the statement.
2. **Self-contained statements.** A reader should not need the proof-map context to know what is being asserted.
3. **Tier A preferred where possible.** If a lemma about exact rational data is checkable by computation, `cited`/`expert` are not acceptable resting states — mark `open` with route "tier A pending" instead of laundering trust through a citation.
4. **Negative results kept.** If verification refutes a lemma, the artifact records it (status stays `open`, refutation linked) — the proof map inherits the problem visibly.

## Where the principles land in a LEMMA

| Section | Principles |
|---------|------------|
| Statement | P6 self-contained, at the strength the proof needs |
| Role in Proof | P8 the edges whose trust this node carries |
| Verification | P1 the tier names the evidence kind; P8 status never exceeds the artifact present (`graph_gate` G2); P9 `cited` quotes the exact statement at a resolved location; P10 refutations kept and linked; P12 `expert-verified` names the reviewer and scope |
