# Round 194 - v1.0 Full Regression

Status: complete.

## Goal

Run the v1.0 full regression gate across API, CLI/MCP, demo, dashboard/export,
privacy, plugin safety, split readiness, and public launch release-candidate
surfaces.

## Output

- `docs/v1.0.0-full-regression-report.md`
- `docs/v1.0.0-regression-failures.md`
- `tests/workflow/test_v1_full_fake_replay.py`
- `tests/contract/test_v1_release_contracts.py`

## Coverage

- API freeze;
- namespace compatibility;
- CLI/MCP sanity;
- quickstart;
- public demo;
- security/privacy;
- plugin safety;
- dashboard/export;
- split readiness;
- public launch RC.

## Verification

- Full pytest: passed.
- `python -m mypy src`: passed.
- Name integrity: passed.
- Privacy gate: passed.
- Pre-push scan: passed with documented non-blocking policy wording.

## Boundaries

- No feature implementation unless needed to fix a failure.
- No network access.
- No release creation.
- No external repository push.
- No physical split execution.
