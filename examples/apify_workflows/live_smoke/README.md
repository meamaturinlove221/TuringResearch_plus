# Web / Apify Optional Live Smoke Example

Status: fake smoke example / live skipped by default.

This folder contains a public-safe Web / Apify smoke example. It uses fake
fixtures and does not require network access, `APIFY_TOKEN`, private scraping,
login bypass, paywall bypass, or cookie storage.

## Fake Smoke

The fake smoke path reads:

- `fake_web_apify_smoke.json`
- `expected_fake_smoke_report.md`

Expected behavior:

- fake smoke pass;
- `APIFY_TOKEN` optional;
- no token in repo;
- no private scraping;
- no login bypass;
- no paywall bypass;
- all output requires human review.

## Live Smoke

Live mode is skipped by default. A private live smoke requires all environment
values to be set outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_WEB_LIVE=1
TURINGRESEARCH_ENABLE_APIFY_LIVE=1
APIFY_TOKEN=<private local value>
```

If any value is missing, the live smoke test must skip rather than attempting
network access.

## Boundary

This example is not a live Apify result, not a private scraping workflow, not a
login bypass, and not observed research evidence.
