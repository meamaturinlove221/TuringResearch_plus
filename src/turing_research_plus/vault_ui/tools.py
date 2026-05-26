"""Local tool wrappers for static vault UI generation."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.vault_graph.models import VaultGraph
from turing_research_plus.vault_ui.models import ResearchVaultUIBundle
from turing_research_plus.vault_ui.static_vault import (
    build_vault_ui_bundle,
    build_vggt_vault_ui_bundle,
)


def vault_ui_build_local(
    graph: VaultGraph,
    *,
    project_name: str,
    output_path: Path,
) -> ResearchVaultUIBundle:
    """Build a static local vault UI."""

    return build_vault_ui_bundle(graph, project_name=project_name, output_path=output_path)


def vault_ui_build_vggt(root: Path, *, write_files: bool = True) -> ResearchVaultUIBundle:
    """Build the VGGT fake/static vault UI fixture."""

    return build_vggt_vault_ui_bundle(root, write_files=write_files)
