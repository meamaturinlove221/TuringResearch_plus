# Lane 311 - Docs Site Build Hardening

Status: completed.

Round: 333.

## Goal

Harden the local docs-site builder so it is closer to deployable, without
deploying it.

## Scope

- Broken link report.
- Missing page report.
- Orphan page report.
- Nav validation.
- Static export manifest.
- No private path scan.

## Deliverables

- `src/turing_research_plus/docs_site/link_checker.py`
- `src/turing_research_plus/docs_site/build_report.py`
- `src/turing_research_plus/docs_site/static_export.py`
- `contracts/docs_site_build_hardening.yaml`
- `tests/unit/test_docs_site_link_checker.py`
- `tests/unit/test_docs_site_build_report.py`
- `tests/unit/test_docs_site_static_export.py`
- `tests/workflow/test_docs_site_build_hardening.py`
- `docs/docs-site-build-hardening.md`
- `docs-site/build_report.md`

## Safety

- No deployment.
- No live network.
- No analytics.
- No private path publication.
- No provider secrets.
- Human review required before any future public publication.

## Validation

- Docs-site hardening tests passed.
- Existing docs-site builder tests passed.
- Privacy/security and public hygiene checks passed.
- Pre-push checks completed for the Round 333 files.
