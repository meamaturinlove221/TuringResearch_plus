# Workflow Missing Execution Paths

Status: completed.

Round: 260.

This document lists the workflow paths that are still missing after v1.2
reference parity.

## Missing Session Runtime Path

Current pieces:

- context pack manifest builder;
- archive safety checker;
- preflight checker;
- structured return manifest builder;
- metadata return verifier.

Missing:

- a single fake-first Session Runtime command/path that connects these steps;
- transfer runner abstraction;
- returned bundle checksum verification;
- proposed update review package;
- operator-facing report that says what can and cannot be ingested.

Do not add remote command execution to close this gap.

## Missing Scholar Runtime Path

Current pieces:

- source priority plan;
- tool list export;
- MCP usage guide;
- fallback policy.

Missing:

- a local fake Scholar workflow that accepts a paper query and returns the
  priority plan, cache policy, and review checklist together;
- visible no-key behavior for optional live providers;
- cached markdown fixture replay.

Do not add automatic paper downloads, paywall bypass, MinerU, or final
conclusions to close this gap.

## Missing Web Runtime Path

Current pieces:

- dry-run web fetching wrapper;
- web content review object;
- Apify usage guide and missing-token path.

Missing:

- a single web workflow demo that shows source metadata, cache policy, and
  review-only content extraction;
- optional live gate report;
- Apify template dry-run examples.

Do not enable default networking or store cookies to close this gap.

## Missing Research Catalog Execution Trace

Current pieces:

- campaign routing;
- strategy book;
- vault/ontology runners;
- stress-test runner;
- experiment runbook builder;
- docs skill map.

Missing:

- one deterministic trace that links a task description to a campaign, skills,
  vault updates, stress checks, experiment runbook, and proposed handoff;
- a machine-readable trace artifact for the public parity dashboard.

Do not add multi-agent runtime or LLM calls to close this gap.

## Missing Public Parity Dashboard Runtime Status

Current pieces:

- public reference parity dashboard JSON;
- docs-site page;
- v1.2 demo.

Missing:

- runtime status fields that distinguish `runnable`, `fake-runnable`,
  `docs-only`, `partial`, `blocked`, `deferred`, and `unsafe-by-default`;
- links from dashboard entries to the exact workflow tests or example fixtures.

Do not describe planned or fake outputs as observed.

## Missing Release-Level Replay

Current pieces:

- v1.2 full fake replay;
- security/privacy gate;
- release contracts.

Missing:

- v1.3 full original parity replay that proves the safe fake runtime path after
  the runtime gaps above are closed.

This should remain local, fake/default, and review-only.
