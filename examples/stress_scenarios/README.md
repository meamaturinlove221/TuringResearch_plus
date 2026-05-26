# Stress Scenario Library Demo

Status: public-safe fake demo.

Round: 281.

This demo documents the v1.3 stress scenario library. It is a local review
catalog, not a multi-agent runtime.

## Scenarios

| Scenario | Category | Severity |
| --- | --- | --- |
| `missing_evidence` | evidence | `high` |
| `unsupported_claim` | claim_safety | `high` |
| `fake_result_risk` | fake_live_boundary | `critical` |
| `artifact_omission` | artifact_readiness | `high` |
| `citation_weakness` | scholar_review | `medium` |
| `privacy_leak` | privacy | `critical` |
| `unsafe_remote_action` | remote_safety | `critical` |
| `plugin_permission_risk` | plugin_safety | `critical` |
| `route_contradiction` | route_integrity | `high` |
| `advisor_report_overclaim` | advisor_safety | `high` |

## Safety Boundary

- fake/demo only;
- no multi-agent runtime;
- no network;
- no remote execution;
- no plugin execution;
- no Evidence Ledger mutation;
- human review required.
