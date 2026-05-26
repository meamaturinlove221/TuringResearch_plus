"""Modal run ingestor facade."""

from __future__ import annotations

from turing_research_plus.run_ingest.local_bundle_ingestor import ingest_local_bundle
from turing_research_plus.run_ingest.models import RunIngestReport, RunIngestRequest


def ingest_modal_run(request: RunIngestRequest) -> RunIngestReport:
    """Ingest a Modal fixture or exported bundle without running Modal."""

    return ingest_local_bundle(request)
