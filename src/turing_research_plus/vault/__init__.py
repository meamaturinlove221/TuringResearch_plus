"""Wiki Vault for TulingResearch Plus."""

from tuling_research_plus.vault.graph import DuplicateEdgeError, VaultGraph
from tuling_research_plus.vault.index import VaultIndex
from tuling_research_plus.vault.lint import lint_vault
from tuling_research_plus.vault.markdown_io import read_page, write_page
from tuling_research_plus.vault.models import (
    VaultEdge,
    VaultEdgeType,
    VaultEntityType,
    VaultGraphStats,
    VaultIngestResult,
    VaultLintIssue,
    VaultPage,
    VaultSearchResult,
)
from tuling_research_plus.vault.service import VaultService

__all__ = [
    "DuplicateEdgeError",
    "VaultEdge",
    "VaultEdgeType",
    "VaultEntityType",
    "VaultGraph",
    "VaultGraphStats",
    "VaultIndex",
    "VaultIngestResult",
    "VaultLintIssue",
    "VaultPage",
    "VaultSearchResult",
    "VaultService",
    "lint_vault",
    "read_page",
    "write_page",
]
