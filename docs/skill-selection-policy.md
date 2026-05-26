# Skill Selection Policy

Status: active.

Use the most specific `turingresearch-*` skill that matches the task. Use
`turingresearch-master-orchestrator` when the request spans multiple lanes,
needs coordination, or has no clear route.

## Tie Breakers

- Contracts and public API changes: prefer `turingresearch-architecture-contracts`.
- Release, packaging, docs, and broad tests: prefer `turingresearch-qa-release`.
- Race mode and feature capsules: prefer `turingresearch-race-feature-capsule-factory`.
- Paper and advisor workflows: prefer `turingresearch-paper-writing-pipeline`.
- Vault, ontology, and wiki graph: prefer `turingresearch-fusion-wiki-vault`.

## Non-Execution Rule

Selecting a skill is not permission to run a tool or execute remote work. The
round request still controls filesystem edits, network access, and live tests.
