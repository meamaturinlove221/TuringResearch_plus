# Campaign Trace E2E Demo

Demo-only campaign trace walkthrough:

`task intent -> campaign route -> required inputs -> skill map -> expected outputs -> trace report`

This demo uses the `stress_test` campaign because it is the safest default for
reviewing unsupported release claims before promotion.

Safety:

- fake trace only;
- no agent runtime;
- no tool execution;
- no LLM call;
- no network;
- no Evidence Ledger mutation;
- proposed outputs stay proposed-only;
- human review required.

Files:

- `task_intent.md`
- `route_summary.json`
- `required_inputs.md`
- `skill_map.md`
- `expected_outputs.md`
- `trace_report.md`
