# Experiment Board Index

Status: v0.4 minimal metadata implementation.

The Experiment Board Index records board-like artifacts for run comparison. It
does not inspect image content. It only records whether board metadata exists,
whether a board is missing, and whether a board is proxy-only evidence such as a
mask, delta, heatmap, or other non-advisor-ready artifact.

## Supported Inputs

- run dashboard metadata;
- manual run summaries;
- board paths from fixture or scan metadata;
- missing visual inventory markers.

## Board Status

- `available`
- `missing`
- `proxy-only`
- `requires-human-review`

## VGGT Boundary

For VGGT runs, a board index is not proof of visual success. Full body,
hairline, hand close-up, and source visual provenance still need human review.
Proxy boards are useful for debugging, but they are not advisor-ready proof.

## Non-Goals

- No image understanding.
- No VGGT execution.
- No Modal execution.
- No private VGGT local path reads.
- No visual success claim from filenames.
