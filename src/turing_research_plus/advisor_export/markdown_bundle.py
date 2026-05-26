"""Build Markdown source bundles for advisor export."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
    AdvisorMarkdownBundleRequest,
)

BUNDLE_FILENAMES = [
    "advisor_report_source.md",
    "slides_outline.md",
    "figure_list.md",
    "table_list.md",
    "evidence_refs.md",
    "limitations.md",
    "next_actions.md",
    "manifest.yaml",
]


def build_advisor_markdown_bundle(
    request: AdvisorMarkdownBundleRequest,
    *,
    write_files: bool = True,
) -> AdvisorMarkdownBundle:
    """Build a Markdown source bundle from existing local review artifacts."""

    output_dir = request.output_dir
    advisor_summary = _read_optional(request.advisor_pack_dir / "advisor_summary.md")
    current_status = _read_optional(request.advisor_pack_dir / "current_status.md")
    evidence_summary = _read_optional(request.advisor_pack_dir / "evidence_summary.md")
    limitations = _read_optional(request.knowledge_pack_dir / "current_state.md")
    next_actions = _read_optional(request.knowledge_pack_dir / "next_actions.md")
    advisor_brief = _read_optional(request.knowledge_pack_dir / "advisor_brief.md")

    contents = {
        "README.md": _readme(request),
        "advisor_report_source.md": _advisor_report_source(
            request,
            advisor_summary,
            current_status,
            advisor_brief,
        ),
        "slides_outline.md": _slides_outline(request),
        "figure_list.md": _figure_list(),
        "table_list.md": _table_list(),
        "evidence_refs.md": _evidence_refs(evidence_summary),
        "limitations.md": _limitations(limitations),
        "next_actions.md": _next_actions(next_actions),
        "manifest.yaml": _manifest(request),
    }
    if write_files:
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in contents.items():
            (output_dir / filename).write_text(content, encoding="utf-8")

    files = [
        AdvisorBundleFile(
            path=str(output_dir / filename),
            role=_role_for(filename),
            source_refs=_source_refs_for(filename, request),
        )
        for filename in BUNDLE_FILENAMES
    ]
    return AdvisorMarkdownBundle(
        bundle_id=request.bundle_id,
        topic=request.topic,
        output_dir=str(output_dir),
        files=files,
        source_paths=[
            str(request.advisor_pack_dir),
            str(request.knowledge_pack_dir),
        ],
        limitations=[
            "Markdown source bundle only.",
            "No PDF, PPTX, DOCX, or HTML file was generated.",
            "Planned work remains planned and is not observed evidence.",
            "SparseConv3D success is not claimed by this bundle.",
        ],
    )


def _read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else f"Missing input: {path}\n"


def _readme(request: AdvisorMarkdownBundleRequest) -> str:
    return (
        "# Advisor Markdown Bundle\n\n"
        f"- Bundle ID: `{request.bundle_id}`\n"
        f"- Topic: {request.topic}\n"
        "- Status: Markdown source package only.\n"
        "- No PDF or PPTX was generated.\n"
        "- Human review is required before advisor delivery.\n"
    )


def _advisor_report_source(
    request: AdvisorMarkdownBundleRequest,
    advisor_summary: str,
    current_status: str,
    advisor_brief: str,
) -> str:
    return "\n".join(
        [
            "# Advisor Report Source",
            "",
            f"Topic: {request.topic}",
            "",
            "## Advisor Summary",
            "",
            advisor_summary.strip(),
            "",
            "## Current Status",
            "",
            current_status.strip(),
            "",
            "## Advisor Brief",
            "",
            advisor_brief.strip(),
            "",
            "## Boundary",
            "",
            "- This source bundle did not generate PDF or PPTX.",
            "- This source bundle did not run VGGT or Modal.",
            "- Planned work is not observed evidence.",
            "- SparseConv3D success is not claimed.",
            "",
        ]
    )


def _slides_outline(request: AdvisorMarkdownBundleRequest) -> str:
    return "\n".join(
        [
            "# Slides Outline",
            "",
            "1. North Star",
            "2. Current Evidence State",
            "3. Artifact and Visual Readiness",
            "4. Failure Modes and Hard Gates",
            "5. Experiment Routes",
            "6. Related Work Positioning",
            "7. Next Actions",
            "",
            "Note: this is an outline only. No PPTX file was generated.",
            f"Topic: {request.topic}",
            "",
        ]
    )


def _figure_list() -> str:
    return (
        "# Figure List\n\n"
        "- No generated figures are included.\n"
        "- Candidate figures must be backed by existing local artifacts.\n"
        "- Do not invent charts, boards, or architecture figures.\n"
    )


def _table_list() -> str:
    return (
        "# Table List\n\n"
        "- Evidence status table: source from existing advisor and knowledge packs.\n"
        "- Artifact completeness table: source from existing audit material.\n"
        "- Failure mode table: source from existing failure taxonomy material.\n"
        "- No synthetic experiment table was generated.\n"
    )


def _evidence_refs(evidence_summary: str) -> str:
    return "# Evidence Refs\n\n" + evidence_summary.strip() + "\n"


def _limitations(limitations: str) -> str:
    return (
        "# Limitations\n\n"
        + limitations.strip()
        + "\n\n"
        "- Markdown bundle only; no binary export generated.\n"
        "- Requires human review.\n"
    )


def _next_actions(next_actions: str) -> str:
    return "# Next Actions\n\n" + next_actions.strip() + "\n"


def _manifest(request: AdvisorMarkdownBundleRequest) -> str:
    files = ["README.md", *BUNDLE_FILENAMES]
    lines = [
        f"bundle_id: {request.bundle_id}",
        f"topic: {request.topic}",
        "status: markdown-source-ready",
        "requires_human_review: true",
        "generated_binary_exports: false",
        "future_exports:",
        "  - pdf",
        "  - pptx",
        "  - docx",
        "  - html",
        "files:",
    ]
    lines.extend([f"  - {filename}" for filename in files])
    lines.extend(
        [
            "boundaries:",
            "  - no_pdf_generated",
            "  - no_pptx_generated",
            "  - no_external_converter_called",
            "  - no_planned_as_observed",
            "  - no_fake_figures",
            "  - requires_human_review",
            "",
        ]
    )
    return "\n".join(lines)


def _role_for(filename: str) -> str:
    return filename.removesuffix(".md").removesuffix(".yaml").replace("_", "-")


def _source_refs_for(filename: str, request: AdvisorMarkdownBundleRequest) -> list[str]:
    if filename in {"advisor_report_source.md", "evidence_refs.md"}:
        return [str(request.advisor_pack_dir)]
    if filename in {"limitations.md", "next_actions.md"}:
        return [str(request.knowledge_pack_dir)]
    return []
