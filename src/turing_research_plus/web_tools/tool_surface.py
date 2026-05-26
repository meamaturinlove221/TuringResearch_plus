"""Web full tool surface catalog."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class WebToolSurfaceEntry(BaseModel):
    """One Web tool-surface entry."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = Field(min_length=1)
    module: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    default_mode: str = "fake/default"
    optional_live: bool = False
    requires_api_key: bool = False
    stores_cookies: bool = False
    fetches_private_content: bool = False
    bypasses_paywall: bool = False
    promotes_to_verified_evidence: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe web defaults are enabled."""

        return (
            self.requires_api_key
            or self.stores_cookies
            or self.fetches_private_content
            or self.bypasses_paywall
            or self.promotes_to_verified_evidence
            or not self.requires_human_review
        )


class WebFullToolSurface(BaseModel):
    """Review-only catalog for the v1.3 Web full tool surface."""

    model_config = ConfigDict(extra="forbid")

    surface_id: str = "web-full-tool-surface-v1.3"
    status: str = "implemented"
    tools: list[WebToolSurfaceEntry] = Field(default_factory=list)
    fake_mode_default: bool = True
    live_tests_skipped_by_default: bool = True
    default_network: bool = False
    stores_cookies: bool = False
    paywall_bypass_allowed: bool = False
    private_content_fetching_allowed: bool = False
    automatic_evidence_promotion: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe surface behavior is enabled."""

        return (
            not self.fake_mode_default
            or not self.live_tests_skipped_by_default
            or self.default_network
            or self.stores_cookies
            or self.paywall_bypass_allowed
            or self.private_content_fetching_allowed
            or self.automatic_evidence_promotion
            or not self.requires_human_review
            or any(tool.release_blocker for tool in self.tools)
        )


def build_web_full_tool_surface() -> WebFullToolSurface:
    """Build the v1.3 Web tool-surface catalog."""

    return WebFullToolSurface(
        tools=[
            WebToolSurfaceEntry(
                tool_name="web.web_fetching",
                module="turing_research_plus.web_tools.web_fetching",
                purpose="Fake/default public web fetching surface.",
            ),
            WebToolSurfaceEntry(
                tool_name="web.web_content",
                module="turing_research_plus.web_tools.web_content",
                purpose="Convert fetched or cached content into review context.",
            ),
            WebToolSurfaceEntry(
                tool_name="web.cache",
                module="turing_research_plus.web_tools.web_cache",
                purpose="Inspect process-local cache status.",
            ),
            WebToolSurfaceEntry(
                tool_name="web.source_metadata",
                module="turing_research_plus.web_tools.source_metadata",
                purpose="Build source metadata without marking content verified.",
            ),
            WebToolSurfaceEntry(
                tool_name="web.apify_optional",
                module="turing_research_plus.web.apify_usage_export",
                purpose="Document optional Apify live usage and no-key behavior.",
                optional_live=True,
            ),
        ]
    )


def render_web_full_tool_surface(surface: WebFullToolSurface) -> str:
    """Render the Web tool surface as Markdown."""

    lines = [
        "# Web Full Tool Surface",
        "",
        f"- Surface ID: `{surface.surface_id}`",
        f"- Status: `{surface.status}`",
        f"- Fake mode default: `{str(surface.fake_mode_default).lower()}`",
        "- Live tests skipped by default: "
        f"`{str(surface.live_tests_skipped_by_default).lower()}`",
        f"- Default network: `{str(surface.default_network).lower()}`",
        f"- Stores cookies: `{str(surface.stores_cookies).lower()}`",
        f"- Paywall bypass allowed: `{str(surface.paywall_bypass_allowed).lower()}`",
        "- Private content fetching allowed: "
        f"`{str(surface.private_content_fetching_allowed).lower()}`",
        "- Automatic evidence promotion: "
        f"`{str(surface.automatic_evidence_promotion).lower()}`",
        f"- Requires human review: `{str(surface.requires_human_review).lower()}`",
        "",
        "| Tool | Module | Purpose | Optional live | Human review |",
        "| --- | --- | --- | --- | --- |",
    ]
    for tool in surface.tools:
        lines.append(
            f"| `{tool.tool_name}` | `{tool.module}` | {tool.purpose} | "
            f"`{str(tool.optional_live).lower()}` | "
            f"`{str(tool.requires_human_review).lower()}` |"
        )
    return "\n".join(lines) + "\n"
