"""Markdown export helpers for VGGT evidence ledgers."""

from __future__ import annotations

from turing_research_plus.vggt.evidence_models import VGGTEvidenceLedger


def export_vggt_evidence_markdown(ledger: VGGTEvidenceLedger) -> str:
    """Return the ledger Markdown representation without adding new claims."""

    return ledger.to_markdown()
