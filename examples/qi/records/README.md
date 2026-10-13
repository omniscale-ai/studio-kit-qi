# Records

Raw run records kept verbatim for provenance. They are **not** registered artifacts (no `cfs validate`,
no `graph_gate`): a script-generated record is never edited by hand, and these were produced before the
checker learned the `--system` flag, so their IDs carry the old hard-coded `fastinflation` prefix.

- `checkrun-srb-222-macos-20260810.md` — the first run of the kit's clean-room checker (then
  `scripts/check_certificate.py` v1.0) on the SRB 2×2×2 certificate, macOS/arm64, Python 3.14. The
  registered CHECK-RUN example for the same certificate is `../CHECK-RUN/example-srb-222-linux-py.md`
  (same checker, now `scripts/checkers/fast_inflation.py` v1.1, Linux/x86_64); together they give the
  certificate environment diversity across OS, architecture and Python version.
