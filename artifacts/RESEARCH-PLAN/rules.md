# RESEARCH-PLAN Rules

**Dependencies**:
- `{principles}` — cross-cutting invariants P1–P13; load before these rules
- `{rplan_template}` — structural reference

---

1. **The plan gates the work.** `propose-conjecture`, `attempt-proof` and a `hunt-counterexample` run under a research question require an `approved` RESEARCH-PLAN covering their scope. Work without one is a rule violation regardless of outcome. Verification of a *published* result is a VERIFICATION-PLAN, not this kind.
2. **One run is one plan, written before the first conjecture is registered.** The research question is copied verbatim from the human, not paraphrased.
3. **The concordance is complete before approval.** Every concept the question mentions has a row with a Lean declaration that was resolved by `#check` or `#print` in the pinned toolchain on a stated date. A project definition counts once its file is named. "We will define it later" blocks approval.
4. **Cost is asked from a human.** The Formalization Cost table is filled with name and date for every row; an empty row is not approvable.
5. **Budget is counted in attempts and hours.** Per conjecture per route, total, and wall-clock. A conjecture at its attempt limit is reported in the last attempt's Handoff and in the register; it is not retried under this plan.
6. **The phase sequence is the skeleton.** EXPLORE → PROPOSE → CHECK → ATTEMPT → REPORT, instance checks strictly before attempts, every phase ending at a human gate with feedback kept verbatim.
7. **The register is the only index of the run's conjectures.** Every CONJECTURE has one row; the row's status equals the CONJECTURE frontmatter (`graph_gate` G8). A status changes in the CONJECTURE first, by a PROOF-ATTEMPT or a certified CLAIM, and the row follows. A refuted row stays.
8. **The independent reader is named before the first conjecture.** The Conjecture Policy says who back-translates formal statements (a human, or a second agent instance started fresh for the purpose) and who confirms; the author of a Lean block never reads it alone (P13).
9. **Success criteria are computable from what an attempt produces.** Every mechanical row is a function of the compiler's output, the project files and the CONJECTURE; a row that nothing can compute and no named human judges does not belong in the table. The six rows `attest_lean.py` measures are present in every plan that allows tier C.
10. **The allowed axiom set is declared here.** Default `propext`, `Classical.choice`, `Quot.sound`. An attempt that needs an external theorem does not add an `axiom`: the theorem becomes a `cited` LEMMA and a CONJECTURE to formalize. Widening the set is a new plan.
11. **Options were real.** The Decisions Log shows genuine alternatives with costs for every brainstorm group, not a single "proposed and accepted" line. If the human waived the brainstorm, the log records the waiver and the defaults applied. Amendments are new dated entries plus re-approval of the changed items; a major pivot is a new plan and the old one is `superseded`.
12. **Approval is a person and a date**, with explicit confirmation of the cost table and the criteria table. `draft` plans gate nothing; `superseded` and `closed` plans gate nothing new but their attempts stand.

## Where the principles land in a RESEARCH-PLAN

| Section | Principles |
|---------|------------|
| Prior Knowledge | P9 verified vs assumed |
| Definitions Concordance | P2 every concept, its Lean declaration, checked how and when |
| Formalization Cost | P3 asked from a human, name and date |
| Phase Sequence | P4 instances before attempts; P12 gates |
| Conjecture Policy | P5 admissible origins; P6 strongest supported; P1 evidence kinds per route; P13 who performs the independent reading |
| Conjecture Register | P10 refuted rows stay; P8 statuses derived, copied from the CONJECTURE |
| Success Criteria | P7 agreed, argued, frozen; P8 vector, mechanical rows measured by the script; P13 `statement-confirmed` reads the cross-check |
| Decisions Log | P12 options were real; choices and feedback verbatim |
| Approval | P3 and P7 confirmed explicitly; P12 |
