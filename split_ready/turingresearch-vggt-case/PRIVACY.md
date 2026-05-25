# Privacy And Public Safety

Status: draft privacy gate / requires human review
Round: Optional 338.5 integrated on newer cloud baseline

This skeleton is designed for future public case-study extraction review.

## Included

- Public-safe Markdown summaries.
- Claim-safety notes.
- Privacy posture.
- Metadata-level case narrative.
- Human review markers.

## Excluded

- Raw data.
- SMPL-X model files.
- Private machine paths.
- Huge arrays.
- Pointcloud files.
- Zip archives.
- Checkpoints.
- VGGT experiment bundles.
- API keys or secrets.
- Private advisor feedback.
- Unsupported experiment success claims.

## Current Gate Decision

The current package is documentation-only and public-safe as a draft. It still requires human review before release.

## Future Asset Rule

If future reviewers add screenshots, tables, or derived artifacts, they must rerun the privacy gate and prove that the added files contain no private paths, raw data, model files, huge artifacts, or unsupported claims.
