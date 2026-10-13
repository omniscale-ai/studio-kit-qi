# Example pack: number theory (Euler's polynomial)

The domain-neutral worked example: no physics, core Lean only, builds in under a second. ID system prefix: `nt`.

Euler's polynomial f(n) = n² + n + 41 is prime for n = 0, …, 39 and composite at n = 40 (1681 = 41²). The pack runs that story through the discovery layer:

| Artifact | Status | How |
|----------|--------|-----|
| `RESEARCH-PLAN/example-euler.md` | approved | question, concordance (incl. a project-defined primality test), cost, budget, policy, register, frozen criteria |
| `CONJECTURE/example-euler-all-prime.md` | **refuted** | origin: pattern in exploration; witness n = 40; `PROOF-ATTEMPT/example-euler-all-prime-refute.md` (`attest_lean.py --refutes`) |
| `CONJECTURE/example-euler-prime-below-40.md` | **proved** | origin: restriction; `PROOF-ATTEMPT/example-euler-prime-below-40-lean.md` (`decide` over 40 cases) |
| `CONJECTURE/example-euler-no-small-prime-factor.md` | **supported** | origin: gap in the refuting attempt's handoff; exact enumeration n < 10⁵; no attempt |

Every CONJECTURE carries a Faithfulness Cross-Check (P13): a second agent instance, shown only `Euler.lean` and the concordance, back-translated each Lean block and — because primality is project-defined here — traced `isPrime` and confirmed it decides primality correctly; `lean-euler/Instances.lean` reproduces `enumerate.py` line by line.

```bash
python3 scripts/graph_gate.py examples/euler-polynomial          # expect PASS
python3 examples/euler-polynomial/enumerate.py                   # the exploration record
( cd examples/euler-polynomial/lean-euler && lake build && lake env lean Instances.lean )
python3 scripts/attest_lean.py --project examples/euler-polynomial/lean-euler --file Euler.lean \
    --decl Euler.not_all_prime --refutes \
    --conjecture examples/euler-polynomial/CONJECTURE/example-euler-all-prime.md \
    --slug euler-all-prime-refute --out /tmp/attempt.md            # expect STATUS: REFUTED
```
