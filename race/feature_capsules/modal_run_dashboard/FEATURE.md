# Modal Run Dashboard



Status: feature capsule skeleton.



## Problem



Run ingest outputs are structured but hard to scan across route status, missing artifacts, gates, and failure categories.



## VGGT motivating example



The VGGT Modal SparseConv3D fixture reports backend missing, missing predictions, missing boards, and proposed not-enough-evidence updates. A dashboard should show this without running Modal.



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



- `ModalRunDashboardReport`.

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



- command: `turing modal dashboard`

- tool: `experiment.modal_dashboard_build`

- output: `ModalRunDashboardReport`



## Related contracts



- `contracts/modal_run_dashboard.yaml`

- `contracts/handoff_bundle.yaml`

- `contracts/run_ingest.yaml`



## Related skills



- `turingresearch-fusion-experiment-execution`

- `turingresearch-master-orchestrator`



## Required tests



- Fake/default workflow test.

- Missing credential or unavailable source test.

- Secret/raw-data/SMPL-X model exclusion test.

- JSON serialization test.

- Markdown export test.

- Evidence-boundary regression test.



## Risks



Dashboard presentation may imply execution or success if limitations are hidden.



## Done criteria



Static report/dashboard from fixture RunIngestReport, visible blockers, hard gates, and not-ready claims.



## Release target



v0.4 Sprint 1 / dashboard phase



## Non-goals



- No default networking.

- No permission bypass.

- No automatic large-file download.

- No remote code execution.

- No saved secrets.

- No raw data or SMPL-X model file packaging.

- No remote artifact treated as verified evidence.

- No legacy project naming.
