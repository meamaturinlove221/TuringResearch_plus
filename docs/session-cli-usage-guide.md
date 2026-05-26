# Session CLI Usage Guide

Status: implemented.

Round: 292.

The Session CLI is a fake/default local interface for the Session runtime
parity chain.

## Show Surface

```powershell
python -m turing_research_plus.session_runtime.cli report
turingresearch-session report
```

## Preflight

```powershell
python -m turing_research_plus.session_runtime.cli session preflight `
  --project-root examples/session_runtime/preflight_fixture `
  --context-source context `
  --output-dir output `
  --output tmp/session-preflight.md
```

## Pack

```powershell
python -m turing_research_plus.session_runtime.cli session pack `
  --source-dir examples/session_runtime/context_pack_fixture/source `
  --output-dir tmp/session-pack `
  --output tmp/session-pack-report.md
```

## Fake Transfer

```powershell
python -m turing_research_plus.session_runtime.cli session transfer --fake `
  --source-dir tmp/session-pack `
  --target-dir tmp/session-transfer `
  --output tmp/session-transfer-report.md
```

## Verify Return

```powershell
python -m turing_research_plus.session_runtime.cli session verify-return `
  --return-dir examples/session_runtime/return_fixture `
  --output tmp/session-return-report.md
```

## Replay

```powershell
python -m turing_research_plus.session_runtime.cli session replay `
  --project-root examples/session_runtime/preflight_fixture `
  --preflight-context-source context `
  --preflight-output-dir output `
  --context-pack-source-dir examples/session_runtime/context_pack_fixture/source `
  --replay-workspace tmp/session-replay `
  --fake-return-fixture-dir examples/session_runtime/return_fixture `
  --output tmp/session-replay-report.md
```

## Non-goals

- no live SSH by default;
- no remote command;
- no secrets logging;
- no automatic Evidence Ledger write;
- no raw data packaging;
- no restricted model payload transfer;
- no fake result promotion.
