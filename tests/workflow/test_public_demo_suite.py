from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo"


def test_public_demo_suite_contains_required_files() -> None:
    required = [
        "README.md",
        "demo_research_intent.md",
        "demo_evidence_ledger.json",
        "demo_artifact_index.md",
        "demo_visual_inventory.md",
        "demo_related_work.md",
        "demo_advisor_pack.md",
        "demo_dashboard.html",
    ]

    for filename in required:
        assert (DEMO / filename).exists()


def test_public_demo_evidence_ledger_is_demo_only() -> None:
    payload = json.loads((DEMO / "demo_evidence_ledger.json").read_text(encoding="utf-8"))

    assert payload["status"] == "demo-only"
    assert payload["requires_human_review"] is True
    statuses = {entry["status"] for entry in payload["entries"]}
    assert {"planned", "fake-data", "not-enough-evidence"} <= statuses
    assert "observed" not in statuses


def test_public_demo_documents_cover_required_capabilities() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DEMO.glob("*.*"))
    lowered = combined.lower()

    required_terms = [
        "evidence ledger",
        "artifact audit",
        "visual audit",
        "method card",
        "related work positioning",
        "route dsl",
        "failure taxonomy",
        "advisor pack",
        "dashboard",
    ]

    for term in required_terms:
        assert term in lowered
    assert "demo only" in lowered


def test_public_demo_has_no_private_or_secret_patterns() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DEMO.glob("*.*"))
    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "SMPLX_",
        "BEGIN " + "PRIVATE KEY",
        "raw dataset payload",
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    for item in forbidden:
        assert item not in combined
    assert not token_like.search(combined)


def test_public_demo_dashboard_is_static_and_demo_only() -> None:
    html = (DEMO / "demo_dashboard.html").read_text(encoding="utf-8")

    assert "demo only" in html
    assert "not an experiment result" in html
    assert "<script" not in html.lower()
    assert "http://" not in html
    assert "https://" not in html
