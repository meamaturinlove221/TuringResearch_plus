"""Public-safe Apify usage guide export."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ApifyUsageGuide(BaseModel):
    """Apify usage guide for optional live workflows."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = "apify_optional"
    default_live_enabled: bool = False
    live_tests_env: str = "TURINGRESEARCH_ENABLE_LIVE_TESTS=0"
    apify_live_env: str = "TURINGRESEARCH_ENABLE_APIFY_LIVE=0"
    token_env: str = "APIFY_TOKEN"
    no_key_behavior: str = "graceful missing-token result"
    stores_cookies: bool = False
    bypasses_paywall: bool = False
    fetches_private_content: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe Apify behavior is enabled."""

        return (
            self.default_live_enabled
            or self.stores_cookies
            or self.bypasses_paywall
            or self.fetches_private_content
            or not self.requires_human_review
        )


def build_apify_usage_guide() -> ApifyUsageGuide:
    """Build the default Apify usage guide."""

    return ApifyUsageGuide()


def render_apify_usage_guide(guide: ApifyUsageGuide) -> str:
    """Render Apify usage guidance as Markdown."""

    return "\n".join(
        [
            "# Apify Usage Guide",
            "",
            f"- Tool: `{guide.tool_name}`",
            f"- Default live enabled: `{str(guide.default_live_enabled).lower()}`",
            f"- Live tests: `{guide.live_tests_env}`",
            f"- Apify live adapter: `{guide.apify_live_env}`",
            f"- Token env: `{guide.token_env}`",
            f"- No-key behavior: {guide.no_key_behavior}",
            f"- Stores cookies: `{str(guide.stores_cookies).lower()}`",
            f"- Bypasses paywall: `{str(guide.bypasses_paywall).lower()}`",
            f"- Fetches private content: `{str(guide.fetches_private_content).lower()}`",
            f"- Requires human review: `{str(guide.requires_human_review).lower()}`",
        ]
    ) + "\n"
