from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.skill_market.models import (
    SkillMarketCategory,
    SkillMarketplaceEntry,
    SkillMarketplaceIndex,
)
from turing_research_plus.skills.models import SkillStatus


def _entry() -> SkillMarketplaceEntry:
    return SkillMarketplaceEntry(
        skill_name="turingresearch-demo-skill",
        path=Path(".agents/skills/turingresearch-demo-skill/SKILL.md"),
        category=SkillMarketCategory.ORCHESTRATION,
        status=SkillStatus.LOCKED,
        summary="Demo skill.",
        docs=["docs/skills-index.md"],
        tests=["tests/contract/test_skills_integrity.py"],
        related_contracts=["contracts/core_tools.yaml"],
        related_lanes=["lanes/00_master_ledger.md"],
        related_modules=["docs/skills-index.md"],
    )


def test_skill_marketplace_entry_records_required_metadata() -> None:
    entry = _entry()

    assert entry.skill_name == "turingresearch-demo-skill"
    assert entry.category == SkillMarketCategory.ORCHESTRATION
    assert entry.status == SkillStatus.LOCKED
    assert entry.docs
    assert entry.tests
    assert entry.related_contracts


def test_skill_marketplace_entry_requires_metadata() -> None:
    with pytest.raises(ValueError, match="related contracts"):
        SkillMarketplaceEntry(
            skill_name="turingresearch-demo-skill",
            path=Path(".agents/skills/turingresearch-demo-skill/SKILL.md"),
            category=SkillMarketCategory.ORCHESTRATION,
            status=SkillStatus.LOCKED,
            summary="Demo skill.",
            docs=["docs/skills-index.md"],
            tests=["tests/contract/test_skills_integrity.py"],
            related_contracts=[],
        )


def test_skill_marketplace_index_is_local_only() -> None:
    with pytest.raises(ValueError, match="local-only"):
        SkillMarketplaceIndex(entries=[_entry()], remote_publish=True)
