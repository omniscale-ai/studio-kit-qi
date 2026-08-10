# fast-inflation nonlocality certificates: decoded semantics

Independent-checker specification for certificates produced by the
`fast-inflation` C++ codebase (V. Gitton & R. Renner, arXiv:2510.15143).
Written so that a third implementation needs **no other source**. Every
convention below was extracted by reading the C++ sources (file references
given) and, where marked **[verified]**, cross-validated against instrumented
reference runs of the C++ binary; conventions marked **[inferred]** follow
from source reading only, but all of them feed into the final exact score,
which was verified end-to-end (see §12).

Reference implementation of this spec: `check_certificate.py` (same
directory).

Notation: the triangle network has three sources α, β, γ (types 0, 1, 2) and
three parties A, B, C (types 0, 1, 2). A distribution `p` over `n` outcomes
per party is a rational tensor `p(a,b,c)`. An *inflation* of size
`z = (z0, z1, z2)` has `z0` copies of α, `z1` of β, `z2` of γ.

---

## 1. The claim a certificate encodes

A certificate proves that a specific inflation linear program is infeasible,
which certifies that the target distribution `p` is **not** triangle-local.
The LP asks for a distribution `q` over the inflation's deterministic events
satisfying, for each listed constraint,

    q_{M0 ∪ … ∪ M(k-1) ∪ N} = p_{M0} · … · p_{M(k-1)} · q_N        (LPI form)

where the `Mi` are *injectable sets* of inflation parties, `N` (possibly
empty) is another set of inflation parties, and all groups are pairwise
d-separated. The certificate is a dual vector `d` (one integer coefficient
block per constraint, in a symmetrized basis) such that

    score(e) := ⟨d, Φ(e)⟩ > 0   for EVERY deterministic inflation event e,

where Φ is the (symmetrized, integer-scaled) constraint map defined in §10.
Since any feasible `q` is a convex combination of deterministic events and
⟨d, Φ(q)⟩ = 0 must hold for feasible `q`, a strictly positive minimum proves
infeasibility. The checking predicate is exactly:

    VALID  ⇔  min over all events e of score(e) > 0  (strict).

(C++: `inf::FeasProblem::read_and_check_dual_vector`, `feas_pb.cpp`;
brute-force minimizer `bf_opt.cpp` iterates *raw* events — symmetrization is
an optimization, not part of correctness. **[verified]**)

---

## 2. Certificate file grammar (text serialization, version 5)

Produced by `util::OutputFileStream` in text mode (`file_stream.h/.cpp`) and
`inf::ConstraintSet::io_dual_vector` (`constraint_set.cpp`). One item per
line, `\n`-separated:

```
line 1        : stream version, unsigned hex, must be "5"
line 2        : free-form metadata string (writer-supplied; for SRB it embeds
                the visibility, e.g. "... visibility 41422/100000 = 41.422% ...")
line 3        : literal "METADATA"
line 4        : inflation metadata string (see below)
line 5        : literal "CONSTRAINT SET"
next K lines  : pretty description of each of the K constraints (§6)
next line     : literal "DUAL VECTOR"
then, for each constraint in the same order:
    1 line    : the constraint's pretty description, repeated verbatim
    1 line    : coefficient count, unsigned hexadecimal (e.g. "e" = 14)
    n lines   : one signed-hex integer per line: mandatory sign character
                '+' or '-' followed by lowercase hex magnitude (e.g. "-6f6ab")
```

Numeric encoding rules: unsigned integral types (`Index`, counts, version)
are written as bare hex with **no** sign prefix; signed types (`Num`, the
coefficients) always carry `+`/`-` (`util::to_hex_str`, `file_stream.h`).
**[verified against `data/srb_222_certificate.txt`]**

Inflation metadata line format (`inf::Inflation::get_metadata`,
`inflation.cpp`):

```
Network name: <name>; Outcomes per party: <n>; Inflation size: <z0>x<z1>x<z2>;
[Using the <s> symmetries of the distribution <SHORT>; ]The inflation has <S> symmetries
```

A checker should parse `n`, `(z0,z1,z2)` from this line and *recompute* `s`
and `S` as consistency checks (§5). **[verified: s=12, S=96 for SRB 2×2×2]**

The coefficient count for each constraint must equal the number of
symmetrized basis classes (§8); mismatch ⇒ reject.

---

## 3. Target distribution registry: SRB

`user::get_noisy_srb(v, D)` (`src/user/applications/srb.cpp`): the noisy
shared random bit with visibility `v/D` over 2 outcomes,

    p(a,b,c) = (D - v)/(8D) + [a=b=c] · 4v/(8D)
             = v · (1/2)[a=b=c] + (1 - v) / 8            with v ≡ v/D.

Exact integer form: numerator `(D−v) + 4v·[a=b=c]`, common denominator `8D`.
**[verified against source]**

**Simplification convention (important):** when a distribution tensor is
stored in a `TargetDistr`, it is GCD-simplified: divide the denominator and
all numerators by `gcd(denominator, all numerators)`
(`TensorWithOrbits::init_event_tensor` → `EventTensor::simplify`,
`event_tensor.cpp`). For SRB at 41422/100000 this divides by 2: numerators
{112133, 29289}, denominator 400000. This matters because it changes the RHS
denominators and hence the integer scale factors (§9–10). **[verified: the
final integer score matches C++ only with this simplification]**

The certificate's free metadata line is the practical source for the
visibility (`visibility <v>/<D>` substring).

---

## 4. Inflation party layout and ordering

(`inf::Inflation::init_parties`, `inflation.cpp`)

An inflation party is a pair `(t, (j, k))` with `t ∈ {0,1,2}` the network
party type (A, B, C) and `(j, k)` the copy indices of the *left* and *right*
parent source, where for type `t`:

    left source type  = (t+1) mod 3,   right source type = (t+2) mod 3.

So (with sources ordered α, β, γ):

    A j k  reads  (β_j, γ_k)
    B j k  reads  (γ_j, α_k)
    C j k  reads  (α_j, β_k)

Party names are `"A"+str(j)+str(k)` etc. Total party count for size
`(z0,z1,z2)`: `z1·z2 + z2·z0 + z0·z1`.

**Party index order** (defines the layout of inflation events as outcome
tuples): build a nested chain of sizes starting at `(1,1,1)`; repeatedly copy
the last size and, scanning source types `i = 0,1,2` in order, increment
component `i` if it is below the target (appending a snapshot after *each*
increment — the same working copy keeps mutating within one sweep). For each
size step in the chain, enumerate source tuples `(s0,s1,s2)` in product order
with the **last index fastest** (`util::ProductRange`), and for each tuple
enumerate network types `t = 0,1,2`; register the party
`(t, (s_{(t+1)%3}, s_{(t+2)%3}))` the first time it appears.

For size (2,2,2) this yields exactly:

    0:A00 1:B00 2:C00 3:B01 4:C10 5:A10 6:C01 7:C11 8:A01 9:B10 10:A11 11:B11

**[verified: instrumented C++ prints this exact order]**

An inflation event `e` is a tuple of outcomes indexed by this order.
Deterministic-event enumeration order (used by the brute-force optimizer) is
again product order, last party fastest — irrelevant for the min, only for
tie-breaking of the reported argmin. **[verified: argmin matches]**

---

## 5. Symmetry groups

A symmetry is a pair `(π, σ)` of a party permutation and an outcome
permutation, acting on an event by

    (g·e)[π(i)] = σ(e[i])      (inf::Symmetry::act_on_event)

i.e. `g·e = σ ∘ e ∘ π^{-1}`.

**5a. Distribution (network) symmetries.** All pairs of the 6 permutations of
the 3 network parties (each tagged with its parity) and the `n!` outcome
permutations that leave the target tensor invariant
(`TargetDistr::init_symmetries`, `Network::get_all_sym`). SRB: all 6 party
perms × both outcome perms = **12**. **[verified: metadata says 12]**

**5b. Applicable symmetries.** A network symmetry `(π, σ)` lifts to the
inflation only if `π` leaves the size vector invariant under
`image[π(i)] = z[i]` (`Inflation::get_applicable_symmetries`). For 2×2×2 all
12 are applicable.

**5c. Lifting a network party permutation** (`network_party_to_inf_party_sym`):
party `(t,(j,k)) ↦ (π(t), (j,k))` if `π` is even, `(π(t), (k,j))` if odd
(odd permutations transpose the copy indices).

**5d. Source-induced symmetries** (`source_sym_to_party_sym`): for one
permutation `s_τ` per source type τ (all `z0!·z1!·z2!` combinations),
`(t,(j,k)) ↦ (t, (s_{(t+1)%3}(j), s_{(t+2)%3}(k)))`.

**5e. Inflation symmetry group** (`init_inflation_symmetries`): the set of
pairs `(π_src ∘ π_lift, σ)` over all applicable network syms `(π_lift, σ)`
and all source syms `π_src` (source applied after lift; either order
generates the same group). For SRB 2×2×2: 12 × 8 = **96**. **[verified]**

---

## 6. Constraint descriptions

(`inf::Constraint::pretty_description`, `constraint.cpp`;
`inf::ConstraintParser`, `constraint_parser.cpp`)

A constraint is an ordered list of party-name groups
`(M0, …, M(k-1), N)`, `N` possibly empty. Pretty form (as stored in the
file):

    q(M0 , M1 , … [, N]) = p(M0) * p(M1) * … [* q(N)]

Groups are comma-separated inflation party names; in the `q(...)` on the left
they are joined by `" , "` (space-comma-space); the trailing `, N` and the
`* q(N)` factor are omitted when `N` is empty.

Derived data:

- **LHS marginal party list** = concatenation of all groups **in the order
  listed** (M0 first, …, N last). Order matters: it defines the slot order of
  the dual-vector basis events (§8) and the RHS tensor layout (§9).
- **RHS marginal party list** = N (possibly empty).
- **Target marginal names**: each `Mi` with copy indices stripped, e.g.
  `A00,B00,C00 → (A,B,C)`, `A00 → (A)`. These must be strictly increasing in
  network-party order (asserted by `TargetDistr::compute_marginal`).

**Constraint group** Ḡ (`Constraint::get_constraint_group`): all inflation
symmetries `(π, σ)` such that `π` maps both

    A := set(LHS) \ set(RHS)   and   B := set(RHS)

onto themselves **as sets**. (For SRB 2×2×2 constraint 1: |projected marginal
symmetries| = 24; constraint 2: 8. **[verified via instrumented log]**)

---

## 7. Marginals: symmetries, reduced permutations, extraction

(`inf::Marginal`, `marginal.cpp`)

Given a marginal party list `M = [p_0, …, p_{m-1}]` (LHS or RHS list of a
constraint) and the constraint group Ḡ:

**7a. Marginal symmetries** (down-conversion, `init_marginal_symmetries`):
for each `(π, σ) ∈ Ḡ`, the slot permutation
`ρ(i) = slot index of π(p_i) within M`, giving the deduplicated set of pairs
`(ρ, σ)`. These act on marginal events by `(h·x)[ρ(i)] = σ(x[i])`.

**7b. Marginal permutations** (`init_marginal_permutations`): for each
inflation symmetry `(π, σ)` (the FULL group, not Ḡ), form the candidate

    perm = (σ, P)   with   P = [π(p_0), …, π(p_{m-1})].

`perm` is kept iff it is the minimum of its orbit under the marginal
symmetries: for every marginal symmetry `(ρ, τ)`, the transformed pair

    (σ ∘ τ^{-1},  P')   with   P'[ρ(i)] = P[i]

must not compare strictly smaller, where comparison is lexicographic on the
outcome permutation's image tuple first, then on the party list
(`Marginal::Permutation::operator<`). The retained set (deduplicated, sorted
in that same order) is the **reduced marginal permutation set**; its
cardinality is the marginal's **denominator** `den(M)`. For the empty
marginal, `den = 1` and there are no permutations. **[inferred from source;
validated indirectly through the exact score match, which depends on every
denominator]**

**7c. Event extraction** (`extract_marg_perm_event`): for a marginal
permutation `(σ, P)` and inflation event `e`,

    x[i] = σ^{-1}( e[ P[i] ] ),   i = 0..m-1.

---

## 8. Symmetrized dual-vector basis (coefficient ordering) — CRITICAL

(`inf::DualVector`, `dual_vector.cpp`; orbits from `orbitable.cpp`)

The stored coefficients of a constraint live in the quotient of the LHS
marginal event space by the marginal symmetries (§7a):

1. Enumerate all marginal events (length m, outcomes `0..n-1`) in product
   order, last slot fastest (= lexicographic ascending order of tuples).
2. Group them into orbits under the marginal symmetries; each orbit's
   representative is its lexicographically minimal element (equivalently:
   first encountered in enumeration order).
3. Order the orbits by ascending representative. The i-th orbit corresponds
   to the i-th stored coefficient. The embedded dual vector is constant on
   each orbit: `F(x) = coeff[orbit_index(x)]`.

(The C++ additionally maintains a "unknown outcome" extension for
branch-and-bound bounds — `StoreBounds` — which appends extra orbit classes
*after* all the no-unknown classes. Files only ever store the no-unknown
coefficients, so a checker can ignore the mechanism entirely.)

**[verified: instrumented C++ prints, for both SRB constraints, the orbit
representatives in exactly this order with values equal to the file
coefficients in file order — 8 classes `000000, 000001, 000011, 000111,
001001, 001010, 001011, 001110` and 14 classes for constraint 2]**

---

## 9. RHS target tensor and reduced dual vector

(`inf::Constraint::set_target_distribution`, `update_rhs_reduced_dual_vector`,
`constraint.cpp`; `TargetDistr::compute_marginal`, `target_distr.cpp`)

- Target marginal `p_{Mi}`: sum the **simplified** full tensor (§3) over the
  absent network parties; keep the same denominator; then GCD-**simplify**
  the marginal. (SRB: `p_(A) = (1,1)/2` after simplification.)
- `T := p_{M0} ⊗ … ⊗ p_{M(k-1)}`: tensor product (party order = factor order,
  each factor's own slot order preserved; numerators multiply, denominators
  multiply), then GCD-**simplify** the product
  (`EventTensor::set_to_tensor_product` calls `simplify()`).
- **Reduced RHS dual vector** over RHS marginal events `r`:

      R(r) = Σ_t  T_num(t) · F(t ⧺ r)

  where `t` ranges over all events of `T`, `⧺` is tuple concatenation, and
  the concatenation is a valid LHS marginal event because the LHS slot order
  is (M0 … M(k-1), N) (§6). If `N` is empty, the scalar
  `R = Σ_t T_num(t) · F(t)`.

**Denominators** used for scaling (`Constraint::get_lhs_denom/get_rhs_denom`):

    lhs_den(c) = |reduced LHS marginal permutations|
    rhs_den(c) = denom(T) · (|reduced RHS marginal permutations| if N ≠ ∅ else 1)

For SRB 2×2×2 at 41422/100000: constraint 1: `lhs_den = 4`,
`rhs_den = 400000² = 1.6·10^11`; constraint 2: `lhs_den = 12`,
`rhs_den = 2 · 12 = 24`. **[verified via final score match and
`QUOVEC_DENOM = 4.8·10^11 = Π denoms / gcd` printed by instrumented C++]**

---

## 10. Integer scale factors and the score

(`inf::ConstraintSet::update_constraint_scale_factors`, `constraint_set.cpp`;
evaluation in `marginal.cpp` / `constraint.cpp`)

Let `P = Π_c lhs_den(c) · rhs_den(c)` over all constraints, and

    lhs_scale(c) = P / lhs_den(c),    rhs_scale(c) = P / rhs_den(c),

all divided by `g := gcd` of all `2K` scale factors. The RHS scale enters
with a **minus sign** (`Constraint::set_rhs_scale`). The integer score of an
inflation event `e` is

    score(e) = Σ_c [ lhs_scale(c) · Σ_{(σ,P) ∈ RedPerms(LHS_c)} F_c(extract(e; σ,P))
                   − rhs_scale(c) · ( R_c  if N_c = ∅
                                      else Σ_{(σ,P) ∈ RedPerms(RHS_c)} R_c(extract(e; σ,P)) ) ]

This equals `(P/g) ·` the natural rational score
`Σ_c [ ⟨F_c⟩_lhs / lhs_den(c) − ⟨R_c⟩_rhs / rhs_den(c) ]`, so the *verdict*
(sign of the minimum) is scale-independent; the integer form is what the C++
computes and prints.

**Checking predicate**: minimize `score(e)` over all `n^{|parties|}` events;
the certificate is valid iff the minimum is strictly `> 0`. Exact rational
minimum = `min_int · g / P`.

---

## 11. What the checker must reject

- version ≠ 5; malformed sign characters; wrong section literals.
- Constraint description repeated in DUAL VECTOR section differing from the
  CONSTRAINT SET section.
- Coefficient count ≠ number of symmetrized basis classes (§8).
- Metadata symmetry counts (when present) differing from the reconstructed
  group sizes (§5).
- Non-strictly-increasing target-marginal party names (§6).

(The C++ additionally checks d-separation and injectability of the groups —
guaranteeing the constraint is a *sound* relaxation. An independent checker
that wants to certify the physics claim, not merely LP infeasibility, should
also verify: all groups pairwise share no parent source copies
(d-separation: party `(t,(j,k))` has parents `((t+1)%3, j)` and
`((t+2)%3, k)`), and each `Mi` maps into `{A00, B00, C00}` under some
source-permutation symmetry (injectability). `check_certificate.py` currently
trusts the constraint set on this point — the SRB set was verified by
inspection: both constraints are standard LPI constraints.)

---

## 12. Validation ledger (SRB 2×2×2, visibility 41422/100000)

Ground truth was produced by temporarily instrumenting the C++ (`user::srb`
placeholder app replaced by a certificate-reading brute-force check;
`make release`, `./release_inf srb`), then reverted. Agreement of the
independent Python implementation:

| Quantity | C++ (instrumented) | Python checker | Match |
|---|---|---|---|
| Party index order | A00 B00 C00 B01 C10 A10 C01 C11 A01 B10 A11 B11 | same | ✓ |
| Distribution / inflation syms | 12 / 96 | 12 / 96 | ✓ |
| Basis classes (c1, c2) | 8, 14 | 8, 14 | ✓ |
| Orbit representatives + coefficient assignment | printed list | identical | ✓ |
| Marginal-symmetry cardinalities (c1, c2) | 24, 8 | 24, 8 | ✓ |
| `QUOVEC_DENOM` = P/g | 4.8·10^11 | 4.8·10^11 | ✓ |
| score(all-zero event) | 1376080207962 | 1376080207962 | ✓ |
| min over 4096 events | 1016080207962 | 1016080207962 | ✓ |
| argmin event | 000011010111 | 000011010111 | ✓ |
| Σ scores over all events | 1035951257759883264 (int64-overflowed) | 333077344584531812352 ≡ same mod 2^64 | ✓ (checker exact) |
| Verdict | nonlocal | VALID (min > 0) | ✓ |
| Sensitivity: verdict vs visibility | nonlocal ⇔ v ≥ 41422 (asserted by `srb_dual_vector_io`) | flips exactly at 41422 (tested 41412–41432) | ✓ |

Exact minimum: **169346701327 / 80000000000** (≈ 2.1168).

**Conventions verified directly**: file grammar; party ordering; basis
ordering and coefficient assignment; symmetry group sizes; final scores.
**Conventions inferred from source and validated only end-to-end** (through
the exact score): the marginal-permutation representative rule (§7b) and the
per-constraint denominators (§9) — an error in either would change the
integer score, so the end-to-end match is strong but not itemized evidence.
**Not validated** (out of scope for the SRB case): the `StoreBounds` unknown-
outcome orbit extension; behavior for >2-outcome / non-(A,B,C)-symmetric
targets; d-separation/injectability re-verification (§11).
