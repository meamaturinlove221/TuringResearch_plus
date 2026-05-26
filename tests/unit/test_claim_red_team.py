from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from turing_research_plus.stress.claim_red_team import red_team_claim
from turing_research_plus.stress.models import Claim, PassFail, Severity
from turing_research_plus.stress.service import StressTestService
from turing_research_plus.stress.tools import research_artifact_stress_test, research_claim_red_team


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def test_unsupported_claim_is_marked() -> None:
    report = red_team_claim(Claim(claim_id="claim-1", statement="Unsupported claim."))

    assert report.pass_fail == PassFail.FAIL
    assert report.severity == Severity.HIGH
    assert report.weaknesses[0].weakness_id == "claim-unsupported"


def test_supported_claim_passes_with_low_scope_risk() -> None:
    report = red_team_claim(
        Claim(
            claim_id="claim-1",
            statement="Supported claim.",
            evidence_refs=[evidence()],
        )
    )

    assert report.pass_fail == PassFail.PASS
    assert report.residual_risk == Severity.LOW


def test_claim_and_artifact_tools_return_json_payloads() -> None:
    service = StressTestService()
    claim_payload = research_claim_red_team(
        Claim(claim_id="claim-1", statement="Unsupported claim."),
        service,
    )
    artifact_payload = research_artifact_stress_test(
        ResearchArtifact(
            artifact_id="artifact-1",
            kind=ArtifactKind.NOTE,
            title="Supported artifact",
            created_by="test",
            evidence=[evidence()],
        ),
        service,
    )

    assert claim_payload["pass_fail"] == "fail"
    assert artifact_payload["artifact_id"] == "artifact-1"
