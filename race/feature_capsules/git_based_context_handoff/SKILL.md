---
name: turingresearch-git-context-handoff
description: Use when designing or implementing Git-based context packages for TuringResearch Plus.
---

# TuringResearch Plus Skill: turingresearch-git-context-handoff

## Role

Design and maintain Git-based context handoff packages without executing remote
code or transferring unsafe data.

## When to use

Use for v0.3 Sprint 1 context package, memory policy, handoff safety, and
structured return planning.

## Inputs

- `docs/git-based-context-handoff.md`
- `contracts/git_context_handoff.yaml`
- v0.2 handoff bundle and route artifacts

## Outputs

- Context package design artifacts
- Safety policy updates
- Tests for package contents and forbidden files

## Rules / constraints

- Git is transport only.
- Do not run remote code.
- Do not include `.env`, API keys, raw data, or SMPL-X body model files.
- Do not treat `MEMORY.md` as the only source of truth.

## Done criteria

- Package design is reviewable.
- Handoff safety gates are enforced.
- Import produces proposed updates only.
