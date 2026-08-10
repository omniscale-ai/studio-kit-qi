---
status: cited
date: 2026-08-10
---

# Erasure identity: I(U;Z) = (1−ε)·I(U;L) for Z = BEC_ε(L)

**ID**: `cpt-qi-lem-pgr-erasure-identity`

## Statement

`cpt-qi-lem-pgr-erasure-identity`: If Z is the output of a binary erasure channel with erasure probability ε applied to L, with the erasure event independent of (U, L), then I(U;Z) = (1−ε)·I(U;L). PGR use ε = 1/2: I(U;Z) = ½·I(U;L).

## Role in Proof

Part-2 of `cpt-qi-pm-pgr-thm1`: gives the exact information content of Eve's variable, paired against the BSC bound (`cpt-qi-lem-pgr-bsc-sdpi`) to establish less-noisy dominance (½ > 9/25).

## Verification

- **Route: cited** — PGR Appendix B, Lemma B.2, with a self-contained three-line proof (chain rule over the visible erasure flag).
- **Upgrade path: tier B** — elementary symbolic identity; SymPy check pending.
