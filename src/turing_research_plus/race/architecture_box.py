"""16-Box Architecture Builder for TuringResearch Plus."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ArchitectureBox(BaseModel):
    """One independently plannable architecture box."""

    model_config = ConfigDict(extra="forbid")

    box_id: int = Field(ge=1, le=16)
    name: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    owner_skill: str = Field(min_length=1)
    public_tools: list[str] = Field(default_factory=list)
    internal_modules: list[str] = Field(min_length=1)
    input_artifacts: list[str] = Field(default_factory=list)
    output_artifacts: list[str] = Field(default_factory=list)
    tests: list[str] = Field(min_length=1)
    priority: str = Field(min_length=1)
    dependencies: list[int] = Field(default_factory=list)


class ArchitectureBoxBuildResult(BaseModel):
    """16-box architecture build output."""

    model_config = ConfigDict(extra="forbid")

    boxes: list[ArchitectureBox] = Field(min_length=16, max_length=16)
    mermaid_graph: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_dependencies(self) -> ArchitectureBoxBuildResult:
        box_ids = {box.box_id for box in self.boxes}
        if len(box_ids) != 16:
            raise ValueError("16 unique architecture boxes are required")
        for box in self.boxes:
            for dependency in box.dependencies:
                if dependency not in box_ids:
                    raise ValueError(f"box {box.box_id} has orphan dependency {dependency}")
        return self


def build_architecture_boxes() -> ArchitectureBoxBuildResult:
    """Build the default TuringResearch Plus 16-box architecture."""

    boxes = _default_boxes()
    return ArchitectureBoxBuildResult(
        boxes=boxes,
        mermaid_graph=build_mermaid_graph(boxes),
    )


def race_architecture_box_build() -> dict[str, object]:
    """Thin race.architecture_box_build wrapper."""

    return build_architecture_boxes().model_dump(mode="json")


def build_mermaid_graph(boxes: list[ArchitectureBox]) -> str:
    """Generate a Mermaid dependency graph."""

    lines = ["flowchart TD"]
    for box in boxes:
        lines.append(f"    B{box.box_id:02d}[\"{box.box_id}. {box.name}\"]")
    for box in boxes:
        for dependency in box.dependencies:
            lines.append(f"    B{dependency:02d} --> B{box.box_id:02d}")
    return "\n".join(lines) + "\n"


def _default_boxes() -> list[ArchitectureBox]:
    return [
        ArchitectureBox(
            box_id=1,
            name="Idea Radar",
            goal="Extract public or authorized Race Mode ideas from noisy text.",
            owner_skill="turingresearch-race-idea-radar",
            public_tools=["race.idea_extract"],
            internal_modules=["src/turing_research_plus/race/idea_radar.py"],
            input_artifacts=["SourceMaterial"],
            output_artifacts=["IdeaCard"],
            tests=["tests/unit/test_idea_radar.py"],
            priority="P0",
            dependencies=[3],
        ),
        ArchitectureBox(
            box_id=2,
            name="Priority Elevator",
            goal="Rank IdeaCards into P0/P1/P2/P3 for release planning.",
            owner_skill="turingresearch-race-priority-elevator",
            public_tools=["race.priority_score"],
            internal_modules=["src/turing_research_plus/race/priority_elevator.py"],
            input_artifacts=["IdeaCard"],
            output_artifacts=["PriorityRecommendation"],
            tests=["tests/unit/test_priority_elevator.py"],
            priority="P0",
            dependencies=[1, 3],
        ),
        ArchitectureBox(
            box_id=3,
            name="Source Hygiene",
            goal="Block private, leaked, NDA, proprietary, or incompatible sources.",
            owner_skill="turingresearch-race-source-hygiene",
            public_tools=["race.source_hygiene_check"],
            internal_modules=["src/turing_research_plus/race/source_hygiene.py"],
            input_artifacts=["SourceMaterial"],
            output_artifacts=["SourceHygieneCheckResult"],
            tests=["tests/unit/test_source_hygiene.py"],
            priority="P0",
        ),
        ArchitectureBox(
            box_id=4,
            name="Upstream Watch",
            goal="Track public upstream changes without converting unclear sources to tasks.",
            owner_skill="turingresearch-race-upstream-watch",
            public_tools=["race.upstream_watch"],
            internal_modules=["src/turing_research_plus/race/upstream_watch.py"],
            input_artifacts=["SourceHygieneCheckResult"],
            output_artifacts=["UpstreamWatchReport"],
            tests=["tests/unit/test_upstream_watch.py"],
            priority="P2",
            dependencies=[3],
        ),
        ArchitectureBox(
            box_id=5,
            name="Feature Capsule",
            goal="Turn P0/P1 IdeaCards into self-contained feature capsule skeletons.",
            owner_skill="turingresearch-race-feature-capsule-factory",
            public_tools=["race.feature_capsule_create"],
            internal_modules=["src/turing_research_plus/race/feature_capsule.py"],
            input_artifacts=["IdeaCard", "PriorityRecommendation"],
            output_artifacts=["FeatureCapsule"],
            tests=["tests/unit/test_feature_capsule.py"],
            priority="P1",
            dependencies=[1, 2, 3],
        ),
        ArchitectureBox(
            box_id=6,
            name="SOP Graph",
            goal="Represent feature and workflow procedures as Mermaid SOP graphs.",
            owner_skill="turingresearch-paper-sop-graph-generator",
            public_tools=["paper.sop_graph_generate"],
            internal_modules=["sop_graphs/feature_graphs/"],
            input_artifacts=["FeatureCapsule"],
            output_artifacts=["SOPGraph"],
            tests=["tests/unit/test_sop_graph.py"],
            priority="P1",
            dependencies=[5],
        ),
        ArchitectureBox(
            box_id=7,
            name="Core Paper Tools",
            goal="Expose local paper content and future paper services through Core.",
            owner_skill="turingresearch-core-reproduction",
            public_tools=["core.paper_content", "core.paper_searching", "core.paper_fetching"],
            internal_modules=["src/turing_research/scholar/"],
            input_artifacts=["PaperContentRequest"],
            output_artifacts=["PaperContent"],
            tests=["tests/unit/test_paper_content_service.py"],
            priority="P0",
        ),
        ArchitectureBox(
            box_id=8,
            name="Core Web Tools",
            goal="Expose local web content services without direct network coupling.",
            owner_skill="turingresearch-core-reproduction",
            public_tools=["core.web_content", "core.web_fetching"],
            internal_modules=["src/turing_research/web/"],
            input_artifacts=["WebContentRequest"],
            output_artifacts=["WebContent"],
            tests=["tests/unit/test_web_content_service.py"],
            priority="P0",
        ),
        ArchitectureBox(
            box_id=9,
            name="PDF Markdown",
            goal="Convert local PDFs to cached markdown with lightweight quality checks.",
            owner_skill="turingresearch-pdf-markdown-core",
            public_tools=["pdf.inspect", "pdf.to_markdown", "pdf.markdown_content"],
            internal_modules=["src/turing_research/pdf/"],
            input_artifacts=["PDFMarkdownInput"],
            output_artifacts=["PDFMarkdownOutput"],
            tests=["tests/unit/test_pdf_markdown_pipeline.py"],
            priority="P0",
            dependencies=[7],
        ),
        ArchitectureBox(
            box_id=10,
            name="Semantic Graph",
            goal="Support citation, reference, recommendation, and author graph workflows.",
            owner_skill="turingresearch-fusion-semantic-graph",
            public_tools=["graph.paper_lookup", "graph.citation_graph_expand"],
            internal_modules=["src/turing_research_plus/semantic_graph/"],
            input_artifacts=["PaperNode"],
            output_artifacts=["CitationGraph"],
            tests=["tests/unit/test_citation_graph.py"],
            priority="P1",
            dependencies=[7],
        ),
        ArchitectureBox(
            box_id=11,
            name="Literature Survey",
            goal="Run depth-gated literature survey workflows.",
            owner_skill="turingresearch-fusion-literature-survey",
            public_tools=["research.survey_plan", "research.survey_run"],
            internal_modules=["src/turing_research_plus/survey/"],
            input_artifacts=["SurveyInput"],
            output_artifacts=["LiteratureSurveyArtifact"],
            tests=["tests/workflow/test_literature_survey_dry_run.py"],
            priority="P1",
            dependencies=[7, 8, 9, 10],
        ),
        ArchitectureBox(
            box_id=12,
            name="Vault",
            goal="Persist research artifacts and graph memory in markdown vault form.",
            owner_skill="turingresearch-fusion-wiki-vault",
            public_tools=["vault.search", "vault.ingest_source", "vault.query_graph"],
            internal_modules=["src/turing_research_plus/vault/"],
            input_artifacts=["ResearchArtifact"],
            output_artifacts=["VaultPage", "VaultEdge"],
            tests=["tests/unit/test_vault_artifact_ingestion.py"],
            priority="P1",
            dependencies=[11],
        ),
        ArchitectureBox(
            box_id=13,
            name="Context",
            goal="Checkpoint and recover long-running research workflow context.",
            owner_skill="turingresearch-fusion-context-management",
            public_tools=["context.init", "context.checkpoint", "context.recover"],
            internal_modules=["src/turing_research_plus/context/"],
            input_artifacts=["ResearchArtifact"],
            output_artifacts=["ContextCheckpoint"],
            tests=["tests/unit/test_context_service.py"],
            priority="P1",
            dependencies=[12],
        ),
        ArchitectureBox(
            box_id=14,
            name="Hypothesis / Ideation",
            goal="Turn gaps into hypotheses, research questions, and diverse ideas.",
            owner_skill="turingresearch-fusion-hypothesis-formation",
            public_tools=["research.hypothesis_generate", "research.idea_generate"],
            internal_modules=[
                "src/turing_research_plus/hypothesis/",
                "src/turing_research_plus/ideation/",
            ],
            input_artifacts=["GapValidationReport", "HypothesisSet"],
            output_artifacts=["HypothesisPortfolio", "IdeaPortfolio"],
            tests=["tests/unit/test_hypothesis_portfolio.py", "tests/unit/test_idea_generation.py"],
            priority="P1",
            dependencies=[11],
        ),
        ArchitectureBox(
            box_id=15,
            name="Convergence / Stress / Experiment",
            goal="Rank ideas, stress-test decisions, and design dry-run experiments.",
            owner_skill="turingresearch-fusion-convergence",
            public_tools=[
                "research.portfolio_optimize",
                "research.artifact_stress_test",
                "research.experiment_design",
            ],
            internal_modules=[
                "src/turing_research_plus/convergence/",
                "src/turing_research_plus/stress/",
                "src/turing_research_plus/experiment/",
            ],
            input_artifacts=["IdeaPortfolio", "HypothesisPortfolio"],
            output_artifacts=["DecisionReport", "StressTestReport", "ExperimentPlan"],
            tests=["tests/unit/test_portfolio_optimize.py", "tests/unit/test_experiment_design.py"],
            priority="P1",
            dependencies=[14],
        ),
        ArchitectureBox(
            box_id=16,
            name="Paper / Figure Pipeline",
            goal="Turn experiment evidence into article blocks, figures, captions, and drafts.",
            owner_skill="turingresearch-paper-writing-pipeline",
            public_tools=[
                "paper.article_block_update",
                "paper.figure_register",
                "paper.draft_generate",
            ],
            internal_modules=["src/turing_research_plus/paper/"],
            input_artifacts=["ExperimentReport", "ArticleBlock"],
            output_artifacts=["PaperDraft"],
            tests=["tests/unit/test_article_block.py"],
            priority="P2",
            dependencies=[15],
        ),
    ]
