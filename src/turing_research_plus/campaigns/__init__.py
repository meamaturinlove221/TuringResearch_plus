"""Campaign catalog and routing surfaces."""

from turing_research_plus.campaigns.catalog import (
    CAMPAIGN_CATALOG,
    get_campaign,
    list_campaigns,
)
from turing_research_plus.campaigns.execution_plan import (
    CampaignExecutionPlan,
    build_campaign_execution_plan,
    render_campaign_execution_plan,
)
from turing_research_plus.campaigns.execution_trace import (
    CampaignExecutionTrace,
    CampaignTraceStep,
    build_campaign_execution_trace,
    trace_from_plan,
)
from turing_research_plus.campaigns.models import (
    CampaignCatalog,
    CampaignDefinition,
    CampaignRouteDecision,
)
from turing_research_plus.campaigns.preconditions import (
    CampaignPreconditionReport,
    evaluate_campaign_preconditions,
    render_campaign_precondition_report,
)
from turing_research_plus.campaigns.router import route_campaign
from turing_research_plus.campaigns.strategy_book import (
    CampaignStrategyBook,
    CampaignStrategyEntry,
    build_campaign_strategy_book,
    render_campaign_strategy_book,
)
from turing_research_plus.campaigns.trace_renderer import render_campaign_execution_trace

__all__ = [
    "CAMPAIGN_CATALOG",
    "CampaignCatalog",
    "CampaignDefinition",
    "CampaignExecutionPlan",
    "CampaignExecutionTrace",
    "CampaignPreconditionReport",
    "CampaignRouteDecision",
    "CampaignStrategyBook",
    "CampaignStrategyEntry",
    "CampaignTraceStep",
    "build_campaign_execution_plan",
    "build_campaign_execution_trace",
    "build_campaign_strategy_book",
    "evaluate_campaign_preconditions",
    "get_campaign",
    "list_campaigns",
    "render_campaign_execution_plan",
    "render_campaign_execution_trace",
    "render_campaign_precondition_report",
    "render_campaign_strategy_book",
    "route_campaign",
    "trace_from_plan",
]
