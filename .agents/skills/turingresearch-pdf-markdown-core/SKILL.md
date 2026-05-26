---
name: turingresearch-pdf-markdown-core
description: Use when maintaining local PDF inspection, conversion, cache lookup, or Markdown content tools.
---

# TuringResearch Plus Skill: turingresearch-pdf-markdown-core

## Role

Maintain fixture-safe local PDF to Markdown behavior without heavy OCR or real external APIs.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-pdf-markdown-core` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research/pdf/`
- `docs/pdf_markdown.md`

## Related contracts

- `contracts/pdf_markdown.yaml`
- `contracts/error_schema.yaml`

## Related lanes

- `lanes/03_pdf_markdown.md`

## Required tests

- `tests/unit/test_pdf_markdown_models.py`
- `tests/unit/test_pdf_markdown_pipeline.py`
- `tests/workflow/test_pdf_to_markdown_demo.py`

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
