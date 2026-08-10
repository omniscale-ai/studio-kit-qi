---
status: certified
date: 2026-08-10
---

# EJM distribution is not 3-local in the triangle network

**ID**: `cpt-qi-claim-ejm-triangle-nonlocal`

## Statement

`cpt-qi-claim-ejm-triangle-nonlocal`: The distribution p_EJM over outcomes (a,b,c) ∈ {1,2,3,4}³ defined in Exact Data admits **no** 3-local triangle model: there exist no response functions p_A, p_B, p_C and no independent latent variables α, β, γ (of any cardinality) realizing the decomposition given in Model Class.

## Model Class

Classical triangle-network (3-local) models:

p(a,b,c) = ∫ dα dβ dγ · p_A(a|β,γ) · p_B(b|γ,α) · p_C(c|α,β)

with α, β, γ independent (each may be taken uniform on [0,1] w.l.o.g.), and p_A, p_B, p_C arbitrary nonnegative normalized response functions. The set of such distributions is closed and non-convex; membership is excluded here via a relaxation: incompatibility with the 2×2×4 inflation linear program implies non-membership (inflation soundness: any 3-local p induces an inflation distribution q satisfying the LP constraints — Wolfe–Spekkens–Fritz, arXiv:1609.00672).

## Exact Data

The EJM distribution: each party performs the Elegant Joint Measurement (Gisin 2019) on its two qubits from two independent singlets. Fully symmetric under S₄ (outcome relabeling) × S₃ (party permutation); characterized by three rational values:

| Outcome pattern | Probability | Count |
|---|---|---|
| a = b = c = k | 25/256 | 4 |
| exactly two equal | 1/256 | 36 |
| all different | 5/256 | 24 |

Normalization: 4·(25/256) + 36·(1/256) + 24·(5/256) = 256/256 = 1.

## Provenance

- Conjectured: N. Gisin, *Entropy* 21:325 (2019), §5–6 ([arXiv:1708.05556](https://arxiv.org/abs/1708.05556) lineage).
- Proved: V. Gitton, R. Renner, *The Elegant Joint Measurement is Non-Classical in the Triangle Network*, [arXiv:2510.15143](https://arxiv.org/abs/2510.15143); full account in Gitton's ETH thesis, DOI [10.3929/ethz-b-000745278](https://doi.org/10.3929/ethz-b-000745278).

## Verification

- `cpt-qi-cert-ejm-224-farkas` — Farkas certificate for 2×2×4-inflation LP infeasibility (this kit, CERTIFICATE example).
