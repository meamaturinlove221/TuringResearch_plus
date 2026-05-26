"""Build conservative related-work positioning reports."""

from __future__ import annotations

from turing_research_plus.related_work.claim_safety import (
    build_missing_evidence,
    build_safe_claims,
    build_unsafe_claims,
)
from turing_research_plus.related_work.grouping import group_method_cards
from turing_research_plus.related_work.models import (
    MethodCluster,
    PaperGroup,
    PaperGroupEntry,
    RelatedWorkPositioningInput,
    RelatedWorkPositioningReport,
)


def build_related_work_positioning(
    request: RelatedWorkPositioningInput,
) -> RelatedWorkPositioningReport:
    """Build a conservative related-work positioning report."""

    groups = group_method_cards(request.method_cards)
    groups.extend(_groups_from_collision_report(request.collision_report))
    groups = _dedupe_groups(groups)
    method_clusters = _build_clusters(groups)
    return RelatedWorkPositioningReport(
        project_topic=request.project_topic,
        paper_groups=groups,
        method_clusters=method_clusters,
        overlap_summary=_overlap_summary(groups),
        differentiation_points=_differentiation_points(),
        safe_claims=build_safe_claims(groups),
        unsafe_claims=build_unsafe_claims(),
        missing_evidence=build_missing_evidence(groups),
        recommended_related_work_structure=_recommended_structure(),
        requires_human_review=True,
    )


def _groups_from_collision_report(report: dict[str, object] | None) -> list[PaperGroupEntry]:
    if not report:
        return []
    risk_scores = report.get("risk_scores")
    if not isinstance(risk_scores, list):
        return []
    groups: list[PaperGroupEntry] = []
    for item in risk_scores:
        if not isinstance(item, dict):
            continue
        paper_id = str(item.get("paper_id") or item.get("title") or "unknown")
        title = str(item.get("title") or paper_id)
        lowered = title.lower()
        if "hart" in lowered:
            group = PaperGroup.RECONSTRUCTION_OR_ANIMATION
            rationale = "HART may be close to human reconstruction and needs focused review."
        elif "vggt-hpe" in lowered:
            group = PaperGroup.VGGT_HUMAN_EXTENSIONS
            rationale = "VGGT-HPE may be lower risk if head-pose only, but details need review."
        elif "hggt" in lowered or "fus3d" in lowered:
            group = PaperGroup.UNKNOWN_OR_REQUIRES_REVIEW
            rationale = "Requires real paper review before positioning."
        else:
            group = PaperGroup.UNKNOWN_OR_REQUIRES_REVIEW
            rationale = "Collision report marks this item as requiring review."
        groups.append(
            PaperGroupEntry(
                paper_id=paper_id,
                title=title,
                group=group,
                rationale=rationale,
                requires_real_paper_review=True,
            )
        )
    return groups


def _dedupe_groups(groups: list[PaperGroupEntry]) -> list[PaperGroupEntry]:
    deduped: dict[str, PaperGroupEntry] = {}
    for group in groups:
        deduped[group.paper_id] = group
    return list(deduped.values())


def _build_clusters(groups: list[PaperGroupEntry]) -> list[MethodCluster]:
    clusters: list[MethodCluster] = []
    by_group: dict[PaperGroup, list[str]] = {}
    for group in groups:
        by_group.setdefault(group.group, []).append(group.paper_id)
    for paper_group, papers in by_group.items():
        clusters.append(
            MethodCluster(
                cluster_id=paper_group.value,
                title=paper_group.value.replace("_", " ").title(),
                papers=papers,
                positioning_note=_cluster_note(paper_group),
                requires_human_review=True,
            )
        )
    return clusters


def _cluster_note(group: PaperGroup) -> str:
    notes = {
        PaperGroup.NEURALBODY_SPARSE_VOXEL: (
            "Use as sparse voxel / structured latent inspiration, not direct VGGT objective match."
        ),
        PaperGroup.HUMANRAM_TRIPLANE_RASTER: (
            "Use as SMPL-X canonical / tri-plane / rasterized token inspiration."
        ),
        PaperGroup.VGGT_HUMAN_EXTENSIONS: (
            "Review as potentially close VGGT-human extension work before positioning."
        ),
        PaperGroup.UNKNOWN_OR_REQUIRES_REVIEW: (
            "Do not position strongly until real paper review exists."
        ),
    }
    return notes.get(group, "Use for context only until evidence-backed review is complete.")


def _overlap_summary(groups: list[PaperGroupEntry]) -> list[str]:
    summary = [
        "SMPL / SMPL-X representation overlap is relevant but not enough to prove collision.",
        "Human-prior methods should be separated by task, output target, and integration point.",
    ]
    for group in groups:
        if group.group == PaperGroup.NEURALBODY_SPARSE_VOXEL:
            summary.append(
                "NeuralBody: SMPL structured latent / sparse voxel inspiration; "
                "target differs from VGGT point completion."
            )
        if group.group == PaperGroup.HUMANRAM_TRIPLANE_RASTER:
            summary.append(
                "HumanRAM: SMPL-X canonical / tri-plane / rasterized token inspiration; "
                "output target differs."
            )
    return list(dict.fromkeys(summary))


def _differentiation_points() -> list[str]:
    return [
        "Frame the project as VGGT-side SMPL-X feature encoding, not direct SMPL-X replacement.",
        "Differentiate by integration point: VGGT token / point residual path "
        "rather than standalone human rendering.",
        "Separate implementation backend claims from scientific contribution claims.",
        "Keep SparseConv3D claims at planned / requires-real-experiment until evidence exists.",
    ]


def _recommended_structure() -> list[str]:
    return [
        "Feed-forward geometry and VGGT context",
        "Human priors and SMPL / SMPL-X representations",
        "Sparse voxel and tri-plane inspiration",
        "VGGT human-extension and close-risk papers requiring review",
        "Positioning of SMPL-X feature encoding for VGGT",
    ]
