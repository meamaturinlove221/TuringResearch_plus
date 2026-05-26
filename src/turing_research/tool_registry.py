"""Tool registry for the minimal TulingResearch Plus MCP smoke surface."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

MCP_SERVER_NAME = "tulingresearch-plus"


class ToolDescriptor(BaseModel):
    """One tool exposed to the local MCP smoke registry."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    implementation_status: str = Field(min_length=1)
    dry_run_supported: bool = True


MINIMAL_MCP_TOOLS: tuple[ToolDescriptor, ...] = (
    ToolDescriptor(
        name="core.health_check",
        description="Return Core health status.",
        implementation_status="implemented_minimal",
    ),
    ToolDescriptor(
        name="core.paper_content",
        description="Read cached paper Markdown.",
        implementation_status="implemented_minimal",
    ),
    ToolDescriptor(
        name="core.web_content",
        description="Read cached web Markdown.",
        implementation_status="implemented_minimal",
    ),
    ToolDescriptor(
        name="core.session_list",
        description="List local research sessions.",
        implementation_status="implemented_minimal",
    ),
    ToolDescriptor(
        name="pdf.inspect",
        description="Inspect a local PDF path.",
        implementation_status="implemented_minimal",
    ),
    ToolDescriptor(
        name="pdf.to_markdown",
        description="Convert a local PDF to Markdown through the Phase A adapter.",
        implementation_status="implemented_minimal",
    ),
    ToolDescriptor(
        name="pdf.markdown_content",
        description="Read cached PDF Markdown content.",
        implementation_status="implemented_minimal",
    ),
)


def list_core_tools() -> list[ToolDescriptor]:
    """Return Core tool descriptors for backward-compatible health checks."""

    return [tool for tool in MINIMAL_MCP_TOOLS if tool.name.startswith("core.")]


def list_mcp_tools() -> list[ToolDescriptor]:
    """Return the v0.1.0 minimal MCP smoke-test tool descriptors."""

    return list(MINIMAL_MCP_TOOLS)


def get_tool_descriptor(tool_name: str) -> ToolDescriptor | None:
    """Return one registered tool descriptor by name."""

    for tool in MINIMAL_MCP_TOOLS:
        if tool.name == tool_name:
            return tool
    return None
