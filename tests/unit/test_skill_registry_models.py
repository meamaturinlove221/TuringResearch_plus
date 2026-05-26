from __future__ import annotations

from pathlib import Path

from turing_research_plus.skills.models import (
    SkillRegistryEntry,
    SkillRoute,
    SkillRoutingDecision,
    SkillStatus,
)


def test_skill_registry_entry_model() -> None:
    entry = SkillRegistryEntry(
        skill_name="turingresearch-master-orchestrator",
        path=Path(".agents/skills/turingresearch-master-orchestrator/SKILL.md"),
        role="coordinate",
        status=SkillStatus.LOCKED,
    )

    assert entry.skill_name == "turingresearch-master-orchestrator"
    assert entry.status == SkillStatus.LOCKED


def test_skill_route_and_decision_do_not_execute() -> None:
    route = SkillRoute(
        category="web fetch",
        recommended_skill="turingresearch-core-reproduction",
        related_lane="lanes/52_web_fetch_apify_adapter.md",
        keywords=["web"],
    )
    decision = SkillRoutingDecision(
        query="web fetch project page",
        category=route.category,
        recommended_skill=route.recommended_skill,
        confidence=0.9,
        rationale="matched",
        related_lane=route.related_lane,
    )

    assert decision.does_not_execute is True
