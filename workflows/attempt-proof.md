---
description: Invoke when the user asks to prove or refute a registered conjecture — e.g. "prove conjecture X in Lean", "try to formalize this", "attempt the n=3 case", "show the conjecture is false". One PROOF-ATTEMPT per route, attested by attest_lean.py; requires an approved RESEARCH-PLAN and a CONJECTURE with a confirmed formal statement.
---

# Workflow: attempt-proof

## Inputs

- A CONJECTURE ID; the route (tier A exact / tier B symbolic / tier C Lean); the plan's Lean project.

## Step 0 — Plan gate and conjecture gate

Locate an `approved` RESEARCH-PLAN covering this conjecture; **if none exists, run `workflows/plan-research.md` FIRST.** Then check the CONJECTURE: Formal Statement compiled and the Faithfulness Cross-Check complete — independent reading with every element row `yes` and no open discrepancy, instance agreement `agree` or `n/a`, dated `Confirmed faithful by` (else back to `propose-conjecture` step 5; `attest_lean.py` would fail `statement-confirmed` anyway); Evidence non-empty (else the attempt records a deviation with a reason); attempts on this route below the plan's limit (else stop and report — a conjecture at its limit is not retried under this plan).

## Steps

1. **Count the budget.** Prior attempts on this conjecture and route, against the plan's limit; this attempt's number goes into the Handoff.
2. **Set up the development.** The plan's project at the pinned `lean-toolchain`; `lake build` green before touching anything; for Mathlib projects `lake exe cache get` first. If the cold build exceeds the confirmed Formalization Cost by the plan's factor, stop and raise it with the human.
3. **Prove one step at a time.** Hardest goal first. `#check` every Mathlib lemma before relying on it (P9). **NEVER add an `axiom`** for a result you cannot prove — it becomes a `cited` LEMMA and a CONJECTURE to formalize. Keep `sorry` on open goals so the file builds and the Handoff can quote them. For a refutation, prove the negation of the formal statement (`¬ …` — exhibit the witness inside that proof; the declaration's type must be the negation itself for `statement-matches` to pass).
4. **Attest.** `python3 {scripts}/attest_lean.py --project <dir> --file <rel.lean> --decl <Full.Name> --conjecture <CONJECTURE.md> --slug <slug> --out <PROOF-ATTEMPT.md>` (add `--refutes` for a refutation; `--route-note` for how the proof was found). The script writes the frontmatter status, Conjecture, Route, Development, Build Log, Verdict and Attestation. **NEVER write or edit those** — re-run the script after any change to the development; it preserves the agent-filled sections.
5. **Fill Assumptions, Deviations, Handoff.** Every fact relied on with its licence; deviations or `None` explicitly; remaining goals quoted as statements, hypotheses the proof did not use, what would refute, the budget limit this attempt counts toward.
6. **Update the CONJECTURE.** Add the attempt to Attempts (most recent first, with status). If the status is `pass` or `refuted`, name the attempt in Proved by or Refuted by and set the frontmatter status to the value that line now entitles (G6 verifies it); then update the register row in the RESEARCH-PLAN. Any other status leaves the conjecture's status unchanged.
7. **Gate.** `python3 {scripts}/graph_gate.py <artifacts-root>` must PASS (G6, G7, G8) before committing.

## Hard rules

- `incomplete` and `error` records are kept; a new attempt is a new artifact, never an overwrite of a failed one.
- A green build whose `statement-matches` row fails is `incomplete`: you proved something else. Fix the development, not the conjecture — or, if the conjecture was mis-formalized, go back to `propose-conjecture` with a human re-confirmation.
- A `refuted` status is a significant event: alert the user; the conjecture stays refuted; the Handoff proposes restrictions as new conjectures, never a retry.
- Time beyond the confirmed cost × the plan's factor: stop and raise with the human before the next attempt.
