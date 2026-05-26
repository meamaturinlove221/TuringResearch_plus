"""Thin tool wrappers for handoff bundle export/import."""

from __future__ import annotations

from turing_research_plus.handoff.exporter import export_handoff_bundle
from turing_research_plus.handoff.importer import import_handoff_bundle
from turing_research_plus.handoff.models import (
    HandoffBundleImportReport,
    HandoffBundleManifest,
    HandoffExportRequest,
    HandoffImportRequest,
)


def handoff_bundle_export(request: HandoffExportRequest) -> HandoffBundleManifest:
    """Export a controlled handoff bundle."""

    return export_handoff_bundle(request)


def handoff_bundle_import(request: HandoffImportRequest) -> HandoffBundleImportReport:
    """Validate a handoff bundle without mutating local ledgers."""

    return import_handoff_bundle(request)
