# Apify Fake / Live Integration Report

Round 311 aligns the optional Apify surface with a fake-first integration
report. It keeps live Apify disabled by default.

## Result

- Fake integration: pass.
- Live integration: skipped by default.
- Token required for private live use: `APIFY_TOKEN`.
- Default network use: false.
- Human review required: true.

## Fake Integration

The fake path uses:

- `examples/apify_workflows/project_page_fetch.yaml`
- `examples/apify_workflows/search_result_fetch.yaml`
- `examples/apify_workflows/content_extract.yaml`
- `turing_research_plus.web.apify.FakeApifyAdapter`

The fixture report lives at:

`examples/apify_workflows/fake_live_report/`

It records a deterministic `dry-run` result and marks output as not human
verified.

## Live Integration Boundary

Live Apify integration is optional and private. It is skipped unless all of the
following are configured outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_APIFY_LIVE=1
APIFY_TOKEN=<private local value>
```

Do not commit tokens or live outputs.

## Safety Boundary

- no live network by default;
- no token in examples;
- no login bypass;
- no paywall bypass;
- no private content scraping;
- no cookie storage;
- no automatic evidence promotion;
- fake/live output remains review context until human verification.

This report is not proof that Apify live integration succeeded.
