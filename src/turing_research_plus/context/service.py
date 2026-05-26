"""Context management service."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from turing_research_plus.artifacts.models import ResearchArtifact
from turing_research_plus.context.index import load_index, upsert_index_entry
from turing_research_plus.context.models import (
    ContextCheckpoint,
    ContextIndex,
    ContextIndexEntry,
    ContextRecoverResult,
    ContextSession,
    ContextSummary,
)


class ContextService:
    """Local context service with recoverable checkpoints."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def init(
        self,
        campaign_id: str,
        run_id: str,
        metadata: dict[str, object] | None = None,
    ) -> ContextSession:
        """Create one context file for a campaign run."""

        path = self._context_path(campaign_id, run_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("", encoding="utf-8")
        session = ContextSession(
            campaign_id=campaign_id,
            run_id=run_id,
            context_path=path,
            metadata=dict(metadata or {}),
        )
        upsert_index_entry(
            self.root,
            ContextIndexEntry(campaign_id=campaign_id, run_id=run_id, context_path=path),
        )
        return session

    def checkpoint(
        self,
        campaign_id: str,
        run_id: str,
        label: str,
        summary: str,
        artifacts: list[ResearchArtifact],
        state: dict[str, object] | None = None,
    ) -> ContextCheckpoint:
        """Append a recoverable checkpoint."""

        if not artifacts:
            raise ValueError("checkpoint requires linked artifacts")
        evidence = [evidence for artifact in artifacts for evidence in artifact.evidence]
        if not evidence:
            raise ValueError("checkpoint requires linked evidence refs")

        session = self.init(campaign_id, run_id)
        checkpoint = ContextCheckpoint(
            checkpoint_id=f"checkpoint-{uuid4()}",
            campaign_id=campaign_id,
            run_id=run_id,
            label=label,
            summary=summary,
            artifacts=artifacts,
            evidence=evidence,
            state=dict(state or {}),
        )
        with session.context_path.open("a", encoding="utf-8") as handle:
            handle.write(checkpoint.model_dump_json() + "\n")
        upsert_index_entry(
            self.root,
            ContextIndexEntry(
                campaign_id=campaign_id,
                run_id=run_id,
                context_path=session.context_path,
                latest_checkpoint_id=checkpoint.checkpoint_id,
                latest_summary=checkpoint.summary,
                artifact_ids=[artifact.artifact_id for artifact in artifacts],
            ),
        )
        return checkpoint

    def index(self) -> ContextIndex:
        """Return the context index."""

        return load_index(self.root)

    def recover(self, campaign_id: str, run_id: str) -> ContextRecoverResult:
        """Recover the latest checkpoint state."""

        checkpoints = self._read_checkpoints(campaign_id, run_id)
        if not checkpoints:
            return ContextRecoverResult(
                campaign_id=campaign_id,
                run_id=run_id,
                latest_summary="No checkpoints found.",
            )
        latest = checkpoints[-1]
        return ContextRecoverResult(
            campaign_id=campaign_id,
            run_id=run_id,
            latest_summary=latest.summary,
            artifacts=latest.artifacts,
            evidence=latest.evidence,
            checkpoint=latest,
        )

    def summarize(self, campaign_id: str, run_id: str) -> ContextSummary:
        """Summarize a context file without calling an LLM."""

        checkpoints = self._read_checkpoints(campaign_id, run_id)
        latest = checkpoints[-1] if checkpoints else None
        artifact_ids: list[str] = []
        for checkpoint in checkpoints:
            artifact_ids.extend(artifact.artifact_id for artifact in checkpoint.artifacts)
        return ContextSummary(
            campaign_id=campaign_id,
            run_id=run_id,
            checkpoint_count=len(checkpoints),
            latest_summary=latest.summary if latest is not None else None,
            artifact_ids=artifact_ids,
        )

    def _context_path(self, campaign_id: str, run_id: str) -> Path:
        return self.root / f"{campaign_id}__{run_id}.jsonl"

    def _read_checkpoints(self, campaign_id: str, run_id: str) -> list[ContextCheckpoint]:
        path = self._context_path(campaign_id, run_id)
        if not path.exists():
            return []
        checkpoints: list[ContextCheckpoint] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            checkpoints.append(ContextCheckpoint.model_validate(json.loads(line)))
        return checkpoints
