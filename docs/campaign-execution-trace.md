# Campaign Execution Trace

Status: implemented.

Round: 277.

This round adds a fake execution trace for the Campaign Catalog. The trace makes
campaign routing more demonstrable without turning the catalog into an agent
runtime.

## What It Does

- Builds a campaign execution plan from a task description.
- Records the routed campaign and recommended skill.
- Records provided and missing preconditions.
- Emits deterministic trace steps.
- Renders the trace as Markdown.
- Keeps proposed outputs proposed-only.

## Trace Steps

| Step | Meaning |
| --- | --- |
| `route_campaign` | Record the campaign routing decision. |
| `check_preconditions` | Record missing or satisfied preconditions. |
| `prepare_handoff` | Prepare a manual skill handoff. |
| `record_proposed_outputs` | List expected outputs for review. |
| `human_review_gate` | Stop before execution or public claim. |

## Safety Boundary

- fake execution trace only;
- not an agent runtime;
- does not execute tools;
- does not call an LLM;
- does not use network;
- does not mutate Evidence Ledger;
- does not replace `turingresearch-master-orchestrator`;
- planned outputs are not observed evidence.

## Example

See:

- `examples/campaigns/execution_trace_demo/README.md`
- `examples/campaigns/execution_trace_demo/trace.md`

## Validation

Run:

```powershell
python -m pytest tests/unit/test_campaign_execution_trace.py tests/unit/test_campaign_trace_renderer.py tests/workflow/test_campaign_execution_trace_fake.py -q
```
