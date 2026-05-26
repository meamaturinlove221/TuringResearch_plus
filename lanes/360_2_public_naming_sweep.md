# Round 360.2 - Public Naming Sweep

Status: complete

## Objective

Sweep public-facing files so the open source display name is TuringResearch
while package, CLI, MCP, and Python import compatibility remains intact.

## Files

- `docs/public-naming-sweep-report.md`
- `docs/public-facing-old-name-inventory.md`
- `docs/public-name-replacement-log.md`
- `tests/contract/test_public_name_integrity_turingresearch.py`
- `lanes/360_2_public_naming_sweep.md`
- `lanes/00_master_ledger.md`

## Scope

Updated public-facing text in:

- README;
- current docs entry points;
- docs-site manifest paths;
- examples and public demo text;
- split-ready and split-manual package text;
- MCP example display description;
- package display description;
- changelog display prose.

## Compatibility Boundary

Retained:

- `turingresearch-plus`;
- `turingresearch-plus-mcp`;
- `turing_research_plus`;
- `src/turing_research_plus/`.

These are compatibility names, not the public brand.

## Non-actions

- No Python import compatibility was removed.
- No package distribution rename was performed.
- No CLI or MCP command was renamed.
- No PyPI release, tag, GitHub release, GitHub repo creation, or deployment was
  performed.
- No fake GitHub URL was added.

## Validation

- Public name integrity tests: passed.
- Name integrity tests: passed.
- Docs deployment dry-run, release bundle, preflight, and sprint-gate tests:
  passed.
- Local install, package metadata, VGGT public case, and split-pack freshness
  focused checks: passed.
- `python -m ruff check .`: passed.
- `python -m mypy src`: passed.
- `git diff --check`: passed with only LF-to-CRLF working-copy warning.
