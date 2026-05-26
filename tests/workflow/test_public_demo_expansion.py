from __future__ import annotations

import json
import re
from pathlib import Path

from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DEMO = ROOT / "examples" / "public_demo"
PROJECTS = PUBLIC_DEMO / "projects"
PROJECT_IDS = [
    "vggt_like_demo",
    "paper_survey_demo",
    "software_tooling_demo",
]
REQUIRED_PROJECT_FILES = [
    "README.md",
    "north_star.md",
    "evidence_ledger.json",
    "artifact_index.md",
    "related_work.md",
    "advisor_pack.md",
    "dashboard.html",
]


def test_public_demo_expansion_projects_have_required_files() -> None:
    for project_id in PROJECT_IDS:
        project = PROJECTS / project_id
        assert project.exists()
        for filename in REQUIRED_PROJECT_FILES:
            assert (project / filename).exists(), f"{project_id}/{filename}"


def test_public_demo_expansion_ledgers_are_demo_only() -> None:
    for project_id in PROJECT_IDS:
        payload = json.loads(
            (PROJECTS / project_id / "evidence_ledger.json").read_text(
                encoding="utf-8"
            )
        )

        assert payload["project_id"] == project_id
        assert payload["status"] == "demo-only"
        assert payload["requires_human_review"] is True
        statuses = {entry["status"] for entry in payload["entries"]}
        assert "observed" not in statuses
        assert {"planned", "fake-data", "not-enough-evidence"} <= statuses


def test_public_demo_expansion_documents_are_demo_marked() -> None:
    for project_id in PROJECT_IDS:
        project = PROJECTS / project_id
        combined = "\n".join(
            (project / filename).read_text(encoding="utf-8")
            for filename in REQUIRED_PROJECT_FILES
        ).lower()

        assert "demo only" in combined
        assert "requires human review" in combined
        assert "not an experiment result" in combined or "not final paper text" in combined


def test_public_demo_workspace_links_project_fixtures() -> None:
    workspace = (PUBLIC_DEMO / "workspace_demo" / "workspace.yaml").read_text(
        encoding="utf-8"
    )

    assert "workspace_id: public_demo_workspace" in workspace
    assert "privacy_level: public-demo" in workspace
    for project_id in PROJECT_IDS:
        assert f"project_id: {project_id}" in workspace
        assert f"../projects/{project_id}" in workspace


def test_public_demo_dashboard_index_is_static_and_links_projects() -> None:
    dashboard = (PUBLIC_DEMO / "dashboard" / "index.html").read_text(
        encoding="utf-8"
    )

    assert "demo only" in dashboard
    assert "safe demo mode" in dashboard
    assert "not an experiment result" in dashboard
    assert "<script" not in dashboard.lower()
    assert "http://" not in dashboard
    assert "https://" not in dashboard
    for project_id in PROJECT_IDS:
        assert f"../projects/{project_id}/dashboard.html" in dashboard


def test_public_demo_expansion_privacy_gate_is_clean() -> None:
    report = scan_privacy_paths([PUBLIC_DEMO])

    assert report.release_blocker is False
    assert report.findings == []
    assert report.requires_human_review is True


def test_public_demo_expansion_has_no_forbidden_public_payloads() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in PUBLIC_DEMO.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".html"}
    )
    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "SMPL" + "-X",
        "SMPLX" + "_",
        "BEGIN " + "PRIVATE KEY",
        "local_project_links" + ".yaml",
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    for item in forbidden:
        assert item not in combined
    assert not token_like.search(combined)


def test_public_demo_project_dashboards_are_static() -> None:
    for project_id in PROJECT_IDS:
        html = (PROJECTS / project_id / "dashboard.html").read_text(encoding="utf-8")

        assert "demo only" in html
        assert "<script" not in html.lower()
        assert "http://" not in html
        assert "https://" not in html
