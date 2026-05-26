from __future__ import annotations

from pathlib import Path

from turing_research_plus.skill_market.catalog import (
    build_skill_marketplace_index,
    review_skill_marketplace,
)
from turing_research_plus.skill_market.models import SkillMarketCategory

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / ".agents" / "skills"
MARKETPLACE_DOC = ROOT / ".agents" / "MARKETPLACE.md"


def test_skill_marketplace_has_no_remote_publish_boundary() -> None:
    index = build_skill_marketplace_index(SKILLS_ROOT)

    assert index.local_only is True
    assert index.remote_publish is False
    assert index.requires_human_review is True


def test_skill_marketplace_aligns_with_repo_skill_folders() -> None:
    index = build_skill_marketplace_index(SKILLS_ROOT)
    report = review_skill_marketplace(index, SKILLS_ROOT)

    assert report.valid is True
    assert report.checked_skills == len(list(SKILLS_ROOT.iterdir()))
    assert all(entry.skill_name.startswith("turingresearch-") for entry in index.entries)


def test_skill_marketplace_categories_are_documented() -> None:
    text = (ROOT / "docs" / "skill-categories.md").read_text(encoding="utf-8")

    for category in SkillMarketCategory:
        assert f"| {category.value} |" in text


def test_agents_marketplace_is_generated_and_uses_current_names() -> None:
    text = MARKETPLACE_DOC.read_text(encoding="utf-8")
    old_name = "Tuling" + "Research"

    assert "turingresearch-master-orchestrator" in text
    assert "Remote publish: `false`" in text
    assert old_name not in text
