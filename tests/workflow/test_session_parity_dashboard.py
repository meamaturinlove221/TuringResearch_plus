from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.docs_site.nav import (
    load_docs_site_manifest,
    load_docs_site_nav,
    validate_nav_against_manifest,
)

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "examples" / "session_runtime" / "session_parity_dashboard.json"


def test_session_parity_dashboard_json_covers_required_runtime_capabilities() -> None:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert data["dashboard_id"] == "session-parity-v1.3"
    assert data["status"] == "public-demo"
    assert data["local_first"] is True
    assert data["requires_human_review"] is True
    assert data["no_live_ssh_required"] is True
    assert data["no_remote_command_execution"] is True
    assert data["no_automatic_ledger_write"] is True

    capabilities = {item["id"]: item for item in data["capabilities"]}
    assert set(capabilities) == {
        "preflight",
        "context-pack",
        "fake-transfer",
        "optional-live-transfer",
        "return-verifier",
        "workflow-replay",
    }
    assert capabilities["preflight"]["status"] == "fake-runnable"
    assert capabilities["context-pack"]["status"] == "fake-runnable"
    assert capabilities["fake-transfer"]["status"] == "fake-runnable"
    assert capabilities["optional-live-transfer"]["status"] == "deferred-live-opt-in"
    assert capabilities["return-verifier"]["status"] == "fake-runnable"
    assert capabilities["workflow-replay"]["status"] == "fake-runnable"


def test_session_parity_dashboard_tracks_deferred_remote_execution() -> None:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    deferred = {item["id"]: item for item in data["deferred"]}
    assert deferred["remote-execution"]["status"] == "deferred"
    assert deferred["ssh-tmux-provision"]["status"] == "deferred"
    assert deferred["automatic-pod-cleanup"]["status"] == "deferred"

    safety = set(data["safety_boundaries"])
    assert "no live SSH by default" in safety
    assert "no remote command execution" in safety
    assert "no automatic Evidence Ledger write" in safety
    assert "fake/demo results remain proposed-only" in safety


def test_session_parity_docs_and_site_page_match_dashboard_boundaries() -> None:
    docs = (ROOT / "docs" / "session-parity-dashboard.md").read_text(encoding="utf-8")
    page = (ROOT / "docs-site" / "pages" / "session-parity.md").read_text(
        encoding="utf-8"
    )

    required_terms = [
        "preflight",
        "context pack",
        "fake transfer",
        "optional live transfer",
        "return verifier",
        "workflow replay",
        "Deferred Remote Execution",
        "Safety Boundaries",
    ]
    for term in required_terms:
        assert term in docs

    assert "examples/session_runtime/session_parity_dashboard.json" in docs
    assert "examples/session_runtime/session_parity_dashboard.json" in page
    assert "no live SSH by default" in page
    assert "no remote command execution" in page


def test_session_parity_dashboard_is_linked_from_docs_site_nav() -> None:
    nav = load_docs_site_nav(ROOT / "docs-site" / "nav.yaml")
    manifest = load_docs_site_manifest(ROOT / "docs-site" / "site_manifest.yaml")

    nav_item = next(item for item in nav.items if item.item_id == "docs_dashboard")
    assert "../docs/session-parity-dashboard.md" in nav_item.source_docs
    assert "../examples/session_runtime/session_parity_dashboard.json" in nav_item.source_docs
    assert "docs_dashboard" in manifest.required_sections
    assert validate_nav_against_manifest(nav, manifest) == []


def test_session_parity_dashboard_contains_no_secret_or_private_path() -> None:
    combined = "\n".join(
        [
            DASHBOARD.read_text(encoding="utf-8"),
            (ROOT / "docs" / "session-parity-dashboard.md").read_text(
                encoding="utf-8"
            ),
            (ROOT / "docs-site" / "pages" / "session-parity.md").read_text(
                encoding="utf-8"
            ),
        ]
    )

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_"]
    for marker in forbidden:
        assert marker not in combined
    assert "sk-" not in combined
    assert "observed " + "success" not in combined.lower()
