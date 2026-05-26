---
name: tulingresearch-architecture-contracts
description: Use when updating TulingResearch Plus architecture docs, MCP namespaces, or YAML contracts.
---

# TulingResearch Plus Skill: tulingresearch-architecture-contracts

## Role

Maintain MCP namespace contracts and architecture documents for TulingResearch Plus.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `tulingresearch-architecture-contracts` or the matching TulingResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TulingResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `docs/architecture.md`
- `docs/mcp-tools.md`
- `contracts/`

## Related contracts

- `contracts/core_tools.yaml`
- `contracts/pdf_markdown.yaml`
- `contracts/fusion_workflows.yaml`
- `contracts/vault_schema.yaml`
- `contracts/artifact_schema.yaml`
- `contracts/race_features.yaml`
- `contracts/paper_pipeline.yaml`
- `contracts/error_schema.yaml`

## Related lanes

- `lanes/01_architecture_contracts.md`

## Required tests

- `tests/contract/test_release_gate_contract.py`

## Rules / constraints

- Project display name is TulingResearch Plus.
- Core package is `tuling_research` and Plus package is `tuling_research_plus`.
- MCP server name is `tulingresearch-plus`.
- Skill names must use the `tulingresearch-` prefix.
- Keep work inside `TulingResearch/TulingResearch_plus`.
- Do not require real network access, external API keys, or live service calls in tests.
- Preserve EvidenceRef, ResearchArtifact, BudgetGate, and StateLedger boundaries when relevant.
- Use service protocols or adapters for external APIs.
- Update the owner lane and `lanes/00_master_ledger.md` after meaningful changes.

## Done criteria

- Implementation status: `locked`.
- Release requirement: `release-critical`.
- Related tests pass or a release blocker is explicitly recorded.
- Documentation and contracts remain aligned with current TulingResearch Plus naming.
