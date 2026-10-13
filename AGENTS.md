# Constructor Studio Kit: Theorem Kit (`studio-kit-qi`)

Agent quick reference for machine-checkable mathematical claims: verified proofs, exact certificates and Lean-attested discovery. Domain-neutral; example packs for quantum information (`examples/qi/`) and number theory (`examples/euler-polynomial/`).

## What it is

Ten artifact kinds in four layers. The **certificate layer** makes an impossibility claim and its exact witness checkable by anyone (CLAIM, CERTIFICATE, CHECK-RUN). The **theorem layer** decomposes a published proof into a claim graph with honest statuses (THEOREM, PROOF-MAP, LEMMA). The **intake plans** record the human's decisions before heavy work starts (VERIFICATION-PLAN for published results, RESEARCH-PLAN for new ones). The **discovery layer** registers new statements and the attempts to prove or refute them, with the Lean compiler as the judge (CONJECTURE, PROOF-ATTEMPT). Thirteen cross-cutting principles bind all ten.

## Artifact kinds

| Kind | Semantic intent (when to use) | References |
| --- | --- | --- |
| CLAIM | One precise finite statement with exact data — an impossibility about a class of models, an infeasible instance, or the exact data of a confirmed counterexample — checkable by a certificate. | `{claim_rules}`, `{claim_template}` |
| CERTIFICATE | The witness of one CLAIM: external hashed file, mathematical semantics precise enough for a clean-room checker, provenance (informational). | `{certificate_rules}`, `{certificate_template}` |
| CHECK-RUN | One verification of one certificate in one environment. Script-generated, never hand-written; verdict `pass` / `fail` / `error`. | `{check_run_rules}`, `{check_run_template}` |
| THEOREM | A published theorem under claim-graph verification: statement, source, proof map, trust summary naming the weakest load-bearing link. | `{theorem_rules}`, `{theorem_template}` |
| PROOF-MAP | The lemma DAG of one published proof, faithful to the source, with load-bearing nodes explicit. | `{proof_map_rules}`, `{proof_map_template}` |
| LEMMA | One node of a proof map with a single verification route (tier A exact / B symbolic / C formal / cited / expert) and a status that never exceeds its artifacts. | `{lemma_rules}`, `{lemma_template}` |
| VERIFICATION-PLAN | Intake decisions for verifying a published result: scope, depth per claim with accepted cost, allowed interventions, budget, deliverables, approval. | `{vplan_rules}`, `{vplan_template}` |
| RESEARCH-PLAN | One discovery run: question, prior knowledge, definitions concordance, human-confirmed formalization cost, budget, phases, conjecture policy, conjecture register, frozen success criteria, approval. | `{rplan_rules}`, `{rplan_template}` |
| CONJECTURE | One new statement: informal and compiled formal statement, the mandatory faithfulness cross-check between the two (independent back-translation + instance agreement), origin under the plan's policy, instance evidence, relations to other conjectures, attempts, status derived from them. | `{conjecture_rules}`, `{conjecture_template}` |
| PROOF-ATTEMPT | One attempt at one conjecture by one route: development, assumptions with licences, script-owned build log and verdict vector, handoff to the next conjecture or attempt. | `{proof_attempt_rules}`, `{proof_attempt_template}` |

## Navigation rules

ALWAYS open and follow `{principles}` WHEN authoring or reviewing any artifact of this kit

ALWAYS open the kind's `rules.md` and `template.md` from the table above WHEN authoring that kind

ALWAYS locate an `approved` VERIFICATION-PLAN or RESEARCH-PLAN covering the work BEFORE verifying, decomposing, searching, proposing or attempting anything; run the matching plan workflow first if none exists

ALWAYS run `cfs validate` and `python3 {graph_gate} <artifacts-root>` on the written artifacts before presenting them

ALWAYS generate a PROOF-ATTEMPT with `python3 {attest_lean} …` and a CHECK-RUN with the kit checker; fill only the sections the script leaves to the agent

NEVER write `pass`, `proved`, `refuted`, `certified`, `machine-checked` or `formalized` on your own authority: a PROOF-ATTEMPT or CHECK-RUN status is written by its script, and a CONJECTURE, CLAIM, LEMMA or THEOREM status is set only together with the artifact that establishes it, which `graph_gate` verifies

NEVER edit the script-owned sections of a PROOF-ATTEMPT or any section of a CHECK-RUN; re-run the script instead

NEVER change success criteria, the allowed axiom set or the conjecture policy outside a new RESEARCH-PLAN

NEVER re-propose a `refuted` conjecture under a new name; a restricted statement is a new CONJECTURE naming the refuted one in its Origin

NEVER confirm the faithfulness of a Lean statement you wrote yourself; the independent reading of the Faithfulness Cross-Check is done by a named human or a second agent instance that has not seen the informal Statement
