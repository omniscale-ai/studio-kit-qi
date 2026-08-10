#!/usr/bin/env python3
"""
check_certificate.py — independent (clean-room) checker for nonlocality
certificates produced by the fast-inflation codebase (Gitton & Renner,
arXiv:2510.15143).

This is a from-scratch re-implementation of the *mathematical checking
predicate* only. No code is shared with fast-inflation; the conventions it
relies on are documented in CERTIFICATE-SEMANTICS.md (same directory) and
were reverse-engineered from the C++ sources and validated against
instrumented reference runs.

What it does
------------
1. Parses a certificate file (text format, version 5).
2. Reconstructs the target distribution from a small built-in registry
   (currently: "srb" — the shared random bit with visibility read from the
   certificate's free-metadata line).
3. Rebuilds the inflation (party layout, symmetry group) and, for each
   constraint, the symmetrized marginal basis in which the stored dual
   vector lives.
4. For every deterministic inflation event e, evaluates the certificate
   score <d, Phi(e)> in exact integer/rational arithmetic.
5. Verdict: the certificate is VALID iff min_e score(e) > 0 (strictly),
   which proves the underlying inflation LP infeasible, i.e. the target
   distribution is not triangle-local.

Usage
-----
    python3 check_certificate.py <certificate-file> [--repo <fast-inflation-root>]
                                 [--target srb] [--check-run <output.md>]

The --repo argument is only used to resolve a relative certificate path
against the repository's data/ directory.

Exit codes: 0 = certificate valid (min > 0), 1 = not valid (min <= 0),
2 = error (parse/consistency failure).

EJM extension point
-------------------
The scoring core is factored so that the event enumerator is pluggable
(see minimize_score(..., event_iter=...)). For the EJM case (4 outcomes,
2x2x4 inflation, 20 parties) raw enumeration (4^20 events) is infeasible;
a symtree-based enumerator over symmetrized event representatives can be
passed in instead. Everything else (basis reconstruction, per-event exact
scoring) is size-agnostic.
"""

import argparse
import hashlib
import itertools
import math
import os
import platform
import re
import sys
import time
from fractions import Fraction

# ----------------------------------------------------------------------------
# Small exact tensor: maps outcome-tuples of fixed length to integer
# numerators over a common denominator.
# ----------------------------------------------------------------------------


class Tensor:
    def __init__(self, n_parties, base, denom=1):
        self.n_parties = n_parties
        self.base = base
        self.denom = denom
        self.num = {e: 0 for e in itertools.product(range(base), repeat=n_parties)}

    def simplify(self):
        """Divide the denominator and all numerators by their common GCD."""
        g = self.denom
        for v in self.num.values():
            g = math.gcd(g, v)
            if g == 1:
                return
        for e in self.num:
            self.num[e] //= g
        self.denom //= g

    def events(self):
        return itertools.product(range(self.base), repeat=self.n_parties)


def tensor_product(factors):
    """Tensor product of Tensor factors (party-index order = factor order),
    numerators multiplied, denominators multiplied, then simplified."""
    n = sum(f.n_parties for f in factors)
    base = factors[0].base
    out = Tensor(n, base)
    out.denom = 1
    for f in factors:
        out.denom *= f.denom
    for e in out.events():
        v = 1
        pos = 0
        for f in factors:
            v *= f.num[e[pos:pos + f.n_parties]]
            pos += f.n_parties
        out.num[e] = v
    out.simplify()
    return out


# ----------------------------------------------------------------------------
# Target-distribution registry.
# Each entry: name -> callable(cert_free_metadata_line) -> (Tensor p, short_name)
# The tensor is the full 3-party distribution over the triangle network with
# parties (A, B, C) in this order.
# ----------------------------------------------------------------------------


def build_srb(free_metadata):
    """Shared random bit with visibility v:
        p(a,b,c) = v * (1/2 if a==b==c else 0) + (1-v)/8
    over 2 outcomes. Exact integer form: with v = vn/vd,
        numerator(a,b,c) = (vd - vn) + 4*vn*[a==b==c],  denominator = 8*vd.
    The visibility is parsed from the certificate's free metadata line
    ('... visibility 41422/100000 ...'); defaults to 41422/100000."""
    m = re.search(r"visibility\s+(\d+)\s*/\s*(\d+)", free_metadata)
    vn, vd = (int(m.group(1)), int(m.group(2))) if m else (41422, 100000)
    if not (0 <= vn <= vd):
        raise ValueError("visibility out of range: %d/%d" % (vn, vd))
    t = Tensor(3, 2, denom=8 * vd)
    for e in t.events():
        t.num[e] = (vd - vn) + (4 * vn if e[0] == e[1] == e[2] else 0)
    t.simplify()
    return t, "SRB", (vn, vd)


def build_ejm(free_metadata):
    raise NotImplementedError(
        "EJM target registered but not implemented yet: requires the exact "
        "4-outcome Elegant Joint Measurement distribution and a symtree-based "
        "event enumerator (see module docstring, 'EJM extension point').")


TARGETS = {"srb": build_srb, "ejm": build_ejm}


# ----------------------------------------------------------------------------
# Certificate file parsing (text format, stream version 5).
# ----------------------------------------------------------------------------


def parse_signed_hex(s):
    if len(s) < 2 or s[0] not in "+-":
        raise ValueError("bad signed hex value: %r" % s)
    v = int(s[1:], 16)
    return -v if s[0] == "-" else v


class Certificate:
    __slots__ = ("free_metadata", "inflation_metadata", "constraints", "path")
    # constraints: list of (pretty_description, [coefficients])


def parse_certificate(path):
    with open(path, "r") as f:
        lines = f.read().split("\n")
    it = iter(lines)

    def nxt():
        try:
            return next(it)
        except StopIteration:
            raise ValueError("unexpected end of certificate file")

    cert = Certificate()
    cert.path = path
    version = int(nxt(), 16)
    if version != 5:
        raise ValueError("unsupported file-stream version %d (expected 5)" % version)
    cert.free_metadata = nxt()
    if nxt() != "METADATA":
        raise ValueError("expected METADATA line")
    cert.inflation_metadata = nxt()
    if nxt() != "CONSTRAINT SET":
        raise ValueError("expected CONSTRAINT SET line")
    descriptions = []
    line = nxt()
    while line != "DUAL VECTOR":
        descriptions.append(line)
        line = nxt()
    if not descriptions:
        raise ValueError("no constraints listed")
    cert.constraints = []
    for desc in descriptions:
        repeated = nxt()
        if repeated != desc:
            raise ValueError("DUAL VECTOR section constraint mismatch:\n  %s\n  %s"
                             % (desc, repeated))
        n = int(nxt(), 16)
        coeffs = [parse_signed_hex(nxt()) for _ in range(n)]
        cert.constraints.append((desc, coeffs))
    return cert


def parse_constraint_description(pretty):
    """Invert the pretty form
        q(G0 , G1 , ... [, R]) = p(G0) * p(G1) * ... [* q(R)]
    back into the party-name groups (G0, ..., Gk-1, R) with R possibly ''.
    Returns (p_groups, rhs_group) where each group is a list of party names."""
    m = re.match(r"^q\((.*)\) = (.*)$", pretty)
    if not m:
        raise ValueError("cannot parse constraint: %r" % pretty)
    lhs_groups = [g.strip() for g in m.group(1).split(" , ")]
    rhs_factors = [f.strip() for f in m.group(2).split(" * ")]
    p_groups = []
    rhs_group = ""
    for f in rhs_factors:
        fm = re.match(r"^([pq])\((.*)\)$", f)
        if not fm:
            raise ValueError("cannot parse constraint factor: %r" % f)
        if fm.group(1) == "p":
            p_groups.append(fm.group(2))
        else:
            if rhs_group:
                raise ValueError("multiple q(...) factors in %r" % pretty)
            rhs_group = fm.group(2)
    expected_lhs = p_groups + ([rhs_group] if rhs_group else [])
    if lhs_groups != expected_lhs:
        raise ValueError("inconsistent constraint sides in %r" % pretty)
    split = lambda g: [p for p in g.split(",") if p]
    return [split(g) for g in p_groups], split(rhs_group)


# ----------------------------------------------------------------------------
# Network + distribution symmetries (triangle network).
# A symmetry is a pair (party_perm pi with parity, outcome_perm sigma); it acts
# on an event e by out[pi[i]] = sigma[e[i]].
# ----------------------------------------------------------------------------

NET_PARTY_PERMS = [  # (image tuple, is_even) — all permutations of (0,1,2)
    ((0, 1, 2), True), ((0, 2, 1), False), ((1, 0, 2), False),
    ((1, 2, 0), True), ((2, 0, 1), True), ((2, 1, 0), False),
]


def distribution_symmetries(p):
    """All (party_perm, parity, outcome_perm) leaving the distribution
    tensor p invariant."""
    syms = []
    for pp, even in NET_PARTY_PERMS:
        for op in itertools.permutations(range(p.base)):
            ok = True
            for e in p.events():
                out = [0, 0, 0]
                for i in range(3):
                    out[pp[i]] = op[e[i]]
                if p.num[tuple(out)] != p.num[e]:
                    ok = False
                    break
            if ok:
                syms.append((pp, even, op))
    return syms


# ----------------------------------------------------------------------------
# Inflation: party layout and symmetry group.
# ----------------------------------------------------------------------------


class Inflation:
    def __init__(self, size, n_outcomes, distr_syms):
        self.size = list(size)        # copies of (alpha, beta, gamma) sources
        self.n_outcomes = n_outcomes
        self._init_parties()
        self._init_symmetries(distr_syms)

    def _init_parties(self):
        """Party ordering convention: enumerate a nested sequence of inflation
        sizes from (1,1,1) up to the full size (incrementing source counts one
        at a time, in source order); within each step, enumerate source tuples
        in product order (last index fastest) and network parties A,B,C;
        register party (t, (left, right)) with left = sources[(t+1)%3],
        right = sources[(t+2)%3] on first sight. Names: 'A'+str(left)+str(right)
        etc.  So Ajk reads (beta_j, gamma_k), Bjk reads (gamma_j, alpha_k),
        Cjk reads (alpha_j, beta_k)."""
        steps = [[1, 1, 1]]
        while steps[-1] != self.size:
            cur = list(steps[-1])
            for i in range(3):
                if cur[i] < self.size[i]:
                    cur[i] += 1
                    steps.append(list(cur))
        self.parties = []             # list of (type, (left, right))
        self.party_index = {}         # (type, (left, right)) -> index
        self.party_names = []
        self.name_index = {}
        for step in steps:
            for sources in itertools.product(*(range(k) for k in step)):
                for t in range(3):
                    left = sources[(t + 1) % 3]
                    right = sources[(t + 2) % 3]
                    party = (t, (left, right))
                    if party not in self.party_index:
                        self.party_index[party] = len(self.parties)
                        self.parties.append(party)
                        name = "ABC"[t] + str(left) + str(right)
                        self.party_names.append(name)
                        self.name_index[name] = len(self.parties) - 1
        self.n_parties = len(self.parties)

    def _init_symmetries(self, distr_syms):
        """Inflation symmetry group = { source_perm_sym o lifted(network_sym) }
        with the network sym's outcome permutation carried along.  Network
        symmetries are 'applicable' only if their party permutation leaves the
        inflation size vector invariant (acting by out[pi[i]] = size[i]).
        Lifting: party (t,(j,k)) -> (pi[t], (j,k)) for even pi, (pi[t], (k,j))
        for odd pi. A source symmetry (one permutation per source type) maps
        (t,(j,k)) -> (t, (s_{left_type}[j], s_{right_type}[k]))."""
        self.n_distr_syms = len(distr_syms)
        applicable = []
        for pp, even, op in distr_syms:
            image = [0, 0, 0]
            for i in range(3):
                image[pp[i]] = self.size[i]
            if image == self.size:
                applicable.append((pp, even, op))

        lifted = []
        for pp, even, op in applicable:
            pmap = [None] * self.n_parties
            for idx, (t, (j, k)) in enumerate(self.parties):
                img = (j, k) if even else (k, j)
                pmap[idx] = self.party_index[(pp[t], img)]
            lifted.append((pmap, op))

        source_syms = []
        for pa in itertools.permutations(range(self.size[0])):
            for pb in itertools.permutations(range(self.size[1])):
                for pg in itertools.permutations(range(self.size[2])):
                    perms = (pa, pb, pg)
                    pmap = [None] * self.n_parties
                    for idx, (t, (j, k)) in enumerate(self.parties):
                        lt, rt = (t + 1) % 3, (t + 2) % 3
                        pmap[idx] = self.party_index[(t, (perms[lt][j], perms[rt][k]))]
                    source_syms.append(pmap)

        group = set()
        for pmap_net, op in lifted:
            for pmap_src in source_syms:
                combined = tuple(pmap_src[pmap_net[i]] for i in range(self.n_parties))
                group.add((combined, tuple(op)))
        # canonical order (irrelevant mathematically, kept deterministic)
        self.symmetries = sorted(group, key=lambda s: (s[1], s[0]))


# ----------------------------------------------------------------------------
# Constraint machinery: constraint group, marginal permutations, dual-vector
# orbit basis, reduced RHS dual vector.
# ----------------------------------------------------------------------------


def constraint_group(inflation, lhs_parties, rhs_parties):
    """Subgroup of the inflation symmetries whose party permutation leaves
    both A := set(lhs) - set(rhs) and B := set(rhs) invariant (as sets)."""
    a_set = frozenset(lhs_parties) - frozenset(rhs_parties)
    b_set = frozenset(rhs_parties)
    group = []
    for pmap, op in inflation.symmetries:
        if frozenset(pmap[p] for p in a_set) == a_set and \
           frozenset(pmap[p] for p in b_set) == b_set:
            group.append((pmap, op))
    return group


def marginal_symmetries(cgroup, marg_parties):
    """Down-convert the constraint group to permutations of the marginal's
    slot indices (deduplicated): msym[i] = slot of pmap[party at slot i]."""
    if not marg_parties:
        return []
    inf_to_slot = {p: i for i, p in enumerate(marg_parties)}
    out = set()
    for pmap, op in cgroup:
        msym = tuple(inf_to_slot[pmap[marg_parties[i]]]
                     for i in range(len(marg_parties)))
        out.add((msym, tuple(op)))
    return sorted(out)


def inverse_perm(p):
    inv = [0] * len(p)
    for i, v in enumerate(p):
        inv[v] = i
    return tuple(inv)


def marginal_permutations(inflation, marg_parties, marg_syms):
    """The reduced set of marginal permutations: orbit representatives (under
    the marginal-symmetry action) of { (sigma_g, [pi_g(p) for p in marg]) :
    g in inflation group }.  A candidate (sigma, parties) is a representative
    iff no marginal symmetry (rho, tau) produces a strictly smaller pair
    (sigma o tau^{-1}, parties') with parties'[rho[i]] = parties[i]; ordering
    is lexicographic on (outcome image tuple, parties tuple).
    Returns the sorted list of (parties_tuple, inverse_outcome_tuple) ready
    for event extraction: extracted[i] = inv_sigma[event[parties[i]]]."""
    if not marg_parties:
        return []
    reps = set()
    for pmap, op in inflation.symmetries:
        cand_parties = tuple(pmap[p] for p in marg_parties)
        cand = (tuple(op), cand_parties)
        is_rep = True
        for rho, tau in marg_syms:
            tau_inv = inverse_perm(tau)
            other_outcome = tuple(op[tau_inv[i]] for i in range(len(op)))
            other_parties = [0] * len(cand_parties)
            for i, v in enumerate(cand_parties):
                other_parties[rho[i]] = v
            if (other_outcome, tuple(other_parties)) < cand:
                is_rep = False
                break
        if is_rep:
            reps.add(cand)
    return [(parties, inverse_perm(op)) for op, parties in sorted(reps)]


def dual_vector_orbits(n_slots, n_outcomes, marg_syms):
    """Orbits of marginal events (length n_slots, outcomes 0..n_outcomes-1)
    under the marginal symmetries acting by out[rho[i]] = tau[e[i]].
    Returns the list of orbits in increasing order of their lexicographically
    minimal representative; this order defines the quovec (stored dual vector
    coefficient) indexing."""
    orbits = []
    seen = set()
    for e in itertools.product(range(n_outcomes), repeat=n_slots):
        if e in seen:
            continue
        orbit = {e}
        for rho, tau in marg_syms:
            out = [0] * n_slots
            for i in range(n_slots):
                out[rho[i]] = tau[e[i]]
            orbit.add(tuple(out))
        seen |= orbit
        orbits.append(sorted(orbit))
    orbits.sort(key=lambda o: o[0])
    return orbits


def target_marginal(p, group_names):
    """Marginal of the (already simplified) target distribution tensor over
    the network parties named in group_names with copy indices stripped, e.g.
    ['A00','B00','C00'] -> parties (A,B,C).  Network party indices must be
    strictly increasing (mirrors the reference convention).  Simplified."""
    idx = ["ABC".index(name[0]) for name in group_names]
    if any(b <= a for a, b in zip(idx, idx[1:])):
        raise ValueError("target marginal parties not strictly increasing: %s"
                         % group_names)
    if idx == [0, 1, 2]:
        return p
    t = Tensor(len(idx), p.base, denom=p.denom)
    for e in p.events():
        key = tuple(e[i] for i in idx)
        t.num[key] += p.num[e]
    t.simplify()
    return t


class CompiledConstraint:
    """Everything needed to score one constraint on an inflation event."""
    __slots__ = ("pretty", "F", "lhs_extractors", "lhs_denom",
                 "R", "rhs_extractors", "rhs_denom", "rhs_scalar",
                 "n_orbits", "lhs_parties", "rhs_parties")


def compile_constraint(inflation, pretty, coeffs, p):
    p_groups, rhs_group = parse_constraint_description(pretty)
    all_groups = p_groups + [rhs_group]
    lhs_parties = [inflation.name_index[n] for g in all_groups for n in g]
    rhs_parties = [inflation.name_index[n] for n in rhs_group]

    cgroup = constraint_group(inflation, lhs_parties, rhs_parties)
    if not cgroup:
        raise ValueError("empty constraint group for %r" % pretty)

    n_out = inflation.n_outcomes

    # LHS: dual vector F over marginal events, from the stored coefficients.
    lhs_syms = marginal_symmetries(cgroup, lhs_parties)
    orbits = dual_vector_orbits(len(lhs_parties), n_out, lhs_syms)
    if len(orbits) != len(coeffs):
        raise ValueError("constraint %r: file has %d coefficients but the "
                         "symmetrized basis has %d orbits"
                         % (pretty, len(coeffs), len(orbits)))
    F = {}
    for i, orbit in enumerate(orbits):
        for e in orbit:
            F[e] = coeffs[i]

    cc = CompiledConstraint()
    cc.pretty = pretty
    cc.F = F
    cc.n_orbits = len(orbits)
    cc.lhs_parties = lhs_parties
    cc.rhs_parties = rhs_parties
    cc.lhs_extractors = marginal_permutations(inflation, lhs_parties, lhs_syms)
    cc.lhs_denom = len(cc.lhs_extractors)

    # RHS: T = tensor product of target marginals (factor order = group order,
    # party order within each factor = strictly increasing network parties).
    T = tensor_product([target_marginal(p, g) for g in p_groups])
    if rhs_parties:
        rhs_syms = marginal_symmetries(cgroup, rhs_parties)
        cc.rhs_extractors = marginal_permutations(inflation, rhs_parties, rhs_syms)
        cc.rhs_denom = T.denom * len(cc.rhs_extractors)
        # Reduced RHS dual vector: R(r) = sum_t T(t) * F(t ++ r)
        cc.R = {}
        for r in itertools.product(range(n_out), repeat=len(rhs_parties)):
            cc.R[r] = sum(T.num[t] * F[t + r] for t in T.events())
        cc.rhs_scalar = None
    else:
        cc.rhs_extractors = []
        cc.rhs_denom = T.denom  # empty marginal contributes denominator 1
        cc.R = None
        cc.rhs_scalar = sum(T.num[t] * F[t] for t in T.events())
    return cc


# ----------------------------------------------------------------------------
# Scoring and minimization.
# ----------------------------------------------------------------------------


def integer_scales(constraints):
    """Positive integer scale factors matching the reference implementation:
    with P = prod_c (lhs_denom_c * rhs_denom_c), the scales are
    P / lhs_denom_c and P / rhs_denom_c, all divided by their common GCD g.
    The integer score equals (P/g) times the natural rational score."""
    P = 1
    for c in constraints:
        P *= c.lhs_denom * c.rhs_denom
    scales = []
    for c in constraints:
        scales.append((P // c.lhs_denom, P // c.rhs_denom))
    g = 0
    for a, b in scales:
        g = math.gcd(g, math.gcd(a, b))
    scales = [(a // g, b // g) for a, b in scales]
    return scales, P, g


def score_event_int(e, constraints, scales):
    """Integer certificate score of inflation event e (tuple of outcomes):
    sum_c [ lhs_scale_c * sum_{(parties,inv) in lhs perms} F(extract)
          - rhs_scale_c * (R_scalar or sum over rhs perms of R(extract)) ]."""
    total = 0
    for c, (sl, sr) in zip(constraints, scales):
        acc = 0
        for parties, inv in c.lhs_extractors:
            acc += c.F[tuple(inv[e[p]] for p in parties)]
        total += sl * acc
        if c.rhs_scalar is not None:
            total -= sr * c.rhs_scalar
        else:
            acc = 0
            for parties, inv in c.rhs_extractors:
                acc += c.R[tuple(inv[e[p]] for p in parties)]
            total -= sr * acc
    return total


def raw_event_iter(n_parties, n_outcomes):
    """Full enumeration of deterministic inflation events.
    EXTENSION POINT: for large inflations (e.g. EJM 2x2x4, 20 parties,
    4 outcomes) replace this with a generator over symmetrized event
    representatives (symtree). Since the score function is invariant under
    the inflation symmetry group, min over representatives = min over all."""
    return itertools.product(range(n_outcomes), repeat=n_parties)


def minimize_score(constraints, scales, event_iter):
    best = None
    best_event = None
    n = 0
    for e in event_iter:
        s = score_event_int(e, constraints, scales)
        n += 1
        if best is None or s < best:
            best = s
            best_event = e
    return best, best_event, n


# ----------------------------------------------------------------------------
# Main driver.
# ----------------------------------------------------------------------------


def check(cert_path, target_name):
    t0 = time.time()
    cert = parse_certificate(cert_path)

    # Metadata: parse inflation size and outcomes, cross-check counts later.
    md = cert.inflation_metadata
    m = re.search(r"Inflation size:\s*(\d+)x(\d+)x(\d+)", md)
    if not m:
        raise ValueError("cannot parse inflation size from metadata: %r" % md)
    size = [int(m.group(i)) for i in (1, 2, 3)]
    m = re.search(r"Outcomes per party:\s*(\d+)", md)
    if not m:
        raise ValueError("cannot parse outcome count from metadata: %r" % md)
    n_outcomes = int(m.group(1))
    if "Triangle network" not in md:
        raise ValueError("only the triangle network is supported")

    p, short_name, vis = TARGETS[target_name](cert.free_metadata)
    if n_outcomes != p.base:
        raise ValueError("metadata says %d outcomes, target %r has %d"
                         % (n_outcomes, target_name, p.base))

    distr_syms = distribution_symmetries(p)
    inflation = Inflation(size, n_outcomes, distr_syms)

    # Cross-check symmetry counts against the metadata line when present.
    m = re.search(r"Using the (\d+) symmetries", md)
    if m and int(m.group(1)) != len(distr_syms):
        raise ValueError("metadata declares %s distribution symmetries, "
                         "reconstructed %d" % (m.group(1), len(distr_syms)))
    m = re.search(r"has (\d+) symmetries", md)
    if m and int(m.group(1)) != len(inflation.symmetries):
        raise ValueError("metadata declares %s inflation symmetries, "
                         "reconstructed %d" % (m.group(1), len(inflation.symmetries)))

    constraints = [compile_constraint(inflation, pretty, coeffs, p)
                   for pretty, coeffs in cert.constraints]
    scales, P, g = integer_scales(constraints)

    min_int, best_event, n_events = minimize_score(
        constraints, scales,
        raw_event_iter(inflation.n_parties, inflation.n_outcomes))

    min_frac = Fraction(min_int * g, P)
    wall = time.time() - t0

    return {
        "certificate": cert,
        "target": target_name,
        "short_name": short_name,
        "visibility": vis,
        "inflation_size": size,
        "n_outcomes": n_outcomes,
        "n_parties": inflation.n_parties,
        "n_distr_syms": len(distr_syms),
        "n_inflation_syms": len(inflation.symmetries),
        "constraints": constraints,
        "scales": scales,
        "scale_P": P,
        "scale_gcd": g,
        "n_events": n_events,
        "min_int": min_int,
        "min_frac": min_frac,
        "best_event": best_event,
        "valid": min_int > 0,
        "wall_time_s": wall,
    }


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def write_check_run(res, out_path, argv):
    r = res
    cert = r["certificate"]
    try:
        import resource
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_str = "%.1f MB (ru_maxrss)" % (peak / (1024 * 1024 if sys.platform == "darwin" else 1024))
    except Exception:
        peak_str = "n/a"
    vn, vd = r["visibility"]
    lines = [
        "---",
        "status: %s" % ("pass" if r["valid"] else "fail"),
        "date: %s" % time.strftime("%Y-%m-%d"),
        "generated-by: check_certificate.py v1.0 (--check-run)",
        "---",
        "",
        "# %s %s certificate, independent Python checker" % (
            r["short_name"], "x".join(map(str, r["inflation_size"]))),
        "",
        "**ID**: `cpt-fastinflation-run-%s-%s-py`" % (
            r["target"], "".join(map(str, r["inflation_size"]))),
        "",
        "## Certificate",
        "",
        "- **File checked**: %s" % cert.path,
        "- **SHA-256 observed**: `%s`" % sha256_file(cert.path),
        "- **Auxiliary inputs observed**: none (target distribution %s with visibility"
        % r["short_name"],
        "  %d/%d is reconstructed from the built-in registry + certificate metadata)" % (vn, vd),
        "",
        "## Checker",
        "",
        "`scripts/check_certificate.py` v1.0 — clean-room independent implementation",
        "(Python 3, exact integer/`fractions.Fraction` arithmetic). Shares no code with",
        "the certificate producer `fast-inflation` (C++); conventions documented in",
        "`scripts/CERTIFICATE-SEMANTICS.md`.",
        "",
        "## Environment",
        "",
        "- OS: %s %s (%s)" % (platform.system(), platform.release(), platform.machine()),
        "- Python: %s" % platform.python_version(),
        "- Exact arithmetic: Python built-in int + fractions.Fraction (stdlib)",
        "",
        "## Command",
        "",
        "```",
        "python3 " + " ".join(argv),
        "```",
        "",
        "## Result",
        "",
        "- **Verdict**: %s — min event score is %s, so the inflation LP %s"
        % ("pass" if r["valid"] else "fail",
           "strictly positive" if r["valid"] else "NOT strictly positive",
           "is infeasible: the target distribution is triangle-nonlocal"
           if r["valid"] else "infeasibility is NOT certified"),
        "- **Wall time**: %.2f s" % r["wall_time_s"],
        "- **Peak memory**: %s" % peak_str,
        "- Events enumerated (raw, no symmetrization): %d" % r["n_events"],
        "- Exact minimum score: %s = %s (integer-scaled: %d, common scale %d/%d)"
        % (r["min_frac"], float(r["min_frac"]), r["min_int"], r["scale_P"], r["scale_gcd"]),
        "- Minimizing inflation event: %s" % "".join(map(str, r["best_event"])),
        "- Constraint basis sizes: %s" % ", ".join(
            "%d" % c.n_orbits for c in r["constraints"]),
        "",
        "## Attestation",
        "",
        "Record emitted by check_certificate.py --check-run at run time; the values",
        "above are the script's own outputs (stdout log of the same run).",
        "",
    ]
    with open(out_path, "w") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description="Independent checker for "
                                 "fast-inflation nonlocality certificates.")
    ap.add_argument("certificate", help="path to certificate .txt file")
    ap.add_argument("--repo", default=None,
                    help="fast-inflation repo root (used to resolve relative "
                         "certificate paths)")
    ap.add_argument("--target", default="srb", choices=sorted(TARGETS),
                    help="target distribution (default: srb)")
    ap.add_argument("--check-run", default=None, metavar="OUT.md",
                    help="write a CHECK-RUN record to this file")
    args = ap.parse_args()

    path = args.certificate
    if not os.path.exists(path) and args.repo:
        for cand in (os.path.join(args.repo, path),
                     os.path.join(args.repo, "data", path)):
            if os.path.exists(cand):
                path = cand
                break
    if not os.path.exists(path):
        print("error: certificate file not found: %s" % args.certificate)
        return 2

    try:
        res = check(path, args.target)
    except (ValueError, NotImplementedError) as exc:
        print("error: %s" % exc)
        return 2

    vn, vd = res["visibility"]
    print("certificate      : %s" % path)
    print("target           : %s (visibility %d/%d)" % (res["short_name"], vn, vd))
    print("inflation        : %s, %d parties, %d outcomes"
          % ("x".join(map(str, res["inflation_size"])), res["n_parties"],
             res["n_outcomes"]))
    print("symmetries       : %d (distribution), %d (inflation)"
          % (res["n_distr_syms"], res["n_inflation_syms"]))
    for c, (sl, sr) in zip(res["constraints"], res["scales"]):
        print("constraint       : %s" % c.pretty)
        print("                   basis size %d, lhs_denom %d, rhs_denom %d, "
              "scales (+%d, -%d)" % (c.n_orbits, c.lhs_denom, c.rhs_denom, sl, sr))
    print("events enumerated: %d (raw)" % res["n_events"])
    print("min score (int)  : %d" % res["min_int"])
    print("min score (exact): %s" % res["min_frac"])
    print("argmin event     : %s" % "".join(map(str, res["best_event"])))
    print("wall time        : %.2f s" % res["wall_time_s"])
    if res["valid"]:
        print("VERDICT          : VALID — min score > 0: the inflation LP is "
              "infeasible;")
        print("                   the target distribution is NOT triangle-local "
              "at this visibility.")
    else:
        print("VERDICT          : NOT VALID — min score <= 0: certificate does "
              "not certify nonlocality.")

    if args.check_run:
        write_check_run(res, args.check_run, sys.argv)
        print("check-run record : %s" % args.check_run)

    return 0 if res["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
