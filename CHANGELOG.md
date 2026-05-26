# Changelog

All notable changes to TuringResearch Plus are documented in this file.

The format follows Keep a Changelog style.

## [1.5.0-rc] - 2026-05-22

### Added

- Docs deployment dry-run.
- Docs navigation polish.
- Split repo manual packs.
- Optional live Scholar/Web/SFTP polish.
- Live safety gate.
- Dashboard landing page.
- Parity showcase view.
- Interview demo view.
- v1.5 full replay.
- v1.5 security/privacy gate.

### Changed

- Package version advanced to `1.5.0rc0`.
- v1.5 release planning now focuses on public externalization while keeping
  v1.4 production parity as the baseline.
- Release docs clarify that public deployment, child repository creation, live
  provider use, and publication remain manual.

### Known limitations

- ARIS remains deferred.
- No public docs deployment is performed.
- No real public URL is written.
- No child repository is created automatically.
- No external push is performed.
- No live provider is run by default.
- No remote command execution is enabled.
- No automatic experiment execution is included.

## [1.4.0-rc] - 2026-05-22

### Added

- Session production parity.
- Session CLI surface.
- Shell script equivalent export.
- Cross-platform archive hardening.
- Remote dry-run plan.
- Return import human confirmation.
- Scholar production parity.
- Paper content/reference/reading E2E.
- Web production parity.
- URL normalization, cache manifest, and content fixtures.
- Apify fake/live report.
- yogsoth production parity.
- Campaign, Research Catalog, Vault Wiki, Ontology, Stress / Convergence, and
  Experiment Runbook E2E demos.
- Parity Dashboard v2.
- v1.4 security/privacy gate and full regression.

### Changed

- Package version advanced to `1.4.0rc0`.
- README and production parity docs now foreground original repo production
  parity while keeping fake/live and privacy boundaries explicit.
- v1.4 release planning keeps ARIS deferred and prioritizes stable production
  parity for the original references.

### Known limitations

- ARIS features remain deferred.
- Remote command execution is not enabled.
- Live SSH/SFTP is not enabled by default.
- Automatic experiment execution is not included.
- Default live networking is not enabled.
- MinerU and heavy OCR are not implemented.
- Final paper automation is not included.

## [1.3.0-rc] - 2026-05-22

### Added

- Full original reference parity scope.
- Session runtime parity with preflight, context pack runtime, fake transfer,
  remote return verifier, workflow replay, and dashboard.
- Optional SFTP transfer runner with fake-first behavior and live opt-in guard.
- Scholar full tool surface for paper searching, content, references, and
  reading plans.
- Web full tool surface for fetching, content, cache, source metadata, and
  optional Apify templates.
- MCP tool parity for v1.3 tool surfaces.
- Campaign execution trace.
- Research Catalog dashboard.
- Vault wiki export demo.
- Ontology runbook demo.
- Stress scenario library.
- Convergence decision report.
- Original parity public demo.
- v1.3 security/privacy gate and full regression.

### Changed

- Package version advanced to `1.3.0rc0`.
- README and parity docs now explain full original-reference parity and ARIS
  deferral more directly.
- v1.3 release planning continues to prioritize stable original parity before
  ARIS runtime study.

### Fixed

- README honesty wording for VGGT and SparseConv3D boundaries was restored for
  legacy public launch tests.

### Known limitations

- ARIS features remain deferred.
- Remote command execution is not enabled.
- Live SSH/SFTP is not enabled by default.
- Automatic experiment execution is not included.
- Default live networking is not enabled.
- Final paper automation is not included.

## [1.2.0-rc] - 2026-05-22

### Added

- Original reference parity strategy.
- Neocortica Session parity for context package safety, archive safety,
  structured return manifests, and platform compatibility notes.
- Neocortica Scholar parity for source priority, tool list export, MCP usage,
  and paper source fallback policy.
- Neocortica Web parity for fake/default web fetching, web content, Apify usage
  guide, cache/source metadata, and no-key graceful skip behavior.
- MCP config parity with fake mode defaults, env block clarity, and optional
  live provider flags.
- Skill SOP parity for priority workflows.
- yogsoth campaign parity with strategy book, preconditions, and review-only
  execution plans.
- Vault/wiki/edge audit parity with wikilinks, backlinks, dangling links, weak
  edge checks, and graph summaries.
- Ontology SOP parity with alias resolution, gap detection, and runbook output.
- Stress test parity for route, claim, artifact, privacy, plugin, and advisor
  risks.
- Experiment execution parity with safe runbooks, artifact requirements, and
  ingest contracts.
- TuringResearch Research Catalog integration.
- Reference Parity Dashboard and v1.2 public demo refresh.
- ARIS deferral roadmap and v1.2 interview pack refresh.

### Changed

- Package version advanced to `1.2.0rc0`.
- v1.2 release planning now prioritizes original-reference parity before ARIS
  study or speculative runtime expansion.
- v1.2 security/privacy and full regression gates now cover the reference
  parity surface.

### Fixed

- v1.2 parity contracts now include release header fields required by contract
  schema integrity checks.

### Known limitations

- ARIS features are deferred.
- MinerU and heavy PDF fallback are not included.
- Remote execution orchestration is not included.
- Automatic experiment execution is not included.
- Default live networking is not enabled.
- Final paper automation is not included.

## [1.1.0-rc] - 2026-05-22

### Added

- Post-v1.0 stabilization and public entry cleanup.
- Split-ready `turingresearch-vggt-case` and `turingresearch-examples` bundles
  prepared for human repository creation review.
- Local-first docs site skeleton and static docs-site builder.
- Read-only localhost dashboard.
- Read-only Dashboard Data API with JSON export.
- Paper writing beta for review-only draft packages.
- Additional public-safe demo cases across robotics, medical imaging, software
  tooling, and multimodal model evaluation planning.
- Case Study Gallery for public-safe cases.
- CI/CD release automation plan.
- GitHub Actions hardening for CI, docs checks, and privacy gate.

### Changed

- Package version advanced to `1.1.0rc0`.
- v1.1 regression coverage now includes docs/dashboard, split-ready bundles,
  paper beta, public demo cases, case gallery, GitHub Actions, privacy/security,
  plugin safety, and v1.0 workflow regressions.
- Docs clarify that split-ready bundles are not published repositories and still
  require human approval.

### Fixed

- Contract headers were normalized for v1.1 docs/dashboard/paper-beta
  contracts.
- Docs-site nav tests now follow the manifest required sections instead of a
  fixed pre-gallery count.

### Known limitations

- No SaaS or cloud user system is included.
- Split repositories still require manual creation.
- Local server dashboard is localhost-only and read-only.
- Paper writing beta requires human review.
- No automatic experiment execution is included.
- Live tests are skipped by default.
- CI does not publish releases automatically.

## [1.0.0-rc] - 2026-05-21

### Added

- Local-first Research OS release-candidate positioning.
- Multi-project workspace, public demo suite, and VGGT public-safe case study.
- Evidence / Artifact / Visual / Advisor review surfaces.
- Paper / Citation / Related Work / Collision Risk surfaces.
- Experiment Route DSL / Hard Gates / Failure Taxonomy.
- Remote Artifact / Handoff / Run Ingest review workflows.
- Dashboard / Advisor Export with optional PDF/PPTX backends.
- Plugin Manifest / Safety / MCP registry and compatibility checks.
- Campaign Catalog and MCP fake-live configuration polish.
- Pod Context Lifecycle Safety Plan.
- Modular monorepo namespace facades and future split strategy.

### Changed

- Package version advanced to `1.0.0rc0`.
- README, quickstart, public demo, split-readiness, and launch docs now reflect
  the v1.0 public launch candidate posture.
- Release documentation now separates feature list, known limitations, test
  summary, upgrade guide, and README update notes.

### Fixed

- Added v1.0 full regression tests and release contract checks.
- Added split execution go/no-go docs that keep physical split out of the v1.0
  prelaunch path.
- Preserved fake/demo boundaries across quickstart, dashboard/export, public
  demo, split-ready bundles, plugin safety, and security/privacy gates.

### Known limitations

- No SaaS or cloud user system is included.
- No automatic experiment execution is included.
- No automatic final paper writing is included.
- Live adapters are optional and disabled by default.
- Plugin execution is restricted.
- Compliance assistant is not legal advice.
- Split repositories are not physically created by default.

## [0.7.0-rc] - 2026-05-21

### Added

- Trusted Local Plugin Loading for local trusted plugin manifests and built-in
  demo plugin metadata without executing plugin code.
- Plugin Sandbox Policy with permission gates, risk reports, and future sandbox
  roadmap.
- Plugin Compatibility Test Harness covering manifest schema, capabilities,
  MCP mapping, safety policy, docs, tests, and forbidden permissions.
- MCP Distribution Polish with safe config examples, tool surface docs, and
  troubleshooting.
- Dashboard Refinement with project cards, evidence/artifact/route/failure
  boards, static search index, and safe demo badges.
- Real Advisor PDF Export and Real Advisor PPTX Export optional paths that
  skip gracefully when local backends are unavailable.
- Export Quality Gate for Advisor Markdown/PDF/PPTX/dashboard outputs.
- Dataset / License Compliance Assistant for datasets, models, papers, code
  repos, usage restrictions, redistribution risk, publication risk, and missing
  license information.
- Local-first Research Vault UI for static browsing of concept, paper, method,
  artifact, claim, failure, and route nodes.
- Paper Deep Review Mode for figure/equation/table checklists, reproduction
  blockers, and claim verification.
- VGGT Public Case Study Builder with redaction and claim-safety reports.
- Public Demo Expansion with VGGT-like, paper survey, and software tooling demo
  projects.

### Changed

- Package version advanced to `0.7.0rc0` for release candidate preparation.
- README and public docs now position TuringResearch Plus as a local-first
  research OS with fake/demo-first defaults, optional live adapters, human
  review requirements, and sensitive-file exclusion.
- v0.7 release docs now separate release notes, feature list, known
  limitations, test summary, README update notes, and upgrade guide.

### Fixed

- Added v0.7 full fake replay covering plugin loading, dashboard/export,
  compliance/vault/case-study, public demo expansion, and v0.6 workflow
  boundaries.
- Added public release RC gate reports and security/privacy final audit.
- Added tests that verify unsafe plugin permissions are blocked, optional
  export backends skip gracefully, public demos do not mark fake results
  observed, and compliance reports do not overclaim legal approval.

### Known limitations

- No SaaS or cloud user system is included.
- Plugin sandboxing is policy-level, not OS-level sandboxing.
- Unknown third-party plugins are disabled.
- PDF/PPTX backends are optional.
- Compliance assistant is not legal advice.
- Paper deep review requires human validation.
- Automatic experiment execution is not included.

## [0.6.0-rc] - 2026-05-21

### Added

- Multi-project Workspace for local project registries, project summaries, and
  Markdown workspace overviews.
- General Research Project Template with reusable template schemas, research
  type templates, and generated placeholder skeletons.
- Cross-project Evidence Graph for JSON / Markdown comparison of claims,
  artifacts, methods, failures, and routes across projects.
- Privacy / Data Policy Layer with safety levels, scanner reports, and
  proposed redaction output.
- Plugin Architecture with manifest-only plugin registry and validation.
- MCP Plugin Registry for mapping reviewed plugin manifests to MCP tool
  declarations without starting a server.
- Tool Capability Manifest for a static catalog of core tools, adapters,
  exporters, workflows, and review surfaces.
- Skill Marketplace Layout for local browsing, categorization, and reference
  of `turingresearch-*` skills.
- Extension Safety Gate for plugin, MCP plugin, skill, and adapter permission
  checks.
- Paper Writing Scaffold plus Method Section Builder, Related Work Draft
  Assistant, Experiment Section Builder, and Paper Assembly Gate.
- Benchmark / Replay Suite covering public demo, VGGT fake replay, demo
  workspace, and paper assembly scenarios.
- Quality / Regression Gate covering docs, contracts, examples, safety,
  fake/live boundaries, privacy gate status, and release readiness.
- v0.6 Documentation Consolidation with docs index, user guide, developer
  guide, architecture overview, and README refresh.

### Changed

- Package version advanced to `0.6.0rc0` for release candidate preparation.
- README now describes v0.6 as local, review-first, fake/default, and
  optional-live.
- v0.6 release docs separate release notes, feature list, limitations, test
  summary, README update notes, and upgrade guide.

### Fixed

- Added v0.6 full fake replay and contract regression checks.
- Added RC gate reports for full tests, mypy, name integrity, privacy gate,
  public demo, docs index, feature accuracy, secret/raw/model safety, fake
  result boundaries, optional live tests, and release blockers.
- Kept paper assembly blocked where real citations, real result tables, final
  abstract, final results, or conclusion would require unsupported evidence.

### Known limitations

- No SaaS product or user system is included.
- No automatic remote experiment execution is included.
- No final paper writing is performed.
- No default live networking is enabled.
- Plugins remain manifest-only unless explicitly enabled by future reviewed
  integrations.
- Paper drafts require human review.
- Privacy scan output is not a legal compliance guarantee.

## [0.5.0-alpha] - 2026-05-21

### Added

- Lightweight Dashboard UI for static HTML / Markdown review dashboards.
- Advisor PDF / PPTX Export Plan with plan-only templates and manifest.
- Project Template Generator for standard research project skeletons.
- MCP / CLI Packaging Polish with CLI reference, MCP reference,
  `.mcp.example.json`, no-secret `.env.example`, and packaging contract tests.
- Public Demo Suite with fake/demo evidence, artifact, visual, related-work,
  advisor, and dashboard examples.
- Real VGGT Dogfooding Replay report from existing local review artifacts.
- v0.5 Alpha Integration Gate covering fake/default workflows.

### Changed

- Package version advanced to `0.5.0a0` for alpha release preparation.
- Release docs now separate static dashboard limits, plan-only advisor export,
  project template skeletons, packaging readiness, public demo boundaries, and
  VGGT replay boundaries.

### Fixed

- Added v0.5 alpha fake end-to-end workflow tests.
- Added v0.5 alpha contract checks.
- Added packaging tests for CLI/MCP entrypoints and no-secret examples.
- Added public demo tests that reject private paths, model files, and
  token-like values.

### Known limitations

- Dashboard is static / lightweight.
- No full SaaS UI is included.
- No real PPTX/PDF generation is performed by default.
- Automatic experiment execution is not included.
- Automatic paper conclusion generation is not included.
- Live adapters remain optional.
- Remote sync remains optional and safety-gated.

## [0.4.0] - 2026-05-21

### Added

- GitHub Artifact Sync with fake/default artifact metadata, selected small-file
  import proposals, live-optional behavior, and safety omissions.
- SSH/SFTP Remote Reader for read-only remote artifact indexes and small review
  files without remote command execution.
- NAS/SMB Shared Store scanner for user-mounted local paths without mount or
  credential handling.
- Cloud Object Artifact Index for provider-neutral S3/R2/OSS/GCS-style object
  manifests without cloud SDK integration.
- Remote Artifact Integration with unified `ArtifactRef` and
  `UnifiedRemoteArtifactReport` outputs across GitHub, SSH/SFTP, shared store,
  and object index sources.
- Modal Run Dashboard for Markdown-first status, candidate, backend, hard gate,
  artifact, visual, failure, next-action, and advisor-readiness views.
- Experiment Board Index and Run Comparison for metadata/report-level
  cross-run comparison.
- Paper Digest / Three-pass Reading Engine with review-required digest outputs
  and method-card bridge.
- Advisor Markdown Export Bundle with source manifest, report source, slide
  outline, figure/table lists, evidence refs, limitations, and next actions.
- v0.4 Integration Gate covering remote artifact, dashboard, paper, advisor,
  and VGGT review flows.

### Changed

- Package version advanced to `0.4.0` for release preparation.
- v0.4 documentation now groups remote artifact safety, dashboard boundaries,
  run comparison boundaries, paper digest limits, and advisor export limits.
- Release docs clarify that remote artifacts are indexed/retrieved, not
  human-verified evidence.

### Fixed

- Added v0.4 fake end-to-end workflow tests.
- Added v0.4 contract checks for review-first and default-off/live-optional
  behavior.
- Added checks that Modal Run Dashboard and Run Comparison do not claim
  SparseConv3D success without real backend evidence.
- Added Advisor Markdown Bundle checks that no PDF/PPTX binary export is
  claimed.

### Known limitations

- Live remote sync is disabled by default.
- No automatic remote command execution is supported.
- TuringResearch does not execute Modal.
- PPTX/PDF export is not implemented yet.
- No UI dashboard is included yet.
- Automatic paper conclusions are not generated.
- No paywall bypass is supported.
- Raw data and SMPL-X model files are not packaged.

## [0.3.0] - 2026-05-20

### Added

- Upstream refresh and v0.3 rescope around active Neocortica split repos.
- Git-based Context Handoff design and Pod Workflow Pack for review-oriented
  context packages and structured output templates.
- Scholar Pipeline Refinement with cache-first source priority, reference
  fallback, cached paper content policy, and three-pass reading plan.
- Web Fetch Adapter and optional Apify Adapter with fake-default behavior,
  source metadata, content hashing, local fixture mode, and live opt-in tests.
- Related Work Positioning Generator for conservative safe claims, unsafe
  claims, paper grouping, and VGGT positioning notes.
- Skill ENTRY / Routing Table with local `turingresearch-*` skill routing
  recommendations.
- Vault Graph Enhancement with typed nodes, typed edges, edge audit, and
  wikilink export.
- Ontology SOPs covering seed-concept-search, source-gathering,
  concept-page-creation, alias-resolution, edge-batch-creation,
  hierarchy-visualization, gap-detection, merge-candidates, confidence-update,
  and ontology-export.
- VGGT Research Knowledge Pack consolidating evidence, artifacts, visual
  readiness, advisor notes, routes, failures, related work, method taxonomy, and
  vault graph review material.
- v0.3 Sprint 1 and Sprint 2 integration gates.

### Changed

- Package version advanced to `0.3.0` for release preparation.
- v0.3 roadmap now prioritizes Git-based context handoff, scholar refinement,
  web retrieval, skill routing, vault graph, and ontology workflows.
- Web and Apify surfaces are implemented as local fake/default adapters with
  live behavior explicitly disabled by default.
- Public release notes now clarify that retrieved web content is not verified
  and related-work positioning requires human paper review.

### Fixed

- Updated package import tests and public import surface tests for `0.3.0`.
- Updated contract tests to reflect that Web Fetch moved from planning to
  `implemented_minimal`.
- Added v0.3 Sprint 2 fake end-to-end tests covering web, related work, skill
  routing, vault graph, and knowledge pack flows.
- Added contract checks for v0.3 Sprint 2 default-off live behavior and
  conservative review boundaries.

### Known limitations

- Live web and Apify adapters are disabled by default and live tests are skipped
  by default.
- Related work positioning requires human paper review.
- Ontology graph output is not final truth.
- Web content is retrieved, not verified.
- No paywall bypass is supported.
- NAS / SSH / GitHub Sync is not implemented yet.
- No full UI is included.
- Automatic paper writing is not included.
- Automatic VGGT experiment execution is not included.

## [0.2.0-beta] - 2026-05-20

### Added

- Live Adapter Contracts with fake-mode defaults and explicit live-test policy.
- Optional Semantic Scholar Live Adapter with default offline behavior.
- Real Citation Graph Expansion with fake, manual, and live-optional modes.
- Paper Collision Risk Detector for conservative overlap, unsafe-claim, and
  safe-claim review.
- Modal / Experiment Run Ingestor for local exported summaries and thin review
  bundles.
- Handoff Bundle Export / Import for controlled cross-machine review packages.
- v0.2 beta integration gate covering paper intelligence, experiment
  intelligence, artifact handoff, advisor inputs, and VGGT route review chains.

### Changed

- Package version advanced to `0.2.0b0` for beta release preparation.
- Beta docs now separate live retrieval, human verification, run ingestion, and
  handoff boundaries.
- MCP docs and contracts now include beta tools for citation graph expansion,
  collision risk detection, run ingest, and handoff bundles.

### Fixed

- Added beta contract checks for live adapter defaults and handoff non-sync
  boundaries.
- Added end-to-end fake beta workflow tests to ensure fake results are not
  promoted to observed evidence.
- Added handoff safety checks that omit raw data, secrets, cache folders, and
  SMPL-X body model files.

### Known limitations

- Live APIs are disabled by default and live tests are skipped by default.
- Citation graph output is not human-verified related work.
- Collision risk requires manual paper review.
- Run ingest does not execute Modal.
- Handoff bundles exclude raw data and SMPL-X model files.
- NAS, SSH, GitHub sync, and cloud artifact stores are not implemented yet.
- OCR heavy pipeline is not complete.
- TuringResearch Plus does not automatically generate final paper conclusions.

## [0.2.0-alpha] - 2026-05-20

### Added

- VGGT/SMPL-X Evidence Ledger for conservative status tracking, evidence refs,
  missing inputs, blockers, and next actions.
- Artifact Auditor for manifest-like local scan indexes, safety flags, omitted
  artifacts, and NPZ header-only summaries.
- Visual Evidence Auditor dry-run surface for missing board proof, visual
  readiness, and not-ready claims.
- Markdown-only Advisor Pack Builder for VGGT / SMPL-X dogfooding summaries.
- PDF Phase B lightweight figure/table extraction, page maps, section trees,
  asset extraction reports, and paper figure registry import.
- Experiment Route DSL for planned VGGT / Modal routes.
- Hard Gate Library for evidence-preserving pass/block/not-enough-evidence /
  human-review validation.
- Failure Taxonomy Engine for VGGT route failure attribution and next actions.
- Paper-to-Method Card workflow for fake/manual paper notes and VGGT mapping.
- Figure-to-Architecture text diagram workflow with Mermaid, DOT, and Markdown
  exports.
- VGGT Modal SparseConv3D Route Pack with route spec, hard gates, failure
  taxonomy, controller prompt, artifact requirements, advisor summary, and
  architecture diagram.
- Sprint 1 and Sprint 2 integration gates, contracts, workflow tests, and
  release-readiness docs.

### Changed

- Package version advanced to `0.2.0a0` for alpha release preparation.
- VGGT dogfooding docs now emphasize SMPL-X feature encoding instead of direct
  replacement.
- Sprint 2 proposed tools remain capsule-local until a future public MCP API
  freeze.
- Release docs now separate route planning, evidence management, and real VGGT
  execution more explicitly.

### Fixed

- Preserved post-rename package imports under `turing_research` and
  `turing_research_plus`.
- Added integration checks that keep route compile distinct from real
  experiment execution.
- Added checks that hard gate validation failures do not imply experiment run
  failures.
- Added checks that paper method fixtures do not claim complete paper reading
  and architecture fixtures remain human-review gated.

### Known limitations

- TuringResearch Plus does not default to network access.
- Live Semantic Scholar adapter is not complete.
- Real citation graph expansion is not complete.
- OCR heavy pipeline is not complete.
- Modal execution is not performed by TuringResearch.
- TuringResearch generates route packs, prompts, and evidence management
  artifacts; it does not replace VGGT experiments.
- Paper Method Card fixtures are not complete paper reviews.
- Architecture diagram fixtures require human review.
- Future Sync Adapters remain non-goal for this alpha.
- Public release and tag creation still require human review.

## [0.1.0] - 2026-05-20

### Added

- Single-window multi-agent lane architecture using `lanes/`, `contracts/`, and `.agents/skills/`.
- Contracts-first MCP tool design for `turingresearch-plus`.
- TuringResearch Core local tools in `turing_research`.
- TuringResearch Plus workflow package in `turing_research_plus`.
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

- Public docs now use the TuringResearch Plus naming system consistently.
- Packaging exposes `turingresearch-plus` and `turingresearch-plus-mcp` entry points.
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
- TuringResearch Plus does not copy incompatible-license project code.
