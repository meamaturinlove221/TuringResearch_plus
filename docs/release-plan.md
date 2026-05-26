# TuringResearch Plus Release Plan

## Release Scope

This release packages a Python MCP-first research workflow engine with deterministic local tests and fake-service workflows.

MCP server name: `turingresearch-plus`.

## Release Stages

1. Contract alignment for `core.*`, `pdf.*`, `graph.*`, `research.*`, `vault.*`, `context.*`, `race.*`, and `paper.*`.
2. Dry-run workflow validation for survey, North Star, Race Mode, PDF Markdown, and paper gates.
3. Public README and examples review.
4. Source Hygiene and license compatibility scan.
5. Final `pytest`, `ruff`, and `mypy` gates.

## Release Decision

Current status: release candidate after QA gates pass.

Known limits:

- No real external API calls in tests.
- Production deployment packaging is not part of this round.
- PDF conversion demo stays fixture/local-path based.

## Final Readiness Gates

- Name/import/contract integrity tests pass.
- MCP local stdio smoke tests pass.
- Examples run in fake mode or dry-run mode.
- Packaging entry points resolve locally.
- CI test/lint workflows are present.
- Public docs use TuringResearch Plus naming consistently.
