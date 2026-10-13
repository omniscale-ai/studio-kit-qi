---
status: checked
date: 2026-08-10
---

# Farkas certificate: EJM incompatible with the 2×2×4 inflation LP


<!-- toc -->

- [Certified Claim](#certified-claim)
- [Certificate File](#certificate-file)
- [Semantics](#semantics)
- [Auxiliary Inputs](#auxiliary-inputs)
- [Provenance](#provenance)
- [Check Runs](#check-runs)

<!-- /toc -->

**ID**: `cpt-qi-cert-ejm-224-farkas`
## Certified Claim

`cpt-qi-claim-ejm-triangle-nonlocal` — non-3-locality of the EJM distribution (via inflation soundness: LP infeasibility at any inflation level implies non-membership in the 3-local set).

## Certificate File

- **Path/URL**: `data/ejm_224_nl_certificate.txt` in [github.com/vgitton/fast-inflation](https://github.com/vgitton/fast-inflation) @ commit `01fcd357ee715dcff721f6a5381aedd2985c5696`
- **Size**: 75,525 bytes (5,792 lines)
- **SHA-256**: `35c0221dea06ba6daf3f8d9a8e01914bc87eaabc8307491fe927173f9a94b20e`
- **Format**: text; METADATA line (network, outcomes, inflation size, symmetry counts) → CONSTRAINT SET (two LPI factorization constraints on marginals of the inflation distribution q, in the authors' party-labeling notation) → DUAL VECTOR: per constraint, a length-prefixed list of signed hexadecimal integer coefficients over the symmetrized marginal basis.

## Semantics

The certificate is a **Farkas separating hyperplane** for a polytope membership LP. Setting: the 2×2×4 inflation of the triangle network (2, 2, 4 copies of sources α, β, γ; 20 parties; 4 outcomes each). Any 3-local model for p_EJM induces a distribution q over inflation events satisfying: (i) symmetry under the 4,608 source-induced inflation symmetries, and (ii) the two LPI marginal factorization constraints listed in the file. The feasible q's form a polytope whose vertices are the images (under the constraint map) of the 244,517,713 symmetrized deterministic inflation events.

**Checking predicate (all in exact rational arithmetic):**

min over all 244,517,713 symmetrized inflation events e of ⟨d, Φ(e)⟩ > 0,

where d is the dual vector from the file and Φ maps a deterministic event to its constraint-space image (marginal factorization residuals against the exact p_EJM values 25/256, 1/256, 5/256). A strictly positive minimum means the hyperplane separates the target from every polytope vertex, hence from the polytope; therefore no feasible q exists; therefore (inflation soundness) p_EJM is not 3-local.

## Auxiliary Inputs

- `data/symtree_EJM_224.txt` — the symmetrized event tree (enumeration of the 244,517,713 orbit representatives), 15,683,446 bytes, SHA-256 `083183360f57c491162998b326453e00c65901ef53bc47276eafff7b6de5fb85`. **Trust status: trusted** (produced by the same codebase; re-derivable in principle from the inflation symmetry group — independent re-derivation is the known weakest link and a target for the independent checker).

## Provenance

Found by `fast-inflation` (Gitton–Renner): fully-corrective Frank–Wolfe over the symmetrized polytope with Mosek as the quadratic-subproblem solver; search time ≈ 1 week (per `user::ejm_find_nl_certificate` docs). Informational only — validity rests entirely on the checking predicate above.

## Check Runs

- `cpt-qi-run-ejm-224-macos-arm64-20260810` — pass (macOS/arm64, Mosek-free build, 21 s).
- Authors' original checks on Linux/x86-64 (reported in arXiv:2510.15143) — not recorded as kit artifacts.
