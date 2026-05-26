from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.docs_site.nav import (
    load_docs_site_manifest,
    load_docs_site_nav,
    validate_nav_against_manifest,
)

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "examples" / "session_runtime" / "session_production_dashboard_v2.json"


def test_session_production_dashboard_v2_covers_runtime_capabilities() -> None:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert data["dashboard_id"] == "session-production-parity-v2"
    assert data["production_parity"] is True
    assert data["live_steps_disabled"] is True
    assert data["no_remote_command_execution"] is True
    assert data["no_automatic_ledger_write"] is True
    assert data["no_automatic_observed_claim"] is True

    capabilities = {item["id"]: item for item in data["capabilities"]}
    assert set(capabilities) == {
        "preflight",
        "context-pack",
        "script-export",
        "fake-transfer",
        "return-verifier",
        "human-confirmation",
        "optional-live-transfer",
        "remote-execution",
    }
    for item_id in [
        "preflight",
        "context-pack",
        "script-export",
        "fake-transfer",
        "return-verifier",
        "human-confirmation",
    ]:
        assert capabilities[item_id]["production_status"] == "runnable"
    assert capabilities["optional-live-transfer"]["production_status"] == "deferred-opt-in"
    assert capabilities["remote-execution"]["production_status"] == "disabled"


def test_session_production_dashboard_v2_docs_match_boundaries() -> None:
    data = DASHBOARD.read_text(encoding="utf-8")
    docs = (ROOT / "docs" / "session-production-dashboard-v2.md").read_text(
        encoding="utf-8"
    )
    page = (ROOT / "docs-site" / "pages" / "session-production-parity.md").read_text(
        encoding="utf-8"
    )
    combined = "\n".join([data, docs, page])

    required_terms = [
        "preflight",
        "context pack",
        "script export",
        "fake transfer",
        "return verifier",
        "human confirmation",
        "optional live transfer",
        "remote execution",
        "live steps disabled",
        "no automatic observed claim",
    ]
    for term in required_terms:
        assert term in combined

    assert "examples/session_runtime/session_production_dashboard_v2.json" in docs
    assert "examples/session_runtime/session_production_dashboard_v2.json" in page


def test_session_production_dashboard_v2_is_linked_from_docs_site_nav() -> None:
    nav = load_docs_site_nav(ROOT / "docs-site" / "nav.yaml")
    manifest = load_docs_site_manifest(ROOT / "docs-site" / "site_manifest.yaml")

    nav_item = next(item for item in nav.items if item.item_id == "docs_dashboard")
    assert "../docs/session-production-dashboard-v2.md" in nav_item.source_docs
    assert (
        "../examples/session_runtime/session_production_dashboard_v2.json"
        in nav_item.source_docs
    )
    assert "docs_dashboard" in manifest.required_sections
    assert validate_nav_against_manifest(nav, manifest) == []


def test_session_production_dashboard_v2_contains_no_secret_or_private_path() -> None:
    combined = "\n".join(
        [
            DASHBOARD.read_text(encoding="utf-8"),
            (ROOT / "docs" / "session-production-dashboard-v2.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs-site" / "pages" / "session-production-parity.md").read_text(
                encoding="utf-8"
            ),
        ]
    )

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_"]
    for marker in forbidden:
        assert marker not in combined
    assert "sk-" not in combined
    assert "observed " + "success" not in combined.lower()
