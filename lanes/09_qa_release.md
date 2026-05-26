# Lane 09: QA Release

## Scope

Create packaging and quality configuration with unit tests.

## Outputs

- `pyproject.toml`
- `tests/unit/*.py`

## Status

Phase 1 complete. Unit tests pass with `python -m pytest`.

## Round 15B Update

2026-05-19: Completed QA + Public Release preparation for TuringResearch Plus.

Created release documentation:

- `docs/public-release-checklist.md`
- `docs/public-readme-draft.md`
- `docs/release-plan.md`
- `docs/examples.md`

Created fake-mode examples:

- `examples/vggt-human-prior-survey/`
- `examples/smplx-feature-adapter-hypothesis/`
- `examples/citation-graph-demo/`
- `examples/pdf-to-markdown-demo/`

Added contract and workflow release gates:

- Race public tool contract payloads.
- Paper public tool contract payloads.
- Release documentation and naming checks.
- Example fake-mode checks.
- Artifact Markdown and JSON serialization checks.
- PDF-to-Markdown fixture-style demo check.

Release gates verified:

- public tools have contract tests or coverage checks
- workflows have dry-run/fake-service tests
- tests require no real API keys
- README and public README draft include quickstart
- license compatibility and Source Hygiene are documented
- examples are fake mode
- artifacts serialize to Markdown and JSON
- paper draft is blocked without ExperimentReport
- Source Hygiene blocks non-public implementation
- Feature Capsule includes contract, skill, tests, and SOP graph outputs
