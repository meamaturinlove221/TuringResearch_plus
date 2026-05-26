# TuringResearch Plus Live Test Policy

Live tests are disabled by default and are never part of the default
TuringResearch Plus test path.

## Default Rule

Default tests must pass without:

- real network access;
- real API keys;
- live Semantic Scholar calls;
- live arXiv calls;
- live web search or fetch calls;
- live LLM calls;
- cloud or GPU services.

## Pytest Markers

Live tests must be marked:

- `live` for tests requiring live provider access;
- `manual` for tests requiring a human-controlled environment.

The default pytest configuration skips both markers.

## Environment Opt-In

Future live tests must require explicit environment variables, such as:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`
- `SEMANTIC_SCHOLAR_API_KEY`
- `APIFY_TOKEN`
- `OPENAI_API_KEY`

Missing keys must skip live tests or return typed missing-key errors. Missing
keys must not fail default tests.

## CI Policy

CI must run fake adapters only by default. Live tests can run only in a separate
manual job with explicit credentials and maintainer approval.

CI must not run live tests by default.

## Semantic Scholar Optional Live Test

`tests/live/test_semantic_scholar_live_optional.py` is marked `live`. It skips
unless both conditions are true:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`
- `SEMANTIC_SCHOLAR_API_KEY` is present

This test checks retrieval plumbing only. It does not verify paper claims and
does not download full text.

## Fake Adapter Requirement

Every live adapter must have a fake adapter equivalent for:

- unit tests;
- contract tests;
- workflow dry-runs;
- examples.

Fake adapter behavior must remain stable even after a live adapter is added.

## Result Verification Policy

Live results must include source metadata and retrieval time. Live results must
not automatically be marked human-verified. Human verification requires a
separate evidence or review step.

## Secrets Policy

Do not commit real API keys, tokens, provider secrets, private papers, or
restricted datasets. Use `.env.example` for variable names only.
