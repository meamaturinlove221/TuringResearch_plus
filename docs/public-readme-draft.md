# TuringResearch Plus

TuringResearch Plus is a Python, MCP-first research workflow engine for evidence-backed research workflows, Race Mode feature planning, and paper pipeline dry-runs.

Packages:

- Core: `turing_research`
- Plus workflows: `turing_research_plus`

MCP server name: `turingresearch-plus`.

## What It Does

- Core local tools for health checks, cached paper/web Markdown, sessions, and local PDF Markdown.
- PDF input to Markdown through Phase A local PyMuPDF-compatible adapter boundaries.
- Depth-gated literature survey with scoping, systematic, deep, narrative, and snowball strategies.
- Semantic citation graph through fake-adapter-tested paper, citation, recommendation, and author tools.
- Claim-evidence vault with markdown pages, typed graph edges, lint, search, and artifact ingestion.
- Hypothesis-to-experiment workflow from gaps to hypotheses, ideas, convergence decisions, stress tests, and experiment plans.
- Race Mode idea capture with Source Hygiene Gate, Priority Elevator, Feature Capsule skeletons, architecture boxes, and Upstream Watch.
- SOP graph generator for campaign, feature, paper, experiment, and release workflows.
- Paper / Figure pipeline with DocFlow Article Blocks, figure registry, captions, draft gate, missing evidence reports, and LaTeX export.
- Codex-compatible repo-scoped skills under `.agents/skills/turingresearch-*`.

## Quickstart

```powershell
python -m pip install -e .[dev,pdf,mcp]
python -m pytest
python -m ruff check .
python -m mypy src
python -m turing_research.mcp_server --manifest
```

Default tests run without real API keys or live network access. Examples use fake services, dry-run workflows, and local fixtures.

## Safety Gates

- Source Hygiene blocks private, leaked, NDA, proprietary, or incompatible-license implementation work.
- Paper drafts are blocked until `ExperimentReport` exists.
- Important outputs become `ResearchArtifact`.
- Major conclusions preserve `EvidenceRef`.
- STDIO MCP mode keeps operational logs off stdout.

## Local Examples

- `examples/vggt-human-prior-survey/`
- `examples/smplx-feature-adapter-hypothesis/`
- `examples/citation-graph-demo/`
- `examples/pdf-to-markdown-demo/`

See `docs/examples.md`.

## References

TuringResearch Plus is inspired by public research-tooling patterns, including Neocortica and Yogsoth AI references. These are references only; project names, packages, tools, docs, and skills use the TuringResearch naming system.
