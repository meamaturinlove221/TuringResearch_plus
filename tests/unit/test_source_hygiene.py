from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.race.models import SourceHygieneStatus
from tuling_research_plus.race.source_hygiene import (
    SafeImplementationMode,
    SourceHygieneDecision,
    SourceKind,
    SourceMaterial,
    race_source_hygiene_check,
    source_hygiene_check,
)


def evidence(source_id: str = "src-1") -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="README",
        quote="Public source description.",
    )


def material(
    kind: SourceKind,
    source_id: str = "src-1",
    license_name: str | None = "MIT",
    intended_use: str = "concept",
    public: bool | None = True,
    authorized: bool | None = True,
) -> SourceMaterial:
    return SourceMaterial(
        source_id=source_id,
        kind=kind,
        license=license_name,
        intended_use=intended_use,
        public=public,
        authorized=authorized,
        evidence=evidence(source_id),
    )


def test_public_source_allowed() -> None:
    result = source_hygiene_check(
        [material(SourceKind.PUBLIC_REPO, license_name="Apache-2.0", intended_use="reuse")]
    )

    assert result.decision == SourceHygieneDecision.ALLOW
    assert result.gate.status == SourceHygieneStatus.PASSED
    assert result.safe_implementation_mode == SafeImplementationMode.COMPATIBLE_LICENSE_REUSE


def test_private_source_blocked() -> None:
    result = source_hygiene_check(
        [
            material(
                SourceKind.PRIVATE_REPO_CONTENT,
                public=False,
                authorized=False,
            )
        ]
    )

    assert result.decision == SourceHygieneDecision.BLOCK
    assert result.gate.status == SourceHygieneStatus.BLOCKED
    assert "private_repo_content" in (result.gate.blocked_reason or "")


def test_unknown_source_becomes_watch() -> None:
    result = source_hygiene_check(
        [material(SourceKind.UNKNOWN, license_name=None, public=None, authorized=None)]
    )

    assert result.decision == SourceHygieneDecision.WATCH
    assert result.safe_implementation_mode == SafeImplementationMode.DOCUMENTATION_ONLY_WATCH
    assert result.gate.status == SourceHygieneStatus.BLOCKED


def test_incompatible_license_blocks_code_copying() -> None:
    result = source_hygiene_check(
        [
            material(
                SourceKind.PUBLIC_REPO,
                license_name="AGPL-3.0",
                intended_use="copy implementation",
            )
        ]
    )

    assert result.decision == SourceHygieneDecision.BLOCK
    assert "incompatible" in (result.gate.blocked_reason or "")


def test_race_source_hygiene_check_tool_returns_json_payload() -> None:
    payload = race_source_hygiene_check([material(SourceKind.PUBLIC_README)])

    assert payload["decision"] == "allow"
    assert payload["gate"]["status"] == "passed"

