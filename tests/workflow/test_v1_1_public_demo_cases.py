from __future__ import annotations

import json
import re
from pathlib import Path

from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "examples" / "public_demo" / "projects"

NEW_PROJECT_IDS = [
    "robotics_paper_survey_demo",
    "medical_imaging_experiment_demo",
    "software_tooling_research_demo",
    "multimodal_model_eval_demo",
]

REQUIRED_FILES = [
    "README.md",
    "north_star.md",
    "evidence_ledger.json",
    "artifact_index.md",
    "related_work.md",
    "route_plan.md",
    "advisor_pack.md",
    "dashboard_data.json",
    "privacy_note.md",
]


def test_v1_1_public_demo_cases_have_required_files() -> None:
    for project_id in NEW_PROJECT_IDS:
        project = PROJECTS / project_id
        assert project.exists(), project_id
        for filename in REQUIRED_FILES:
            assert (project / filename).exists(), f"{project_id}/{filename}"


def test_v1_1_public_demo_case_ledgers_are_demo_only() -> None:
    for project_id in NEW_PROJECT_IDS:
        payload = json.loads(
            (PROJECTS / project_id / "evidence_ledger.json").read_text(
                encoding="utf-8"
            )
        )
        statuses = {entry["status"] for entry in payload["entries"]}

        assert payload["project_id"] == project_id
        assert payload["status"] == "demo-only"
        assert payload["requires_human_review"] is True
        assert {"planned", "fake-data", "not-enough-evidence"} <= statuses
        assert "observed" not in statuses


def test_v1_1_public_demo_cases_mark_safety_boundaries() -> None:
    for project_id in NEW_PROJECT_IDS:
        project = PROJECTS / project_id
        combined = "\n".join(
            (project / filename).read_text(encoding="utf-8")
            for filename in REQUIRED_FILES
        ).lower()

        assert "demo only" in combined
        assert "requires human review" in combined
        assert "not an experiment result" in combined
        assert "no secrets" in combined
        assert "no raw data" in combined
        assert "no unsupported claims" in combined


def test_v1_1_public_demo_cases_have_dashboard_data() -> None:
    for project_id in NEW_PROJECT_IDS:
        payload = json.loads(
            (PROJECTS / project_id / "dashboard_data.json").read_text(
                encoding="utf-8"
            )
        )

        assert payload["project_id"] == project_id
        assert payload["status"] == "demo-only"
        assert payload["read_only"] is True
        assert payload["no_secrets"] is True
        assert payload["no_raw_data"] is True
        assert payload["no_private_path"] is True
        assert len(payload["cards"]) == 4


def test_v1_1_public_demo_cases_are_privacy_safe() -> None:
    report = scan_privacy_paths([*(PROJECTS / project_id for project_id in NEW_PROJECT_IDS)])

    assert report.release_blocker is False
    assert report.findings == []
    assert report.requires_human_review is True


def test_v1_1_public_demo_cases_have_no_forbidden_payloads() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for project_id in NEW_PROJECT_IDS
        for path in (PROJECTS / project_id).rglob("*")
        if path.is_file()
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
