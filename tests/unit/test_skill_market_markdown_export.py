from __future__ import annotations

from pathlib import Path

from turing_research_plus.skill_market.catalog import build_skill_marketplace_index
from turing_research_plus.skill_market.markdown_export import (
    render_skill_marketplace_markdown,
)

ROOT = Path(__file__).resolve().parents[2]


def test_skill_marketplace_markdown_export_is_local_only() -> None:
    index = build_skill_marketplace_index(ROOT / ".agents" / "skills")
    markdown = render_skill_marketplace_markdown(index)

    assert "Skill Marketplace: turingresearch_skill_marketplace" in markdown
    assert "Remote publish: `false`" in markdown
    assert "does not upload, install, or execute skills" in markdown
    assert "turingresearch-master-orchestrator" in markdown
