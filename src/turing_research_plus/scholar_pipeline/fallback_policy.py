"""Paper source fallback policy for Scholar parity."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ScholarFallbackStatus(StrEnum):
    """Fallback policy status."""

    ALLOWED = "allowed"
    DEFERRED = "deferred"
    REJECTED = "rejected"


class ScholarFallbackRule(BaseModel):
    """One paper source fallback rule."""

    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1)
    status: ScholarFallbackStatus
    reason: str = Field(min_length=1)
    requires_live_opt_in: bool = False
    requires_human_review: bool = True


class ScholarFallbackPolicy(BaseModel):
    """Review-only paper source fallback policy."""

    model_config = ConfigDict(extra="forbid")

    rules: list[ScholarFallbackRule] = Field(default_factory=list)
    final_paper_conclusion_allowed: bool = False
    automatic_full_paper_download_allowed: bool = False
    paywall_bypass_allowed: bool = False
    heavy_ocr_allowed: bool = False

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe fallback behavior is enabled."""

        return (
            self.final_paper_conclusion_allowed
            or self.automatic_full_paper_download_allowed
            or self.paywall_bypass_allowed
            or self.heavy_ocr_allowed
        )


def build_scholar_fallback_policy() -> ScholarFallbackPolicy:
    """Build the default Scholar paper source fallback policy."""

    return ScholarFallbackPolicy(
        rules=[
            ScholarFallbackRule(
                source="cached_markdown",
                status=ScholarFallbackStatus.ALLOWED,
                reason="Local cached Markdown is preferred when already available.",
            ),
            ScholarFallbackRule(
                source="known_arxiv_metadata",
                status=ScholarFallbackStatus.ALLOWED,
                reason="Known arXiv metadata or URL may be used without downloading full text.",
            ),
            ScholarFallbackRule(
                source="semantic_scholar_fake_or_live",
                status=ScholarFallbackStatus.ALLOWED,
                reason="Fake adapter is default; live adapter requires explicit opt-in.",
                requires_live_opt_in=True,
            ),
            ScholarFallbackRule(
                source="manual_reference_list",
                status=ScholarFallbackStatus.ALLOWED,
                reason="Manual fallback remains review-only.",
            ),
            ScholarFallbackRule(
                source="mineru_heavy_pdf_fallback",
                status=ScholarFallbackStatus.DEFERRED,
                reason="Heavy PDF fallback is deferred beyond v1.2 runtime.",
            ),
            ScholarFallbackRule(
                source="paywall_bypass",
                status=ScholarFallbackStatus.REJECTED,
                reason="Paywall bypass is not allowed.",
            ),
            ScholarFallbackRule(
                source="automatic_full_paper_download",
                status=ScholarFallbackStatus.REJECTED,
                reason="Full paper download is not automatic.",
            ),
        ]
    )


def render_scholar_fallback_policy(policy: ScholarFallbackPolicy) -> str:
    """Render the Scholar fallback policy as Markdown."""

    lines = [
        "# Paper Source Fallback Policy",
        "",
        f"- Release blocker: `{str(policy.release_blocker).lower()}`",
        f"- Final paper conclusion allowed: `{str(policy.final_paper_conclusion_allowed).lower()}`",
        "- Automatic full paper download allowed: "
        f"`{str(policy.automatic_full_paper_download_allowed).lower()}`",
        f"- Paywall bypass allowed: `{str(policy.paywall_bypass_allowed).lower()}`",
        f"- Heavy OCR allowed: `{str(policy.heavy_ocr_allowed).lower()}`",
        "",
        "| Source | Status | Live opt-in | Reason |",
        "| --- | --- | --- | --- |",
    ]
    for rule in policy.rules:
        lines.append(
            f"| `{rule.source}` | `{rule.status.value}` | "
            f"`{str(rule.requires_live_opt_in).lower()}` | {rule.reason} |"
        )
    return "\n".join(lines) + "\n"
