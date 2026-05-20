# TulingResearch Plus

TulingResearch Plus is a Python, MCP-first research workflow engine for evidence-backed literature work, idea capture, feature planning, experiment design, and paper pipeline dry-runs.

It is built as one repository with two Python packages:

- `tuling_research`: Core tools for local cache, sessions, content lookup, PDF Markdown, and the local MCP smoke server.
- `tuling_research_plus`: Plus workflows for survey, semantic graph, vault, context, Race Mode, SOP, experiment, and paper pipelines.

MCP server name: `tulingresearch-plus`.

## Python MCP-First Design

TulingResearch Plus treats MCP tools as the public boundary. Contracts live in `contracts/`, Pydantic models define stable payloads, and implementations stay behind service protocols or adapters. External APIs are adapterized, network tests are mocked, and default workflows run in dry-run or fake-service mode.

The local MCP smoke module is:

```powershell
python -m tuling_research.mcp_server --manifest
```

Console entry points:

- `tulingresearch-plus`
- `tulingresearch-plus-mcp`

Both call `tuling_research.mcp_server:main`.

## Single Window, Multiple Lanes

The project is designed for single-window multi-agent style development. Parallel work is coordinated through:

- `lanes/`: lane ledgers and release-candidate state.
- `contracts/`: stable tool and artifact contracts.
- `.agents/skills/`: Codex-compatible repo-scoped skills with `tulingresearch-` names.

This keeps architecture, implementation, QA, and release work in one repository without splitting context or package ownership.

## Core Tools

The Core layer provides local deterministic tools:

- `core.health_check`
- `core.paper_content`
- `core.web_content`
- `core.session_list`

The Core package is `tuling_research`.

## PDF Input To Markdown

Phase A supports local PDF paths through `tuling_research.pdf`:

- `pdf.inspect`
- `pdf.to_markdown`
- `pdf.cache_lookup`
- `pdf.markdown_content`

The output model is `PDFMarkdownOutput`, including markdown path, page map, quality score, warnings, and cache-hit state. Heavy OCR and complex layout parsing are outside `v0.1.0`.

## Depth-Gated Literature Survey

The survey workflow supports scoping, systematic, deep, narrative, and snowball strategies. It routes through fake paper/PDF/graph services in tests and enforces depth gates such as full-text ratio and evidence-backed final gaps.

## Semantic Citation Graph

The semantic graph layer exposes `graph.*` tools for paper lookup, references, citations, recommendations, author lookup, citation graph expansion, and author networks. Tests use fake adapters; no Semantic Scholar key is required by default.

## Claim-Evidence Vault

The Vault is a local markdown knowledge graph with typed entities, typed edges, lint, search, and artifact ingestion. Claims connect to evidence through explicit edges, and orphan or malformed pages are lintable.

## Hypothesis-To-Experiment Workflow

TulingResearch Plus can dry-run a research chain from validated gaps to hypotheses, idea portfolios, convergence decisions, stress tests, experiment plans, constraint analysis, scenario plans, implementation plans, result schemas, and dry-run result analysis.

## Race Mode Idea Capture

Race Mode turns public or authorized notes into IdeaCards, priority scores, feature capsule skeletons, architecture boxes, and upstream watch reports. Source Hygiene Gate blocks private, leaked, NDA, proprietary, or incompatible-license material from becoming implementation work.

## Feature Capsule Workflow

Feature Capsules are self-contained implementation planning bundles. A capsule includes a problem statement, user story, contract, skill skeleton, tests, docs, and SOP graph. `v0.1.0` generates minimal skeletons only.

## SOP Graph Generator

The SOP graph generator creates Mermaid graphs and SOP documents for campaign, feature, paper, experiment, and release flows. Graphs include nodes, edges, input/output artifacts, tools, quality gates, and failure gates.

## Paper / Figure Pipeline

The paper pipeline includes DocFlow Article Blocks, figure registry, caption generation, missing-evidence reports, draft gate, and LaTeX export. Full paper drafts are blocked until required artifacts, especially `ExperimentReport`, are present.

## Codex-Compatible Skills

Repo-scoped skills live under `.agents/skills/tulingresearch-*/SKILL.md`. They document owner lanes, related contracts, required tests, constraints, and done criteria for single-window coordinated development.

## Quickstart

```powershell
python -m pip install -e .[dev]
python -m pytest
python -m ruff check .
python -m mypy src
```

Optional local PDF and MCP extras:

```powershell
python -m pip install -e .[dev,pdf,mcp]
python -m tuling_research.mcp_server --manifest
tulingresearch-plus-mcp --health-check
```

Default tests use fake services, dry-run workflows, and local fixtures. They do not require real API keys or live network access.

## Local Fake-Mode Examples

See `docs/examples.md` and `examples/` for release-candidate examples:

- `examples/vggt-human-prior-survey/`
- `examples/smplx-feature-adapter-hypothesis/`
- `examples/citation-graph-demo/`
- `examples/pdf-to-markdown-demo/`

Each example has `input/`, `expected_outputs/`, `fake_run_config.yaml`, and workflow tests.

## Safety / Source Hygiene

- Source Hygiene blocks unsafe or unauthorized source material.
- Every major conclusion should preserve `EvidenceRef`.
- Important workflow outputs become `ResearchArtifact`.
- Network tests are mocked.
- Live/manual tests are skipped by default.
- STDIO MCP mode does not write logs to stdout.

## Roadmap

`v0.1.0` focuses on local contracts, dry-run workflows, fake adapters, examples, CI, and release readiness. Future work can add live adapters, richer PDF parsing, heavier workflow automation, public package publishing, and production deployment after the current contracts remain stable.

## References

TulingResearch Plus is inspired by public research-tooling ideas and workflow patterns, including Neocortica and Yogsoth AI references. They are references only; this project, packages, MCP server, tools, skills, and documentation use the TulingResearch naming system.
