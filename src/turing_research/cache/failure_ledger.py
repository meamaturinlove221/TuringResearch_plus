"""Failure ledger for retryable cache and adapter failures."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FailureRecord(BaseModel):
    """One failure entry with optional retry scheduling."""

    model_config = ConfigDict(extra="forbid")

    failure_id: str = Field(min_length=1)
    key: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    retry_after: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(default_factory=dict)

    def is_retry_allowed(self, now: datetime | None = None) -> bool:
        """Return whether retry is allowed at the given time."""

        if self.retry_after is None:
            return True
        current = now or datetime.now(UTC)
        return current >= self.retry_after


class FailureLedger:
    """JSON-backed append-only failure ledger."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def list_records(self) -> list[FailureRecord]:
        """Return all recorded failures."""

        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [FailureRecord.model_validate(item) for item in raw]

    def append(self, record: FailureRecord) -> FailureRecord:
        """Append a failure record."""

        records = self.list_records()
        records.append(record)
        self.path.write_text(
            json.dumps(
                [record.model_dump(mode="json") for record in records],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return record

    def retryable(self, now: datetime | None = None) -> list[FailureRecord]:
        """Return records whose retry_after has passed."""

        return [record for record in self.list_records() if record.is_retry_allowed(now)]
