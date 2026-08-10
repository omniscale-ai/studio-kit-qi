---
date: {YYYY-MM-DD}
---

# {Proof map title}

**ID**: `cpt-{system}-pm-{slug}`

## Theorem

{Reference: `cpt-{system}-thm-{slug}`.}

## Dependency Graph

{The lemma DAG. For each node: ID, one-line statement, status, and incoming edges.
Mermaid or a table; edges mean "is used by". Every node ID must resolve to a LEMMA artifact
(or to a CLAIM for certificate-backed leaves).}

## Load-Bearing Nodes

{The subset of nodes whose failure kills the theorem (not merely a proof route), each with
current status. This list drives the theorem's computed trust status.}
