# SSH / SFTP Remote Artifact Reader



Status: feature capsule skeleton.



## Problem



Remote GPU machines may expose exported result folders through SSH or SFTP, but TuringResearch must inspect them without becoming a remote executor.



## VGGT motivating example



A VGGT remote machine exposes a thin review bundle over SFTP. TuringResearch should list files, classify allowed summaries, and record missing artifacts without running remote shell commands.



## User story



As a TuringResearch operator, I want this feature to produce reviewable,

audit-friendly artifacts while preserving evidence boundaries, so that VGGT and

paper workflows can advance without leaking secrets or overclaiming results.



## Inputs



- Handoff bundle manifests.

- Run ingest reports.

- Artifact audit reports.

- Evidence Ledger status labels.

- VGGT Research Knowledge Pack material.

- Manual review notes when needed.



## Outputs



- `RemoteArtifactReadReport`.

- JSON-serializable report.

- Markdown review summary.

- Proposed evidence updates only when relevant.



## Data model



- status: planned / retrieved / indexed / blocked / requires-human-review.

- source refs and sha256 metadata.

- safety warnings and omitted items.

- limitations and blockers.

- manual review flag.



## Proposed commands / tools



- command: `turing artifact sftp-read`

- tool: `artifact.sftp_read_optional`

- output: `RemoteArtifactReadReport`



## Related contracts



- `contracts/ssh_sftp_remote_reader.yaml`

- `contracts/handoff_bundle.yaml`

- `contracts/run_ingest.yaml`



## Related skills



- `turingresearch-fusion-context-management`

- `turingresearch-master-orchestrator`



## Required tests



- Fake/default workflow test.

- Missing credential or unavailable source test.

- Secret/raw-data/SMPL-X model exclusion test.

- JSON serialization test.

- Markdown export test.

- Evidence-boundary regression test.



## Risks



Credential handling, remote path traversal, and accidental remote execution.



## Done criteria



Fake SFTP listing, credential-absent skip, read-only contract, path policy, and no remote command execution.



## Release target



v0.4 Sprint 1



## Non-goals



- No default networking.

- No permission bypass.

- No automatic large-file download.

- No remote code execution.

- No saved secrets.

- No raw data or SMPL-X model file packaging.

- No remote artifact treated as verified evidence.

- No legacy project naming.
