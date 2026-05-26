# Scholar / Web Demo

Status: fake/demo only.

This page summarizes the v1.3 Neocortica-Scholar and Neocortica-Web parity
surfaces.

## Scholar Surface

- `scholar.paper_searching`
- `scholar.paper_content`
- `scholar.paper_reference`
- `scholar.paper_reading`

These surfaces are fake/default and review-only. Fake citations are not marked
as verified.

## Web Surface

- `web.web_fetching`
- `web.web_content`
- `web.cache`
- `web.source_metadata`
- `web.apify_optional`

Web and Apify live paths are optional and disabled by default.

## MCP Boundary

The v1.3 MCP tool surface is documentation-contract-only. It maps tool names
and safety metadata but does not start a live MCP server.

## Boundaries

- no API key required for fake mode;
- no automatic full paper download;
- no paywall bypass;
- no private content scraping;
- no cookie storage;
- no automatic evidence promotion;
- human review required.
