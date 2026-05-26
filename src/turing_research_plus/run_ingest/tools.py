"""Thin tool wrappers for experiment run ingestion."""

from __future__ import annotations

from turing_research_plus.run_ingest.local_bundle_ingestor import ingest_local_bundle
from turing_research_plus.run_ingest.modal_ingestor import ingest_modal_run
from turing_research_plus.run_ingest.models import RunIngestReport, RunIngestRequest, RunSourceType


def ingest_experiment_run(request: RunIngestRequest) -> RunIngestReport:
    """Ingest Modal/local/thin review bundle metadata."""

    if request.source_type in {RunSourceType.MODAL_FIXTURE, RunSourceType.MODAL_EXPORT}:
        return ingest_modal_run(request)
    return ingest_local_bundle(request)
