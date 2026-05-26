"""Optional heavy PDF backend slot.

This module reserves an interface for future heavy PDF backends such as MinerU
or arxiv2md fallback without implementing or importing those backends.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class HeavyPdfBackendStatus(StrEnum):
    """Status values for optional heavy PDF backend planning."""

    DISABLED = "disabled"
    SKIPPED = "skipped"
    FUTURE_BACKEND = "future-backend"


class HeavyPdfBackendKind(StrEnum):
    """Known future backend slots."""

    MINERU = "mineru"
    ARXIV2MD = "arxiv2md"
    CUSTOM = "custom"


class HeavyPdfBackendRequest(BaseModel):
    """Request for describing a future heavy PDF backend.

    The request intentionally cannot enable processing in v1.4.
    """

    model_config = ConfigDict(extra="forbid")

    backend: HeavyPdfBackendKind = HeavyPdfBackendKind.MINERU
    pdf_path: Path | None = None
    enabled: bool = False
    ocr_enabled: bool = False
    large_pdf_processing: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_disabled_slot(self) -> Self:
        if self.enabled:
            raise ValueError("heavy PDF backend slot is disabled by default")
        if self.ocr_enabled:
            raise ValueError("heavy PDF backend slot does not enable OCR")
        if self.large_pdf_processing:
            raise ValueError("heavy PDF backend slot does not process large PDFs")
        if not self.requires_human_review:
            raise ValueError("heavy PDF backend slot requires human review")
        return self


class HeavyPdfBackendSlot(BaseModel):
    """Description of the reserved backend slot."""

    model_config = ConfigDict(extra="forbid")

    backend: HeavyPdfBackendKind
    status: HeavyPdfBackendStatus = HeavyPdfBackendStatus.DISABLED
    interface_only: bool = True
    implementation_present: bool = False
    dependency_required: bool = False
    ocr_enabled: bool = False
    large_pdf_processing: bool = False
    skipped_reason: str = Field(min_length=1)
    future_backend_notes: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe heavy backend behavior was enabled."""

        return (
            self.implementation_present
            or self.dependency_required
            or self.ocr_enabled
            or self.large_pdf_processing
            or not self.requires_human_review
        )


def build_heavy_pdf_backend_slot(
    request: HeavyPdfBackendRequest | None = None,
) -> HeavyPdfBackendSlot:
    """Build a disabled interface-only backend slot."""

    request = request or HeavyPdfBackendRequest()
    backend_name = request.backend.value
    return HeavyPdfBackendSlot(
        backend=request.backend,
        status=HeavyPdfBackendStatus.SKIPPED,
        interface_only=True,
        implementation_present=False,
        dependency_required=False,
        ocr_enabled=False,
        large_pdf_processing=False,
        skipped_reason=(
            f"{backend_name} is reserved as a future optional backend; "
            "v1.4 exposes only the interface slot."
        ),
        future_backend_notes=[
            "Backend must remain opt-in.",
            "Backend must not add heavy dependencies to the default install.",
            "Backend outputs must remain review-only until human verified.",
        ],
        requires_human_review=request.requires_human_review,
    )


def render_heavy_pdf_backend_slot(slot: HeavyPdfBackendSlot) -> str:
    """Render the backend slot as Markdown."""

    lines = [
        "# Optional Heavy PDF Backend Slot",
        "",
        f"- Backend: `{slot.backend.value}`",
        f"- Status: `{slot.status.value}`",
        f"- Interface only: `{str(slot.interface_only).lower()}`",
        f"- Implementation present: `{str(slot.implementation_present).lower()}`",
        f"- Dependency required: `{str(slot.dependency_required).lower()}`",
        f"- OCR enabled: `{str(slot.ocr_enabled).lower()}`",
        f"- Large PDF processing: `{str(slot.large_pdf_processing).lower()}`",
        f"- Requires human review: `{str(slot.requires_human_review).lower()}`",
        "",
        "## Skipped Reason",
        "",
        slot.skipped_reason,
        "",
        "## Future Backend Notes",
        "",
    ]
    lines.extend(f"- {note}" for note in slot.future_backend_notes)
    return "\n".join(lines) + "\n"
