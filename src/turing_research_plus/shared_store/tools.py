"""Local tool wrappers for shared store scanning."""

from __future__ import annotations

from turing_research_plus.shared_store.local_mount_reader import scan_local_mount
from turing_research_plus.shared_store.models import SharedStoreReport, SharedStoreScanRequest


def artifact_shared_store_index(request: SharedStoreScanRequest) -> SharedStoreReport:
    """Index an already mounted shared artifact store path."""

    return scan_local_mount(request)
