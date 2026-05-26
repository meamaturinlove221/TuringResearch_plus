---
name: turingresearch-fusion-literature-survey
description: Use when maintaining depth-gated literature survey workflows.
---

# TuringResearch Plus Skill: turingresearch-fusion-literature-survey

## Role

Maintain survey strategies, screening, evidence matrix, gap extraction, and dry-run export.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-fusion-literature-survey` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research_plus/survey/`

## Related contracts

- `contracts/fusion_workflows.yaml`

## Related lanes

- `lanes/04_yogsoth_fusion.md`

## Required tests

- `tests/unit/test_survey_models.py`
- `tests/unit/test_survey_depth_gate.py`
- `tests/unit/test_survey_strategies.py`
- `tests/unit/test_evidence_matrix.py`
- `tests/unit/test_gap_extractor.py`
- `tests/workflow/test_literature_survey_dry_run.py`

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

- `workflow`: scholar pipeline
- `when_to_use`: plan or review paper search priority, cached Markdown use,
  citation status, source fallback, and Scholar MCP usage.
- `inputs`: research question, known paper ids/URLs, cached Markdown, source
  priority policy, and fake/live config.
- `outputs`: source priority plan, tool list, usage guide, fallback decision,
  and citation/source review notes.
- `safety`: live Scholar access is optional and private; cached content is
  review context, not final evidence or paper conclusions.
- `non-goals`: no MinerU runtime, heavy OCR, automatic full paper download,
  paywall bypass, or final paper conclusion.
- `handoff`: record sources used, unresolved sources, fallback path, and human
  review requirements.
- `tests`: Scholar source priority, tool list, MCP usage, fallback policy, and
  workflow tests.
- `related_docs`: `docs/scholar-tool-list.md`,
  `docs/scholar-mcp-usage-guide.md`, `docs/paper-source-fallback-policy.md`.
