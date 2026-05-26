"""Local helper wrappers for extension safety gates."""

from __future__ import annotations

from turing_research_plus.extension_safety.models import (
    ExtensionManifestRef,
    ExtensionSafetyReport,
)
from turing_research_plus.extension_safety.report import (
    render_extension_safety_report_markdown,
)
from turing_research_plus.extension_safety.validator import validate_extension_safety


def extension_safety_check(manifest: ExtensionManifestRef) -> ExtensionSafetyReport:
    """Validate one extension manifest reference."""

    return validate_extension_safety(manifest)


def extension_safety_markdown(manifest: ExtensionManifestRef) -> str:
    """Render the safety report for one extension manifest reference."""

    return render_extension_safety_report_markdown(validate_extension_safety(manifest))
