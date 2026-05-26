from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.docs_site.nav import (
    load_docs_site_manifest,
    load_docs_site_nav,
    validate_nav_against_manifest,
)

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "examples" / "public_demo" / "parity_dashboard_v2.json"


def test_original_repo_parity_dashboard_v2_json_tracks_progress_levels() -> None:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert data["dashboard_id"] == "original-repo-parity-v2"
    assert data["status"] == "public-demo"
    assert data["local_first"] is True
    assert data["requires_human_review"] is True
    assert data["no_live_network_required"] is True
    assert data["no_core_runtime_added"] is True
    assert data["no_unsafe_live_default"] is True
    assert set(data["levels"]) == {"structural", "runtime", "production", "deferred"}

    groups = {group["id"]: group for group in data["groups"]}
    assert set(groups) == {"session", "scholar", "web", "yogsoth", "aris"}
    for group_id in ["session", "scholar", "web", "yogsoth"]:
        assert groups[group_id]["structural_parity"] == "complete"
        assert groups[group_id]["runtime_parity"] == "complete"
        assert groups[group_id]["production_parity"].startswith("complete")
        assert groups[group_id]["evidence_docs"]

    assert groups["aris"]["structural_parity"] == "deferred"
    assert groups["aris"]["runtime_parity"] == "deferred"
    assert groups["aris"]["production_parity"] == "deferred"
    assert data["overall"]["production_parity"] == "pass-with-review"
    assert data["overall"]["unsafe_live_default"] is False


def test_original_repo_parity_dashboard_v2_tracks_deferred_and_rejected_items() -> None:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    groups = {group["id"]: group for group in data["groups"]}

    assert "remote command execution" in groups["session"]["deferred"]
    assert "MinerU implementation" in groups["scholar"]["deferred"]
    assert "private scraping" in groups["web"]["deferred"]
    assert "automatic experiment execution" in groups["yogsoth"]["deferred"]
    assert "cross-model review" in groups["aris"]["deferred"]
    assert "proof-checker" in groups["aris"]["deferred"]
    assert "meta-optimize" in groups["aris"]["deferred"]
    assert "paper-claim-audit" in groups["aris"]["deferred"]

    rejected = set(data["rejected_unsafe_features"])
    assert "automatic experiment execution" in rejected
    assert "automatic observed result writes" in rejected
    assert "fake/demo result promotion" in rejected
    assert "default network access" in rejected


def test_original_repo_parity_dashboard_v2_docs_and_site_page_match_json() -> None:
    docs = (ROOT / "docs" / "original-repo-parity-dashboard-v2.md").read_text(
        encoding="utf-8"
    )
    page = (ROOT / "docs-site" / "pages" / "original-repo-parity-v2.md").read_text(
        encoding="utf-8"
    )
    combined = docs + "\n" + page

    required = [
        "structural parity",
        "runtime parity",
        "production parity",
        "deferred",
        "Neocortica Session",
        "Neocortica Scholar",
        "Neocortica Web",
        "yogsoth-ai",
        "ARIS",
        "examples/public_demo/parity_dashboard_v2.json",
        "docs/v1.4.0-full-production-replay-report.md",
    ]
    for term in required:
        assert term in combined


def test_original_repo_parity_dashboard_v2_is_linked_from_docs_site_nav() -> None:
    nav = load_docs_site_nav(ROOT / "docs-site" / "nav.yaml")
    manifest = load_docs_site_manifest(ROOT / "docs-site" / "site_manifest.yaml")

    nav_ids = {item.item_id for item in nav.items}
    assert "original_repo_parity" in nav_ids
    assert "original_repo_parity" in manifest.required_sections
    assert validate_nav_against_manifest(nav, manifest) == []

    nav_item = next(item for item in nav.items if item.item_id == "original_repo_parity")
    assert nav_item.page == "pages/original-repo-parity.md"
    assert "../examples/public_demo/parity_dashboard_v2.json" in nav_item.source_docs


def test_original_repo_parity_dashboard_v2_preserves_safety_boundaries() -> None:
    combined = "\n".join(
        [
            DASHBOARD.read_text(encoding="utf-8"),
            (ROOT / "docs" / "original-repo-parity-dashboard-v2.md").read_text(
                encoding="utf-8"
            ),
            (
                ROOT / "docs-site" / "pages" / "original-repo-parity-v2.md"
            ).read_text(encoding="utf-8"),
        ]
    )

    required = [
        "no unsafe live default",
        "no default network",
        "no automatic experiment execution",
        "no Evidence Ledger mutation",
        "no fake/demo result promotion",
        "human review required",
    ]
    for item in required:
        assert item in combined

    forbidden = [
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "sk-",
        '"status": "' + 'observed"',
    ]
    for marker in forbidden:
        assert marker not in combined

    assert "Tuling" + "Research" not in combined
