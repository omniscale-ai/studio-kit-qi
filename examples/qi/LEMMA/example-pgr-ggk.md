---
status: cited
date: 2026-08-10
---

# Less-noisy dominance bounds the secret-key rate (GGK)


<!-- toc -->

- [Statement](#statement)
- [Role in Proof](#role-in-proof)
- [Verification](#verification)

<!-- /toc -->

**ID**: `cpt-qi-lem-pgr-ggk`
## Statement

For a fixed honest-party marginal P_XY, if Eve's channel dominates another channel in the less-noisy sense, P_Z|XY ⪰_ln P_J|XY (i.e., I(U;Z) ≥ I(U;J) for every auxiliary U and every input law), then S(X;Y‖Z) ≤ S(X;Y‖J) — against arbitrary interactive public-discussion protocols at all blocklengths.

## Role in Proof

Feeds part-3 of `cpt-qi-pm-pgr-thm1`: combined with X ⊥ Y | J (part-1) it yields S(X;Y‖Z) ≤ S(X;Y‖J) = 0 — the entire vanishing-rate half rests on this node.

## Verification

- **Route: cited.** Exact external statement: Gohari, Günlü, Kramer, *Coding for positive rate in the source model key agreement problem*, IEEE Trans. Inf. Theory 66:6303 (2020), Proposition 1; PGR reproduce a self-contained proof as their Appendix C (Lemmas C.1 tensorization + Prop. C.2).
- Reference resolves (audited 2026-08-10 against IEEE Xplore listing in the paper's bibliography).
- **Upgrade path:** tier C — mechanization in Lean 4 (Mathlib entropy + a new Maurer–Wolf protocol model). Identified as unmechanized in any proof assistant (Deep Research survey 2026-08-09); this is the "very high difficulty, publishable" node. Until then, `cited` is this node's honest ceiling — and it is the trust bottleneck of the whole theorem.
