"""Safety checks for generated Session shell script equivalents."""

from __future__ import annotations

import re
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

DESTRUCTIVE_COMMAND_PATTERN = re.compile(
    r"^\s*(rm|rmdir|del|erase|format|mkfs|dd|shutdown|reboot|kill|pkill)\b"
)
REMOTE_EXECUTION_PATTERN = re.compile(r"\b(ssh|tmux|kubectl\s+exec|docker\s+exec)\b")
SECRET_PATTERN = re.compile(
    r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token|secret|password)\s*="
)
UNQUOTED_VARIABLE_PATTERN = re.compile(
    r"(?<!['\"])\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})(?!['\"])"
)


class ScriptSafetyStatus(StrEnum):
    """Safety result status."""

    PASS = "pass"
    BLOCKED = "blocked"


class ScriptSafetyFinding(BaseModel):
    """One script safety finding."""

    model_config = ConfigDict(extra="forbid")

    finding_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
    line_number: int | None = None
    line: str | None = None
    release_blocker: bool = False


class ScriptSafetyReport(BaseModel):
    """Review-only safety report for a generated shell script."""

    model_config = ConfigDict(extra="forbid")

    script_name: str = Field(min_length=1)
    status: ScriptSafetyStatus
    findings: list[ScriptSafetyFinding] = Field(default_factory=list)
    has_shellcheck_notes: bool = False
    has_manual_live_marker: bool = False
    contains_secrets: bool = False
    contains_destructive_commands: bool = False
    contains_remote_execution: bool = False
    contains_unquoted_variables: bool = False
    live_steps_commented: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_report_boundary(self) -> Self:
        if self.contains_secrets:
            raise ValueError("script safety report cannot allow secrets")
        if self.contains_destructive_commands:
            raise ValueError("script safety report cannot allow destructive commands")
        if self.contains_remote_execution:
            raise ValueError("script safety report cannot allow active remote execution")
        if self.contains_unquoted_variables:
            raise ValueError("script safety report cannot allow unquoted variables")
        if not self.live_steps_commented:
            raise ValueError("script safety report requires live steps to be commented")
        if not self.requires_human_review:
            raise ValueError("script safety report requires human review")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether this script blocks export review."""

        return self.status == ScriptSafetyStatus.BLOCKED or any(
            finding.release_blocker for finding in self.findings
        )


def audit_shell_script(script_name: str, content: str) -> ScriptSafetyReport:
    """Audit generated shell script text without executing it."""

    findings: list[ScriptSafetyFinding] = []
    has_shellcheck_notes = "shellcheck" in content.lower()
    has_manual_live_marker = "MANUAL LIVE STEP" in content
    live_steps_commented = True

    for index, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        is_comment = stripped.startswith("#")
        if not is_comment and DESTRUCTIVE_COMMAND_PATTERN.search(line):
            findings.append(_finding("destructive-command", "destructive command", index, line))
        if not is_comment and REMOTE_EXECUTION_PATTERN.search(line):
            findings.append(_finding("remote-execution", "remote execution command", index, line))
        if SECRET_PATTERN.search(line):
            findings.append(_finding("secret-assignment", "secret-like assignment", index, line))
        if not is_comment and _has_unquoted_variable(line):
            findings.append(_finding("unquoted-variable", "unquoted shell variable", index, line))
        if _mentions_live_step(line) and not (
            is_comment and "MANUAL LIVE STEP" in line and "disabled" in line.lower()
        ):
            live_steps_commented = False
            findings.append(
                _finding(
                    "active-live-step",
                    "live step is not commented/manual",
                    index,
                    line,
                )
            )

    blocked = any(finding.release_blocker for finding in findings)
    return ScriptSafetyReport(
        script_name=script_name,
        status=ScriptSafetyStatus.BLOCKED if blocked else ScriptSafetyStatus.PASS,
        findings=findings,
        has_shellcheck_notes=has_shellcheck_notes,
        has_manual_live_marker=has_manual_live_marker,
        contains_secrets=any(item.finding_id == "secret-assignment" for item in findings),
        contains_destructive_commands=any(
            item.finding_id == "destructive-command" for item in findings
        ),
        contains_remote_execution=any(item.finding_id == "remote-execution" for item in findings),
        contains_unquoted_variables=any(
            item.finding_id == "unquoted-variable" for item in findings
        ),
        live_steps_commented=live_steps_commented,
        requires_human_review=True,
    )


def render_script_safety_report(report: ScriptSafetyReport) -> str:
    """Render script safety report Markdown."""

    lines = [
        f"# Script Safety Report: {report.script_name}",
        "",
        f"- Status: `{report.status}`",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        f"- Shellcheck-style notes: `{str(report.has_shellcheck_notes).lower()}`",
        f"- Manual live marker: `{str(report.has_manual_live_marker).lower()}`",
        "- Contains secrets: `false`",
        "- Contains destructive commands: `false`",
        "- Contains active remote execution: `false`",
        "- Contains unquoted variables: `false`",
        f"- Live steps commented: `{str(report.live_steps_commented).lower()}`",
        "- Requires human review: `true`",
        "",
        "## Findings",
        "",
    ]
    lines.extend(
        [
            f"- `{finding.finding_id}` line `{finding.line_number}`: {finding.message}"
            for finding in report.findings
        ]
        or ["- None."]
    )
    return "\n".join(lines) + "\n"


def _finding(
    finding_id: str,
    message: str,
    line_number: int,
    line: str,
) -> ScriptSafetyFinding:
    return ScriptSafetyFinding(
        finding_id=finding_id,
        message=message,
        line_number=line_number,
        line=line,
        release_blocker=True,
    )


def _has_unquoted_variable(line: str) -> bool:
    # Ignore command substitution and quoted variables; this is intentionally conservative
    # for generated scripts rather than a general shell parser.
    return bool(UNQUOTED_VARIABLE_PATTERN.search(line.replace("$(", "")))


def _mentions_live_step(line: str) -> bool:
    lowered = line.lower()
    return any(token in lowered for token in ["live ssh", "live sftp", "manual live", " sftp "])
