#!/usr/bin/env python3
"""Exact enumeration record for the kit's discovery-layer example (stdlib only).

Correlator expressions E = Σ_{x,y∈{0,1}} c_xy · a_x · b_y on deterministic strategies
(a_0, a_1, b_0, b_1) ∈ {+1, −1}^4 of the (2,2,2) Bell scenario, in integer arithmetic.
This is the EXPLORE phase of examples/qi/RESEARCH-PLAN/example-chsh.md and the
exact instance check (principle P4) cited in the CONJECTURE examples' Evidence tables.
"""
import itertools

PM = (1, -1)
STRATEGIES = list(itertools.product(PM, repeat=4))          # a0 a1 b0 b1


def bell(c, s):
    c00, c01, c10, c11 = c
    a0, a1, b0, b1 = s
    return c00 * a0 * b0 + c01 * a0 * b1 + c10 * a1 * b0 + c11 * a1 * b1


def values(c):
    return sorted({bell(c, s) for s in STRATEGIES})


CHSH = (1, 1, 1, -1)
print("strategies enumerated: %d (exact integer arithmetic)" % len(STRATEGIES))
print("CHSH c=%s: values on deterministic strategies = %s, max = %d" % (CHSH, values(CHSH), max(values(CHSH))))
print()
print("all 16 sign patterns c in {+1,-1}^4:")
odd_ok, even_vals = True, set()
for c in itertools.product(PM, repeat=4):
    neg = c.count(-1)
    v = values(c)
    print("  c=%-16s negatives=%d  values=%s" % (c, neg, v))
    if neg % 2 == 1:
        odd_ok &= set(v) <= {-2, 2}
    else:
        even_vals |= set(v)
print()
print("odd number of negative coefficients  -> values ⊆ {-2, 2}: %s (8 patterns × 16 strategies = 128 cases)" % odd_ok)
print("even number of negative coefficients -> values observed: %s" % sorted(even_vals))
w = ((1, 1, 1, 1), (1, 1, 1, 1))
print("counterexample to 'every ±1 pattern gives only ±2': c=%s, strategy=%s -> E = %d" % (w[0], w[1], bell(*w)))
