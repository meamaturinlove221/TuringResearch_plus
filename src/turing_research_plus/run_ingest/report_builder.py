"""Build RunIngestReport from parsed bundle metadata."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.run_ingest.models import (
    BackendStatus,
    CandidateResult,
    HardGateResult,
    RunArtifact,
    RunIngestReport,
    RunSourceType,
    RunStatus,
    run_evidence_ref,
)
from turing_research_plus.run_ingest.status_parser import parse_backend_status, parse_run_status

REQUIRED_ARTIFACTS = [
    "final_status.json",
    "ranked_candidates.csv",
    "predictions.npz",
    "board_inventory.md",
    "advisor_summary.md",
    "failure_report.md",
    "sha256_manifest.txt",
    "cleanup_report.md",
]


def build_run_ingest_report(
    *,
    source_type: RunSourceType,
    source_path: Path,
    payload: dict[str, Any],
) -> RunIngestReport:
    """Build a conservative run ingest report from metadata."""

    run_id = str(payload.get("run_id") or source_path.name or "unknown-run")
    route_id = str(payload.get("route_id") or "modal_sparseconv_v0")
    status = parse_run_status(_string(payload.get("status")))
    backend_status = parse_backend_status(_string(payload.get("backend_status")))
    present_files = _present_files(payload, source_path)
    artifacts = _artifacts(present_files)
    missing_artifacts = [
        artifact.path for artifact in artifacts if artifact.required and not artifact.present
    ]
    candidates = _candidates(payload)
    hard_gates = _hard_gates(payload, artifacts, backend_status)
    failures = _failure_categories(payload, artifacts, backend_status, status)
    evidence_updates = _evidence_updates(
        run_id,
        route_id,
        status,
        backend_status,
        missing_artifacts,
    )
    return RunIngestReport(
        run_id=run_id,
        route_id=route_id,
        source_type=source_type,
        source_path=str(source_path),
        status=status,
        duration=_string(payload.get("duration")),
        backend_status=backend_status,
        candidates=candidates,
        best_candidate=_best_candidate(candidates),
        artifacts=artifacts,
        missing_artifacts=missing_artifacts,
        hard_gate_results=hard_gates,
        failure_categories=list(dict.fromkeys(failures)),
        evidence_updates=evidence_updates,
        advisor_pack_inputs={
            "run_id": run_id,
            "route_id": route_id,
            "status": status.value,
            "missing_artifacts": missing_artifacts,
            "failure_categories": [item.value for item in failures],
        },
        requires_human_review=True,
    )


def _present_files(payload: dict[str, Any], source_path: Path) -> set[str]:
    files = payload.get("artifacts")
    if isinstance(files, list):
        return {str(item) for item in files}
    if source_path.is_dir():
        return {path.name for path in source_path.iterdir() if path.is_file()}
    return set()


def _artifacts(present_files: set[str]) -> list[RunArtifact]:
    return [
        RunArtifact(
            path=name,
            artifact_type=_artifact_type(name),
            present=name in present_files,
            required=True,
            notes=[] if name in present_files else ["required artifact missing"],
        )
        for name in REQUIRED_ARTIFACTS
    ]


def _candidates(payload: dict[str, Any]) -> list[CandidateResult]:
    raw = payload.get("candidates")
    if not isinstance(raw, list):
        return []
    candidates: list[CandidateResult] = []
    for item in raw:
        if isinstance(item, dict):
            candidates.append(
                CandidateResult(
                    candidate_id=str(item.get("candidate_id") or item.get("id") or "candidate"),
                    score=_float_or_none(item.get("score")),
                    status=str(item.get("status") or "unknown"),
                    notes=[str(note) for note in item.get("notes", [])]
                    if isinstance(item.get("notes"), list)
                    else [],
                )
            )
    return candidates


def _best_candidate(candidates: list[CandidateResult]) -> CandidateResult | None:
    scored = [candidate for candidate in candidates if candidate.score is not None]
    if not scored:
        return None
    return sorted(scored, key=lambda item: item.score or 0, reverse=True)[0]


def _hard_gates(
    payload: dict[str, Any],
    artifacts: list[RunArtifact],
    backend_status: BackendStatus,
) -> list[HardGateResult]:
    raw = payload.get("hard_gates")
    gates: list[HardGateResult] = []
    if isinstance(raw, dict):
        for gate_id, value in raw.items():
            passed = bool(value)
            gates.append(
                HardGateResult(
                    gate_id=str(gate_id),
                    passed=passed,
                    reason="passed in fixture metadata" if passed else "failed in fixture metadata",
                )
            )
    gates.append(
        HardGateResult(
            gate_id="real_sparse_backend_required",
            passed=backend_status == BackendStatus.REAL_BACKEND_CONFIRMED,
            reason="real sparse backend log is required",
        )
    )
    for artifact in artifacts:
        gates.append(
            HardGateResult(
                gate_id=f"{artifact.path}_required",
                passed=artifact.present,
                reason=(
                    "required artifact present"
                    if artifact.present
                    else "required artifact missing"
                ),
            )
        )
    return gates


def _failure_categories(
    payload: dict[str, Any],
    artifacts: list[RunArtifact],
    backend_status: BackendStatus,
    status: RunStatus,
) -> list[FailureCategory]:
    failures: list[FailureCategory] = []
    if status in {RunStatus.HARD_BLOCKED, RunStatus.RUN_FAILED, RunStatus.UNKNOWN}:
        failures.append(FailureCategory.NOT_ENOUGH_EVIDENCE)
    if backend_status == BackendStatus.REAL_BACKEND_MISSING:
        failures.extend(
            [FailureCategory.REAL_BACKEND_UNAVAILABLE, FailureCategory.SPARSE_BACKEND_UNAVAILABLE]
        )
    if backend_status == BackendStatus.FALLBACK_USED:
        failures.append(FailureCategory.FALLBACK_ONLY)
    missing = {artifact.path for artifact in artifacts if not artifact.present}
    if "predictions.npz" in missing:
        failures.append(FailureCategory.MISSING_ASSETS)
    if "board_inventory.md" in missing:
        failures.append(FailureCategory.VISUAL_PROOF_INSUFFICIENT)
    if "cleanup_report.md" in missing:
        failures.append(FailureCategory.PACKAGE_INCOMPLETE)
    if _report_only(payload, missing):
        failures.append(FailureCategory.REPORT_ONLY)
    return failures


def _evidence_updates(
    run_id: str,
    route_id: str,
    status: RunStatus,
    backend_status: BackendStatus,
    missing_artifacts: list[str],
) -> list[dict[str, Any]]:
    if backend_status == BackendStatus.REAL_BACKEND_CONFIRMED and not missing_artifacts:
        evidence_status = "requires-human-review"
        claim = "Run bundle is review-ready but not promoted."
    else:
        evidence_status = "not-enough-evidence"
        claim = "Run bundle is insufficient to claim SparseConv3D success."
    return [
        {
            "run_id": run_id,
            "version_label": route_id,
            "claim": claim,
            "status": evidence_status,
            "evidence_refs": [
                run_evidence_ref(run_id, "final_status", status.value).model_dump(mode="json")
            ],
            "blockers": missing_artifacts,
            "next_actions": ["Review missing artifacts and hard gate failures."],
        }
    ]


def _artifact_type(name: str) -> str:
    suffix = Path(name).suffix.lower().lstrip(".")
    return suffix or "unknown"


def _report_only(payload: dict[str, Any], missing: set[str]) -> bool:
    artifacts = payload.get("artifacts")
    if artifacts == ["report.md"] or artifacts == ["failure_report.md"]:
        return True
    return "final_status.json" not in missing and len(missing) >= len(REQUIRED_ARTIFACTS) - 2


def _string(value: object) -> str | None:
    return None if value is None else str(value)


def _float_or_none(value: object) -> float | None:
    if value is None:
        return None
    if not isinstance(value, str | bytes | bytearray | int | float):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
