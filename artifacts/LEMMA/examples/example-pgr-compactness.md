---
status: cited
date: 2026-08-10
---

# Compactness: zero intrinsic information implies an exact decoupling channel


<!-- toc -->

- [Statement](#statement)
- [Role in Proof](#role-in-proof)
- [Verification](#verification)

<!-- /toc -->

**ID**: `cpt-qi-lem-pgr-compactness`
## Statement

For finite alphabets, I(X;Y↓Z) = 0 implies the infimum in the intrinsic information is attained: there exists a channel Z→Z̃ with I(X;Y|Z̃) = 0 exactly. (Closes the loophole of a sequence of channels decoupling only in the limit.)

## Role in Proof

Part-4 of `cpt-qi-pm-pgr-thm1`: converts "every exact decoupler must simulate J, and none exists" into the strict inequality I(X;Y↓Z) > 0.

## Verification

- **Route: cited** — Christandl–Renner–Wolf 2003 (ISIT), property of intrinsic mutual information; PGR give a self-contained compactness proof in Appendix F.
- **Upgrade path: tier C** — continuity + compactness argument over the channel simplex; natural Lean target once channel preorders exist in Mathlib (part of the identified formalization gap).
