"""MCP usage guide export for Scholar parity."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ScholarMcpUsageGuide(BaseModel):
    """Safe MCP usage guide for Scholar parity."""

    model_config = ConfigDict(extra="forbid")

    server_name: str = "turingresearch-plus"
    command: str = "turingresearch-plus-mcp"
    args: list[str] = Field(default_factory=lambda: ["--manifest"])
    mode_env: str = "TURINGRESEARCH_MODE=fake"
    live_tests_env: str = "TURINGRESEARCH_ENABLE_LIVE_TESTS=0"
    semantic_scholar_live_env: str = "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0"
    credential_policy: str = "Committed examples leave provider credential fields blank."
    plugin_policy: str = "Plugin tools are disabled by default."
    requires_human_review: bool = True


def build_scholar_mcp_usage_guide() -> ScholarMcpUsageGuide:
    """Return the default Scholar MCP usage guide."""

    return ScholarMcpUsageGuide()


def render_scholar_mcp_usage_guide(guide: ScholarMcpUsageGuide) -> str:
    """Render a public-safe Scholar MCP usage guide."""

    return "\n".join(
        [
            "# Scholar MCP Usage Guide",
            "",
            f"- Server name: `{guide.server_name}`",
            f"- Command: `{guide.command}`",
            f"- Args: `{guide.args}`",
            f"- Default mode: `{guide.mode_env}`",
            f"- Live tests: `{guide.live_tests_env}`",
            f"- Semantic Scholar live adapter: `{guide.semantic_scholar_live_env}`",
            f"- Credential policy: {guide.credential_policy}",
            f"- Plugin policy: {guide.plugin_policy}",
            f"- Requires human review: `{str(guide.requires_human_review).lower()}`",
            "",
            "Live provider access is opt-in and must use private local environment configuration.",
        ]
    ) + "\n"
