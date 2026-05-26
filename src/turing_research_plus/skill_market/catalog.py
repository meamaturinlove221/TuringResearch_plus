"""Build and validate the local skill marketplace catalog."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.skill_market.category import categorize_skill
from turing_research_plus.skill_market.models import (
    SkillMarketplaceEntry,
    SkillMarketplaceIndex,
    SkillMarketplaceReviewReport,
)
from turing_research_plus.skills.registry import load_skill_registry

ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = ROOT / ".agents" / "skills"


def build_skill_marketplace_index(skills_root: Path = SKILLS_ROOT) -> SkillMarketplaceIndex:
    """Build a local marketplace index from repo skill files."""

    entries: list[SkillMarketplaceEntry] = []
    for skill in load_skill_registry(skills_root):
        entries.append(
            SkillMarketplaceEntry(
                skill_name=skill.skill_name,
                path=skill.path,
                category=categorize_skill(skill),
                status=skill.status,
                summary=skill.role.splitlines()[0],
                docs=_docs_for_skill(skill.related_modules),
                tests=_tests_for_skill(skill),
                related_contracts=skill.related_contracts,
                related_lanes=skill.related_lanes,
                related_modules=skill.related_modules,
            )
        )
    return SkillMarketplaceIndex(
        entries=entries,
        docs=["docs/skill-marketplace-layout.md", "docs/skill-catalog.md"],
        tests=["tests/contract/test_skill_marketplace_integrity.py"],
        local_only=True,
        remote_publish=False,
        requires_human_review=True,
    )


def review_skill_marketplace(
    index: SkillMarketplaceIndex,
    skills_root: Path = SKILLS_ROOT,
) -> SkillMarketplaceReviewReport:
    """Review marketplace alignment with `.agents/skills`."""

    actual_skill_names = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
    indexed_skill_names = sorted(entry.skill_name for entry in index.entries)
    missing_skills = sorted(set(actual_skill_names) - set(indexed_skill_names))
    invalid_names = [
        name
        for name in indexed_skill_names
        if not name.startswith("turingresearch-")
    ]
    missing_metadata = [
        entry.skill_name
        for entry in index.entries
        if not entry.docs or not entry.tests or not entry.related_contracts
    ]

    valid = (
        not missing_skills
        and not invalid_names
        and not missing_metadata
        and not index.remote_publish
    )

    return SkillMarketplaceReviewReport(
        marketplace_id=index.marketplace_id,
        valid=valid,
        checked_skills=len(index.entries),
        missing_skills=missing_skills,
        invalid_names=invalid_names,
        missing_metadata=missing_metadata,
        remote_publish=index.remote_publish,
        requires_human_review=True,
    )


def _docs_for_skill(related_modules: list[str]) -> list[str]:
    docs = [item for item in related_modules if item.startswith("docs/")]
    return docs or ["docs/skills-index.md"]


def _tests_for_skill(skill: object) -> list[str]:
    tests: list[str] = []
    for value in getattr(skill, "related_modules", []):
        if value.startswith("tests/"):
            tests.append(value)
    return tests or ["tests/contract/test_skills_integrity.py"]
