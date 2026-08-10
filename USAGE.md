# Using the QI Kit locally

No Constructor Studio installation is required for the standalone workflow — just `python3` (3.9+, stdlib only) and `git`.

## 0. Get the kit

```bash
git clone <this-repo> studio-kit-qi && cd studio-kit-qi
```

## 1. Tour the artifact chain (5 minutes, read-only)

Two complete worked examples ship with the kit:

**Certificate layer (EJM):** read in this order —

```
artifacts/CLAIM/examples/example-ejm.md            # the impossibility statement + exact data
artifacts/CERTIFICATE/examples/example-ejm.md      # the witness: file, SHA-256, checking predicate
artifacts/CHECK-RUN/examples/example-ejm-macos.md  # one verification in one environment
```

**Theorem layer (PGR bound information):**

```
artifacts/THEOREM/examples/example-pgr.md          # statement + trust summary (weakest link named)
artifacts/PROOF-MAP/examples/example-pgr.md        # the 7-node lemma DAG with statuses
artifacts/LEMMA/examples/example-pgr-*.md          # per-node statement + verification route
```

Every artifact kind has `template.md` (structure), `rules.md` (hard rules), `checklist.md` (review questions) next to the examples.

## 2. Run the semantic gate

```bash
python3 scripts/graph_gate.py artifacts
```

Expected: `graph_gate: 12 artifacts scanned` … `PASS`. The gate enforces what static validation can't: theorem statuses are computed not asserted (G1), lemma statuses never exceed their artifacts (G2), every load-bearing node resolves (G3), `certified` claims have passing runs (G4). Try breaking it: edit `artifacts/THEOREM/examples/example-pgr.md` frontmatter to `status: verified` and re-run — G1 fails with the exact offending nodes.

## 3. Re-verify a real nonlocality certificate (30 seconds)

Fetch the certificate data (sparse clone, ~20 MB):

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/vgitton/fast-inflation fi
git -C fi sparse-checkout set data
```

Verify integrity against the declared hash, then run the independent checker:

```bash
echo "6db0eb30dffb77b5603cde96efd9ad5ffac93ac0032946a7a94b81e527fa72d4  fi/data/srb_222_certificate.txt" | shasum -a 256 -c -
python3 scripts/check_certificate.py fi/data/srb_222_certificate.txt \
    --repo fi --target srb --check-run my-first-checkrun.md
```

Expected output ends with:

```
min score (exact): 169346701327/80000000000
VERDICT          : VALID — min score > 0: the inflation LP is infeasible;
                   the target distribution is NOT triangle-local at this visibility.
```

You have just re-proven, on your machine, in exact arithmetic, with an implementation that shares zero code with the original, that the shared-random-bit distribution at visibility 41.422% is nonlocal in the triangle network — and `my-first-checkrun.md` is the CHECK-RUN artifact recording it. That file is the unit of trust in this kit: script-generated, hash-anchored, environment-stamped.

What the checker does is specified in `scripts/CERTIFICATE-SEMANTICS.md` — precisely enough that you could write a third implementation from it alone.

(The EJM 2×2×4 certificate needs the symtree-based event enumerator — the marked extension point in `check_certificate.py`; today it is checked via the ported original code, see the EJM CHECK-RUN example.)

## 4. Author your own claim graph

1. Copy templates from `artifacts/*/template.md`; follow the matching `workflows/*.md` (they are agent-facing but human-readable):
   - new impossibility result → `workflows/decompose-proof.md` (THEOREM → PROOF-MAP → LEMMAs, statuses start `open`/`cited`)
   - got a certificate → `workflows/verify-certificate.md` (hash first, check, script-generated CHECK-RUN, then statuses)
   - searching for examples → `workflows/hunt-counterexample.md` (floats screen, only exact arithmetic asserts)
   - citations → `workflows/audit-references.md`
2. Gate before every commit: `python3 scripts/graph_gate.py <your-artifacts-root>`.
3. CI (`.github/workflows/gates.yml`) re-runs both gates on push.

## 5. With Constructor Studio (optional)

The kit follows the SDLC-kit layout (`manifest.toml` schema v1.0, `constraints.toml` for `cfs validate`):

```bash
cfs kit install <owner>/studio-kit-qi
cfs validate .
```

`cfs validate` adds the static layer: required sections per artifact kind, ID grammar (`cpt-{system}-{claim|cert|run|thm|pm|lem}-{slug}`), and the reference chain (every CLAIM must be referenced by a CERTIFICATE, every CERTIFICATE by a CHECK-RUN). *Note: installation against a live Studio instance is not yet exercised — file an issue if the manifest schema drifts.*
