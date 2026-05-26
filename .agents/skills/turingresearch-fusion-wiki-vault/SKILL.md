---
name: turingresearch-fusion-wiki-vault
description: Use when maintaining the markdown vault, BM25-like index, graph edges, lint, or artifact ingestion.
---

# TuringResearch Plus Skill: turingresearch-fusion-wiki-vault

## Role

Maintain local claim-evidence vault pages, graph edges, linting, search, and ResearchArtifact ingestion.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-fusion-wiki-vault` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research_plus/vault/`
- `docs/vault.md`

## Related contracts

- `contracts/vault_schema.yaml`
- `contracts/artifact_schema.yaml`

## Related lanes

- `lanes/05_vault_memory.md`

## Required tests

- `tests/unit/test_vault_models.py`
- `tests/unit/test_vault_markdown_io.py`
- `tests/unit/test_vault_graph.py`
- `tests/unit/test_vault_lint.py`
- `tests/unit/test_vault_artifact_ingestion.py`

## Rules / constraints

- Project display name is TuringResearch Plus.
- Core package is `turing_research` and Plus package is `turing_research_plus`.
- MCP server name is `turingresearch-plus`.
- Skill names must use the `turingresearch-` prefix.
- Keep work inside `TuringResearch/TuringResearch_plus`.
- Do not require real network access, external API keys, or live service calls in tests.
- Preserve EvidenceRef, ResearchArtifact, BudgetGate, and StateLedger boundaries when relevant.
- Use service protocols or adapters for external APIs.
- Update the owner lane and `lanes/00_master_ledger.md` after meaningful changes.

## Done criteria

- Implementation status: `locked`.
- Release requirement: `release-critical`.
- Related tests pass or a release blocker is explicitly recorded.
- Documentation and contracts remain aligned with current TuringResearch Plus naming.
