# Lane 216 - Neocortica Web Parity

Status: completed.

Round: 238.

## Goal

Align stable Web reference ideas with TuringResearch's fake-first web fetch,
web content, Apify, cache, source metadata, and MCP configuration boundaries.

## Implemented

- Public-safe `web_fetching` tool wrapper.
- Review-only `web_content` tool wrapper.
- Apify optional live usage guide export.
- v1.2 Web parity contract.
- Fake/default Web parity workflow tests.

## Outputs

- `src/turing_research_plus/web/web_fetching_tool.py`
- `src/turing_research_plus/web/web_content_tool.py`
- `src/turing_research_plus/web/apify_usage_export.py`
- `contracts/neocortica_web_parity.yaml`
- `docs/neo` `cortica-web-parity.md`
- `docs/web-fetching-usage-guide.md`
- `docs/web-content-usage-guide.md`
- `docs/apify-usage-guide.md`

## Explicit Non-goals

- No default networking.
- No paywall bypass.
- No private content fetching.
- No cookie storage.
- No committed real key.
- No automatic conversion from web content to verified evidence.

## Safety

- No upstream code was copied.
- Live Web / Apify paths remain opt-in only.
- Missing Apify token returns a graceful typed skip.
- Fetched or cached web content remains review context and requires human
  review.
