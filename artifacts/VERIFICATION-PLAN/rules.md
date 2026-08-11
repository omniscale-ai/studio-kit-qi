# VERIFICATION-PLAN — Generation & Validation Rules

1. **The plan precedes the work.** Downstream workflows (verify-certificate, decompose-proof, hunt-counterexample) require an `approved` plan covering their scope. Work without one is a rule violation regardless of outcome.
2. **Options were real.** The Decisions Log must show genuine alternatives with costs, not a single "proposed and accepted" line per topic. If the user waived the brainstorm, the log records the waiver and which defaults were applied.
3. **Interventions are enumerated.** Any modification of third-party code, dependency stubbing, author contact, or publication MUST appear in Allowed Interventions before it happens. Discovering mid-work that an unlisted intervention is needed sends you back to plan-verification for an amendment, not into improvisation.
4. **Amendments supersede, never overwrite.** Changing an approved plan = new dated entry in the Decisions Log + re-approval of the changed items; major pivots = a new plan artifact, the old one marked `superseded`.
5. **`approved` requires the Approval section** (person + date). `draft` plans gate nothing.
