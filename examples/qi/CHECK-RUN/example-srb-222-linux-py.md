---
description: SRB 2x2x2 certificate checked by the kit's independent exact checker on Linux — verdict pass.
status: pass
date: 2026-10-13
generated-by: fast_inflation.py v1.1 (--check-run)
---

# SRB 2x2x2 certificate, independent Python checker

**ID**: `cpt-qi-run-srb-222-linux-py`

## Certificate

- **File checked**: fi/data/srb_222_certificate.txt
- **SHA-256 observed**: `6db0eb30dffb77b5603cde96efd9ad5ffac93ac0032946a7a94b81e527fa72d4`
- **Auxiliary inputs observed**: none (target distribution SRB with visibility
  41422/100000 is reconstructed from the built-in registry + certificate metadata)

## Checker

`scripts/checkers/fast_inflation.py` v1.1 — clean-room independent implementation
(Python 3, exact integer/`fractions.Fraction` arithmetic). Shares no code with
the certificate producer `fast-inflation` (C++); conventions documented in
`scripts/checkers/FAST-INFLATION-SEMANTICS.md`.

## Environment

- OS: Linux 7.0.0-34-generic (x86_64)
- Python: 3.10.15
- Exact arithmetic: Python built-in int + fractions.Fraction (stdlib)

## Command

```
python3 scripts/checkers/fast_inflation.py fi/data/srb_222_certificate.txt --repo fi --target srb --system qi --run-slug srb-222-linux-py --check-run examples/qi/CHECK-RUN/example-srb-222-linux-py.md
```

## Result

- **Verdict**: pass — min event score is strictly positive, so the inflation LP is infeasible: the target distribution is triangle-nonlocal
- **Wall time**: 0.07 s
- **Peak memory**: 17.2 MB (ru_maxrss)
- Events enumerated (raw, no symmetrization): 4096
- Exact minimum score: 169346701327/80000000000 = 2.1168337665875 (integer-scaled: 1016080207962, common scale 184320000000000/384)
- Minimizing inflation event: 000011010111
- Constraint basis sizes: 8, 14

## Attestation

Record emitted by fast_inflation.py v1.1 --check-run at run time; the values
above are the script's own outputs (stdout log of the same run).
