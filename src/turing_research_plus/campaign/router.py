"""Campaign strategy router."""

from __future__ import annotations

from turing_research_plus.campaign.models import CampaignSpec, StrategySpec


class CampaignRouter:
    """Select a strategy for a campaign run."""

    def select_strategy(self, spec: CampaignSpec) -> StrategySpec:
        """Select a strategy using requested strategy ID, tag, or first strategy."""

        if not spec.strategies:
            raise ValueError("campaign requires at least one strategy")

        requested = spec.inputs.get("strategy_id")
        if isinstance(requested, str):
            for strategy in spec.strategies:
                if strategy.strategy_id == requested:
                    return strategy
            raise ValueError(f"strategy not found: {requested}")

        requested_tag = spec.inputs.get("strategy_tag")
        if isinstance(requested_tag, str):
            for strategy in spec.strategies:
                if requested_tag in strategy.selection_tags:
                    return strategy
            raise ValueError(f"strategy tag not found: {requested_tag}")

        return spec.strategies[0]
