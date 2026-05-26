# Feature Capsule: related_work_positioning

## Problem

TuringResearch has method cards, citation graphs, and collision risk reports,
but it needs a conservative layer that turns them into related-work positioning
without overclaiming novelty.

## VGGT motivating example

VGGT / SMPL-X feature encoding must be positioned against NeuralBody, HumanRAM,
HART, VGGT-HPE, HGGT, and Fus3D. The report should distinguish overlap,
difference, safe claims, unsafe claims, and missing evidence.

## Upstream inspiration

Neocortica-Scholar and Yogsoth workflows emphasize structured reading,
references, and routing. TuringResearch should use those ideas to improve
positioning while keeping evidence refs and human review.

## User story

As a researcher, I want a related-work positioning report that says what is
probably overlapping, what is different, and what cannot be claimed yet.

## Inputs

- PaperMethodCard
- CitationGraph
- CollisionRiskReport
- cached or fetched public source summaries
- manual reviewer notes

## Outputs

- `RelatedWorkPositioningReport`
- safe positioning notes
- unsafe claim list
- missing evidence list
- recommended next review actions

## Data model

- `RelatedWorkPositioningReport`
- `PositioningClaim`
- `MissingEvidenceItem`
- `ComparisonAxis`

## Proposed commands / tools

- command: `turing paper position`
- tool: `paper.related_work_position`
- output: `RelatedWorkPositioningReport`

## Related contracts

- `contracts/paper_method_card.yaml`
- `contracts/citation_graph.yaml`
- `contracts/collision_risk.yaml`

## Related skills

- `turingresearch-paper-writing-pipeline`
- `turingresearch-fusion-semantic-graph`
- `turingresearch-qa-release`

## Required tests

- fake citation graph positioning
- safe claim generation
- unsafe claim rejection
- missing evidence report
- markdown export

## Risks

- definitive novelty claims without evidence
- collision risk under-reporting
- treating fake method cards as full paper review

## Done criteria

- report consumes method cards, citation graph, and collision risk
- every claim has evidence or requires human review
- unsafe claims are listed explicitly
- output supports JSON and Markdown

## Release target

v0.3 Sprint 2.

## Non-goals

- no final related-work section generation
- no automatic novelty proof
- no claim that fake fixtures are complete paper review
