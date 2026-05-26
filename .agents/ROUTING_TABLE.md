# TuringResearch Skill Routing Table

Status: active.

| Category | Recommended skill | Ranked skills | Lane | Contracts |
| --- | --- | --- | --- | --- |
| upstream watch | `turingresearch-race-upstream-watch` | `turingresearch-race-upstream-watch`, `turingresearch-master-orchestrator` | `lanes/21_upstream_watch_baseline.md` | `contracts/race_features.yaml` |
| VGGT dogfooding | `turingresearch-master-orchestrator` | `turingresearch-master-orchestrator`, `turingresearch-fusion-experiment-execution` | `lanes/14_v0.2_sprint_1.md` | `contracts/vggt_evidence.yaml` |
| evidence ledger | `turingresearch-cache-and-ledger` | `turingresearch-cache-and-ledger`, `turingresearch-master-orchestrator` | `lanes/14_v0.2_sprint_1.md` | `contracts/vggt_evidence.yaml` |
| artifact audit | `turingresearch-cache-and-ledger` | `turingresearch-cache-and-ledger`, `turingresearch-master-orchestrator` | `lanes/14_v0.2_sprint_1.md` | `contracts/artifact_audit.yaml` |
| visual audit | `turingresearch-master-orchestrator` | `turingresearch-master-orchestrator`, `turingresearch-paper-figure-asset-pipeline` | `lanes/14_v0.2_sprint_1.md` | `contracts/visual_evidence.yaml` |
| advisor pack | `turingresearch-paper-writing-pipeline` | `turingresearch-paper-writing-pipeline`, `turingresearch-master-orchestrator` | `lanes/14_v0.2_sprint_1.md` | `contracts/advisor_pack.yaml` |
| PDF extraction | `turingresearch-pdf-markdown-core` | `turingresearch-pdf-markdown-core`, `turingresearch-paper-figure-asset-pipeline` | `lanes/03_pdf_markdown.md` | `contracts/pdf_markdown.yaml` |
| route DSL | `turingresearch-fusion-experiment-execution` | `turingresearch-fusion-experiment-execution`, `turingresearch-master-orchestrator` | `lanes/27_experiment_route_and_hard_gates.md` | `contracts/experiment_route.yaml` |
| hard gates | `turingresearch-fusion-experiment-execution` | `turingresearch-fusion-experiment-execution`, `turingresearch-master-orchestrator` | `lanes/27_experiment_route_and_hard_gates.md` | `contracts/hard_gates.yaml` |
| failure taxonomy | `turingresearch-fusion-stress-test` | `turingresearch-fusion-stress-test`, `turingresearch-master-orchestrator` | `lanes/28_failure_taxonomy_engine.md` | `contracts/failure_taxonomy.yaml` |
| paper method | `turingresearch-paper-writing-pipeline` | `turingresearch-paper-writing-pipeline`, `turingresearch-master-orchestrator` | `lanes/29_paper_to_method_card.md` | `contracts/paper_method_card.yaml` |
| figure architecture | `turingresearch-paper-figure-asset-pipeline` | `turingresearch-paper-figure-asset-pipeline`, `turingresearch-master-orchestrator` | `lanes/30_figure_to_architecture.md` | `contracts/architecture_diagram.yaml` |
| citation graph | `turingresearch-fusion-semantic-graph` | `turingresearch-fusion-semantic-graph`, `turingresearch-master-orchestrator` | `lanes/38_citation_graph_expansion.md` | `contracts/citation_graph.yaml` |
| collision risk | `turingresearch-paper-writing-pipeline` | `turingresearch-paper-writing-pipeline`, `turingresearch-fusion-semantic-graph` | `lanes/39_paper_collision_risk.md` | `contracts/collision_risk.yaml` |
| related work | `turingresearch-paper-writing-pipeline` | `turingresearch-paper-writing-pipeline`, `turingresearch-fusion-semantic-graph` | `lanes/53_related_work_positioning.md` | `contracts/related_work_positioning.yaml` |
| web fetch | `turingresearch-core-reproduction` | `turingresearch-core-reproduction`, `turingresearch-architecture-contracts` | `lanes/52_web_fetch_apify_adapter.md` | `contracts/web_fetch_adapter.yaml`, `contracts/apify_adapter.yaml` |
| handoff | `turingresearch-fusion-context-management` | `turingresearch-fusion-context-management`, `turingresearch-master-orchestrator` | `lanes/41_handoff_bundle.md` | `contracts/handoff_bundle.yaml` |
| pod workflow | `turingresearch-fusion-context-management` | `turingresearch-fusion-context-management`, `turingresearch-master-orchestrator` | `lanes/46_pod_workflow_pack.md` | `contracts/pod_workflow.yaml` |
| vault graph | `turingresearch-fusion-wiki-vault` | `turingresearch-fusion-wiki-vault`, `turingresearch-master-orchestrator` | `lanes/05_vault_memory.md` | `contracts/vault_schema.yaml` |
| ontology | `turingresearch-fusion-wiki-vault` | `turingresearch-fusion-wiki-vault`, `turingresearch-master-orchestrator` | `lanes/05_vault_memory.md` | `contracts/vault_schema.yaml` |

## Round 240 SOP Parity Routes

| Workflow | Recommended skill | Inputs | Outputs | Safety |
| --- | --- | --- | --- | --- |
| master orchestrator | `turingresearch-master-orchestrator` | round request, docs, contracts, tests, lanes | scoped changes, validation, ledger summary | no hidden release or unapproved live/network access |
| upstream watch | `turingresearch-race-upstream-watch` | watch targets, baselines, reports | honest baseline/diff report | no fake diff or code copy |
| campaign catalog | `turingresearch-fusion-campaign-engine` | task description, catalog, preconditions | recommended campaign and skill | advisory only, no runtime execution |
| scholar pipeline | `turingresearch-fusion-literature-survey` | question, papers, cached Markdown, config | source priority, fallback, usage notes | no MinerU/heavy OCR/paywall bypass |
| web fetch | `turingresearch-core-reproduction` | URL/fixture, hygiene status, fake/live flags | fetch/content result and metadata | no default networking, cookies, private fetch, or paywall bypass |
| pod workflow | `turingresearch-fusion-context-management` | context pack, route spec, transfer policy | manifest, preflight, proposed updates | no SSH/tmux/Modal/remote command/git push |
| artifact audit | `turingresearch-cache-and-ledger` | artifact paths, manifests, evidence ledger | audit report and blockers | no raw data, secrets, private paths, or fake observed results |
| advisor pack | `turingresearch-paper-writing-pipeline` | evidence, artifacts, route, related work | advisor pack and missing evidence report | no final paper or fabricated claims |
| release gate | `turingresearch-qa-release` | release scope, tests, docs, policies | go/no-go report and blockers | no auto publish, tag, push, or live tests |
