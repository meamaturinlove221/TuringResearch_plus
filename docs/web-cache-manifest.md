# Web Cache Manifest

Round 309 adds a review-only cache manifest for the Web tool surface. The
manifest does not fetch pages. It records cache provenance for content that was
already produced by a fake, cache-only, or explicitly live workflow.

## Tracked Fields

- Source URL.
- Normalized URL.
- Fetch time.
- Content hash.
- Stable cache key.
- Retrieval status.
- Fake / cache-only / live status.
- Source type and provider.
- Human review boundary.

## Safety Boundary

- Fake mode remains the default.
- Live network is disabled by default.
- Cookie storage is disabled.
- Private content is blocked.
- Cache entries are not human verified by default.
- Cache manifest entries do not become observed evidence.
- Human review is required before using cached content in claims.

## Intended Use

Use `build_web_cache_manifest_entry` when a fake or reviewed Web workflow has
content and needs a stable manifest row:

```python
from turing_research_plus.web_tools import build_web_cache_manifest_entry

entry = build_web_cache_manifest_entry(
    source_url="https://example.com/project?utm_source=demo",
    content="cached demo content",
)
```

Use `build_web_cache_manifest` to collect entries into a release-reviewable
manifest. The manifest is documentation and review metadata only; it is not a
fetcher, not a crawler, and not a source-verification engine.
