"""Paper writing scaffold helpers."""

from turing_research_plus.paper_write.citation_safety import (
    CitationSafetyReport,
    RelatedWorkCitation,
    citation_from_digest_fixture,
    evaluate_citation_safety,
    render_citation_safety_report,
)
from turing_research_plus.paper_write.citation_status_guard import (
    PaperCitationStatus,
    PaperCitationStatusReport,
    parse_citation_status_report,
    render_paper_citation_status_report,
)
from turing_research_plus.paper_write.claim_guard import (
    PaperClaimGuardReport,
    evaluate_paper_claims,
    render_paper_claim_guard_report,
)
from turing_research_plus.paper_write.draft_assembly import assemble_paper_draft_beta
from turing_research_plus.paper_write.draft_package import (
    PaperDraftPackage,
    export_paper_draft_package,
    render_paper_draft_package,
)
from turing_research_plus.paper_write.evidence_linker import (
    build_vggt_evidence_requirements,
    missing_evidence_report,
)
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
from turing_research_plus.paper_write.models import (
    EvidenceRequirement,
    PaperScaffold,
    PaperSectionPlan,
    PaperSectionStatus,
)
from turing_research_plus.paper_write.related_work_builder import (
    RelatedWorkDraftSkeleton,
    build_vggt_related_work_draft_skeleton,
    render_related_work_citation_safety,
    render_related_work_skeleton,
)
from turing_research_plus.paper_write.result_table_guard import (
    ResultTableGuardReport,
    build_missing_result_table_guard,
    render_result_table_guard,
)
from turing_research_plus.paper_write.scaffold import build_vggt_paper_scaffold
from turing_research_plus.paper_write.section_status import (
    infer_section_status,
    summarize_section_status,
)

__all__ = [
    "CitationSafetyReport",
    "EvidenceRequirement",
    "ExperimentSectionSkeleton",
    "MethodSectionSkeleton",
    "PaperScaffold",
    "PaperCitationStatus",
    "PaperCitationStatusReport",
    "PaperClaimGuardReport",
    "PaperDraftPackage",
    "PaperSectionPlan",
    "PaperSectionStatus",
    "RelatedWorkCitation",
    "RelatedWorkDraftSkeleton",
    "ResultTableGuardReport",
    "assemble_paper_draft_beta",
    "build_missing_result_table_guard",
    "build_vggt_evidence_requirements",
    "build_vggt_experiment_section_skeleton",
    "build_vggt_method_section_skeleton",
    "build_vggt_paper_scaffold",
    "build_vggt_related_work_draft_skeleton",
    "citation_from_digest_fixture",
    "evaluate_citation_safety",
    "evaluate_paper_claims",
    "export_paper_draft_package",
    "infer_section_status",
    "missing_evidence_report",
    "parse_citation_status_report",
    "render_citation_safety_report",
    "render_evidence_gap_report",
    "render_experiment_result_table_missing_items",
    "render_experiment_section_skeleton",
    "render_method_figure_links",
    "render_method_section_skeleton",
    "render_paper_outline",
    "render_paper_citation_status_report",
    "render_paper_claim_guard_report",
    "render_paper_draft_package",
    "render_related_work_citation_safety",
    "render_related_work_skeleton",
    "render_result_table_guard",
    "render_section_status",
    "summarize_section_status",
]
