from __future__ import annotations

import pytest

from turing_research_plus.scholar_tools import (
    PaperReadingToolRequest,
    run_paper_reading_tool,
)


def test_paper_reading_tool_builds_review_plan() -> None:
    result = run_paper_reading_tool(
        PaperReadingToolRequest(paper_id="paper-1", title="Paper")
    )

    assert result.tool_name == "scholar.paper_reading"
    assert result.pass_1
    assert result.pass_2
    assert result.pass_3
    assert result.final_conclusion_generated is False
    assert result.camera_ready_text_generated is False
    assert result.human_verified is False
    assert result.requires_human_review is True
    assert result.release_blocker is False


def test_paper_reading_tool_rejects_final_paper_outputs() -> None:
    with pytest.raises(ValueError, match="final conclusions"):
        PaperReadingToolRequest(
            paper_id="paper-1",
            title="Paper",
            generate_final_conclusion=True,
        )
    with pytest.raises(ValueError, match="camera-ready"):
        PaperReadingToolRequest(
            paper_id="paper-1",
            title="Paper",
            camera_ready_text=True,
        )
