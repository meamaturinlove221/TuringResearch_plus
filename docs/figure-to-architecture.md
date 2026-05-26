# TuringResearch Plus Figure-to-Architecture

Status: implemented minimal for v0.2 Sprint 2.

Figure-to-Architecture converts method cards and experiment routes into text
architecture diagrams. It produces Mermaid, Graphviz DOT, and Markdown. It does
not call image understanding models, third-party graph APIs, or network
services, and it does not fabricate paper figure content.

## Core Models

- `ArchitectureDiagramSpec`
- `ArchitectureNode`
- `ArchitectureEdge`
- `ArchitectureGroup`

## Exports

- Mermaid `flowchart TB`
- minimal Graphviz DOT
- Markdown summary with embedded Mermaid

## VGGT Examples

Generated example diagrams:

- `examples/vggt-human-prior-survey/architecture_diagrams/neuralbody_mapping.mmd`
- `examples/vggt-human-prior-survey/architecture_diagrams/humanram_mapping.mmd`
- `examples/vggt-human-prior-survey/architecture_diagrams/modal_sparseconv_route.mmd`

All fixture-derived diagrams must be treated as `derived-from-fixture` and
`requires-human-review`.

## Text Mapping Examples

NeuralBody-inspired fixture mapping:

```text
SMPL structured latent code
-> sparse voxel / SparseConvNet
-> latent volume
-> query decoder
```

TuringResearch VGGT mapping:

```text
SMPL-X voxel feature
-> SparseConv3D
-> geometry latent field
-> VGGT token / point residual
```

HumanRAM-inspired fixture mapping:

```text
SMPL-X canonical point
-> tri-plane neural texture
-> rasterized pose feature
-> transformer token
```

TuringResearch VGGT mapping:

```text
SMPL-X feature raster / tri-plane
-> VGGT token injection
-> human-region geometry refinement
```

Modal SparseConv3D route:

```text
local evidence ledger
-> route DSL
-> Modal sparse backend probe
-> voxel feature adapter
-> evaluation / hard gates
-> advisor pack
```

## Tool Boundary

Proposed capsule-local tool:

- command: `turing figure arch`
- tool: `paper.figure_to_architecture`
- output: `ArchitectureDiagramSpec`

This is not a frozen public MCP API until root contracts and `docs/mcp-tools.md`
accept it.
