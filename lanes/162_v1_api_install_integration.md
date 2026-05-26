# Lane 162 - v1.0 API / Install Integration Gate

Status: integration gate complete.

Round: 181.

## Goal

Integrate the v1.0 scope, public API freeze, namespace compatibility, CLI/MCP
sanity, public quickstart, and demo/benchmark refresh into one release-hardening
gate.

## Outputs

- `docs/v1.0.0-api-install-integration-report.md`
- `docs/v1.0.0-api-install-known-limitations.md`
- `tests/workflow/test_v1_api_install_end_to_end_fake.py`
- `tests/contract/test_v1_api_install_contracts.py`
- `lanes/00_master_ledger.md`

## Checked

- public API tests pass;
- namespace tests pass;
- CLI/MCP config examples pass;
- quickstart fake test pass;
- demo refresh pass;
- no old project naming;
- no secrets;
- no raw data;
- no private local path;
- fake/live boundary remains explicit;
- plugin tools disabled by default;
- no observed fake result.

## Boundaries

- No feature implementation.
- No PyPI publish.
- No GitHub release.
- No network access.
- No real experiment execution.
- No unknown plugin execution.
- No final paper generation.
