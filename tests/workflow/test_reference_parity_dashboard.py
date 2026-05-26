from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "examples" / "public_demo" / "reference_parity_dashboard.json"


def test_reference_parity_dashboard_json_covers_required_groups() -> None:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert data["dashboard_id"] == "reference-parity-v1.2"
    assert data["status"] == "public-demo"
    assert data["local_first"] is True
    assert data["requires_human_review"] is True
    assert data["no_live_network_required"] is True
    assert data["no_core_runtime_added"] is True

    groups = {group["id"]: group for group in data["groups"]}
    assert set(groups) == {"neocortica", "yogsoth"}

    neocortica_items = {item["id"]: item for item in groups["neocortica"]["items"]}
    assert set(neocortica_items) == {
        "reference-session",
        "reference-scholar",
        "reference-web",
    }
    assert all(item["status"] == "complete" for item in neocortica_items.values())

    yogsoth_items = {item["id"]: item for item in groups["yogsoth"]["items"]}
    assert {
        "campaign",
        "vault",
        "ontology",
        "stress-test",
        "experiment-execution",
        "research-catalog",
    } <= set(yogsoth_items)
    assert all(item["status"] == "complete" for item in yogsoth_items.values())


def test_reference_parity_dashboard_tracks_deferred_and_rejected_items() -> None:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    deferred = {item["id"]: item for item in data["deferred"]}
    assert deferred["aris"]["status"] == "deferred"
    assert "v1.3" in deferred["aris"]["target"]

    rejected = set(data["rejected_unsafe_features"])
    assert "unknown remote execution" in rejected
    assert "automatic experiment execution" in rejected
    assert "automatic observed result writes" in rejected
    assert "fake/demo result promotion" in rejected
    assert "default network access" in rejected


def test_reference_parity_docs_and_site_page_match_dashboard_boundaries() -> None:
    docs = (ROOT / "docs" / "reference-parity-dashboard.md").read_text(
        encoding="utf-8"
    )
    page = (ROOT / "docs-site" / "pages" / "reference-parity.md").read_text(
        encoding="utf-8"
    )

    required_terms = [
        "Neocortica Session parity",
        "Neocortica Scholar parity",
        "Neocortica Web parity",
        "yogsoth-ai",
        "Deferred ARIS",
        "Rejected Unsafe Features",
        "Future Roadmap",
    ]
    for term in required_terms:
        assert term in docs

    assert "examples/public_demo/reference_parity_dashboard.json" in docs
    assert "examples/public_demo/reference_parity_dashboard.json" in page
    assert "Automatic experiment execution" in page
    assert "Fake/demo result promotion" in page


def test_reference_parity_dashboard_contains_no_secret_or_private_path() -> None:
    combined = "\n".join(
        [
            DASHBOARD.read_text(encoding="utf-8"),
            (ROOT / "docs" / "reference-parity-dashboard.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs-site" / "pages" / "reference-parity.md").read_text(
                encoding="utf-8"
            ),
        ]
    )

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_"]
    for marker in forbidden:
        assert marker not in combined
    assert "sk-" not in combined
