from __future__ import annotations

from pathlib import Path

from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo" / "v1_3_original_parity_demo"


def _read(name: str) -> str:
    return (DEMO / name).read_text(encoding="utf-8")


def test_v1_3_original_parity_public_demo_files_exist() -> None:
    required_files = [
        "README.md",
        "session_runtime_demo.md",
        "scholar_web_demo.md",
        "research_catalog_demo.md",
        "stress_convergence_demo.md",
    ]

    for name in required_files:
        assert (DEMO / name).exists(), name


def test_v1_3_original_parity_public_demo_covers_required_surfaces() -> None:
    combined = "\n".join(
        [
            _read("README.md"),
            _read("session_runtime_demo.md"),
            _read("scholar_web_demo.md"),
            _read("research_catalog_demo.md"),
            _read("stress_convergence_demo.md"),
        ]
    )
    lower = combined.lower()

    required = [
        "Session runtime replay",
        "preflight",
        "context pack",
        "fake transfer",
        "return verifier",
        "Scholar / Web parity",
        "MCP",
        "campaign execution trace",
        "Research Catalog dashboard",
        "vault wiki export demo",
        "ontology runbook demo",
        "stress scenario library",
        "ARIS remains deferred",
    ]
    for term in required:
        assert term in combined
    assert "convergence decision report" in lower


def test_v1_3_original_parity_public_demo_is_fake_only_and_review_only() -> None:
    combined = "\n".join(
        [
            _read("README.md"),
            _read("session_runtime_demo.md"),
            _read("scholar_web_demo.md"),
            _read("research_catalog_demo.md"),
            _read("stress_convergence_demo.md"),
        ]
    )

    required_boundaries = [
        "fake/demo only",
        "no live provider calls",
        "no remote command execution",
        "no automatic experiment execution",
        "no automatic Evidence Ledger mutation",
        "no fake/demo result promotion",
        "human review required",
        "Passing the demo does not mean a real experiment was run.",
    ]
    for boundary in required_boundaries:
        assert boundary in combined


def test_v1_3_original_parity_public_demo_has_no_sensitive_payload() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DEMO.glob("*.md"))
    lower = combined.lower()

    forbidden = [
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
    for marker in forbidden:
        assert marker.lower() not in lower

    assert "fake/demo result cannot become observed evidence" in combined


def test_v1_3_original_parity_public_demo_privacy_gate() -> None:
    report = scan_privacy_paths([DEMO])

    assert report.requires_human_review is True
    assert report.release_blocker is False
    assert report.findings == []
