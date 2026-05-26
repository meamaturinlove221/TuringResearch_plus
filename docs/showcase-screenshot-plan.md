# Showcase Screenshot Plan

Status: screenshot plan only.

Round: 220.

This plan defines screenshots to capture after human review. It does not
generate or fake screenshots.

## Required Screenshots

| Asset | Source | Purpose | Status |
| --- | --- | --- | --- |
| README first screen | `README.md` rendered on GitHub | Project pitch | planned |
| Research OS architecture | `docs/architecture-diagram-final.mmd` | Architecture overview | planned |
| Public demo walkthrough | `examples/public_demo/WALKTHROUGH.md` | Demo path | planned |
| Evidence ledger | `examples/public_demo/demo_evidence_ledger.json` | Evidence states | planned |
| Artifact audit | `examples/public_demo/demo_artifact_index.md` | Artifact review | planned |
| Dashboard | `examples/public_demo/demo_dashboard_refined.html` | Review UI | planned |
| Dashboard Data API JSON | Dashboard API public demo export | Read-only data layer | planned |
| Local server dashboard | localhost preview | Local-only route view | planned |
| VGGT claim safety | `split_ready/turingresearch-vggt-case/CLAIM_SAFETY.md` | Claim boundary | planned |

## Capture Rules

- Do not include API keys.
- Do not include private local paths.
- Do not include raw private data.
- Do not include restricted model files.
- Do not show fake/demo material as observed evidence.
- Do not imply that split-ready bundles are published child repositories.
- Mark generated screenshots as showcase assets after human review.

## Output Location

Future reviewed screenshots can be placed under `assets/screenshots/`. Until
they are captured, the checklist remains the source of truth.
