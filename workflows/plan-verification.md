---
description: Invoke FIRST whenever the user asks to verify a paper, repository, certificate, or theorem and no approved VERIFICATION-PLAN covers that work — e.g. "verify arXiv:XXXX", "check this repo", "validate Gitton's result". Interactive brainstorm producing a VERIFICATION-PLAN artifact; other kit workflows require it.
---

# Workflow: plan-verification

## Purpose

Verification work has order-of-magnitude cost differences (hash check: minutes; independent checker: days; Lean: months) and irreversible-ish decisions (modifying third-party code, contacting authors, publishing results). These are the **user's** decisions. This workflow elicits them BEFORE any heavy action and records them in a VERIFICATION-PLAN artifact that downstream workflows reference.

## Steps

1. **Light recon only.** Read the paper abstract and the repo README/layout. **NEVER clone-and-build, port code, or run anything at this stage** — recon is for informing questions, not starting work.
2. **Brainstorm with the user — one group at a time, offering options with trade-offs** (SDLC-brainstorm style). Required groups:
   - **Scope.** Which claim(s) exactly? The whole paper, one theorem, or just the shipped certificate? Offer the decomposition you see, let the user pick and rank.
   - **Depth per claim.** Menu with costs: (a) integrity only — hashes match declared values; (b) reproduce — run the authors' checker as-is; (c) environment diversity — authors' checker in a new OS/arch/toolchain; (d) implementation diversity — independent clean-room checker; (e) formalization — proof-assistant-verified. State estimated effort for each in this concrete case.
   - **Allowed interventions.** May third-party code be patched (ports, dependency removal)? May commercial dependencies be stubbed? May the authors be contacted? Default: ask-per-case.
   - **Budget & environment.** Time box; machines available; solver/library licenses.
   - **Deliverables.** Artifacts only / report / slides / upstream PR / publication-grade record.
3. **Write the VERIFICATION-PLAN** from `artifacts/VERIFICATION-PLAN/template.md`, including the Decisions Log (question → options offered → user's choice).
4. **Get explicit approval** — the user confirms the plan; record the date in the Approval section. Only then dispatch to `verify-certificate` / `decompose-proof` / `hunt-counterexample`.

## Hard rules

- **NEVER start verification work without an approved plan.** If the user explicitly waives planning ("just do it"), still write a minimal plan recording that waiver and the defaults you chose — the waiver is itself a decision worth an artifact.
- Questions come in small groups with concrete options and costs, not as a wall of 20 questions.
- Scope changes discovered mid-work (e.g., "the build needs a commercial solver we don't have") return to this workflow: update the plan, re-approve the affected decision — do not improvise.
