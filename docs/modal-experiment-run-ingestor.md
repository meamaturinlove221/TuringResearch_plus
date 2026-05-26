# TuringResearch Plus Modal / Experiment Run Ingestor

Status: v0.2 beta minimal implementation.

Round 59 adds a local run ingestor for Modal fixture exports, local VGGT bundles,
thin review bundles, and manual summaries. It does not run Modal and does not
read private VGGT paths by default.

## Supported Source Types

- `modal_fixture`
- `modal_export`
- `local_vggt_bundle`
- `thin_review_bundle`
- `manual_summary`

## Recognized Statuses

- `REVIEW_READY_NOT_PROMOTED`
- `ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS`
- `HARD_BLOCKED`
- `RUN_FAILED`
- `PARTIAL`
- `UNKNOWN`

## Output

`RunIngestReport` contains:

- run id and route id;
- source type and source path;
- run status and duration;
- sparse backend status;
- candidates and best candidate;
- observed and missing artifacts;
- hard gate results;
- failure categories;
- proposed evidence updates;
- advisor pack inputs;
- human-review boundary.

## VGGT Rules

- Without a real sparse backend log, the report cannot claim SparseConv3D
  success.
- Missing `predictions.npz` or a thin summary becomes a missing artifact.
- Report-only bundles are classified as `REPORT_ONLY`.
- Fallback backend use is classified as `FALLBACK_ONLY`.
- Missing visual board evidence is classified as `VISUAL_PROOF_INSUFFICIENT`.
- Missing cleanup report is recorded as package/cleanup missing.

## Evidence Boundary

The ingestor generates proposed evidence updates only. It does not automatically
modify the VGGT Evidence Ledger and does not promote a route.

## Fixture

`examples/vggt-human-prior-survey/run_ingest_fixtures/modal_run_fixture/`
contains a small synthetic fixture bundle for local tests. It is not a real VGGT
or Modal run.
