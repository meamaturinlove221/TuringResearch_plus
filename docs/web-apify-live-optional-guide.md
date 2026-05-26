# Web / Apify Live Optional Guide

Status: optional live polish.

Round: 346.

Web and Apify live mode is optional, private, and disabled by default. Fake Web
and Apify tests must continue to run without a token, network access, private
scraping, login bypass, or cookie storage.

## Default Fake Mode

Default mode is fake:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_WEB_LIVE=0
TURINGRESEARCH_ENABLE_APIFY_LIVE=0
APIFY_TOKEN=
```

`APIFY_TOKEN` is optional. It is not required for fake/default tests.

## Optional Live Mode

Private live mode requires explicit opt-in outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_WEB_LIVE=1
TURINGRESEARCH_ENABLE_APIFY_LIVE=1
APIFY_TOKEN=<private local value>
```

Do not commit real values. Do not paste real values into docs, examples, test
fixtures, logs, reports, cache manifests, or dashboard outputs.

## Test Policy

- fake Web and Apify tests run by default;
- live Web and Apify tests are skipped by default;
- live Apify tests require explicit env opt-in and a private token;
- live Web/Apify output remains review context;
- live Web/Apify output is not observed evidence.

## Safety Boundaries

- no live network by default;
- no key in repo;
- no private scraping;
- no login bypass;
- no paywall bypass;
- no cookie storage;
- no automatic Evidence Ledger write;
- no automatic claim verification.

## Example

See `examples/apify_workflows/live_optional/README.md` for a local private
configuration shape with blank placeholders only.
