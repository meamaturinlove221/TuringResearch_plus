from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DEMO = ROOT / "examples" / "public_demo"
PROJECTS = [
    "vggt_like_demo",
    "paper_survey_demo",
    "software_tooling_demo",
]


def test_v1_quickstart_docs_and_demo_entrypoint_exist() -> None:
    required = [
        ROOT / "docs" / "v1.0.0-quickstart.md",
        ROOT / "docs" / "v1.0.0-quickstart-troubleshooting.md",
        ROOT / "docs" / "v1.0.0-demo-expected-output.md",
        PUBLIC_DEMO / "QUICKSTART.md",
        PUBLIC_DEMO / "README.md",
        PUBLIC_DEMO / "dashboard" / "index.html",
    ]

    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]

    assert missing == []


def test_v1_quickstart_references_required_demo_steps() -> None:
    text = (ROOT / "docs" / "v1.0.0-quickstart.md").read_text(encoding="utf-8")
    lowered = text.lower()

    required_terms = [
        "install",
        "public demo",
        "evidence ledger",
        "dashboard",
        "advisor markdown bundle",
        "related work",
        "live adapters are disabled by default",
    ]

    for term in required_terms:
        assert term in lowered


def test_v1_public_demo_project_files_are_present() -> None:
    required_files = [
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
        for filename in required_files:
            assert (project / filename).exists(), f"{project_id}/{filename}"


def test_v1_public_quickstart_ledgers_are_demo_only_not_observed() -> None:
    ledger_paths = [PUBLIC_DEMO / "demo_evidence_ledger.json"]
    ledger_paths.extend(
        PUBLIC_DEMO / "projects" / project_id / "evidence_ledger.json"
        for project_id in PROJECTS
    )

    for path in ledger_paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        statuses = {entry["status"] for entry in payload["entries"]}

        assert payload["status"] == "demo-only"
        assert payload["requires_human_review"] is True
        assert "observed" not in statuses
        assert statuses <= {"planned", "fake-data", "not-enough-evidence"}


def test_v1_public_quickstart_has_no_private_or_live_requirements() -> None:
    paths = [
        ROOT / "docs" / "v1.0.0-quickstart.md",
        ROOT / "docs" / "v1.0.0-quickstart-troubleshooting.md",
        ROOT / "docs" / "v1.0.0-demo-expected-output.md",
        PUBLIC_DEMO / "QUICKSTART.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    lowered = text.lower()
    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "SMPLX" + "_",
        "local_project_links" + ".yaml",
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    for item in forbidden:
        assert item not in text
    assert not token_like.search(text)
    assert "no real api key" in lowered or "does not require api keys" in lowered
    assert "no live adapter by default" in lowered or "live adapters are disabled" in lowered
