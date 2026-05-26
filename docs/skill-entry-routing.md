# Skill Entry Routing

Status: implemented minimal.

Round 73 adds a local routing surface for TuringResearch Plus skills:

- `.agents/ENTRY.md`
- `.agents/ROUTING_TABLE.md`
- `.agents/SKILL_POLICY.md`
- `src/turing_research_plus/skills/`

The router recommends a skill and ranked alternatives. It does not execute a
skill, spawn an agent, or run a tool.

## Covered Categories

- upstream watch
- VGGT dogfooding
- evidence ledger
- artifact audit
- visual audit
- advisor pack
- PDF extraction
- route DSL
- hard gates
- failure taxonomy
- paper method
- figure architecture
- citation graph
- collision risk
- related work
- web fetch
- handoff
- pod workflow
- vault graph
- ontology

## Missing Inputs

`docs/upstream-learning-report.md` is not present. Round 73 uses
`docs/upstream-refresh-2026-05-20.md` as the conservative upstream context.

## Boundary

Routing is a decision aid. It never replaces the current round instructions,
never runs live services by itself, and never converts planned work into
observed evidence.
