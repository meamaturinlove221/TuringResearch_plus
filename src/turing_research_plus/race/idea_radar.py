"""Race Mode Idea Radar."""

from __future__ import annotations

import re
from hashlib import sha256

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.race.models import IdeaCard, IdeaPriority, RecommendedAction
from turing_research_plus.race.source_hygiene import (
    SourceHygieneCheckResult,
    SourceHygieneDecision,
    SourceMaterial,
    source_hygiene_check,
)


class IdeaRadarInput(BaseModel):
    """Input text for idea extraction."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)
    source: SourceMaterial
    source_hygiene: SourceHygieneCheckResult | None = None


class IdeaRadarResult(BaseModel):
    """Result of idea extraction."""

    model_config = ConfigDict(extra="forbid")

    ideas: list[IdeaCard] = Field(default_factory=list)
    source_hygiene: SourceHygieneCheckResult
    skipped_reason: str | None = None


TTS_CORRECTIONS = {
    "m c p": "MCP",
    "mcp first": "MCP-first",
    "cash": "cache",
    "cashe": "cache",
    "letter": "ledger",
    "legder": "ledger",
    "raise mode": "Race Mode",
}

UNCERTAIN_PATTERNS = (
    "maybe",
    "not sure",
    "sounds like",
    "unknown",
    "unclear",
    "???",
)


def extract_idea(input_data: IdeaRadarInput) -> IdeaRadarResult:
    """Extract one deterministic IdeaCard from high-noise source text."""

    hygiene = input_data.source_hygiene or source_hygiene_check([input_data.source])
    if hygiene.decision == SourceHygieneDecision.BLOCK:
        return IdeaRadarResult(
            ideas=[],
            source_hygiene=hygiene,
            skipped_reason="source hygiene blocked idea extraction",
        )

    normalized, uncertain_terms = _normalize_tts(input_data.text)
    summary = _summary(normalized)
    evidence = input_data.source.evidence
    scores = _score(normalized, bool(uncertain_terms))
    priority = _priority(scores)
    action = _action(hygiene, priority, uncertain_terms)
    card = IdeaCard(
        idea_id=_idea_id(input_data.source.source_id, normalized),
        title=_title(summary),
        raw_text=input_data.text,
        normalized_summary=summary,
        inferred_intent=_intent(summary),
        source=input_data.source.source_id,
        value_score=scores["value"],
        feasibility_score=scores["feasibility"],
        urgency_score=scores["urgency"],
        novelty_score=scores["novelty"],
        priority=priority,
        recommended_action=action,
        evidence_refs=[evidence],
        uncertain_terms=uncertain_terms,
        hygiene_gate=hygiene.gate,
        tags=["race", "idea_radar", "speculative" if uncertain_terms else "high_confidence"],
    )
    return IdeaRadarResult(
        ideas=[card],
        source_hygiene=hygiene,
        skipped_reason=None if hygiene.decision == SourceHygieneDecision.ALLOW else "watch only",
    )


def race_idea_extract(input_data: IdeaRadarInput) -> dict[str, object]:
    """Thin race.idea_extract wrapper."""

    return extract_idea(input_data).model_dump(mode="json")


def _normalize_tts(text: str) -> tuple[str, list[str]]:
    lowered = text.lower()
    normalized = text
    for wrong, replacement in TTS_CORRECTIONS.items():
        normalized = re.sub(wrong, replacement, normalized, flags=re.IGNORECASE)
    uncertain = [
        token
        for token in UNCERTAIN_PATTERNS
        if token in lowered
    ]
    noisy_tokens = re.findall(r"\b[a-zA-Z]+(?:ish|maybe)\b", text)
    uncertain.extend(token for token in noisy_tokens if token not in uncertain)
    return " ".join(normalized.split()), sorted(set(uncertain))


def _summary(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    first = sentences[0] if sentences else text
    return first[:240].strip()


def _title(summary: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9 _:-]", "", summary)
    words = cleaned.split()
    title = " ".join(words[:8]).strip()
    return title or "Race Mode idea"


def _intent(summary: str) -> str:
    lowered = summary.lower()
    if "cache" in lowered or "ledger" in lowered:
        return "Improve research workflow reliability."
    if "mcp" in lowered or "tool" in lowered:
        return "Improve MCP-first workflow tooling."
    return "Track a possible Race Mode opportunity."


def _score(text: str, speculative: bool) -> dict[str, float]:
    lowered = text.lower()
    value = 0.75 if any(word in lowered for word in ["improve", "reduce", "faster"]) else 0.6
    feasibility = 0.78 if any(word in lowered for word in ["local", "dry-run", "cache"]) else 0.62
    urgency = 0.8 if any(word in lowered for word in ["urgent", "break", "regression"]) else 0.55
    novelty = 0.72 if any(word in lowered for word in ["new", "novel", "mcp"]) else 0.58
    if speculative:
        value -= 0.1
        feasibility -= 0.1
    return {
        "value": round(max(0.0, min(1.0, value)), 3),
        "feasibility": round(max(0.0, min(1.0, feasibility)), 3),
        "urgency": round(max(0.0, min(1.0, urgency)), 3),
        "novelty": round(max(0.0, min(1.0, novelty)), 3),
    }


def _priority(scores: dict[str, float]) -> IdeaPriority:
    average = sum(scores.values()) / len(scores)
    if average >= 0.72:
        return IdeaPriority.HIGH
    if average >= 0.6:
        return IdeaPriority.MEDIUM
    return IdeaPriority.WATCH


def _action(
    hygiene: SourceHygieneCheckResult,
    priority: IdeaPriority,
    uncertain_terms: list[str],
) -> RecommendedAction:
    if hygiene.decision != SourceHygieneDecision.ALLOW:
        return RecommendedAction.WATCH
    if uncertain_terms:
        return RecommendedAction.DOCUMENT
    if priority == IdeaPriority.HIGH:
        return RecommendedAction.IMPLEMENT
    return RecommendedAction.WATCH


def _idea_id(source_id: str, normalized: str) -> str:
    digest = sha256(f"{source_id}:{normalized}".encode()).hexdigest()[:12]
    return f"idea-{digest}"
