"""Unsafe claim guards for paper draft beta packages."""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

UNSAFE_CLAIM_MARKERS = (
    "SparseConv3D success",
    "SparseConv3D integration is already successful",
    "quantitative experiment numbers",
    "final novelty",
    "final paper",
    "camera-ready",
    "observed result",
)

BLOCKING_CONTEXT_MARKERS = (
    "do not claim",
    "do not report",
    "not claimed",
    "not established",
    "blocked",
    "missing",
    "requires human review",
    "reason:",
    "requires real experiment evidence",
    "not final",
    "before final",
    "not observed",
    "not camera-ready",
)


class PaperClaimGuardReport(BaseModel):
    """Report describing unsafe paper claims and how they are blocked."""

    model_config = ConfigDict(extra="forbid")

    blocked_claims: list[str] = Field(default_factory=list)
    risky_unblocked_claims: list[str] = Field(default_factory=list)
    final_paper_claim_blocked: bool = True
    fake_observed_claim_blocked: bool = True
    result_fabrication_blocked: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def guard_must_block_final_or_fake_claims(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("paper claim guard requires human review")
        if not self.final_paper_claim_blocked:
            raise ValueError("final paper claim blocking must stay enabled")
        if not self.fake_observed_claim_blocked:
            raise ValueError("fake observed claim blocking must stay enabled")
        if not self.result_fabrication_blocked:
            raise ValueError("result fabrication blocking must stay enabled")
        return self


def evaluate_paper_claims(text_by_section: dict[str, str]) -> PaperClaimGuardReport:
    """Evaluate draft input text without promoting unsafe claims."""

    blocked: list[str] = []
    risky: list[str] = []

    for section, text in text_by_section.items():
        for line in text.splitlines():
            normalized = line.strip()
            if not normalized:
                continue
            lowered = normalized.lower()
            if not any(marker.lower() in lowered for marker in UNSAFE_CLAIM_MARKERS):
                continue
            entry = f"{section}: {normalized}"
            if any(marker in lowered for marker in BLOCKING_CONTEXT_MARKERS):
                blocked.append(entry)
            else:
                risky.append(entry)

    return PaperClaimGuardReport(
        blocked_claims=blocked,
        risky_unblocked_claims=risky,
    )


def render_paper_claim_guard_report(report: PaperClaimGuardReport) -> str:
    """Render claim guard results as Markdown."""

    lines = [
        "# Unsafe Claim Report",
        "",
        f"- Final paper claim blocked: `{str(report.final_paper_claim_blocked).lower()}`",
        f"- Fake observed claim blocked: `{str(report.fake_observed_claim_blocked).lower()}`",
        f"- Result fabrication blocked: `{str(report.result_fabrication_blocked).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in report.blocked_claims],
        "",
        "## Claims Requiring Additional Review",
        "",
        *([f"- {claim}" for claim in report.risky_unblocked_claims] or ["- None."]),
        "",
        "## Boundary",
        "",
        "- This beta package does not write final paper claims.",
        "- Demo or fixture material is not observed evidence.",
        "- Unsupported experiment success claims remain blocked.",
        "",
    ]
    return "\n".join(lines)
