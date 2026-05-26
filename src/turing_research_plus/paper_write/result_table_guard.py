"""Guards that prevent fabricated result tables."""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ResultTableGuardReport(BaseModel):
    """Report explaining why result tables are blocked or allowed."""

    model_config = ConfigDict(extra="forbid")

    result_tables_allowed: bool = False
    missing_result_tables: list[str] = Field(default_factory=list)
    missing_artifacts: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    planned_not_executed: bool = True
    dashboard_is_not_result: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def no_result_table_without_evidence(self) -> Self:
        if self.result_tables_allowed and (
            self.missing_result_tables or self.missing_artifacts
        ):
            raise ValueError("result tables cannot be allowed with missing evidence")
        if not self.dashboard_is_not_result:
            raise ValueError("dashboard must not be treated as paper result")
        if not self.requires_human_review:
            raise ValueError("result table guard requires human review")
        return self


def build_missing_result_table_guard(
    *,
    missing_artifacts: list[str],
    run_status: str,
    route_status: str,
) -> ResultTableGuardReport:
    """Build a conservative guard when real result evidence is missing."""

    missing_tables = [
        "main_quantitative_results",
        "ablation_results",
        "failure_case_visual_table",
    ]
    blocked = [
        "Do not report quantitative result values without real run evidence.",
        "Do not claim planned route execution as completed.",
        "Do not treat dashboard status as a paper result.",
        "Do not claim SparseConv3D success without backend evidence.",
    ]
    if run_status and run_status not in {"REVIEW_READY_NOT_PROMOTED", "PARTIAL"}:
        blocked.append(f"Run status `{run_status}` is not ready for result tables.")
    if route_status and route_status != "executed":
        blocked.append(f"Route status `{route_status}` is not executed.")
    return ResultTableGuardReport(
        result_tables_allowed=False,
        missing_result_tables=missing_tables,
        missing_artifacts=missing_artifacts,
        blocked_claims=blocked,
        planned_not_executed=True,
        dashboard_is_not_result=True,
        requires_human_review=True,
    )


def render_result_table_guard(report: ResultTableGuardReport) -> str:
    """Render missing result table items as Markdown."""

    lines = [
        "# Result Table Missing Items",
        "",
        f"- Result tables allowed: `{str(report.result_tables_allowed).lower()}`",
        f"- Planned is not executed: `{str(report.planned_not_executed).lower()}`",
        f"- Dashboard is not result: `{str(report.dashboard_is_not_result).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Missing Result Tables",
        "",
        *[f"- {item}" for item in report.missing_result_tables],
        "",
        "## Missing Artifacts",
        "",
        *[f"- `{item}`" for item in report.missing_artifacts],
        "",
        "## Blocked Claims",
        "",
        *[f"- {item}" for item in report.blocked_claims],
        "",
        "## Boundary",
        "",
        "- No result value is generated.",
        "- No figure or table is fabricated.",
        "- Missing tables stay missing until real evidence exists.",
        "",
    ]
    return "\n".join(lines)
