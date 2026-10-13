# Checkers

One script per certificate format. A checker is a computational gate: it reads a CERTIFICATE's
external file(s), evaluates the checking predicate in exact arithmetic, and **generates** the
CHECK-RUN artifact. Nobody writes a CHECK-RUN by hand (CHECK-RUN rules, rule 1; principle P8).

| Checker | Format | Spec | Status |
|---------|--------|------|--------|
| `fast_inflation.py` | fast-inflation nonlocality certificates (Gitton–Renner), text format v5 | `FAST-INFLATION-SEMANTICS.md` | SRB 2×2×2 verified; EJM 2×2×4 needs the symtree enumerator (extension point marked) |

## Contract

A checker `scripts/checkers/<format>.py`:

1. **Takes** the certificate file (and any auxiliary inputs the CERTIFICATE lists), plus
   `--check-run OUT.md`, `--system <id-system>`, `--cert-id <CERTIFICATE id>`, `--run-slug <slug>`.
2. **Observes hashes**: computes the SHA-256 of every input it reads and writes them into the
   Certificate section; it never copies a declared hash.
3. **Evaluates exactly**: integers, `fractions.Fraction`, or another exact representation. No
   floating point on the path from input to verdict.
4. **Emits** the CHECK-RUN with the template's sections (Certificate, Checker, Environment, Command,
   Result, Attestation), frontmatter `status: pass | fail | error`, `generated-by: <script> <version>`,
   a `description:` line, and the ID `cpt-<system>-run-<slug>`. The Checker section states the
   independence relation to the certificate producer honestly (same codebase / independent
   implementation / formally verified). The Command section is the exact invocation.
5. **Verdict vocabulary**: `pass` (predicate verified), `fail` (predicate violated), `error` (the
   check did not complete — an outage is never a verdict). Exit code 0 / 1 / 2 respectively.
6. **Ships a semantics document** next to it, precise enough for a clean-room third implementation.

A certificate format without a checker is not checkable: write the checker from the CERTIFICATE's
Semantics section first, then run it. Trust never lives in the search (P11) — two certificates that
pass the same checker are equally trusted whoever found them.
