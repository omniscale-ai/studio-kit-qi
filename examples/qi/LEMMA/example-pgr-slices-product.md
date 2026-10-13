---
status: open
date: 2026-08-10
---

# J-slices are rank-one: J decouples X from Y (PGR, part 1)


<!-- toc -->

- [Statement](#statement)
- [Role in Proof](#role-in-proof)
- [Verification](#verification)

<!-- /toc -->

**ID**: `cpt-qi-lem-pgr-slices-product`
## Statement

The slices of the PGR source conditioned on J, A = (1/18)[[4,2],[2,1]] and B = (1/18)[[1,2],[2,4]], are rank-one matrices; hence, conditioned on either value of J, the pair (X,Y) is a product distribution: X ⊥ Y | J. Moreover A + B = P_XY.

## Role in Proof

Part-1 of `cpt-qi-pm-pgr-thm1`. Both halves of the theorem route through it: the vanishing-rate half needs X ⊥ Y | J to apply GGK with S(X;Y‖J) = 0; the positive-cost half needs A, B as the rank-one rays of the rigidity argument.

## Verification

- **Route: tier A** — exact 2×2 arithmetic: det A = det B = 0, factorizations A = (1/18)(2;1)(2 1), B = (1/18)(1;2)(1 2), and A + B = (1/18)[[5,4],[4,5]] = P_XY. Kit script pending.
- Present status **open**: no artifact yet (paper's ancillary code covers it; independent check trivial).
