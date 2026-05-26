"""Proposed evidence update parsing for remote return verification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProposedEvidenceUpdate(BaseModel):
    """One proposed evidence update emitted by a return package."""

    model_config = ConfigDict(extra="forbid")

    update_id: str = Field(min_length=1)
    claim: str = Field(min_length=1)
    status: str = "proposed"
    evidence_refs: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_proposed_only(self) -> Self:
        if self.status == "observed":
            raise ValueError("return verifier cannot accept observed proposed updates")
        if not self.requires_human_review:
            raise ValueError("proposed evidence updates require human review")
        return self


class ProposedUpdateLoadReport(BaseModel):
    """Load report for proposed evidence updates."""

    model_config = ConfigDict(extra="forbid")

    updates: list[ProposedEvidenceUpdate] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    raw_count: int = 0
    auto_apply_evidence_updates: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether proposed update parsing blocks ingest review."""

        return bool(self.errors)


def load_proposed_updates(path: Path) -> ProposedUpdateLoadReport:
    """Load proposed evidence updates without applying them."""

    if not path.exists():
        return ProposedUpdateLoadReport(errors=["PROPOSED_EVIDENCE_UPDATES.json is missing"])
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report parse errors instead of crashing.
        return ProposedUpdateLoadReport(errors=[f"proposed update parse failed: {exc}"])

    items = _coerce_items(payload)
    updates: list[ProposedEvidenceUpdate] = []
    errors: list[str] = []
    for index, item in enumerate(items):
        try:
            updates.append(
                ProposedEvidenceUpdate(
                    update_id=str(item.get("update_id") or f"proposed-{index + 1}"),
                    claim=str(item.get("claim") or ""),
                    status=str(item.get("status") or "proposed"),
                    evidence_refs=[str(ref) for ref in item.get("evidence_refs", [])],
                    requires_human_review=bool(item.get("requires_human_review", True)),
                )
            )
        except Exception as exc:  # noqa: BLE001 - validation errors become blocker report.
            errors.append(f"unsafe proposed update {index + 1}: {exc}")
    return ProposedUpdateLoadReport(updates=updates, errors=errors, raw_count=len(items))


def _coerce_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("updates"), list):
        return [item for item in payload["updates"] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []
