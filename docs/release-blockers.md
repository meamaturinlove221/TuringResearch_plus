# TulingResearch Plus Release Blockers

Date: 2026-05-20

## Current Status

No active blocker after final Round 23 validation.

## Active Blockers

None.

## Watch Items

- Contract-only tools are intentionally planned after `v0.1.0` and must not be advertised as live capabilities.
- Live API adapters require explicit future configuration and tests marked `live` or `manual`.
- Heavy OCR, complex PDF layout parsing, and full paper automation remain outside the release candidate.

## Resolution Rule

Any failing default test, naming integrity failure, contract/docs drift, unsafe source handling, or paper draft fabrication risk becomes a release blocker.

## Final Round 23 Validation

- `python -m pytest`: 301 passed.
- `python -m ruff check .`: passed.
- `python -m mypy src`: passed.
- Forbidden naming scan: no hits.

Release blocker status: clear.
