from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_research_catalog_docs_exist_and_cover_required_surfaces() -> None:
    catalog = _read("docs/turingresearch-research-catalog.md")

    required_terms = [
        "Campaigns",
        "Skills",
        "Capabilities",
        "Vault graph",
        "Ontology SOPs",
        "Stress tests",
        "Experiment runbooks",
        "Advisor pack",
        "Public release",
    ]
    for term in required_terms:
        assert term in catalog


def test_research_catalog_routing_maps_core_campaigns_to_skills_and_gates() -> None:
    routing = _read("docs/research-catalog-routing.md")

    expected_campaigns = [
        "north_star",
        "knowledge_acquisition",
        "deep_insight",
        "hypothesis_formation",
        "convergence",
        "stress_test",
        "experiment_planning",
        "artifact_audit",
        "advisor_pack",
        "public_release",
    ]
    for campaign in expected_campaigns:
        assert f"`{campaign}`" in routing

    assert "stress-test runner" in routing
    assert "privacy/security gate" in routing
    assert "Routing does not execute the skill." in routing


def test_research_catalog_skill_map_links_parity_surfaces() -> None:
    skill_map = _read("docs/research-catalog-skill-map.md")

    expected_docs = [
        "docs/turingresearch-campaign-catalog.md",
        "docs/yogsoth-vault-parity.md",
        "docs/yogsoth-ontology-parity.md",
        "docs/yogsoth-stress-test-parity.md",
        "docs/yogsoth-experiment-execution-parity.md",
        "docs/advisor-pack-builder.md",
        "docs/v1.0.0-public-launch-rc-report.md",
    ]
    for doc in expected_docs:
        assert doc in skill_map


def test_research_catalog_preserves_safety_boundaries() -> None:
    combined = "\n".join(
        [
            _read("docs/turingresearch-research-catalog.md"),
            _read("docs/research-catalog-routing.md"),
            _read("docs/research-catalog-skill-map.md"),
        ]
    ).lower()

    required_boundaries = [
        "no automatic experiment execution",
        "no multi-agent runtime",
        "no default networking",
        "no unknown plugin execution",
        "no fake/demo result promotion",
        "human review",
    ]
    for boundary in required_boundaries:
        assert boundary in combined
