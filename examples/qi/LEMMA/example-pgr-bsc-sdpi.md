---
status: cited
date: 2026-08-10
---

# BSC strong data-processing inequality


<!-- toc -->

- [Statement](#statement)
- [Role in Proof](#role-in-proof)
- [Verification](#verification)

<!-- /toc -->

**ID**: `cpt-qi-lem-pgr-bsc-sdpi`
## Statement

For L ∈ {0,1}, J = L ⊕ N with N ~ Bern(δ) independent of (U,L), 0 ≤ δ ≤ 1/2: I(U;J) ≤ (1−2δ)²·I(U;L). PGR use δ = 1/5: I(U;J) ≤ (9/25)·I(U;L).

## Role in Proof

Part-2 of `cpt-qi-pm-pgr-thm1`: bounds what any auxiliary variable learns through the flip channel; with the erasure identity it yields P_Z|XY ⪰_ln P_J|XY since 1/2 > 9/25.

## Verification

- **Route: cited** — PGR Appendix B, Lemma B.3 (self-contained proof via convexity of g(q) = h₂(r(q)) − c²h₂(q); underlying result Ahlswede–Gács 1976).
- **Upgrade path: tier B** — the g″(q) ≥ 0 computation (paper Eqs. B.7–B.8) is a one-variable symbolic check; SymPy script pending.
