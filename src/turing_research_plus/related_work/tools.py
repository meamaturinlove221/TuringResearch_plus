"""Thin tool wrapper for related-work positioning."""

from __future__ import annotations

from turing_research_plus.related_work.models import (
    RelatedWorkPositioningInput,
    RelatedWorkPositioningReport,
)
from turing_research_plus.related_work.positioning import build_related_work_positioning


def related_work_position(
    request: RelatedWorkPositioningInput,
) -> RelatedWorkPositioningReport:
    """Build a conservative related-work positioning report."""

    return build_related_work_positioning(request)
