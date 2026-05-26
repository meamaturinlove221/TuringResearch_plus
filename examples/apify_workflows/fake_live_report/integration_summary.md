# Apify Fake / Live Integration Summary

Round 311 validates the optional Apify integration shape without enabling live
network access.

Fake path:

- Uses existing Apify workflow templates.
- Uses the deterministic fake Apify adapter.
- Produces `dry-run` output.
- Requires human review.
- Marks `human_verified: false`.

Live path:

- Disabled by default.
- Skipped unless live tests and a private token are explicitly enabled.
- Must not bypass login, bypass paywalls, scrape private content, or store
  cookies.

Result:

Fake integration is demonstrable. Live integration remains optional and
private; it is not required for CI, public demos, or v1.4 production parity.
