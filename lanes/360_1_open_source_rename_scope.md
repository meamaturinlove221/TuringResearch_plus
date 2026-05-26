# Round 360.1 - Open Source Rename Scope

Status: complete

## Objective

Lock the open source public naming scope after the v1.5 final handoff. The
public project name should be TuringResearch, while runtime compatibility names
remain until separate package, CLI, MCP, and import audits approve changes.

## Files

- `docs/open-source-rename-scope.md`
- `docs/turingresearch-public-naming-policy.md`
- `docs/public-name-migration-plan.md`
- `docs/public-name-risk-register.md`
- `docs/legacy-name-compatibility-policy.md`
- `lanes/360_1_open_source_rename_scope.md`
- `lanes/00_master_ledger.md`

## Public Naming Rules

- GitHub repo name target: `TuringResearch`.
- Public project name: TuringResearch.
- README title target: TuringResearch.
- Docs title target: TuringResearch.
- Release title target: TuringResearch.
- Package display name target: TuringResearch.

## Compatibility Boundary

- Python import compatibility may remain temporarily.
- Package distribution rename needs package availability and compatibility
  review.
- CLI and MCP names require a separate audit before any rename.
- This round does not publish PyPI, create a tag, publish a GitHub release, or
  create a GitHub repository.

## Validation

- Name integrity tests: passed.
- Public release hygiene focused check: passed.
- `python -m ruff check .`: passed.
- `python -m mypy src`: passed.
- `git diff --check`: passed with LF-to-CRLF working-copy warning only.
