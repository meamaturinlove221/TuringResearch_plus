from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo" / "v1_2_demo"


def _read(relative: str) -> str:
    return (DEMO / relative).read_text(encoding="utf-8")


def test_v1_2_public_demo_files_exist_and_cover_required_topics() -> None:
    required_files = [
        "README.md",
        "research_catalog_demo.md",
        "reference_parity_demo.md",
        "stress_test_demo.md",
    ]
    for name in required_files:
        assert (DEMO / name).exists(), name

    combined = "\n".join(_read(name) for name in required_files)
    for term in [
        "Research Catalog",
        "Reference Parity Dashboard",
        "Stress Test",
        "fake/demo only",
        "human review",
    ]:
        assert term in combined


def test_v1_2_public_demo_reference_dashboard_data_is_available() -> None:
    dashboard = ROOT / "examples" / "public_demo" / "reference_parity_dashboard.json"
    data = json.loads(dashboard.read_text(encoding="utf-8"))

    assert data["dashboard_id"] == "reference-parity-v1.2"
    assert data["status"] == "public-demo"
    assert data["requires_human_review"] is True
    assert any(item["id"] == "aris" for item in data["deferred"])
    assert "automatic experiment execution" in data["rejected_unsafe_features"]


def test_v1_2_public_demo_has_no_sensitive_payload_or_overclaim() -> None:
    combined = "\n".join(
        [
            _read("README.md"),
            _read("research_catalog_demo.md"),
            _read("reference_parity_demo.md"),
            _read("stress_test_demo.md"),
            (ROOT / "docs" / "v1.2.0-public-demo-refresh.md").read_text(
                encoding="utf-8"
            ),
        ]
    )
    lower = combined.lower()

    forbidden_literals = [
        "D:/vggt",
        "D:\\vggt",
        "local_project_links.yaml",
        "ghp_",
        "sk-",
        "SMPL-X",
        "SMPLX_",
        "raw data included",
        "real patient data",
        "experiment succeeded",
        "observed result",
        "SparseConv3D success",
    ]
    for marker in forbidden_literals:
        assert marker.lower() not in lower

    assert "fake/demo only" in lower
    assert "passing the demo does not mean a real experiment was run" in lower
    assert "no verified live result write" in lower


def test_v1_2_public_demo_docs_report_exists() -> None:
    report = ROOT / "docs" / "v1.2.0-public-demo-refresh.md"

    assert report.exists()
    text = report.read_text(encoding="utf-8")
    assert "Research Catalog routing" in text
    assert "Reference parity dashboard" in text
    assert "Stress-test review" in text
