# TuringResearch Plus Agent Guide

TuringResearch Plus is developed as a single-window, single-repository, MCP-first research workflow engine. Parallel work is coordinated through `lanes/`, `contracts/`, and `.agents/skills/` in this repository.

## Naming

- Project display name: TuringResearch Plus
- Repository root: `TuringResearch/TuringResearch_plus`
- Core package: `turing_research`
- Plus package: `turing_research_plus`
- MCP server name: `turingresearch-plus`
- Skill names must start with `turingresearch-`

Do not create legacy reference-project directories, legacy reference-project package
names, or use any reference project name as this project name.

## Development Order

Every interface-facing change follows this order:

1. Update `contracts/`.
2. Add or update Pydantic models.
3. Add implementation behind a service protocol.
4. Add contract tests.
5. Update `lanes/00_master_ledger.md`.

## Architecture Rules

- Fusion workflows may depend on Core service protocols only, not Core internals.
- External APIs must be adapterized.
- Network tests must be mocked.
- Workflows must support `dry_run` and fake-service execution.
- Important outputs must be represented as `ResearchArtifact`.
- Conclusions must include `EvidenceRef`.
- Workflows must support `BudgetGate` and `StateLedger`.
- STDIO MCP mode must not write logs to stdout.

## Phase 1 Scope

Phase 1 creates the engineering skeleton only. It does not implement complex business logic, heavy OCR, production search, ranking, full agent orchestration, or paper drafting.
