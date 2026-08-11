---
description: Invoke when the user asks to search for counterexamples or witnesses in a finite model class — e.g. "search for sources in the less-noisy gap", "hunt counterexamples to X", "find a distribution violating Y". Runs a search program whose outputs are certificate-shaped.
---

# Workflow: hunt-counterexample

## Inputs

- A target property (what a hit looks like), the search space (alphabet sizes, parameterization), and per-candidate checkable conditions.

## Step 0 — Plan gate

Locate an `approved` VERIFICATION-PLAN covering this work. **If none exists, run `workflows/plan-verification.md` FIRST** — brainstorm scope, depth, allowed interventions, budget with the user before any heavy action. NEVER patch third-party code, stub dependencies, choose verification depth, or contact authors unless the plan authorizes it; an unlisted intervention sends you back to plan-verification for an amendment.

## Steps

1. **Specify the search as data.** Write the search spec: candidate space, per-candidate predicate (each condition with its verification tier — e.g., rank-one separation: exact arithmetic; less-noisy dominance: numeric screening + exact certification; simulation infeasibility: LP + Farkas certificate), and scoring for ranking hits.
2. **Screen numerically, certify exactly.** Floating point may *rank* candidates; only exact arithmetic may *assert*. Every reported hit must carry its exact certificate — a hit without a certificate is a lead, not a result.
3. **Package hits as kit artifacts.** Each confirmed hit = CLAIM (the exact candidate data) + CERTIFICATE (its witness) + CHECK-RUN (via verify-certificate workflow).
4. **Record negative space.** Log the searched region and screening thresholds even when empty — "searched X, found nothing" is a result (kept as a run record), and prevents silent re-searching.
5. **Gate.** graph_gate must PASS on the new artifacts.

## Hard rules

- No float ever crosses from screening into an assertion.
- Ranking heuristics (e.g. Δ_guess, TV-infimum scores) are logged with the hits so reruns are comparable.
- If the search program itself embeds a claim (e.g. "condition 2 implies membership"), that claim gets a LEMMA artifact with its own verification route.
