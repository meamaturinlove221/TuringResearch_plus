---
name: tulingresearch-core-reproduction
description: Use when maintaining the minimal TulingResearch Core MCP tool loop.
---

# TulingResearch Plus Skill: tulingresearch-core-reproduction

## Role

Maintain local-only Core tools and keep MCP wrappers thin over services.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `tulingresearch-core-reproduction` or the matching TulingResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TulingResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/tuling_research/mcp_server.py`
- `src/tuling_research/scholar/`
- `src/tuling_research/web/`
- `src/tuling_research/session/`

## Related contracts

- `contracts/core_tools.yaml`
- `contracts/error_schema.yaml`

## Related lanes

- `lanes/02_core_reproduction.md`

## Required tests

- `tests/contract/test_core_health_check.py`
- `tests/unit/test_paper_content_service.py`
- `tests/unit/test_web_content_service.py`
- `tests/unit/test_session_registry.py`

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
