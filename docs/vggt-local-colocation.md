# VGGT Local Co-location Mode

Round 33.5 prepares TuringResearch Plus to dogfood against a VGGT checkout that
lives on the same Windows machine. The mode is documentation and configuration
only: it defines how a later workflow can discover local VGGT paths and summarize
readable files without modifying VGGT or running real experiments.

## Scope

- Project: `VGGT / SMPL-X Human Prior`
- Mode: `local-colocation`
- Access: read-only
- Example config: `examples/vggt-human-prior-survey/local_project_links.example.yaml`
- Private config: `local_project_links.yaml`, ignored by Git

Round 33.5 does not create cross-machine handoff logic, does not launch VGGT,
does not execute training or inference, and does not fabricate experiment
results.

This local co-location mode does not run VGGT.

## Read Boundary

The local co-location reader may inspect only allow-listed file types declared in
`local_project_links.yaml`. The example policy allows Markdown, text, JSON, YAML,
CSV, PNG/JPEG images, and `.npz` files.

`.npz` files are summary-only by default. A future reader may record keys, shapes,
dtypes, and small scalar metadata, but must not treat raw arrays as verified
metrics unless a real experiment report and human review support that claim.

## Write Boundary

TuringResearch Plus must not write inside a VGGT repository or output directory.
The local policy keeps these invariants explicit:

- never modify VGGT files
- never delete VGGT files
- never write inside a VGGT repository
- keep generated summaries inside TuringResearch Plus

Any path that is absent, unreadable, too large, or outside the allow-list should
be recorded as `missing`, `failed`, or `requires-human-review` instead of causing
the workflow to fail.

## Status Labels

The local co-location summary may use only the labels listed in the config:

- `observed`
- `planned`
- `fake-data`
- `failed`
- `hard-blocked`
- `requires-real-paper`
- `requires-real-experiment`
- `requires-human-review`

`observed` means a local file or directory was actually seen. It does not mean a
VGGT result is correct. Real result claims require real experiment evidence and
human review.

## Round 33.5 Readiness

Round 33.5 is ready when:

- the committed example config contains only candidate local paths and safety
  policy
- the real machine-specific `local_project_links.yaml` is ignored by Git
- documentation says missing paths are recorded, not fatal
- documentation states that remote handoff, NAS, SSH, and GitHub artifact routes
  are future plans only
- the focused workflow test passes without network access or VGGT execution
