from __future__ import annotations

from pathlib import Path

from turing_research_plus.skill_market.catalog import build_skill_marketplace_index
from turing_research_plus.skill_market.models import SkillMarketCategory

ROOT = Path(__file__).resolve().parents[2]


def test_skill_categories_are_allowed_values() -> None:
    index = build_skill_marketplace_index(ROOT / ".agents" / "skills")

    allowed = {category.value for category in SkillMarketCategory}

    assert {entry.category for entry in index.entries}.issubset(allowed)


def test_skill_categories_include_core_marketplace_axes() -> None:
    index = build_skill_marketplace_index(ROOT / ".agents" / "skills")
    categories = {entry.category for entry in index.entries}

    assert SkillMarketCategory.ORCHESTRATION in categories
    assert SkillMarketCategory.PAPER in categories
    assert SkillMarketCategory.PLUGIN in categories
    assert SkillMarketCategory.RELEASE in categories
    assert SkillMarketCategory.WORKSPACE in categories
