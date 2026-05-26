"""Models for pod workflow packs."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.git_handoff.models import ContextPackage, StructuredOutputTemplate


class PodWorkflowPackBuildInput(BaseModel):
    """Input for building a pod workflow pack from an existing route pack."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str = Field(default="vggt-modal-sparseconv-pod-pack", min_length=1)
    route_id: str = Field(default="modal_sparseconv_real_v0", min_length=1)
    route_pack_dir: Path
    output_dir: Path
    advisor_intent: str = (
        "Prepare a review-only VGGT Modal SparseConv3D route execution package without "
        "claiming success."
    )
    source_machine_label: str = "local-planning-machine"


class PodWorkflowPack(BaseModel):
    """Generated pod workflow pack metadata."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    output_dir: str = Field(min_length=1)
    context_package: ContextPackage
    structured_output_template: StructuredOutputTemplate
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    def to_markdown(self) -> str:
        """Render pod workflow pack summary."""

        lines = [
            f"# Pod Workflow Pack: {self.pack_id}",
            "",
            f"- Route: `{self.route_id}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            "- Execution: not executed by TuringResearch",
            "- Remote control: not provided",
            "",
            "## Context Package",
            "",
            f"- Package: `{self.context_package.package_id}`",
            f"- Files: {len(self.context_package.context_files)}",
            "",
            "## Structured Output Template",
            "",
            *[f"- `{item}`" for item in self.structured_output_template.output_files],
            "",
            "## Warnings",
            "",
        ]
        lines.extend([f"- {item}" for item in self.warnings] or ["- None."])
        return "\n".join(lines) + "\n"
