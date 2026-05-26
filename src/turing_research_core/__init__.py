"""Core public namespace facade for TuringResearch.

This package is a lightweight re-export layer. Implementations still live under
``turing_research_plus`` until a future migration round moves them.
"""

from turing_research_core.public_api import (
    COMPATIBILITY_NAMESPACE,
    NAMESPACE,
    PUBLIC_MODULE_ALIASES,
    STABILITY,
    PrivacyScanReport,
    ProjectIndex,
    QualityReport,
    ResearchProjectTemplate,
    Workspace,
    WorkspaceOverview,
    WorkspaceProject,
    generate_research_project_template,
    load_workspace_registry,
    scan_privacy_paths,
)

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
