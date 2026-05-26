"""Guard optional live report text before it is written to artifacts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.live_safety.redaction import (
    LiveRedactionFinding,
    redact_live_output,
)


class LiveReportGuardResult(BaseModel):
    """Review-only guarded live report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    sanitized_text: str
    redactions: list[LiveRedactionFinding] = Field(default_factory=list)
    blocked: bool = False
    raw_output_retained: bool = False
    automatic_evidence_write: bool = False
    requires_human_review: bool = True
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def enforce_live_report_safety(self) -> LiveReportGuardResult:
        if self.raw_output_retained:
            raise ValueError("live report guard must not retain raw output")
        if self.automatic_evidence_write:
            raise ValueError("live report guard cannot write evidence automatically")
        if not self.requires_human_review:
            raise ValueError("live report guard requires human review")
        return self


def guard_live_report(*, report_id: str, source: str, live_output: str) -> LiveReportGuardResult:
    """Return a sanitized live report and block status."""

    redaction = redact_live_output(live_output)
    warnings = [
        "sensitive live output was redacted; human review required"
        for _ in redaction.findings[:1]
    ]
    if not redaction.findings:
        warnings.append("no sensitive live output detected; human review still required")

    return LiveReportGuardResult(
        report_id=report_id,
        source=source,
        sanitized_text=redaction.sanitized_text,
        redactions=redaction.findings,
        blocked=bool(redaction.findings),
        raw_output_retained=False,
        automatic_evidence_write=False,
        requires_human_review=True,
        warnings=warnings,
    )


def render_live_report_guard(result: LiveReportGuardResult) -> str:
    """Render a guarded live report without raw sensitive output."""

    lines = [
        f"# Live Report Guard: {result.report_id}",
        "",
        f"- Source: `{result.source}`",
        f"- Blocked: `{str(result.blocked).lower()}`",
        "- Raw output retained: `false`",
        "- Automatic evidence write: `false`",
        "- Requires human review: `true`",
        "",
        "## Redactions",
        "",
    ]
    if result.redactions:
        lines.extend(
            [
                f"- `{item.kind}` -> `{item.replacement}` ({item.count})"
                for item in result.redactions
            ]
        )
    else:
        lines.append("- None.")

    lines.extend(["", "## Sanitized Output", "", result.sanitized_text])
    return "\n".join(lines).rstrip() + "\n"
