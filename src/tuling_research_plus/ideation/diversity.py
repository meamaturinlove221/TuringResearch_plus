"""Quality-diversity filtering."""

from __future__ import annotations

from tuling_research_plus.ideation.models import (
    DiversityFilterReport,
    IdeaCandidate,
    IdeaGenerationResult,
)


def quality_diversity_filter(
    generation: IdeaGenerationResult,
    report_id: str = "idea-diversity-1",
) -> DiversityFilterReport:
    """Retain one highest-quality idea per diversity cluster."""

    retained_by_signature: dict[tuple[object, ...], IdeaCandidate] = {}
    rejected: list[IdeaCandidate] = []
    for candidate in generation.candidates:
        signature = candidate.cluster_key.signature()
        existing = retained_by_signature.get(signature)
        if existing is None:
            retained_by_signature[signature] = candidate
            continue
        if candidate.quality_score > existing.quality_score:
            rejected.append(existing)
            retained_by_signature[signature] = candidate
        else:
            rejected.append(candidate)

    retained = sorted(
        retained_by_signature.values(),
        key=lambda candidate: candidate.quality_score,
        reverse=True,
    )
    return DiversityFilterReport(
        report_id=report_id,
        retained=retained,
        rejected_duplicates=rejected,
        cluster_count=len(retained_by_signature),
    )

