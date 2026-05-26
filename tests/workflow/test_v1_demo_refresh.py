from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DEMO = ROOT / "examples" / "public_demo"
PROJECTS = ["vggt_like_demo", "paper_survey_demo", "software_tooling_demo"]


def test_v1_public_demo_manifest_and_required_files_exist() -> None:
    manifest = PUBLIC_DEMO / "demo_manifest.yaml"
    assert manifest.exists()

    required = [
        "README.md",
        "QUICKSTART.md",
        "demo_manifest.yaml",
        "demo_research_intent.md",
        "demo_evidence_ledger.json",
        "demo_artifact_index.md",
        "demo_visual_inventory.md",
        "demo_related_work.md",
        "demo_advisor_pack.md",
        "demo_dashboard.html",
        "demo_dashboard_refined.html",
        "dashboard/index.html",
    ]
    for item in required:
        assert (PUBLIC_DEMO / item).exists(), item


def test_v1_public_demo_projects_have_quickstart_surfaces() -> None:
    required = [
        "README.md",
        "north_star.md",
        "evidence_ledger.json",
        "artifact_index.md",
        "related_work.md",
        "advisor_pack.md",
        "dashboard.html",
    ]

    for project_id in PROJECTS:
        project = PUBLIC_DEMO / "projects" / project_id
        for filename in required:
            assert (project / filename).exists(), f"{project_id}/{filename}"


def test_v1_public_demo_dashboards_and_advisor_bundles_are_demo_marked() -> None:
    paths = [
        PUBLIC_DEMO / "dashboard" / "index.html",
        PUBLIC_DEMO / "demo_dashboard.html",
        PUBLIC_DEMO / "demo_dashboard_refined.html",
        PUBLIC_DEMO / "demo_advisor_pack.md",
    ]
    paths.extend(
        PUBLIC_DEMO / "projects" / project_id / "dashboard.html" for project_id in PROJECTS
    )
    paths.extend(
        PUBLIC_DEMO / "projects" / project_id / "advisor_pack.md" for project_id in PROJECTS
    )

    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        assert "demo" in text
        assert "not an experiment result" in text or "requires human review" in text


def test_v1_public_demo_ledgers_remain_fake_not_observed() -> None:
    ledgers = [PUBLIC_DEMO / "demo_evidence_ledger.json"]
    ledgers.extend(
        PUBLIC_DEMO / "projects" / project_id / "evidence_ledger.json" for project_id in PROJECTS
    )

    for path in ledgers:
        payload = json.loads(path.read_text(encoding="utf-8"))
        statuses = {entry["status"] for entry in payload["entries"]}

        assert payload["status"] == "demo-only"
        assert payload["requires_human_review"] is True
        assert "observed" not in statuses
        assert statuses <= {"planned", "fake-data", "not-enough-evidence"}


def test_v1_public_demo_refresh_has_no_sensitive_payloads() -> None:
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
        "local_project_links" + ".yaml",
        "BEGIN " + "PRIVATE KEY",
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    for item in forbidden:
        assert item not in combined
    assert not token_like.search(combined)
