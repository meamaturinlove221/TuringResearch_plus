# Stress Scenario Library

Status: v1.3 public-safe library.

Round: 281.

This round extends the stress-test scenario catalog into a display-ready library
that is closer to the yogsoth-style stress-test thinking. It does not add a
multi-agent runtime.

## Required Scenarios

| Scenario | Purpose |
| --- | --- |
| `missing_evidence` | Catch claims without evidence refs. |
| `unsupported_claim` | Catch claims that exceed support. |
| `fake_result_risk` | Keep fake/demo output from becoming observed evidence. |
| `artifact_omission` | Require inspectable artifacts. |
| `citation_weakness` | Surface thin or unverified citation context. |
| `privacy_leak` | Detect private data, paths, or credential risk. |
| `unsafe_remote_action` | Block remote command or destructive remote action requests. |
| `plugin_permission_risk` | Detect unsafe plugin permissions. |
| `route_contradiction` | Detect route claims that contradict gates. |
| `advisor_report_overclaim` | Catch advisor-facing unsupported claims. |

## Library Properties

- local and deterministic;
- fake-runnable;
- review-only;
- no multi-agent runtime;
- no network required;
- human review required.

## Example

See:

- `examples/stress_scenarios/README.md`

## Validation

Run:

```powershell
python -m pytest tests/unit/test_stress_scenario_library.py tests/workflow/test_stress_scenario_library_fake.py -q
```
