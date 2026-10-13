# CONJECTURE — Review Checklist

- [ ] Statement has every quantifier explicit and names the RESEARCH-PLAN it belongs to?
- [ ] Formal Statement block is a compiler's `#check` output (stub file and commit named), not typed by hand?
- [ ] Every symbol of the formal statement resolves to a row of the plan's Definitions Concordance?
- [ ] Faithfulness Cross-Check: the independent reader did not write the Lean block and was not shown the Statement; back-translation quoted verbatim; every element row `yes`?
- [ ] Faithfulness Cross-Check: Lean definitions evaluated on the Evidence instances and compared with the exploration record (`agree`, or `n/a` with a reason)?
- [ ] Every discrepancy recorded with its resolution; `Confirmed faithful by` names a person and a date written after both parts agree (or the route is tier A via a CLAIM)?
- [ ] Exactly one origin, with the IDs or record it derives from?
- [ ] Evidence has at least one exact instance check before the first attempt, with the region and the record; negative space recorded?
- [ ] Claimed scope equals the checked region; no hypothesis dropped beyond what the evidence covers?
- [ ] Attempts listed most recent first with statuses; attempt limit respected?
- [ ] Status lines (Proved by / Refuted by / Withdrawn by) resolve to artifacts with the required status (run graph_gate)?
- [ ] If an ancestor was refuted: Relations names it and the hypothesis that excludes the counterexample?
