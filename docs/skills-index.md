# TuringResearch Plus Skills Index



This index locks the repo-scoped skills used by TuringResearch Plus before Release Freeze.



| Skill name | Owner lane | Status | Related contracts | Related modules | Related tests | Release requirement | Notes |

| --- | --- | --- | --- | --- | --- | --- | --- |

| `turingresearch-master-orchestrator` | `lanes/00_master_ledger.md` | locked | `contracts/core_tools.yaml`<br>`contracts/fusion_workflows.yaml`<br>`contracts/race_features.yaml`<br>`contracts/paper_pipeline.yaml` | `lanes/`<br>`contracts/`<br>`docs/` | `tests/contract/test_release_gate_contract.py`<br>`tests/contract/test_skills_integrity.py` | release-critical | locked in Round 15C |

| `turingresearch-architecture-contracts` | `lanes/01_architecture_contracts.md` | locked | `contracts/core_tools.yaml`<br>`contracts/pdf_markdown.yaml`<br>`contracts/fusion_workflows.yaml`<br>`contracts/vault_schema.yaml`<br>`contracts/artifact_schema.yaml`<br>`contracts/race_features.yaml`<br>`contracts/paper_pipeline.yaml`<br>`contracts/error_schema.yaml` | `docs/architecture.md`<br>`docs/mcp-tools.md`<br>`contracts/` | `tests/contract/test_release_gate_contract.py` | release-critical | locked in Round 15C |

| `turingresearch-cache-and-ledger` | `lanes/06_workflow_orchestration.md` | locked | `contracts/core_tools.yaml`<br>`contracts/error_schema.yaml`<br>`contracts/artifact_schema.yaml` | `src/turing_research/cache/`<br>`src/turing_research_plus/budget/`<br>`src/turing_research_plus/ledger/` | `tests/unit/test_cache_keys.py`<br>`tests/unit/test_cache_manager.py`<br>`tests/unit/test_failure_ledger.py`<br>`tests/unit/test_budget_models.py`<br>`tests/unit/test_state_ledger.py` | release-critical | locked in Round 15C |

| `turingresearch-qa-release` | `lanes/09_qa_release.md` | locked | `contracts/core_tools.yaml`<br>`contracts/fusion_workflows.yaml`<br>`contracts/race_features.yaml`<br>`contracts/paper_pipeline.yaml` | `docs/public-release-checklist.md`<br>`docs/public-readme-draft.md`<br>`docs/release-plan.md`<br>`examples/`<br>`tests/contract/`<br>`tests/workflow/` | `tests/contract/test_release_gate_contract.py`<br>`tests/workflow/test_release_examples_fake_mode.py` | release-critical | locked in Round 15C |

| `turingresearch-core-reproduction` | `lanes/02_core_reproduction.md` | locked | `contracts/core_tools.yaml`<br>`contracts/error_schema.yaml` | `src/turing_research/mcp_server.py`<br>`src/turing_research/scholar/`<br>`src/turing_research/web/`<br>`src/turing_research/session/` | `tests/contract/test_core_health_check.py`<br>`tests/unit/test_paper_content_service.py`<br>`tests/unit/test_web_content_service.py`<br>`tests/unit/test_session_registry.py` | release-critical | locked in Round 15C |

| `turingresearch-pdf-markdown-core` | `lanes/03_pdf_markdown.md` | locked | `contracts/pdf_markdown.yaml`<br>`contracts/error_schema.yaml` | `src/turing_research/pdf/`<br>`docs/pdf_markdown.md` | `tests/unit/test_pdf_markdown_models.py`<br>`tests/unit/test_pdf_markdown_pipeline.py`<br>`tests/workflow/test_pdf_to_markdown_demo.py` | release-critical | locked in Round 15C |

| `turingresearch-yogsoth-module-audit` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `docs/yogsoth-module-map.md`<br>`docs/fusion-priority.md`<br>`docs/reuse-boundary.md` | `tests/contract/test_release_gate_contract.py` | planning-required | locked in Round 15C |

| `turingresearch-fusion-campaign-engine` | `lanes/06_workflow_orchestration.md` | locked | `contracts/fusion_workflows.yaml`<br>`contracts/artifact_schema.yaml` | `src/turing_research_plus/campaign/`<br>`src/turing_research_plus/subtask/` | `tests/unit/test_campaign_runner.py`<br>`tests/unit/test_campaign_registry.py`<br>`tests/unit/test_subtask_models.py` | workflow-required | locked in Round 15C |

| `turingresearch-fusion-semantic-graph` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/semantic_graph/` | `tests/unit/test_semantic_graph_models.py`<br>`tests/unit/test_citation_graph.py`<br>`tests/unit/test_author_graph.py`<br>`tests/contract/test_graph_tools_contract.py` | release-critical | locked in Round 15C |

| `turingresearch-fusion-literature-survey` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/survey/` | `tests/unit/test_survey_models.py`<br>`tests/unit/test_survey_depth_gate.py`<br>`tests/unit/test_survey_strategies.py`<br>`tests/unit/test_evidence_matrix.py`<br>`tests/unit/test_gap_extractor.py`<br>`tests/workflow/test_literature_survey_dry_run.py` | release-critical | locked in Round 15C |

| `turingresearch-fusion-north-star` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/north_star/` | `tests/unit/test_north_star_models.py`<br>`tests/unit/test_north_star_service.py`<br>`tests/workflow/test_north_star_dry_run.py` | workflow-required | locked in Round 15C |

| `turingresearch-fusion-deep-insight` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/insight/` | `tests/unit/test_gap_analysis.py`<br>`tests/unit/test_boundary_map.py`<br>`tests/unit/test_sensitivity_probe.py`<br>`tests/unit/test_problem_reformulation.py` | workflow-required | locked in Round 15C |

| `turingresearch-fusion-hypothesis-formation` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/hypothesis/` | `tests/unit/test_hypothesis_models.py`<br>`tests/unit/test_gap_prioritization.py`<br>`tests/unit/test_falsifiability.py`<br>`tests/unit/test_finer.py`<br>`tests/unit/test_hypothesis_portfolio.py` | workflow-required | locked in Round 15C |

| `turingresearch-fusion-creative-ideation` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/ideation/` | `tests/unit/test_idea_models.py`<br>`tests/unit/test_morphological_matrix.py`<br>`tests/unit/test_idea_diversity.py`<br>`tests/unit/test_idea_generation.py` | workflow-required | locked in Round 15C |

| `turingresearch-fusion-convergence` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/convergence/` | `tests/unit/test_candidate_scoring.py`<br>`tests/unit/test_pairwise_ranking.py`<br>`tests/unit/test_feasibility_assessment.py`<br>`tests/unit/test_portfolio_optimize.py`<br>`tests/unit/test_promotion_decide.py` | workflow-required | locked in Round 15C |

| `turingresearch-fusion-stress-test` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/stress/` | `tests/unit/test_claim_red_team.py`<br>`tests/unit/test_hypothesis_debate.py`<br>`tests/unit/test_experiment_premortem.py`<br>`tests/unit/test_counterfactual_probe.py`<br>`tests/unit/test_stress_report.py` | workflow-required | locked in Round 15C |

| `turingresearch-fusion-experiment-execution` | `lanes/04_yogsoth_fusion.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/experiment/` | `tests/unit/test_experiment_models.py`<br>`tests/unit/test_experiment_design.py`<br>`tests/unit/test_constraint_analysis.py`<br>`tests/unit/test_scenario_plan.py`<br>`tests/unit/test_implementation_plan.py`<br>`tests/unit/test_result_schema.py` | workflow-required | locked in Round 15C |

| `turingresearch-fusion-wiki-vault` | `lanes/05_vault_memory.md` | locked | `contracts/vault_schema.yaml`<br>`contracts/artifact_schema.yaml` | `src/turing_research_plus/vault/`<br>`docs/vault.md` | `tests/unit/test_vault_models.py`<br>`tests/unit/test_vault_markdown_io.py`<br>`tests/unit/test_vault_graph.py`<br>`tests/unit/test_vault_lint.py`<br>`tests/unit/test_vault_artifact_ingestion.py` | release-critical | locked in Round 15C |

| `turingresearch-fusion-context-management` | `lanes/05_vault_memory.md` | locked | `contracts/fusion_workflows.yaml`<br>`contracts/artifact_schema.yaml` | `src/turing_research_plus/context/` | `tests/unit/test_context_models.py`<br>`tests/unit/test_context_service.py`<br>`tests/unit/test_context_index.py` | release-critical | locked in Round 15C |

| `turingresearch-fusion-subtask-runtime` | `lanes/06_workflow_orchestration.md` | locked | `contracts/fusion_workflows.yaml` | `src/turing_research_plus/subtask/`<br>`docs/codex-multi-agent.md` | `tests/unit/test_subtask_runner.py`<br>`tests/unit/test_subtask_quality.py`<br>`tests/unit/test_subtask_models.py` | workflow-required | locked in Round 15C |

| `turingresearch-race-source-hygiene` | `lanes/07_race_mode.md` | locked | `contracts/race_features.yaml` | `src/turing_research_plus/race/source_hygiene.py`<br>`docs/race_mode.md` | `tests/unit/test_source_hygiene.py`<br>`tests/contract/test_race_tools_contract.py` | release-critical | locked in Round 15C |

| `turingresearch-race-idea-radar` | `lanes/07_race_mode.md` | locked | `contracts/race_features.yaml` | `src/turing_research_plus/race/idea_radar.py`<br>`race/idea_cards/` | `tests/unit/test_idea_card.py`<br>`tests/unit/test_idea_radar.py`<br>`tests/contract/test_race_tools_contract.py` | release-critical | locked in Round 15C |

| `turingresearch-race-priority-elevator` | `lanes/07_race_mode.md` | locked | `contracts/race_features.yaml` | `src/turing_research_plus/race/priority_elevator.py`<br>`race/priority_board.md` | `tests/unit/test_priority_elevator.py`<br>`tests/contract/test_race_tools_contract.py` | release-critical | locked in Round 15C |

| `turingresearch-race-feature-capsule-factory` | `lanes/07_race_mode.md` | locked | `contracts/race_features.yaml` | `src/turing_research_plus/race/feature_capsule.py`<br>`race/feature_capsules/`<br>`docs/features/`<br>`sop_graphs/feature_graphs/` | `tests/unit/test_feature_capsule.py`<br>`tests/contract/test_race_tools_contract.py` | release-critical | locked in Round 15C |

| `turingresearch-race-architecture-box-builder` | `lanes/07_race_mode.md` | locked | `contracts/race_features.yaml` | `src/turing_research_plus/race/architecture_box.py`<br>`docs/architecture_16box.md` | `tests/unit/test_architecture_box.py` | release-critical | locked in Round 15C |

| `turingresearch-race-upstream-watch` | `lanes/07_race_mode.md` | locked | `contracts/race_features.yaml` | `src/turing_research_plus/race/upstream_watch.py`<br>`race/upstream_reports/` | `tests/unit/test_upstream_watch.py` | release-critical | locked in Round 15C |

| `turingresearch-paper-docflow-article-blocks` | `lanes/08_paper_pipeline.md` | locked | `contracts/paper_pipeline.yaml`<br>`contracts/artifact_schema.yaml` | `src/turing_research_plus/paper/models.py`<br>`src/turing_research_plus/paper/docflow.py`<br>`paper/blocks/` | `tests/unit/test_article_block.py`<br>`tests/unit/test_docflow.py`<br>`tests/contract/test_paper_tools_contract.py` | release-critical | locked in Round 15C |

| `turingresearch-paper-sop-graph-generator` | `lanes/08_paper_pipeline.md` | locked | `contracts/paper_pipeline.yaml` | `src/turing_research_plus/sop/`<br>`sop_graphs/` | `tests/unit/test_sop_graph.py`<br>`tests/unit/test_mermaid_export.py`<br>`tests/contract/test_paper_tools_contract.py` | release-critical | locked in Round 15C |

| `turingresearch-paper-figure-asset-pipeline` | `lanes/08_paper_pipeline.md` | locked | `contracts/paper_pipeline.yaml` | `src/turing_research_plus/paper/figure_registry.py`<br>`src/turing_research_plus/paper/caption_generator.py`<br>`paper/figures/`<br>`paper/captions/`<br>`paper/tables/` | `tests/unit/test_figure_registry.py`<br>`tests/unit/test_caption_generator.py`<br>`tests/contract/test_paper_tools_contract.py` | release-critical | locked in Round 15C |

| `turingresearch-paper-writing-pipeline` | `lanes/08_paper_pipeline.md` | locked | `contracts/paper_pipeline.yaml` | `src/turing_research_plus/paper/paper_writer.py`<br>`src/turing_research_plus/paper/latex_export.py`<br>`paper/draft/` | `tests/unit/test_paper_writer.py`<br>`tests/unit/test_paper_gate.py`<br>`tests/unit/test_latex_export.py`<br>`tests/contract/test_paper_tools_contract.py` | release-critical | locked in Round 15C |
