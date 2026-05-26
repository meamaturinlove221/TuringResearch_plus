from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"
PUBLIC_DEMO = ROOT / "examples" / "public_demo"


def test_v0_7_vault_compliance_case_study_chain_is_review_safe() -> None:
    compliance = (VGGT / "compliance" / "compliance_report.md").read_text(
        encoding="utf-8"
    )
    case_draft = (
        VGGT / "public_case_study" / "case_study_draft.md"
    ).read_text(encoding="utf-8")
    redaction = (
        VGGT / "public_case_study" / "redaction_report.md"
    ).read_text(encoding="utf-8")
    claim_guard = (
        VGGT / "public_case_study" / "claim_safety_report.md"
    ).read_text(encoding="utf-8")
    vault_ui = (VGGT / "vault_ui" / "index.html").read_text(encoding="utf-8")
    deep_review = (
        VGGT / "paper_deep_review" / "neuralbody_review_checklist.md"
    ).read_text(encoding="utf-8")

    assert "not legal advice" in compliance.lower()
    assert "restricted" in compliance
    assert "requires human review" in compliance.lower()
    assert "Sanitized: `true`" in redaction
    assert "Safe to publish: `true`" in claim_guard
    assert "Unsupported Experiment Claims" in claim_guard
    assert "Do not claim SparseConv3D success" in case_draft
    assert "It does not claim experiment success." in case_draft
    assert "Graph is not truth" in vault_ui
    assert "No network" in vault_ui
    assert "Reading status: `needs-real-paper`" in deep_review
    assert "No final paper conclusion is generated" in deep_review


def test_v0_7_public_demo_expansion_remains_privacy_safe() -> None:
    report = scan_privacy_paths([PUBLIC_DEMO])

    assert report.release_blocker is False
    assert report.findings == []
    assert report.requires_human_review is True


def test_v0_7_public_demo_ledgers_do_not_mark_fake_results_observed() -> None:
    for ledger in (PUBLIC_DEMO / "projects").glob("*/evidence_ledger.json"):
        payload = json.loads(ledger.read_text(encoding="utf-8"))
        statuses = {entry["status"] for entry in payload["entries"]}

        assert payload["status"] == "demo-only"
        assert payload["requires_human_review"] is True
        assert "observed" not in statuses


def test_v0_7_public_outputs_do_not_leak_private_paths_or_secrets() -> None:
    files = [
        VGGT / "public_case_study" / "case_study_draft.md",
        VGGT / "public_case_study" / "redaction_report.md",
        VGGT / "public_case_study" / "claim_safety_report.md",
        VGGT / "vault_ui" / "index.html",
        VGGT / "paper_deep_review" / "neuralbody_review_checklist.md",
        *[path for path in PUBLIC_DEMO.rglob("*") if path.is_file()],
    ]
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in files
        if path.suffix.lower() in {".md", ".json", ".yaml", ".html"}
    )
    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "BEGIN " + "PRIVATE KEY",
        "local_project_links" + ".yaml",
        "SMPLX" + "_",
    ]

    for item in forbidden:
        assert item not in combined
    assert "sk-" + "demo" not in combined


def test_v0_7_case_study_does_not_overclaim_license_or_success() -> None:
    compliance = (VGGT / "compliance" / "compliance_report.md").read_text(
        encoding="utf-8"
    )
    case_draft = (
        VGGT / "public_case_study" / "case_study_draft.md"
    ).read_text(encoding="utf-8")

    assert "not legal advice" in compliance.lower()
    assert "license restricted" in compliance
    assert "unknown" in compliance
    assert "Do not claim SparseConv3D success" in case_draft
    assert "What Not To Claim" in case_draft
    assert "experiment success" in case_draft
