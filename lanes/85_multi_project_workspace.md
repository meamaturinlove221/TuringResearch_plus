# Lane 85 - Multi-project Workspace

Status: implemented minimal.

Round: 104.

## Scope

Implemented a local read-only multi-project workspace registry for fake/demo
projects. This round did not migrate real data, access private VGGT paths, use
network access, upload data, or treat the workspace index as evidence.

## Added

- `src/turing_research_plus/workspace/`
- `contracts/multi_project_workspace.yaml`
- `docs/multi-project-workspace.md`
- `examples/workspaces/demo_workspace/`
- workspace unit tests
- workspace fake workflow test

## Demo Projects

- `vggt_human_prior`: review-only VGGT case mirror.
- `demo_medical_imaging`: fake/demo non-VGGT project with no real patient data.

## Boundaries

- VGGT is one project case, not the whole system.
- Demo medical imaging is fake/demo only.
- No real `D:/vggt` access.
- No upload.
- No network access.
- No automatic data ingestion.
- Workspace index is not an evidence source.
- No SparseConv3D success claim.
