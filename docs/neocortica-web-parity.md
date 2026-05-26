# Neocortica Web Parity

Status: v1.2 parity implementation.

Round: 238.

This round aligns TuringResearch with stable Web reference ideas: explicit
`web_fetching` and `web_content` user-facing surfaces, optional Apify live
usage, cache/provenance policy, source metadata, MCP fake/live boundaries, and
no-key graceful skip behavior.

The implementation is fake-first and review-only. It does not add default
network access, paywall bypass, private content fetching, cookie storage, or
any committed real API key.

## Implemented

- `web_fetching` wrapper around the existing fake/default web fetch adapter.
- `web_content` wrapper for already fetched or cached content.
- Apify usage guide export for optional live workflows.
- v1.2 Web parity contract and fake workflow tests.
- Public usage guides for web fetching, web content, and Apify.

## Web Fetching

`web_fetching` is the user-facing fetch surface. Defaults are conservative:

- `dry_run: true`
- `live_enabled: false`
- `default_network: false`
- `stores_cookies: false`
- `requires_api_key: false`
- `requires_human_review: true`

Private or restricted source hygiene returns a blocked result instead of
fetching content.

## Web Content

`web_content` turns fetched or cached content into review context with source
metadata and provenance fields. It keeps:

- `human_verified: false`
- `requires_human_review: true`
- content hash and cache key
- source hygiene status
- limitations

Retrieved or cached content is not automatically evidence and must not be
converted into paper claims without review.

## Apify Optional Live

Apify remains optional live infrastructure:

- live access is disabled by default;
- missing `APIFY_TOKEN` returns a typed missing-token result;
- live tests require explicit private opt-in;
- public docs and tests do not require real credentials.

## MCP Config Parity

The committed `.mcp.example.json` style remains fake/default:

- server name: `turingresearch-plus`;
- command: `turingresearch-plus-mcp`;
- live tests disabled by default;
- Web / Apify live adapters disabled by default;
- credential fields blank;
- plugin tools disabled by default.

## Explicit Non-goals

- No default networking.
- No paywall bypass.
- No private content fetching.
- No cookie storage.
- No real key in repository files.
- No automatic conversion from web content to verified evidence.
- No final paper conclusion generation.

## Tests

- `tests/unit/test_web_fetching_tool.py`
- `tests/unit/test_web_content_tool.py`
- `tests/unit/test_apify_usage_export.py`
- `tests/workflow/test_neo` `cortica_web_parity_fake.py`
