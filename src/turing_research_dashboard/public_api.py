"""Public API facade for dashboard and export modules."""

from turing_research_plus.advisor_export import (
    AdvisorMarkdownBundle,
    export_advisor_pdf_optional,
    export_advisor_pptx_optional,
)
from turing_research_plus.advisor_export.quality_gate import ExportQualityReport
from turing_research_plus.case_study.models import CaseStudyDraft as PublicCaseStudyDraft
from turing_research_plus.ui import DashboardCard, build_static_dashboard
from turing_research_plus.vault_ui import ResearchVaultUIBundle

NAMESPACE = "turing_research_dashboard"
COMPATIBILITY_NAMESPACE = "turing_research_plus"
STABILITY = "experimental"
PUBLIC_MODULE_ALIASES = {
    "ui": "turing_research_plus.ui",
    "advisor_export": "turing_research_plus.advisor_export",
    "case_study": "turing_research_plus.case_study",
    "vault_ui": "turing_research_plus.vault_ui",
}

__all__ = [
    "COMPATIBILITY_NAMESPACE",
    "NAMESPACE",
    "PUBLIC_MODULE_ALIASES",
    "STABILITY",
    "AdvisorMarkdownBundle",
    "DashboardCard",
    "ExportQualityReport",
    "PublicCaseStudyDraft",
    "ResearchVaultUIBundle",
    "build_static_dashboard",
    "export_advisor_pdf_optional",
    "export_advisor_pptx_optional",
]
