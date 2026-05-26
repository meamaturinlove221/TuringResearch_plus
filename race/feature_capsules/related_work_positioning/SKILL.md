---
name: turingresearch-related-work-positioning
description: Build conservative related-work positioning reports from method cards, citation graphs, and collision risk.
---

## Role

Create evidence-backed related-work positioning for TuringResearch Plus without
overclaiming novelty.

## When to use

Use after PaperMethodCard, CitationGraph, and CollisionRiskReport artifacts
exist.

## Inputs

- PaperMethodCard
- CitationGraph
- CollisionRiskReport
- manual reviewer notes

## Outputs

- RelatedWorkPositioningReport
- safe claims
- unsafe claims
- missing evidence

## Required files

- `race/feature_capsules/related_work_positioning/FEATURE.md`
- `race/feature_capsules/related_work_positioning/contract.yaml`

## Related contracts

- `contracts/paper_method_card.yaml`
- `contracts/citation_graph.yaml`
- `contracts/collision_risk.yaml`

## Related lanes

- `lanes/51_v0.3_sprint_2_scope_and_capsules.md`

## Required tests

- positioning unit tests
- fake workflow tests
- markdown export tests

## Rules / constraints

- Do not produce definitive novelty claims without evidence.
- Do not treat fake method cards as full paper review.
- Keep `requires_human_review` where evidence is incomplete.

## Done criteria

- report supports JSON and Markdown
- safe and unsafe claims are separated
- missing evidence is explicit
