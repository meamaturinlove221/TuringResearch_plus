"""Export safe shell script equivalents for Session runtime parity."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.session_runtime.script_safety import (
    ScriptSafetyReport,
    audit_shell_script,
    render_script_safety_report,
)
from turing_research_plus.session_runtime.sop_export import render_session_script_sop

SCRIPT_ORDER = [
    "preflight.sh",
    "build-context-pack.sh",
    "fake-transfer.sh",
    "verify-return.sh",
    "workflow-replay.sh",
]


class SessionScriptExportStatus(StrEnum):
    """Status for script export reports."""

    EXPORTED = "exported"
    BLOCKED = "blocked"


class SessionScriptSpec(BaseModel):
    """One generated script specification."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    content: str = Field(min_length=1)
    safety: ScriptSafetyReport


class SessionScriptExportRequest(BaseModel):
    """Request to export review-only Session shell equivalents."""

    model_config = ConfigDict(extra="forbid")

    output_dir: Path
    project_root: str = "examples/session_runtime/preflight_fixture"
    preflight_context_source: str = "context"
    preflight_output_dir: str = "output"
    context_pack_source_dir: str = "examples/session_runtime/context_pack_fixture/source"
    context_pack_output_dir: str = "tmp/session-script-context-pack"
    fake_transfer_target_dir: str = "tmp/session-script-fake-transfer"
    return_fixture_dir: str = "examples/session_runtime/return_fixture"
    replay_workspace: str = "tmp/session-script-replay"
    shell: str = "bash"
    remote_execution_enabled: bool = False
    live_ssh_enabled: bool = False
    automatic_evidence_ledger_write: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_export_boundary(self) -> Self:
        if self.remote_execution_enabled:
            raise ValueError("script export cannot enable remote execution")
        if self.live_ssh_enabled:
            raise ValueError("script export cannot enable live SSH")
        if self.automatic_evidence_ledger_write:
            raise ValueError("script export cannot auto-write Evidence Ledger")
        if not self.requires_human_review:
            raise ValueError("script export requires human review")
        return self


class SessionScriptExportReport(BaseModel):
    """Review-only report for exported shell equivalents."""

    model_config = ConfigDict(extra="forbid")

    status: SessionScriptExportStatus
    output_dir: str = Field(min_length=1)
    scripts: list[SessionScriptSpec] = Field(default_factory=list)
    sop_path: str | None = None
    remote_execution_enabled: bool = False
    live_ssh_enabled: bool = False
    automatic_evidence_ledger_write: bool = False
    scripts_executed: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_report_boundary(self) -> Self:
        if self.remote_execution_enabled:
            raise ValueError("script export report cannot enable remote execution")
        if self.live_ssh_enabled:
            raise ValueError("script export report cannot enable live SSH")
        if self.automatic_evidence_ledger_write:
            raise ValueError("script export report cannot auto-write Evidence Ledger")
        if self.scripts_executed:
            raise ValueError("script export report cannot execute scripts")
        if not self.requires_human_review:
            raise ValueError("script export report requires human review")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether any exported script blocks review."""

        return any(script.safety.release_blocker for script in self.scripts)


def build_session_script_specs(request: SessionScriptExportRequest) -> list[SessionScriptSpec]:
    """Build script specs and audit them without writing files."""

    builders = [
        ("preflight.sh", "run local session preflight", _preflight_script),
        ("build-context-pack.sh", "build safe local context pack", _pack_script),
        ("fake-transfer.sh", "copy context pack to local fake target", _fake_transfer_script),
        ("verify-return.sh", "verify structured fake return package", _verify_return_script),
        ("workflow-replay.sh", "run full fake pod workflow replay", _workflow_replay_script),
    ]
    specs: list[SessionScriptSpec] = []
    for name, purpose, builder in builders:
        content = builder(request)
        specs.append(
            SessionScriptSpec(
                name=name,
                purpose=purpose,
                content=content,
                safety=audit_shell_script(name, content),
            )
        )
    return specs


def export_session_scripts(request: SessionScriptExportRequest) -> SessionScriptExportReport:
    """Write safe shell script equivalents and SOP files without executing scripts."""

    specs = build_session_script_specs(request)
    request.output_dir.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        script_path = request.output_dir / spec.name
        script_path.write_text(spec.content, encoding="utf-8", newline="\n")
        safety_path = request.output_dir / f"{spec.name}.safety.md"
        safety_path.write_text(render_script_safety_report(spec.safety), encoding="utf-8")

    sop = render_session_script_sop(
        script_names=[spec.name for spec in specs],
        safety_reports=[spec.safety for spec in specs],
    )
    sop_path = request.output_dir / "SESSION_SCRIPT_SOP.md"
    sop_path.write_text(sop, encoding="utf-8")
    return SessionScriptExportReport(
        status=SessionScriptExportStatus.BLOCKED
        if any(spec.safety.release_blocker for spec in specs)
        else SessionScriptExportStatus.EXPORTED,
        output_dir=request.output_dir.as_posix(),
        scripts=specs,
        sop_path=sop_path.as_posix(),
        remote_execution_enabled=False,
        live_ssh_enabled=False,
        automatic_evidence_ledger_write=False,
        scripts_executed=False,
        requires_human_review=True,
    )


def render_session_script_export_report(report: SessionScriptExportReport) -> str:
    """Render the export report for human review."""

    lines = [
        "# Session Script Export Report",
        "",
        f"- Status: `{report.status}`",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        f"- Output dir: `{report.output_dir}`",
        "- Remote execution enabled: `false`",
        "- Live SSH enabled: `false`",
        "- Automatic Evidence Ledger write: `false`",
        "- Scripts executed during export: `false`",
        "- Requires human review: `true`",
        "",
        "## Scripts",
        "",
    ]
    lines.extend(
        [
            f"- `{script.name}`: {script.purpose}; safety `{script.safety.status}`"
            for script in report.scripts
        ]
    )
    lines.extend(["", "## SOP", "", f"- `{report.sop_path}`"])
    return "\n".join(lines) + "\n"


def _header(title: str) -> list[str]:
    return [
        "#!/usr/bin/env bash",
        "# shellcheck shell=bash",
        f"# {title}",
        "# Generated by TuringResearch Session script exporter.",
        "# Review before manual execution.",
        "# Safety: fake/dry-run default; no secrets; no destructive commands.",
        "# Safety: no remote execution by default; no automatic Evidence Ledger write.",
        "# MANUAL LIVE STEP (disabled): live SSH/SFTP requires explicit human review.",
        "set -euo pipefail",
        "",
    ]


def _readonly(name: str, value: str) -> str:
    escaped = value.replace('"', '\\"')
    return f"readonly {name}=\"{escaped}\""


def _preflight_script(request: SessionScriptExportRequest) -> str:
    lines = _header("preflight.sh - local Session preflight")
    lines.extend(
        [
            _readonly("PROJECT_ROOT", request.project_root),
            _readonly("CONTEXT_SOURCE", request.preflight_context_source),
            _readonly("PREFLIGHT_OUTPUT_DIR", request.preflight_output_dir),
            _readonly("REPORT_PATH", "tmp/session-script-preflight.md"),
            "",
            'python -m turing_research_plus.session_runtime.cli session preflight \\',
            '  --project-root "${PROJECT_ROOT}" \\',
            '  --context-source "${CONTEXT_SOURCE}" \\',
            '  --output-dir "${PREFLIGHT_OUTPUT_DIR}" \\',
            '  --output "${REPORT_PATH}"',
            "",
        ]
    )
    return "\n".join(lines)


def _pack_script(request: SessionScriptExportRequest) -> str:
    lines = _header("build-context-pack.sh - safe local context pack")
    lines.extend(
        [
            _readonly("SOURCE_DIR", request.context_pack_source_dir),
            _readonly("OUTPUT_DIR", request.context_pack_output_dir),
            _readonly("REPORT_PATH", "tmp/session-script-pack.md"),
            "",
            'python -m turing_research_plus.session_runtime.cli session pack \\',
            '  --source-dir "${SOURCE_DIR}" \\',
            '  --output-dir "${OUTPUT_DIR}" \\',
            '  --output "${REPORT_PATH}"',
            "",
        ]
    )
    return "\n".join(lines)


def _fake_transfer_script(request: SessionScriptExportRequest) -> str:
    lines = _header("fake-transfer.sh - local fake transfer")
    lines.extend(
        [
            _readonly("SOURCE_DIR", request.context_pack_output_dir),
            _readonly("TARGET_DIR", request.fake_transfer_target_dir),
            _readonly("REPORT_PATH", "tmp/session-script-transfer.md"),
            "",
            'python -m turing_research_plus.session_runtime.cli session transfer --fake \\',
            '  --source-dir "${SOURCE_DIR}" \\',
            '  --target-dir "${TARGET_DIR}" \\',
            '  --output "${REPORT_PATH}"',
            "",
        ]
    )
    return "\n".join(lines)


def _verify_return_script(request: SessionScriptExportRequest) -> str:
    lines = _header("verify-return.sh - structured return verifier")
    lines.extend(
        [
            _readonly("RETURN_DIR", request.return_fixture_dir),
            _readonly("REPORT_PATH", "tmp/session-script-return.md"),
            "",
            'python -m turing_research_plus.session_runtime.cli session verify-return \\',
            '  --return-dir "${RETURN_DIR}" \\',
            '  --output "${REPORT_PATH}"',
            "",
        ]
    )
    return "\n".join(lines)


def _workflow_replay_script(request: SessionScriptExportRequest) -> str:
    lines = _header("workflow-replay.sh - full fake workflow replay")
    lines.extend(
        [
            _readonly("PROJECT_ROOT", request.project_root),
            _readonly("PREFLIGHT_CONTEXT_SOURCE", request.preflight_context_source),
            _readonly("PREFLIGHT_OUTPUT_DIR", request.preflight_output_dir),
            _readonly("CONTEXT_PACK_SOURCE_DIR", request.context_pack_source_dir),
            _readonly("REPLAY_WORKSPACE", request.replay_workspace),
            _readonly("FAKE_RETURN_FIXTURE_DIR", request.return_fixture_dir),
            _readonly("REPORT_PATH", "tmp/session-script-replay.md"),
            "",
            'python -m turing_research_plus.session_runtime.cli session replay \\',
            '  --project-root "${PROJECT_ROOT}" \\',
            '  --preflight-context-source "${PREFLIGHT_CONTEXT_SOURCE}" \\',
            '  --preflight-output-dir "${PREFLIGHT_OUTPUT_DIR}" \\',
            '  --context-pack-source-dir "${CONTEXT_PACK_SOURCE_DIR}" \\',
            '  --replay-workspace "${REPLAY_WORKSPACE}" \\',
            '  --fake-return-fixture-dir "${FAKE_RETURN_FIXTURE_DIR}" \\',
            '  --output "${REPORT_PATH}"',
            "",
        ]
    )
    return "\n".join(lines)
