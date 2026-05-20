# TulingResearch Plus Name Audit Report

Round 17 audited repository naming across `.py`, `.md`, `.yaml`, and `.toml` files before the `v0.1.0` release candidate freeze.

## Canonical Names

- Project display name: TulingResearch Plus
- Repository root: `TulingResearch/TulingResearch_plus`
- Core package: `tuling_research`
- Plus package: `tuling_research_plus`
- MCP server: `tulingresearch-plus`
- Skill prefix: `tulingresearch-`

## Scan Scope

- Files scanned by integrity tests: 334 text/config/source files.
- Python files scanned: 244.
- Included extensions: `.py`, `.md`, `.yaml`, `.toml`.
- Ignored generated caches: `.git`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `__pycache__`, package egg-info.

## Findings

- Legacy plus-slug project directory references: none remaining.
- Legacy underscore package references: none remaining.
- Legacy source package path references: none remaining.
- Legacy import references: none remaining.
- Legacy doubled-plus project-name references: none remaining.
- Legacy skill-name prefix references: none remaining.

The only permitted reference-project naming remains ordinary `Neocortica` references in reference/inspiration contexts and `Yogsoth AI` references in module-audit documentation.

## Fixes Applied

- Reworded `AGENTS.md` to describe forbidden legacy reference-project names without spelling those names directly.
- Added `tests/contract/test_name_integrity.py` to lock project naming, package naming, MCP server naming, and import naming.

## Remaining Naming Risks

No known naming pollution remains. Future docs should avoid writing forbidden legacy slug/package strings directly, even in "do not use" sentences, because release integrity tests now scan all repository text.
