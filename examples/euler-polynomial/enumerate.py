#!/usr/bin/env python3
"""Exact enumeration record for the number-theory example pack (stdlib only).

Euler's polynomial f(n) = n² + n + 41 over the naturals, with trial-division primality —
the EXPLORE phase of examples/euler-polynomial/RESEARCH-PLAN/example-euler.md and the exact
instance check (principle P4) cited in the CONJECTURE examples' Evidence tables.
"""


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def f(n):
    return n * n + n + 41


composite = [n for n in range(100) if not is_prime(f(n))]
print("n < 100 with f(n) composite:", composite)
print("f(n) prime for every n < 40:", all(is_prime(f(n)) for n in range(40)))
print("f(40) =", f(40), "=", 41 * 41, "(41 * 41)")
small_primes = [p for p in range(41) if is_prime(p)]
print("primes below 41:", small_primes)
N = 100000
print("no prime below 41 divides f(n) for any n < %d:" % N,
      all(f(n) % p != 0 for p in small_primes for n in range(N)))
print("prime factors of f(40) below 100:", [p for p in range(100) if is_prime(p) and f(40) % p == 0])
