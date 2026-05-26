---
name: turingresearch-figure-to-architecture
description: Use when planning or implementing Sprint 2 figure-to-architecture diagram drafts.
---

# TuringResearch Plus Skill: figure_to_architecture

## Role

Maintain architecture diagram draft generation from Method Cards and figure
provenance.

## When to use

Use when a task touches figure-to-component mapping, Mermaid architecture drafts,
Graphviz export planning, or unsupported architecture claim warnings.

## Inputs

- Paper Method Cards.
- PDF Phase B asset reports.
- Figure registry entries.
- Route DSL specs.

## Outputs

- `ArchitectureDiagramSpec`
- Mermaid draft
- unsupported-edge report

## Required files

- `race/feature_capsules/figure_to_architecture/FEATURE.md`
- `race/feature_capsules/figure_to_architecture/contract.yaml`
- `race/feature_capsules/figure_to_architecture/sop.mmd`
- `race/feature_capsules/figure_to_architecture/test_plan.md`

## Related contracts

- `contracts/figure_architecture.yaml`
- `contracts/method_cards.yaml`
- `contracts/paper_pipeline.yaml`

## Related lanes

- `lanes/25_v0.2_sprint_2_scope.md`
- `lanes/26_v0.2_sprint_2_feature_capsules.md`

## Required tests

- diagram schema validation
- Mermaid export
- unsupported edge warning
- provenance preservation

## Rules / constraints

- Do not fabricate diagram edges.
- Do not treat draft diagrams as proof.
- Do not require network or live paper lookup.

## Done criteria

- Architecture drafts are traceable to Method Cards and figures.
