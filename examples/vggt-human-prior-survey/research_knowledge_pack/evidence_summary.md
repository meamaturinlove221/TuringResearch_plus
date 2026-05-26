# Evidence Summary

## Status Buckets

### observed

- V129: SMPL-X anchored completion is recorded as engineering context.
- V900: Feature adapter entrypoint is recorded as observed engineering context.
- V930: HumanRAM-style tri-plane adapter has an observed short-training signal.
- V999: Long-run tri-plane-only route status is observed as engineering context.

### local-observed

- V770: Diagnostic crop residual milestone is tracked as local dogfooding context.

### planned

- Modal Real SparseConv3D route.
- SMPL-X voxel feature encoding route.
- Future artifact-backed run ingest from VGGT-side outputs.

### hard-blocked

- V260: Required semantic assets are unavailable in the current scan.

### not-enough-evidence

- V999-SparseConv3D: no local evidence ledger, backend artifact, or run output
  confirms SparseConv3D success.
- `modal_sparseconv_v0`: current fixture ingest proposes `not-enough-evidence`.

### requires-human-review

- V120: no committed local evidence ledger JSON.
- V121: no committed local visual inventory.
- Related work claims: fake/manual method cards and citation graph are not enough
  for final related-work claims.
- Visual readiness: full body, hairline, and hand close-up evidence are missing.

## Evidence Boundary

Missing evidence is not negative proof and is not success proof. Any final claim
must be backed by a source artifact, evidence reference, and human review when
the evidence is ambiguous.
