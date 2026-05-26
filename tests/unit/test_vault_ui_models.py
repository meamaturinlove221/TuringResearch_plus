from __future__ import annotations

import pytest

from turing_research_plus.vault_graph.models import VaultGraphNodeType
from turing_research_plus.vault_ui.models import (
    ResearchVaultUIBundle,
    VaultSearchEntry,
    VaultUISafetyReport,
    VaultUISection,
)


def test_vault_ui_bundle_requires_review_and_sections() -> None:
    bundle = ResearchVaultUIBundle(
        bundle_id="demo",
        project_name="Demo Project",
        graph_id="graph",
        sections=[
            VaultUISection(
                section_id="concepts",
                title="Concepts",
                markdown="- [[VGGT]]",
            )
        ],
        search_index=[
            VaultSearchEntry(
                entry_id="vggt",
                title="VGGT",
                node_type=VaultGraphNodeType.CONCEPT,
                text="VGGT concept",
                href="#node-vggt",
            )
        ],
    )

    payload = bundle.model_dump(mode="json")

    assert payload["requires_human_review"] is True
    assert payload["safety_report"]["no_server"] is True
    assert payload["wikilinks_optional"] is True


def test_vault_ui_rejects_server_boundary_break() -> None:
    with pytest.raises(ValueError, match="local/static/review-only"):
        VaultUISafetyReport(no_server=False)


def test_vault_ui_bundle_requires_section() -> None:
    with pytest.raises(ValueError, match="at least one section"):
        ResearchVaultUIBundle(
            bundle_id="bad",
            project_name="Demo",
            graph_id="graph",
            sections=[],
        )
