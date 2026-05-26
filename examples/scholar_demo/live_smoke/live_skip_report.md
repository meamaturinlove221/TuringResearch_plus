# Scholar Live Smoke Skip Report

Status: skipped by default.

## Default Skip Conditions

Live Scholar smoke must skip unless all of these are set outside the
repository:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`
- `TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=1`
- `SEMANTIC_SCHOLAR_API_KEY=<private local value>`

## Safety

- no API key in repo;
- no paper download by default;
- no paywall bypass;
- no fake citation verified;
- skipped live output is not observed evidence.
