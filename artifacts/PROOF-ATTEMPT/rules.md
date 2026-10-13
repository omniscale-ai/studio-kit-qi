# PROOF-ATTEMPT Rules

**Dependencies**:
- `{principles}` — cross-cutting invariants P1–P13; load before these rules
- `{proof_attempt_template}` — structural reference
- `{attest_lean}` — the script that generates this kind

---

1. **Script-generated skeleton, script-owned verdict.** `attest_lean.py` writes the frontmatter and the sections Conjecture, Route, Development, Build Log, Verdict and Attestation. None of them is edited by hand. The `status` and `generated-by` lines and the five sections before Attestation are sealed: `graph_gate` G7 recomputes the owned-sections hash and a mismatch fails the artifact. Attestation and the `description` and `date` lines are script-written but not sealed — editing them is still a violation of this rule, only not a mechanically detected one. To change anything script-owned, change the development and re-run the script. The agent fills Assumptions, Deviations and Handoff; the script preserves them on re-run.
2. **One attempt is one conjecture, one route, one declaration.** The attested declaration and its closure are what is judged; other theorems in the file are not. A refutation is an attempt run with `--refutes`: its declaration's type must be the negation of the formal statement (`¬ …`, typically proved by exhibiting a witness inside the proof — a declaration of any other shape, such as an existential, fails `statement-matches`), and a passing vector gives status `refuted`.
3. **The status vocabulary is closed.** `pass` — every criterion row passes; `refuted` — every row passes for a refutation; `incomplete` — the attestation completed and at least one row fails (a build error, a `sorry`, an extra axiom, a different statement); `error` — the attestation started but could not complete (toolchain missing, declaration not found after a green build). A usage error (missing file, CONJECTURE without a compiled Formal Statement) exits 2 and writes no artifact. `incomplete` and `error` records are kept, not deleted; "retry until green" never erases history.
4. **The verdict has exactly the plan's rows.** A concern that surfaces during the attempt goes into Deviations or into the next plan, never into a new row and never into an edited one.
5. **Every fact relied on has a licence.** A Mathlib lemma: `#check` resolved in the pinned toolchain on a date. A project lemma: the attempt that proved it, or this file. An external result: exact statement and resolvable location, and the CONJECTURE under which it is being formalized — never an `axiom`. The Assumptions table documents; `sorry-free` and `axioms-standard` enforce.
6. **A green build of a different statement is `incomplete`.** `statement-matches` compares the declaration's type with the CONJECTURE's compiled Formal Statement up to whitespace; a mismatch means a different theorem was proved, however good it looks.
7. **The judged row is copied, not filled.** `statement-confirmed` reads the CONJECTURE's Faithfulness Cross-Check — independent reading with no open discrepancy, instance agreement, dated `Confirmed faithful by` — and the script only checks that the record is complete; an attempt never confirms its own statement, and the author of the Lean block never performs the reading alone (P13).
8. **The handoff is about this attempt only.** Remaining goals quoted as statements, unused hypotheses, what would refute, which budget limit this attempt counts toward. Which conjecture to pursue next is decided in the RESEARCH-PLAN's register at the phase gate, not here.
9. **Reproduction is Development plus Build Log.** Project commit, file hash, toolchain, pinned packages and the exact command are enough for a third party to re-run the script and obtain the same vector.
10. **Time is a deviation, not a footnote.** An attempt whose actual time exceeds the confirmed Formalization Cost by the plan's factor records it in Deviations and is raised with the human before the next attempt.

## Where the principles land in a PROOF-ATTEMPT

| Section | Principles |
|---------|------------|
| Conjecture | P2 the expected statement is the cross-checked formal statement; P13 |
| Route | P1 the tier names the evidence kind; P11 tools are informational |
| Development | P11 provenance; P9 the pinned toolchain the licences refer to |
| Assumptions | P9 a licence per fact relied on |
| Deviations | P3 time beyond the confirmed cost; P4 attempt without instance evidence; P7 doubts about a row; P12 feedback verbatim |
| Verdict | P7 exactly the plan's rows; P8 vector, mechanical rows from the compiler, judged row copied; P13 `statement-confirmed` |
| Handoff | P5 the source of gap origins; P6 unused hypotheses |
| Attestation | P8 owned-sections hash seals the script's output |
