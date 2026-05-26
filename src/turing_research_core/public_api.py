"""Public API facade for core research OS modules."""

from turing_research_plus.privacy import PrivacyScanReport, scan_privacy_paths
from turing_research_plus.project_template import (
    ResearchProjectTemplate,
    generate_research_project_template,
)
from turing_research_plus.quality import QualityReport
from turing_research_plus.workspace import (
    ProjectIndex,
    Workspace,
    WorkspaceOverview,
    WorkspaceProject,
    load_workspace_registry,
)

NAMESPACE = "turing_research_core"
COMPATIBILITY_NAMESPACE = "turing_research_plus"
STABILITY = "beta"
PUBLIC_MODULE_ALIASES = {
    "workspace": "turing_research_plus.workspace",
    "privacy": "turing_research_plus.privacy",
    "quality": "turing_research_plus.quality",
    "project_template": "turing_research_plus.project_template",
}

__all__ = [
    "COMPATIBILITY_NAMESPACE",
    "NAMESPACE",
    "PUBLIC_MODULE_ALIASES",
    "STABILITY",
    "PrivacyScanReport",
    "ProjectIndex",
    "QualityReport",
    "ResearchProjectTemplate",
    "Workspace",
    "WorkspaceOverview",
    "WorkspaceProject",
    "generate_research_project_template",
    "load_workspace_registry",
    "scan_privacy_paths",
]
