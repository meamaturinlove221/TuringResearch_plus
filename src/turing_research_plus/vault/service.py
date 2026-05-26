"""Wiki Vault service."""

from __future__ import annotations

from pathlib import Path

from tuling_research_plus.artifacts.models import EvidenceRef, ResearchArtifact
from tuling_research_plus.vault.graph import DuplicateEdgeError, VaultGraph
from tuling_research_plus.vault.index import VaultIndex
from tuling_research_plus.vault.lint import lint_vault
from tuling_research_plus.vault.markdown_io import read_page, write_page
from tuling_research_plus.vault.models import (
    VaultEdge,
    VaultEdgeType,
    VaultEntityType,
    VaultGraphStats,
    VaultIngestResult,
    VaultLintIssue,
    VaultPage,
    VaultSearchResult,
)


class VaultService:
    """Filesystem-backed Wiki Vault."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.graph = VaultGraph(self.root)
        self.index = VaultIndex(self.root)

    def compile_page(self, page: VaultPage) -> Path:
        return write_page(self.root, page)

    def read_page(self, page_id: str) -> VaultPage:
        return read_page(self.root / f"{page_id}.md")

    def search(self, query: str, limit: int = 10) -> list[VaultSearchResult]:
        return self.index.search(query, limit)

    def add_edge(self, edge: VaultEdge) -> VaultEdge:
        return self.graph.add_edge(edge)

    def query_graph(self, page_id: str, depth: int = 1) -> list[str]:
        return self.graph.neighbors(page_id, depth)

    def graph_stats(self) -> VaultGraphStats:
        return self.graph.stats()

    def lint(self) -> list[VaultLintIssue]:
        return lint_vault(self.root)

    def edge_audit(self) -> list[VaultEdge]:
        return self.graph.list_edges()

    def ingest_artifact(self, artifact: ResearchArtifact) -> VaultIngestResult:
        """Ingest a ResearchArtifact as claim and evidence vault pages."""

        claim = VaultPage(
            page_id=f"claim-{artifact.artifact_id}",
            title=artifact.title,
            entity_type=VaultEntityType.CLAIM,
            body=str(artifact.content),
            evidence=artifact.evidence,
            artifact_id=artifact.artifact_id,
            tags=artifact.tags,
        )
        self.compile_page(claim)
        pages = [claim]
        edges: list[VaultEdge] = []
        for index, evidence in enumerate(artifact.evidence, start=1):
            evidence_page = VaultPage(
                page_id=f"evidence-{artifact.artifact_id}-{index}",
                title=f"Evidence for {artifact.title} #{index}",
                entity_type=VaultEntityType.EVIDENCE,
                body=evidence.quote,
                evidence=[evidence],
                artifact_id=artifact.artifact_id,
            )
            self.compile_page(evidence_page)
            pages.append(evidence_page)
            edge = VaultEdge(
                source_id=claim.page_id,
                target_id=evidence_page.page_id,
                edge_type=VaultEdgeType.SUPPORTED_BY,
                evidence=[evidence],
            )
            try:
                self.add_edge(edge)
                edges.append(edge)
            except DuplicateEdgeError:
                pass
        return VaultIngestResult(pages=pages, edges=edges)

    def ingest_source(
        self,
        page_id: str,
        title: str,
        body: str,
        evidence: list[EvidenceRef],
    ) -> VaultPage:
        page = VaultPage(
            page_id=page_id,
            title=title,
            entity_type=VaultEntityType.SOURCE,
            body=body,
            evidence=evidence,
        )
        self.compile_page(page)
        return page
