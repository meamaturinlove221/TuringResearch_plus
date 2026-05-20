# Changelog

All notable changes to TulingResearch Plus are documented in this file.

The format follows Keep a Changelog style.

## [0.1.0] - 2026-05-20

### Added

- Single-window multi-agent lane architecture using `lanes/`, `contracts/`, and `.agents/skills/`.
- Contracts-first MCP tool design for `tulingresearch-plus`.
- TulingResearch Core local tools in `tuling_research`.
- TulingResearch Plus workflow package in `tuling_research_plus`.
- PDF input to Markdown Phase A for local PDF inspection, conversion, cache lookup, and markdown content.
- Semantic Graph dry-run and fake-adapter graph tools.
- Depth-gated Literature Survey dry-run workflows.
- Vault and Context base capabilities.
- Race Mode base with Source Hygiene, Idea Radar, Priority Elevator, Feature Capsule skeleton, architecture boxes, and Upstream Watch.
- Feature Capsule skeleton generation.
- DocFlow Article Blocks.
- SOP Graph Generator.
- Figure Asset Registry and caption generation.
- Paper Draft Gate and missing-evidence reporting.
- Codex-compatible repo-scoped skills.
- QA / release checklist, release freeze docs, release candidate report, final verification docs, local install smoke docs, and CI workflows.
- Fake-mode examples for survey, feature-adapter hypothesis, citation graph, and PDF Markdown.
- Public repo hygiene files, issue templates, pull request template, Source Hygiene policy, and license decision note.

### Changed

- Public docs now use the TulingResearch Plus naming system consistently.
- Packaging exposes `tulingresearch-plus` and `tulingresearch-plus-mcp` entry points.
- Pytest defaults skip `live` and `manual` tests.
- Mypy is configured for release-candidate typed-boundary checks.
- Example READMEs explicitly state that real API keys are not required.
- Release notes now clarify fake/dry-run mode and the `v0.1.0` scope boundary.

### Fixed

- Removed legacy naming drift from docs, tests, contracts, and skill metadata.
- Synchronized MCP tool implementation statuses between contracts and docs.
- Fixed contract YAML status/type concatenation.
- Added integrity tests for names, imports, tool namespaces, contracts, skills, package metadata, entry points, local install assumptions, public import surface, and MCP entrypoint behavior.
- Documented that PyMuPDF is optional and must not break package imports when missing.

### Known limitations

- Live network adapters are not enabled by default.
- OCR is not complete.
- Advanced PDF layout parsing is not complete.
- Paper draft does not fabricate experiment results.
- Real GPU experiment execution is not included.
- API keys are required only for future live mode.
- `v0.1.0` mainly demonstrates architecture, contracts, dry-run workflow, and local tools.
- Contract-only tools are planned interfaces, not complete live implementations.
- Public release requires final human review.
- TulingResearch Plus does not copy incompatible-license project code.
