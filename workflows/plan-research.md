---
description: Invoke FIRST whenever the user wants to find, state or prove something NEW — a bound, a conjecture, a generalization, a Lean formalization of an unpublished result — and no approved RESEARCH-PLAN covers it, e.g. "find the classical bound of this Bell expression", "conjecture and prove the n=3 case", "formalize this in Lean". Interactive brainstorm producing a RESEARCH-PLAN; propose-conjecture and attempt-proof require it. Verifying a PUBLISHED result is plan-verification instead.
---

# Workflow: plan-research

## Purpose

Discovery work has order-of-magnitude cost differences (exact enumeration of a finite scenario: seconds; a symbolic identity: hours; a Lean proof against Mathlib: days to months) and decisions that are the **user's**: what counts as proved, which axioms are acceptable, how many attempts a conjecture gets, which definitions the formalization commits to. This workflow elicits them BEFORE any exploration or proving and records them in a RESEARCH-PLAN that `propose-conjecture`, `attempt-proof` and `hunt-counterexample` reference.

## Steps

1. **Light recon only.** Read what the user gives (question, notes, a paper the question extends). Resolve with `#check` in the pinned toolchain which Mathlib declarations the question's concepts map to, and note which do not exist. **NEVER enumerate, prove, build Mathlib from cold, or write Lean definitions at this stage** — recon informs the questions, it does not start the work.
2. **Brainstorm with the user — one group at a time, offering options with trade-offs.** Required groups:
   - **Question and object class.** Which scenario, alphabets, model class, resource? What is a deliverable: a proved CONJECTURE with a passing PROOF-ATTEMPT, a refuted one with a certified counterexample, a THEOREM once there is a write-up? What is withheld from the agent?
   - **Prior knowledge and concordance.** Which results are known and where exactly; which Mathlib definitions the run builds on; which it must define; encodings and conventions (outcome encoding, normalisation, party labels). Every concept gets a concordance row with a `#check`-verified declaration or a named project file.
   - **Routes and cost.** Per conjecture type: tier A exact via CLAIM/CERTIFICATE, tier B symbolic, tier C Lean. Ask the human for the cold and cached build time on the available machine and the effort per route in this concrete case; record name and date.
   - **Budget.** Attempts per conjecture per route, total attempts, time box, exploration compute, conjectures open at once.
   - **Success criteria.** The six rows `attest_lean.py` measures (builds, sorry-free, axioms-standard, statement-matches, dependencies-pinned, statement-confirmed), the allowed axiom set (default `propext`, `Classical.choice`, `Quot.sound`), and any route-specific row. Each with a justification; confirmed by name and date; frozen before the first attempt.
   - **Cross-check roles (P13).** Who performs the independent reading of every formal statement — a named human, or a second agent instance started fresh and shown only the Lean block, its definitions and the concordance — and who confirms faithfulness. The author of a Lean block never reads it alone.
   - **Deliverables.** Artifacts only / report / Lean repository / Mathlib PR / preprint. For a Mathlib PR the `mathlib-pr` and `mathlib-review` skills from leanprover/skills carry the upstream conventions (PR title format, labels, style); note in the plan that they apply.
3. **Write the RESEARCH-PLAN** from `artifacts/RESEARCH-PLAN/template.md`, including the Decisions Log (question → options offered → user's choice) and an empty Conjecture Register.
4. **Get explicit approval** — the user confirms the plan, the cost table and the criteria table; record the date in the Approval section. Only then dispatch to `propose-conjecture`, `attempt-proof` or `hunt-counterexample`.

## Hard rules

- **NEVER start discovery work without an approved plan.** If the user waives planning ("just try to prove it"), still write a minimal plan recording the waiver and the defaults chosen — the waiver is itself a decision worth an artifact.
- Questions come in small groups with concrete options and costs, not as a wall of 20 questions.
- A concept without a concordance row blocks approval; "we will define it later" is not a row.
- Scope changes discovered mid-work (a definition needs Mathlib that does not exist; a conjecture needs an axiom outside the set; the build is ten times slower than confirmed) return to this workflow: amend the plan, re-approve the affected decision — do not improvise.
