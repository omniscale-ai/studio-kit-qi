# Example pack: quantum information theory

The kit's original domain, kept as an example pack. ID system prefix: `qi`.

| Chain | Files |
|-------|-------|
| Certificate layer — Elegant Joint Measurement nonlocality (Gitton–Renner, arXiv:2510.15143) | `CLAIM/example-ejm.md` → `CERTIFICATE/example-ejm.md` → `CHECK-RUN/example-ejm-macos.md` (hand-assembled bootstrap record; environment diversity). `CHECK-RUN/example-srb-222-linux-py.md`: the SRB 2×2×2 certificate checked by the kit's own clean-room checker (`scripts/checkers/fast_inflation.py`, Linux/x86_64) — implementation diversity. It demonstrates the checker on a real certificate; the SRB CLAIM and CERTIFICATE artifacts are not in this pack, so it certifies nothing in the pack's claim graph. The earlier macOS/arm64 run of the same checker is kept verbatim in `records/` (see its README) |
| Verification intake | `VERIFICATION-PLAN/example-ejm-plan.md` |
| Theorem layer — bipartite bound information (Pauwels–Gisin–Renner) | `THEOREM/example-pgr.md` → `PROOF-MAP/example-pgr.md` → `LEMMA/example-pgr-*.md` (7 nodes) |
| Discovery layer — CHSH deterministic bounds | `RESEARCH-PLAN/example-chsh.md`; `CONJECTURE/example-chsh-det-bound.md` (proved), `example-bell-pm-coeff-values.md` (refuted), `example-bell-odd-sign-values.md` (supported); `PROOF-ATTEMPT/*.md` (script-generated, with `.build.log`); `lean-chsh/` (core Lean project: `Chsh.lean` proofs, `Stubs.lean` statement stubs, `Instances.lean` instance agreement); `chsh-enumerate.py` (exploration record) |

```bash
python3 scripts/graph_gate.py examples/qi                      # semantic gate, expect PASS
python3 examples/qi/chsh-enumerate.py                          # the exploration record
( cd examples/qi/lean-chsh && lake build && lake env lean Instances.lean )   # instance agreement
python3 scripts/attest_lean.py --project examples/qi/lean-chsh --file Chsh.lean --decl Chsh.chsh_det_le_two \
    --conjecture examples/qi/CONJECTURE/example-chsh-det-bound.md --slug chsh-det-bound-lean --out /tmp/attempt.md
```

The certificate re-check (`scripts/checkers/fast_inflation.py` on the real SRB certificate) is in `USAGE.md` §3.
