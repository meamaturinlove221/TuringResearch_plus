# TuringResearch Plus v0.1.0 Release Notes

Date: 2026-05-20

## 1. What Is TuringResearch Plus

TuringResearch Plus is a Python MCP-first research workflow engine for evidence-backed research planning, literature workflow dry-runs, idea capture, experiment planning, and paper pipeline gating.

It is organized as one repository with two Python packages:

- `turing_research`: Core local tools, cache, sessions, PDF Markdown, and the local MCP smoke server.
- `turing_research_plus`: Plus workflows for survey, semantic graph, vault, context, Race Mode, SOP, experiment, and paper pipelines.

MCP server name: `turingresearch-plus`.

## 2. v0.1.0 Scope

`v0.1.0` is a release-candidate foundation. It demonstrates the architecture, contracts, local tools, dry-run workflows, fake adapters, examples, skills, and release gates. It is not a fully automated live research system.

Included:

- Core local tools.
- PDF Markdown Phase A.
- Semantic Graph fake adapter and dry-run.
- Literature Survey dry-run.
- Vault / Context base.
- Race Mode base.
- Feature Capsule skeleton.
- DocFlow Article Blocks.
- SOP Graph Generator.
- Figure Asset Registry.
- Paper Draft Gate.
- Codex-compatible repo-scoped skills.
- Contract tests, workflow dry-run tests, and fake-mode examples.

## 3. Main Features

- Single-window multi-agent lane architecture.
- Contracts-first design.
- TuringResearch Core local tools.
- PDF input to Markdown Phase A.
- Semantic Graph dry-run.
- Literature Survey dry-run.
- Vault / Context base.
- Race Mode base.
- Feature Capsule skeleton.
- DocFlow Article Blocks.
- SOP Graph Generator.
- Figure Asset Registry.
- Paper Draft Gate.
- Codex-compatible skills.

## 4. What Is Fake / Dry-Run Mode

Fake mode and dry-run mode are deterministic local execution modes used for tests, examples, and release validation.

They provide:

- Stable outputs without real network access.
- Fake adapters instead of live scholarly or web APIs.
- Local fixtures instead of private papers or restricted datasets.
- Workflow shape validation without claiming live research completeness.

They do not provide:

- Live Semantic Scholar or arXiv fetching by default.
- Live web crawling.
- Real GPU experiment execution.
- Final scientific conclusions without external review.

## 5. What Is Not Included Yet

- Live network adapters enabled by default.
- Heavy OCR.
- Advanced PDF layout parsing.
- Full automatic paper writing.
- Real GPU experiment execution.
- Automatic PyPI publishing.
- Private or unauthorized source idea implementation.

## 6. PDF Markdown Phase A Status

PDF Markdown Phase A supports local PDF paths and a minimal PyMuPDF converter route when the optional PDF extra is installed.

Included:

- `pdf.inspect`
- `pdf.to_markdown`
- `pdf.cache_lookup`
- `pdf.markdown_content`
- Cache metadata.
- Page map output.
- Quality score and warnings.

Not included yet:

- Heavy OCR.
- Complex layout-aware parsing.
- Production-grade figure extraction.
- Production-grade table extraction.

## 7. MCP Tools Status

The frozen MCP namespaces are:

- `core.*`
- `pdf.*`
- `graph.*`
- `research.*`
- `vault.*`
- `context.*`
- `race.*`
- `paper.*`

Release candidate status:

| Status | Meaning |
| --- | --- |
| `implemented_minimal` | Local deterministic implementation exists. |
| `implemented_dry_run` | Deterministic fake-service or dry-run workflow exists. |
| `contract_only` | Public contract exists; live or complex implementation is planned later. |

The release candidate report records 79 MCP tools across approved namespaces.

## 8. Skills Status

Repo-scoped skills live in `.agents/skills/turingresearch-*/SKILL.md`.

Status:

- Required skills exist.
- Skills use the `turingresearch-` prefix.
- Skills are indexed in `docs/skills-index.md`.
- Release-critical skills are locked.

## 9. Examples Status

Release examples run in fake mode or local fixture dry-run mode:

- `examples/vggt-human-prior-survey/`
- `examples/smplx-feature-adapter-hypothesis/`
- `examples/citation-graph-demo/`
- `examples/pdf-to-markdown-demo/`

Examples do not require real API keys, live network access, private papers, or restricted datasets.

## 10. Known Limitations

- Live network adapters are not enabled by default.
- OCR is not complete.
- Advanced PDF layout parsing is not complete.
- Paper draft does not fabricate experiment results.
- Real GPU experiment execution is not included.
- API keys are required only for future live mode.
- `v0.1.0` mainly demonstrates architecture, contracts, dry-run workflows, and local tools.

## 11. Safety And Source Hygiene

TuringResearch Plus blocks implementation work from private repository content, leaked roadmap material, NDA content, proprietary code, copied incompatible-license implementation details, private papers without authorization, restricted datasets, and secrets.

Allowed sources include public repositories, public README files, public issues, public release notes, user-owned notes, and authorized transcripts.

The default release path does not require real API keys and does not perform live network calls in tests.

## 12. Roadmap

Planned post-`v0.1.0` work:

- `v0.2.0`: opt-in live Semantic Scholar and arXiv adapters, better PDF converters, figure/table extraction, real citation graph expansion, stronger Vault traversal, better examples.
- `v0.3.0`: OCR pipeline, layout-aware PDF parsing, advanced survey workflows, hypothesis-to-experiment polish, optional LLM-assisted convergence and stress tests.
- `v0.4.0`: Race Mode upstream watch, automated Feature Capsule generation, SOP graph UI/export, paper figure pipeline polish, assisted paper writing.
- `v1.0.0`: stable public API, live MCP adapters, tested examples, full docs, optional LLM integrations, and optional cloud/GPU execution adapters.

## Release Recommendation

GO for final human review and `v0.1.0` release tag preparation.
