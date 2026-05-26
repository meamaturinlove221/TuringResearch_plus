"""Skill marketplace category assignment."""

from __future__ import annotations

from turing_research_plus.skill_market.models import SkillMarketCategory
from turing_research_plus.skills.models import SkillRegistryEntry


def categorize_skill(entry: SkillRegistryEntry) -> SkillMarketCategory:
    """Assign a conservative marketplace category for a skill."""

    name = entry.skill_name
    blob = " ".join(
        [
            name,
            entry.role,
            " ".join(entry.related_contracts),
            " ".join(entry.related_lanes),
            " ".join(entry.related_modules),
        ]
    ).lower()

    if "qa-release" in name or "release" in blob or "public-readme" in blob:
        return SkillMarketCategory.RELEASE
    if "architecture" in name or "contracts" in name:
        return SkillMarketCategory.PLUGIN
    if "figure-asset" in name:
        return SkillMarketCategory.VISUAL
    if "pdf" in name or "pdf" in blob:
        return SkillMarketCategory.PDF
    if "paper" in name:
        return SkillMarketCategory.PAPER
    if "cache" in name or "ledger" in name:
        return SkillMarketCategory.EVIDENCE
    if "experiment-execution" in name:
        return SkillMarketCategory.ROUTE
    if "stress-test" in name:
        return SkillMarketCategory.FAILURE
    if "wiki-vault" in name or "context-management" in name:
        return SkillMarketCategory.WORKSPACE
    if "upstream-watch" in name or "source-hygiene" in name:
        return SkillMarketCategory.WEB
    if "feature-capsule" in name or "idea-radar" in name or "priority-elevator" in name:
        return SkillMarketCategory.PLUGIN
    if "core-reproduction" in name:
        return SkillMarketCategory.WEB
    if "literature-survey" in name or "semantic-graph" in name:
        return SkillMarketCategory.PAPER
    if "subtask-runtime" in name or "campaign-engine" in name:
        return SkillMarketCategory.ORCHESTRATION
    if "orchestrator" in name:
        return SkillMarketCategory.ORCHESTRATION
    if "fusion" in name:
        return SkillMarketCategory.ORCHESTRATION
    return SkillMarketCategory.ORCHESTRATION
