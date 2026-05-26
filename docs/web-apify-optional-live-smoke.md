# Web / Apify Optional Live Smoke

Round: 374
Status: fake smoke ready / live skipped by default

## Objective

Define a Web / Apify optional live smoke path that keeps fake mode runnable by
default and keeps live mode skipped unless a maintainer explicitly opts in with
private environment variables.

This round does not call live Web or Apify services, require `APIFY_TOKEN`,
scrape private content, bypass login, bypass paywalls, store cookies, or write
live output as observed evidence.

## Default Fake Smoke

Default smoke uses committed fake fixtures only:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_WEB_LIVE=0
TURINGRESEARCH_ENABLE_APIFY_LIVE=0
APIFY_TOKEN=
```

Expected result:

- fake smoke pass;
- `APIFY_TOKEN` optional;
- no token in repo;
- no network required;
- no private scraping;
- no login bypass;
- no paywall bypass;
- all outputs require human review.

## Optional Live Smoke

Private live smoke requires all of the following outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_WEB_LIVE=1
TURINGRESEARCH_ENABLE_APIFY_LIVE=1
APIFY_TOKEN=<private local value>
```

If any flag or token is missing, the live smoke test must skip. Skipping is the
correct default behavior.

## Example Files

See `examples/apify_workflows/live_smoke/`:

- `README.md`
- `fake_web_apify_smoke.json`
- `expected_fake_smoke_report.md`
- `live_skip_report.md`

## Safety Rules

- live skipped by default;
- live requires explicit env;
- `APIFY_TOKEN` optional for fake/default;
- no token in repo;
- no private scraping;
- no login bypass;
- no paywall bypass;
- no cookie storage;
- no automatic Evidence Ledger write;
- no public claim from fake or skipped live output.

## Decision

Web / Apify optional live smoke is ready for fake/default review. It remains
NO-GO for default live networking.
