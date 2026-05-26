from __future__ import annotations

import pytest

from turing_research_plus.adapters.models import SourceMetadata
from turing_research_plus.scholar_pipeline.models import (
    ScholarPipelineResult,
    ScholarPipelineStatus,
    ScholarSourcePriority,
    ThreePassReadingPlan,
)


def test_scholar_result_rejects_human_verified_source_metadata() -> None:
    with pytest.raises(ValueError, match="human verified"):
        ScholarPipelineResult(
            query="VGGT",
            source_priority=[ScholarSourcePriority.CACHED_MARKDOWN],
            selected_source=ScholarSourcePriority.SEMANTIC_SCHOLAR,
            status=ScholarPipelineStatus.FAKE_RESULT,
            source_metadata=[SourceMetadata(provider="fake", human_verified=True)],
        )


def test_three_pass_plan_cannot_be_human_verified_by_template() -> None:
    with pytest.raises(ValueError, match="human verified"):
        ThreePassReadingPlan(
            paper_id="p",
            title="Paper",
            pass_1=["scan"],
            pass_2=["read"],
            pass_3=["understand"],
            human_verified=True,
        )
