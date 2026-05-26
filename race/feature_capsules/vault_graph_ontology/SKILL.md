---
name: turingresearch-vault-graph-ontology
description: Maintain vault graph enhancements and ontology SOPs for evidence-backed research memory.
---

## Role

Improve TuringResearch Plus vault graph traversal, edge audit, and ontology
SOPs.

## When to use

Use when research artifacts need typed graph edges, alias resolution, ontology
exports, or missing evidence checks.

## Inputs

- vault pages
- evidence refs
- method cards
- citation graph nodes
- collision reports

## Outputs

- VaultGraphAuditReport
- OntologySOPResult
- graph traversal report

## Required files

- `contracts/vault_schema.yaml`
- `race/feature_capsules/vault_graph_ontology/contract.yaml`

## Related contracts

- `contracts/vault_schema.yaml`

## Related lanes

- `lanes/51_v0.3_sprint_2_scope_and_capsules.md`

## Required tests

- vault graph tests
- edge audit tests
- ontology SOP fixture tests

## Rules / constraints

- Do not promote evidence-free edges.
- Keep graph outputs deterministic.
- Require human review for ontology exports.

## Done criteria

- graph audit exists
- ontology SOP fixtures exist
- missing evidence is reported
