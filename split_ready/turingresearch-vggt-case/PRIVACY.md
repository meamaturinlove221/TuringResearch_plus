# Privacy

Status: draft privacy gate
Round: Optional 338.5
Date: 2026-05-25

## Included

- Public-safe Markdown summaries.
- Claim-safety notes.
- Privacy posture.
- Metadata-level case narrative.

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

## Current Gate Decision

The current package is documentation-only and public-safe as a draft. It still requires human review before release because the public safety checklist and original replication progress inputs were missing when this refresh ran.

## Future Asset Rule

If future reviewers add screenshots, tables, or derived artifacts, they must rerun the privacy gate and prove that the added files contain no private paths, raw data, model files, huge artifacts, or unsupported claims.
