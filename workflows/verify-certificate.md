---
description: Invoke when the user asks to verify/check a nonlocality or impossibility certificate — e.g. "verify this certificate", "check the EJM certificate", "re-run the certificate check". Runs the kit checker and records a CHECK-RUN artifact.
---

# Workflow: verify-certificate

## Inputs

- A CERTIFICATE artifact (or a path to a certificate file plus enough context to draft one).

## Steps

1. **Resolve the CERTIFICATE artifact.** If only a raw file is given, first create the CERTIFICATE artifact from `artifacts/CERTIFICATE/template.md` — the Semantics section must be complete before any run (rules.md rule 2).
2. **Recompute hashes.** `shasum -a 256` on the certificate file and every auxiliary input. Compare against the artifact's declared hashes. Mismatch → stop; record a CHECK-RUN with verdict `error` stating the mismatch. **NEVER proceed on a hash mismatch.**
3. **Run the checker.** `python3 {scripts}/check_certificate.py <certificate-file> ...` (see script `--help`). Capture the full log.
4. **Record the CHECK-RUN.** The script emits the CHECK-RUN artifact; place it under the project's CHECK-RUN directory. **NEVER write a CHECK-RUN by hand and NEVER edit the verdict, timings, or hashes the script produced.**
5. **Update references.** Add the new run ID to the CERTIFICATE's Check Runs section (most recent first). If this is the certificate's first passing run, update its frontmatter `status: checked`; if the certified CLAIM was `open`, set `status: certified`.
6. **Gate.** Run `python3 {scripts}/graph_gate.py <artifacts-root>` — must PASS before committing.

## Hard rules

- An outage, crash, or missing input is verdict `error`, never `fail` and never silence.
- Verdict `fail` (predicate actually violated) is a significant event: keep the record, alert the user, do NOT delete or retry-until-green.
- State explicitly which diversity axis this run adds (new OS/arch/compiler/checker) relative to existing runs.
