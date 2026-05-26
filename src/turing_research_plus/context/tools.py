"""Thin context.* tool wrappers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tuling_research_plus.artifacts.models import ResearchArtifact
from tuling_research_plus.context.service import ContextService


def _service(root: str | Path) -> ContextService:
    return ContextService(root)


def context_init(root: str | Path, campaign_id: str, run_id: str) -> dict[str, Any]:
    return _service(root).init(campaign_id, run_id).model_dump(mode="json")


def context_checkpoint(
    root: str | Path,
    campaign_id: str,
    run_id: str,
    label: str,
    summary: str,
    artifacts: list[ResearchArtifact],
) -> dict[str, Any]:
    return _service(root).checkpoint(
        campaign_id=campaign_id,
        run_id=run_id,
        label=label,
        summary=summary,
        artifacts=artifacts,
    ).model_dump(mode="json")


def context_recover(root: str | Path, campaign_id: str, run_id: str) -> dict[str, Any]:
    return _service(root).recover(campaign_id, run_id).model_dump(mode="json")


def context_index(root: str | Path) -> dict[str, Any]:
    return _service(root).index().model_dump(mode="json")


def context_summarize(root: str | Path, campaign_id: str, run_id: str) -> dict[str, Any]:
    return _service(root).summarize(campaign_id, run_id).model_dump(mode="json")
