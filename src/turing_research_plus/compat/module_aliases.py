"""Namespace compatibility alias registry.

The new namespace packages are facades. This registry documents how they map to
the current ``turing_research_plus`` implementation modules.
"""

from __future__ import annotations

from dataclasses import dataclass

COMPATIBILITY_NAMESPACE = "turing_research_plus"
TARGET_NAMESPACES = (
    "turing_research_core",
    "turing_research_paper",
    "turing_research_artifact",
    "turing_research_experiment",
    "turing_research_dashboard",
    "turing_research_plugins",
    "turing_research_cases",
)


@dataclass(frozen=True)
class ModuleAlias:
    target_namespace: str
    target_module: str
    legacy_module: str
    stability: str


MODULE_ALIASES: tuple[ModuleAlias, ...] = (
    ModuleAlias("turing_research_core", "workspace", "turing_research_plus.workspace", "beta"),
    ModuleAlias("turing_research_core", "privacy", "turing_research_plus.privacy", "beta"),
    ModuleAlias("turing_research_core", "quality", "turing_research_plus.quality", "beta"),
    ModuleAlias(
        "turing_research_core",
        "project_template",
        "turing_research_plus.project_template",
        "beta",
    ),
    ModuleAlias(
        "turing_research_paper",
        "paper_write",
        "turing_research_plus.paper_write",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_paper",
        "paper_review",
        "turing_research_plus.paper_review",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_paper",
        "paper_digest",
        "turing_research_plus.paper_digest",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_artifact",
        "artifact_audit",
        "turing_research_plus.artifact_audit",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_artifact",
        "handoff",
        "turing_research_plus.handoff",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_artifact",
        "run_ingest",
        "turing_research_plus.run_ingest",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_experiment",
        "experiment_route",
        "turing_research_plus.experiment_route",
        "beta",
    ),
    ModuleAlias(
        "turing_research_experiment",
        "hard_gates",
        "turing_research_plus.hard_gates",
        "beta",
    ),
    ModuleAlias("turing_research_experiment", "failure", "turing_research_plus.failure", "beta"),
    ModuleAlias("turing_research_dashboard", "ui", "turing_research_plus.ui", "experimental"),
    ModuleAlias(
        "turing_research_dashboard",
        "advisor_export",
        "turing_research_plus.advisor_export",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_dashboard",
        "case_study",
        "turing_research_plus.case_study",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_plugins",
        "plugins",
        "turing_research_plus.plugins",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_plugins",
        "mcp_plugins",
        "turing_research_plus.mcp_plugins",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_plugins",
        "capabilities",
        "turing_research_plus.capabilities",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_cases",
        "benchmark",
        "turing_research_plus.benchmark",
        "experimental",
    ),
    ModuleAlias(
        "turing_research_cases",
        "case_study",
        "turing_research_plus.case_study",
        "experimental",
    ),
)


def list_module_aliases() -> tuple[ModuleAlias, ...]:
    return MODULE_ALIASES


def aliases_for_namespace(namespace: str) -> tuple[ModuleAlias, ...]:
    return tuple(alias for alias in MODULE_ALIASES if alias.target_namespace == namespace)


def legacy_module_for(target_namespace: str, target_module: str) -> str | None:
    for alias in MODULE_ALIASES:
        if alias.target_namespace == target_namespace and alias.target_module == target_module:
            return alias.legacy_module
    return None


__all__ = [
    "COMPATIBILITY_NAMESPACE",
    "MODULE_ALIASES",
    "TARGET_NAMESPACES",
    "ModuleAlias",
    "aliases_for_namespace",
    "legacy_module_for",
    "list_module_aliases",
]
