"""Build a minimal VGGT / SMPL-X evidence ledger from safe local scan summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.vggt.evidence_models import (
    VGGTEvidenceLedger,
    VGGTEvidenceLedgerBuildInput,
    VGGTEvidenceRow,
    VGGTEvidenceStatus,
)


def build_vggt_evidence_ledger(
    request: VGGTEvidenceLedgerBuildInput,
) -> VGGTEvidenceLedger:
    """Build a conservative VGGT evidence ledger without touching VGGT project paths."""

    generated_from: list[str] = []
    missing_inputs: list[str] = []
    warnings: list[str] = []

    summary_text = _read_committed_text(
        request.local_scan_summary_path,
        generated_from,
        missing_inputs,
    )
    index_text = _read_committed_text(
        request.local_scan_artifact_index_path,
        generated_from,
        missing_inputs,
    )
    local_rows = _read_optional_json_rows(
        request.local_scan_evidence_ledger_path,
        generated_from,
        missing_inputs,
        warnings,
    )

    rows = _default_rows(
        request.run_id,
        request.local_scan_summary_path,
        request.local_scan_artifact_index_path,
        summary_text,
        index_text,
    )
    rows.extend(local_rows)

    if request.local_scan_evidence_ledger_path is None:
        missing_inputs.append("examples/vggt-human-prior-survey/local_scan_evidence_ledger.json")
    elif not request.local_scan_evidence_ledger_path.exists():
        missing_inputs.append(str(request.local_scan_evidence_ledger_path))

    if missing_inputs:
        warnings.append("Missing local evidence inputs prevent V120/V121 promotion.")

    return VGGTEvidenceLedger(
        ledger_id=f"{request.run_id}-evidence-ledger",
        run_id=request.run_id,
        rows=rows,
        generated_from=generated_from,
        missing_inputs=_dedupe(missing_inputs),
        warnings=_dedupe(warnings),
    )


def vggt_evidence_ledger_build(request: VGGTEvidenceLedgerBuildInput) -> dict[str, Any]:
    """Capsule-local thin wrapper for the proposed vggt.evidence_ledger_build tool."""

    return build_vggt_evidence_ledger(request).model_dump(mode="json")


def _read_committed_text(path: Path, generated_from: list[str], missing_inputs: list[str]) -> str:
    if not path.exists():
        missing_inputs.append(str(path))
        return ""
    generated_from.append(str(path))
    return path.read_text(encoding="utf-8")


def _read_optional_json_rows(
    path: Path | None,
    generated_from: list[str],
    missing_inputs: list[str],
    warnings: list[str],
) -> list[VGGTEvidenceRow]:
    if path is None:
        return []
    if not path.exists():
        missing_inputs.append(str(path))
        return []
    generated_from.append(str(path))
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        warnings.append(f"Could not parse local evidence ledger JSON: {exc}")
        return []

    raw_rows = payload.get("rows", payload if isinstance(payload, list) else [])
    rows: list[VGGTEvidenceRow] = []
    for raw in raw_rows:
        if not isinstance(raw, dict):
            warnings.append("Skipped non-object evidence row from local evidence ledger JSON.")
            continue
        rows.append(VGGTEvidenceRow.model_validate(raw))
    return rows


def _default_rows(
    run_id: str,
    summary_path: Path,
    artifact_index_path: Path,
    summary_text: str,
    index_text: str,
) -> list[VGGTEvidenceRow]:
    summary_ref = _evidence_ref(
        summary_path,
        "local scan summary",
        _quote_or_default(summary_text, "Safety boundary"),
        confidence=0.7,
    )
    artifact_ref = _evidence_ref(
        artifact_index_path,
        "local artifact index",
        _quote_or_default(index_text, "No artifacts were scanned"),
        confidence=0.7,
    )
    engineering_ref = EvidenceRef(
        source_id="round-36-dogfooding-context",
        locator="docs/dogfooding-vggt-smplx.md",
        quote="Milestone labels are engineering context unless backed by local scan evidence.",
        confidence=0.5,
    )

    return [
        VGGTEvidenceRow(
            run_id=run_id,
            version_label="V770",
            claim="Diagnostic crop residual milestone is tracked as local dogfooding context.",
            status=VGGTEvidenceStatus.LOCAL_OBSERVED,
            evidence_refs=[summary_ref],
            source_files=[str(summary_path)],
            limitations=["Local scan confirms project co-location, not result artifact quality."],
            blockers=[],
            next_actions=["Attach artifact-backed diagnostic output before promotion."],
        ),
        VGGTEvidenceRow(
            run_id=run_id,
            version_label="V129",
            claim="SMPL-X anchored completion is recorded as engineering context.",
            status=VGGTEvidenceStatus.OBSERVED,
            evidence_refs=[engineering_ref],
            source_files=[str(summary_path)],
            limitations=["Full-body completion and hairline regression remain unresolved."],
            blockers=[],
            next_actions=["Require artifact-backed visual and metric evidence."],
        ),
        VGGTEvidenceRow(
            run_id=run_id,
            version_label="V260",
            claim="Semantic-temporal fusion route is hard-blocked for Sprint 1 evidence use.",
            status=VGGTEvidenceStatus.HARD_BLOCKED,
            evidence_refs=[engineering_ref],
            source_files=[str(artifact_index_path)],
            limitations=["No committed artifact confirms adjacent predictions or semantic assets."],
            blockers=["Required semantic assets are unavailable in the local scan."],
            next_actions=["Keep out of advisor-ready claims until artifacts are supplied."],
        ),
        VGGTEvidenceRow(
            run_id=run_id,
            version_label="V900",
            claim="Feature adapter entrypoint is recorded as observed engineering context.",
            status=VGGTEvidenceStatus.OBSERVED,
            evidence_refs=[engineering_ref],
            source_files=[str(summary_path)],
            limitations=["Architecture entrypoint is not enough to prove experiment success."],
            blockers=[],
            next_actions=["Attach run artifacts and metrics when available."],
        ),
        VGGTEvidenceRow(
            run_id=run_id,
            version_label="V930",
            claim="HumanRAM-style tri-plane adapter has an observed short-training signal.",
            status=VGGTEvidenceStatus.OBSERVED,
            evidence_refs=[engineering_ref],
            source_files=[str(summary_path)],
            limitations=["Short-training signal is not a completed VGGT result."],
            blockers=[],
            next_actions=["Collect repeatable run evidence and visual comparisons."],
        ),
        VGGTEvidenceRow(
            run_id=run_id,
            version_label="V999",
            claim="Long-run triplane-only route status is observed as engineering context.",
            status=VGGTEvidenceStatus.OBSERVED,
            evidence_refs=[engineering_ref],
            source_files=[str(summary_path)],
            limitations=["SparseConv3D success is not proven by this route status."],
            blockers=[],
            next_actions=["Separate route status from SparseConv3D backend success."],
        ),
        VGGTEvidenceRow(
            run_id=run_id,
            version_label="V999-SparseConv3D",
            claim="SparseConv3D backend success is not established by current local evidence.",
            status=VGGTEvidenceStatus.NOT_ENOUGH_EVIDENCE,
            evidence_refs=[artifact_ref],
            source_files=[str(artifact_index_path)],
            limitations=["Artifact index reports no scanned artifacts."],
            blockers=[
                "No local evidence ledger or backend artifact confirms SparseConv3D success.",
            ],
            next_actions=["Require real run artifact, sidecar, and evidence ledger entry."],
        ),
        VGGTEvidenceRow(
            run_id=run_id,
            version_label="V120",
            claim="Modal real spconv backend success requires human review.",
            status=VGGTEvidenceStatus.REQUIRES_HUMAN_REVIEW,
            evidence_refs=[],
            source_files=[],
            limitations=["No local evidence ledger JSON is committed."],
            blockers=["V120 cannot be local-observed without explicit local evidence."],
            next_actions=["Provide local_scan_evidence_ledger.json or artifact-backed report."],
        ),
        VGGTEvidenceRow(
            run_id=run_id,
            version_label="V121",
            claim="True region pointcloud visual gate requires human review.",
            status=VGGTEvidenceStatus.REQUIRES_HUMAN_REVIEW,
            evidence_refs=[],
            source_files=[],
            limitations=["No visual inventory is committed."],
            blockers=["V121 cannot be local-observed without visual inventory evidence."],
            next_actions=["Provide local_scan_visual_inventory.md with provenance."],
        ),
    ]


def _evidence_ref(path: Path, locator: str, quote: str, confidence: float) -> EvidenceRef:
    return EvidenceRef(
        source_id=path.name,
        locator=locator,
        quote=quote,
        confidence=confidence,
    )


def _quote_or_default(text: str, marker: str) -> str:
    for line in text.splitlines():
        stripped = line.strip("- ").strip()
        if marker.lower() in stripped.lower():
            return stripped[:220]
    return marker


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
