# Scholar Optional Live Smoke Example

Status: fake smoke example / live skipped by default.

This folder contains a public-safe Scholar smoke example. It uses fake fixtures
and does not require network access, API keys, paper downloads, MinerU, OCR, or
paywall bypass.

## Fake Smoke

The fake smoke path reads:

- `fake_smoke_input.json`
- `../fake_paper_content.md`
- `../fake_reference_report.md`

Expected behavior:

- fake smoke pass;
- no API key in repo;
- no paper download by default;
- no fake citation verified;
- all output requires human review.

## Live Smoke

Live mode is skipped by default. A private live smoke requires all environment
values to be set outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=1
SEMANTIC_SCHOLAR_API_KEY=<private local value>
```

If any value is missing, the live smoke test must skip rather than attempting
network access.

## Boundary

This example is not a verified citation report, not a paper download workflow,
and not observed research evidence.
