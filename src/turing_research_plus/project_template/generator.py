"""Generate local research project skeletons."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.project_template.models import (
    ProjectTemplateFile,
    ProjectTemplateRequest,
    ProjectTemplateResult,
)
from turing_research_plus.project_template.renderers import render_research_template_file
from turing_research_plus.project_template.schema import (
    GeneratedResearchProjectFile,
    ResearchProjectTemplateManifest,
    ResearchProjectTemplateRequest,
)
from turing_research_plus.project_template.template_registry import (
    get_research_project_template,
)
from turing_research_plus.project_template.templates import (
    PROJECT_TEMPLATE_FILES,
    REQUIRED_DIRECTORIES,
)

RESEARCH_TEMPLATE_DIRECTORIES = [
    "docs",
    "lanes",
    "examples",
    "contracts",
    "race",
    "race/feature_capsules",
]


def generate_project_template(
    request: ProjectTemplateRequest,
    *,
    write_files: bool = True,
) -> ProjectTemplateResult:
    """Generate a local project skeleton without network or private data access."""

    output_dir = request.output_dir
    created_dirs: list[str] = []
    generated_files: list[ProjectTemplateFile] = []
    omitted_items: list[str] = []

    for directory in REQUIRED_DIRECTORIES:
        target = output_dir / directory
        created_dirs.append(directory)
        if write_files:
            target.mkdir(parents=True, exist_ok=True)

    for relative_path, (role, renderer) in PROJECT_TEMPLATE_FILES.items():
        target = output_dir / relative_path
        exists = target.exists()
        if exists and not request.overwrite:
            omitted_items.append(f"{relative_path}: already exists")
            generated_files.append(
                ProjectTemplateFile(
                    relative_path=relative_path,
                    role=role,
                    generated=False,
                    overwrite=False,
                )
            )
            continue

        if write_files:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(renderer(request), encoding="utf-8")
        generated_files.append(
            ProjectTemplateFile(
                relative_path=relative_path,
                role=role,
                generated=True,
                overwrite=exists and request.overwrite,
            )
        )

    return ProjectTemplateResult(
        project_id=request.project_id,
        project_name=request.project_name,
        output_dir=str(output_dir),
        generated_files=generated_files,
        created_directories=created_dirs,
        omitted_items=omitted_items,
        safety_warnings=[
            "Generated template contains no experiment results.",
            "Generated template must not be treated as observed evidence.",
            "Do not add secrets, raw data, or private model files to generated projects.",
        ],
    )


def summarize_project_template(result: ProjectTemplateResult) -> str:
    """Render a generated project template summary as Markdown."""

    lines = [
        f"# Project Template Summary: {result.project_name}",
        "",
        f"- Project ID: `{result.project_id}`",
        f"- Output dir: `{Path(result.output_dir).as_posix()}`",
        f"- Requires human review: `{str(result.requires_human_review).lower()}`",
        "",
        "## Generated Files",
        "",
    ]
    lines.extend(
        [
            f"- `{item.relative_path}` ({item.role}, generated={str(item.generated).lower()})"
            for item in result.generated_files
        ]
    )
    lines.extend(["", "## Omitted Items", ""])
    lines.extend([f"- {item}" for item in result.omitted_items] or ["- none"])
    lines.extend(["", "## Safety Warnings", ""])
    lines.extend([f"- {item}" for item in result.safety_warnings])
    lines.append("")
    return "\n".join(lines)


def generate_research_project_template(
    request: ResearchProjectTemplateRequest,
    *,
    write_files: bool = True,
) -> ResearchProjectTemplateManifest:
    """Generate a typed reusable research project skeleton."""

    template = get_research_project_template(request.template_type)
    output_dir = request.output_dir
    created_dirs: list[str] = []
    generated_files: list[GeneratedResearchProjectFile] = []
    omitted_items: list[str] = []

    for directory in RESEARCH_TEMPLATE_DIRECTORIES:
        target = output_dir / directory
        created_dirs.append(directory)
        if write_files:
            target.mkdir(parents=True, exist_ok=True)

    for section in template.sections:
        target = output_dir / section.relative_path
        exists = target.exists()
        if exists and not request.overwrite:
            omitted_items.append(f"{section.relative_path}: already exists")
            generated_files.append(
                GeneratedResearchProjectFile(
                    relative_path=section.relative_path,
                    role=section.role,
                    generated=False,
                    overwrite=False,
                )
            )
            continue
        if write_files:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                render_research_template_file(section.relative_path, request),
                encoding="utf-8",
            )
        generated_files.append(
            GeneratedResearchProjectFile(
                relative_path=section.relative_path,
                role=section.role,
                generated=True,
                overwrite=exists and request.overwrite,
            )
        )

    return ResearchProjectTemplateManifest(
        project_id=request.project_id,
        project_name=request.project_name,
        template_type=request.template_type,
        output_dir=str(output_dir),
        generated_files=generated_files,
        created_directories=created_dirs,
        omitted_items=omitted_items,
        safety_warnings=[
            "Generated content is template / placeholder material.",
            "Generated template contains no observed evidence.",
            "Generated template contains no real citations.",
            "Do not add secrets, raw data, or private model files.",
        ],
        requires_human_review=True,
        network_used=False,
        read_private_vggt=False,
        observed_evidence_generated=False,
    )


def summarize_research_project_template(result: ResearchProjectTemplateManifest) -> str:
    """Render a typed project template generation summary as Markdown."""

    lines = [
        f"# Research Project Template Summary: {result.project_name}",
        "",
        f"- Project ID: `{result.project_id}`",
        f"- Template type: `{result.template_type}`",
        f"- Output dir: `{Path(result.output_dir).as_posix()}`",
        f"- Requires human review: `{str(result.requires_human_review).lower()}`",
        "",
        "## Generated Files",
        "",
    ]
    lines.extend(
        [
            f"- `{item.relative_path}` ({item.role}, generated={str(item.generated).lower()})"
            for item in result.generated_files
        ]
    )
    lines.extend(["", "## Omitted Items", ""])
    lines.extend([f"- {item}" for item in result.omitted_items] or ["- none"])
    lines.extend(["", "## Safety Warnings", ""])
    lines.extend([f"- {item}" for item in result.safety_warnings])
    lines.append("")
    return "\n".join(lines)
