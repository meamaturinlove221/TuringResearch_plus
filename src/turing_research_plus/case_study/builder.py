"""Build sanitized public case study drafts."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.case_study.claim_guard import guard_case_study_claims
from turing_research_plus.case_study.models import (
    CaseStudyDraft,
    CaseStudyRedactionReport,
    CaseStudySection,
)
from turing_research_plus.case_study.redactor import redact_public_case_study_text


def build_vggt_public_case_study(root: Path) -> CaseStudyDraft:
    """Build a sanitized VGGT public case study draft from local review artifacts."""

    pack = root / "examples" / "vggt-human-prior-survey" / "research_knowledge_pack"
    source_paths = {
        "north_star": pack / "north_star.md",
        "current_state": pack / "current_state.md",
        "evidence_summary": pack / "evidence_summary.md",
        "failure_taxonomy": pack / "failure_taxonomy.md",
        "advisor_brief": pack / "advisor_brief.md",
        "next_actions": pack / "next_actions.md",
    }
    source_text = "\n\n".join(path.read_text(encoding="utf-8") for path in source_paths.values())
    _, redaction_report = redact_public_case_study_text(source_text)
    raw_sections = _build_vggt_sections(source_paths)
    draft_text = "\n".join(bullet for section in raw_sections for bullet in section.bullets)
    sanitized_text, draft_redactions = redact_public_case_study_text(draft_text)
    redaction_report = _merge_redaction_reports(redaction_report, draft_redactions)
    claim_report = guard_case_study_claims(sanitized_text)

    return CaseStudyDraft(
        case_study_id="vggt_public_case_study_draft",
        title="VGGT Human Prior Dogfooding Case Study Draft",
        problem_background=raw_sections[0],
        why_turingresearch_was_useful=raw_sections[1],
        route_changes=raw_sections[2],
        evidence_management=raw_sections[3],
        failures_and_blockers=raw_sections[4],
        advisor_pack=raw_sections[5],
        what_remains_human_work=raw_sections[6],
        what_not_to_claim=raw_sections[7],
        redaction_report=redaction_report,
        claim_safety_report=claim_report,
    )


def _build_vggt_sections(source_paths: dict[str, Path]) -> list[CaseStudySection]:
    refs = {key: path.as_posix() for key, path in source_paths.items()}
    return [
        CaseStudySection(
            section_id="problem-background",
            title="Problem Background",
            bullets=[
                "The VGGT dogfooding line explored how human-prior structure "
                "could be organized for a future VGGT-side experiment.",
                "The safest public framing is the North Star shift from direct "
                "SMPL-X replacement to SMPL-X feature encoding for VGGT.",
                "This draft is public-demo material and not a final research result.",
            ],
            evidence_refs=[refs["north_star"], refs["current_state"]],
        ),
        CaseStudySection(
            section_id="why-useful",
            title="Why TuringResearch Was Useful",
            bullets=[
                "It organized evidence states, artifacts, visual readiness, "
                "routes, related work, and advisor notes into reviewable artifacts.",
                "It kept planned routes separate from observed engineering context.",
                "It made missing evidence and unsafe claims visible before public communication.",
            ],
            evidence_refs=[refs["advisor_brief"], refs["evidence_summary"]],
        ),
        CaseStudySection(
            section_id="route-changes",
            title="Route Changes",
            bullets=[
                "The route changed away from direct replacement toward feature "
                "encoding and hard-gated experiment planning.",
                "V260 remains hard-blocked.",
                "Modal SparseConv3D remains planned / requires-real-experiment.",
                "V999-SparseConv3D remains not-enough-evidence.",
            ],
            evidence_refs=[refs["current_state"], refs["next_actions"]],
        ),
        CaseStudySection(
            section_id="evidence-management",
            title="Evidence Management",
            bullets=[
                "Evidence buckets distinguish observed engineering context, "
                "local-observed context, planned routes, hard-blocked states, "
                "and not-enough-evidence states.",
                "Artifact and visual readiness gaps remain explicit.",
                "No workspace index or dashboard display is treated as evidence by itself.",
            ],
            evidence_refs=[refs["evidence_summary"], refs["current_state"]],
        ),
        CaseStudySection(
            section_id="failures-and-blockers",
            title="Failures And Blockers",
            bullets=[
                "Failure taxonomy records missing assets, fallback-only paths, "
                "insufficient visual proof, and not-enough-evidence states.",
                "Sparse backend proof, predictions or thin summaries, visual "
                "boards, manifests, and cleanup reports remain missing.",
                "Failures are presented as research learning, not as successful results.",
            ],
            evidence_refs=[refs["failure_taxonomy"]],
        ),
        CaseStudySection(
            section_id="advisor-pack",
            title="Advisor Pack",
            bullets=[
                "Advisor material can state what is organized, what is missing, "
                "and what should be run next.",
                "Advisor-ready visual proof is not available in the current public draft.",
                "The recommended advisor ask is whether the planned route and "
                "hard gates are acceptable before larger experiment investment.",
            ],
            evidence_refs=[refs["advisor_brief"], refs["next_actions"]],
        ),
        CaseStudySection(
            section_id="human-work",
            title="What Remains Human Work",
            bullets=[
                "Run the real VGGT-side or Modal-side experiment outside this "
                "public case study draft.",
                "Review papers manually before final related-work wording.",
                "Interpret failures and approve final claims.",
                "Review privacy, license, and publication boundaries before release.",
            ],
            evidence_refs=[refs["next_actions"]],
        ),
        CaseStudySection(
            section_id="what-not-to-claim",
            title="What Not To Claim",
            bullets=[
                "Do not claim SparseConv3D success.",
                "Do not describe planned routes as executed or observed.",
                "Do not claim final paper conclusions.",
                "Do not include private local paths, restricted datasets, model "
                "files, non-public advisor notes, or non-public artifacts.",
            ],
            evidence_refs=[refs["evidence_summary"], refs["failure_taxonomy"]],
        ),
    ]


def _merge_redaction_reports(
    first: CaseStudyRedactionReport,
    second: CaseStudyRedactionReport,
) -> CaseStudyRedactionReport:
    return CaseStudyRedactionReport(
        redactions=[*first.redactions, *second.redactions],
        sanitized=first.sanitized and second.sanitized,
        release_blockers=[*first.release_blockers, *second.release_blockers],
    )
