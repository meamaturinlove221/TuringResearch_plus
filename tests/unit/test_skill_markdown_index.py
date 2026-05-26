from __future__ import annotations

from pathlib import Path

from turing_research_plus.skills.markdown_index import (
    render_registry_summary,
    render_routing_table,
)
from turing_research_plus.skills.registry import load_skill_registry
from turing_research_plus.skills.router import DEFAULT_ROUTES

ROOT = Path(__file__).resolve().parents[2]


def test_render_routing_table_contains_categories() -> None:
    markdown = render_routing_table(DEFAULT_ROUTES)

    assert "# TuringResearch Skill Routing Table" in markdown
    assert "web fetch" in markdown
    assert "`turingresearch-core-reproduction`" in markdown


def test_render_registry_summary_contains_skills() -> None:
    entries = load_skill_registry(ROOT / ".agents" / "skills")
    markdown = render_registry_summary(entries)

    assert "TuringResearch Skill Registry Summary" in markdown
    assert "`turingresearch-master-orchestrator`" in markdown
