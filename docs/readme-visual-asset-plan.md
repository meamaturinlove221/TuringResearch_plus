# README Visual Asset Plan

Status: planning draft.

Round: 164.

This plan defines the visual assets needed for a future public README polish.
It does not generate complex images, screenshots, or GIFs.

## Asset Goals

- make the Research OS architecture visible quickly;
- show fake/demo and privacy boundaries;
- make dashboard and case-study surfaces concrete;
- avoid overclaiming research results;
- avoid leaking private data.

## Required Diagrams

1. Research OS overview.
2. Evidence to Advisor flow.
3. Paper to Method Card flow.
4. Experiment Route to Run Ingest flow.
5. Plugin / Skill routing.
6. VGGT dogfooding case.

## Files

- `docs/architecture-diagram-final.mmd`
- `docs/research-os-flow.mmd`
- `docs/vggt-case-flow.mmd`
- `docs/plugin-system-flow.mmd`
- `docs/dashboard-screenshot-checklist.md`
- `docs/demo-gif-script.md`
- `examples/assets/asset_manifest.yaml`

## README Placement

Recommended README section:

```markdown
## Visual Tour

- Architecture diagrams: `docs/architecture-diagram-final.mmd`
- Research OS flow: `docs/research-os-flow.mmd`
- VGGT dogfooding flow: `docs/vggt-case-flow.mmd`
- Plugin safety flow: `docs/plugin-system-flow.mmd`
- Screenshot/GIF plans: `docs/dashboard-screenshot-checklist.md`,
  `docs/demo-gif-script.md`
```

## Safety Rules

- Use public-safe fake/demo material only.
- Do not show private paths.
- Do not show raw data.
- Do not show model payloads.
- Do not show API keys or tokens.
- Do not imply VGGT or SparseConv3D success.
- Do not present dashboard views as research evidence.
