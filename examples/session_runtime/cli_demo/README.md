# Session CLI Demo

Status: fake/demo only.

Round: 292.

This directory documents the public-safe Session CLI demo path. It reuses the
existing Session runtime fixtures:

- `../preflight_fixture/`
- `../context_pack_fixture/`
- `../return_fixture/`

## Demo Commands

```powershell
python -m turing_research_plus.session_runtime.cli report
python -m turing_research_plus.session_runtime.cli session replay `
  --project-root examples/session_runtime/preflight_fixture `
  --preflight-context-source context `
  --preflight-output-dir output `
  --context-pack-source-dir examples/session_runtime/context_pack_fixture/source `
  --replay-workspace tmp/session-cli-demo-replay `
  --fake-return-fixture-dir examples/session_runtime/return_fixture
```

## Safety

- fake/dry-run default;
- no live SSH;
- no remote command;
- no secrets logging;
- no automatic Evidence Ledger write;
- proposed updates only;
- human review required.
