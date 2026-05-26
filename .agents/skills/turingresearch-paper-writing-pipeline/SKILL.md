---
name: turingresearch-paper-writing-pipeline
description: Use when defining TuringResearch Plus paper writing and draft workflow boundaries.
---

# TuringResearch Plus Skill: turingresearch-paper-writing-pipeline

## Role

Maintain paper draft gates, missing evidence reports, section readiness, no-fabrication rules, and LaTeX export.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-paper-writing-pipeline` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research_plus/paper/paper_writer.py`
- `src/turing_research_plus/paper/latex_export.py`
- `paper/draft/`

## Related contracts

- `contracts/paper_pipeline.yaml`

## Related lanes

- `lanes/08_paper_pipeline.md`

## Required tests

- `tests/unit/test_paper_writer.py`
- `tests/unit/test_paper_gate.py`
- `tests/unit/test_latex_export.py`
- `tests/contract/test_paper_tools_contract.py`

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

- `workflow`: advisor pack
- `when_to_use`: package review material, paper scaffold, related work notes,
  draft beta outputs, or advisor-facing Markdown/PDF/PPTX plans.
- `inputs`: evidence ledger, artifact audit, route plan, related work notes,
  paper draft package, and known limitations.
- `outputs`: advisor pack, missing evidence report, unsafe claim report,
  citation status, and paper outline or draft beta package.
- `safety`: do not write final papers, fabricate results, bypass human review,
  or present fake/demo evidence as observed.
- `non-goals`: no camera-ready paper, no automatic conclusion, no automatic
  paper download, no claim beyond evidence.
- `handoff`: record unresolved evidence, blocked result sections, citation
  status, and required advisor review.
- `tests`: advisor pack, paper draft assembly, claim guard, citation status,
  and workflow tests.
- `related_docs`: `docs/paper-draft-assembly-beta.md`,
  `docs/v1.1.0-paper-writing-beta-scope.md`, `docs/interview-demo-walkthrough.md`.
