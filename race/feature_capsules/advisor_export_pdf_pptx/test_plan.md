# Test Plan: Advisor PDF / PPTX Export



Status: skeleton.



## Required tests



- Fake/default path requires no network.

- Missing credential or source returns a graceful skipped/blocked report.

- `.env`, secrets, raw data, cache folders, and SMPL-X model files are denied.

- Large files are manifest-only or summary-only by default.

- Output serializes to JSON.

- Markdown review summary includes limitations.

- Remote/retrieved/indexed artifacts are not marked as human verified.

- Planned work is not promoted to observed evidence.



## Workflow fixture



Use a small VGGT review fixture derived from existing handoff, run ingest, or

knowledge-pack examples. Do not read private VGGT paths.



## Live/manual tests



Any live remote access must be marked live/manual and skipped by default.
