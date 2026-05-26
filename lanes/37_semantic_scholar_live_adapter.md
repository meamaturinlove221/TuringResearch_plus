# Lane 37: Semantic Scholar Live Adapter

Status: implemented as optional minimal live adapter.

## Scope

Round 56 adds the optional Semantic Scholar live adapter while preserving fake
mode as the default path.

## Implemented

- `SemanticScholarLiveAdapter`
- adapter cache helper with sha256 keys
- rate limit placeholder with typed errors
- live test opt-in helpers
- semantic graph live bridge
- `contracts/semantic_scholar_live.yaml`
- default-skipped live test

## Boundaries

- No default networking.
- No live test without `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`.
- No API key required for default tests.
- Live results are retrieved, not human-verified.
- No full-text download.
- No paper conclusion generation.

## Validation

- Semantic Scholar adapter focused unit tests: passed.
- Live optional test default behavior: skipped without explicit opt-in.
- Package import / public import / name integrity checks: passed.
- Contract tests: passed.
- Full pytest: passed with live tests deselected by default.
- `python -m mypy src`: passed.
- Focused ruff check: passed.
