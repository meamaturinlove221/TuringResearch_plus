"""Default hard gate definitions."""

from __future__ import annotations

from turing_research_plus.hard_gates.models import GateCondition, GateSpec

VGGT_GATE_IDS = [
    "not_report_only",
    "not_fast_return",
    "not_identity_copy",
    "not_fallback_only",
    "no_promotion",
    "no_strict_registry",
    "no_v50_modification",
    "real_backend_required",
    "candidate_predictions_required",
    "visual_board_required",
    "npz_diff_required",
    "sha256_required",
    "zip_test_clean",
    "cleanup_required",
    "sparse_backend_probe_required",
    "smplx_alignment_risk_logged",
    "hairline_regression_checked",
    "hand_object_confusion_checked",
]


def default_vggt_gate_library() -> dict[str, GateSpec]:
    """Return deterministic VGGT hard gate definitions."""

    return {gate_id: _gate(gate_id) for gate_id in VGGT_GATE_IDS}


def _gate(gate_id: str) -> GateSpec:
    return GateSpec(
        gate_id=gate_id,
        name=gate_id.replace("_", " ").title(),
        description=_description(gate_id),
        severity="critical" if gate_id in {"no_promotion", "real_backend_required"} else "high",
        conditions=[
            GateCondition(
                condition_id=f"{gate_id}_evidence",
                description=f"{gate_id} must have supporting evidence or an explicit blocker.",
                forbidden_statuses=["failed", "hard-blocked", "not-enough-evidence"],
                required_evidence=gate_id
                in {
                    "real_backend_required",
                    "candidate_predictions_required",
                    "visual_board_required",
                    "npz_diff_required",
                    "sha256_required",
                    "zip_test_clean",
                    "sparse_backend_probe_required",
                },
            )
        ],
        default_block_reason=_description(gate_id),
    )


def _description(gate_id: str) -> str:
    descriptions = {
        "not_report_only": "Output must include evidence artifacts, not only a report.",
        "not_fast_return": "Route must not pass through a fast-return shortcut.",
        "not_identity_copy": "Route must not be identity-copy behavior.",
        "not_fallback_only": "Fallback-only output cannot be promoted.",
        "no_promotion": "Planned or insufficient evidence cannot be promoted to observed.",
        "no_strict_registry": "Strict registry failures cannot be ignored.",
        "no_v50_modification": "V50 baseline modification is forbidden without explicit approval.",
        "real_backend_required": "A real backend is required for execution claims.",
        "candidate_predictions_required": "Candidate predictions must be present for route proof.",
        "visual_board_required": "Visual board proof is required for visual readiness.",
        "npz_diff_required": "NPZ diff evidence is required for numeric artifact changes.",
        "sha256_required": "Checksums are required for promoted artifact bundles.",
        "zip_test_clean": "Zip/package test must be clean before promotion.",
        "cleanup_required": "Temporary artifacts must have cleanup requirements.",
        "sparse_backend_probe_required": "Sparse backend probe evidence is required.",
        "smplx_alignment_risk_logged": "SMPL-X alignment risk must be logged.",
        "hairline_regression_checked": "Hairline regression must be checked.",
        "hand_object_confusion_checked": "Hand/object confusion must be checked.",
    }
    return descriptions[gate_id]
