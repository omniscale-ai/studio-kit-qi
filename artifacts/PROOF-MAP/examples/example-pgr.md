---
date: 2026-08-10
---

# Proof map: PGR Theorem 1 (bipartite bound information)

**ID**: `cpt-qi-pm-pgr-thm1`

## Theorem

`cpt-qi-thm-pgr-bound-info`

## Dependency Graph

Following the paper's own decomposition (Appendix A: "four logically separate parts"):

| Node | Statement (one line) | Status | Feeds |
|---|---|---|---|
| `cpt-qi-lem-pgr-slices-product` | Slices A, B of the J-channel output are rank-one ⇒ X ⊥ Y \| J | **open** (tier A pending: exact 2×2 arithmetic) | part-1 |
| `cpt-qi-lem-pgr-erasure-identity` | BEC(1/2): I(U;Z) = ½·I(U;L) (App. B.2) | **cited** (tier B candidate) | part-2 |
| `cpt-qi-lem-pgr-bsc-sdpi` | BSC strong data-processing: I(U;J) ≤ (1−2δ)²·I(U;L) (App. B.3) | **cited** (tier B candidate: convexity of g(q)) | part-2 |
| `cpt-qi-lem-pgr-ggk` | Less-noisy dominance ⇒ S(X;Y‖Z) ≤ S(X;Y‖J) (GGK Prop. 1; App. C) | **cited** (formalization = open gap) | part-3 |
| `cpt-qi-lem-pgr-det-identity` | det(aA + bB) = ab/36 for all real a, b (App. E.2) | **open** (tier A pending: symbolic 2×2 determinant) | part-4 |
| `cpt-qi-lem-pgr-no-channel` | No stochastic channel Z→J reproduces the joint slices (r-system contradiction, Eq. 12) | **open** (tier A pending: tiny LP infeasibility → CLAIM+CERTIFICATE candidate) | part-4 |
| `cpt-qi-lem-pgr-compactness` | Finite alphabets: zero intrinsic info ⇒ exact decoupling channel exists (App. F) | **cited** | part-4 |

Parts: **part-1** (J decouples X,Y) + **part-2** (Eve's channel less-noisy dominates J) + **part-3** (dominance ⇒ S = 0) give the vanishing-rate half; **part-1** + **part-4** (no channel Z→J ⇒ any exact decoupler impossible ⇒ I(X;Y↓Z) > 0) give the positive-cost half.

## Load-Bearing Nodes

All seven nodes above are load-bearing (the paper's four parts each rest on their listed lemmas; no redundant routes in v1). Current bottleneck statuses: 4 × `open` (all tier-A/B upgradable by computation), 3 × `cited` (GGK and compactness are the deep external dependencies; erasure identity is elementary).
