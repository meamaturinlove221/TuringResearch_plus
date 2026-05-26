"""Safety checks for structured return packages."""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.handoff.manifest import sha256_file
from turing_research_plus.pod_lifecycle.transfer_policy import transfer_warnings_for_path
from turing_research_plus.session_runtime.return_manifest import ReturnManifestRuntime

FAKE_OBSERVED_PATTERN = re.compile(
    r"(?i)(fake|demo|synthetic|placeholder).{0,80}(observed|success|verified)"
)


class ReturnSafetyFinding(BaseModel):
    """One return package safety finding."""

    model_config = ConfigDict(extra="forbid")

    finding_id: str = Field(min_length=1)
    path: str | None = None
    message: str = Field(min_length=1)
    release_blocker: bool = True


class ReturnSafetyReport(BaseModel):
    """Safety report for a structured return package."""

    model_config = ConfigDict(extra="forbid")

    findings: list[ReturnSafetyFinding] = Field(default_factory=list)
    checked_files: list[str] = Field(default_factory=list)
    auto_apply_evidence_updates: bool = False
    fake_result_observed_promotion: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether any safety finding blocks ingest review."""

        return any(item.release_blocker for item in self.findings)


def run_return_safety_checks(
    return_dir: Path,
    manifest: ReturnManifestRuntime,
) -> ReturnSafetyReport:
    """Validate return files, paths, checksums, and fake/observed boundaries."""

    findings: list[ReturnSafetyFinding] = []
    checked: list[str] = []
    for file_record in manifest.files:
        path = return_dir / file_record.path
        if not file_record.present:
            if file_record.required:
                findings.append(
                    ReturnSafetyFinding(
                        finding_id="missing-artifact",
                        path=file_record.path,
                        message=f"required return artifact missing: {file_record.path}",
                    )
                )
            continue
        checked.append(file_record.path)
        warnings = transfer_warnings_for_path(
            file_record.path,
            file_size=path.stat().st_size,
        )
        for warning in warnings:
            findings.append(
                ReturnSafetyFinding(
                    finding_id="unsafe-file",
                    path=file_record.path,
                    message=f"unsafe returned file blocked: {warning}",
                )
            )
        expected = manifest.sha256_manifest.get(file_record.path)
        if expected:
            actual = sha256_file(path)
            if actual != expected:
                findings.append(
                    ReturnSafetyFinding(
                        finding_id="checksum-mismatch",
                        path=file_record.path,
                        message="returned file checksum does not match SHA256SUMS.txt",
                    )
                )
        elif file_record.path != "SHA256SUMS.txt":
            findings.append(
                ReturnSafetyFinding(
                    finding_id="missing-checksum",
                    path=file_record.path,
                    message="returned file has no checksum entry",
                )
            )
        if _text_contains_fake_observed_claim(path):
            findings.append(
                ReturnSafetyFinding(
                    finding_id="fake-result-observed-claim",
                    path=file_record.path,
                    message="fake/demo result cannot be treated as observed or verified",
                )
            )

    return ReturnSafetyReport(findings=findings, checked_files=checked)


def _text_contains_fake_observed_claim(path: Path) -> bool:
    if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".txt"}:
        return False
    if path.stat().st_size > 500_000:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return bool(FAKE_OBSERVED_PATTERN.search(text))
