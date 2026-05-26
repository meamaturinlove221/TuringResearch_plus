"""Runtime verifier for fake or remote structured return packages."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.session_runtime.proposed_updates import (
    ProposedUpdateLoadReport,
    load_proposed_updates,
)
from turing_research_plus.session_runtime.return_manifest import (
    ReturnManifestRuntime,
    load_return_manifest,
)
from turing_research_plus.session_runtime.return_safety import (
    ReturnSafetyReport,
    run_return_safety_checks,
)


class ReturnVerifierStatus(StrEnum):
    """Status for structured return verification."""

    PASS = "pass"
    BLOCKED = "blocked"


class ReturnVerifierReport(BaseModel):
    """Review-only runtime return verification report."""

    model_config = ConfigDict(extra="forbid")

    return_id: str = Field(min_length=1)
    return_dir: str = Field(min_length=1)
    status: ReturnVerifierStatus
    manifest: ReturnManifestRuntime
    safety: ReturnSafetyReport
    proposed_updates: ProposedUpdateLoadReport
    missing_artifacts: list[str] = Field(default_factory=list)
    unsafe_files: list[str] = Field(default_factory=list)
    checksum_mismatches: list[str] = Field(default_factory=list)
    auto_write_evidence_ledger: bool = False
    proposed_updates_only: bool = True
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether verification blocks ingest review."""

        return self.status == ReturnVerifierStatus.BLOCKED


def verify_return_package(
    return_dir: Path,
    *,
    return_id: str = "return-runtime",
) -> ReturnVerifierReport:
    """Verify a structured return package without applying evidence updates."""

    manifest = load_return_manifest(return_dir)
    safety = run_return_safety_checks(return_dir, manifest)
    proposed_updates = load_proposed_updates(return_dir / "PROPOSED_EVIDENCE_UPDATES.json")

    missing_artifacts = [
        finding.path or ""
        for finding in safety.findings
        if finding.finding_id == "missing-artifact"
    ]
    unsafe_files = [
        finding.path or ""
        for finding in safety.findings
        if finding.finding_id in {"unsafe-file", "fake-result-observed-claim"}
    ]
    checksum_mismatches = [
        finding.path or ""
        for finding in safety.findings
        if finding.finding_id == "checksum-mismatch"
    ]
    blocked = (
        safety.release_blocker
        or proposed_updates.release_blocker
        or bool(manifest.missing_required_files)
    )
    return ReturnVerifierReport(
        return_id=return_id,
        return_dir=return_dir.as_posix(),
        status=ReturnVerifierStatus.BLOCKED if blocked else ReturnVerifierStatus.PASS,
        manifest=manifest,
        safety=safety,
        proposed_updates=proposed_updates,
        missing_artifacts=[item for item in missing_artifacts if item],
        unsafe_files=[item for item in unsafe_files if item],
        checksum_mismatches=[item for item in checksum_mismatches if item],
        auto_write_evidence_ledger=False,
        proposed_updates_only=True,
        requires_human_review=True,
    )


def render_return_verifier_report(report: ReturnVerifierReport) -> str:
    """Render a verifier report for human review."""

    lines = [
        f"# Remote Return Verifier Report: {report.return_id}",
        "",
        f"- Status: `{report.status}`",
        f"- Return dir: `{report.return_dir}`",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        "- Auto-write Evidence Ledger: `false`",
        "- Proposed updates only: `true`",
        "- Requires human review: `true`",
        "",
        "## Missing Artifacts",
        "",
    ]
    lines.extend([f"- `{item}`" for item in report.missing_artifacts] or ["- None."])
    lines.extend(["", "## Unsafe Files", ""])
    lines.extend([f"- `{item}`" for item in report.unsafe_files] or ["- None."])
    lines.extend(["", "## Checksum Mismatches", ""])
    lines.extend([f"- `{item}`" for item in report.checksum_mismatches] or ["- None."])
    lines.extend(["", "## Proposed Updates", ""])
    lines.extend(
        [f"- `{item.update_id}` status `{item.status}`" for item in report.proposed_updates.updates]
        or ["- None."]
    )
    lines.extend(["", "## Findings", ""])
    lines.extend(
        [
            f"- `{item.finding_id}`"
            + (f" `{item.path}`" if item.path else "")
            + f": {item.message}"
            for item in report.safety.findings
        ]
        or ["- None."]
    )
    return "\n".join(lines) + "\n"
