# Lane 157 - Campaign Catalog and MCP Config Polish

Status: implemented minimal.

Round: 176 upstream adjustment.

## Goal

Add the two v1.0 prelaunch planning adjustments from the upstream refresh:

1. TuringResearch Campaign Catalog.
2. MCP / `.mcp.example.json` / live-fake config polish.

## Outputs

- `docs/turingresearch-campaign-catalog.md`
- `docs/campaign-routing-table.md`
- `docs/campaign-preconditions.md`
- `docs/campaign-to-skill-map.md`
- `docs/mcp-config-polish-v1.0.md`
- `docs/mcp-env-block-policy.md`
- `docs/live-fake-config-examples.md`
- `.mcp.example.json`
- `contracts/campaign_catalog.yaml`
- `src/turing_research_plus/campaigns/`
- `tests/unit/test_campaign_catalog_models.py`
- `tests/unit/test_campaign_catalog.py`
- `tests/unit/test_campaign_router.py`
- `tests/contract/test_mcp_example_config_v1.py`
- `tests/contract/test_live_fake_config_defaults.py`

## Campaigns

- `north_star`
- `knowledge_acquisition`
- `deep_insight`
- `hypothesis_formation`
- `creative_ideation`
- `convergence`
- `stress_test`
- `experiment_planning`
- `artifact_audit`
- `advisor_pack`
- `public_release`

## Boundary

- No upstream code copied.
- No complex agent runtime.
- No skill execution.
- No LLM call.
- No default networking.
- No real API key.
- No private VGGT path read.
- No planned-to-observed promotion.

## Status

Ready for local tests and release review.
