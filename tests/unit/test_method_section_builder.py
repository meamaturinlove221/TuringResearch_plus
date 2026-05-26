from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.paper_write.method_builder import (
    MethodSectionSkeleton,
    build_vggt_method_section_skeleton,
)

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"


def _skeleton() -> MethodSectionSkeleton:
    return build_vggt_method_section_skeleton(
        VGGT / "paper_method_cards",
        VGGT / "architecture_diagrams",
        VGGT / "route_specs",
    )


def test_build_vggt_method_section_skeleton_contains_required_sections() -> None:
    skeleton = _skeleton()

    assert skeleton.project_topic == "VGGT / SMPL-X Human Prior"
    assert skeleton.problem_setting
    assert skeleton.overview
    assert skeleton.smplx_feature_encoding
    assert skeleton.vggt_integration
    assert skeleton.route_variants
    assert skeleton.hard_gates
    assert skeleton.implementation_notes
    assert skeleton.limitations
    assert skeleton.figure_placeholders
    assert skeleton.evidence_refs
    assert skeleton.requires_human_review is True


def test_build_vggt_method_section_skeleton_keeps_route_planned() -> None:
    skeleton = _skeleton()
    route_text = "\n".join(skeleton.route_variants)
    limitation_text = "\n".join(skeleton.limitations)

    assert "requires-real-experiment" in route_text
    assert "not executed" in route_text
    assert "SparseConv3D backend success is not established" in limitation_text
    assert "Do not claim SparseConv3D success." in skeleton.unsafe_claims
    assert skeleton.claims_experiment_verified is False
    assert skeleton.generated_final_contribution_claims is False


def test_method_section_skeleton_rejects_experiment_verification_claim() -> None:
    payload = _skeleton().model_dump(mode="python")
    payload["claims_experiment_verified"] = True

    with pytest.raises(ValueError, match="must not claim verification"):
        MethodSectionSkeleton(**payload)


def test_method_section_skeleton_rejects_final_contribution_claims() -> None:
    payload = _skeleton().model_dump(mode="python")
    payload["generated_final_contribution_claims"] = True

    with pytest.raises(ValueError, match="must not generate final claims"):
        MethodSectionSkeleton(**payload)
