# CHECK-RUN — Generation & Validation Rules

**Dependencies**:
- `{principles}` — cross-cutting invariants P1–P13; load before these rules
- `{check_run_template}` — structural reference

---

1. **Script-generated only.** CHECK-RUN artifacts are written by checker scripts (one per certificate format under `scripts/checkers/`, see its README for the contract), never by hand and never by an LLM narrating what it believes happened. The `generated-by` frontmatter field and the `Attestation` section are mandatory.
2. **Verdict vocabulary is closed:** `pass` (predicate verified), `fail` (predicate violated — the certificate does not witness the claim), `error` (check did not complete — an outage is never a verdict). No other values. `fail` and `error` records are kept, not deleted.
3. **Hashes observed, not copied.** The run records the SHA-256 it computed from the actual input files. Hash mismatch with the CERTIFICATE ⇒ verdict `error` with the mismatch stated.
4. **One certificate, one environment, one record.** Re-runs in new environments are new CHECK-RUN artifacts; diversity across records is the point (different OS/arch/compiler/checker each strengthen the chain differently — say which axis a run adds).
5. **Reproducibility.** The `Command` section must be sufficient for a third party with the referenced inputs to reproduce the run bit-for-bit (modulo timing).
6. **Independence disclosure.** The `Checker` section MUST state honestly whether the checker shares code with the certificate producer. A same-codebase run is evidence; an independent-implementation run is much stronger evidence; say which one this is.

## Where the principles land in a CHECK-RUN

| Section | Principles |
|---------|------------|
| frontmatter, Result | P8 verdict written by the script from a closed vocabulary; the agent never writes `pass` |
| Certificate | P1 hashes observed, not copied |
| Checker | P11 independence relation disclosed; trust by check, not by producer |
| Environment, Command | P8 reproducible bit-for-bit; the diversity axis this run adds is named |
| Attestation | P8 what produced the record and where the raw log lives |
