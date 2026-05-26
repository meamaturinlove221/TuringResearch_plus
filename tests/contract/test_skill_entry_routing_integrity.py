from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.skills.router import DEFAULT_ROUTES

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / ".agents" / "skills"
REQUIRED_CAPSULE_SKILLS = {
    "web_fetch_adapter",
    "apify_adapter",
    "related_work_positioning",
    "skill_entry_routing",
    "vault_graph_ontology",
}
FORBIDDEN = [
    "Tuling" + "Research",
    "Tuling" + "Research_plus",
    "tuling" + "_research",
    "tuling" + "_research_plus",
    "tuling" + "research-plus",
    "tuling" + "research-",
]


def test_agents_entry_and_routing_files_exist_without_old_names() -> None:
    paths = [
        ROOT / ".agents" / "ENTRY.md",
        ROOT / ".agents" / "ROUTING_TABLE.md",
        ROOT / ".agents" / "SKILL_POLICY.md",
    ]

    for path in paths:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN:
            assert forbidden not in text


def test_routing_table_skills_exist() -> None:
    skill_names = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
    table = (ROOT / ".agents" / "ROUTING_TABLE.md").read_text(encoding="utf-8")
    names = set(re.findall(r"`(turingresearch-[a-z0-9-]+)`", table))

    assert names <= skill_names
    assert {route.recommended_skill for route in DEFAULT_ROUTES} <= skill_names


def test_routes_cover_required_categories() -> None:
    categories = {route.category for route in DEFAULT_ROUTES}
    required = {
        "upstream watch",
        "VGGT dogfooding",
        "evidence ledger",
        "artifact audit",
        "visual audit",
        "advisor pack",
        "PDF extraction",
        "route DSL",
        "hard gates",
        "failure taxonomy",
        "paper method",
        "figure architecture",
        "citation graph",
        "collision risk",
        "related work",
        "web fetch",
        "handoff",
        "pod workflow",
        "vault graph",
        "ontology",
    }

    assert required <= categories


def test_feature_capsule_skill_files_align_with_routing_scope() -> None:
    for capsule in REQUIRED_CAPSULE_SKILLS:
        skill_path = ROOT / "race" / "feature_capsules" / capsule / "SKILL.md"
        assert skill_path.exists()
        text = skill_path.read_text(encoding="utf-8")
        assert "TuringResearch" in text
        for forbidden in FORBIDDEN:
            assert forbidden not in text
