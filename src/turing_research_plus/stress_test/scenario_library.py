"""Expanded stress scenario library for v1.3 parity demos."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StressScenarioLibraryEntry(BaseModel):
    """One display-ready stress scenario definition."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    risk_question: str = Field(min_length=1)
    trigger_examples: list[str] = Field(min_length=1)
    expected_signal: str = Field(min_length=1)
    recommended_action: str = Field(min_length=1)
    default_severity: str = Field(pattern=r"^(critical|high|medium|low)$")
    requires_human_review: bool = True
    fake_runnable: bool = True
    multi_agent_runtime: bool = False
    network_required: bool = False


class StressScenarioLibrary(BaseModel):
    """Expanded review-only scenario catalog."""

    model_config = ConfigDict(extra="forbid")

    library_id: str = "stress-scenario-library-v1.3"
    status: str = "review-only"
    scenarios: list[StressScenarioLibraryEntry] = Field(min_length=1)
    multi_agent_runtime: bool = False
    network_required: bool = False
    requires_human_review: bool = True

    def by_id(self) -> dict[str, StressScenarioLibraryEntry]:
        """Return scenarios keyed by id."""

        return {scenario.scenario_id: scenario for scenario in self.scenarios}


def build_stress_scenario_library() -> StressScenarioLibrary:
    """Build the expanded v1.3 stress scenario library."""

    return StressScenarioLibrary(
        scenarios=[
            StressScenarioLibraryEntry(
                scenario_id="missing_evidence",
                title="Missing Evidence",
                category="evidence",
                risk_question="Does every claim have a reviewable evidence ref?",
                trigger_examples=["claim text without evidence_refs"],
                expected_signal="missing evidence refs or empty ledger links",
                recommended_action="Block convergence until evidence refs are added.",
                default_severity="high",
            ),
            StressScenarioLibraryEntry(
                scenario_id="unsupported_claim",
                title="Unsupported Claim",
                category="claim_safety",
                risk_question="Does the text claim more than available support allows?",
                trigger_examples=["proves", "verified success", "final conclusion"],
                expected_signal="overclaim wording or missing support links",
                recommended_action="Downgrade claim to planned or requires-review wording.",
                default_severity="high",
            ),
            StressScenarioLibraryEntry(
                scenario_id="fake_result_risk",
                title="Fake Result Risk",
                category="fake_live_boundary",
                risk_question="Could a fake/demo fixture be mistaken for observed output?",
                trigger_examples=["fake demo with observed wording"],
                expected_signal="fake/demo boundary missing or observed wording present",
                recommended_action="Keep fake/demo status explicit and block observed wording.",
                default_severity="critical",
            ),
            StressScenarioLibraryEntry(
                scenario_id="artifact_omission",
                title="Artifact Omission",
                category="artifact_readiness",
                risk_question="Can a reviewer inspect the required artifacts?",
                trigger_examples=["missing artifact_refs", "missing index"],
                expected_signal="required artifacts absent or not indexed",
                recommended_action="Add artifact refs or keep the route blocked.",
                default_severity="high",
            ),
            StressScenarioLibraryEntry(
                scenario_id="citation_weakness",
                title="Citation Weakness",
                category="scholar_review",
                risk_question="Is the citation context strong enough for review?",
                trigger_examples=["single related-work ref", "fake citation"],
                expected_signal="thin related-work refs or unverified citation markers",
                recommended_action="Add source refs and keep fake citations unverified.",
                default_severity="medium",
            ),
            StressScenarioLibraryEntry(
                scenario_id="privacy_leak",
                title="Privacy Leak",
                category="privacy",
                risk_question="Could public output expose private data or credentials?",
                trigger_examples=["private path", "token-like text", "raw data"],
                expected_signal="privacy marker, credential marker, or restricted file marker",
                recommended_action="Redact, remove, or block public release.",
                default_severity="critical",
            ),
            StressScenarioLibraryEntry(
                scenario_id="unsafe_remote_action",
                title="Unsafe Remote Action",
                category="remote_safety",
                risk_question="Could the workflow run remote commands or mutate a remote host?",
                trigger_examples=["ssh command", "remote delete", "shell execution"],
                expected_signal="remote command or destructive operation request",
                recommended_action="Block remote action unless a dedicated live gate approves it.",
                default_severity="critical",
            ),
            StressScenarioLibraryEntry(
                scenario_id="plugin_permission_risk",
                title="Plugin Permission Risk",
                category="plugin_safety",
                risk_question="Does a plugin request unsafe permissions by default?",
                trigger_examples=["execute_code", "network", "secrets"],
                expected_signal="unsafe plugin permission requested",
                recommended_action="Disable plugin or require explicit review.",
                default_severity="critical",
            ),
            StressScenarioLibraryEntry(
                scenario_id="route_contradiction",
                title="Route Contradiction",
                category="route_integrity",
                risk_question="Do route claims contradict hard gates or forbidden actions?",
                trigger_examples=["no live gate plus live enabled", "blocked claim completed"],
                expected_signal="completion claim contradicts route gate",
                recommended_action="Resolve route contradiction before convergence.",
                default_severity="high",
            ),
            StressScenarioLibraryEntry(
                scenario_id="advisor_report_overclaim",
                title="Advisor Report Overclaim",
                category="advisor_safety",
                risk_question="Does advisor-facing output overstate evidence support?",
                trigger_examples=["advisor claim without evidence", "camera-ready wording"],
                expected_signal="advisor claim missing evidence refs or using final-paper wording",
                recommended_action="Link advisor claims to evidence or block the section.",
                default_severity="high",
            ),
        ]
    )


def render_stress_scenario_library(library: StressScenarioLibrary | None = None) -> str:
    """Render the expanded scenario library as Markdown."""

    active = library or build_stress_scenario_library()
    lines = [
        "# Stress Scenario Library",
        "",
        f"- Library id: `{active.library_id}`",
        f"- Status: `{active.status}`",
        f"- Multi-agent runtime: `{str(active.multi_agent_runtime).lower()}`",
        f"- Network required: `{str(active.network_required).lower()}`",
        f"- Requires human review: `{str(active.requires_human_review).lower()}`",
        "",
        "| Scenario | Category | Severity |",
        "| --- | --- | --- |",
    ]
    for scenario in active.scenarios:
        lines.append(
            f"| `{scenario.scenario_id}` | {scenario.category} | "
            f"`{scenario.default_severity}` |"
        )
    return "\n".join(lines) + "\n"
