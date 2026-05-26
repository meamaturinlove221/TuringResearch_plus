# Apify Adapter

Status: implemented minimal.

The Apify Adapter is an optional live adapter behind the web retrieval surface.
It is disabled by default and has a deterministic fake adapter for default
tests.

## Behavior

- Default path: `FakeApifyAdapter`.
- Live path: requires `live_enabled=True`, `dry_run=False`, and `APIFY_TOKEN`.
- Live tests: skipped unless `TURINGRESEARCH_ENABLE_LIVE_TESTS=1` and
  `APIFY_TOKEN` exists.
- Missing token returns a typed error instead of failing default tests.

## Output

`ApifyRunResult` records:

- optional `actor_id`
- optional `run_id`
- `status`
- `input`
- `output_items`
- `retrieved_at`
- warnings
- typed errors
- `requires_human_review`

## Safety

- Do not bypass login or paywalls.
- Do not fetch restricted or private content.
- Do not store API tokens in fixtures or cache.
- Do not mark fetched content as human verified.
- Do not convert fetched content into final research claims.

## VGGT Use

Future VGGT workflows may use Apify for public project pages or README-like
pages when simple HTTP fetch is insufficient. This remains optional and does not
replace real paper review.
