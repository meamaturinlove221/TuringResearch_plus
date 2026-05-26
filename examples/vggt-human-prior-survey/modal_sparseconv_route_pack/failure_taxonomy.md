# Modal SparseConv3D Failure Taxonomy

Status: planned taxonomy for future VGGT-side execution.

| Category | Meaning | Next Action |
| --- | --- | --- |
| `REAL_BACKEND_UNAVAILABLE` | Modal environment did not provide a usable real sparse backend. | Record backend logs, keep route blocked, do not fallback-promote. |
| `SPARSE_BACKEND_UNAVAILABLE` | `spconv`, `MinkowskiEngine`, and `TorchSparse` were absent or unusable. | Add backend install/probe report and retry only after environment fix. |
| `MISSING_ASSETS` | Required predictions, board files, NPZ diff, or manifest are absent. | Produce missing artifacts or keep package not-ready. |
| `VISUAL_PROOF_INSUFFICIENT` | Visual boards do not prove full-body, hairline, and hand/object behavior. | Generate board inventory and required close-up comparisons. |
| `HAIRLINE_REGRESSION` | Candidate damages hairline or head boundary behavior. | Keep candidate rejected and add focused visual comparison. |
| `HAND_OBJECT_CONFUSION` | Candidate worsens hands or object-like confusion. | Keep candidate rejected and add hand close-up evidence. |
| `FALLBACK_ONLY` | Route only uses fallback behavior, not real SparseConv3D. | Mark route failed; do not count as SparseConv3D evidence. |
| `REPORT_ONLY` | Output is a report without executable evidence artifacts. | Reject package and request concrete outputs. |
| `NOT_ENOUGH_EVIDENCE` | Evidence is incomplete for promotion. | Keep route planned or requires-human-review. |

## Attribution Rule

Every failure attribution must cite an evidence ref or explicitly set
`requires-human-review`. Missing evidence is not a reason to invent a cause.
