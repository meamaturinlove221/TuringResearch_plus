"""Thin capsule-local advisor pack tool wrappers."""

from __future__ import annotations

from typing import Any

from turing_research_plus.advisor.models import AdvisorPackBuildInput
from turing_research_plus.advisor.pack_builder import advisor_pack_build, write_advisor_pack


def advisor_pack_build_tool(request: AdvisorPackBuildInput) -> dict[str, Any]:
    """Return the advisor pack payload without writing files."""

    return advisor_pack_build(request)


def advisor_pack_write_tool(request: AdvisorPackBuildInput) -> dict[str, Any]:
    """Write the advisor pack files and return the payload."""

    return write_advisor_pack(request).model_dump(mode="json")
