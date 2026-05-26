from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.markdown_bundle import (
    build_advisor_markdown_bundle,
)
from turing_research_plus.advisor_export.models import AdvisorMarkdownBundleRequest

ROOT = Path(__file__).resolve().parents[2]


def test_build_advisor_markdown_bundle_writes_required_files(tmp_path: Path) -> None:
    bundle = build_advisor_markdown_bundle(
        AdvisorMarkdownBundleRequest(
            output_dir=tmp_path,
            advisor_pack_dir=ROOT
            / "examples"
            / "vggt-human-prior-survey"
            / "advisor_pack",
            knowledge_pack_dir=ROOT
            / "examples"
            / "vggt-human-prior-survey"
            / "research_knowledge_pack",
        )
    )

    expected = {
        "advisor_report_source.md",
        "slides_outline.md",
        "figure_list.md",
        "table_list.md",
        "evidence_refs.md",
        "limitations.md",
        "next_actions.md",
        "manifest.yaml",
    }

    assert {Path(item.path).name for item in bundle.files} == expected
    assert (tmp_path / "README.md").exists()
    assert "No PDF or PPTX was generated" in (tmp_path / "README.md").read_text(
        encoding="utf-8"
    )
    assert "SparseConv3D success is not claimed" in (
        tmp_path / "advisor_report_source.md"
    ).read_text(encoding="utf-8")
    assert "generated_binary_exports: false" in (tmp_path / "manifest.yaml").read_text(
        encoding="utf-8"
    )


def test_build_advisor_markdown_bundle_can_plan_without_writing(tmp_path: Path) -> None:
    bundle = build_advisor_markdown_bundle(
        AdvisorMarkdownBundleRequest(
            output_dir=tmp_path,
            advisor_pack_dir=ROOT
            / "examples"
            / "vggt-human-prior-survey"
            / "advisor_pack",
            knowledge_pack_dir=ROOT
            / "examples"
            / "vggt-human-prior-survey"
            / "research_knowledge_pack",
        ),
        write_files=False,
    )

    assert bundle.output_dir == str(tmp_path)
    assert not (tmp_path / "manifest.yaml").exists()
