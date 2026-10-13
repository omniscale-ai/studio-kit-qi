---
description: Invoke when the user asks to search for counterexamples or witnesses in a finite class of objects — e.g. "hunt counterexamples to X", "search for an object violating Y", "find a distribution in the less-noisy gap". Runs a search program whose outputs are certificate-shaped.
---

# Workflow: hunt-counterexample

## Inputs

- A target property (what a hit looks like), the search space (alphabet sizes, parameterization), and per-candidate checkable conditions.

## Step 0 — Plan gate

Locate an `approved` VERIFICATION-PLAN (verifying a published result) or RESEARCH-PLAN (searching under a research question) covering this work. **If none exists, run `workflows/plan-verification.md` or `workflows/plan-research.md` FIRST** — brainstorm scope, depth, allowed interventions, budget with the user before any heavy action. Under a VERIFICATION-PLAN: NEVER patch third-party code, stub dependencies, choose verification depth, or contact authors unless the plan authorizes it. Under a RESEARCH-PLAN: the Conjecture Policy, Budget and Formalization Cost govern the search space, the exact-check routes and the compute spent. An intervention or cost the governing plan does not cover sends you back to the workflow that owns that plan (`plan-verification` or `plan-research`) for an amendment.

## Steps

1. **Specify the search as data.** Write the search spec: candidate space, per-candidate predicate (each condition with its verification tier — e.g. an algebraic condition: exact arithmetic; a dominance or optimality condition: numeric screening + exact certification; infeasibility of a model: LP + Farkas certificate, or SAT + DRAT proof), and scoring for ranking hits.
2. **Screen numerically, certify exactly.** Floating point may *rank* candidates; only exact arithmetic may *assert*. Every reported hit must carry its exact certificate — a hit without a certificate is a lead, not a result.
3. **Package hits as kit artifacts.** Each confirmed hit = CLAIM (the exact candidate data) + CERTIFICATE (its witness) + CHECK-RUN (via verify-certificate workflow).
4. **Record negative space.** Log the searched region and screening thresholds even when empty — "searched X, found nothing" is a result (kept as a run record), and prevents silent re-searching.
5. **Feed the conjecture.** If the search targets a registered CONJECTURE: a confirmed hit refutes it — name the hit's CLAIM in the conjecture's Refuted by line, set its status to `refuted` once that CLAIM is `certified` (G6 verifies), update the register row; an empty search extends its Evidence table (region, `exact`, this run record) and may move it to `supported`.
6. **Gate.** graph_gate must PASS on the new artifacts.

## Hard rules

- No float ever crosses from screening into an assertion.
- Ranking heuristics (distance scores, objective gaps, …) are logged with the hits so reruns are comparable.
- If the search program itself embeds a claim (e.g. "condition 2 implies membership"), that claim gets a LEMMA artifact with its own verification route.
