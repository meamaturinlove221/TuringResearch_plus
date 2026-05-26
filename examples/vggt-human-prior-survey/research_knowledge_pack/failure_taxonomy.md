# Failure Taxonomy

## Current Blockers

- V260: `MISSING_ASSETS` / hard-blocked due to missing adjacent predictions or
  semantic assets.
- V999-SparseConv3D: `NOT_ENOUGH_EVIDENCE` because no real backend artifact or
  evidence ledger entry confirms success.
- Modal SparseConv3D fixture: `REAL_BACKEND_UNAVAILABLE`,
  `SPARSE_BACKEND_UNAVAILABLE`, `MISSING_ASSETS`,
  `VISUAL_PROOF_INSUFFICIENT`, and `PACKAGE_INCOMPLETE`.
- Visual readiness: missing board inventory, full body, hairline, and hand
  close-up evidence.

## Recurring Failure Modes

- `REPORT_ONLY`: narrative output without artifacts.
- `FALLBACK_ONLY`: fallback path used instead of real sparse route.
- `IDENTITY_COPY`: unchanged baseline output presented as progress.
- `MISSING_ASSETS`: required predictions, boards, NPZ diff, or manifest absent.
- `VISUAL_PROOF_INSUFFICIENT`: visual proof does not cover full body, hairline,
  and hand/object behavior.
- `NOT_ENOUGH_EVIDENCE`: route status exists but promotion evidence is absent.

## Next Mitigation

1. Require real sparse backend probe logs before any SparseConv3D promotion.
2. Require predictions or a thin prediction summary.
3. Require board inventory and visual close-up evidence.
4. Require sha256 manifest and cleanup report.
5. Generate failure analysis even when the route fails or is blocked.
