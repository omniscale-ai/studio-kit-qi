---
status: approved
date: 2026-08-11
---

# Verification plan: Gitton–Renner EJM nonlocality (arXiv:2510.15143)


<!-- toc -->

- [Scope](#scope)
- [Depth Targets](#depth-targets)
- [Allowed Interventions](#allowed-interventions)
- [Budget](#budget)
- [Deliverables](#deliverables)
- [Decisions Log](#decisions-log)
- [Approval](#approval)

<!-- /toc -->

**ID**: `cpt-qi-vplan-ejm-gitton`
## Scope

Verify the central computational claim of arXiv:2510.15143 via its artifact repository github.com/vgitton/fast-inflation:

1. (priority 1) `cpt-qi-claim-ejm-triangle-nonlocal` — the EJM 2×2×4 nonlocality certificate.
2. (priority 2) the shipped SRB 2×2×2 certificate — as the tractable target for implementation diversity.

Out of scope: the paper's analytic sections (inflation convergence theory); the symtree re-derivation (flagged as the known weakest link, deferred).

## Depth Targets

- EJM certificate: **(c) environment diversity** — authors' checker on macOS/arm64/clang/libc++ without Mosek (estimate accepted: ~half a day incl. porting). (d) implementation diversity deferred until a symtree-based enumerator exists.
- SRB certificate: **(d) implementation diversity** — clean-room checker from decoded semantics (estimate accepted: ~1 day, agent-assisted).

## Allowed Interventions

- Patching fast-inflation for the macOS port: **approved**, mechanical fixes only, semantics untouched, patch preserved for upstream PR.
- Stubbing the commercial Mosek dependency: **approved** — justified because the check path never calls the solver (to be evidenced by `fw: 0ms` in logs).
- Contacting the authors: **not yet** — deferred to a separate decision.
- Publication of the verification project: **approved** (public kit repo).

## Budget

One working day; Apple Silicon laptop; GMP via Homebrew; no solver licenses.

## Deliverables

CLAIM/CERTIFICATE/CHECK-RUN artifact chains for both certificates; both gates green (`cfs validate`, `graph_gate`); walkthrough deck.

## Decisions Log

- *Scope:* offered (a) certificate-only vs (b) certificate + claim-graph of the paper's analytic half vs (c) full paper. Chosen: (a) for EJM + SRB; (b) deferred to the PGR track where it is already exercised.
- *EJM depth:* offered (b) reproduce on Linux (needs Mosek license for the build system as shipped) vs (c) port to macOS with Mosek stubbed. Chosen: (c) — no license available, and the port doubles as an upstream contribution.
- *SRB depth:* offered (c) same-port rerun vs (d) independent checker. Chosen: (d) — SRB's 4096-event space makes clean-room verification cheap and it validates the certificate *semantics*, benefiting EJM later.
- *Mosek stub:* explicitly flagged as third-party code modification; approved with the `fw: 0ms` evidence requirement.

*Provenance note: this plan was reconstructed post-hoc from the 2026-08-10/11 session as the kit's canonical example — the run itself predated the plan-verification workflow (which this example motivated).*

## Approval

Approved by the project owner in-session, 2026-08-11 (retroactive record).
