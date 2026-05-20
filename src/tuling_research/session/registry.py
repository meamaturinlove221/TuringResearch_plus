"""Local session registry."""

from __future__ import annotations

import json
from pathlib import Path

from tuling_research.session.models import SessionInfo, SessionListResult


class SessionRegistry:
    """Read-only local session registry."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def list_sessions(self) -> SessionListResult:
        """Return registered sessions, or an empty list if no registry exists."""

        if not self.path.exists():
            return SessionListResult()
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            sessions = raw.get("sessions", [])
        else:
            sessions = raw
        return SessionListResult(
            sessions=[SessionInfo.model_validate(session) for session in sessions]
        )
