# LEMMA — Generation & Validation Rules

1. **Status follows artifacts.** The frontmatter status equals the strongest verification artifact present in the Verification section — never stronger. `machine-checked` requires a passing CHECK-RUN or equivalent script output; `formalized` requires a building Lean/Coq/Isabelle development containing the statement.
2. **Self-contained statements.** A reader should not need the proof-map context to know what is being asserted.
3. **Tier A preferred where possible.** If a lemma about exact rational data is checkable by computation, `cited`/`expert` are not acceptable resting states — mark `open` with route "tier A pending" instead of laundering trust through a citation.
4. **Negative results kept.** If verification refutes a lemma, the artifact records it (status stays `open`, refutation linked) — the proof map inherits the problem visibly.
