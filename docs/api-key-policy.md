# TuringResearch Plus API Key Policy

Status: active for beta planning.

TuringResearch Plus must not require API keys for default tests, examples, or
fake-mode workflows.

## Rules

- Do not commit real API keys.
- Do not print API keys in logs.
- Do not place API keys in examples.
- Use `.env.example` for variable names only.
- Default tests must pass when every live API key is missing.
- Live adapters must be disabled by default.
- Live tests must require explicit opt-in and credentials.
- Missing keys must produce a typed adapter error or skip live tests.

## Supported Environment Variable Names

- `SEMANTIC_SCHOLAR_API_KEY`
- `TURINGRESEARCH_ENABLE_LIVE_TESTS`
- `APIFY_TOKEN`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`

## Human Verification Boundary

A live adapter result is not human-verified evidence. It must carry source
metadata and retrieval time, then pass through the appropriate evidence,
source-hygiene, or human-review gate.

## Semantic Scholar

`SEMANTIC_SCHOLAR_API_KEY` is optional for normal use. Semantic Scholar live
tests also require `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`. Without that explicit
opt-in, default tests use fake adapters and do not touch the network.
