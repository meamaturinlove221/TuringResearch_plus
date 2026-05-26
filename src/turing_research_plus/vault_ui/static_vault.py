"""Build and render local-first static research vault UI."""

from __future__ import annotations

import html
import json
from pathlib import Path

from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import (
    VaultGraph,
    VaultGraphEdgeType,
    VaultGraphNodeType,
)
from turing_research_plus.vault_graph.node_builder import build_node
from turing_research_plus.vault_ui.graph_view import (
    build_vault_graph_view,
    render_vault_graph_view_html,
)
from turing_research_plus.vault_ui.models import (
    ResearchVaultUIBundle,
    VaultUISection,
    VaultUIStatus,
)
from turing_research_plus.vault_ui.search_index import build_vault_search_index

VAULT_UI_CSS = """
:root {
  color-scheme: light;
  --bg: #f7f8fa;
  --panel: #ffffff;
  --text: #1f2937;
  --muted: #5b6573;
  --line: #d9dee7;
  --accent: #215f9a;
  --warn: #8a4b00;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.5;
}
header, main, footer { max-width: 1180px; margin: 0 auto; padding: 24px; }
header { padding-top: 32px; }
h1, h2, h3 { margin: 0 0 10px; }
.meta, .boundary { color: var(--muted); }
.badge {
  display: inline-block;
  border: 1px solid var(--line);
  border-radius: 4px;
  background: var(--panel);
  padding: 2px 6px;
  margin: 0 6px 6px 0;
  font-size: 0.85rem;
}
.layout { display: grid; grid-template-columns: 220px 1fr; gap: 24px; }
nav { position: sticky; top: 12px; align-self: start; display: grid; gap: 8px; }
nav a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid var(--line);
  padding-bottom: 6px;
}
section {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 18px;
  margin-bottom: 16px;
}
pre {
  white-space: pre-wrap;
  background: #f1f3f6;
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 12px;
}
ul { padding-left: 22px; }
.node-list { columns: 2; }
@media (max-width: 760px) {
  .layout { grid-template-columns: 1fr; }
  nav { position: static; }
  .node-list { columns: 1; }
}
"""


def build_vault_ui_bundle(
    graph: VaultGraph,
    *,
    project_name: str,
    output_path: Path | None = None,
    source_markdown: dict[str, str] | None = None,
) -> ResearchVaultUIBundle:
    """Build a static research vault UI bundle from a vault graph."""

    sections = _build_sections(graph, source_markdown or {})
    search_index = build_vault_search_index(graph)
    view = build_vault_graph_view(graph)
    bundle = ResearchVaultUIBundle(
        bundle_id=f"{graph.graph_id}_vault_ui",
        project_name=project_name,
        graph_id=graph.graph_id,
        sections=sections,
        search_index=search_index,
        missing_edges=graph.missing_edges,
        requires_review_nodes=view.requires_review_nodes,
        generated_files=[str(output_path)] if output_path else [],
    )
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_vault_ui_html(bundle, graph), encoding="utf-8")
    return bundle


def render_vault_ui_html(bundle: ResearchVaultUIBundle, graph: VaultGraph) -> str:
    """Render a standalone static vault UI HTML document."""

    nav = "\n".join(
        f'<a href="#{html.escape(section.section_id)}">{html.escape(section.title)}</a>'
        for section in bundle.sections
    )
    section_html = "\n".join(_render_section(section) for section in bundle.sections)
    view_html = render_vault_graph_view_html(build_vault_graph_view(graph))
    search_json = html.escape(
        json.dumps(
            [entry.model_dump(mode="json") for entry in bundle.search_index],
            ensure_ascii=False,
        )
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(bundle.project_name)} Research Vault UI</title>
  <style>{VAULT_UI_CSS}</style>
</head>
<body>
  <header>
    <h1>{html.escape(bundle.project_name)} Research Vault UI</h1>
    <p class="meta">local-first static vault browser - requires human review</p>
    <span class="badge">No server</span>
    <span class="badge">No login</span>
    <span class="badge">No network</span>
    <span class="badge">No graph database</span>
    <span class="badge">Graph is not truth</span>
  </header>
  <main class="layout">
    <nav aria-label="Vault sections">{nav}<a href="#search-index">Search Index</a></nav>
    <div>
      {view_html}
      {section_html}
      <section id="search-index">
        <h2>Simple Static Search Index</h2>
        <p class="boundary">Embedded JSON only. No remote search service is used.</p>
        <script type="application/json" id="vault-search-index">{search_json}</script>
      </section>
    </div>
  </main>
  <footer>
    This vault UI displays existing local graph artifacts only. It does not infer truth,
    run experiments, upload data, or read private paths.
  </footer>
</body>
</html>
"""


def build_vggt_vault_ui_graph() -> VaultGraph:
    """Build the VGGT fixture graph used by the static vault UI."""

    nodes = [
        build_node("vggt", "VGGT", VaultGraphNodeType.CONCEPT, source_refs=["vault_graph"]),
        build_node("smplx", "SMPL-X", VaultGraphNodeType.METHOD, source_refs=["vault_graph"]),
        build_node(
            "feature_adapter",
            "feature adapter",
            VaultGraphNodeType.METHOD,
            source_refs=["vault_graph"],
        ),
        build_node(
            "sparseconv3d",
            "SparseConv3D",
            VaultGraphNodeType.METHOD,
            confidence=0.35,
            source_refs=["vault_graph:planned"],
        ),
        build_node(
            "neuralbody",
            "NeuralBody",
            VaultGraphNodeType.PAPER,
            source_refs=["related_work_fixture"],
        ),
        build_node(
            "humanram",
            "HumanRAM",
            VaultGraphNodeType.PAPER,
            source_refs=["related_work_fixture"],
        ),
        build_node(
            "raw_artifact_gap",
            "raw artifact gap",
            VaultGraphNodeType.ARTIFACT,
            confidence=0.4,
            source_refs=["edge_audit_report"],
        ),
        build_node(
            "sparseconv_success_claim",
            "SparseConv3D success claim",
            VaultGraphNodeType.CLAIM,
            confidence=0.1,
            source_refs=["edge_audit_report:not-established"],
        ),
        build_node(
            "hairline_regression",
            "hairline regression",
            VaultGraphNodeType.FAILURE,
            source_refs=["related_work_graph"],
        ),
        build_node(
            "modal_sparseconv_route",
            "modal_sparseconv_v0",
            VaultGraphNodeType.ROUTE,
            confidence=0.4,
            source_refs=["route_specs"],
        ),
    ]
    edges = [
        build_edge("smplx", "feature_adapter", VaultGraphEdgeType.MAPS_TO, source_refs=["fixture"]),
        build_edge("feature_adapter", "vggt", VaultGraphEdgeType.USES, source_refs=["fixture"]),
        build_edge("neuralbody", "sparseconv3d", VaultGraphEdgeType.RELATED_TO),
        build_edge("humanram", "feature_adapter", VaultGraphEdgeType.RELATED_TO),
        build_edge("hairline_regression", "modal_sparseconv_route", VaultGraphEdgeType.RISKS),
        build_edge("raw_artifact_gap", "sparseconv_success_claim", VaultGraphEdgeType.BLOCKS),
    ]
    return VaultGraph(
        graph_id="vggt-local-vault-ui",
        nodes=nodes,
        edges=edges,
        source_refs=["examples/vggt-human-prior-survey/vault_graph"],
        missing_edges=[
            "SparseConv3D success claim lacks evidence-bearing support edge",
            "Third-party paper links require real source refs before final use",
            "Artifact gap must be resolved before promotion",
        ],
        wikilink_export="optional",
    )


def build_vggt_vault_ui_bundle(root: Path, *, write_files: bool = True) -> ResearchVaultUIBundle:
    """Build the committed VGGT vault UI fixture."""

    graph = build_vggt_vault_ui_graph()
    vault_graph_dir = root / "examples" / "vggt-human-prior-survey" / "vault_graph"
    source_markdown = {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(vault_graph_dir.glob("*.md"))
    }
    output_path = root / "examples" / "vggt-human-prior-survey" / "vault_ui" / "index.html"
    return build_vault_ui_bundle(
        graph,
        project_name="VGGT Human Prior Survey",
        output_path=output_path if write_files else None,
        source_markdown=source_markdown,
    )


def _build_sections(graph: VaultGraph, source_markdown: dict[str, str]) -> list[VaultUISection]:
    grouped = {
        node_type: [node for node in graph.nodes if node.node_type == node_type]
        for node_type in {
            VaultGraphNodeType.CONCEPT,
            VaultGraphNodeType.PAPER,
            VaultGraphNodeType.METHOD,
            VaultGraphNodeType.ARTIFACT,
            VaultGraphNodeType.CLAIM,
            VaultGraphNodeType.FAILURE,
            VaultGraphNodeType.ROUTE,
        }
    }
    sections: list[VaultUISection] = []
    for node_type, nodes in sorted(grouped.items(), key=lambda item: item[0].value):
        title = f"{node_type.value.replace('_', ' ').title()} Nodes"
        if not nodes:
            markdown = "- none recorded"
            status = VaultUIStatus.MISSING
        else:
            markdown = "\n".join(
                f"- [[{node.label}]] (`{node.node_id}`) confidence={node.confidence:.2f} "
                f"status={node.status}"
                for node in nodes
            )
            status = VaultUIStatus.REQUIRES_REVIEW
        sections.append(
            VaultUISection(
                section_id=f"{node_type.value}-nodes",
                title=title,
                status=status,
                node_types=[node_type],
                markdown=markdown,
            )
        )
    sections.append(
        VaultUISection(
            section_id="source-vault-artifacts",
            title="Source Vault Artifacts",
            status=VaultUIStatus.REQUIRES_REVIEW,
            markdown="\n\n".join(
                f"### {name}\n\n{text.strip()}" for name, text in source_markdown.items()
            )
            or "- no source markdown provided",
        )
    )
    return sections


def _render_section(section: VaultUISection) -> str:
    escaped = html.escape(section.markdown.strip())
    return f"""<section id="{html.escape(section.section_id)}">
  <h2>{html.escape(section.title)}</h2>
  <p><span class="badge">{html.escape(section.status)}</span></p>
  <pre>{escaped}</pre>
</section>"""
