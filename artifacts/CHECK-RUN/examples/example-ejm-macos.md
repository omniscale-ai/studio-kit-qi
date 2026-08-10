---
status: pass
date: 2026-08-10
generated-by: manual-bootstrap (kit Step 1; script generation arrives with scripts/check_certificate.py in Step 2)
---

# EJM 2×2×4 certificate check — macOS/arm64, Mosek-free build


<!-- toc -->

- [Certificate](#certificate)
- [Checker](#checker)
- [Environment](#environment)
- [Command](#command)
- [Result](#result)
- [Attestation](#attestation)

<!-- /toc -->

**ID**: `cpt-qi-run-ejm-224-macos-arm64-20260810`
## Certificate

`cpt-qi-cert-ejm-224-farkas`

- **File checked**: `data/ejm_224_nl_certificate.txt`
- **SHA-256 observed**: `35c0221dea06ba6daf3f8d9a8e01914bc87eaabc8307491fe927173f9a94b20e` (= declared)
- **Auxiliary inputs observed**: `data/symtree_EJM_224.txt`: `083183360f57c491162998b326453e00c65901ef53bc47276eafff7b6de5fb85` (= declared)

## Checker

`fast-inflation` application `ejm_check_nl_certificate`, upstream commit `01fcd357ee715dcff721f6a5381aedd2985c5696` + macOS port patch (7 mechanical fixes; SHA of patch file `fast-inflation-macos-port.patch` in project attachments). **Independence relation: same codebase as producer** — this run adds *environment* diversity (OS, arch, compiler, stdlib, solver removed), not implementation diversity. Implementation diversity is Step 2.

## Environment

- macOS (Darwin 25.5.0), **arm64** (Apple Silicon)
- Apple clang 21.0.0, **libc++** (authors built with GCC/libstdc++ on Linux/x86-64)
- GMP 6.3.0 (Homebrew) — exact rational arithmetic
- **Mosek: absent** — Frank–Wolfe solver stubbed out at compile time; the check path never invokes it (`fw: 0ms` in log)

## Command

```
make release -j8   # with macOS port patch applied
/usr/bin/time -l ./release_inf ejm_check_nl_certificate --verb 2
```

## Result

- **Verdict**: **pass** — checker reports `inf::FeasProblem::Status::nonlocal`: the minimum inner product over all 244,517,713 symmetrized inflation events is strictly positive; the Farkas hyperplane separates. Combined with inflation soundness this witnesses `cpt-qi-claim-ejm-triangle-nonlocal`.
- **Wall time**: 21.17 s (optimizer/enumeration step: 8.194 s; single thread)
- **Peak memory**: 2,046,214,144 bytes maximum resident set (~2.0 GB)
- Symmetrized event tree: 244,517,713 leaves / 351,731,012 nodes, as declared in symtree metadata

## Attestation

Produced during the 2026-08-10 reproduction session (Constructor-Fabric project); raw log preserved in the session task output and summarized in the project note "EJM Certificate Reproduction — Slides". This record was hand-assembled from the raw log as a Step-1 bootstrap; rule 1 of CHECK-RUN/rules.md (script-generated only) becomes enforceable when `scripts/check_certificate.py` lands in Step 2 and regenerates this record.
