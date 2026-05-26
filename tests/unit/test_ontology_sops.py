from __future__ import annotations

import pytest

from turing_research_plus.vault_graph.ontology import list_ontology_sops, run_ontology_sop


def test_ontology_sop_list_contains_required_steps() -> None:
    sops = list_ontology_sops()

    assert "seed-concept-search" in sops
    assert "ontology-export" in sops
    assert len(sops) == 10


def test_run_ontology_sop_returns_review_result() -> None:
    result = run_ontology_sop("alias-resolution", inputs=["SMPL-X", "SMPLX"])

    assert result.sop_name == "alias-resolution"
    assert result.required_human_review is True
    assert result.outputs


def test_run_ontology_sop_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="unsupported ontology SOP"):
        run_ontology_sop("unknown")
