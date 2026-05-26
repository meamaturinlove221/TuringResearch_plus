"""Quality gate for Advisor export artifacts."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.advisor_export.export_audit import (
    ExportAuditFinding,
    ExportAuditSeverity,
    ExportFileAudit,
    audit_export_outputs,
)


class ExportQualityStatus(StrEnum):
    """Overall export quality gate status."""

    PASS = "pass"
    PASS_WITH_WARNINGS = "pass-with-warnings"
    FAIL = "fail"


class ExportQualityGateRequest(BaseModel):
    """Input paths for export quality checks."""

    model_config = ConfigDict(extra="forbid")

    advisor_export_dir: Path
    dashboard_paths: list[Path] = Field(default_factory=list)
    required_outputs: list[str] = Field(default_factory=list)


class ExportQualityReport(BaseModel):
    """Quality report for Advisor and dashboard exports."""

    model_config = ConfigDict(extra="forbid")

    status: ExportQualityStatus
    checked_paths: list[str]
    file_audits: list[ExportFileAudit]
    findings: list[ExportAuditFinding]
    skipped_outputs: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


DEFAULT_REQUIRED_OUTPUTS = [
    "advisor_report_source.md",
    "evidence_refs.md",
    "limitations.md",
    "next_actions.md",
    "pdf_export/pdf_export_report.md",
    "pdf_export/advisor_pdf_review_source.md",
    "pptx_export/pptx_export_report.md",
    "pptx_export/advisor_pptx_review_source.md",
]


def run_export_quality_gate(request: ExportQualityGateRequest) -> ExportQualityReport:
    """Run local export quality checks over Advisor and dashboard outputs."""

    required = request.required_outputs or DEFAULT_REQUIRED_OUTPUTS
    advisor_paths = [request.advisor_export_dir / item for item in required]
    all_paths = [*advisor_paths, *request.dashboard_paths]

    audits = audit_export_outputs(all_paths, require_limitations=False)
    findings = [finding for audit in audits for finding in audit.findings]
    findings.extend(_check_evidence_refs(request.advisor_export_dir))
    findings.extend(_check_limitations(request.advisor_export_dir))

    skipped_outputs = [
        audit.path for audit in audits if audit.skipped and audit.skipped_reason is not None
    ]
    errors = [item for item in findings if item.severity == ExportAuditSeverity.ERROR]
    warnings = [item for item in findings if item.severity == ExportAuditSeverity.WARNING]
    status = ExportQualityStatus.PASS
    if errors:
        status = ExportQualityStatus.FAIL
    elif warnings or skipped_outputs:
        status = ExportQualityStatus.PASS_WITH_WARNINGS

    return ExportQualityReport(
        status=status,
        checked_paths=[str(path) for path in all_paths],
        file_audits=audits,
        findings=findings,
        skipped_outputs=skipped_outputs,
    )


def render_export_quality_report(report: ExportQualityReport) -> str:
    """Render an export quality report as Markdown."""

    lines = [
        "# Export Quality Report",
        "",
        f"- status: {report.status.value}",
        "- requires_human_review: true",
        "",
        "## Checked Paths",
        "",
    ]
    lines.extend([f"- `{Path(path).as_posix()}`" for path in report.checked_paths])
    lines.extend(["", "## Skipped Outputs", ""])
    if report.skipped_outputs:
        lines.extend([f"- `{Path(path).as_posix()}`" for path in report.skipped_outputs])
    else:
        lines.append("- none")
    lines.extend(["", "## Findings", ""])
    if report.findings:
        lines.extend(
            [
                f"- `{finding.severity.value}` `{finding.check_id}`: {finding.message}"
                for finding in report.findings
            ]
        )
    else:
        lines.append("- none")
    lines.extend(["", "## File Audits", ""])
    for audit in report.file_audits:
        status = "exists" if audit.exists else "missing"
        if audit.skipped:
            status = f"skipped ({audit.skipped_reason})"
        lines.append(f"- `{Path(audit.path).as_posix()}`: {status}")
    lines.append("")
    return "\n".join(lines)


def _check_evidence_refs(advisor_export_dir: Path) -> list[ExportAuditFinding]:
    path = advisor_export_dir / "evidence_refs.md"
    if not path.exists():
        return [
            ExportAuditFinding(
                check_id="missing-evidence-refs",
                severity=ExportAuditSeverity.ERROR,
                message="Evidence refs file is missing.",
                path=str(path),
            )
        ]
    text = path.read_text(encoding="utf-8").lower()
    if "evidence" in text and "human review" in text:
        return []
    return [
        ExportAuditFinding(
            check_id="weak-evidence-refs",
            severity=ExportAuditSeverity.ERROR,
            message="Evidence refs are missing evidence and human-review markers.",
            path=str(path),
        )
    ]


def _check_limitations(advisor_export_dir: Path) -> list[ExportAuditFinding]:
    path = advisor_export_dir / "limitations.md"
    if not path.exists():
        return [
            ExportAuditFinding(
                check_id="missing-limitations",
                severity=ExportAuditSeverity.ERROR,
                message="Limitations file is missing.",
                path=str(path),
            )
        ]
    text = path.read_text(encoding="utf-8").lower()
    if "human review" in text and "does not" in text:
        return []
    return [
        ExportAuditFinding(
            check_id="weak-limitations",
            severity=ExportAuditSeverity.ERROR,
            message="Limitations must preserve human-review and no-overclaim markers.",
            path=str(path),
        )
    ]
