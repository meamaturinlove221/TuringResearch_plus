"""Campaign registry."""

from __future__ import annotations

from turing_research_plus.campaign.models import CampaignSpec


class CampaignRegistry:
    """In-memory campaign registry for tests and fake-service runtime."""

    def __init__(self) -> None:
        self._campaigns: dict[str, CampaignSpec] = {}

    def register(self, spec: CampaignSpec) -> CampaignSpec:
        """Register a campaign spec."""

        if spec.campaign_id in self._campaigns:
            raise ValueError(f"campaign already registered: {spec.campaign_id}")
        self._campaigns[spec.campaign_id] = spec
        return spec

    def get(self, campaign_id: str) -> CampaignSpec:
        """Return a registered campaign."""

        try:
            return self._campaigns[campaign_id]
        except KeyError as exc:
            raise KeyError(f"campaign not found: {campaign_id}") from exc

    def list(self) -> list[CampaignSpec]:
        """Return registered campaigns."""

        return list(self._campaigns.values())
