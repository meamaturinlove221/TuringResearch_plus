"""Operator-facing Web tool surfaces for v1.3 parity."""

from turing_research_plus.web_tools.cache_manifest import (
    WebCacheLiveStatus,
    WebCacheManifest,
    WebCacheManifestEntry,
    build_web_cache_manifest,
    build_web_cache_manifest_entry,
    manifest_entry_from_cache_record,
)
from turing_research_plus.web_tools.source_metadata import (
    WebSourceMetadataSurfaceReport,
    build_web_source_metadata_report,
)
from turing_research_plus.web_tools.tool_surface import (
    WebFullToolSurface,
    WebToolSurfaceEntry,
    build_web_full_tool_surface,
    render_web_full_tool_surface,
)
from turing_research_plus.web_tools.url_normalization import (
    NormalizedUrl,
    UrlNormalizationRequest,
    normalize_url,
    normalize_url_string,
    url_cache_key,
)
from turing_research_plus.web_tools.web_cache import (
    WebCacheSurfaceReport,
    inspect_web_cache,
)
from turing_research_plus.web_tools.web_content import (
    WebContentSurfaceRequest,
    WebContentSurfaceResult,
    run_web_content_surface,
)
from turing_research_plus.web_tools.web_fetching import (
    WebFetchingSurfaceRequest,
    WebFetchingSurfaceResult,
    run_web_fetching_surface,
)

__all__ = [
    "WebCacheSurfaceReport",
    "WebCacheLiveStatus",
    "WebCacheManifest",
    "WebCacheManifestEntry",
    "WebContentSurfaceRequest",
    "WebContentSurfaceResult",
    "WebFetchingSurfaceRequest",
    "WebFetchingSurfaceResult",
    "WebFullToolSurface",
    "WebSourceMetadataSurfaceReport",
    "WebToolSurfaceEntry",
    "NormalizedUrl",
    "UrlNormalizationRequest",
    "build_web_cache_manifest",
    "build_web_cache_manifest_entry",
    "build_web_full_tool_surface",
    "build_web_source_metadata_report",
    "inspect_web_cache",
    "manifest_entry_from_cache_record",
    "normalize_url",
    "normalize_url_string",
    "render_web_full_tool_surface",
    "run_web_content_surface",
    "run_web_fetching_surface",
    "url_cache_key",
]
