# Web Fetch Adapter Plan

Status: v0.3 Sprint 3 design draft.

TuringResearch Plus will add a Web Fetch Adapter after the current scholar and
handoff work stabilizes. The adapter is for public, source-hygiene-safe pages
such as paper project pages, GitHub README files, method pages, and arXiv HTML
pages. It is not a bypass tool and it does not replace real paper reading.

## Adapter Surface

Planned adapters:

- `WebFetchAdapter`
- `WebContentAdapter`
- `ApifyAdapter`
- `FakeWebFetchAdapter`
- `FakeWebContentAdapter`
- `FakeApifyAdapter`

Proposed tools:

- `web.fetch`
- `web.content`
- `web.search_optional`
- `web.apify_run_optional`

These are proposed v0.3 tools only. They are not part of the current public MCP
tool freeze.

## Default Behavior

- Default workflows do not touch the network.
- Fake adapters remain the default.
- Live tests are skipped by default.
- `APIFY_TOKEN` is optional and must not be required by default tests.
- Missing API keys must produce typed errors or skipped live tests.

## Source Metadata

Every fetched content item must record:

- `source_url`
- `retrieval_time`
- `content_hash`
- provider
- status
- `human_verified: false`

Live retrieval means retrieved, not verified.

## Cache Policy

The adapter should cache normalized public content by hashed URL and request
parameters. Cache records should include:

- content hash;
- retrieval time;
- source URL;
- adapter name;
- content type;
- source hygiene status;
- expiration or refresh policy.

Raw URLs must not be used as filenames.

## Safety Policy

- Do not fetch restricted content.
- Do not bypass login, paywall, robots-like restrictions, or access controls.
- Do not scrape private repositories.
- Do not store API tokens in content cache.
- Do not treat fetched web content as human-verified evidence.

## VGGT Use

Future VGGT workflows can use this adapter for:

- paper project pages;
- GitHub README files;
- method pages;
- arXiv HTML pages;
- public release notes.

These pages can seed method cards, collision notes, or advisor packs, but they
do not automatically become final claims.

## Non-Goals

- No live adapter implementation in this round.
- No Apify call in this round.
- No network access in this round.
- No upstream code copying.
- No default live web search.
