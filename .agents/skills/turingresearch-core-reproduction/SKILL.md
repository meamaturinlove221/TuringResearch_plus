---
name: turingresearch-core-reproduction
description: Use when maintaining the minimal TuringResearch Core MCP tool loop.
---

# TuringResearch Plus Skill: turingresearch-core-reproduction

## Role

Maintain local-only Core tools and keep MCP wrappers thin over services.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-core-reproduction` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research/mcp_server.py`
- `src/turing_research/scholar/`
- `src/turing_research/web/`
- `src/turing_research/session/`

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

## Round 240 SOP Parity

- `workflow`: web fetch
- `when_to_use`: maintain local/fake web fetch, web content, Apify usage, MCP
  manifest checks, or source metadata surfaces.
- `inputs`: public URL or local fixture, source hygiene status, fake/live flags,
  cache policy, and provider-specific config.
- `outputs`: typed fetch/content result, source metadata, limitations, cache
  key/hash, and human-review boundary.
- `safety`: default mode must not network, bypass paywalls, fetch private
  content, store cookies, or require real keys.
- `non-goals`: no default live web access, no private scraping, no verified
  evidence claim from fetched content.
- `handoff`: record retrieval status, graceful skip behavior, source hygiene,
  and whether live mode was explicitly disabled.
- `tests`: web fetch, web content, Apify usage, MCP config, and name integrity
  tests.
- `related_docs`: `docs/web-fetching-usage-guide.md`,
  `docs/web-content-usage-guide.md`, `docs/apify-usage-guide.md`.
