"""Audit helpers for advisor export outputs."""

from __future__ import annotations

import re
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class ExportAuditSeverity(StrEnum):
    """Severity levels for export audit findings."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ExportAuditFinding(BaseModel):
    """One quality or safety finding for an exported artifact."""

    model_config = ConfigDict(extra="forbid")

    check_id: str = Field(min_length=1)
    severity: ExportAuditSeverity
    message: str = Field(min_length=1)
    path: str | None = None
    requires_human_review: bool = True


class ExportFileAudit(BaseModel):
    """Audit summary for one export file."""

    model_config = ConfigDict(extra="forbid")

    path: str
    exists: bool
    skipped: bool = False
    skipped_reason: str | None = None
    findings: list[ExportAuditFinding] = Field(default_factory=list)


SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
]
OLD_PROJECT_NAME = "Tu" + "lingResearch"

UNSAFE_CLAIM_PATTERNS = [
    re.compile(r"sparseconv3d\s+(success|succeeded|works|complete)", re.IGNORECASE),
    re.compile(r"fully\s+verified", re.IGNORECASE),
    re.compile(r"final\s+result", re.IGNORECASE),
]

PLANNED_AS_OBSERVED_PATTERN = re.compile(
    r"(planned|future)\s+.*\b(observed|verified|executed|completed)\b",
    re.IGNORECASE,
)


def audit_export_file(path: Path, *, require_limitations: bool = False) -> ExportFileAudit:
    """Audit a single export output file."""

    if not path.exists():
        return ExportFileAudit(
            path=str(path),
            exists=False,
            findings=[
                ExportAuditFinding(
                    check_id="missing-output",
                    severity=ExportAuditSeverity.ERROR,
                    message="Output file is missing and no skipped reason was recorded.",
                    path=str(path),
                )
            ],
        )

    text = path.read_text(encoding="utf-8")
    findings = [
        *_scan_old_naming(text, path),
        *_scan_secrets(text, path),
        *_scan_unsafe_claims(text, path),
        *_scan_planned_as_observed(text, path),
        *_scan_fake_result(text, path),
        *_scan_broken_figure_refs(text, path),
    ]
    if require_limitations and "limitation" not in text.lower():
        findings.append(
            ExportAuditFinding(
                check_id="missing-limitations",
                severity=ExportAuditSeverity.ERROR,
                message="Export output is missing limitations text.",
                path=str(path),
            )
        )

    skipped = "status: skipped" in text.lower()
    skipped_reason = _extract_skipped_reason(text) if skipped else None
    if skipped and not skipped_reason:
        findings.append(
            ExportAuditFinding(
                check_id="missing-skipped-reason",
                severity=ExportAuditSeverity.ERROR,
                message="Output is skipped but skipped reason is missing.",
                path=str(path),
            )
        )

    return ExportFileAudit(
        path=str(path),
        exists=True,
        skipped=skipped,
        skipped_reason=skipped_reason,
        findings=findings,
    )


def audit_export_outputs(
    paths: list[Path],
    *,
    require_limitations: bool = False,
) -> list[ExportFileAudit]:
    """Audit multiple advisor export files."""

    return [audit_export_file(path, require_limitations=require_limitations) for path in paths]


def _scan_old_naming(text: str, path: Path) -> list[ExportAuditFinding]:
    if OLD_PROJECT_NAME not in text:
        return []
    return [
        ExportAuditFinding(
            check_id="old-naming",
            severity=ExportAuditSeverity.ERROR,
            message="Old project naming appears in export output.",
            path=str(path),
        )
    ]


def _scan_secrets(text: str, path: Path) -> list[ExportAuditFinding]:
    findings: list[ExportAuditFinding] = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(
                ExportAuditFinding(
                    check_id="secret-like-value",
                    severity=ExportAuditSeverity.ERROR,
                    message="Secret-like value appears in export output.",
                    path=str(path),
                )
            )
    return findings


def _scan_unsafe_claims(text: str, path: Path) -> list[ExportAuditFinding]:
    findings: list[ExportAuditFinding] = []
    for segment in _iter_claim_segments(text):
        if _is_boundary_line(segment):
            continue
        for pattern in UNSAFE_CLAIM_PATTERNS:
            if pattern.search(segment):
                findings.append(
                    ExportAuditFinding(
                        check_id="unsafe-claim",
                        severity=ExportAuditSeverity.ERROR,
                        message="Unsafe success/finality claim appears in export output.",
                        path=str(path),
                    )
                )
                break
    return findings


def _is_boundary_line(line: str) -> bool:
    lowered = line.lower()
    boundary_markers = [
        "does not",
        "do not",
        "not claim",
        "not claimed",
        "no ",
        "without evidence",
        "remains planned",
        "not observed",
        "not executed",
        "must not",
        "is not",
        "before any",
        "separate from",
        "unsafe claims",
        "not-enough-evidence",
        "not enough evidence",
        "confirms success",
        "requires human review",
        "requires-real-experiment",
        "not-ready",
    ]
    return any(marker in lowered for marker in boundary_markers) or lowered.startswith("confirms ")


def _is_planned_as_observed_line(line: str) -> bool:
    if _is_boundary_line(line):
        return False
    lowered = line.lower()
    if "planned" not in lowered and "future" not in lowered:
        return False
    observed_markers = [" observed", " verified", " executed", " completed"]
    return any(marker in lowered for marker in observed_markers)


def _scan_planned_as_observed(text: str, path: Path) -> list[ExportAuditFinding]:
    if not any(
        PLANNED_AS_OBSERVED_PATTERN.search(segment)
        and _is_planned_as_observed_line(segment)
        for segment in _iter_claim_segments(text)
    ):
        return []
    return [
        ExportAuditFinding(
            check_id="planned-as-observed",
            severity=ExportAuditSeverity.ERROR,
            message="Planned or future work appears to be written as observed.",
            path=str(path),
        )
    ]


def _scan_fake_result(text: str, path: Path) -> list[ExportAuditFinding]:
    lowered = text.lower()
    if "fake result observed" not in lowered and "demo result observed" not in lowered:
        return []
    return [
        ExportAuditFinding(
            check_id="fake-result-observed",
            severity=ExportAuditSeverity.ERROR,
            message="Fake/demo result appears to be marked observed.",
            path=str(path),
        )
    ]


def _scan_broken_figure_refs(text: str, path: Path) -> list[ExportAuditFinding]:
    findings: list[ExportAuditFinding] = []
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "#")):
            continue
        if not (path.parent / target).exists():
            findings.append(
                ExportAuditFinding(
                    check_id="broken-figure-ref",
                    severity=ExportAuditSeverity.ERROR,
                    message=f"Figure reference does not resolve: {target}",
                    path=str(path),
                )
            )
    return findings


def _extract_skipped_reason(text: str) -> str | None:
    for line in text.splitlines():
        if line.lower().startswith("- skipped_reason:"):
            return line.split(":", 1)[1].strip()
        if line.lower().startswith("skipped_reason:"):
            return line.split(":", 1)[1].strip()
    return None


def _iter_claim_segments(text: str) -> list[str]:
    segments: list[str] = []
    for line in text.splitlines():
        normalized = (
            line.replace("&quot;", '"')
            .replace("</pre>", ".")
            .replace("<br>", ".")
            .replace(" - ", ". ")
        )
        parts = re.split(r"(?<=[.!?])\s+|;\s+|\|\s+", normalized)
        segments.extend(part.strip() for part in parts if part.strip())
    return segments
