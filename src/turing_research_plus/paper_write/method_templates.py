"""Markdown templates for method section skeletons."""

from __future__ import annotations

from turing_research_plus.paper_write.figure_linker import render_figure_links_markdown
from turing_research_plus.paper_write.method_builder import MethodSectionSkeleton


def render_method_section_skeleton(skeleton: MethodSectionSkeleton) -> str:
    """Render the method section skeleton as Markdown."""

    lines = [
        f"# Method Section Skeleton: {skeleton.project_topic}",
        "",
        "This is an evidence-linked skeleton, not a final method section.",
        "",
        "## Problem Setting",
        "",
        *_bullets(skeleton.problem_setting),
        "",
        "## Overview",
        "",
        *_bullets(skeleton.overview),
        "",
        "## SMPL-X Feature Encoding",
        "",
        *_bullets(skeleton.smplx_feature_encoding),
        "",
        "## VGGT Integration",
        "",
        *_bullets(skeleton.vggt_integration),
        "",
        "## Route Variants",
        "",
        *_bullets(skeleton.route_variants),
        "",
        "## Hard Gates",
        "",
        *_bullets(skeleton.hard_gates),
        "",
        "## Implementation Notes",
        "",
        *_bullets(skeleton.implementation_notes),
        "",
        "## Limitations",
        "",
        *_bullets(skeleton.limitations),
        "",
        "## Figure Placeholders",
        "",
        *_bullets(
            [
                f"`{link.figure_id}` - {link.title}"
                for link in skeleton.figure_placeholders
            ]
        ),
        "",
        "## Evidence Refs",
        "",
        *_bullets([f"`{ref}`" for ref in skeleton.evidence_refs]),
        "",
        "## Unsafe Claims",
        "",
        *_bullets(skeleton.unsafe_claims),
        "",
        "## Safety Boundary",
        "",
        "- No final contribution claims are generated.",
        "- No method verification is claimed.",
        "- No experiment, figure, table, metric, or ablation result is fabricated.",
        "- Human review is required before drafting paper prose.",
        "",
    ]
    return "\n".join(lines)


def render_method_figure_links(skeleton: MethodSectionSkeleton) -> str:
    """Render the figure links for a method skeleton."""

    return render_figure_links_markdown(skeleton.figure_placeholders)


def _bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] or ["- Not specified."]
