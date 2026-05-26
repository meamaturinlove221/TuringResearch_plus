"""Static campaign router."""

from __future__ import annotations

from turing_research_plus.campaigns.catalog import CAMPAIGN_CATALOG
from turing_research_plus.campaigns.models import CampaignCatalog, CampaignRouteDecision


def route_campaign(
    task_description: str,
    catalog: CampaignCatalog | None = None,
) -> CampaignRouteDecision:
    """Recommend a campaign and skill without executing anything."""

    active_catalog = catalog or CAMPAIGN_CATALOG
    lowered = task_description.lower()
    scored: list[tuple[int, str]] = []
    for campaign in active_catalog.campaigns:
        score = 0
        if campaign.campaign_id.replace("_", " ") in lowered:
            score += 4
        for keyword in campaign.keywords:
            if keyword.lower() in lowered:
                score += 2
        for phrase in campaign.when_to_use:
            if phrase.lower() in lowered:
                score += 1
        if score:
            scored.append((score, campaign.campaign_id))

    if not scored:
        fallback = active_catalog.by_id()["north_star"]
        return CampaignRouteDecision(
            task_description=task_description,
            recommended_campaign=fallback.campaign_id,
            recommended_skill=fallback.recommended_skills[0],
            ranked_campaigns=[fallback.campaign_id],
            ranked_skills=fallback.recommended_skills,
            confidence=0.25,
            rationale="No specific campaign matched; start with north star clarification.",
        )

    scored.sort(key=lambda item: item[0], reverse=True)
    campaign_map = active_catalog.by_id()
    ranked_campaigns = [campaign_id for _, campaign_id in scored]
    best_score, best_id = scored[0]
    best = campaign_map[best_id]
    ranked_skills = _dedupe(
        [
            skill
            for campaign_id in ranked_campaigns
            for skill in campaign_map[campaign_id].recommended_skills
        ]
    )
    confidence = min(0.95, 0.35 + best_score * 0.1)
    return CampaignRouteDecision(
        task_description=task_description,
        recommended_campaign=best.campaign_id,
        recommended_skill=best.recommended_skills[0],
        ranked_campaigns=ranked_campaigns,
        ranked_skills=ranked_skills,
        confidence=confidence,
        rationale=f"Matched campaign `{best.campaign_id}` from task keywords.",
    )


def _dedupe(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))
