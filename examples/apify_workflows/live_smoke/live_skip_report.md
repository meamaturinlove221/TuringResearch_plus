# Web / Apify Live Smoke Skip Report

Status: skipped by default.

## Default Skip Conditions

Live Web / Apify smoke must skip unless all of these are set outside the
repository:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`
- `TURINGRESEARCH_ENABLE_WEB_LIVE=1`
- `TURINGRESEARCH_ENABLE_APIFY_LIVE=1`
- `APIFY_TOKEN=<private local value>`

## Safety

- `APIFY_TOKEN` optional for fake/default;
- no token in repo;
- no private scraping;
- no login bypass;
- no paywall bypass;
- skipped live output is not observed evidence.
