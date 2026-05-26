# Modal SparseConv3D Artifact Requirements

Status: planned artifact checklist for future VGGT-side execution.

## Required Files

| Artifact | Purpose | Promotion Required |
| --- | --- | --- |
| `final_status.json` | Machine-readable route status and evidence state | yes |
| `ranked_candidates.csv` | Candidate ranking and metric summary | yes |
| `predictions.npz` or thin summary | Candidate prediction evidence without loading huge arrays in review | yes |
| board inventory | Visual proof index for full body, hairline, and hand/object boards | yes |
| advisor summary | Human-readable summary for advisor review | yes |
| failure report | Required on blocked, failed, or incomplete route | yes |
| sha256 manifest | Integrity check for all important artifacts | yes |
| cleanup report | Confirms private paths and temporary files were excluded | yes |

## Thin Summary Rules

If `predictions.npz` is too large to move, provide a thin summary with keys,
shapes, dtypes, file size, and hashes. Do not load huge arrays only for a
summary.

## Not Ready Conditions

- Missing board inventory.
- Missing NPZ diff or thin prediction summary.
- Missing backend probe.
- Missing cleanup report.
- Missing hashes.
- Any candidate marked successful without hard gate evidence.
