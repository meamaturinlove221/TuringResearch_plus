from __future__ import annotations

import json
import re
from pathlib import Path

from turing_research_plus.scholar_pipeline import build_heavy_pdf_backend_slot
from turing_research_plus.scholar_tools import (
    PaperContentToolRequest,
    PaperReadingToolRequest,
    PaperReferenceToolRequest,
    run_paper_content_tool,
    run_paper_reading_tool,
    run_paper_reference_tool,
)

ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_scholar_production_gate_required_docs_exist() -> None:
    required = [
        "docs/scholar-production-tool-list.md",
        "docs/scholar-pipeline-public-readme-section.md",
        "docs/scholar-mcp-test-results-fake.md",
        "docs/paper-content-e2e.md",
        "docs/paper-reference-e2e.md",
        "docs/three-pass-reading-e2e.md",
        "docs/keshav-reading-template.md",
        "docs/optional-heavy-pdf-backend-slot.md",
        "docs/scholar-production-parity-gate-report.md",
        "docs/scholar-production-parity-go-no-go.md",
    ]

    for path in required:
        assert (ROOT / path).exists(), path


def test_scholar_production_gate_tool_list_passes() -> None:
    combined = "\n".join(
        [
            _read("docs/scholar-production-tool-list.md"),
            _read("examples/scholar_demo/TOOL_LIST.md"),
        ]
    )

    for tool in [
        "scholar.paper_searching",
        "scholar.paper_content",
        "scholar.paper_reference",
        "scholar.paper_reading",
    ]:
        assert tool in combined

    assert "fake/default" in combined
    assert "human review required" in combined


def test_scholar_production_gate_paper_content_e2e_passes() -> None:
    demo = ROOT / "examples" / "scholar_demo" / "paper_content_e2e"
    descriptor = json.loads((demo / "method_card_input.json").read_text("utf-8"))

    result = run_paper_content_tool(
        PaperContentToolRequest(
            paper_id=descriptor["paper_id"],
            title=descriptor["title"],
            cached_markdown_path=demo / "cached_paper.md",
        )
    )

    assert result.tool_name == "scholar.paper_content"
    assert result.cache_hit is True
    assert result.references_section_present is True
    assert result.release_blocker is False
    assert result.requires_human_review is True


def test_scholar_production_gate_paper_reference_e2e_passes() -> None:
    metadata = json.loads(
        (
            ROOT
            / "examples"
            / "scholar_demo"
            / "paper_reference_e2e"
            / "paper_metadata.json"
        ).read_text("utf-8")
    )

    result = run_paper_reference_tool(
        PaperReferenceToolRequest(paper_id=metadata["paper_id"], limit=3)
    )

    assert result.tool_name == "scholar.paper_reference"
    assert result.source == "semantic_scholar"
    assert len(result.references) == 3
    assert result.release_blocker is False
    assert result.requires_human_review is True


def test_scholar_production_gate_three_pass_reading_e2e_passes() -> None:
    result = run_paper_reading_tool(
        PaperReadingToolRequest(
            paper_id="fake-three-pass-reading",
            title="Fake Three-Pass Reading Paper",
        )
    )

    assert result.tool_name == "scholar.paper_reading"
    assert result.pass_1
    assert result.pass_2
    assert result.pass_3
    assert result.release_blocker is False
    assert result.requires_human_review is True


def test_scholar_production_gate_optional_backend_slot_passes() -> None:
    slot = build_heavy_pdf_backend_slot()

    assert slot.interface_only is True
    assert slot.implementation_present is False
    assert slot.dependency_required is False
    assert slot.ocr_enabled is False
    assert slot.large_pdf_processing is False
    assert slot.release_blocker is False


def test_scholar_production_gate_keeps_mineru_unimplemented() -> None:
    combined = "\n".join(
        [
            _read("docs/optional-heavy-pdf-backend-slot.md"),
            _read("contracts/heavy_pdf_backend_slot.yaml"),
            _read("docs/scholar-production-parity-gate-report.md"),
            _read("docs/scholar-production-parity-go-no-go.md"),
        ]
    ).lower()

    assert "mineru not implemented" in combined
    assert "mineru implementation;" in combined
    assert "ocr default" in combined
    assert "large pdf processing" in combined


def test_scholar_production_gate_no_fake_citation_verified() -> None:
    combined = "\n".join(
        [
            _read("docs/scholar-production-tool-list.md"),
            _read("docs/paper-reference-e2e.md"),
            _read("docs/three-pass-reading-e2e.md"),
            _read("docs/scholar-production-parity-gate-report.md"),
            _read("docs/scholar-production-parity-go-no-go.md"),
        ]
    ).lower()

    assert "no fake citation is marked as verified" in combined
    assert "fake citation is verified" not in combined
    assert "final paper conclusion" in combined


def test_scholar_production_gate_has_no_secrets_or_private_paths() -> None:
    combined = "\n".join(
        [
            _read("docs/scholar-production-parity-gate-report.md"),
            _read("docs/scholar-production-parity-go-no-go.md"),
            _read("docs/paper-content-e2e.md"),
            _read("docs/paper-reference-e2e.md"),
            _read("docs/three-pass-reading-e2e.md"),
            _read("docs/optional-heavy-pdf-backend-slot.md"),
        ]
    )

    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assert not token_like.search(combined)
    assert "Tuling" + "Research" not in combined
    assert "D:" + "/vggt" not in combined
    assert "local_project_links.yaml" not in combined
