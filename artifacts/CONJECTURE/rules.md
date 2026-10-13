# CONJECTURE Rules

**Dependencies**:
- `{principles}` — cross-cutting invariants P1–P13; load before these rules
- `{conjecture_template}` — structural reference

---

1. **Status is derived, not asserted.** `proved` requires a PROOF-ATTEMPT with status `pass` or a CLAIM with status `certified` named in the Proved by line; `refuted` requires an attempt with status `refuted` or a certified counterexample CLAIM in the Refuted by line; `supported` requires at least one exact row in Evidence; `withdrawn` requires a person, date and reason (G6 checks the line is filled and dated). Every conjecture references the RESEARCH-PLAN it belongs to. Enforced by `graph_gate` G6.
2. **The formal statement is compiled, not typed.** The Lean block is the `#check` output of a stub compiled in the plan's pinned toolchain, with the stub's file and commit named. A hand-typed signature that no compiler saw is not a formal statement.
3. **Faithfulness is cross-checked, never self-declared.** The author of the Lean block does not confirm it alone. The Faithfulness Cross-Check records (a) an *independent reading* — a named human or a second agent instance, shown the block, its definitions and the concordance but not the Statement, back-translates it into prose, and the two are compared element by element (quantified objects, hypotheses, conclusion, encoding, what is not claimed) — and (b) *instance agreement* — the Lean definitions evaluated on the Evidence instances reproduce the exploration record. Every discrepancy is written down with its resolution; a changed block recompiles the stub and restarts the check. Only then is `Confirmed faithful by` written, with a person and a date. It is the only judged row of an attempt's verdict; `attest_lean.py` checks the section is complete and `graph_gate` G6 fails a conjecture with attempts, or `proved` / `refuted`, without it.
4. **One origin, with IDs.** Exactly one row of the plan's Conjecture Policy, naming the artifact or record it derives from. A conjecture with no origin is not registered.
5. **Instances before attempts.** Evidence records the region, the method and where the check lives before the first attempt. `none` is allowed only while the status is `open`; an attempt on such a conjecture is a deviation with a reason in that attempt. Numerical evidence alone never moves a conjecture to `supported`.
6. **Strongest supported, no stronger.** The claimed scope equals the checked region; the hypotheses are the ones the evidence needs. A wider or weaker-hypothesis statement is a separate CONJECTURE with its own evidence and an origin pointing here.
7. **Refuted stays refuted.** A refuted conjecture is not re-proposed in the same or a renamed form. A restricted statement is a new CONJECTURE whose Origin is `restriction of <this ID>` and whose hypotheses exclude the counterexample, named in Relations.
8. **Attempts are listed, most recent first, with their status.** A conjecture at the plan's attempt limit says so and is not retried under that plan.
9. **Finite objects go through the certificate layer.** A conjecture about one finite object with exact data whose natural route is tier A is written as a CLAIM; this artifact then names the CLAIM in its Formal Statement and in Proved by or Refuted by, and inherits `proved` or `refuted` from `certified`.
10. **Promotion is by source.** A proved conjecture becomes a THEOREM only once it has a citable write-up (preprint or paper) — THEOREM artifacts track sources. Until then the CONJECTURE plus its passing attempt is the record. A proved conjecture that a proof map needs becomes a LEMMA with status `formalized` referencing the attempt.

## Where the principles land in a CONJECTURE

| Section | Principles |
|---------|------------|
| Statement | P6 scope equals the checked region |
| Formal Statement | P2 every symbol resolves to the concordance; compiled, not typed |
| Faithfulness Cross-Check | P13 independent reading and instance agreement before any attempt; P12 confirmed by a person and date; P8 the judged row of the attempt vector lives here |
| Origin | P5 derived, not guessed; P11 a derivation record, not a trust argument |
| Evidence | P1 exact vs numerical, `supported` is not `proved`; P4 instances before formalization |
| Relations | P6 stronger statements are separate; P10 restrictions name the refuted ancestor |
| Status | P8 derived from attempts and claims; P10 refuted stays refuted |
