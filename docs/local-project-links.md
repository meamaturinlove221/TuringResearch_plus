# Local Project Links

Local project links describe read-only relationships between TulingResearch Plus
and nearby research project folders on the same machine. They are intended for
dogfooding and evidence collection, not for controlling the external project.

## Files

- Commit `local_project_links.example.yaml` as a safe template.
- Keep `local_project_links.yaml` machine-private and ignored by Git.
- Keep imported summaries in TulingResearch Plus, not inside the linked project.

The VGGT dogfood example lives at:

`examples/vggt-human-prior-survey/local_project_links.example.yaml`

## Rules

- Read local project files only when their extension is allow-listed.
- Treat `.npz` as `summary-only` unless a later explicit round adds a stricter
  parser and tests.
- Do not write, delete, rename, or normalize files in the linked project.
- Do not run training, inference, benchmarks, or cleanup jobs in the linked
  project.
- Do not infer successful experiment results from file presence alone.
- If a candidate path is absent, record `missing` and continue.

## Summary Output

Local summaries should separate path observations from research claims.

Recommended fields:

- source config path
- candidate path
- candidate kind, such as root, output, docs, log, or artifact
- status label
- observed file type
- size policy result
- evidence reference to the local path
- notes

Allowed labels are defined by the example config. A summary may say a path was
`observed`, but claims about VGGT quality, metrics, or reconstruction behavior
must remain `requires-real-experiment` or `requires-human-review` until backed by
real evidence.

## Future Plan

Round 33.5 intentionally implements local co-location only. These routes are
future plans and should not be implemented in this round:

- remote handoff packages between machines
- NAS or shared-drive project links
- SSH readers for remote experiment hosts
- GitHub artifact download or upload workflows
- cloud artifact registries

Each future route needs its own contracts, threat model, fake-service tests,
budget/state ledger behavior, and human approval boundary.

