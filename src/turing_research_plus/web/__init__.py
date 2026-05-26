"""Optional public web fetch and Apify adapters.

The package is fake-first. Importing it never performs network access.
"""

from turing_research_plus.web.apify import ApifyAdapter
from turing_research_plus.web.apify_fake import FakeApifyAdapter
from turing_research_plus.web.apify_usage_export import (
    ApifyUsageGuide,
    build_apify_usage_guide,
    render_apify_usage_guide,
)
from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import WebFetchRequest, WebFetchResult
from turing_research_plus.web.web_content_tool import (
    WebContentToolResult,
    render_web_content_usage,
    web_content_from_cache_record,
    web_content_from_fetch_result,
)
from turing_research_plus.web.web_fetching_tool import (
    WebFetchingToolRequest,
    WebFetchingToolResult,
    render_web_fetching_usage,
    run_web_fetching_tool,
)

__all__ = [
    "ApifyAdapter",
    "ApifyUsageGuide",
    "FakeApifyAdapter",
    "WebContentToolResult",
    "WebFetchRequest",
    "WebFetchResult",
    "WebFetcher",
    "WebFetchingToolRequest",
    "WebFetchingToolResult",
    "build_apify_usage_guide",
    "render_apify_usage_guide",
    "render_web_content_usage",
    "render_web_fetching_usage",
    "run_web_fetching_tool",
    "web_content_from_cache_record",
    "web_content_from_fetch_result",
]
