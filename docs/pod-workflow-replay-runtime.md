# Pod Workflow Replay Runtime

Round 268 adds a complete fake pod workflow replay for v1.3 Session runtime
parity. The replay is local-only and deterministic. It proves that the runtime
pieces from Rounds 264-267 can be chained without opening SSH, running a remote
command, or writing the Evidence Ledger.

## Replay Chain

1. `SessionPreflightRunner`
2. `ContextPackBuilder`
3. `FakeTransferRunner`
4. `FakePodReturnFixture`
5. `RemoteReturnVerifier`
6. `ProposedEvidenceUpdateReport`

The implementation lives in
`src/turing_research_plus/session_runtime/workflow_replay.py`.

## What It Does

- runs local session preflight against a public fake fixture;
- builds a safe context pack with required handoff files;
- performs a fake/local transfer into a temporary replay target;
- copies a fake pod return fixture into the replay workspace;
- verifies required return files and checksums;
- exposes proposed evidence updates for human review.

The required return files remain:

- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `SHA256SUMS.txt`

## Safety Boundaries

- No live SSH.
- No remote command execution.
- No automatic Evidence Ledger write.
- No automatic experiment execution.
- No default live network.
- No secrets.
- No raw data.
- No restricted model payloads.
- Fake/demo return claims remain proposed-only.

The replay report sets:

- `live_ssh_enabled = false`
- `live_network_enabled = false`
- `remote_command_execution = false`
- `automatic_ledger_write = false`
- `proposed_updates_only = true`
- `requires_human_review = true`

## Example Fixture

`examples/session_runtime/pod_workflow_replay/` describes the fixture inputs.
The workflow test writes generated replay output to a temporary directory, so
runtime output is not committed to the repository.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_pod_workflow_replay_runtime_fake.py -q
```

This test verifies the full fake replay chain and confirms the generated output
does not include secrets, raw data, private path metadata, or restricted model
payloads.
