# Feature Capsule: vault_graph_ontology

## Problem

TuringResearch vault and graph memory need stronger traversal, edge audit, and
ontology SOPs so research claims, method cards, and positioning notes remain
evidence-backed.

## VGGT motivating example

VGGT related work creates many concepts: SMPL-X feature encoding, SparseConv3D,
tri-plane features, token injection, and collision risk. These need typed graph
edges, aliases, confidence, and audit trails.

## Upstream inspiration

Yogsoth signals highlight wiki/vault edge audit, inline `[[wikilink]]`, and
ontology SOPs such as seed-concept search, alias resolution, edge batch
creation, hierarchy visualization, and ontology export.

## User story

As a researcher, I want vault graph and ontology operations to preserve evidence
refs, confidence, and auditability across related-work and experiment artifacts.

## Inputs

- vault pages
- method cards
- citation graph nodes
- collision reports
- evidence refs
- manual concept notes

## Outputs

- `VaultGraphAuditReport`
- ontology SOP outputs
- missing evidence report
- graph traversal report
- ontology export

## Data model

- `VaultGraphAuditReport`
- `OntologySOPResult`
- `ConceptNode`
- `TypedEvidenceEdge`
- `AliasResolution`

## Proposed commands / tools

- command: `turing vault graph-audit`
- tool: `vault.graph_audit`
- output: `VaultGraphAuditReport`

## Related contracts

- `contracts/vault_schema.yaml`

## Related skills

- `turingresearch-fusion-wiki-vault`
- `turingresearch-architecture-contracts`
- `turingresearch-qa-release`

## Required tests

- typed edge traversal
- edge audit
- missing evidence detection
- alias resolution SOP
- ontology export fixture

## Risks

- graph noise
- unsupported edges
- evidence-free ontology claims
- SOP sprawl

## Done criteria

- edge audit reports missing evidence
- graph traversal is deterministic
- ontology SOP fixtures exist
- exports support Markdown and JSON

## Release target

v0.3 Sprint 2.

## Non-goals

- no automatic truth inference
- no unsupported edge promotion
- no UI graph editor
