---
status: pass
date: 2026-08-10
generated-by: check_certificate.py v1.0 (--check-run)
---

# SRB 2x2x2 certificate, independent Python checker

**ID**: `cpt-fastinflation-run-srb-222-py`

## Certificate

- **File checked**: /private/tmp/claude-501/-Users-anaderi-Obsidian-iCloud-vault/32d99617-9c73-4659-bd7b-587d6ab3eb5e/scratchpad/fast-inflation/data/srb_222_certificate.txt
- **SHA-256 observed**: `6db0eb30dffb77b5603cde96efd9ad5ffac93ac0032946a7a94b81e527fa72d4`
- **Auxiliary inputs observed**: none (target distribution SRB with visibility
  41422/100000 is reconstructed from the built-in registry + certificate metadata)

## Checker

`scripts/check_certificate.py` v1.0 — clean-room independent implementation
(Python 3, exact integer/`fractions.Fraction` arithmetic). Shares no code with
the certificate producer `fast-inflation` (C++); conventions documented in
`scripts/CERTIFICATE-SEMANTICS.md`.

## Environment

- OS: Darwin 25.5.0 (arm64)
- Python: 3.14.5
- Exact arithmetic: Python built-in int + fractions.Fraction (stdlib)

## Command

```
python3 scripts/check_certificate.py /private/tmp/claude-501/-Users-anaderi-Obsidian-iCloud-vault/32d99617-9c73-4659-bd7b-587d6ab3eb5e/scratchpad/fast-inflation/data/srb_222_certificate.txt --target srb --check-run scripts/checkrun-srb-222.md
```

## Result

- **Verdict**: pass — min event score is strictly positive, so the inflation LP is infeasible: the target distribution is triangle-nonlocal
- **Wall time**: 0.04 s
- **Peak memory**: 24.6 MB (ru_maxrss)
- Events enumerated (raw, no symmetrization): 4096
- Exact minimum score: 169346701327/80000000000 = 2.1168337665875 (integer-scaled: 1016080207962, common scale 184320000000000/384)
- Minimizing inflation event: 000011010111
- Constraint basis sizes: 8, 14

## Attestation

Record emitted by check_certificate.py --check-run at run time; the values
above are the script's own outputs (stdout log of the same run).
