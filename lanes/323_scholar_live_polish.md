# Lane 323 - Scholar Live Polish

Round: 345.

Status: complete.

## Objective

Polish Scholar live optional documentation, example configuration, and skipped
tests without requiring or running live access.

## Files

- `docs/scholar-live-optional-guide.md`
- `examples/scholar_demo/live_optional/`
- `tests/live/test_scholar_live_skipped_by_default.py`
- `tests/contract/test_scholar_live_env_policy.py`

## Result

Scholar live remains optional and disabled by default. Fake tests still run
without an API key.

## Safety Boundaries

- Live disabled by default.
- Explicit env required.
- No key in repo.
- Fake tests always pass.
- No paper download by default.
- No paywall bypass.
- No fake citation marked verified.
