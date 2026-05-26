"""Thin citation graph tool wrappers."""

from __future__ import annotations

from turing_research_plus.citation_graph.expander import CitationGraphExpander
from turing_research_plus.citation_graph.markdown_export import citation_graph_to_markdown
from turing_research_plus.citation_graph.models import CitationGraph, CitationGraphRequest


def citation_graph_expand(request: CitationGraphRequest) -> CitationGraph:
    """Expand a citation graph through fake/manual/live-optional adapters."""

    return CitationGraphExpander().expand(request)


def citation_graph_export_markdown(graph: CitationGraph) -> str:
    """Export citation graph to Markdown."""

    return citation_graph_to_markdown(graph)
