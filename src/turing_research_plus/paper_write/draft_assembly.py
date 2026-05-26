"""Assemble evidence-linked paper draft beta packages."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.citation_status_guard import (
    parse_citation_status_report,
    render_paper_citation_status_report,
)
from turing_research_plus.paper_write.claim_guard import (
    evaluate_paper_claims,
    render_paper_claim_guard_report,
)
from turing_research_plus.paper_write.draft_package import PaperDraftPackage


def assemble_paper_draft_beta(
    scaffold_dir: Path,
    *,
    package_id: str = "vggt_paper_draft_beta",
    topic: str = "VGGT / SMPL-X Human Prior",
) -> PaperDraftPackage:
    """Assemble a review-only paper draft package from existing scaffold files."""

    paper_outline = _read_required(scaffold_dir / "paper_outline.md")
    related_work = _read_required(scaffold_dir / "related_work_skeleton.md")
    method = _read_required(scaffold_dir / "method_section_skeleton.md")
    experiment = _read_required(scaffold_dir / "experiment_section_skeleton.md")
    result_guard = _read_required(scaffold_dir / "result_table_missing_items.md")
    evidence_gap = _read_required(scaffold_dir / "evidence_gap_report.md")
    citation_safety = _read_required(scaffold_dir / "citation_safety_report.md")

    section_texts = {
        "paper_outline": paper_outline,
        "related_work": related_work,
        "method": method,
        "experiment": experiment,
        "results": result_guard,
        "evidence_gap": evidence_gap,
    }
    claim_report = evaluate_paper_claims(section_texts)
    citation_report = parse_citation_status_report(citation_safety)

    return PaperDraftPackage(
        package_id=package_id,
        topic=topic,
        title_candidates=_extract_title_candidates(paper_outline),
        abstract_placeholder=(
            "Abstract placeholder only. Real abstract prose is blocked until "
            "evidence, citations, results, and human review are complete."
        ),
        introduction_skeleton=_extract_markdown_section(paper_outline, "### Introduction"),
        related_work_skeleton=related_work,
        method_skeleton=method,
        experiment_skeleton=experiment,
        results_blocked_section=result_guard,
        limitations=_extract_markdown_section(paper_outline, "### Limitations"),
        missing_evidence_report=evidence_gap,
        unsafe_claim_report=render_paper_claim_guard_report(claim_report),
        citation_status_report=render_paper_citation_status_report(citation_report),
    )


def _read_required(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"missing paper scaffold file: {path}")
    return path.read_text(encoding="utf-8").strip()


def _extract_title_candidates(markdown: str) -> list[str]:
    in_titles = False
    titles: list[str] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped == "## Title Candidates":
            in_titles = True
            continue
        if in_titles and stripped.startswith("## "):
            break
        if in_titles and stripped.startswith("- "):
            titles.append(stripped[2:].strip())
    return titles or ["Review-only paper draft beta"]


def _extract_markdown_section(markdown: str, heading: str) -> str:
    capture = False
    lines: list[str] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped == heading:
            capture = True
            lines.append(line)
            continue
        if capture and stripped.startswith("### "):
            break
        if capture:
            lines.append(line)
    return "\n".join(lines).strip() or f"{heading}\n\n- Section requires human review."
