# Test Maintenance Policy

Status: planning policy.

Round: 150.

This policy defines how the test suite should be maintained as TuringResearch
Plus grows across local dashboards, plugins, exports, compliance, case studies,
and paper-review workflows.

## Test Strategy

- Keep fake/default workflows runnable without network access.
- Keep live tests optional and explicitly marked.
- Add contract tests for public surfaces before treating them as release-ready.
- Add workflow tests for public demos, case studies, dashboards, exports, and
  replay paths.
- Prefer small focused tests for new behavior and integration gates for
  cross-module readiness.

## Required Test Layers

| Layer | Purpose | Cadence |
| --- | --- | --- |
| Unit tests | Validate local models, renderers, validators, scanners, gates, and report builders. | Every implementation round. |
| Contract tests | Protect package names, public imports, CLI/MCP metadata, schemas, plugin surfaces, and safety rules. | Every release gate and public-surface change. |
| Workflow tests | Exercise fake/default public demos, replay chains, case studies, and dashboards. | Every feature integration gate. |
| Security/privacy tests | Check secrets, private paths, raw data markers, unsafe permissions, and public demo safety. | Every RC and public demo/case-study change. |
| Type checks | Keep `python -m mypy src` passing or document known exceptions. | Every integration and release gate. |
| Lint checks | Keep focused `ruff check` passing for touched files or all files when practical. | Every implementation and release gate. |

## Regression Gate

Regression gates should fail or block release review when:

- old project naming appears in current public surfaces;
- fake/demo results are marked observed;
- live tests are required by default;
- optional backends fail instead of skipping gracefully;
- contract files drift from tests and docs;
- public demo outputs are missing;
- privacy or compliance reports show release blockers;
- plugin safety rules allow unsafe permissions without review.

## Test Coverage Proxy

TuringResearch Plus does not require a numeric line coverage target for every
planning round. Instead, each release should maintain coverage proxies:

- every new module has focused tests;
- every new contract has a contract test or integration gate;
- every public example has a workflow test;
- every release-sensitive surface has a privacy or quality gate;
- every optional dependency has a skip-path test.

## Test Data Policy

- Use fake/demo fixtures by default.
- Do not commit private project paths, raw datasets, credential-bearing logs, or
  licensed model payloads.
- Use tiny synthetic fixtures for safety tests when needed.
- Clearly allowlist intentional safety fixtures.
- Do not use real VGGT artifacts unless a later explicit local dogfooding round
  supplies reviewed public-safe outputs.

## Maintenance Tasks

- Remove stale tests when a feature is retired and migration is complete.
- Update tests when contracts or docs intentionally change.
- Keep test names aligned with release lanes and feature names.
- Avoid broad brittle assertions over historical docs when current public
  surfaces are the intended gate.
- Keep public demo and replay tests short enough for default local runs.
