# Web Content Extraction Fixtures

Round 310 adds local HTML fixtures for the `web_content` review path. The goal
is to make the Web demo easier to inspect without live network access.

## Fixture Path

`examples/web_demo/content_fixtures/`

Included fixtures:

- `project_page.html`: fake project page with overview, method, and artifact
  sections.
- `paper_abstract.html`: fake paper-style page with abstract, contribution,
  and limitation text.
- `noisy_navigation.html`: fake page with script/style/navigation noise.
- `expected_extraction.md`: human-readable extraction expectations.

## What The Tests Prove

- Local fixture HTML can be read by the existing fake-first `WebFetcher`.
- `web_content_from_fetch_result` can turn the fixture result into review text.
- Script and style text are not included in extracted review text.
- The fixture output stays unverified and requires human review.
- Extracted fixture text can be represented in a Web cache manifest entry.

## Safety Boundary

- No live network.
- No API key.
- No cookies.
- No login bypass.
- No paywall bypass.
- No private content scraping.
- No automatic evidence promotion.
- Human review is required.

These fixtures are demo evidence for extraction mechanics only. They are not
proof that a web source is correct, current, or claim-ready.
