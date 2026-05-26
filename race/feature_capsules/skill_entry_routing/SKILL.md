---
name: turingresearch-skill-entry-routing
description: Maintain ENTRY.md and routing tables for TuringResearch Plus skills and lanes.
---

## Role

Maintain TuringResearch Plus skill and lane routing.

## When to use

Use when adding workflows, skills, or entry-point guidance.

## Inputs

- docs/skills-index.md
- lanes
- contracts
- workflow docs

## Outputs

- ENTRY.md
- routing table
- SkillRoutingDecision

## Required files

- `ENTRY.md`
- `race/feature_capsules/skill_entry_routing/contract.yaml`

## Related contracts

- skills integrity contract

## Related lanes

- `lanes/51_v0.3_sprint_2_scope_and_capsules.md`

## Required tests

- entry routing tests
- skill integrity tests
- name integrity tests

## Rules / constraints

- Do not execute code from routing.
- Do not reference missing skills.
- Do not use old names.

## Done criteria

- every route resolves
- missing routes are reported
- stale names fail tests
