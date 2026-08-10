# Constructor Studio QI Kit

A [Constructor Studio](https://github.com/constructorfabric/studio) kit for **machine-checkable impossibility claims in quantum information theory**.

The kit packages an artifact pipeline for claims of the form *"no classical model of kind X reproduces object Y"* — network nonlocality, bound information, key-rate bounds — where the proof is an **exact rational certificate** (Farkas vector, SOS decomposition) found by heavy computation but checkable cheaply and deterministically.

```
find (SDP / Frank–Wolfe / LLM, days)  ≫  check (exact arithmetic, seconds)
```

Trust never lives in the search. Only the certificate and its checker need to be believed — so the kit makes certificates and check-runs first-class, traceable, gated artifacts.

## Artifact pipeline

```
CLAIM ──▶ CERTIFICATE ──▶ CHECK-RUN            (certificate layer, self-contained)
  ▲
THEOREM ──▶ PROOF-MAP ──▶ LEMMA                (theorem layer, planned — Step 3)
```

- **CLAIM** — a precise impossibility statement about a finite probabilistic model, with exact rational data.
- **CERTIFICATE** — the witness: file reference + SHA-256 + mathematical semantics + provenance. Never inlined, never trusted by origin.
- **CHECK-RUN** — a record of one verification of one certificate in one environment. **Script-generated, never hand-written.** Trust grows with environment diversity across runs.

The certificate layer works bare (no theorem needed). The theorem layer (claim graph with statuses `formalized / machine-checked / expert-verified / cited / open`) references down into it.

## Gates (three layers)

1. `constraints.toml` — structure and traceability via `cfs validate`: required sections, ID grammar (`cpt-{system}-{claim|cert|run}-{slug}`), every CLAIM referenced by a CERTIFICATE, every CERTIFICATE by a CHECK-RUN.
2. `scripts/` — the computational gates: independent exact-arithmetic checkers that *generate* CHECK-RUN artifacts.
3. `workflows/` — agent orchestration with hard rules (a status may never be claimed without its artifact).

## Canonical example

The **Elegant Joint Measurement** distribution in the triangle network (Gisin 2019, conjecture; Gitton–Renner 2025, proof — [arXiv:2510.15143](https://arxiv.org/abs/2510.15143)): non-3-locality certified by a 2×2×4-inflation Farkas certificate, reproduced independently on macOS/arm64 without the commercial LP solver. See `artifacts/*/examples/`.

## Status

- [x] Step 1 — kit skeleton, certificate-layer artifact types, EJM canonical example
- [ ] Step 2 — independent exact checker (`scripts/check_certificate.py`)
- [ ] Step 3 — theorem layer (THEOREM / PROOF-MAP / LEMMA) + PGR bound-information example
- [ ] Step 4 — workflows (verify-certificate, decompose-proof, hunt-counterexample, audit-references)
- [ ] Step 5 — CI hook re-running computational gates
- [ ] Step 6 — pilot integration

## Usage

See [USAGE.md](USAGE.md) — standalone quickstart (no Studio needed): tour the examples, run the semantic gate, re-verify a real nonlocality certificate in 30 seconds.

## Install

```bash
cfs kit install <owner>/studio-kit-qi
```

## License

Apache 2.0.
