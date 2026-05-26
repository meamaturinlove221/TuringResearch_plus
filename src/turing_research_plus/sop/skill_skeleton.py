"""Optional skill skeleton generation for SOP outputs."""

from turing_research_plus.sop.models import SOPGraph


def generate_skill_skeleton(graph: SOPGraph) -> str:
    """Generate a repo-scoped skill skeleton for an SOP graph."""

    skill_name = f"turingresearch-sop-{graph.graph_type}-{graph.graph_id}"
    return f"""---
name: {skill_name}
description: Use when executing the {graph.title} SOP.
---

# TuringResearch Plus SOP Skill

Graph: `{graph.graph_id}`

Follow the SOP document and keep all outputs evidence-backed.
"""
