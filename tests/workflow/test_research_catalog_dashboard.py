from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "examples" / "research_catalog" / "dashboard.json"


def test_research_catalog_dashboard_json_covers_required_groups() -> None:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert data["dashboard_id"] == "research-catalog-v1.3"
    assert data["status"] == "public-demo"
    assert data["local_first"] is True
    assert data["dashboard_only"] is True
    assert data["requires_human_review"] is True
    assert data["no_agent_runtime"] is True
    assert data["no_tool_execution"] is True
    assert data["no_default_network"] is True
    assert data["no_experiment_execution"] is True

    groups = {group["id"]: group for group in data["groups"]}
    assert set(groups) == {
        "campaigns",
        "skills",
        "vault",
        "stress",
        "experiment_runbooks",
        "advisor_release",
    }

    assert "stress_test" in groups["campaigns"]["items"]
    assert "turingresearch-fusion-stress-test" in groups["skills"]["items"]
    assert "edge quality" in groups["vault"]["items"]
    assert "fake result risk" in groups["stress"]["items"]
    assert "artifact requirements" in groups["experiment_runbooks"]["items"]
    assert "release gate" in groups["advisor_release"]["items"]


def test_research_catalog_dashboard_edges_show_expected_flow() -> None:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    edges = {(edge["from"], edge["to"], edge["relation"]) for edge in data["edges"]}

    assert ("campaigns", "skills", "routes_to") in edges
    assert ("vault", "stress", "feeds_claim_review") in edges
    assert ("stress", "experiment_runbooks", "blocks_or_refines") in edges
    assert (
        "experiment_runbooks",
        "advisor_release",
        "prepares_review_artifacts",
    ) in edges


def test_research_catalog_dashboard_docs_and_site_page_match_json() -> None:
    docs = (ROOT / "docs" / "research-catalog-dashboard.md").read_text(
        encoding="utf-8"
    )
    page = (ROOT / "docs-site" / "pages" / "research-catalog.md").read_text(
        encoding="utf-8"
    )
    nav = (ROOT / "docs-site" / "nav.yaml").read_text(encoding="utf-8")
    manifest = (ROOT / "docs-site" / "site_manifest.yaml").read_text(encoding="utf-8")

    required_terms = [
        "Campaigns",
        "Skills",
        "Vault / Ontology",
        "Stress",
        "Experiment Runbooks",
        "Advisor / Release",
        "examples/research_catalog/dashboard.json",
    ]
    for term in required_terms:
        assert term in docs

    assert "examples/research_catalog/dashboard.json" in page
    assert "research-catalog-dashboard.md" in nav
    assert "examples/research_catalog/dashboard.json" in nav
    assert "docs_dashboard" in manifest


def test_research_catalog_dashboard_preserves_safety_boundaries() -> None:
    combined = "\n".join(
        [
            DASHBOARD.read_text(encoding="utf-8"),
            (ROOT / "docs" / "research-catalog-dashboard.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs-site" / "pages" / "research-catalog.md").read_text(
                encoding="utf-8"
            ),
        ]
    )

    required = [
        "no agent runtime",
        "no automatic tool execution",
        "no default network",
        "no experiment execution",
        "no Evidence Ledger mutation",
        "no fake/demo result promotion",
        "human review required",
    ]
    for item in required:
        assert item in combined

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_", "sk-"]
    for marker in forbidden:
        assert marker not in combined
