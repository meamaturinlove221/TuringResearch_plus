"""Campaign runtime for Strategy -> Tactic -> SOP execution."""

from __future__ import annotations

from collections.abc import Callable
from uuid import uuid4

from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from turing_research_plus.campaign.models import (
    CampaignResult,
    CampaignRun,
    CampaignSpec,
    SOPExecutionMode,
    SOPSpec,
    StrategySpec,
    WorkflowStatus,
)
from turing_research_plus.campaign.router import CampaignRouter
from turing_research_plus.ledger.models import LedgerEvent, LedgerEventType, StateLedger
from turing_research_plus.subtask.models import SubtaskSpec, TaskProfile
from turing_research_plus.subtask.runner import SubtaskRunner

SOPHandler = Callable[[SOPSpec, CampaignRun], list[ResearchArtifact]]
QualityGate = Callable[[CampaignRun], bool]
CheckpointHook = Callable[[CampaignRun], None]


class CampaignRunner:
    """Run abstract TuringResearch Plus campaigns."""

    def __init__(
        self,
        router: CampaignRouter | None = None,
        subtask_runner: SubtaskRunner | None = None,
        checkpoint_hook: CheckpointHook | None = None,
    ) -> None:
        self.router = router or CampaignRouter()
        self.subtask_runner = subtask_runner or SubtaskRunner()
        self.checkpoint_hook = checkpoint_hook
        self.handlers: dict[str, SOPHandler] = {"default": self._default_handler}

    def register_handler(self, name: str, handler: SOPHandler) -> None:
        """Register a direct/imported SOP handler."""

        self.handlers[name] = handler

    def run(
        self,
        spec: CampaignSpec,
        quality_gates: dict[str, QualityGate] | None = None,
    ) -> CampaignResult:
        """Run a campaign with a selected strategy."""

        ledger = StateLedger(ledger_id=spec.state_ledger.ledger_id, lane=spec.state_ledger.lane)
        run = CampaignRun(
            run_id=f"run-{uuid4()}",
            campaign_id=spec.campaign_id,
            status=WorkflowStatus.RUNNING,
            ledger=ledger,
        )
        self._append_event(run, LedgerEventType.CREATED, "Campaign run initialized.")

        strategy = self.router.select_strategy(spec)
        run.selected_strategy_id = strategy.strategy_id
        self._append_event(
            run,
            LedgerEventType.UPDATED,
            f"Selected strategy: {strategy.strategy_id}",
        )

        if spec.budget_gate.is_blocked:
            return self._blocked_result(spec, run, "BudgetGate is blocked")

        if not spec.budget_gate.meets_minimum_ratio and not spec.budget_gate.deviation_reason:
            return self._blocked_result(spec, run, "BudgetGate minimum ratio not met")

        if not spec.budget_gate.meets_minimum_ratio and spec.budget_gate.deviation_reason:
            self._append_event(
                run,
                LedgerEventType.UPDATED,
                f"Budget deviation accepted: {spec.budget_gate.deviation_reason}",
            )

        self._execute_strategy(strategy, run)

        quality_results = self._run_quality_gates(spec, run, quality_gates or {})
        if not all(quality_results.values()):
            return self._blocked_result(spec, run, "Quality gate failed", quality_results)

        run.status = WorkflowStatus.COMPLETED
        self._append_event(run, LedgerEventType.COMPLETED, "Campaign run completed.")
        if self.checkpoint_hook is not None:
            self.checkpoint_hook(run)

        return CampaignResult(
            campaign_id=spec.campaign_id,
            run_id=run.run_id,
            status=WorkflowStatus.COMPLETED,
            selected_strategy_id=run.selected_strategy_id,
            artifacts=run.artifacts,
            ledger=run.ledger,
            quality_gate_results=quality_results,
        )

    def _execute_strategy(self, strategy: StrategySpec, run: CampaignRun) -> None:
        for tactic in strategy.tactics:
            self._append_event(
                run,
                LedgerEventType.UPDATED,
                f"Executing tactic: {tactic.tactic_id}",
            )
            for sop in tactic.sops:
                artifacts = self._execute_sop(sop, run)
                for artifact in artifacts:
                    run.artifacts.append(artifact)
                    run.ledger.append_artifact(artifact)
                    self._append_event(
                        run,
                        LedgerEventType.ARTIFACT,
                        f"Collected artifact: {artifact.artifact_id}",
                    )

    def _execute_sop(self, sop: SOPSpec, run: CampaignRun) -> list[ResearchArtifact]:
        if sop.execution_mode == SOPExecutionMode.SUBTASK:
            subtask = SubtaskSpec(
                subtask_id=sop.sop_id,
                title=sop.title,
                inputs=sop.inputs,
            )
            profile = TaskProfile(
                name=f"profile-{sop.sop_id}",
                role="turingresearch-subtask",
                goal=f"Execute SOP {sop.sop_id} in fake-service mode.",
                input_schema={"type": "object"},
                output_schema={"type": "object"},
                dry_run=True,
            )
            return self.subtask_runner.run(subtask, profile).artifacts

        handler = self.handlers.get(sop.handler, self._default_handler)
        return handler(sop, run)

    def _run_quality_gates(
        self,
        spec: CampaignSpec,
        run: CampaignRun,
        gates: dict[str, QualityGate],
    ) -> dict[str, bool]:
        results: dict[str, bool] = {}
        for gate in spec.quality_gates:
            check = gates.get(gate.gate_id)
            passed = check(run) if check is not None else bool(run.artifacts)
            results[gate.gate_id] = passed
            self._append_event(
                run,
                LedgerEventType.UPDATED,
                f"Quality gate {gate.gate_id}: {'passed' if passed else 'failed'}",
            )
        return results

    def _blocked_result(
        self,
        spec: CampaignSpec,
        run: CampaignRun,
        reason: str,
        quality_results: dict[str, bool] | None = None,
    ) -> CampaignResult:
        run.status = WorkflowStatus.BLOCKED
        blocker = LedgerEvent(
            event_id=f"event-{uuid4()}",
            event_type=LedgerEventType.BLOCKED,
            message=reason,
        )
        run.ledger.append_blocker(blocker)
        if self.checkpoint_hook is not None:
            self.checkpoint_hook(run)
        return CampaignResult(
            campaign_id=spec.campaign_id,
            run_id=run.run_id,
            status=WorkflowStatus.BLOCKED,
            selected_strategy_id=run.selected_strategy_id,
            artifacts=run.artifacts,
            ledger=run.ledger,
            quality_gate_results=quality_results or {},
            blocked_reason=reason,
        )

    def _append_event(
        self,
        run: CampaignRun,
        event_type: LedgerEventType,
        message: str,
    ) -> None:
        event = LedgerEvent(
            event_id=f"event-{uuid4()}",
            event_type=event_type,
            message=message,
        )
        run.events.append(event)
        run.ledger.append_event(event)

    def _default_handler(self, sop: SOPSpec, run: CampaignRun) -> list[ResearchArtifact]:
        return [
            ResearchArtifact(
                artifact_id=f"artifact-{run.campaign_id}-{sop.sop_id}",
                kind=ArtifactKind.WORKFLOW_STATE,
                title=f"SOP output: {sop.title}",
                created_by="CampaignRunner",
                content={"sop_id": sop.sop_id, "execution_mode": sop.execution_mode},
                evidence=[
                    EvidenceRef(
                        source_id=f"sop:{sop.sop_id}",
                        locator="fake-service",
                        quote="SOP executed by the abstract campaign runtime.",
                        confidence=1.0,
                    )
                ],
            )
        ]
