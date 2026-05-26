# TuringResearch Plus Semantic Scholar Live Adapter

Status: v0.2 beta optional live adapter.

Round 56 adds an optional Semantic Scholar adapter while keeping fake mode as
the default. Importing the adapter does not start network work. Live calls only
run when a request explicitly sets `context.live_enabled = true`,
`context.dry_run = false`, and `SEMANTIC_SCHOLAR_API_KEY` is present.

## Supported Operations

- paper lookup by title query;
- paper lookup by Semantic Scholar paper id;
- batch paper lookup;
- references;
- citations;
- recommendations, minimal optional support;
- author lookup, minimal optional support.

## Default Behavior

Default tests and workflows use `FakeSemanticScholarAdapter`. Missing API keys
do not fail default tests. Live tests are marked `live` and skipped unless
`TURINGRESEARCH_ENABLE_LIVE_TESTS=1` is set.

## Cache And Rate Limit

The adapter uses sha256 cache keys through `build_adapter_cache_key`; raw query
text and URLs are not used as filenames. The current rate limit layer is a
placeholder that returns typed `rate_limited` errors instead of sleeping.

## Result Boundary

Live Semantic Scholar results are retrieval metadata only:

- `human_verified` remains false;
- results are not paper conclusions;
- full text is not downloaded;
- long paper text is not copied into repository artifacts;
- downstream workflows must still use EvidenceRef, source hygiene, and human
  review gates where needed.

## Environment

- `SEMANTIC_SCHOLAR_API_KEY`, optional for default use and required for live
  calls.
- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`, required before live tests are allowed.

## Modules

- `turing_research_plus.adapters.semantic_scholar.SemanticScholarLiveAdapter`
- `turing_research_plus.adapters.cache`
- `turing_research_plus.adapters.rate_limit`
- `turing_research_plus.adapters.live_test_markers`
- `turing_research_plus.semantic_graph.live_service.SemanticScholarLiveGraphService`

## Tests

- Unit tests cover models, fake adapter behavior, typed error mapping, cache
  policy, and rate limit placeholder behavior.
- `tests/live/test_semantic_scholar_live_optional.py` is explicitly marked
  `live` and skipped by default.
