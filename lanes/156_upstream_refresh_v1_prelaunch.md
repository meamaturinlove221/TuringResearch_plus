# Lane 156 - Upstream Refresh v1 Prelaunch

Status: manual upstream refresh complete.

Round: 175 upstream refresh.

## Goal

Record v1.0 prelaunch upstream signals and decide whether they adjust the v1.0
plan before API freeze and public launch hardening.

## Outputs

- `docs/upstream-refresh-v1.0-prelaunch.md`
- `docs/upstream-change-classification-v1.0.md`
- `docs/upstream-adoption-plan-v1.0-v1.2.md`
- `docs/v1.0.0-plan-adjustment-from-upstream.md`
- `docs/v1.1.0-upstream-driven-candidates.md`
- `docs/v1.2.0-heavy-paper-ingestion-roadmap.md`
- `upstream_watch/reports/v1_prelaunch_manual_snapshot.md`
- `upstream_watch/targets.yaml`

## Decision

Do not change the v1.0 main goal.

Add two pre-freeze planning adjustments:

1. Campaign Catalog and MCP Config Polish.
2. Pod Context Lifecycle Safety Plan.

## Deferred

- Pod Lifecycle Manager: v1.1 candidate.
- Context Return Verifier: v1.1 candidate.
- Web live mode polish: v1.1 candidate.
- Campaign Router model: v1.1 candidate.
- MinerU / heavy PDF fallback: v1.2 candidate.
- Remote execution orchestration: v1.2 or later research item.

## Boundaries

- No upstream code copied.
- No feature implementation.
- No private VGGT path read.
- No remote execution.
- No default live networking.
- No planned-to-observed promotion.
