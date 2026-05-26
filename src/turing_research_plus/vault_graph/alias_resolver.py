"""Alias resolution helpers for review-only ontology SOPs."""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.vault_graph.models import VaultGraph


class AliasResolutionCandidate(BaseModel):
    """One candidate alias-to-node resolution."""

    model_config = ConfigDict(extra="forbid")

    alias: str = Field(min_length=1)
    canonical_node_id: str = Field(min_length=1)
    canonical_label: str = Field(min_length=1)
    confidence: float = Field(default=0.5, ge=0, le=1)
    source_refs: list[str] = Field(default_factory=list)
    reason: str = Field(min_length=1)
    requires_human_review: bool = True


class AliasResolutionReport(BaseModel):
    """Review-only alias resolution report."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    candidates: list[AliasResolutionCandidate] = Field(default_factory=list)
    unresolved_aliases: list[str] = Field(default_factory=list)
    duplicate_aliases: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    def by_alias(self) -> dict[str, AliasResolutionCandidate]:
        """Return candidates keyed by original alias text."""

        return {candidate.alias: candidate for candidate in self.candidates}


def normalize_alias(value: str) -> str:
    """Normalize labels and aliases for conservative local matching."""

    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def resolve_aliases(graph: VaultGraph, aliases: list[str]) -> AliasResolutionReport:
    """Resolve aliases against node labels and node aliases without side effects."""

    alias_index: dict[str, list[str]] = {}
    nodes_by_id = {node.node_id: node for node in graph.nodes}
    for node in graph.nodes:
        names = [node.label, *node.aliases]
        for name in names:
            alias_index.setdefault(normalize_alias(name), []).append(node.node_id)

    candidates: list[AliasResolutionCandidate] = []
    unresolved: list[str] = []
    duplicates: list[str] = []
    for alias in aliases:
        normalized = normalize_alias(alias)
        node_ids = sorted(set(alias_index.get(normalized, [])))
        if len(node_ids) == 1:
            node = nodes_by_id[node_ids[0]]
            candidates.append(
                AliasResolutionCandidate(
                    alias=alias,
                    canonical_node_id=node.node_id,
                    canonical_label=node.label,
                    confidence=node.confidence,
                    source_refs=node.source_refs,
                    reason="matched node label or declared alias",
                )
            )
        elif len(node_ids) > 1:
            duplicates.append(alias)
        else:
            unresolved.append(alias)

    return AliasResolutionReport(
        graph_id=graph.graph_id,
        candidates=candidates,
        unresolved_aliases=unresolved,
        duplicate_aliases=duplicates,
    )


def render_alias_resolution_report(report: AliasResolutionReport) -> str:
    """Render an alias report as Markdown."""

    candidate_lines = [
        f"- `{item.alias}` -> `{item.canonical_node_id}` ({item.canonical_label})"
        for item in report.candidates
    ] or ["- none"]
    unresolved_lines = [f"- `{item}`" for item in report.unresolved_aliases] or ["- none"]
    duplicate_lines = [f"- `{item}`" for item in report.duplicate_aliases] or ["- none"]

    lines = [
        f"# Alias Resolution Report: {report.graph_id}",
        "",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Candidates",
        "",
        *candidate_lines,
        "",
        "## Unresolved",
        "",
        *unresolved_lines,
        "",
        "## Duplicates",
        "",
        *duplicate_lines,
    ]
    return "\n".join(lines) + "\n"
