# GitHub Artifact Sync



Status: feature capsule skeleton.



## Problem



Remote VGGT and pod work can return structured review artifacts, but v0.3 only has local handoff bundles and pod context packages. The project needs a controlled GitHub-based artifact return plan without pushing secrets or raw data.



## VGGT motivating example



A future VGGT Modal SparseConv3D run produces final_status.json, failure_report.md, board inventory, sha256 sums, and thin prediction summaries. The main machine needs to ingest those review files without downloading raw datasets or SMPL-X model files.



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



- `GitHubArtifactSyncReport`.

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



- command: `turing artifact github-sync`

- tool: `artifact.github_sync`

- output: `GitHubArtifactSyncReport`



## Related contracts



- `contracts/github_artifact_sync.yaml`

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



Accidental push or ingestion of private artifacts, secrets, or oversized payloads.



## Done criteria



Fake repository fixture sync plan, manifest validation, denied-file checks, no default push, and proposed evidence updates only.



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
