# TuringResearch Plus Roadmap

This roadmap starts after the TuringResearch Plus v0.1.0 release preparation baseline. It keeps the project MCP-first, contracts-first, source-hygiene gated, and fake-mode testable by default.

## Roadmap Principles

- Public APIs stay under the `turing_research` and `turing_research_plus` packages.
- MCP server identity remains `turingresearch-plus`.
- Live adapters are opt-in and must not make default tests require network access or API keys.
- Research claims, gaps, decisions, and paper sections continue to require EvidenceRef-backed artifacts.
- Race Mode can only promote public or authorized sources that pass Source Hygiene.

## Version Overview

| Version | Theme | Release stance |
| --- | --- | --- |
| v0.2.0 | Live adapters and evidence expansion | Add opt-in live discovery while preserving dry-run defaults. |
| v0.3.0 | Parsing quality and workflow intelligence | Improve OCR, PDF layout, survey depth, and optional LLM-assisted review. |
| v0.4.0 | Race and paper productization | Turn Race Mode, SOP graphs, and paper assets into stronger operator workflows. |
| v1.0.0 | Stable research workflow engine | Freeze public APIs and ship tested end-to-end research workflows. |

## v0.2.0

### Goals

- Add opt-in live scholarly discovery without changing fake-mode defaults.
- Improve PDF Markdown quality beyond Phase A while keeping converter adapters replaceable.
- Expand real citation graph and vault traversal capabilities.
- Make examples more representative of practical research workflows.

### Features

- Live Semantic Scholar adapter behind explicit configuration.
- Live arXiv adapter behind explicit configuration.
- Better PDF Markdown converter selection and quality reports.
- PDF figure and table extraction for local files.
- Real citation graph expansion with depth, frontier, and recommendation controls.
- Stronger vault graph traversal and edge audit workflows.
- Better examples for survey, citation graph, PDF Markdown, and Race Mode.

### Non-Goals

- No default live network execution.
- No heavy OCR pipeline.
- No full complex PDF layout parser.
- No automatic paper writing beyond the existing draft gate.
- No cloud or GPU experiment execution.

### Risks

- Scholarly API rate limits and schema drift can make live adapters flaky.
- PDF extraction quality varies widely across publishers and scanned documents.
- Citation graph expansion can exceed budget if frontier controls are weak.
- Source provenance and license checks must remain explicit when live sources are introduced.

### Required Tests

- Mocked adapter contract tests for Semantic Scholar and arXiv.
- Manual or live-marked tests for optional live calls, skipped by default.
- PDF fixture tests for figure and table extraction.
- Citation graph budget, deduplication, frontier, and recommendation tests.
- Vault traversal tests covering duplicate edges, orphan nodes, and evidence links.
- Example dry-run tests remain network-free.

### Required Docs

- Live adapter setup guide.
- API key and rate-limit guidance without embedding secrets.
- PDF extraction limits and quality scoring guide.
- Citation graph expansion examples.
- Vault traversal and edge audit examples.

### Release Blockers

- Any default test requiring live network or real API keys.
- Any adapter bypassing Source Hygiene or service protocols.
- Any graph expansion path without depth or budget controls.
- Any PDF extraction output that cannot serialize to markdown and json.

## v0.3.0

### Goals

- Add OCR and layout-aware PDF parsing as opt-in, testable pipelines.
- Improve depth-gated literature survey behavior for systematic and deep modes.
- Polish hypothesis-to-experiment workflows into a clearer operator path.
- Add optional LLM-assisted convergence and stress checks while keeping deterministic fallbacks.

### Features

- OCR pipeline for local PDFs with explicit quality warnings.
- Layout-aware PDF parsing for sections, figures, tables, captions, and page maps.
- Advanced literature survey planning, screening, snowballing, and evidence matrix export.
- Hypothesis-to-experiment workflow polish across hypothesis, ideation, convergence, stress, and experiment modules.
- Optional LLM-assisted convergence and stress tests with fake-service fallbacks.
- Source Hygiene dashboard for watch, block, and implementation-eligible ideas.

### Non-Goals

- No unreviewed automatic implementation from external source material.
- No mandatory LLM dependency.
- No claim generation without EvidenceRef.
- No production cloud execution.
- No replacement of the existing contracts-first workflow.

### Risks

- OCR and layout parsing can create misleading text unless quality gates are visible.
- Optional LLM paths can drift from deterministic tests if prompts are not locked.
- Advanced survey workflows can overstate conclusions when full text coverage is weak.
- Dashboard scope can grow into product UI work before the research engine is ready.

### Required Tests

- OCR fixture tests with warnings for low-quality or empty pages.
- Layout parser tests for heading, figure, table, caption, and page-map extraction.
- Deep survey gate tests for full-text ratio and evidence-backed final gaps.
- Hypothesis-to-experiment workflow dry-run tests covering artifact continuity.
- Optional LLM path tests mocked by protocol, skipped for live providers.
- Source Hygiene dashboard model and export tests.

### Required Docs

- OCR pipeline guide and known failure modes.
- Layout-aware PDF parsing guide.
- Advanced survey workflow guide.
- Hypothesis-to-experiment operator guide.
- Optional LLM configuration and safety policy.
- Source Hygiene dashboard documentation.

### Release Blockers

- OCR or layout output without quality warnings.
- Survey conclusions that can pass without evidence refs.
- Optional LLM execution in default tests.
- Source Hygiene dashboard accepting private, leaked, or unauthorized material into implementation.

## v0.4.0

### Goals

- Productize Race Mode as a usable upstream-watch and feature-capsule workflow.
- Improve SOP graph export and paper asset handling.
- Add assisted paper writing while preserving the ExperimentReport hard gate.

### Features

- Race Mode upstream watch improvements for public releases, docs, issues, examples, and commits.
- Automated Feature Capsule generation from hygiene-passed P0/P1 IdeaCards.
- SOP graph UI/export-friendly artifacts and richer Mermaid output.
- Paper figure pipeline polish for diagrams, tables, captions, and block linkage.
- Paper draft assisted writing that remains blocked without ExperimentReport.

### Non-Goals

- No private repository monitoring.
- No bypass of Source Hygiene for competitive intelligence.
- No fully autonomous public release decisions.
- No fabricated paper results.
- No complex web UI beyond export-friendly artifacts unless separately approved.

### Risks

- Upstream watch can confuse roadmap signals with implementation permission.
- Automated capsules can create noisy work unless priority thresholds stay strict.
- Paper writing assistance can overproduce prose without enough evidence.
- SOP graph outputs can drift from actual tool contracts if not validated.

### Required Tests

- Upstream watch snapshot diff tests using public-only fake snapshots.
- Feature Capsule generation tests for contract, skill, tests, docs, and SOP graph skeletons.
- SOP graph export tests for valid Mermaid and quality/failure gate coverage.
- Figure registry tests for caption and ArticleBlock linkage.
- Paper draft gate tests that block missing ExperimentReport.

### Required Docs

- Race Mode upstream watch guide.
- Feature Capsule workflow guide.
- SOP graph export guide.
- Figure and caption pipeline guide.
- Assisted paper writing safety guide.

### Release Blockers

- Any Race Mode path that promotes unknown or blocked sources into implementation.
- Feature Capsule skeleton missing tests, contract, skill, docs, or SOP graph.
- Paper draft generation without ExperimentReport.
- SOP graph docs that diverge from current MCP tools.

## v1.0.0

### Goals

- Ship TuringResearch Plus as a stable, full research workflow engine.
- Stabilize public Python APIs, MCP tool namespaces, contracts, and artifact schemas.
- Provide tested examples and complete documentation for local, fake, and opt-in live workflows.
- Support optional LLM and cloud/GPU adapters through explicit protocols.

### Features

- Full research workflow engine from intent to survey, hypothesis, experiment planning, evidence vault, and paper artifacts.
- Live MCP adapters with clear configuration, rate-limit handling, and fake-mode parity.
- Stable public API for `turing_research` and `turing_research_plus`.
- Full docs, release notes, API references, and operator guides.
- Tested examples covering core, PDF, graph, survey, Race Mode, Vault, Context, SOP, and Paper Pipeline.
- Optional LLM integrations through protocol adapters.
- Optional cloud and GPU execution adapters for experiment workflows.

### Non-Goals

- No default collection from private or unauthorized sources.
- No promise that live APIs are available without user-provided credentials.
- No unsupported copying from license-incompatible projects.
- No hidden network activity during imports, tests, or dry runs.

### Risks

- Stabilizing APIs too early can freeze weak abstractions.
- Live adapter coverage can become provider-specific without strict protocols.
- Optional cloud/GPU execution increases configuration, security, and cost risk.
- Full workflow claims need strong evidence continuity across many modules.

### Required Tests

- Full unit, contract, workflow, integration_fake, package, namespace, and example test matrix.
- Stable API regression tests for public models and tool contracts.
- Live adapter smoke tests marked manual or live and skipped by default.
- End-to-end fake-mode research workflow tests.
- Source Hygiene, Paper Draft Gate, and EvidenceRef integrity tests.

### Required Docs

- Stable API reference.
- MCP tool reference.
- Adapter configuration guide.
- End-to-end workflow guide.
- Security and Source Hygiene policy.
- License review and contribution guide.

### Release Blockers

- Any public tool missing contract and docs coverage.
- Any default path requiring network, API keys, LLM providers, cloud, or GPU.
- Any artifact path that cannot serialize to markdown and json.
- Any paper or research conclusion that can pass without EvidenceRef-backed support.
- Any unresolved naming, import, package, or MCP namespace drift.
