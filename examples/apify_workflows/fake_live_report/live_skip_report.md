# Apify Live Skip Report

Status: skipped by default.

Live Apify integration is not part of default tests. It requires all private
opt-in controls to be configured outside the repository:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`
- `TURINGRESEARCH_ENABLE_APIFY_LIVE=1`
- `APIFY_TOKEN` set in a private local shell or secret manager

Default behavior:

- live tests are excluded by pytest default markers;
- fake integration tests require no token;
- no Apify request is sent;
- no fetched content is marked human verified;
- no output is promoted into evidence automatically.

This report is not proof that Apify live integration succeeded.
