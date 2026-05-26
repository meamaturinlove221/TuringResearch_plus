"""Static TuringResearch campaign catalog."""

from __future__ import annotations

from turing_research_plus.campaigns.models import CampaignCatalog, CampaignDefinition

MASTER = "turingresearch-master-orchestrator"


CAMPAIGN_CATALOG = CampaignCatalog(
    campaigns=[
        CampaignDefinition(
            campaign_id="north_star",
            purpose="Clarify the research north star, scope, non-goals, and review boundary.",
            when_to_use=["project start", "scope drift", "release positioning"],
            preconditions=["research intent or project brief"],
            recommended_skills=["turingresearch-fusion-north-star", MASTER],
            required_inputs=["research intent", "known constraints"],
            expected_outputs=["north star note", "scope boundary", "non-goals"],
            safety_notes=["do not turn aspirations into observed evidence"],
            fake_live_boundary="Local planning only; no live adapter is required.",
            docs=["docs/north-star.md", "docs/v1.0.0-final-scope.md"],
            tests=["tests/unit/test_template_registry.py"],
            keywords=["north star", "scope", "goal", "positioning", "non-goal"],
        ),
        CampaignDefinition(
            campaign_id="knowledge_acquisition",
            purpose="Collect source material, papers, and project context with source hygiene.",
            when_to_use=["literature intake", "source collection", "context gathering"],
            preconditions=["source list or search intent", "source hygiene boundary"],
            recommended_skills=["turingresearch-fusion-literature-survey", MASTER],
            required_inputs=["source hints", "allowed source policy"],
            expected_outputs=["source list", "paper digest inputs", "missing source notes"],
            safety_notes=["do not download restricted material by default"],
            fake_live_boundary=(
                "Fake/cache-first; live scholar or web adapters require explicit opt-in."
            ),
            docs=["docs/scholar-pipeline-refinement.md", "docs/web-fetch-adapter.md"],
            tests=[
                "tests/unit/test_scholar_search_priority.py",
                "tests/unit/test_web_fetch_fake.py",
            ],
            keywords=["knowledge", "paper", "source", "literature", "web fetch"],
        ),
        CampaignDefinition(
            campaign_id="deep_insight",
            purpose="Turn gathered evidence into reviewable insights and uncertainty notes.",
            when_to_use=["gap analysis", "claim review", "advisor preparation"],
            preconditions=["evidence notes", "claim candidates"],
            recommended_skills=["turingresearch-fusion-deep-insight", MASTER],
            required_inputs=["evidence ledger", "claims or questions"],
            expected_outputs=["gap analysis", "sensitivity notes", "advisor questions"],
            safety_notes=["requires human review before conclusions"],
            fake_live_boundary="Local analysis only; no network or live adapter required.",
            docs=["docs/paper-deep-review-mode.md", "docs/export-quality-gate.md"],
            tests=["tests/unit/test_export_quality_gate.py"],
            keywords=["insight", "gap", "claim", "advisor", "uncertainty"],
        ),
        CampaignDefinition(
            campaign_id="hypothesis_formation",
            purpose="Shape hypotheses and falsifiability checks without promoting them to results.",
            when_to_use=["new idea", "experiment proposal", "route planning"],
            preconditions=["north star", "evidence constraints"],
            recommended_skills=["turingresearch-fusion-hypothesis-formation", MASTER],
            required_inputs=["candidate idea", "constraints"],
            expected_outputs=["hypothesis card", "falsifiability checklist", "risk notes"],
            safety_notes=["planned hypotheses are not executed evidence"],
            fake_live_boundary="Planning only; no experiment execution.",
            docs=["docs/experiment-route-dsl.md", "docs/hard-gate-library.md"],
            tests=["tests/unit/test_experiment_route_compiler.py"],
            keywords=["hypothesis", "falsify", "experiment idea", "proposal"],
        ),
        CampaignDefinition(
            campaign_id="creative_ideation",
            purpose="Generate bounded research or engineering options for human selection.",
            when_to_use=["design exploration", "feature candidates", "roadmap options"],
            preconditions=["problem statement", "constraints"],
            recommended_skills=["turingresearch-fusion-creative-ideation", MASTER],
            required_inputs=["problem", "constraints", "risk appetite"],
            expected_outputs=["candidate ideas", "selection notes", "non-goals"],
            safety_notes=["ideas remain proposals until reviewed"],
            fake_live_boundary="Local ideation only; no live services.",
            docs=["docs/v0.8.0-candidates.md", "docs/v1.0.0-risk-register.md"],
            tests=["tests/unit/test_quality_metrics.py"],
            keywords=["idea", "creative", "candidate", "roadmap", "brainstorm"],
        ),
        CampaignDefinition(
            campaign_id="convergence",
            purpose="Compare candidates and converge on feasible release or research choices.",
            when_to_use=["selection", "scope lock", "go/no-go"],
            preconditions=["candidate list", "evaluation criteria"],
            recommended_skills=["turingresearch-fusion-convergence", MASTER],
            required_inputs=["candidates", "criteria", "constraints"],
            expected_outputs=["ranked options", "decision notes", "deferred list"],
            safety_notes=["ranking is decision support, not automatic approval"],
            fake_live_boundary="Local scoring only; no network required.",
            docs=["docs/v1.0.0-final-scope.md", "docs/v1.0.0-go-no-go.md"],
            tests=["tests/unit/test_regression_gate.py"],
            keywords=["converge", "selection", "priority", "scope lock", "go no-go"],
        ),
        CampaignDefinition(
            campaign_id="stress_test",
            purpose="Stress-test claims, plans, and release posture before promotion.",
            when_to_use=["release gate", "unsafe claim review", "failure analysis"],
            preconditions=["candidate claim or release surface"],
            recommended_skills=["turingresearch-fusion-stress-test", MASTER],
            required_inputs=["claims", "evidence", "known risks"],
            expected_outputs=["risk report", "blocked claims", "next actions"],
            safety_notes=["blocks unsupported claims and fake observed results"],
            fake_live_boundary="Local gate only; live data does not become verified automatically.",
            docs=["docs/quality-metrics.md", "docs/regression-gate.md"],
            tests=[
                "tests/unit/test_regression_gate.py",
                "tests/contract/test_v1_security_privacy_gate.py",
            ],
            keywords=["stress", "risk", "unsafe", "blocker", "gate"],
        ),
        CampaignDefinition(
            campaign_id="experiment_planning",
            purpose="Plan experiment routes, hard gates, metrics, and missing results.",
            when_to_use=["route DSL", "experiment setup", "run planning"],
            preconditions=["north star", "dataset/setup placeholder", "hard gates"],
            recommended_skills=["turingresearch-fusion-experiment-execution", MASTER],
            required_inputs=["route intent", "metrics", "constraints"],
            expected_outputs=["route spec", "hard gate report", "planned run checklist"],
            safety_notes=["planned is not executed and dashboard is not paper result"],
            fake_live_boundary="Planning and replay only; real execution is not automatic.",
            docs=["docs/experiment-route-dsl.md", "docs/experiment-section-builder.md"],
            tests=[
                "tests/unit/test_experiment_route_compiler.py",
                "tests/unit/test_result_table_guard.py",
            ],
            keywords=["experiment", "route", "modal", "metrics", "planned"],
        ),
        CampaignDefinition(
            campaign_id="artifact_audit",
            purpose="Audit artifacts, manifests, completeness, and public-safe export readiness.",
            when_to_use=["artifact review", "handoff", "release export"],
            preconditions=["artifact manifest or expected outputs"],
            recommended_skills=["turingresearch-cache-and-ledger", MASTER],
            required_inputs=["artifact index", "expected artifacts"],
            expected_outputs=["artifact audit report", "missing items", "safety notes"],
            safety_notes=["do not package raw data, secrets, or restricted model files"],
            fake_live_boundary="Local file metadata only by default; remote adapters are optional.",
            docs=["docs/artifact-auditor.md", "docs/export-quality-gate.md"],
            tests=[
                "tests/unit/test_artifact_audit_manifest.py",
                "tests/unit/test_export_quality_gate.py",
            ],
            keywords=["artifact", "audit", "manifest", "export", "missing"],
        ),
        CampaignDefinition(
            campaign_id="advisor_pack",
            purpose="Package current research state into advisor-review material.",
            when_to_use=["advisor meeting", "progress review", "decision needed"],
            preconditions=["evidence summary", "artifact readiness", "limitations"],
            recommended_skills=["turingresearch-paper-writing-pipeline", MASTER],
            required_inputs=["advisor context", "evidence summary", "next actions"],
            expected_outputs=["advisor Markdown bundle", "optional export plan", "quality report"],
            safety_notes=["requires human review and must not fabricate figures or results"],
            fake_live_boundary="Markdown/export plan is local; PDF/PPTX backends are optional.",
            docs=["docs/advisor-markdown-bundle.md", "docs/advisor-export-guide.md"],
            tests=["tests/workflow/test_vggt_advisor_markdown_bundle.py"],
            keywords=["advisor", "pack", "meeting", "decision", "summary"],
        ),
        CampaignDefinition(
            campaign_id="public_release",
            purpose=(
                "Prepare public release posture with privacy, compliance, and regression gates."
            ),
            when_to_use=["release candidate", "public launch", "README hardening"],
            preconditions=["passing tests", "public-safe docs", "privacy scan"],
            recommended_skills=["turingresearch-qa-release", MASTER],
            required_inputs=["release docs", "test summary", "audit reports"],
            expected_outputs=["go/no-go report", "blockers", "release notes"],
            safety_notes=["do not publish from dirty worktree or include private data"],
            fake_live_boundary="Release checks are local by default; no publication action.",
            docs=["docs/v1.0.0-public-release-plan.md", "docs/v1.0.0-public-launch-go-no-go.md"],
            tests=["tests/workflow/test_v1_public_launch_rc.py"],
            keywords=["release", "public", "launch", "readme", "privacy", "rc"],
        ),
    ]
)


def list_campaigns() -> list[CampaignDefinition]:
    """Return all campaign definitions."""

    return list(CAMPAIGN_CATALOG.campaigns)


def get_campaign(campaign_id: str) -> CampaignDefinition:
    """Return a campaign definition by id."""

    try:
        return CAMPAIGN_CATALOG.by_id()[campaign_id]
    except KeyError as exc:
        raise KeyError(f"unknown campaign: {campaign_id}") from exc
