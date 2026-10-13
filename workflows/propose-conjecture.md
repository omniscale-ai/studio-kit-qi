---
description: Invoke when the user asks to state, register or formalize a NEW conjecture under a research run — e.g. "conjecture the bound for n=3", "register this pattern as a conjecture", "write the Lean statement of X". Produces a CONJECTURE artifact with an exact instance check and a compiled formal statement; requires an approved RESEARCH-PLAN.
---

# Workflow: propose-conjecture

## Inputs

- A candidate statement and where it came from: an exploration record, a PROOF-ATTEMPT handoff, a proved or refuted CONJECTURE, a cited result.

## Step 0 — Plan gate

Locate an `approved` RESEARCH-PLAN covering this work. **If none exists, run `workflows/plan-research.md` FIRST.** The plan's Conjecture Policy, Definitions Concordance and Budget govern every step below; a concept with no concordance row sends you back to plan-research for an amendment.

## Steps

1. **Name the origin.** Exactly one row of the plan's Conjecture Policy, with the IDs or record it derives from. A statement with no origin is not registered: report it to the user as an observation, not a conjecture.
2. **State it at the strength the evidence supports.** The claimed scope is the region you will check in step 3; the hypotheses are the ones the evidence needs. A wider statement is a second CONJECTURE with its own evidence, not a footnote.
3. **Check instances exactly, before anything else.** Enumerate or compute with exact arithmetic over the smallest non-trivial region (all deterministic strategies, all alphabets up to a bound, all parameter values on a grid of rationals); for larger spaces run `workflows/hunt-counterexample.md`. Record region, method and where the check lives in the Evidence table, including an empty result. A counterexample is a result: package it as a CLAIM (+ CERTIFICATE + CHECK-RUN when the check is non-trivial), name it in the Refuted by line, and register the conjecture directly as `refuted`.
4. **Compile the formal statement.** In the plan's project at the pinned toolchain, write a stub `theorem <name> : <statement> := sorry`, build, and run `#check @<name>`; paste the output into the Formal Statement block verbatim with the stub's file and commit. Map every symbol to a concordance row. **NEVER type a signature by hand.**
5. **Cross-check faithfulness, independently (P13).** (a) *Independent reading*: hand the Lean block, the definitions it uses and the plan's Definitions Concordance — and NOT the Statement section — to someone who did not write the block: a named human, or a second agent instance started fresh for this purpose (the plan's Conjecture Policy says which). They translate it back into prose: quantified objects, hypotheses, conclusion, encoding relied on, what is not claimed, and anything that looks unintended. Quote the back-translation verbatim and compare it with the Statement element by element in the Faithfulness Cross-Check table. (b) *Instance agreement*: evaluate the Lean definitions (`#eval` / `decide` in the plan's project) on the instances of the Evidence table and compare with the exploration record. Record every discrepancy and its resolution; a discrepancy in the Lean block sends you back to step 4 (new stub, new compilation) and restarts this step. **The author of the block never performs the reading alone, and the agent never confirms its own formalization.** Only when every element row is `yes` and every instance row is `agree` or `n/a` does the confirming person write the `Confirmed faithful by` line; without it no attempt can start and none can be `pass`.
6. **Register.** Add the row to the RESEARCH-PLAN's Conjecture Register with the status copied from the frontmatter; fill Relations (what it implies, strengthens, restricts; the refuted ancestor if any).
7. **Gate.** `python3 {scripts}/graph_gate.py <artifacts-root>` must PASS (G6 status evidence, G8 register consistency).

## Hard rules

- Numerical screening never moves a conjecture to `supported`; only an exact check does.
- A `refuted` conjecture is never re-proposed under a new name; a restriction is a new CONJECTURE whose Origin is `restriction of <ID>` and whose hypotheses exclude the counterexample.
- One statement per CONJECTURE; a conjunction whose parts have different routes is split.
- A back-translation that disagrees with the Statement is a defect in the Lean block or in the concordance, never something to argue away in the Discrepancies line; fix, recompile, re-read.
- Statuses `proved` and `refuted` are set only together with the artifact that establishes them, named in the Proved by / Refuted by lines (a certified CLAIM or an attested PROOF-ATTEMPT), never on the agent's judgment; graph_gate G6 verifies every such status.
