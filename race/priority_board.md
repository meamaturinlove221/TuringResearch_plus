# TuringResearch Plus Race Priority Board

Idea Radar outputs are staged here after `race.source_hygiene_check` passes or returns documentation-only watch. Implementation work is allowed only when the idea is public or authorized and source hygiene passes.

## Priority Elevator Rules

Formula:

`PriorityScore = 0.30 * value_score + 0.25 * urgency_score + 0.20 * feasibility_score + 0.15 * novelty_score + 0.10 * strategic_fit`

| Level | Action | Rule |
| --- | --- | --- |
| P0 | prototype immediately | score >= 0.85 and source hygiene passed |
| P1 | create feature capsule this sprint | score >= 0.70 and source hygiene passed |
| P2 | document and monitor | score >= 0.45 or source hygiene did not pass |
| P3 | archive | score < 0.45 |

Source hygiene that does not pass forces P0/P1 candidates down to P2.

## v0.2.0 Backlog Priorities

| Priority | Backlog | Candidate work | Owner skill | Source gate | Dependencies |
| --- | --- | --- | --- | --- | --- |
| P0 | BL-04 | API key handling and live test policy | `turingresearch-qa-release` | no real keys in repo | existing pytest live/manual markers |
| P0 | BL-01 | Live Semantic Scholar adapter | `turingresearch-fusion-semantic-graph` | provider public docs and terms | BL-04 |
| P0 | BL-02 | Live arXiv adapter | `turingresearch-core-reproduction` | public arXiv data and terms | BL-04 |
| P0 | BL-05 | PDF figure extraction | `turingresearch-pdf-markdown-core` | local/public fixture PDFs | PDF Phase A |
| P0 | BL-06 | PDF table extraction | `turingresearch-pdf-markdown-core` | local/public fixture PDFs | PDF Phase A |
| P0 | BL-07 | PDF section tree and page map upgrade | `turingresearch-pdf-markdown-core` | local/public fixture PDFs | PDF Phase A |
| P0 | BL-09 | Real citation graph optional expansion | `turingresearch-fusion-semantic-graph` | live adapter opt-in only | BL-01, BL-04 |
| P0 | BL-13 | Stronger Vault search | `turingresearch-fusion-wiki-vault` | local artifacts | existing Vault index |
| P0 | BL-14 | Vault graph traversal improvements | `turingresearch-fusion-wiki-vault` | local artifacts | typed edge schema |
| P1 | BL-03 | Optional Apify web adapter | `turingresearch-core-reproduction` | public web sources only | BL-04 |
| P1 | BL-08 | Better PDF quality report | `turingresearch-pdf-markdown-core` | local/public fixture PDFs | BL-05, BL-06, BL-07 |
| P1 | BL-10 | Literature survey screening upgrade | `turingresearch-fusion-literature-survey` | evidence-backed sources | BL-09 |
| P1 | BL-11 | Evidence matrix upgrade | `turingresearch-fusion-literature-survey` | EvidenceRef required | BL-10 |
| P1 | BL-12 | Gap extraction improvement | `turingresearch-fusion-literature-survey` | EvidenceRef required | BL-11 |
| P1 | BL-15 | Vault artifact ingestion improvements | `turingresearch-fusion-wiki-vault` | local artifacts | BL-11, BL-13 |
| P1 | BL-16 | Upstream watch from public snapshots | `turingresearch-race-upstream-watch` | public snapshots only | Source Hygiene |
| P1 | BL-17 | Better IdeaCard scoring | `turingresearch-race-priority-elevator` | hygiene downgrade rules | existing IdeaCard fields |
| P1 | BL-18 | Feature capsule implementation workflow | `turingresearch-race-feature-capsule-factory` | passed hygiene only | BL-17 |
| P1 | BL-19 | Better figure captions | `turingresearch-paper-figure-asset-pipeline` | figure provenance required | BL-05 |
| P1 | BL-20 | Paper section status upgrade | `turingresearch-paper-docflow-article-blocks` | evidence required | existing DocFlow |
| P1 | BL-21 | Method figure linkage | `turingresearch-paper-writing-pipeline` | required figures present | BL-19, BL-20 |
| P1 | BL-22 | v0.2.0 examples upgrade | `turingresearch-qa-release` | fake mode default | milestone completion |

## Later Roadmap Watch

| Priority | Target | Candidate work | Source gate | Release lane |
| --- | --- | --- | --- | --- |
| P1 | v0.3.0 | OCR pipeline and layout-aware PDF parsing | local PDF fixtures and public sample documents | Lane 03 PDF Markdown |
| P1 | v0.3.0 | Advanced survey, hypothesis-to-experiment polish, optional LLM-assisted convergence and stress checks | adapter protocol only, live providers manual | Lane 04 fusion |
| P2 | v0.3.0 | Source Hygiene dashboard export | internal Race Mode state | Lane 07 race mode |
| P2 | v0.4.0 | Race Mode upstream watch and automated Feature Capsule generation | public-only upstream snapshots | Lane 07 race mode |
| P2 | v0.4.0 | SOP graph UI/export-friendly artifacts and paper figure pipeline polish | internal contracts and paper assets | Lane 08 paper pipeline |
| P2 | v0.4.0 | Assisted paper writing with ExperimentReport hard gate | internal experiment and evidence artifacts | Lane 08 paper pipeline |
| P3 | v1.0.0 | Optional cloud/GPU execution adapters | explicit user configuration only | Future adapter lane |

## Release Gate Notes

- v0.2.0 must not make live network access the default path.
- v0.2.0 live adapters must be optional, adapterized, and tested with mocks by default.
- v0.2.0 PDF extraction must record provenance and warnings.
- Race Mode implementation promotion remains gated by Source Hygiene.
- Later versions must keep OCR, layout parsing, optional LLM, and cloud/GPU work opt-in and quality-gated.

## v0.2.0 Sprint 1 Feature Capsules

Round 37 creates capsule skeletons for the VGGT dogfooding Top 5. These are P0
planning inputs, not implemented features.

| Priority | Capsule | Proposed command | Proposed tool | Status | Dependency |
| --- | --- | --- | --- | --- | --- |
| P0 | `vggt_smplx_evidence_ledger` | `tuling vggt ledger build` | `vggt.evidence_ledger_build` | skeleton | Round 36 scope |
| P0 | `artifact_auditor` | `tuling audit artifact` | `artifact.audit` | skeleton | Evidence Ledger |
| P0 | `visual_evidence_auditor` | `tuling audit visual` | `visual.audit_evidence` | skeleton | Artifact Auditor |
| P0 | `advisor_pack_builder` | `tuling advisor pack` | `advisor.pack_build` | skeleton | Evidence Ledger and auditors |
| P0 | `pdf_phase_b_figure_table_extraction` | `tuling pdf extract-assets` | `pdf.extract_figures`, `pdf.extract_tables` | skeleton | PDF Phase B contracts |

The non-PDF proposed tool namespaces are capsule-local and must not be treated
as public API until a later contracts-first round accepts them.

## Watch Items

- Provider schema and rate-limit changes for scholarly APIs.
- PDF extraction quality across scanned and publisher-formatted documents.
- Evidence continuity across survey, insight, hypothesis, experiment, and paper artifacts.
- License compatibility for any public reference material.

## v0.2.0 Sprint 2 Planning

Round 43 selects the next Sprint 2 candidates from the post-Sprint 1 integration
gate. Sprint 2 should focus on experiment semantics and reusable gates before
live adapters.

| Priority | Candidate | Status | Owner skill | Rationale |
| --- | --- | --- | --- | --- |
| P0 | Hard Gate Library | selected | `turingresearch-master-orchestrator` | Centralizes repeated pass/block/requires-human-review gates. |
| P0 | Experiment Route DSL | selected | `turingresearch-fusion-experiment-execution` | Gives VGGT routes structured, testable execution semantics before ingestion. |
| P0 | Failure Taxonomy Engine | selected | `turingresearch-fusion-stress-test` | Normalizes failures, blockers, regressions, and not-ready claims. |
| P1 | Paper-to-Method Card | selected | `turingresearch-paper-writing-pipeline` | Converts provenance-backed paper/PDF assets into method cards. |
| P1 | Figure-to-Architecture | selected | `turingresearch-paper-figure-asset-pipeline` | Maps extracted figures to architecture drafts without fabricating claims. |
| P2 | Modal Experiment Run Ingestor | deferred | `turingresearch-fusion-experiment-execution` | Should follow route DSL and hard gates. |
| P2 | Live Semantic Scholar adapter | deferred | `turingresearch-fusion-semantic-graph` | Live adapter work remains lower priority than VGGT local evidence semantics. |
| P2 | Real citation graph expansion | deferred | `turingresearch-fusion-semantic-graph` | Depends on live adapter and budget controls. |
| P2 | Vault graph enhancement | deferred | `turingresearch-fusion-wiki-vault` | Useful but not Sprint 2 critical path. |

## v0.2.0 Sprint 2 Feature Capsules

Round 45 created design skeletons for the selected Sprint 2 features. These are
capsule-local planning artifacts until implementation rounds accept contracts.

| Priority | Capsule | Proposed command | Proposed tool | Status | Dependency |
| --- | --- | --- | --- | --- | --- |
| P0 | `hard_gate_library` | `turing gates validate` | `experiment.hard_gate_validate` | skeleton | Sprint 1 evidence statuses |
| P0 | `experiment_route_dsl` | `turing route compile` | `experiment.route_compile` | skeleton | Hard Gate Library |
| P0 | `failure_taxonomy_engine` | `turing failure analyze` | `experiment.failure_analyze` | skeleton | Hard Gate Library and Route DSL |
| P1 | `paper_to_method_card` | `turing paper method-card` | `paper.method_card_extract` | skeleton | PDF Phase B and evidence refs |
| P1 | `figure_to_architecture` | `turing figure arch` | `paper.figure_to_architecture` | skeleton | Method cards and figure registry |

## v0.3.0 Sprint 1 Priority Update

Round 64 shifts the next implementation planning lane to Git-based Context
Handoff / Pod Workflow.

| Priority | Capsule | Proposed command | Proposed tool | Status | Dependency |
| --- | --- | --- | --- | --- | --- |
| P0 | `git_based_context_handoff` | `turing context package` | `context.git_handoff_package` | design_only | v0.2 handoff bundle |
| P0 | `pod_workflow_pack` | `turing pod workflow-pack` | `context.pod_workflow_pack` | implemented_minimal | Git context package and run ingest |

## v0.3.0 Sprint 3 Web Adapter Planning

Round 67 adds design-only planning entries for optional public web retrieval.

| Priority | Capsule | Proposed command | Proposed tool | Status | Dependency |
| --- | --- | --- | --- | --- | --- |
| P1 | `web_fetch_adapter` | `turing web fetch` | `web.fetch`, `web.content` | design_only | live adapter contracts |
| P1 | `apify_adapter` | `turing web apify-run` | `web.apify_run_optional` | design_only | web fetch adapter |

## v0.3.0 Sprint 2 Selection

Round 69 selects the next implementation focus after the v0.3 Sprint 1
integration gate.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | Web Fetch Adapter / Apify Adapter implementation | selected | Closes the public project-page and README retrieval gap. |
| P0 | Related Work Positioning Generator | selected | Converts method cards, citation graph, and collision risk into conservative positioning. |
| P1 | Skill ENTRY.md / Routing Table | selected | Makes skill and lane routing explicit and auditable. |
| P1 | Vault Graph Enhancement | selected | Strengthens evidence-backed graph storage and traversal. |
| P1 | Knowledge Graph / Wiki / Ontology SOPs | selected | Adds graph maintenance SOPs aligned with upstream learning. |
| P2 | Modal Run Dashboard | deferred | Needs stable run ingestion and UI scope first. |
| P2 | Advisor Pack richer export | deferred | PDF/PPTX export is useful but not the next bottleneck. |
| P3 | NAS / SMB Shared Artifact Store | deferred | Sync adapters remain non-goal for this sprint. |
| P3 | SSH / SFTP Remote Artifact Reader | deferred | Sync adapters remain non-goal for this sprint. |
| P3 | GitHub Artifact Sync | deferred | Sync adapters remain non-goal for this sprint. |

## v0.3.0 Sprint 2 Scope Lock

Round 70 locks the selected Sprint 2 items into feature capsules. The capsules
are planning artifacts until implementation rounds promote their draft
contracts and tests.

| Priority | Capsule | Proposed command | Proposed tool | Status | Dependency |
| --- | --- | --- | --- | --- | --- |
| P0 | `web_fetch_adapter` | `turing web fetch` | `web.fetch` | scope_locked | live adapter contracts |
| P0 | `apify_adapter` | `turing web apify-run` | `web.apify_run_optional` | scope_locked | web fetch adapter |
| P0 | `related_work_positioning` | `turing paper position` | `paper.related_work_position` | scope_locked | method cards, citation graph, collision risk |
| P1 | `skill_entry_routing` | `turing skills route` | `skills.route_query` | scope_locked | skills index, lanes, contracts |
| P1 | `vault_graph_ontology` | `turing vault graph-audit` | `vault.graph_audit` | scope_locked | vault schema and evidence refs |

## v0.4.0 Planning

Round 78 selects v0.4 candidates after v0.3 release prep. The current default
recommendation assumes the VGGT mainline still needs cross-machine and remote
GPU artifact return.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | GitHub Artifact Sync | recommended | Extends Git-based context handoff and handoff bundles for structured artifact return. |
| P0 | SSH / SFTP Remote Artifact Reader | recommended | Useful for remote GPU/pod outputs, but must remain read-only and fake-default first. |
| P0 | Modal Run Dashboard | recommended | Makes route/run status inspectable from structured outputs without running Modal. |
| P1 | Advisor Pack PDF / PPTX Export | recommended | Improves advisor communication once evidence boundaries are stable. |
| P1 | Paper Digest / Three-pass Reading Expansion | recommended | Strengthens writing workflow while preserving human paper review. |
| P1 | Related Work Positioning Refinement | alternate writing-first | Moves to P0 if the next sprint shifts toward paper writing. |
| P1 | Paper Collision Risk Deep Review | alternate writing-first | Useful for novelty/positioning review after more paper digests exist. |
| P2 | NAS / SMB Shared Artifact Store | deferred | Higher environment risk; consider after GitHub/SSH patterns mature. |
| P2 | Lightweight UI / Dashboard | deferred | Keep report-first until dashboard scope is stable. |
| P3 | Cloud Object Storage Adapter | deferred | Highest credential/storage governance risk; not Sprint 1. |

## v0.5.0 Scope Lock

Round 91 selects the next productization and public-release hardening direction
after v0.4 release prep.

| Priority | Capsule | Status | Rationale |
| --- | --- | --- | --- |
| P0 | `project_template_generator` | scope_locked | Generic templates reduce setup friction and prevent VGGT-specific leakage into new projects. |
| P0 | `packaging_polish` | scope_locked | CLI/MCP/package consistency is needed before public demos and UI work. |
| P0 | `public_demo_suite` | scope_locked | A curated fake/default demo gives public users a safe end-to-end path. |
| P1 | `lightweight_dashboard_ui` | scope_locked | Local UI should render stable v0.4 review artifacts without becoming SaaS. |
| P1 | `advisor_pdf_pptx_export` | scope_locked | Binary advisor exports should follow Markdown bundle boundaries. |
| P1 | `vggt_dogfooding_replay` | scope_locked | Real VGGT replay should come after templates, demos, and export boundaries are stable. |

## v0.5.0 Beta Planning

Round 100 selects beta priorities after v0.5 alpha release prep. The beta should
stabilize public-facing alpha capabilities before expanding into larger plugin
or live-replay systems.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | Public Release Hardening | recommended | Required before broader public use; checks docs, examples, package metadata, and safety boundaries. |
| P0 | Real PPTX/PDF Export | recommended | Converts advisor plans into optional binary exports while preserving limitations. |
| P1 | Dashboard refinement | recommended | Improves usability while staying static/lightweight. |
| P1 | MCP installation flow | recommended | Makes local install and MCP configuration easier to verify. |
| P1 | Benchmark/demo test suite | recommended | Gives public users a stable fake/default validation path. |
| P2 | Documentation polish | supporting | Fold into release hardening unless it becomes large enough for its own lane. |
| P2 | More public demos | supporting | Add only curated demos that preserve no-secret/no-raw-data boundaries. |
| P2 | Community contribution guide | defer | Useful after public hardening is stable. |

## v1.6.0 Public Release Execution Pack

Round 361 locks v1.6 as public release execution readiness rather than feature
expansion.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | Docs deployment ready | scope_locked | The v1.5 dry-run exists; v1.6 should make it reviewable for real public docs deployment without auto-deploying. |
| P0 | GitHub Pages-ready workflow | scope_locked | Maintainers need a manual, approval-gated path for docs publication. |
| P0 | Package / install readiness | scope_locked | Public release credibility depends on install, import, CLI, and metadata checks. |
| P0 | Release artifact build | scope_locked | Artifacts should be reproducible and scanned before any PyPI decision. |
| P0 | Public launch checklist | scope_locked | Release actions must remain manual and auditable. |
| P1 | Split repo manual execution pack | scope_locked | Existing manual packs need final review support before any child repo creation. |
| P1 | Optional live smoke ready | scope_locked | Live remains private, opt-in, skipped by default, and credential-gated. |
| P1 | Screenshot / demo asset pack | scope_locked | Public showcase needs assets that are demo-safe and claim-safe. |
| P1 | v1.6 full regression | scope_locked | v1.6 must protect v1.4 production parity and v1.5 public externalization surfaces. |
| P2 | v1.7 roadmap | scope_locked | Next-stage choices should be planned after release readiness, not mixed into v1.6. |
| P3 | ARIS implementation | deferred | ARIS remains future-study only and must not enter v1.6 implementation. |
| P3 | Plugin architecture | defer | Too broad for beta unless separately scoped. |
| P3 | Real VGGT replay with new artifacts | blocked until artifacts | Requires actual new artifacts; must not be simulated. |

## v0.6.0 Scope Lock

Round 103 locks v0.6 as the Research OS / multi-project / plugin-readiness
scope. Implementation should begin with workspace foundations before plugin or
marketplace surfaces.

| Priority | Capsule | Status | Rationale |
| --- | --- | --- | --- |
| P0 | `multi_project_workspace` | scope_locked | Required foundation for multiple research projects and workspace dashboards. |
| P0 | `general_research_project_template` | scope_locked | Generalizes the VGGT project package without carrying VGGT-specific claims. |
| P0 | `cross_project_evidence_graph` | scope_locked | Enables reusable pattern discovery while keeping evidence project-scoped. |
| P0 | `privacy_data_policy` | scope_locked | Needed before cross-project dashboards, public examples, or plugin exposure. |
| P1 | `plugin_architecture` | scope_locked | Defines extension boundaries after workspace safety is clear. |
| P1 | `mcp_plugin_registry` | scope_locked | Prepares MCP metadata and compatibility checks without marketplace publishing. |
| P1 | `tool_capability_manifest` | scope_locked | Gives routing, docs, and plugin surfaces a unified capability index. |
| P1 | `skill_marketplace_layout` | scope_locked | Documents skill packaging layout without automatic install/runtime behavior. |
| P2 | `paper_writing_scaffold` | scope_locked | Adds claim-checked outlines, not final paper prose. |
| P2 | `benchmark_replay_suite` | scope_locked | Strengthens fake/default demos and replay validation without real result claims. |

## v0.7.0 Scope Lock

Round 127 locks v0.7 as controlled public-readiness work: trusted local plugin
loading, sandbox policy, distribution polish, dashboard/export refinement,
dataset/license review assistance, local-first vault UI planning, paper deep
review, VGGT public case study preparation, and public release RC gating.

| Priority | Capsule | Status | Rationale |
| --- | --- | --- | --- |
| P0 | `trusted_local_plugin_loading` | scope_locked | Enables reviewed local plugins without unknown third-party execution. |
| P0 | `plugin_sandbox_policy` | scope_locked | Required safety layer before any runtime plugin expansion. |
| P0 | `plugin_compatibility_harness` | scope_locked | Tests plugin manifests and compatibility without executing unsafe code. |
| P0 | `mcp_distribution_polish` | scope_locked | Improves install, smoke tests, config examples, and MCP readiness. |
| P1 | `dashboard_refinement` | scope_locked | Makes static dashboards more useful without creating SaaS scope. |
| P1 | `advisor_real_pdf_export` | scope_locked | Adds optional PDF adapter path after advisor bundle boundaries. |
| P1 | `advisor_real_pptx_export` | scope_locked | Adds optional PPTX adapter path with slide mapping and no fake charts. |
| P1 | `dataset_license_compliance` | scope_locked | Provides review aid for data/license risk without legal guarantees. |
| P2 | `local_first_research_vault_ui` | scope_locked | Explores local UI after privacy and dashboard safety boundaries. |

## v1.3.0 Full Original Parity Scope

Round 259 locks v1.3 around full original parity rather than ARIS
implementation. The next work should make the v1.2 structural parity surfaces
more runnable, traceable, and demoable.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | Neocortica Session runtime parity | scope_locked | Makes context handoff and structured return parity runnable without default remote execution. |
| P0 | Neocortica Scholar full tool surface parity | scope_locked | Aligns source priority, tool list, MCP usage, and fallback behavior into a fuller fake/default surface. |
| P0 | Neocortica Web full tool surface parity | scope_locked | Aligns web_fetching, web_content, Apify optional guidance, cache, and source metadata without default networking. |
| P0 | MCP / SKILL / README parity | scope_locked | Ensures config, skill SOPs, and public docs point to the same runnable fake path. |
| P1 | yogsoth Campaign execution trace | scope_locked | Shows deterministic campaign trace without agent runtime overreach. |
| P1 | yogsoth Vault / Ontology / Wiki demo | scope_locked | Makes graph/wiki/ontology parity visible as public-safe demo material. |
| P1 | yogsoth Stress / Convergence / Experiment runbook parity | scope_locked | Connects stress findings to convergence and runbook requirements without real execution. |
| P1 | Full original parity replay | scope_locked | Provides end-to-end fake replay for original parity. |
| P2 | Public parity dashboard refresh | scope_locked | Keeps public status clear for complete, partial, deferred, and rejected items. |
| P2 | v1.3 release prep | scope_locked | Closes v1.3 with release notes, tests, limitations, and handoff. |

ARIS remains deferred from this implementation line.

## v1.4.0 Original Repo Production Parity

Round 291 adjusts v1.4 away from ARIS study prototypes and toward original repo
production parity. The latest human upstream scan indicates the stable
reference work remains centered on Session, Scholar, Web, and yogsoth research
engine production surfaces.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | Neocortica Session production parity | scope_locked | Hardens Git context, pod deployment planning, dotfile handling, shell safety, and cross-platform archive behavior without default remote execution. |
| P0 | Neocortica Scholar production parity | scope_locked | Aligns MCP config, paper_content, paper_reference, paper_reading, SKILL.md, README tool list, and arxiv2md fallback policy. |
| P0 | Neocortica Web production parity | scope_locked | Aligns Apify, web_fetching, web_content, cache, MCP config, and dotenv removal while keeping live networking opt-in. |
| P0 | yogsoth research engine production parity | scope_locked | Makes campaign, vault, ontology, stress, convergence, and experiment runbook surfaces replayable without agent runtime overreach. |
| P1 | full original repo production replay | scope_locked | Provides a release-quality fake/default replay across all original parity surfaces. |
| P1 | parity dashboard v2 | scope_locked | Makes complete, partial, deferred, rejected, and production-ready status visible. |
| P1 | README / docs production polish | scope_locked | Clarifies original repo production parity, fake/live boundaries, privacy defaults, and ARIS deferral. |
| P0 | v1.4 release prep | scope_locked | Closes v1.4 with release notes, limitations, regression, and manual release docs. |

ARIS remains deferred from the v1.4 implementation line.

## v1.5.0 Public Externalization Scope Lock

Round 331 locks v1.5 as Public Externalization after v1.4 original repo
production parity and final handoff. The implementation line should make the
project easier to publish, review, split, demo, and optionally exercise in
private live mode while keeping ARIS deferred.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | public docs deployment prep | scope_locked | Public docs are the highest-value next externalization step after v1.4 release prep. |
| P0 | docs site build hardening | scope_locked | Deployment prep needs reliable nav/build/link checks before public exposure. |
| P0 | physical split execution pack | scope_locked | Split repositories require manual packs and privacy gates before creation. |
| P0 | vggt-case repo manual pack | scope_locked | First public-safe case repo candidate, still manual and approval-gated. |
| P1 | examples repo manual pack | scope_locked | Useful after case pack readiness confirms the split pattern. |
| P1 | optional live Scholar/Web/SFTP polish | scope_locked | Improves opt-in ergonomics while keeping live behavior skipped by default. |
| P1 | dashboard UX showcase | scope_locked | Makes production parity and public demos easier to inspect. |
| P0 | v1.5 full replay | scope_locked | Confirms public externalization surfaces remain fake/default and safe. |
| P0 | v1.5 release prep | scope_locked | Closes v1.5 with release notes, limitations, test summary, and manual release docs. |
| P1 | v1.6 roadmap | scope_locked | Decides whether ARIS returns as study-only after v1.5. |

ARIS remains deferred from the v1.5 implementation line.
| P2 | `paper_deep_review_mode` | scope_locked | Improves citation-grade review while requiring human paper reading. |
| P2 | `vggt_public_case_study` | scope_locked | Prepares dogfooding case study without unsupported experiment claims. |
| P0 | `public_release_candidate_gate` | scope_locked | Final v0.7 release gate for safety, docs, tests, and public posture. |

## v0.8.0 Roadmap

Round 149 plans v0.8 after v0.7 release prep. The recommendation is to improve
daily local usability first, then expand paper assistance and public extension
metadata while keeping plugin execution, private data, live networking, and
final paper conclusions gated.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | Local server dashboard | recommended | Highest usability gain after v0.7 static dashboards; must remain local-first with static fallback. |
| P0 | Research paper writing beta | recommended | Builds on scaffold/method/related-work/experiment gates without generating final conclusions. |
| P0 | Public plugin registry draft | recommended | Natural next step after manifests, compatibility harness, sandbox policy, and MCP polish. |
| P1 | More case studies | recommended | Improves public understanding if examples stay demo-safe or evidence-reviewed. |
| P1 | Real OS-level plugin sandbox research | recommended | Required research before any unknown third-party plugin execution can be considered. |
| P1 | Real PPTX/PDF polish | supporting | Optional export paths exist; polish should preserve graceful skip and quality gates. |
| P1 | Dataset/license compliance expansion | supporting | Useful for public case studies, but remains review aid rather than legal advice. |
| P1 | MCP marketplace polish | supporting | Should follow registry metadata and compatibility labels without automatic install. |
| P2 | Multi-project analytics | deferred | Needs local dashboard foundation and evidence-transfer safeguards first. |
| P2 | Collaboration workflow | deferred | Needs privacy-first review semantics before any broader collaboration surface. |

## v1.1.0 Roadmap

Round 199 plans v1.1 after the v1.0 public-launch candidate. The recommendation
is to turn the public launch into a clearer product surface while keeping the
main repository as the flagship.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | `turingresearch-vggt-case` physical split | recommended | Safest first spoke after human approval; strong dogfooding story without moving core runtime. |
| P0 | Public documentation site | recommended | Improves public navigation and lowers README load after launch. |
| P1 | Local server dashboard | recommended | Highest local usability gain, provided static fallback and no-SaaS boundaries remain. |
| P1 | Research paper writing beta | recommended | Builds on evidence, method, related-work, and claim gates without generating final papers. |
| P1 | More public demos | recommended | Helps users understand workflows if every demo remains public-safe and fake/demo-first. |
| P2 | `turingresearch-examples` physical split | second split candidate | Useful after the case repo validates the spoke pattern and sync policy. |
| P2 | Plugin ecosystem expansion | gated | Requires real contributor demand, review capacity, and no unsafe execution path. |
| P2 | Real web live mode polish | gated | Useful only with explicit opt-in and no real keys in repo. |
| P2 | More compliance helpers | supporting | Helps public cases while remaining review aid rather than legal advice. |
| P2 | CI/CD release polish | supporting | Reduces release friction after branch and worktree discipline are clarified. |

## v1.1.0 Scope Lock

Round 205 locks v1.1 as a post-v1 stabilization and public-surface improvement
release. The first step is baseline stabilization because v1.0 is documented as
a planning baseline, not a verified public release baseline.

| Priority | Workstream | Status | Rationale |
| --- | --- | --- | --- |
| P0 | v1.0 baseline stabilization | scope_locked | Required before split, docs-site, dashboard, or release-candidate execution. |
| P0 | `turingresearch-vggt-case` split-ready finalization | scope_locked | First public-safe spoke after human approval. |
| P0 | Public documentation site | scope_locked | Best public onboarding improvement after baseline cleanup. |
| P1 | `turingresearch-examples` split-ready finalization | scope_locked | Second spoke after case repo path is validated. |
| P1 | Local server dashboard | scope_locked | Local-first usability improvement with static fallback and no SaaS scope. |
| P1 | Paper writing beta | scope_locked | Reviewable beta scaffolds only, not final paper generation. |
| P1 | More public demo cases | scope_locked | Public-safe demos to improve understanding without result claims. |
| P1 | Case study gallery | scope_locked | Organizes public-safe case studies without overclaiming. |
| P1 | CI/CD release hardening | scope_locked | Reduces branch/release friction without automatic publishing. |
| P0 | v1.1 release candidate | scope_locked | Final integration, regression, privacy/security, and release docs gate. |

## v1.2.0 Roadmap

Round 230 plans v1.2 as ecosystem execution rather than additional
documentation stacking. The focus is real public touchpoints, local usability,
and safety-first lifecycle tooling.

| Priority | Candidate | Status | Rationale |
| --- | --- | --- | --- |
| P0 | `turingresearch-vggt-case` physical split execution | recommended | Safest first public child repo after human approval; preserves flagship install path. |
| P0 | `turingresearch-examples` physical split execution | recommended after case | Public demo/template mirror after the spoke sync pattern is validated. |
| P0 | Public docs deployment | recommended | Converts local docs-site builder into a public navigation surface after safety checks. |
| P1 | Local server dashboard polish | recommended | High daily usability value while remaining localhost-only and read-only. |
| P1 | Pod Lifecycle Manager | recommended prototype | Local lifecycle checks and metadata validation without remote execution. |
| P1 | Paper writing beta refinement | recommended | Better review-only drafts, evidence links, and guards without final paper generation. |
| P2 | Real web / scholar live mode polish | gated | Useful only with explicit opt-in, no keys in repo, and fake tests as default. |
| P2 | Apify workflow templates | gated | Template/demo-only until live adapter policy and cost controls are clear. |
| P2 | Context Return Verifier | supporting | Validate structured return metadata before proposed updates are reviewed. |
| P2 | More case studies | supporting | Add only public-safe or redacted cases with no unsupported claims. |
| P3 | MinerU / heavy PDF fallback research | research_only | Dependency-heavy; not a default PDF path. |
| P3 | OS-level plugin sandbox research | research_only | Required before unknown plugin execution, but not a v1.2 default runtime promise. |

## v1.2.0 Scope Lock - Original Reference Parity First

Round 231 narrows v1.2 execution: finish stable original-reference parity before
chasing ARIS-style research-loop features. ARIS is valuable, but it moves to a
v1.3 study roadmap or later.

| Priority | Workstream | Status | Rationale |
| --- | --- | --- | --- |
| P0 | Upstream strict diff | scope_locked | Required before claiming parity or adopting new upstream ideas. |
| P0 | MCP config parity | scope_locked | Aligns fake/live config, env block, and MCP examples with stable reference patterns. |
| P0 | Neocortica-Session parity | scope_locked | Context lifecycle, preflight, transfer, return verification, and safety checks without remote execution. |
| P0 | Neocortica-Scholar parity | scope_locked | Scholar pipeline/config/source fallback parity without heavy PDF default runtime. |
| P0 | Neocortica-Web parity | scope_locked | Optional web/live adapter parity while keeping fake mode default. |
| P0 | yogsoth campaign / vault / ontology parity | scope_locked | Campaign catalog, vault graph, ontology SOP, stress-test, and experiment-planning continuity. |
| P1 | Skill SOP parity | scope_locked | Makes skill routing and SOP handoffs explicit and testable. |
| P1 | Public demo refresh | scope_locked | Keeps demos broad, fake/default, privacy-safe, and not VGGT-only. |
| P0 | v1.2 full regression | scope_locked | Final gate over v1.0, v1.1, and v1.2 surfaces. |
| P1 | v1.3 ARIS study roadmap | scope_locked | Captures ARIS cross-model review, meta-optimize, proof-checker, and paper-writing automation as future study. |

## ARIS Deferral Decision

Round 233 locks ARIS out of the v1.2 implementation line. Round 291 keeps ARIS
as a future reference and confirms it is still deferred from v1.4 implementation.

| Priority | ARIS item | Status | Rationale |
| --- | --- | --- | --- |
| P2 | cross-model review loop | deferred_not_v1.2 | Requires design and safety review to avoid false authority and agent-runtime overreach. |
| P2 | claim audit | deferred_not_v1.2 | Useful future review aid, but must not become proof or final claim generation. |
| P2 | result-to-claim verification | deferred_not_v1.2 | Needs evidence semantics design before any runtime adoption. |
| P2 | experiment audit | deferred_not_v1.2 | Must not imply automatic experiment success. |
| P3 | proof checker | deferred_not_v1.2 | High risk of overstating correctness. |
| P2 | paper compile audit | deferred_not_v1.2 | Needs boundaries against final paper automation. |
| P3 | meta-optimize | deferred_not_v1.2 | Opaque optimization is too risky before parity baseline. |
| P3 | effort levels | deferred_not_v1.2 | Requires clear budget/quality semantics. |
| P3 | session stop hook | deferred_not_v1.2 | Lifecycle side effects require design. |
| P3 | paper resubmit pipeline | deferred_not_v1.2 | Must not become automatic paper-writing/resubmission machinery. |
