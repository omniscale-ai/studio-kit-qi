# Principles

Cross-cutting invariants for every artifact in this kit — the certificate layer
(CLAIM, CERTIFICATE, CHECK-RUN), the theorem layer (THEOREM, PROOF-MAP, LEMMA),
the intake plans (VERIFICATION-PLAN, RESEARCH-PLAN) and the discovery layer
(CONJECTURE, PROOF-ATTEMPT). Each `rules.md` loads this file first and keeps
only what is specific to its own kind. A principle is stated once here; the
per-kind line says where it lands in that artifact.

P1. **Evidence kinds are never pooled.** There are three: *numerical* (floating
    point — screens and ranks candidates, asserts nothing), *exact* (rational or
    integer arithmetic on finite instances — asserts those instances, certifies
    a finite CLAIM), and *formal* (a building proof-assistant development —
    asserts the statement for every case in its scope). A conjecture checked on
    a million instances is `supported`, not `proved`; a Lean theorem about a
    definition that differs from the paper's proves nothing about the paper.
    Every artifact says which kind it carries, and no artifact reports a
    weaker kind as a stronger one.
    CLAIM: Exact Data is exact only. CERTIFICATE and CHECK-RUN: the checking
    predicate is exact. LEMMA: Verification names the tier (A exact / B
    symbolic / C formal). CONJECTURE: Evidence says exact or numerical per
    instance check; `supported` is never `proved`. PROOF-ATTEMPT: Route names
    the tier.

P2. **Definitions are reconciled before the first attempt.** One concordance
    table: each concept, its notation in the source or the informal statement,
    the Lean declaration it maps to (Mathlib name or project definition with
    file), and how and when the mapping was checked. Encoding choices (±1 vs
    {0,1} outcomes, normalisation conventions, party and setting labels) are
    rows of this table, never applied silently. A proof attempted against an
    unreconciled definition is an attempt at a different statement.
    RESEARCH-PLAN: Definitions Concordance; a missing row blocks approval.
    CONJECTURE: every symbol of the Formal Statement resolves to a concordance
    row, and a named human confirms the formal statement is faithful to the
    informal one. PROOF-ATTEMPT: criterion `statement-matches` compares the
    built declaration's signature with the confirmed Formal Statement. CLAIM:
    the Model Class decomposition matches the cited literature's convention.

P3. **Cost is asked from a human, not assumed.** Before approval a human states
    the figures the plan depends on: toolchain and Mathlib build time on the
    available machine, effort per route tier for this concrete case, compute per
    exploration batch, solver and library licences. Recorded with name and
    date. An agent that cannot find a figure asks instead of estimating.
    VERIFICATION-PLAN: Depth Targets quote the effort that was accepted.
    RESEARCH-PLAN: Formalization Cost; an empty table is not approvable.
    PROOF-ATTEMPT: actual time beyond the confirmed figure by the plan's factor
    is a Deviation raised with the human before the next attempt.

P4. **Instances before formalization.** Before any Lean effort on a conjecture
    it is checked exactly on finite instances (small parameters, small
    alphabets or dimensions, enumerable structure spaces) and the checked region is recorded,
    including an empty result. A conjecture that fails an instance check is
    refuted at the cost of seconds, not weeks. Skipping the check is a
    deviation with a stated reason.
    RESEARCH-PLAN: Phase Sequence places instance checks before attempts.
    CONJECTURE: Evidence records region, method and where the check lives.
    PROOF-ATTEMPT: an attempt on a conjecture with empty Evidence is listed in
    Deviations. The hunt-counterexample workflow records negative space.

P5. **New conjectures are derived, not guessed.** Every CONJECTURE names its
    origin as exactly one of: generalization or specialization of a proved or
    cited statement (its ID); a pattern in an exploration record (record and
    cases); a gap left by an attempt's handoff (attempt ID and goal); a
    strengthening or weakening of a refuted or proved conjecture (its ID).
    "Interesting", "natural" and "explore" are not origins; a statement without
    one is not registered.
    RESEARCH-PLAN: Conjecture Policy lists the admissible origins. CONJECTURE:
    Origin. PROOF-ATTEMPT: Handoff is the only legitimate source of gap
    origins.

P6. **A conjecture is the strongest statement its evidence supports, and no
    stronger.** Hypotheses are the fewest the instance checks and the proof
    use; scope is claimed only where instances were checked; a statement
    beyond the checked region, or with a hypothesis dropped, is a separate
    CONJECTURE with its own evidence. When an attempt's proof does not use a
    hypothesis, the handoff says so and the strengthened statement enters as a
    new conjecture with origin "strengthening of <ID>".
    CONJECTURE: Statement, Evidence (checked region next to claimed scope),
    Relations. PROOF-ATTEMPT: Handoff names unused hypotheses.

P7. **What counts as proved is agreed with a human and frozen.** The success
    criteria of a plan — build passes, closure sorry-free, axioms within the
    allowed set, signature equals the confirmed formal statement, dependencies
    pinned, formal statement confirmed faithful, and any route-specific row —
    are proposed with a justification (what the row measures, why it answers
    the research question, what it would miss), confirmed by name and date,
    and frozen when the first attempt starts: no row added, removed or
    re-thresholded. A criterion that turns out wrong is raised with the human;
    the fix is a new plan with a new ID, and attempts judged under the old plan
    stand.
    RESEARCH-PLAN: Success Criteria blocks, Frozen at line, Confirmed by.
    PROOF-ATTEMPT: Verdict has exactly the plan's rows; a doubt about a row
    goes into Deviations with a proposal for a new plan.

P8. **The verdict is a vector and the checker is the judge.** No confidence
    score, no "essentially proved", no weighting of rows into one number. Each
    criterion is pass or fail from its own measurement. Mechanical rows are
    written by the attestation script from the compiler's own output and are
    never edited by hand; a judged row names the human who filled it. The
    status field of a PROOF-ATTEMPT or a CHECK-RUN belongs to the script: an
    agent never writes `pass`, `proved` or `certified` on its own authority.
    PROOF-ATTEMPT: the status and generated-by lines and the sections
    Conjecture, Route, Development, Build Log and Verdict are script-owned and
    sealed by the owned-sections hash that `graph_gate` recomputes; Attestation
    records that hash.
    CHECK-RUN: script-generated only. CONJECTURE: `proved` and `refuted` are
    derived from attempts and claims by `graph_gate`, never asserted. THEOREM:
    status computed from load-bearing nodes.

P9. **A statement is verified before it licenses a step.** A Mathlib lemma
    enters an attempt only after `#check` resolves it in the pinned version; an
    external theorem enters a proof map only as `cited` with its exact
    statement at a resolved location; a result recalled from memory or
    literature without a located quote is `assumed` and licenses nothing but a
    diagnostic instance check.
    RESEARCH-PLAN: Prior Knowledge marks `verified` / `assumed`. PROOF-ATTEMPT:
    Assumptions give a licence per lemma relied on. LEMMA: `cited` quotes the
    exact statement. The audit-references workflow enforces statement-level
    resolution.

P10. **Refuted stays refuted.** A CONJECTURE with a refuting attempt or a
    certified counterexample CLAIM keeps status `refuted`. It is not
    re-proposed in the same or a renamed form; a restricted statement is a new
    CONJECTURE whose Origin names the refuted one and whose hypotheses exclude
    the counterexample. A lemma refuted during verification keeps the
    refutation linked.
    CONJECTURE: Status and Relations. RESEARCH-PLAN: the register keeps the
    refuted row. LEMMA: negative results kept (rule 4). `graph_gate` fails a
    conjecture that is not `refuted` while a refuting artifact references it.

P11. **Trust never lives in the search.** How a certificate, a counterexample
    or a proof was found — SDP, Frank–Wolfe, an LLM, a week of a human's time —
    is provenance, informational only. Two artifacts that pass the same checks
    are equally trusted; an artifact that passes no check is trusted by nobody
    whoever produced it.
    CERTIFICATE: Provenance is informational. PROOF-ATTEMPT: Route and
    Development record the tools; the Verdict comes from the checker alone.
    CONJECTURE: Origin is a derivation record, not a trust argument.

P12. **Human gates and their feedback are part of the record.** Plans are
    approved by a person and a date; every phase ends at a gate; a rejected
    phase re-runs with the feedback text kept verbatim on the artifacts it
    changed, with what changed because of it.
    VERIFICATION-PLAN and RESEARCH-PLAN: Approval. CONJECTURE: Faithfulness
    Cross-Check confirmed by a person and date. PROOF-ATTEMPT: Deviations cite
    feedback verbatim. THEOREM and LEMMA: `expert-verified` names the reviewer
    and the scope of review.

P13. **The formal statement is cross-checked against the informal one,
    independently, before any attempt.** The compiler checks that a Lean
    statement is well-typed, never that it says what the human meant; a green
    proof of a mis-stated theorem passes every mechanical gate. So every
    CONJECTURE with a Lean block carries a Faithfulness Cross-Check with two
    parts. *Independent reading*: someone who did not write the block — a named
    human, or a second agent instance given only the block, the definitions it
    uses and the plan's concordance, and not the informal Statement — translates
    it back into prose, and the back-translation is compared with the Statement
    element by element: quantified objects, hypotheses, conclusion, encoding and
    conventions, what is not claimed. *Instance agreement*: where finite
    instances exist, the Lean definitions are evaluated on the instances of the
    Evidence table and must reproduce the exploration record. Every discrepancy
    is recorded with its resolution; a change to the block recompiles the stub
    and restarts the check. No attempt starts, and no attempt is `pass` or
    `refuted`, without both parts agreeing and a named, dated confirmation.
    CONJECTURE: Faithfulness Cross-Check section; `Confirmed faithful by` only
    after both parts agree. RESEARCH-PLAN: criterion `statement-confirmed`;
    Conjecture Policy names who performs the independent reading; Definitions
    Concordance supplies the rows the check cites. PROOF-ATTEMPT: the
    `statement-confirmed` row is copied from the cross-check and never filled by
    the attempt; `statement-matches` ties the proved declaration to the
    cross-checked block. `graph_gate` G6 fails a conjecture that has attempts, or
    is `proved` / `refuted`, without a complete cross-check.
