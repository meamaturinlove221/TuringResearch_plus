# Apify Live Optional Example

Status: example only / no token in repo.

This folder documents the private opt-in shape for Web / Apify live mode. It
does not contain credentials and does not require live mode for normal tests.

## Fake Default

Use fake mode unless you are deliberately testing private live access:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_WEB_LIVE=0
TURINGRESEARCH_ENABLE_APIFY_LIVE=0
APIFY_TOKEN=
```

## Private Live Shape

If a maintainer wants to test live Web / Apify locally, configure this outside
the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_WEB_LIVE=1
TURINGRESEARCH_ENABLE_APIFY_LIVE=1
APIFY_TOKEN=<private local value>
```

## Safety

- `APIFY_TOKEN` optional;
- no token in repo;
- live disabled by default;
- no private scraping;
- no login bypass;
- no paywall bypass;
- no cookie storage;
- live output remains review context.
