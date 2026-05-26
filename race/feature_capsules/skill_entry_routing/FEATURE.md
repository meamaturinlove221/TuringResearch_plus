# Feature Capsule: skill_entry_routing

## Problem

TuringResearch has many skills, lanes, and workflows. It needs an explicit
`ENTRY.md` / routing table surface so contributors can choose the right skill
and lane without stale names.

## VGGT motivating example

VGGT dogfooding now spans handoff, run ingest, scholar pipeline, positioning,
advisor pack, and vault work. Routing must identify which skill handles each
request.

## Upstream inspiration

Yogsoth and split-repo signals emphasize `ENTRY.md`, campaign routing tables,
and skill routing. TuringResearch can adopt the pattern with its own skills and
lanes.

## User story

As a contributor, I want one routing entry point that maps user intent to skill,
lane, contract, and expected test surface.

## Inputs

- skill index
- lanes
- contracts
- docs
- workflow names

## Outputs

- `SkillRoutingDecision`
- `ENTRY.md`
- routing table
- missing route report

## Data model

- `SkillRoute`
- `SkillRoutingDecision`
- `RouteTarget`
- `MissingRouteItem`

## Proposed commands / tools

- command: `turing skills route`
- tool: `skills.route_query`
- output: `SkillRoutingDecision`

## Related contracts

- skills integrity contract
- campaign routing docs

## Related skills

- `turingresearch-master-orchestrator`
- `turingresearch-architecture-contracts`
- `turingresearch-qa-release`

## Required tests

- `ENTRY.md` exists
- routes point to existing skill/lane
- stale names rejected
- missing route report generated

## Risks

- stale skill names
- routing drift
- over-centralized routing table

## Done criteria

- entry file exists
- routing table covers major workflows
- integrity tests verify targets
- old names are rejected

## Release target

v0.3 Sprint 2.

## Non-goals

- no dynamic remote skill loading
- no automatic code execution from route selection
- no old project naming
