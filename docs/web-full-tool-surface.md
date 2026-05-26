# Web Full Tool Surface

Status: implemented.

Round: 273.

This round adds an operator-facing Web tool surface for v1.3
Neocortica-Web parity. It wraps the existing fake-first web fetch, content,
cache, metadata, and Apify guidance into a complete, testable surface.

## Tool Surface

| Tool | Module | Purpose | Default |
| --- | --- | --- | --- |
| `web.web_fetching` | `turing_research_plus.web_tools.web_fetching` | Fake/default public web fetching | fake/default |
| `web.web_content` | `turing_research_plus.web_tools.web_content` | Convert fetched or cached content into review context | review-only |
| `web.cache` | `turing_research_plus.web_tools.web_cache` | Inspect process-local cache status | local |
| `web.source_metadata` | `turing_research_plus.web_tools.source_metadata` | Build source metadata without marking content verified | review-only |
| `web.apify_optional` | `turing_research_plus.web.apify_usage_export` | Document optional Apify live usage and no-key behavior | disabled by default |

## What It Adds

- A public `turing_research_plus.web_tools` package.
- Stable request/result models for web fetching and web content review.
- Cache and source metadata review surfaces.
- A `WebFullToolSurface` catalog for docs and tests.
- Fake workflow tests across fetching, content, cache, metadata, and Apify
  usage guidance.

## Safety Boundary

- No default networking.
- No real API key required for fake mode.
- No cookie storage.
- No private content fetching.
- No paywall bypass.
- No automatic promotion to verified evidence.
- Optional Apify remains live opt-in only.
- Retrieved content is review context, not verified evidence.

## Relationship To Existing Web Layer

The new package is a thin tool surface over the existing web layer:

- `web_fetching` reuses the fake-first `WebFetcher`.
- `web_content` reuses fetched-content review conversion.
- `web_cache` reuses the process-local cache key/status behavior.
- `source_metadata` reuses the source metadata hashing helpers.
- `web.apify_optional` reuses the Apify usage guide.

The goal is parity of usable tool entry points, not a new browser or crawler.

## Validation

Run:

```powershell
python -m pytest tests/unit/test_web_tool_surface.py tests/unit/test_web_fetching_tool_surface.py tests/unit/test_web_content_tool_surface.py tests/workflow/test_web_full_tool_surface_fake.py -q
```
