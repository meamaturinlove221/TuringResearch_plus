"""Report helpers for the local Session CLI surface."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SessionCLIStatus(StrEnum):
    """Status labels for CLI command execution."""

    PASS = "pass"
    PASS_WITH_WARNINGS = "pass-with-warnings"
    BLOCKED = "blocked"


class SessionCLICommandReport(BaseModel):
    """Review-only report for a Session CLI command."""

    model_config = ConfigDict(extra="forbid")

    command: str = Field(min_length=1)
    status: SessionCLIStatus
    summary: str = Field(min_length=1)
    output_path: str | None = None
    detail_markdown: str = Field(default="")
    data: dict[str, Any] = Field(default_factory=dict)
    live_ssh_enabled: bool = False
    live_network_enabled: bool = False
    remote_command_execution: bool = False
    secrets_logged: bool = False
    automatic_evidence_ledger_write: bool = False
    proposed_updates_only: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_cli_boundaries(self) -> Self:
        if self.live_ssh_enabled:
            raise ValueError("Session CLI cannot enable live SSH by default")
        if self.live_network_enabled:
            raise ValueError("Session CLI cannot enable live networking by default")
        if self.remote_command_execution:
            raise ValueError("Session CLI cannot execute remote commands")
        if self.secrets_logged:
            raise ValueError("Session CLI reports cannot log secrets")
        if self.automatic_evidence_ledger_write:
            raise ValueError("Session CLI cannot auto-write Evidence Ledger entries")
        if not self.proposed_updates_only:
            raise ValueError("Session CLI must keep evidence updates proposed-only")
        if not self.requires_human_review:
            raise ValueError("Session CLI requires human review")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether this CLI command blocks review."""

        return self.status == SessionCLIStatus.BLOCKED


def render_session_cli_command_report(report: SessionCLICommandReport) -> str:
    """Render a deterministic CLI command report."""

    lines = [
        f"# Session CLI Report: {report.command}",
        "",
        f"- Status: `{report.status}`",
        f"- Summary: {report.summary}",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        "- Live SSH enabled: `false`",
        "- Live network enabled: `false`",
        "- Remote command execution: `false`",
        "- Secrets logged: `false`",
        "- Automatic Evidence Ledger write: `false`",
        "- Proposed updates only: `true`",
        "- Requires human review: `true`",
    ]
    if report.output_path:
        lines.append(f"- Output path: `{report.output_path}`")
    if report.data:
        lines.extend(["", "## Data", ""])
        for key, value in sorted(report.data.items()):
            lines.append(f"- `{key}`: `{value}`")
    if report.detail_markdown.strip():
        lines.extend(["", "## Detail", "", report.detail_markdown.strip()])
    return "\n".join(lines) + "\n"


def build_session_cli_surface_report() -> SessionCLICommandReport:
    """Return the static review report for available Session CLI commands."""

    commands = [
        "session preflight",
        "session pack",
        "session transfer --fake",
        "session verify-return",
        "session replay",
        "session report",
    ]
    detail = "\n".join(
        [
            "# Session CLI Surface",
            "",
            "## Commands",
            "",
            *[f"- `{command}`" for command in commands],
            "",
            "## Safety Boundaries",
            "",
            "- fake/dry-run defaults;",
            "- live SSH disabled by default;",
            "- no remote command execution;",
            "- no secrets logging;",
            "- no automatic Evidence Ledger write;",
            "- proposed updates require human review.",
        ]
    )
    return SessionCLICommandReport(
        command="session report",
        status=SessionCLIStatus.PASS,
        summary="Session CLI surface is available in fake/dry-run mode.",
        detail_markdown=detail,
        data={
            "command_count": len(commands),
            "entrypoint": "turing_research_plus.session_runtime.cli:main",
        },
    )


def write_cli_report_if_requested(
    report: SessionCLICommandReport,
    output_path: Path | None,
) -> SessionCLICommandReport:
    """Write report Markdown when requested and return an updated report."""

    if output_path is None:
        return report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = render_session_cli_command_report(report)
    output_path.write_text(text, encoding="utf-8")
    return report.model_copy(update={"output_path": output_path.as_posix()})
