---
status: open
date: 2026-08-10
---

# Determinant identity: det(aA + bB) = ab/36 (rank-one rigidity core)


<!-- toc -->

- [Statement](#statement)
- [Role in Proof](#role-in-proof)
- [Verification](#verification)

<!-- /toc -->

**ID**: `cpt-qi-lem-pgr-det-identity`
## Statement

For all real a, b: det(aA + bB) = ab/36, where A, B are the J-slices of `cpt-qi-lem-pgr-slices-product`. Consequently any nonzero, entrywise-nonnegative, rank-one combination aA + bB is a positive multiple of A or of B — the only two nonnegative rank-one rays in the span.

## Role in Proof

Part-4 of `cpt-qi-pm-pgr-thm1`: the rigidity that forces any exact decoupling channel Z→Z̃ to reproduce the slices of J exactly, reducing "no decoupler" to `cpt-qi-lem-pgr-no-channel`.

## Verification

- **Route: tier A** — expand det((1/18)[[4a+b, 2a+2b],[2a+2b, a+4b]]) symbolically: ((4a+b)(a+4b) − 4(a+b)²)/18² = 9ab/324 = ab/36 (paper Eqs. E.3–E.4). Two-variable polynomial identity — exact symbolic check, script pending.
- Present status **open**: no artifact yet.
