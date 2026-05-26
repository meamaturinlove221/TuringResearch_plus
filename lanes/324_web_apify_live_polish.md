# Lane 324 - Web / Apify Live Polish

Round: 346.

Status: complete.

## Objective

Polish Web / Apify live optional documentation, example configuration, and
skipped tests without requiring or running live access.

## Files

- `docs/web-apify-live-optional-guide.md`
- `examples/apify_workflows/live_optional/`
- `tests/live/test_apify_live_skipped_by_default.py`
- `tests/contract/test_apify_live_env_policy.py`

## Result

Web / Apify live remains optional and disabled by default. Fake Apify tests
still run without a token.

## Safety Boundaries

- `APIFY_TOKEN` optional.
- Live disabled by default.
- No key in repo.
- No private scraping.
- No login bypass.
- No paywall bypass.
- No cookie storage.
