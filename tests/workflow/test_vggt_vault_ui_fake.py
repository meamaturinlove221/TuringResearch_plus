from __future__ import annotations

from pathlib import Path

from turing_research_plus.vault_ui.tools import vault_ui_build_vggt

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "examples" / "vggt-human-prior-survey" / "vault_ui" / "index.html"


def test_vggt_vault_ui_fake_builds_static_html(tmp_path: Path) -> None:
    bundle = vault_ui_build_vggt(ROOT, write_files=False)

    assert bundle.project_name == "VGGT Human Prior Survey"
    assert bundle.safety_report.no_network is True
    assert bundle.safety_report.graph_not_truth is True
    assert "sparseconv_success_claim" in bundle.requires_review_nodes
    assert any(entry.title == "SparseConv3D" for entry in bundle.search_index)


def test_committed_vggt_vault_ui_fixture_preserves_boundaries() -> None:
    text = OUTPUT.read_text(encoding="utf-8")

    assert "VGGT Human Prior Survey Research Vault UI" in text
    assert "No server" in text
    assert "No login" in text
    assert "No network" in text
    assert "Graph is not truth" in text
    assert "SparseConv3D success claim lacks evidence-bearing support edge" in text
    assert "vault-search-index" in text
    assert "D:/vggt" not in text
