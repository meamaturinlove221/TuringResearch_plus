# VGGT Local Scan Missing Items

Round: Optional 337.5
Date: 2026-05-25

## Missing Or Private Inputs

| Item | Status | Impact |
| --- | --- | --- |
| `examples/vggt-human-prior-survey/local_project_links.yaml` | private/missing | Private config is intentionally not committed. |
| exact local VGGT path inventory | redacted | Current cloud baseline keeps public-safe summaries instead of private paths. |
| public release approval | requires-human-review | Split readiness cannot be promoted automatically. |

## Missing Or Unconfirmed VGGT Evidence

| Claim or marker | Status | Notes |
| --- | --- | --- |
| Modal real spconv backend success | requires-human-review | V120/V121-related files exist, but this scan did not confirm backend success. |
| Advisor final approval | requires-human-review | No local file should be interpreted as final advisor acceptance. |
| Promotion decision | requires-human-review | Local reports distinguish review-ready or ready-not-promoted states from promotion. |
| True public split readiness | requires-human-review | Requires public safety review, claim safety review, and maintainer approval. |

## Current Cloud Baseline Note

The newer TuringResearch Plus cloud branch includes public case-study builder docs, original-repo replication docs, and split-ready/manual pack scaffolding. Those files make the repo more complete than the original Round 337.5 scan-time branch, but they do not upgrade any local-only claim to public observed status.

## Out Of Scope By Policy

- planned: no VGGT experiment execution.
- planned: no VGGT code execution.
- planned: no raw data copy.
- planned: no SMPL-X model file copy.
- planned: no huge npz, ply, zip, or VGGT bundle copy.
- planned: no external child repository creation or push.
