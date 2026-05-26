# VGGT Case Public Safety Checklist

Status: design checklist.

Round: 159.

Use this checklist before extracting `turingresearch-vggt-case` into any future
public repository.

## Data Safety

- [ ] No private local paths.
- [ ] No raw data.
- [ ] No private data folders.
- [ ] No SMPL-X model files.
- [ ] No model checkpoints.
- [ ] No large `npz` prediction payloads.
- [ ] No API keys or tokens.
- [ ] No private advisor feedback.

## Claim Safety

- [ ] No unsupported experiment success claims.
- [ ] No planned route described as executed.
- [ ] No dashboard view described as paper evidence.
- [ ] No SparseConv3D success claim.
- [ ] No final research conclusion claim.
- [ ] Human review requirement remains visible.

## License And Compliance

- [ ] Compliance disclaimer included.
- [ ] Third-party paper figures are not bundled.
- [ ] License-restricted files are not bundled.
- [ ] Unknown license items are marked for review.
- [ ] Public release decision remains maintainer-owned.

## Flagship Strategy

- [ ] README links back to flagship repo in the first section.
- [ ] README states the flagship remains the install and star entry point.
- [ ] The case repo does not duplicate the main package release story.
- [ ] The case repo does not imply it replaces TuringResearch.

## Required Reports

- [ ] Redaction report present.
- [ ] Claim safety report present.
- [ ] Privacy note present.
- [ ] Manifest present.
- [ ] Human review marker present.

## Current Round 159 Status

The current skeleton is design-only and not approved for extraction.
