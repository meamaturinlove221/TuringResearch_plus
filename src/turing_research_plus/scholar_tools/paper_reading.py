"""Paper reading plan tool surface."""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.scholar_pipeline import (
    ThreePassReadingPlan,
    build_three_pass_reading_plan,
)


class PaperReadingToolRequest(BaseModel):
    """Request for a review-only paper reading plan."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    generate_final_conclusion: bool = False
    camera_ready_text: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_reading_boundary(self) -> Self:
        if self.generate_final_conclusion:
            raise ValueError("paper reading tool cannot generate final conclusions")
        if self.camera_ready_text:
            raise ValueError("paper reading tool cannot generate camera-ready text")
        if not self.requires_human_review:
            raise ValueError("paper reading tool requires human review")
        return self


class PaperReadingToolResult(BaseModel):
    """Result returned by the paper reading tool surface."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = "scholar.paper_reading"
    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    pass_1: list[str] = Field(default_factory=list)
    pass_2: list[str] = Field(default_factory=list)
    pass_3: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    final_conclusion_generated: bool = False
    camera_ready_text_generated: bool = False
    human_verified: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe reading behavior was enabled."""

        return (
            self.final_conclusion_generated
            or self.camera_ready_text_generated
            or self.human_verified
            or not self.requires_human_review
        )


def run_paper_reading_tool(request: PaperReadingToolRequest) -> PaperReadingToolResult:
    """Build a Keshav-style three-pass reading plan."""

    plan: ThreePassReadingPlan = build_three_pass_reading_plan(
        paper_id=request.paper_id,
        title=request.title,
    )
    return PaperReadingToolResult(
        paper_id=plan.paper_id,
        title=plan.title,
        pass_1=plan.pass_1,
        pass_2=plan.pass_2,
        pass_3=plan.pass_3,
        outputs=plan.outputs,
        final_conclusion_generated=False,
        camera_ready_text_generated=False,
        human_verified=plan.human_verified,
        requires_human_review=plan.requires_real_paper_review,
    )
