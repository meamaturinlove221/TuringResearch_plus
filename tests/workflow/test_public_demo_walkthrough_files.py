from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DEMO = ROOT / "examples" / "public_demo"
PROJECTS = ["vggt_like_demo", "paper_survey_demo", "software_tooling_demo"]

WALKTHROUGH_DOCS = [
    ROOT / "docs" / "v1.0.0-public-demo-walkthrough.md",
    ROOT / "docs" / "v1.0.0-demo-script.md",
    PUBLIC_DEMO / "WALKTHROUGH.md",
    PUBLIC_DEMO / "EXPECTED_OUTPUTS.md",
]

REQUIRED_TOPICS = [
    "workspace",
    "evidence ledger",
    "artifact audit",
    "visual audit",
    "paper method",
    "related work",
    "route dsl",
    "advisor pack",
    "dashboard",
    "privacy gate",
]


def test_public_demo_walkthrough_files_exist() -> None:
    missing = [str(path.relative_to(ROOT)) for path in WALKTHROUGH_DOCS if not path.exists()]

    assert missing == []


def test_public_demo_walkthrough_covers_required_topics() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in WALKTHROUGH_DOCS)

    for topic in REQUIRED_TOPICS:
        assert topic in combined


def test_public_demo_walkthrough_boundaries_are_explicit() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in WALKTHROUGH_DOCS)
    required = [
        "demo only",
        "no network",
        "no api key",
        "no real vggt",
        "human review",
        "not observed",
    ]

    for phrase in required:
        assert phrase in combined


def test_public_demo_expected_files_are_present() -> None:
    root_files = [
        "README.md",
        "QUICKSTART.md",
        "WALKTHROUGH.md",
        "EXPECTED_OUTPUTS.md",
        "demo_manifest.yaml",
        "demo_evidence_ledger.json",
        "demo_artifact_index.md",
        "demo_visual_inventory.md",
        "demo_related_work.md",
        "demo_advisor_pack.md",
        "demo_dashboard.html",
        "demo_dashboard_refined.html",
        "dashboard/index.html",
    ]
    project_files = [
        "README.md",
        "north_star.md",
        "evidence_ledger.json",
        "artifact_index.md",
        "related_work.md",
        "advisor_pack.md",
        "dashboard.html",
    ]

    for filename in root_files:
        assert (PUBLIC_DEMO / filename).exists(), filename
    for project_id in PROJECTS:
        for filename in project_files:
            assert (PUBLIC_DEMO / "projects" / project_id / filename).exists(), (
                f"{project_id}/{filename}"
            )


def test_public_demo_walkthrough_ledgers_remain_demo_only() -> None:
    ledgers = [PUBLIC_DEMO / "demo_evidence_ledger.json"]
    ledgers.extend(
        PUBLIC_DEMO / "projects" / project / "evidence_ledger.json"
        for project in PROJECTS
    )

    for path in ledgers:
        payload = json.loads(path.read_text(encoding="utf-8"))
        statuses = {entry["status"] for entry in payload["entries"]}

        assert payload["status"] == "demo-only"
        assert payload["requires_human_review"] is True
        assert "observed" not in statuses
        assert statuses <= {"planned", "fake-data", "not-enough-evidence"}


def test_public_demo_walkthrough_has_no_sensitive_payloads() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in WALKTHROUGH_DOCS
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
