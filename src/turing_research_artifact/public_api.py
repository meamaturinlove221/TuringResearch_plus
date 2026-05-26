"""Public API facade for artifact workflow modules."""

from turing_research_plus.artifact_audit import ArtifactAuditReport, artifact_audit
from turing_research_plus.handoff import HandoffBundleManifest
from turing_research_plus.remote_artifacts import (
    UnifiedRemoteArtifactReport,
    build_unified_remote_artifact_report,
)
from turing_research_plus.run_ingest import RunIngestReport

NAMESPACE = "turing_research_artifact"
COMPATIBILITY_NAMESPACE = "turing_research_plus"
STABILITY = "experimental"
PUBLIC_MODULE_ALIASES = {
    "artifact_audit": "turing_research_plus.artifact_audit",
    "handoff": "turing_research_plus.handoff",
    "remote_artifacts": "turing_research_plus.remote_artifacts",
    "run_ingest": "turing_research_plus.run_ingest",
}

__all__ = [
    "COMPATIBILITY_NAMESPACE",
    "NAMESPACE",
    "PUBLIC_MODULE_ALIASES",
    "STABILITY",
    "ArtifactAuditReport",
    "HandoffBundleManifest",
    "RunIngestReport",
    "UnifiedRemoteArtifactReport",
    "artifact_audit",
    "build_unified_remote_artifact_report",
]
