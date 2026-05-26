from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.method_builder import (
    build_vggt_method_section_skeleton,
)
from turing_research_plus.paper_write.method_templates import (
    render_method_figure_links,
    render_method_section_skeleton,
)

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"


def test_render_method_section_skeleton_has_required_headings() -> None:
    skeleton = build_vggt_method_section_skeleton(
        VGGT / "paper_method_cards",
        VGGT / "architecture_diagrams",
        VGGT / "route_specs",
    )

    markdown = render_method_section_skeleton(skeleton)

    for heading in [
        "## Problem Setting",
        "## Overview",
        "## SMPL-X Feature Encoding",
        "## VGGT Integration",
        "## Route Variants",
        "## Hard Gates",
        "## Implementation Notes",
        "## Limitations",
        "## Figure Placeholders",
        "## Evidence Refs",
    ]:
        assert heading in markdown
    assert "No final contribution claims are generated." in markdown
    assert "No method verification is claimed." in markdown


def test_render_method_figure_links_keeps_placeholders_review_only() -> None:
    skeleton = build_vggt_method_section_skeleton(
        VGGT / "paper_method_cards",
        VGGT / "architecture_diagrams",
        VGGT / "route_specs",
    )

    markdown = render_method_figure_links(skeleton)

    assert "`modal_sparseconv_route`" in markdown
    assert "not fabricated paper figures" in markdown
    assert "`true`" in markdown
