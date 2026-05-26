# TuringResearch Plus Name Audit Report

Round 38.5 updates the name audit after the global rename from the prior
incorrect naming system to TuringResearch.

## Canonical Names

- Project display name: TuringResearch Plus
- Repository root: `TuringResearch/TuringResearch_plus`
- Core package: `turing_research`
- Plus package: `turing_research_plus`
- MCP server: `turingresearch-plus`
- Skill prefix: `turingresearch-`

## Scan Scope

- Files scanned by integrity tests: repository `.py`, `.md`, `.yaml`, and `.toml` files.
- Python files scanned: `src/` and `tests/`.
- Ignored generated caches: `.git`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `__pycache__`, package egg-info.

## Findings

- Prior incorrect project-name terms are blocked outside the explicit rename checkpoint/report allowlist.
- Core and Plus package imports now use `turing_research` and `turing_research_plus`.
- MCP server and console entry points now use `turingresearch-plus`.
- Repo-scoped skills now use the `turingresearch-` prefix.
- External reference project names Neocortica and Yogsoth AI were not changed.

## Fixes Applied

- Renamed package directories to `turing_research*`.
- Renamed repo-scoped skill directories to `turingresearch-*`.
- Updated `pyproject.toml` package discovery and console scripts.
- Updated tests, docs, contracts, lanes, examples, and race files.
- Updated `tests/contract/test_name_integrity.py` to allow old terms only in the rename checkpoint/report files.

## Remaining Naming Risks

No known naming pollution remains outside the explicit rename checkpoint/report
allowlist. Future docs should use TuringResearch naming unless they are part of
an approved rename audit.
