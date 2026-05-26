# Campaign Trace E2E

Round 314 turns the campaign execution trace into a complete fake E2E demo:

`task intent -> campaign route -> required inputs -> skill map -> expected outputs -> trace report`

## Demo Path

`examples/campaigns/e2e_trace_demo/`

Files:

- `task_intent.md`
- `route_summary.json`
- `required_inputs.md`
- `skill_map.md`
- `expected_outputs.md`
- `trace_report.md`

## E2E Flow

1. Start from a task intent: stress-test an unsafe release claim.
2. Route the intent to `stress_test`.
3. Record required inputs and visible preconditions.
4. Map the campaign to `turingresearch-fusion-stress-test`.
5. List expected outputs and proposed trace outputs.
6. Render a review-only campaign trace report.

## Safety Boundary

- fake trace only;
- no agent runtime;
- no tool execution;
- no LLM call;
- no network;
- no Evidence Ledger mutation;
- no proposed output becomes observed evidence;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_campaign_trace_e2e.py -q
```
