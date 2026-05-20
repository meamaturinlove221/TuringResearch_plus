# Lane 10: Release Candidate

## Scope

Round 16 freezes TulingResearch Plus `v0.1.0` public API, MCP tool namespace, contracts, artifact schemas, package structure, and release boundaries.

## Frozen Version

- Version: `v0.1.0`
- Project: TulingResearch Plus
- Packages: `tuling_research`, `tuling_research_plus`
- MCP server: `tulingresearch-plus`

## Included In v0.1.0

- Core local tools
- PDF Markdown Phase A
- Semantic Graph fake adapter / dry-run
- Literature Survey dry-run
- Vault / Context basic capabilities
- Race Mode basics
- Feature Capsule skeleton
- DocFlow
- Figure registry
- Paper draft gate
- Contract tests
- Workflow dry-run tests
- Examples fake mode

## Excluded From v0.1.0

- real network API execution by default
- heavy OCR
- complex PDF layout parsing
- full automatic paper generation
- real GPU experiment execution
- automatic PyPI publishing
- private or unauthorized source idea implementation

## Created Freeze Documents

- `docs/release-freeze.md`
- `docs/api-freeze-v0.1.0.md`
- `docs/tool-namespace-freeze.md`

## Release Candidate Rules

Allowed changes:

- bug fixes
- tests
- naming fixes
- documentation fixes
- contract fixes
- example fixes
- packaging fixes

Blocked changes:

- new major workflow features
- default live API execution
- unreviewed namespace changes
- unreviewed schema changes
- unreviewed package structure changes

## Validation

Release candidate validation must pass:

- `python -m pytest`
- `python -m ruff check .`
- `python -m mypy src`

## Round 17 Name / Import / Contract Audit

Round 17 audited release-candidate naming, imports, MCP namespaces, and contract drift.

Created or updated:

- `docs/name-audit-report.md`
- `docs/import-audit-report.md`
- `docs/contract-drift-report.md`
- `tests/contract/test_name_integrity.py`
- `tests/contract/test_tool_namespace_integrity.py`
- `tests/contract/test_contract_schema_integrity.py`

Findings:

- No forbidden legacy project/package/skill naming remains in scanned `.py`, `.md`, `.yaml`, or `.toml` files.
- Python local import roots are limited to `tuling_research` and `tuling_research_plus`.
- Contracts and `docs/mcp-tools.md` both declare 79 frozen MCP tools.
- Approved namespaces remain `core`, `pdf`, `graph`, `research`, `vault`, `context`, `race`, and `paper`.
- Contract `implementation_status` values now match public tool docs.

## Round 18 MCP Local Smoke Test

Round 18 added the local STDIO smoke surface for `tulingresearch-plus`.

Created or updated:

- `src/tuling_research/mcp_server.py`
- `src/tuling_research/tool_registry.py`
- `docs/mcp-local-smoke-test.md`
- `.codex/config.example.toml`
- `tests/contract/test_mcp_server_import.py`
- `tests/contract/test_mcp_tool_registry.py`
- `tests/contract/test_mcp_stdio_safety.py`

Findings:

- Importing `tuling_research.mcp_server` does not start network services or write stdout/stderr.
- Default module execution writes no stdout logs; human-readable status goes to stderr.
- Explicit `--manifest` and `--health-check` modes write JSON payloads to stdout.
- Minimal tools registered for smoke testing: `core.health_check`, `core.paper_content`, `core.web_content`, `core.session_list`, `pdf.inspect`, `pdf.to_markdown`, and `pdf.markdown_content`.

## Round 19 Examples End-to-End Dry Run

Round 19 made the release examples executable in fake mode or local fixture dry-run mode.

Created or updated:

- `examples/README.md`
- `examples/vggt-human-prior-survey/`
- `examples/smplx-feature-adapter-hypothesis/`
- `examples/citation-graph-demo/`
- `examples/pdf-to-markdown-demo/`
- `tests/workflow/test_example_vggt_human_prior.py`
- `tests/workflow/test_example_smplx_feature_adapter.py`
- `tests/workflow/test_example_citation_graph.py`
- `tests/workflow/test_example_pdf_to_markdown.py`
- `docs/examples.md`

Findings:

- Every example has `input/`, `expected_outputs/`, `README.md`, `fake_run_config.yaml`, and an expected artifact list.
- VGGT survey dry-runs ResearchBrief, LiteratureSurveyArtifact, GapReport, HypothesisPortfolio, and ExperimentPlan.
- SMPL-X adapter hypothesis dry-runs HypothesisPortfolio, IdeaPortfolio, DecisionReport, and StressTestReport.
- Citation graph demo dry-runs CitationGraph, recommended next reads, and frontier nodes through a fake adapter.
- PDF demo dry-runs a generated local fixture PDF, PDFMarkdownOutput, markdown artifact, quality report, and cache hit test.

## Round 20 Packaging / Pyproject / Entry Points

Round 20 validated local package installation metadata and CLI/MCP entry points.

Created or updated:

- `pyproject.toml`
- `README.md`
- `src/tuling_research/__init__.py`
- `src/tuling_research_plus/__init__.py`
- `docs/install.md`
- `docs/package-structure.md`
- `tests/contract/test_package_imports.py`
- `tests/contract/test_entry_points.py`

Findings:

- Distribution name is `tulingresearch-plus`.
- Python requirement is `>=3.11`.
- Package discovery covers `tuling_research*` and `tuling_research_plus*`.
- Console scripts `tulingresearch-plus` and `tulingresearch-plus-mcp` both target `tuling_research.mcp_server:main`.
- Extras are declared for `dev`, `pdf`, `mcp`, and `all`.

## Round 21 CI / Lint / Test Matrix

Round 21 added the release-candidate CI and testing matrix.

Created or updated:

- `.github/workflows/test.yml`
- `.github/workflows/lint.yml`
- `pyproject.toml`
- `docs/testing.md`
- `docs/ci.md`
- `tests/README.md`

Findings:

- CI runs Python 3.11 and 3.12 pytest jobs.
- Ruff is a blocking lint job.
- Mypy runs as optional, non-blocking CI.
- Default pytest skips `live` and `manual` markers.
- Examples run only in fake mode / dry-run mode.
- Default tests require no real API keys and no real network access.

## Round 22 Docs Polish / README Final

Round 22 polished the public release documentation.

Created or updated:

- `README.md`
- `docs/public-readme-draft.md`
- `docs/architecture.md`
- `docs/mcp-tools.md`
- `docs/workflows.md`
- `docs/pdf_markdown.md`
- `docs/race_mode.md`
- `docs/vault.md`
- `docs/examples.md`
- `docs/install.md`
- `docs/testing.md`
- `docs/release-plan.md`
- `docs/faq.md`
- `docs/roadmap.md`

Findings:

- README now covers the project purpose, Python MCP-first design, single-window multi-lane workflow, Core tools, PDF Markdown, survey, semantic graph, Vault, hypothesis-to-experiment flow, Race Mode, Feature Capsules, SOP graphs, paper/figure pipeline, skills, quickstart, examples, safety, roadmap, and references.
- Public docs consistently use TulingResearch Plus, `tuling_research`, `tuling_research_plus`, and `tulingresearch-plus`.
- Reference projects are mentioned only in references/inspiration context.

## Round 23 Release Candidate Report

Round 23 generated the `v0.1.0` release candidate decision report.

Created:

- `docs/release-candidate-report-v0.1.0.md`
- `docs/release-blockers.md`
- `docs/known-limitations.md`
- `docs/security-and-source-hygiene.md`
- `docs/license-review.md`

Findings:

- MCP tools: 79 documented tools across approved namespaces.
- Contracts: 8 contract files covered by schema and drift tests.
- Tests: `python -m pytest` passes with 301 tests.
- Lint: `python -m ruff check .` passes.
- Types: `python -m mypy src` passes.
- Naming: forbidden naming scan has no hits.
- Release blockers: none active.
- Recommendation: GO for `v0.1.0` release preparation.

## Round 24 v0.1.0 Release Prep

Round 24 prepared the `v0.1.0` release materials.

Created or updated:

- `CHANGELOG.md`
- `VERSION`
- `docs/release-notes-v0.1.0.md`
- `docs/v0.1.0-feature-list.md`
- `docs/v0.1.0-limitations.md`
- `docs/v0.1.0-upgrade-plan.md`
- `docs/public-release-checklist.md`

Findings:

- `VERSION` is `0.1.0`.
- `CHANGELOG.md` uses Keep a Changelog headings: Added, Changed, Fixed, Known limitations.
- Feature list covers single-window lanes, contracts-first design, Core local tools, PDF Markdown Phase A, Semantic Graph dry-run, Literature Survey dry-run, Vault/Context, Race Mode, Feature Capsule, DocFlow, SOP, Figure Registry, Paper Draft Gate, QA, and fake-mode examples.
- Limitations clearly record live adapter, OCR, advanced PDF layout, paper writing, GPU execution, human review, and license-reuse limits.

## Status

Release candidate freeze prepared. Round 17 through Round 24 audits completed. No naming, import, contract-drift, local MCP smoke, example dry-run, packaging, CI matrix, docs, release-report, or release-prep blocker is recorded in this lane. Recommendation: GO for `v0.1.0` release preparation after final human review.
