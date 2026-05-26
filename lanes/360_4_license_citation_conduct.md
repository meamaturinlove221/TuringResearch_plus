# Round 360.4 - License / Citation / Conduct Decision

Status: complete

## Objective

Prepare public repository governance files for human review before any open
source release.

## Files

- `LICENSE`
- `CITATION.cff`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `docs/open-source-license-decision.md`
- `docs/open-source-compliance-checklist.md`
- `lanes/360_4_license_citation_conduct.md`
- `lanes/00_master_ledger.md`

## Decisions

- Current license remains proprietary and consistent with `pyproject.toml`.
- Open source license choice requires later human approval.
- CITATION metadata uses TuringResearch as the public project name.
- Security guidance tells users not to submit secrets or private data in public
  issues.
- Contributing guidance preserves fake/live boundaries and no-private-data
  requirements.

## Non-actions

- No legal advice.
- No open source license selected.
- No upstream license text copied.
- No PyPI publication.
- No GitHub release publication.
- No tag creation.

## Validation

- License/docs checks: passed.
- Public name integrity: passed.
- Public release hygiene and security/privacy checks: passed.
- Full test suite: passed (`2013 passed, 10 deselected`).
- `python -m ruff check .`: passed.
- `python -m mypy src`: passed.
- `git diff --check`: passed with LF-to-CRLF working-copy warning only.
