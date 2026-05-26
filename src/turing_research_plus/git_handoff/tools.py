"""Thin local tool wrappers for Git context handoff."""

from __future__ import annotations

from typing import Any

from turing_research_plus.git_handoff.context_package import build_context_package
from turing_research_plus.git_handoff.models import ContextPackageBuildInput
from turing_research_plus.git_handoff.structured_output import (
    build_structured_output_template,
    write_structured_output_template,
)


def git_context_package_build_tool(request: ContextPackageBuildInput) -> dict[str, Any]:
    """Build a local context package and return metadata."""

    return build_context_package(request).model_dump(mode="json")


def structured_output_template_write_tool(output_dir: str, route_id: str) -> dict[str, Any]:
    """Write structured output template files and return template metadata."""

    from pathlib import Path

    template = build_structured_output_template(route_id=route_id)
    write_structured_output_template(Path(output_dir), template)
    return template.model_dump(mode="json")
