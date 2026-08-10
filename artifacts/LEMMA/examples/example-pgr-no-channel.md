---
status: open
date: 2026-08-10
---

# No stochastic channel Z→J reproduces the J-slices (PGR, part 4 core)

**ID**: `cpt-qi-lem-pgr-no-channel`

## Statement

`cpt-qi-lem-pgr-no-channel`: There is no stochastic channel Z→J (a 3×2 row-stochastic matrix, Z ∈ {0,1,⊥}, J ∈ {0,1}) such that processing the Z-output of the PGR source yields the exact joint slices A = (1/18)[[4,2],[2,1]], B = (1/18)[[1,2],[2,4]] of the J-channel. Concretely (paper Eq. 12): writing r_z = P(J=1|Z=z), the constraints force (r₀+r⊥)/2 = 1/5 and (r₁+r⊥)/2 = 4/5, hence r₁ − r₀ = 6/5 > 1 — impossible for probabilities.

## Role in Proof

Feeds part-4 of `cpt-qi-pm-pgr-thm1`: together with rank-one rigidity (`cpt-qi-lem-pgr-det-identity`), any channel decoupling X from Y would have to simulate J exactly; this lemma shows no such channel exists, so (with `cpt-qi-lem-pgr-compactness`) the intrinsic information stays strictly positive. Without it the positive-cost half collapses.

## Verification

- **Route: tier A** — a finite LP infeasibility over 6 variables with rational data; a Farkas certificate is 3 rational numbers. Candidate CLAIM+CERTIFICATE pair for this kit (the minimal end-to-end example of the certificate layer — planned).
- The elementary contradiction (r₁ − r₀ = 6/5) is also directly checkable by exact arithmetic; kit script pending.
- Present status **open**: no artifact yet. The paper's own verification code (ancillary material of arXiv:2607.25838) covers the finite computations and can seed the CHECK-RUN once wrapped.
