# Apify Adapter Plan

Status: v0.3 Sprint 3 design draft.

The Apify Adapter is a future optional live implementation behind the Web Fetch
Adapter family. It should be useful for public pages where a simple HTTP fetch
is not enough, but it must remain opt-in and source-hygiene gated.

## Planned Contract

`ApifyAdapter` should support:

- public web page fetch;
- optional search/discovery actor;
- run id metadata;
- rate limit policy;
- retry and timeout policy;
- cache integration;
- typed provider errors;
- fake adapter equivalent.

## Environment

- `APIFY_TOKEN` is optional.
- Live tests require `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`.
- CI defaults to fake adapters only.
- `.mcp.json` or `.codex/config.example.toml` may document env variable names,
  but real tokens must never be committed.

## Output Metadata

Apify live outputs must record:

- provider: `apify`;
- actor or endpoint label;
- source URL;
- retrieval time;
- content hash;
- run id when available;
- `human_verified: false`.

## Safety

- Do not bypass login.
- Do not bypass paywalls.
- Do not fetch restricted or private content.
- Do not crawl private repositories.
- Do not store secrets in cache.
- Do not auto-convert fetched content into final research claims.

## Testing

Default tests:

- fake Apify adapter only;
- no `APIFY_TOKEN`;
- no network;
- deterministic fixture content.

Optional live tests:

- marked `live`;
- skipped unless `TURINGRESEARCH_ENABLE_LIVE_TESTS=1` and `APIFY_TOKEN` exists;
- verify retrieval plumbing only, not truth of claims.

## Upstream Learning

Neocortica-Web demonstrates that a REST client, MCP server entry, and `.mcp.json`
env block pattern can be useful. TuringResearch should adopt the architecture
idea and test discipline, not copy upstream code.
