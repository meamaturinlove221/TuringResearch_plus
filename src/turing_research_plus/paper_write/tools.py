"""Local helper wrappers for paper writing scaffolds."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.experiment_builder import (
    ExperimentSectionSkeleton,
    build_vggt_experiment_section_skeleton,
    render_experiment_result_table_missing_items,
    render_experiment_section_skeleton,
)
from turing_research_plus.paper_write.markdown_export import (
    render_evidence_gap_report,
    render_paper_outline,
    render_section_status,
)
from turing_research_plus.paper_write.method_builder import (
    MethodSectionSkeleton,
    build_vggt_method_section_skeleton,
)
from turing_research_plus.paper_write.method_templates import (
    render_method_figure_links,
    render_method_section_skeleton,
)
from turing_research_plus.paper_write.models import PaperScaffold
from turing_research_plus.paper_write.related_work_builder import (
    RelatedWorkDraftSkeleton,
    build_vggt_related_work_draft_skeleton,
    render_related_work_citation_safety,
    render_related_work_skeleton,
)
from turing_research_plus.paper_write.scaffold import build_vggt_paper_scaffold


def paper_scaffold_build_vggt(knowledge_pack_dir: Path) -> PaperScaffold:
    """Build the VGGT paper scaffold."""

    return build_vggt_paper_scaffold(knowledge_pack_dir)


def paper_scaffold_export_markdown(scaffold: PaperScaffold, output_dir: Path) -> list[Path]:
    """Write scaffold Markdown files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        (output_dir / "paper_outline.md", render_paper_outline(scaffold)),
        (output_dir / "section_status.md", render_section_status(scaffold)),
        (output_dir / "evidence_gap_report.md", render_evidence_gap_report(scaffold)),
    ]
    for path, text in outputs:
        path.write_text(text, encoding="utf-8")
    return [path for path, _ in outputs]


def method_section_build_vggt(
    method_cards_dir: Path,
    architecture_diagrams_dir: Path,
    route_specs_dir: Path,
) -> MethodSectionSkeleton:
    """Build the VGGT method section skeleton."""

    return build_vggt_method_section_skeleton(
        method_cards_dir=method_cards_dir,
        architecture_diagrams_dir=architecture_diagrams_dir,
        route_specs_dir=route_specs_dir,
    )


def method_section_export_markdown(
    skeleton: MethodSectionSkeleton, output_dir: Path
) -> list[Path]:
    """Write method section skeleton Markdown files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        (
            output_dir / "method_section_skeleton.md",
            render_method_section_skeleton(skeleton),
        ),
        (output_dir / "method_figure_links.md", render_method_figure_links(skeleton)),
    ]
    for path, text in outputs:
        path.write_text(text, encoding="utf-8")
    return [path for path, _ in outputs]


def related_work_draft_build_vggt(
    related_work_dir: Path,
    collision_risk_dir: Path,
    paper_digest_dir: Path,
) -> RelatedWorkDraftSkeleton:
    """Build the VGGT related-work draft skeleton."""

    return build_vggt_related_work_draft_skeleton(
        related_work_dir=related_work_dir,
        collision_risk_dir=collision_risk_dir,
        paper_digest_dir=paper_digest_dir,
    )


def related_work_draft_export_markdown(
    skeleton: RelatedWorkDraftSkeleton, output_dir: Path
) -> list[Path]:
    """Write related-work draft skeleton Markdown files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        (
            output_dir / "related_work_skeleton.md",
            render_related_work_skeleton(skeleton),
        ),
        (
            output_dir / "citation_safety_report.md",
            render_related_work_citation_safety(skeleton),
        ),
    ]
    for path, text in outputs:
        path.write_text(text, encoding="utf-8")
    return [path for path, _ in outputs]


def experiment_section_build_vggt(
    run_ingest_report_path: Path,
    dashboard_dir: Path,
    route_spec_path: Path,
) -> ExperimentSectionSkeleton:
    """Build the VGGT experiment section skeleton."""

    return build_vggt_experiment_section_skeleton(
        run_ingest_report_path=run_ingest_report_path,
        dashboard_dir=dashboard_dir,
        route_spec_path=route_spec_path,
    )


def experiment_section_export_markdown(
    skeleton: ExperimentSectionSkeleton, output_dir: Path
) -> list[Path]:
    """Write experiment section skeleton Markdown files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        (
            output_dir / "experiment_section_skeleton.md",
            render_experiment_section_skeleton(skeleton),
        ),
        (
            output_dir / "result_table_missing_items.md",
            render_experiment_result_table_missing_items(skeleton),
        ),
    ]
    for path, text in outputs:
        path.write_text(text, encoding="utf-8")
    return [path for path, _ in outputs]
