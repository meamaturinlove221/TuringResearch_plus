from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_v0_7_case_study_related_contracts_exist() -> None:
    required = [
        "contracts/dataset_license_compliance.yaml",
        "contracts/local_research_vault_ui.yaml",
        "contracts/paper_deep_review.yaml",
        "contracts/case_study_builder.yaml",
    ]

    for relative_path in required:
        assert (ROOT / relative_path).exists(), relative_path


def test_case_study_contract_preserves_public_safety_boundary() -> None:
    text = _read("contracts/case_study_builder.yaml")

    assert "requires_human_review: true" in text
    assert "no_sparseconv3d_success_claim: true" in text
    assert "no_private_path_leak: true" in text
    assert "no_network: true" in text


def test_compliance_contract_does_not_overclaim_legal_review() -> None:
    text = _read("contracts/dataset_license_compliance.yaml")

    assert "requires_human_review: true" in text
    assert "no_legal_advice: true" in text
    assert "no_license_download: true" in text
    assert "github_code_missing_license: unknown until reviewed" in text


def test_deep_review_contract_blocks_final_conclusions() -> None:
    text = _read("contracts/paper_deep_review.yaml")

    assert "requires_human_review: true" in text
    assert "no_pdf_download: true" in text
    assert "no_final_conclusions: true" in text
    assert "fake_fixture_not_citation_grade: true" in text


def test_vault_ui_contract_marks_graph_as_review_surface() -> None:
    text = _read("contracts/local_research_vault_ui.yaml")

    assert "requires_human_review: true" in text
    assert "no_server: true" in text
    assert "no_network: true" in text
    assert "graph_not_truth: true" in text
