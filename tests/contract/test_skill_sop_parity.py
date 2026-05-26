from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / ".agents" / "skills"

PRIORITY_WORKFLOWS = {
    "master orchestrator": "turingresearch-master-orchestrator",
    "upstream watch": "turingresearch-race-upstream-watch",
    "campaign catalog": "turingresearch-fusion-campaign-engine",
    "scholar pipeline": "turingresearch-fusion-literature-survey",
    "web fetch": "turingresearch-core-reproduction",
    "pod workflow": "turingresearch-fusion-context-management",
    "artifact audit": "turingresearch-cache-and-ledger",
    "advisor pack": "turingresearch-paper-writing-pipeline",
    "release gate": "turingresearch-qa-release",
}

REQUIRED_SOP_FIELDS = [
    "`workflow`",
    "`when_to_use`",
    "`inputs`",
    "`outputs`",
    "`safety`",
    "`non-goals`",
    "`handoff`",
    "`tests`",
    "`related_docs`",
]

FORBIDDEN_TERMS = [
    "Tuling" + "Research",
    "tuling" + "_research",
    "tuling" + "research-",
]


def _skill_text(skill_name: str) -> str:
    return (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")


def test_priority_skills_have_round_240_sop_parity_fields() -> None:
    for workflow, skill_name in PRIORITY_WORKFLOWS.items():
        text = _skill_text(skill_name)

        assert "## Round 240 SOP Parity" in text
        assert f"- `workflow`: {workflow}" in text
        for field in REQUIRED_SOP_FIELDS:
            assert field in text


def test_agents_entry_marketplace_and_routing_table_cover_priority_workflows() -> None:
    combined = "\n".join(
        [
            (ROOT / ".agents" / "ENTRY.md").read_text(encoding="utf-8"),
            (ROOT / ".agents" / "MARKETPLACE.md").read_text(encoding="utf-8"),
            (ROOT / ".agents" / "ROUTING_TABLE.md").read_text(encoding="utf-8"),
        ]
    )

    for workflow, skill_name in PRIORITY_WORKFLOWS.items():
        assert workflow in combined
        assert f"`{skill_name}`" in combined


def test_skill_sop_docs_define_required_style_and_boundaries() -> None:
    text = "\n".join(
        [
            (ROOT / "docs" / "skill-sop-parity.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "skill-sop-style-guide.md").read_text(encoding="utf-8"),
        ]
    )

    for field in REQUIRED_SOP_FIELDS:
        assert field in text
    assert "no default live networking" in text.lower()
    assert "not runtime code" in text.lower()
    assert "observed evidence" in text.lower()


def test_skill_sop_parity_does_not_reintroduce_old_names() -> None:
    paths = [
        ROOT / ".agents" / "ENTRY.md",
        ROOT / ".agents" / "MARKETPLACE.md",
        ROOT / ".agents" / "ROUTING_TABLE.md",
        ROOT / "docs" / "skill-sop-parity.md",
        ROOT / "docs" / "skill-sop-style-guide.md",
        *[
            SKILLS_ROOT / skill_name / "SKILL.md"
            for skill_name in PRIORITY_WORKFLOWS.values()
        ],
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        for term in FORBIDDEN_TERMS:
            assert term not in text
