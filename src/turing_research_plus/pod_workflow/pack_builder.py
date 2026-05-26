"""Build pod workflow packs from route pack artifacts."""

from __future__ import annotations

import shutil
from pathlib import Path

from turing_research_plus.git_handoff.context_package import build_context_package
from turing_research_plus.git_handoff.models import ContextPackageBuildInput
from turing_research_plus.git_handoff.structured_output import (
    build_structured_output_template,
    write_structured_output_template,
)
from turing_research_plus.pod_workflow.models import PodWorkflowPack, PodWorkflowPackBuildInput
from turing_research_plus.pod_workflow.templates import memory_summary, project_context, readme


def build_vggt_modal_pod_workflow_pack(request: PodWorkflowPackBuildInput) -> PodWorkflowPack:
    """Build a minimal VGGT Modal pod workflow pack."""

    route_pack = request.route_pack_dir
    output_dir = request.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    route_spec = _read_required(route_pack / "route_spec.yaml")
    hard_gates = _read_required(route_pack / "hard_gates.md")
    artifact_requirements = _read_required(route_pack / "artifact_requirements.md")
    failure_taxonomy = _read_required(route_pack / "failure_taxonomy.md")
    advisor_summary = _read_optional(route_pack / "advisor_summary.md")
    architecture = route_pack / "architecture.mmd"
    if architecture.exists():
        shutil.copy2(architecture, output_dir / "architecture.mmd")

    context = build_context_package(
        ContextPackageBuildInput(
            package_id=f"{request.pack_id}-context",
            route_id=request.route_id,
            output_dir=output_dir,
            project_context=project_context(request.route_id),
            memory_summary=memory_summary(request.route_id),
            route_spec_text=_planned_header("ROUTE_SPEC.yaml") + route_spec,
            hard_gates_text=hard_gates,
            artifact_requirements_text=artifact_requirements,
            failure_taxonomy_text=failure_taxonomy,
            advisor_intent=request.advisor_intent + "\n\n" + advisor_summary,
            readme_text=readme(request.pack_id, request.route_id),
            source_refs={
                "ROUTE_SPEC.yaml": str(route_pack / "route_spec.yaml"),
                "HARD_GATES.md": str(route_pack / "hard_gates.md"),
                "ARTIFACT_REQUIREMENTS.md": str(route_pack / "artifact_requirements.md"),
                "FAILURE_TAXONOMY.md": str(route_pack / "failure_taxonomy.md"),
            },
        )
    )
    template = build_structured_output_template(route_id=request.route_id)
    write_structured_output_template(output_dir / "STRUCTURED_OUTPUT_TEMPLATE", template)
    pack = PodWorkflowPack(
        pack_id=request.pack_id,
        route_id=request.route_id,
        output_dir=str(output_dir),
        context_package=context,
        structured_output_template=template,
        warnings=[
            "planned route only",
            "not executed by TuringResearch",
            "requires-real-experiment",
        ],
        requires_human_review=True,
    )
    (output_dir / "POD_WORKFLOW_PACK.md").write_text(pack.to_markdown(), encoding="utf-8")
    return pack


def _read_required(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def _read_optional(path: Path) -> str:
    if not path.exists():
        return "Missing advisor summary; requires human review.\n"
    return path.read_text(encoding="utf-8")


def _planned_header(filename: str) -> str:
    return (
        f"# Source: {filename}\n"
        "# Status: planned\n"
        "# Execution: not executed by TuringResearch\n"
        "# Requires real experiment: true\n\n"
    )
