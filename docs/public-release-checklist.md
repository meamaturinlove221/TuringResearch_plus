# TuringResearch Plus Public Release Checklist

## Gates

- [x] Project name is TuringResearch Plus.
- [x] Python packages are `turing_research` and `turing_research_plus`.
- [x] MCP server name is `turingresearch-plus`.
- [x] Public tools have contract tests or contract coverage checks.
- [x] Workflows have dry-run or fake-service tests.
- [x] No real API key or live network is required for tests.
- [x] Public README draft has quickstart.
- [x] License compatibility and Source Hygiene rules are documented.
- [x] Examples run in fake mode.
- [x] Artifacts serialize to Markdown and JSON in tests.
- [x] PDF to Markdown demo uses fixture-style local input.
- [x] Paper pipeline blocks draft without ExperimentReport.
- [x] Source Hygiene blocks non-public idea implementation.
- [x] Feature Capsule contains contract, skill, tests, and SOP graph outputs.
- [x] `CHANGELOG.md` exists and follows Keep a Changelog headings.
- [x] `VERSION` is `0.1.0`.
- [x] v0.1.0 release notes, feature list, limitations, and upgrade plan are present.
- [x] Release candidate report recommends GO for release preparation.

## Validation Commands

```powershell
python -m pytest
python -m ruff check .
python -m mypy src
```

## Remaining Public Release Notes

- Production API adapters remain outside the default test path.
- Heavy OCR and complex paper layout understanding are not part of this release.
- Public examples are deterministic fake-mode workflows.
- Public release still requires final human review before tagging or publication.
