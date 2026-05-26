# Round 311 - Apify Fake / Live Integration Report

Status: completed.

Scope:

- Add an Apify fake/live integration report.
- Demonstrate fake Apify integration through existing templates and fake adapter.
- Confirm live Apify remains skipped by default.
- Do not call Apify or require `APIFY_TOKEN`.

Artifacts:

- `docs/apify-fake-live-integration-report.md`
- `tests/workflow/test_apify_fake_integration_report.py`
- `tests/live/test_apify_live_skipped_by_default.py`
- `examples/apify_workflows/fake_live_report/`

Safety:

- No live network by default.
- No token in examples.
- No login bypass.
- No paywall bypass.
- No private content scraping.
- No cookie storage.
- No automatic evidence promotion.
- Human review required.

Validation:

- Apify fake integration tests, explicit live skip behavior, privacy/security
  checks, targeted scans, large-file checks, and whitespace checks were run for
  Round 311.

Push:

- Not pushed from this workspace because the target branch is absent locally or
  not safe to push from the current dirty worktree.
