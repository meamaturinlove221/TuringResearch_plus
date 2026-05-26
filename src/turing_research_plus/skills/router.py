"""Skill routing recommendations."""

from __future__ import annotations

from turing_research_plus.skills.models import SkillRoute, SkillRoutingDecision

MASTER_SKILL = "turingresearch-master-orchestrator"


DEFAULT_ROUTES: list[SkillRoute] = [
    SkillRoute(
        category="upstream watch",
        recommended_skill="turingresearch-race-upstream-watch",
        ranked_skills=["turingresearch-race-upstream-watch", MASTER_SKILL],
        related_lane="lanes/21_upstream_watch_baseline.md",
        related_contracts=["contracts/race_features.yaml"],
        keywords=["upstream", "watch", "github", "snapshot"],
    ),
    SkillRoute(
        category="VGGT dogfooding",
        recommended_skill=MASTER_SKILL,
        ranked_skills=[MASTER_SKILL, "turingresearch-fusion-experiment-execution"],
        related_lane="lanes/14_v0.2_sprint_1.md",
        related_contracts=["contracts/vggt_evidence.yaml"],
        keywords=["vggt", "dogfooding", "smpl", "smpl-x"],
    ),
    SkillRoute(
        category="evidence ledger",
        recommended_skill="turingresearch-cache-and-ledger",
        ranked_skills=["turingresearch-cache-and-ledger", MASTER_SKILL],
        related_lane="lanes/14_v0.2_sprint_1.md",
        related_contracts=["contracts/vggt_evidence.yaml"],
        keywords=["evidence", "ledger", "observed", "planned"],
    ),
    SkillRoute(
        category="artifact audit",
        recommended_skill="turingresearch-cache-and-ledger",
        ranked_skills=["turingresearch-cache-and-ledger", MASTER_SKILL],
        related_lane="lanes/14_v0.2_sprint_1.md",
        related_contracts=["contracts/artifact_audit.yaml"],
        keywords=["artifact", "audit", "manifest", "npz", "sha256"],
    ),
    SkillRoute(
        category="visual audit",
        recommended_skill=MASTER_SKILL,
        ranked_skills=[MASTER_SKILL, "turingresearch-paper-figure-asset-pipeline"],
        related_lane="lanes/14_v0.2_sprint_1.md",
        related_contracts=["contracts/visual_evidence.yaml"],
        keywords=["visual", "board", "image", "hairline", "hand"],
    ),
    SkillRoute(
        category="advisor pack",
        recommended_skill="turingresearch-paper-writing-pipeline",
        ranked_skills=["turingresearch-paper-writing-pipeline", MASTER_SKILL],
        related_lane="lanes/14_v0.2_sprint_1.md",
        related_contracts=["contracts/advisor_pack.yaml"],
        keywords=["advisor", "summary", "pack", "message"],
    ),
    SkillRoute(
        category="PDF extraction",
        recommended_skill="turingresearch-pdf-markdown-core",
        ranked_skills=[
            "turingresearch-pdf-markdown-core",
            "turingresearch-paper-figure-asset-pipeline",
        ],
        related_lane="lanes/03_pdf_markdown.md",
        related_contracts=["contracts/pdf_markdown.yaml"],
        keywords=["pdf", "figure", "table", "markdown", "extract"],
    ),
    SkillRoute(
        category="route DSL",
        recommended_skill="turingresearch-fusion-experiment-execution",
        ranked_skills=["turingresearch-fusion-experiment-execution", MASTER_SKILL],
        related_lane="lanes/27_experiment_route_and_hard_gates.md",
        related_contracts=["contracts/experiment_route.yaml"],
        keywords=["route dsl", "experiment route", "compile route", "modal", "sparseconv"],
    ),
    SkillRoute(
        category="hard gates",
        recommended_skill="turingresearch-fusion-experiment-execution",
        ranked_skills=["turingresearch-fusion-experiment-execution", MASTER_SKILL],
        related_lane="lanes/27_experiment_route_and_hard_gates.md",
        related_contracts=["contracts/hard_gates.yaml"],
        keywords=["hard gate", "gate", "validate", "promotion"],
    ),
    SkillRoute(
        category="failure taxonomy",
        recommended_skill="turingresearch-fusion-stress-test",
        ranked_skills=["turingresearch-fusion-stress-test", MASTER_SKILL],
        related_lane="lanes/28_failure_taxonomy_engine.md",
        related_contracts=["contracts/failure_taxonomy.yaml"],
        keywords=["failure", "taxonomy", "next action", "attribution"],
    ),
    SkillRoute(
        category="paper method",
        recommended_skill="turingresearch-paper-writing-pipeline",
        ranked_skills=["turingresearch-paper-writing-pipeline", MASTER_SKILL],
        related_lane="lanes/29_paper_to_method_card.md",
        related_contracts=["contracts/paper_method_card.yaml"],
        keywords=["method card", "paper method", "neuralbody", "humanram"],
    ),
    SkillRoute(
        category="figure architecture",
        recommended_skill="turingresearch-paper-figure-asset-pipeline",
        ranked_skills=["turingresearch-paper-figure-asset-pipeline", MASTER_SKILL],
        related_lane="lanes/30_figure_to_architecture.md",
        related_contracts=["contracts/architecture_diagram.yaml"],
        keywords=["architecture", "mermaid", "graphviz", "figure"],
    ),
    SkillRoute(
        category="citation graph",
        recommended_skill="turingresearch-fusion-semantic-graph",
        ranked_skills=["turingresearch-fusion-semantic-graph", MASTER_SKILL],
        related_lane="lanes/38_citation_graph_expansion.md",
        related_contracts=["contracts/citation_graph.yaml"],
        keywords=["citation", "graph", "frontier", "semantic scholar"],
    ),
    SkillRoute(
        category="collision risk",
        recommended_skill="turingresearch-paper-writing-pipeline",
        ranked_skills=[
            "turingresearch-paper-writing-pipeline",
            "turingresearch-fusion-semantic-graph",
        ],
        related_lane="lanes/39_paper_collision_risk.md",
        related_contracts=["contracts/collision_risk.yaml"],
        keywords=["collision", "overlap", "safe claims", "unsafe claims"],
    ),
    SkillRoute(
        category="related work",
        recommended_skill="turingresearch-paper-writing-pipeline",
        ranked_skills=[
            "turingresearch-paper-writing-pipeline",
            "turingresearch-fusion-semantic-graph",
        ],
        related_lane="lanes/53_related_work_positioning.md",
        related_contracts=["contracts/related_work_positioning.yaml"],
        keywords=["related work", "position", "positioning", "literature"],
    ),
    SkillRoute(
        category="web fetch",
        recommended_skill="turingresearch-core-reproduction",
        ranked_skills=["turingresearch-core-reproduction", "turingresearch-architecture-contracts"],
        related_lane="lanes/52_web_fetch_apify_adapter.md",
        related_contracts=["contracts/web_fetch_adapter.yaml", "contracts/apify_adapter.yaml"],
        keywords=["web fetch", "apify", "project page", "readme", "html"],
    ),
    SkillRoute(
        category="handoff",
        recommended_skill="turingresearch-fusion-context-management",
        ranked_skills=["turingresearch-fusion-context-management", MASTER_SKILL],
        related_lane="lanes/41_handoff_bundle.md",
        related_contracts=["contracts/handoff_bundle.yaml"],
        keywords=["handoff", "bundle", "export", "import"],
    ),
    SkillRoute(
        category="pod workflow",
        recommended_skill="turingresearch-fusion-context-management",
        ranked_skills=["turingresearch-fusion-context-management", MASTER_SKILL],
        related_lane="lanes/46_pod_workflow_pack.md",
        related_contracts=["contracts/pod_workflow.yaml"],
        keywords=["pod", "workflow", "context package", "git handoff"],
    ),
    SkillRoute(
        category="vault graph",
        recommended_skill="turingresearch-fusion-wiki-vault",
        ranked_skills=["turingresearch-fusion-wiki-vault", MASTER_SKILL],
        related_lane="lanes/05_vault_memory.md",
        related_contracts=["contracts/vault_schema.yaml"],
        keywords=["vault", "graph", "edge", "wikilink"],
    ),
    SkillRoute(
        category="ontology",
        recommended_skill="turingresearch-fusion-wiki-vault",
        ranked_skills=["turingresearch-fusion-wiki-vault", MASTER_SKILL],
        related_lane="lanes/05_vault_memory.md",
        related_contracts=["contracts/vault_schema.yaml"],
        keywords=["ontology", "alias", "concept", "sop"],
    ),
]


def route_skill(query: str, routes: list[SkillRoute] | None = None) -> SkillRoutingDecision:
    """Return a ranked skill recommendation without executing it."""

    route_table = routes or DEFAULT_ROUTES
    lowered = query.lower()
    scored: list[tuple[int, SkillRoute]] = []
    for route in route_table:
        score = sum(1 for keyword in route.keywords if keyword.lower() in lowered)
        if route.category.lower() in lowered:
            score += 2
        if score:
            scored.append((score, route))
    if not scored:
        return SkillRoutingDecision(
            query=query,
            category="fallback",
            recommended_skill=MASTER_SKILL,
            ranked_skills=[MASTER_SKILL],
            confidence=0.25,
            rationale="No specific route matched; use the master orchestrator.",
            related_lane="lanes/00_master_ledger.md",
        )
    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_route = scored[0]
    ranked = _dedupe(
        [skill for _, route in scored for skill in [route.recommended_skill, *route.ranked_skills]]
    )
    confidence = min(0.95, 0.45 + best_score * 0.15)
    return SkillRoutingDecision(
        query=query,
        category=best_route.category,
        recommended_skill=best_route.recommended_skill,
        ranked_skills=ranked,
        confidence=confidence,
        rationale=f"Matched route category `{best_route.category}` from query keywords.",
        related_lane=best_route.related_lane,
        does_not_execute=True,
    )


def _dedupe(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))
