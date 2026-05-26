# Round 360.3 - README First Public Version

Status: complete

## Objective

Create and submit the first open-source-facing README with TuringResearch as
the only public project name.

## Files

- `README.md`
- `docs/readme-first-public-version-report.md`
- `docs/readme-public-section-checklist.md`
- `lanes/360_3_readme_first_public_version.md`
- `lanes/00_master_ledger.md`

## Decisions

- README uses TuringResearch as the public project name.
- Compatibility command, package, MCP, and import names remain documented as
  compatibility surfaces.
- ARIS remains deferred.
- README does not add public deployment URLs or split-repo URLs.

## Non-actions

- No release.
- No tag.
- No PyPI publish.
- No GitHub Pages deployment.
- No GitHub repository creation.
- No package, CLI, MCP, or import rename.

## Validation

- README checks: passed.
- Public name integrity: passed.
- Privacy gate: passed.
- Full test suite: passed (`2013 passed, 10 deselected`).
- `python -m ruff check .`: passed.
- `python -m mypy src`: passed.
- `git diff --check`: passed with LF-to-CRLF working-copy warning only.
