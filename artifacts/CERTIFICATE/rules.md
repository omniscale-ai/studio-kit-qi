# CERTIFICATE — Generation & Validation Rules

1. **Never inline, always hash.** The certificate lives as an external file; this artifact carries its SHA-256. Any check-run MUST record the hash it actually observed; a mismatch invalidates the run, not the certificate.
2. **Semantics must be self-sufficient.** The `Semantics` section MUST specify the checking predicate precisely enough that a clean-room implementation is possible from this artifact alone (plus cited definitions). If understanding the check requires reading the producer's source code, the artifact is incomplete.
3. **Auxiliary inputs are part of the trust surface.** Every extra file the check reads (event enumerations, constraint tables) MUST be listed with a hash and an explicit trust status: `verified` (independently checked), `re-derivable` (procedure stated), or `trusted` (weak point — say so).
4. **Exact arithmetic only.** The certificate data and the checking predicate MUST be over exact rationals/integers. A certificate whose validity depends on floating-point tolerance is a different (weaker) artifact kind — do not use CERTIFICATE for it.
5. **Provenance is informational.** Nothing in the trust chain may depend on how the certificate was found. A certificate from an untrusted LLM and one from a week of Frank–Wolfe are equally good iff they pass the same checks.
6. **One claim per certificate.** Composite witnesses split into multiple CERTIFICATE artifacts.
