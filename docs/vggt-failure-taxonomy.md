# TuringResearch Plus VGGT Failure Taxonomy

This document maps VGGT dogfooding failure signals to the minimal Failure
Taxonomy Engine.

| VGGT signal | Category | Boundary |
| --- | --- | --- |
| V260 missing adjacent predictions / semantic assets | `MISSING_ASSETS` | hard-blocked until assets exist |
| SparseConv3D backend unavailable | `REAL_BACKEND_UNAVAILABLE` / `SPARSE_BACKEND_UNAVAILABLE` | requires real backend evidence |
| missing board proof | `VISUAL_PROOF_INSUFFICIENT` | not advisor-ready |
| V129 hairline degradation | `HAIRLINE_REGRESSION` | requires visual comparison |
| fallback-only path | `FALLBACK_ONLY` | cannot be promoted |
| report-only output | `REPORT_ONLY` | artifacts required |
| no real experiment evidence | `NOT_ENOUGH_EVIDENCE` | no success claim |

## Non-Claims

- The taxonomy does not run VGGT.
- The taxonomy does not inspect private `D:/vggt` paths.
- The taxonomy does not prove SparseConv3D success.
- The taxonomy does not replace human review.
