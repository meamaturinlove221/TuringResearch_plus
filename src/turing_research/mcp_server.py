"""STDIO-safe MCP smoke server surface for TuringResearch Plus."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from pydantic import BaseModel, ConfigDict

from turing_research import __version__
from turing_research.pdf.tools import pdf_inspect, pdf_markdown_content
from turing_research.scholar.content_service import PaperContentService
from turing_research.scholar.models import PaperContentRequest
from turing_research.session.registry import SessionRegistry
from turing_research.settings import CoreSettings, get_settings
from turing_research.tool_registry import MCP_SERVER_NAME, list_core_tools, list_mcp_tools
from turing_research.web.content_service import WebContentService
from turing_research.web.models import WebContentRequest


class HealthCheckResult(BaseModel):
    """Health check result for core.health_check."""

    model_config = ConfigDict(extra="forbid")

    status: str
    package: str
    version: str
    tools: list[str]


def core_health_check() -> dict[str, Any]:
    """MCP wrapper for core.health_check."""

    result = HealthCheckResult(
        status="ok",
        package="turing_research",
        version=__version__,
        tools=[tool.name for tool in list_core_tools()],
    )
    return result.model_dump(mode="json")


def core_paper_content(
    paper_id: str,
    settings: CoreSettings | None = None,
    service: PaperContentService | None = None,
) -> dict[str, Any]:
    """MCP wrapper for core.paper_content."""

    active_settings = settings or get_settings()
    active_service = service or PaperContentService(active_settings.cache_dir)
    result = active_service.get_content(PaperContentRequest(paper_id=paper_id))
    return result.model_dump(mode="json")


def core_web_content(
    url: str,
    settings: CoreSettings | None = None,
    service: WebContentService | None = None,
) -> dict[str, Any]:
    """MCP wrapper for core.web_content."""

    active_settings = settings or get_settings()
    active_service = service or WebContentService(active_settings.cache_dir)
    result = active_service.get_content(WebContentRequest(url=url))
    return result.model_dump(mode="json")


def core_session_list(
    settings: CoreSettings | None = None,
    registry: SessionRegistry | None = None,
) -> dict[str, Any]:
    """MCP wrapper for core.session_list."""

    active_settings = settings or get_settings()
    active_registry = registry or SessionRegistry(active_settings.session_registry_path)
    result = active_registry.list_sessions()
    return result.model_dump(mode="json")


def list_registered_tools() -> list[dict[str, Any]]:
    """Return registered local MCP smoke-test tools."""

    return [tool.model_dump(mode="json") for tool in list_mcp_tools()]


def dry_run_tool(tool_name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run a deterministic local dry-run for the minimal MCP smoke tools."""

    payload = arguments or {}
    if tool_name == "core.health_check":
        return core_health_check()
    if tool_name == "core.paper_content":
        return core_paper_content(paper_id=str(payload.get("paper_id", "dry-run-paper")))
    if tool_name == "core.web_content":
        return core_web_content(url=str(payload.get("url", "https://example.invalid/dry-run")))
    if tool_name == "core.session_list":
        return core_session_list()
    if tool_name == "pdf.inspect":
        return pdf_inspect(payload.get("pdf_path", "dry-run.pdf"))
    if tool_name == "pdf.to_markdown":
        return {
            "status": "planned",
            "tool_name": "pdf.to_markdown",
            "dry_run": True,
            "message": "Provide a local PDF path to run Phase A conversion.",
        }
    if tool_name == "pdf.markdown_content":
        return pdf_markdown_content(payload.get("pdf_path", "dry-run.pdf"))

    return {
        "status": "error",
        "tool_name": tool_name,
        "error": {"code": "unknown_tool", "message": "Tool is not registered."},
    }


def build_stdio_manifest() -> dict[str, Any]:
    """Build a serializable local MCP manifest without starting network services."""

    return {
        "server_name": MCP_SERVER_NAME,
        "package": "turing_research",
        "version": __version__,
        "transport": "stdio",
        "tools": list_registered_tools(),
    }


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for local STDIO smoke tests.

    This command prints protocol payloads to stdout only when explicitly asked.
    Operational logs go to stderr to preserve STDIO MCP safety.
    """

    parser = argparse.ArgumentParser(description="TuringResearch Plus local MCP smoke server.")
    parser.add_argument(
        "--manifest",
        action="store_true",
        help="Print the local tool manifest as JSON.",
    )
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Run core.health_check as JSON.",
    )
    args = parser.parse_args(argv)

    if args.manifest:
        sys.stdout.write(json.dumps(build_stdio_manifest(), ensure_ascii=False) + "\n")
        return 0
    if args.health_check:
        sys.stdout.write(json.dumps(core_health_check(), ensure_ascii=False) + "\n")
        return 0

    sys.stderr.write(
        "turingresearch-plus local stdio smoke module imported; no network server started.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
