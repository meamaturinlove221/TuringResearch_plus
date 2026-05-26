from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.case_study.gallery import (
    load_case_gallery_manifest,
    render_case_gallery_markdown,
)
from turing_research_plus.paper_write.citation_status_guard import (
    parse_citation_status_report,
)
from turing_research_plus.paper_write.claim_guard import evaluate_paper_claims
from turing_research_plus.paper_write.draft_assembly import assemble_paper_draft_beta
from turing_research_plus.paper_write.draft_package import export_paper_draft_package
from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
SCAFFOLD = ROOT / "examples" / "vggt-human-prior-survey" / "paper_scaffold"
PROJECTS = ROOT / "examples" / "public_demo" / "projects"
GALLERY = ROOT / "examples" / "public_demo" / "case_gallery"
MANIFEST = GALLERY / "gallery_manifest.yaml"

NEW_PROJECT_IDS = [
    "robotics_paper_survey_demo",
    "medical_imaging_experiment_demo",
    "software_tooling_research_demo",
    "multimodal_model_eval_demo",
]


def test_v1_1_paper_demo_integration_exports_review_package(tmp_path: Path) -> None:
    package = assemble_paper_draft_beta(SCAFFOLD)
    outputs = export_paper_draft_package(package, tmp_path)

    assert {path.name for path in outputs} == {
        "paper_draft_beta.md",
        "missing_evidence_report.md",
        "unsafe_claim_report.md",
        "citation_status_report.md",
    }
    draft = (tmp_path / "paper_draft_beta.md").read_text(encoding="utf-8")
    unsafe = (tmp_path / "unsafe_claim_report.md").read_text(encoding="utf-8")
    citations = (tmp_path / "citation_status_report.md").read_text(encoding="utf-8")

    assert "This is not a final paper." in draft
    assert "Result tables allowed: `false`" in draft
    assert "Fake observed claim blocked: `true`" in unsafe
    assert "Fabricated citation blocked: `true`" in citations
    assert "Risky Unblocked Claims" not in unsafe


def test_v1_1_paper_demo_integration_claim_and_citation_guards_work() -> None:
    claim_report = evaluate_paper_claims(
        {
            "blocked": "Do not claim SparseConv3D success without backend evidence.",
            "risky": "SparseConv3D success improves all benchmark results.",
        }
    )
    citation_report = parse_citation_status_report(
        (SCAFFOLD / "citation_safety_report.md").read_text(encoding="utf-8")
    )

    assert claim_report.blocked_claims
    assert claim_report.risky_unblocked_claims
    assert citation_report.fabricated_citation_blocked is True
    assert citation_report.blocked_citations
    assert all(not citation.citation_grade for citation in citation_report.citations)


def test_v1_1_paper_demo_integration_public_cases_pass() -> None:
    for project_id in NEW_PROJECT_IDS:
        project = PROJECTS / project_id
        ledger = json.loads((project / "evidence_ledger.json").read_text(encoding="utf-8"))
        dashboard = json.loads((project / "dashboard_data.json").read_text(encoding="utf-8"))
        statuses = {entry["status"] for entry in ledger["entries"]}

        assert ledger["status"] == "demo-only"
        assert "observed" not in statuses
        assert dashboard["read_only"] is True
        assert dashboard["no_secrets"] is True
        assert dashboard["no_raw_data"] is True
        assert dashboard["no_private_path"] is True


def test_v1_1_paper_demo_integration_case_gallery_builds() -> None:
    manifest = load_case_gallery_manifest(MANIFEST)
    markdown = render_case_gallery_markdown(manifest)

    assert len(manifest.cases) >= 5
    for project_id in NEW_PROJECT_IDS:
        assert project_id in markdown
    assert "vggt_public_safe_case" in markdown
    assert "Demo outputs are not observed research evidence." in markdown


def test_v1_1_paper_demo_integration_privacy_gate_passes() -> None:
    scan_roots = [
        SCAFFOLD / "draft_beta",
        GALLERY,
        *[PROJECTS / project_id for project_id in NEW_PROJECT_IDS],
    ]
    report = scan_privacy_paths(scan_roots)

    assert report.release_blocker is False
    assert report.findings == []
    assert report.requires_human_review is True


def test_v1_1_paper_demo_integration_has_no_public_overclaim_payloads() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for root in [SCAFFOLD / "draft_beta", GALLERY, *[PROJECTS / p for p in NEW_PROJECT_IDS]]
        for path in root.rglob("*")
        if path.is_file()
    )

    assert "D:/vggt" not in combined
    assert "D:\\\\vggt" not in combined
    assert "local_project_links.yaml" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "\"status\": \"observed\"" not in combined
    assert "SparseConv3D integration succeeded" not in combined
