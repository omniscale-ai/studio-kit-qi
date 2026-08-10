---
status: in-verification
date: 2026-08-10
---

# Bipartite bound information exists (Pauwels–Gisin–Renner, Theorem 1)

**ID**: `cpt-qi-thm-pgr-bound-info`

## Statement

`cpt-qi-thm-pgr-bound-info`: The source of PGR Table I — the distribution over (X,Y,Z) ∈ {0,1}²×{0,1,⊥} with slices M₀ = (1/36)[[5,2],[2,0]], M₁ = (1/36)[[0,2],[2,5]], M⊥ = (1/36)[[5,4],[4,5]] — has bipartite bound information:

S(X;Y‖Z) = 0 < I(X;Y↓Z) ≤ I_form(X;Y|Z),

i.e., the secret-key rate against arbitrary interactive public discussion vanishes, while the intrinsic information (and hence the formation cost) is strictly positive.

## Source

J. Pauwels, N. Gisin, R. Renner, *Bipartite Bound Information Exists*, [arXiv:2607.25838](https://arxiv.org/abs/2607.25838) (v1, Jul 2026). Proof map tracks v1, main text + Appendices A–F.

## Proof Map

`cpt-qi-pm-pgr-thm1` (artifacts/PROOF-MAP/examples/example-pgr.md)

## Trust Summary

Weakest load-bearing link today: the GGK less-noisy monotonicity (`cpt-qi-lem-pgr-ggk`, status **cited** — external theorem, unmechanized in any proof assistant; its formalization is the identified publishable gap) and the compactness argument (`cpt-qi-lem-pgr-compactness`, status **cited**). Tier-A candidates (slice arithmetic, determinant identity, the r-system contradiction) are `open` pending kit scripts — upgrading them to `machine-checked` requires only exact-arithmetic checks against the paper's ancillary verification code.
