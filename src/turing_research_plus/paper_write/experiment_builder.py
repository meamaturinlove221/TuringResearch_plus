"""Build experiment section skeletons from local run review artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.paper_write.result_table_guard import (
    ResultTableGuardReport,
    build_missing_result_table_guard,
    render_result_table_guard,
)


class ExperimentSectionSkeleton(BaseModel):
    """Review-only experiment section skeleton."""

    model_config = ConfigDict(extra="forbid")

    skeleton_id: str = Field(min_length=1)
    project_topic: str = Field(min_length=1)
    dataset_setup_placeholder: list[str] = Field(default_factory=list)
    baselines: list[str] = Field(default_factory=list)
    ablations: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    route_status: str = Field(min_length=1)
    run_status: str = Field(min_length=1)
    backend_status: str = Field(min_length=1)
    missing_result_tables: list[str] = Field(default_factory=list)
    failure_cases: list[str] = Field(default_factory=list)
    planned_experiments: list[str] = Field(default_factory=list)
    not_ready_claims: list[str] = Field(default_factory=list)
    result_table_guard: ResultTableGuardReport
    evidence_refs: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    generated_result_values: bool = False
    fabricated_tables: bool = False
    dashboard_treated_as_result: bool = False

    @model_validator(mode="after")
    def experiment_skeleton_stays_review_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("experiment section skeleton requires human review")
        if self.generated_result_values:
            raise ValueError("experiment section skeleton must not generate result values")
        if self.fabricated_tables:
            raise ValueError("experiment section skeleton must not fabricate tables")
        if self.dashboard_treated_as_result:
            raise ValueError("dashboard must not be treated as paper result")
        if not self.missing_result_tables:
            raise ValueError("experiment section skeleton must list missing result tables")
        if not self.not_ready_claims:
            raise ValueError("experiment section skeleton must list not-ready claims")
        if not self.evidence_refs:
            raise ValueError("experiment section skeleton must link evidence refs")
        return self


def build_vggt_experiment_section_skeleton(
    run_ingest_report_path: Path,
    dashboard_dir: Path,
    route_spec_path: Path,
    *,
    skeleton_id: str = "vggt_experiment_section_skeleton",
) -> ExperimentSectionSkeleton:
    """Build a conservative VGGT experiment section skeleton."""

    route_payload = _read_json_like(route_spec_path)
    run_text = run_ingest_report_path.read_text(encoding="utf-8")
    route_status = str(route_payload.get("status", "requires-human-review"))
    run_status = _extract_backtick_value(run_text, "Status") or "unknown"
    backend_status = _extract_backtick_value(run_text, "Backend status") or "unknown"
    missing_artifacts = _extract_bullets_under(run_text, "Missing Artifacts")
    failure_cases = _extract_bullets_under(run_text, "Failure Categories")
    hard_gates = [f"`{gate}`" for gate in route_payload.get("hard_gates", [])]
    planned = [
        "Run real SparseConv3D backend probe before result writing.",
        "Collect predictions, visual board, sha256 manifest, and cleanup report.",
        "Re-run visual readiness checks before advisor or paper promotion.",
    ]
    guard = build_missing_result_table_guard(
        missing_artifacts=missing_artifacts,
        run_status=run_status,
        route_status=route_status,
    )

    return ExperimentSectionSkeleton(
        skeleton_id=skeleton_id,
        project_topic="VGGT / SMPL-X Human Prior",
        dataset_setup_placeholder=[
            "Dataset/setup details remain placeholders until real experiment logs exist.",
            "Do not infer dataset results from route or dashboard fixtures.",
        ],
        baselines=[
            "VGGT baseline placeholder requires real run evidence.",
            "Human-prior route comparison requires real run evidence.",
        ],
        ablations=[
            "SMPL-X feature encoding ablation placeholder.",
            "SparseConv3D backend ablation placeholder.",
            "Visual proof ablation placeholder.",
        ],
        metrics=[
            "Metric names may be planned, but result values are blocked.",
            "Quantitative tables require real predictions and manifest evidence.",
        ],
        route_status=route_status,
        run_status=run_status,
        backend_status=backend_status,
        missing_result_tables=guard.missing_result_tables,
        failure_cases=failure_cases,
        planned_experiments=planned,
        not_ready_claims=[
            "Planned route is not an executed experiment.",
            "Dashboard is not a paper result.",
            "SparseConv3D success is not established.",
            "Quantitative result tables are missing.",
            *[f"Hard gate pending: {gate}" for gate in hard_gates],
        ],
        result_table_guard=guard,
        evidence_refs=[
            run_ingest_report_path.as_posix(),
            (dashboard_dir / "run_dashboard.md").as_posix(),
            (dashboard_dir / "status_board.md").as_posix(),
            (dashboard_dir / "failure_board.md").as_posix(),
            route_spec_path.as_posix(),
        ],
        requires_human_review=True,
    )


def render_experiment_section_skeleton(skeleton: ExperimentSectionSkeleton) -> str:
    """Render an experiment skeleton without result values."""

    lines = [
        f"# Experiment Section Skeleton: {skeleton.project_topic}",
        "",
        "This is an evidence-linked skeleton, not a paper results section.",
        "",
        "## Dataset / Setup Placeholder",
        "",
        *_bullets(skeleton.dataset_setup_placeholder),
        "",
        "## Baselines",
        "",
        *_bullets(skeleton.baselines),
        "",
        "## Ablations",
        "",
        *_bullets(skeleton.ablations),
        "",
        "## Metrics",
        "",
        *_bullets(skeleton.metrics),
        "",
        "## Route Status",
        "",
        f"- Route status: `{skeleton.route_status}`",
        f"- Run status: `{skeleton.run_status}`",
        f"- Backend status: `{skeleton.backend_status}`",
        "",
        "## Missing Result Tables",
        "",
        *_bullets(skeleton.missing_result_tables),
        "",
        "## Failure Cases",
        "",
        *_bullets(skeleton.failure_cases),
        "",
        "## Planned Experiments",
        "",
        *_bullets(skeleton.planned_experiments),
        "",
        "## Not-ready Claims",
        "",
        *_bullets(skeleton.not_ready_claims),
        "",
        "## Evidence Refs",
        "",
        *_bullets([f"`{ref}`" for ref in skeleton.evidence_refs]),
        "",
        "## Boundary",
        "",
        "- No result value is generated.",
        "- Planned is not executed.",
        "- Dashboard is not a paper result.",
        "- Failure analysis is internal analysis until paper evidence exists.",
        "- No figure or table is fabricated.",
        "",
    ]
    return "\n".join(lines)


def render_experiment_result_table_missing_items(
    skeleton: ExperimentSectionSkeleton,
) -> str:
    """Render missing result table guard report."""

    return render_result_table_guard(skeleton.result_table_guard)


def _read_json_like(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {"status": "requires-human-review"}
    return payload if isinstance(payload, dict) else {}


def _extract_backtick_value(text: str, label: str) -> str | None:
    prefix = f"- {label}: `"
    for line in text.splitlines():
        if line.startswith(prefix) and line.endswith("`"):
            return line.removeprefix(prefix).removesuffix("`")
    return None


def _extract_bullets_under(text: str, heading: str) -> list[str]:
    bullets: list[str] = []
    in_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == f"## {heading}":
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if in_section and stripped.startswith("- "):
            bullets.append(stripped[2:].strip("`"))
    return bullets


def _bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] or ["- Not specified."]
