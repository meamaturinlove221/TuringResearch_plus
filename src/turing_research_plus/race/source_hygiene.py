"""Source Hygiene Gate for Race Mode."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.race.models import SourceHygieneGate, SourceHygieneStatus


class SourceKind(StrEnum):
    """Declared source kind."""

    PUBLIC_REPO = "public_repo"
    PUBLIC_README = "public_readme"
    PUBLIC_ISSUE = "public_issue"
    PUBLIC_RELEASE_NOTES = "public_release_notes"
    USER_OWNED_NOTES = "user_owned_notes"
    AUTHORIZED_TRANSCRIPT = "authorized_transcript"
    PRIVATE_REPO_CONTENT = "private_repo_content"
    LEAKED_ROADMAP = "leaked_roadmap"
    NDA_CONTENT = "nda_content"
    PROPRIETARY_CODE = "proprietary_code"
    UNKNOWN = "unknown"


class SafeImplementationMode(StrEnum):
    """Allowed implementation mode after source hygiene check."""

    INDEPENDENT_CLEAN_ROOM = "independent_clean_room_implementation"
    CONCEPT_LEVEL_REIMPLEMENTATION = "concept_level_reimplementation"
    COMPATIBLE_LICENSE_REUSE = "compatible_license_reuse"
    DOCUMENTATION_ONLY_WATCH = "documentation_only_watch"


class SourceHygieneDecision(StrEnum):
    """Source hygiene decision."""

    ALLOW = "allow"
    BLOCK = "block"
    WATCH = "watch"


class SourceMaterial(BaseModel):
    """One source material declaration for Race Mode."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    kind: SourceKind
    license: str | None = None
    public: bool | None = None
    authorized: bool | None = None
    intended_use: str = Field(default="concept", min_length=1)
    evidence: EvidenceRef


class SourceHygieneCheckResult(BaseModel):
    """Result of source hygiene check."""

    model_config = ConfigDict(extra="forbid")

    decision: SourceHygieneDecision
    gate: SourceHygieneGate
    safe_implementation_mode: SafeImplementationMode
    checked_sources: list[EvidenceRef] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


ALLOW_KINDS = {
    SourceKind.PUBLIC_REPO,
    SourceKind.PUBLIC_README,
    SourceKind.PUBLIC_ISSUE,
    SourceKind.PUBLIC_RELEASE_NOTES,
    SourceKind.USER_OWNED_NOTES,
    SourceKind.AUTHORIZED_TRANSCRIPT,
}

BLOCK_KINDS = {
    SourceKind.PRIVATE_REPO_CONTENT,
    SourceKind.LEAKED_ROADMAP,
    SourceKind.NDA_CONTENT,
    SourceKind.PROPRIETARY_CODE,
}

COMPATIBLE_LICENSES = {
    "apache-2.0",
    "mit",
    "bsd-2-clause",
    "bsd-3-clause",
    "cc-by-4.0",
}

INCOMPATIBLE_LICENSES = {
    "agpl-3.0",
    "gpl-2.0",
    "gpl-3.0",
    "lgpl-2.1",
    "lgpl-3.0",
    "proprietary",
    "unknown-proprietary",
}


def source_hygiene_check(sources: list[SourceMaterial]) -> SourceHygieneCheckResult:
    """Check whether Race Mode sources are safe to use."""

    if not sources:
        return _watch([], ["No source material was provided."])

    reasons: list[str] = []
    checked = [source.evidence for source in sources]
    for source in sources:
        reason = _blocking_reason(source)
        if reason is not None:
            reasons.append(reason)
    if reasons:
        return SourceHygieneCheckResult(
            decision=SourceHygieneDecision.BLOCK,
            gate=SourceHygieneGate(
                status=SourceHygieneStatus.BLOCKED,
                checked_sources=checked,
                blocked_reason="; ".join(reasons),
            ),
            safe_implementation_mode=SafeImplementationMode.DOCUMENTATION_ONLY_WATCH,
            checked_sources=checked,
            reasons=reasons,
        )

    if any(source.kind == SourceKind.UNKNOWN for source in sources):
        return _watch(checked, ["Unknown source requires documentation-only watch."])

    if any(source.kind not in ALLOW_KINDS for source in sources):
        return _watch(checked, ["Unrecognized source kind requires documentation-only watch."])

    mode = _safe_mode(sources)
    return SourceHygieneCheckResult(
        decision=SourceHygieneDecision.ALLOW,
        gate=SourceHygieneGate(
            status=SourceHygieneStatus.PASSED,
            checked_sources=checked,
        ),
        safe_implementation_mode=mode,
        checked_sources=checked,
        reasons=["Source material is public or authorized."],
    )


def race_source_hygiene_check(sources: list[SourceMaterial]) -> dict[str, object]:
    """Thin race.source_hygiene_check wrapper."""

    return source_hygiene_check(sources).model_dump(mode="json")


def _blocking_reason(source: SourceMaterial) -> str | None:
    if source.kind in BLOCK_KINDS:
        return f"{source.source_id} is blocked because source kind is {source.kind}."
    if source.public is False and source.kind not in {
        SourceKind.USER_OWNED_NOTES,
        SourceKind.AUTHORIZED_TRANSCRIPT,
    }:
        return f"{source.source_id} is blocked because it is not public."
    if source.authorized is False:
        return f"{source.source_id} is blocked because it is not authorized."
    license_name = _normalize_license(source.license)
    if license_name in INCOMPATIBLE_LICENSES and "copy" in source.intended_use.lower():
        return (
            f"{source.source_id} is blocked because license {source.license} "
            "is incompatible with code copying."
        )
    return None


def _safe_mode(sources: list[SourceMaterial]) -> SafeImplementationMode:
    if all(_normalize_license(source.license) in COMPATIBLE_LICENSES for source in sources):
        return SafeImplementationMode.COMPATIBLE_LICENSE_REUSE
    if any(source.intended_use.lower() == "concept" for source in sources):
        return SafeImplementationMode.CONCEPT_LEVEL_REIMPLEMENTATION
    return SafeImplementationMode.INDEPENDENT_CLEAN_ROOM


def _watch(
    checked_sources: list[EvidenceRef],
    reasons: list[str],
) -> SourceHygieneCheckResult:
    return SourceHygieneCheckResult(
        decision=SourceHygieneDecision.WATCH,
        gate=SourceHygieneGate(
            status=SourceHygieneStatus.BLOCKED,
            checked_sources=checked_sources,
            blocked_reason="; ".join(reasons),
        ),
        safe_implementation_mode=SafeImplementationMode.DOCUMENTATION_ONLY_WATCH,
        checked_sources=checked_sources,
        reasons=reasons,
    )


def _normalize_license(license_name: str | None) -> str:
    return (license_name or "").strip().lower()

