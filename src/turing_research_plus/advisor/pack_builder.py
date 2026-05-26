"""Build Markdown-only advisor packs from Sprint 1 artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from turing_research_plus.advisor.models import (
    AdvisorPack,
    AdvisorPackBuildInput,
    AdvisorPackSection,
    AdvisorReadinessStatus,
)
from turing_research_plus.advisor.sections import (
    render_current_status,
    render_evidence_summary,
    render_failure_analysis,
    render_next_actions,
    render_visual_readiness,
)
from turing_research_plus.advisor.templates import (
    ADVISOR_MESSAGE_TEMPLATE,
    CURRENT_ROUTE_TEMPLATE,
    NO_FABRICATION_NOTICE,
)
from turing_research_plus.artifact_audit.auditor import audit_artifacts
from turing_research_plus.artifact_audit.models import ArtifactAuditInput, ArtifactAuditReport
from turing_research_plus.vggt.evidence_ledger import build_vggt_evidence_ledger
from turing_research_plus.vggt.evidence_models import (
    VGGTEvidenceLedger,
    VGGTEvidenceLedgerBuildInput,
    VGGTEvidenceStatus,
)


def build_advisor_pack(request: AdvisorPackBuildInput) -> AdvisorPack:
    """Build a conservative advisor pack without reading private VGGT paths."""

    missing_inputs = _missing_inputs(request)
    file_text = _read_optional_texts(request, missing_inputs)
    ledger = build_vggt_evidence_ledger(
        VGGTEvidenceLedgerBuildInput(
            run_id=request.pack_id,
            local_scan_summary_path=request.local_scan_summary_path,
            local_scan_artifact_index_path=request.local_scan_artifact_index_path,
            local_scan_evidence_ledger_path=request.local_scan_evidence_ledger_path,
        )
    )
    audit_report = audit_artifacts(
        ArtifactAuditInput(source_path=request.local_scan_artifact_index_path)
    )
    missing_inputs.extend(ledger.missing_inputs)

    visual_scorecard = _read_visual_scorecard(request.visual_evidence_scorecard_path)
    visual_blocked = _visual_is_blocked(visual_scorecard, file_text)
    observed_evidence = _observed_evidence(ledger)
    limitations = _limitations(ledger, audit_report, visual_blocked)
    blockers = _blockers(ledger, audit_report, visual_blocked)
    not_ready_claims = _not_ready_claims(ledger, visual_blocked)
    next_actions = _next_actions(ledger, visual_blocked)
    required_human_review = _required_human_review(missing_inputs, visual_blocked)

    pack = AdvisorPack(
        pack_id=request.pack_id,
        advisor_goal=request.advisor_goal,
        current_route_summary=CURRENT_ROUTE_TEMPLATE,
        what_changed_since_last_update=[
            "The working direction is now SMPL-X feature encoding, not direct SMPL-X replacement.",
            (
                "Evidence is summarized from the VGGT evidence ledger, artifact audit, "
                "and visual dry-run outputs."
            ),
            (
                "Missing visual proof is explicitly blocked instead of being presented "
                "as advisor-ready."
            ),
        ],
        observed_evidence=observed_evidence,
        limitations=limitations,
        blockers=blockers,
        visual_readiness=AdvisorReadinessStatus.BLOCKED
        if visual_blocked
        else AdvisorReadinessStatus.READY_FOR_REVIEW,
        not_ready_claims=not_ready_claims,
        next_actions=next_actions,
        suggested_advisor_message=ADVISOR_MESSAGE_TEMPLATE,
        required_human_review=required_human_review,
        missing_inputs=_dedupe(missing_inputs),
        sections=[],
    )
    return pack.model_copy(update={"sections": _sections_for(pack)})


def write_advisor_pack(request: AdvisorPackBuildInput) -> AdvisorPack:
    """Build and write the advisor pack Markdown files."""

    if request.output_dir is None:
        raise ValueError("output_dir is required when writing advisor pack files")
    pack = build_advisor_pack(request)
    request.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "advisor_summary.md": pack.to_markdown(),
        "current_status.md": render_current_status(pack),
        "evidence_summary.md": render_evidence_summary(pack),
        "visual_readiness.md": render_visual_readiness(pack),
        "failure_analysis.md": render_failure_analysis(pack),
        "next_actions.md": render_next_actions(pack),
    }
    for filename, content in outputs.items():
        (request.output_dir / filename).write_text(content, encoding="utf-8")
    return pack


def advisor_pack_build(request: AdvisorPackBuildInput) -> dict[str, Any]:
    """Capsule-local thin wrapper for the proposed advisor.pack_build tool."""

    return build_advisor_pack(request).model_dump(mode="json")


def _missing_inputs(request: AdvisorPackBuildInput) -> list[str]:
    paths = [
        request.dogfooding_doc_path,
        request.vggt_evidence_doc_path,
        request.artifact_auditor_doc_path,
        request.visual_evidence_doc_path,
        request.sprint_plan_path,
        request.risk_register_path,
        request.local_scan_summary_path,
        request.local_scan_artifact_index_path,
        request.local_scan_evidence_ledger_path,
        request.visual_evidence_audit_report_path,
        request.visual_evidence_missing_items_path,
    ]
    return [str(path) for path in paths if path is not None and not path.exists()]


def _read_optional_texts(
    request: AdvisorPackBuildInput,
    missing_inputs: list[str],
) -> dict[str, str]:
    texts: dict[str, str] = {}
    for field_name in [
        "dogfooding_doc_path",
        "vggt_evidence_doc_path",
        "artifact_auditor_doc_path",
        "visual_evidence_doc_path",
        "sprint_plan_path",
        "risk_register_path",
        "local_scan_summary_path",
        "local_scan_artifact_index_path",
        "visual_evidence_audit_report_path",
        "visual_evidence_missing_items_path",
    ]:
        path = getattr(request, field_name)
        if path is None:
            continue
        if path.exists():
            texts[field_name] = path.read_text(encoding="utf-8")
        elif str(path) not in missing_inputs:
            missing_inputs.append(str(path))
    return texts


def _read_visual_scorecard(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _visual_is_blocked(scorecard: dict[str, Any], texts: dict[str, str]) -> bool:
    if scorecard:
        return scorecard.get("advisor_ready_visual_proof") is not True
    combined = "\n".join(texts.values()).lower()
    return "visual inventory" in combined and ("missing" in combined or "blocked" in combined)


def _observed_evidence(ledger: VGGTEvidenceLedger) -> list[str]:
    return [
        f"{row.version_label}: {row.status.value} - {row.claim}"
        for row in ledger.rows
        if row.status in {VGGTEvidenceStatus.OBSERVED, VGGTEvidenceStatus.LOCAL_OBSERVED}
    ]


def _limitations(
    ledger: VGGTEvidenceLedger,
    audit_report: ArtifactAuditReport,
    visual_blocked: bool,
) -> list[str]:
    values: list[str] = []
    for row in ledger.rows:
        values.extend(f"{row.version_label}: {item}" for item in row.limitations)
    values.extend(audit_report.warnings)
    if visual_blocked:
        values.append(
            "Visual proof is missing; proxy or absent boards cannot support "
            "advisor-ready proof."
        )
    values.append(NO_FABRICATION_NOTICE)
    return _dedupe(values)


def _blockers(
    ledger: VGGTEvidenceLedger,
    audit_report: ArtifactAuditReport,
    visual_blocked: bool,
) -> list[str]:
    values: list[str] = []
    for row in ledger.rows:
        values.extend(f"{row.version_label}: {item}" for item in row.blockers)
    if audit_report.records == []:
        values.append("Artifact audit found no scanned artifacts.")
    if visual_blocked:
        values.append("Full body, hairline, and hand close-up visual proof are missing.")
    return _dedupe(values)


def _not_ready_claims(ledger: VGGTEvidenceLedger, visual_blocked: bool) -> list[str]:
    claims = [
        "V260 is hard-blocked and must not be described as a successful route.",
        "V999 long-run route status is not final target achievement.",
        "SparseConv3D success is not complete without real evidence.",
        "Modal Real SparseConv3D is planned / next action, not an observed result.",
    ]
    for row in ledger.rows:
        if row.status in {
            VGGTEvidenceStatus.HARD_BLOCKED,
            VGGTEvidenceStatus.REQUIRES_HUMAN_REVIEW,
            VGGTEvidenceStatus.NOT_ENOUGH_EVIDENCE,
            VGGTEvidenceStatus.REQUIRES_REAL_EXPERIMENT,
        }:
            claims.append(f"{row.version_label}: {row.claim} ({row.status.value}).")
    if visual_blocked:
        claims.append(
            "Advisor visual readiness is not ready because required visual proof is missing."
        )
    return _dedupe(claims)


def _next_actions(ledger: VGGTEvidenceLedger, visual_blocked: bool) -> list[str]:
    actions: list[str] = []
    for row in ledger.rows:
        actions.extend(f"{row.version_label}: {item}" for item in row.next_actions)
    if visual_blocked:
        actions.extend(
            [
                "Produce local_scan_visual_inventory.md with board provenance.",
                "Collect full-body, hairline, and hand close-up visual evidence.",
                "Keep proxy, mask, and delta boards separate from advisor-ready proof.",
            ]
        )
    actions.append(
        "Run Modal Real SparseConv3D only as a future planned experiment with "
        "artifact-backed evidence."
    )
    return _dedupe(actions)


def _required_human_review(missing_inputs: list[str], visual_blocked: bool) -> list[str]:
    review = [f"Missing input requires review: {item}" for item in _dedupe(missing_inputs)]
    if visual_blocked:
        review.append("Human review is required before any visual readiness claim.")
    return review


def _sections_for(pack: AdvisorPack) -> list[AdvisorPackSection]:
    return [
        AdvisorPackSection(
            section_id="current_status",
            title="Current Status",
            status=AdvisorReadinessStatus.REQUIRES_HUMAN_REVIEW,
            body=render_current_status(pack),
            missing_inputs=pack.missing_inputs,
        ),
        AdvisorPackSection(
            section_id="evidence_summary",
            title="Evidence Summary",
            status=AdvisorReadinessStatus.REQUIRES_HUMAN_REVIEW,
            body=render_evidence_summary(pack),
            missing_inputs=pack.missing_inputs,
        ),
        AdvisorPackSection(
            section_id="visual_readiness",
            title="Visual Readiness",
            status=pack.visual_readiness,
            body=render_visual_readiness(pack),
            missing_inputs=pack.missing_inputs,
        ),
        AdvisorPackSection(
            section_id="failure_analysis",
            title="Failure Analysis",
            status=AdvisorReadinessStatus.REQUIRES_HUMAN_REVIEW,
            body=render_failure_analysis(pack),
            missing_inputs=pack.missing_inputs,
        ),
        AdvisorPackSection(
            section_id="next_actions",
            title="Next Actions",
            status=AdvisorReadinessStatus.REQUIRES_HUMAN_REVIEW,
            body=render_next_actions(pack),
            missing_inputs=pack.missing_inputs,
        ),
    ]


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
