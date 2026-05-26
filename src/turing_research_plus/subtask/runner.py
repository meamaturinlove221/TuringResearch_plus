"""Minimal fake subtask runtime."""

from __future__ import annotations

from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from turing_research_plus.subtask.models import (
    SubtaskError,
    SubtaskErrorCode,
    SubtaskExecutionMode,
    SubtaskResult,
    SubtaskSpec,
    SubtaskStatus,
    TaskProfile,
)
from turing_research_plus.subtask.prompts import render_role_prompt
from turing_research_plus.subtask.quality import evaluate_quality_gate


class SubtaskRunner:
    """Run subtasks in single-window simulation modes."""

    def run(
        self,
        spec: SubtaskSpec,
        profile: TaskProfile,
        execution_mode: SubtaskExecutionMode | str = SubtaskExecutionMode.DRY_RUN,
    ) -> SubtaskResult:
        """Run a subtask without calling external LLMs or network services."""

        if execution_mode == SubtaskExecutionMode.LLM_CLIENT:
            raise ValueError("llm_client execution is not implemented in Round 5B")

        if execution_mode == SubtaskExecutionMode.MANUAL_CODEX_ROLE:
            result = self._manual_codex_role(spec, profile)
        elif execution_mode == SubtaskExecutionMode.DRY_RUN:
            result = self._dry_run(spec, profile)
        else:
            return SubtaskResult(
                subtask_id=spec.subtask_id,
                status=SubtaskStatus.FAILED,
                error=SubtaskError(
                    code=SubtaskErrorCode.UNSUPPORTED_EXECUTION_MODE,
                    message=f"unsupported execution mode: {execution_mode}",
                ),
            )

        if not evaluate_quality_gate(result, profile):
            return SubtaskResult(
                subtask_id=spec.subtask_id,
                status=SubtaskStatus.FAILED,
                artifacts=result.artifacts,
                message="quality gate failed",
                rendered_prompt=result.rendered_prompt,
                error=SubtaskError(
                    code=SubtaskErrorCode.QUALITY_GATE_FAILED,
                    message=f"quality gate failed: {profile.quality_gate}",
                ),
            )
        return result

    def _dry_run(self, spec: SubtaskSpec, profile: TaskProfile) -> SubtaskResult:
        artifact = ResearchArtifact(
            artifact_id=f"artifact-{spec.subtask_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title=f"Subtask output: {spec.title}",
            created_by=profile.role,
            content={
                "execution_mode": SubtaskExecutionMode.DRY_RUN,
                "inputs": spec.inputs,
                "profile_id": profile.profile_id,
            },
            evidence=[
                EvidenceRef(
                    source_id=f"subtask:{spec.subtask_id}",
                    locator="fake-service",
                    quote="Subtask executed in dry-run or fake-service mode.",
                    confidence=1.0,
                )
            ],
        )
        return SubtaskResult(
            subtask_id=spec.subtask_id,
            status=SubtaskStatus.COMPLETED,
            artifacts=[artifact],
            message="subtask completed",
        )

    def _manual_codex_role(self, spec: SubtaskSpec, profile: TaskProfile) -> SubtaskResult:
        rendered_prompt = render_role_prompt(spec, profile)
        artifact = ResearchArtifact(
            artifact_id=f"prompt-{spec.subtask_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title=f"Manual role prompt: {profile.name}",
            created_by="SubtaskRunner",
            content={"prompt": rendered_prompt},
            evidence=[
                EvidenceRef(
                    source_id=f"subtask:{spec.subtask_id}",
                    locator="manual_codex_role",
                    quote="Role prompt rendered for single-window Codex execution.",
                    confidence=1.0,
                )
            ],
        )
        return SubtaskResult(
            subtask_id=spec.subtask_id,
            status=SubtaskStatus.COMPLETED,
            artifacts=[artifact],
            message="manual role prompt rendered",
            rendered_prompt=rendered_prompt,
        )
