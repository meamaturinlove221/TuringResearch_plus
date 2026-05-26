# Public Release Hardening



Status: feature capsule skeleton.



## Problem



Before v0.4 release, docs, contracts, examples, packaging, and sensitive-file gates need a final hardening pass.



## VGGT motivating example



Remote artifact features increase risk of accidentally committing private configs, tokens, raw data, or stale planned/observed labels.



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



- `PublicReleaseHardeningReport`.

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



- command: `turing release harden`

- tool: `release.hardening_check`

- output: `PublicReleaseHardeningReport`



## Related contracts



- `contracts/public_release_hardening.yaml`

- `contracts/handoff_bundle.yaml`

- `contracts/run_ingest.yaml`



## Related skills



- `turingresearch-qa-release`

- `turingresearch-master-orchestrator`



## Required tests



- Fake/default workflow test.

- Missing credential or unavailable source test.

- Secret/raw-data/SMPL-X model exclusion test.

- JSON serialization test.

- Markdown export test.

- Evidence-boundary regression test.



## Risks



Release docs or examples overclaim live capabilities or leak sensitive paths.



## Done criteria



Name, secret, raw-data, package, docs, examples, and fake/live boundary gates pass before release prep.



## Release target



v0.4 release hardening



## Non-goals



- No default networking.

- No permission bypass.

- No automatic large-file download.

- No remote code execution.

- No saved secrets.

- No raw data or SMPL-X model file packaging.

- No remote artifact treated as verified evidence.

- No legacy project naming.
