# VGGT Local Scan Artifact Index

Round: Optional 367.5
Date: 2026-05-26
Index mode: metadata-only, no artifact copy

This index records lightweight local file evidence from the VGGT desktop
freshness recheck. It intentionally uses redacted evidence labels instead of
machine paths and does not copy VGGT artifacts into TuringResearch.

## Root Candidates

| Candidate | Status | Notes |
| --- | --- | --- |
| VGGT parent workspace | local-observed | Redacted local parent workspace existed during the recheck. |
| Primary VGGT main checkout | local-observed | Local checkout existed and exposed recent report metadata. |
| Feature-adapter checkout | local-observed | Local workspace existed and exposed tool/report metadata. |
| Alternate VGGT checkout A | local-observed | Alternate checkout existed; treated as contextual only. |
| Alternate VGGT checkout B | local-observed | Alternate checkout existed; treated as contextual only. |

## Lightweight Reports And Manifests

| Evidence class | Status | Notes |
| --- | --- | --- |
| V3000 final status metadata | local-observed | Small JSON metadata includes ready-not-promoted wording; not advisor promotion. |
| V2900 upload sidecar metadata | local-observed | Small JSON metadata includes hash/bundle checks; payloads remain external. |
| V2900 omitted-large-file metadata | local-observed | Small JSON metadata records an omission policy for large local files. |
| V2600 viewer metadata | local-observed | Viewer manifest metadata existed; viewer was not opened in this round. |
| V2010 training manifest metadata | local-observed | Small manifest metadata existed; no training command was run. |
| V2000/V2010 output listings | local-observed | File names were listed as metadata only; contents were not copied. |
| V600 quality rebuild report family | local-observed | Report metadata existed under the primary VGGT workspace. |
| V900/V930 feature-adapter reports | local-observed | Report and process metadata existed; not proof of promotion. |
| V120/V121 goal-manifest evidence | local-observed | Goal-manifest/tooling metadata existed; backend status remains review-gated. |

## Tool And Controller File Evidence

| Evidence class | Status | Notes |
| --- | --- | --- |
| V120 paper-grade surface backend tooling | local-observed | File presence only; not executed. |
| V121 mentor visual gate tooling | local-observed | File presence only; visual gate still requires human review. |
| V900/V930 teacher-distillation tooling | local-observed | File presence only; not executed. |
| V999 long-run controller family | local-observed | File presence only; no controller was run. |
| V2000/V2010 adapter training/eval tooling | local-observed | File presence only; no command was run. |

## Split Package Evidence

| Evidence class | Status | Notes |
| --- | --- | --- |
| split-ready case package | observed | `split_ready/turingresearch-vggt-case` exists as a public-safe documentation draft. |
| split-ready manifest | observed | Manifest keeps no raw data, no restricted model payload, and no unsupported claim boundaries. |
| split-manual case package | observed | `split_manual/turingresearch-vggt-case` exists as a manual human-review pack. |
| split-manual freshness check | observed | Existing freshness check marks the pack as fresh-manual-draft, requires-human-review. |

## Large Artifact Handling

- planned: large arrays, point clouds, archives, raw datasets, checkpoints, and restricted body-model files remain outside TuringResearch.
- local-observed: local metadata can describe hashes, sizes, or omitted payload categories.
- requires-human-review: any selected public asset must pass claim safety, privacy, and maintainer review before inclusion.
