# TulingResearch Plus Live Test Policy

Live tests are never part of the default TulingResearch Plus test path.

## Default Rule

Default tests must pass without:

- real network access
- real API keys
- live Semantic Scholar calls
- live arXiv calls
- live Apify calls
- live LLM calls
- cloud or GPU services

## Pytest Markers

Live tests must be marked:

- `live` for tests requiring live provider access
- `manual` for tests requiring a human-controlled environment

The default pytest configuration skips both markers.

## Environment Opt-In

Future live tests must require explicit environment variables, such as:

- `TULING_RESEARCH_ENABLE_LIVE_TESTS=1`
- `SEMANTIC_SCHOLAR_API_KEY`
- `ARXIV_API_KEY`
- `APIFY_TOKEN`
- `OPENAI_API_KEY`

Missing keys must skip live tests or return typed missing-key errors. Missing keys must not fail default tests.

## CI Policy

CI must not run live tests by default. Live tests can run only in a separate manual job with explicit credentials and maintainer approval.

## Fake Adapter Requirement

Every live adapter must have a fake adapter equivalent for:

- unit tests
- contract tests
- workflow dry-runs
- examples

Fake adapter behavior must remain stable even after a live adapter is added.

## Secrets Policy

Do not commit real API keys, tokens, provider secrets, private papers, or restricted datasets. Use `.env.example` for variable names only.

## Failure Policy

Live provider failures must not block the default release gate. Live failures are tracked as live/manual adapter issues unless they also break fake-mode, contracts, imports, or default tests.
