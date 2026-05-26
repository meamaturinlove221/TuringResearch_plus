from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_digest.three_pass import build_three_pass_notes
from turing_research_plus.scholar_tools import (
    PaperReadingToolRequest,
    run_paper_reading_tool,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "scholar_demo" / "three_pass_reading"


def test_three_pass_reading_e2e_builds_review_outputs() -> None:
    cached_note = (DEMO / "cached_note.md").read_text("utf-8")

    result = run_paper_reading_tool(
        PaperReadingToolRequest(
            paper_id="fake-three-pass-reading",
            title="Fake Three-Pass Reading Paper",
        )
    )
    notes = build_three_pass_notes(cached_note)

    assert result.tool_name == "scholar.paper_reading"
    assert result.paper_id == "fake-three-pass-reading"
    assert result.pass_1
    assert result.pass_2
    assert result.pass_3
    assert result.outputs == [
        "method card",
        "collision notes",
        "borrow/not-copy list",
        "VGGT mapping",
    ]
    assert result.final_conclusion_generated is False
    assert result.camera_ready_text_generated is False
    assert result.human_verified is False
    assert result.requires_human_review is True
    assert result.release_blocker is False

    assert "Bird's-eye scan" in notes.pass1_summary
    assert notes.pass2_notes
    assert notes.pass3_deep_notes
    assert notes.requires_real_paper_review is True


def test_three_pass_reading_demo_exports_expected_sections() -> None:
    combined = "\n".join(
        [
            (DEMO / "README.md").read_text("utf-8"),
            (DEMO / "reading_plan.md").read_text("utf-8"),
            (DEMO / "five_cs_report.md").read_text("utf-8"),
            (DEMO / "method_mapping.md").read_text("utf-8"),
            (DEMO / "limitations.md").read_text("utf-8"),
            (ROOT / "docs" / "three-pass-reading-e2e.md").read_text("utf-8"),
            (ROOT / "docs" / "keshav-reading-template.md").read_text("utf-8"),
        ]
    )

    for required in [
        "Pass 1: Bird's-Eye",
        "Pass 2: Content Grasp",
        "Pass 3: Deep Understanding",
        "Five Cs",
        "method mapping",
        "limitations",
        "requires human review",
    ]:
        assert required.lower() in combined.lower()

    for forbidden in [
        "D:/vggt",
        "D:\\vggt",
        "local_project_links.yaml",
        "ghp_",
        "sk-",
    ]:
        assert forbidden not in combined


def test_three_pass_reading_demo_does_not_claim_final_review() -> None:
    combined = "\n".join(path.read_text("utf-8") for path in DEMO.glob("*.md"))

    assert "no final paper conclusion" in combined
    assert "No complete paper reading claim" in combined
    assert "verified citations" not in combined.lower()
    assert "camera-ready paper text" in combined
