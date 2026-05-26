# Method Section Builder

Status: implemented minimal.

The Method Section Builder turns local method-card fixtures, architecture
diagram placeholders, and route DSL specs into an evidence-linked method
section skeleton. It is a writing scaffold, not final method prose.

## Inputs

- Method cards under `examples/vggt-human-prior-survey/paper_method_cards/`
- Mermaid architecture diagrams under
  `examples/vggt-human-prior-survey/architecture_diagrams/`
- Route specs under `examples/vggt-human-prior-survey/route_specs/`

## Outputs

- `method_section_skeleton.md`
- `method_figure_links.md`

## Skeleton Sections

- Problem setting
- Overview
- SMPL-X feature encoding
- VGGT integration
- Route variants
- Hard gates
- Implementation notes
- Limitations
- Figure placeholders
- Evidence refs

## Safety Boundary

- No method verification is claimed.
- No final contribution claims are generated.
- No experiment, metric, ablation, figure, or table is fabricated.
- SparseConv3D success is not claimed.
- Route variants remain planned / requires-real-experiment unless evidence
  changes.
- Human review is required before drafting paper prose.

## Non-goals

- No final method section.
- No final contribution claim generation.
- No fake figures.
- No fake experiments.
- No network access.
- No private VGGT path access.

## Tests

- `tests/unit/test_method_section_builder.py`
- `tests/unit/test_method_templates.py`
- `tests/unit/test_figure_linker.py`
- `tests/workflow/test_vggt_method_section_skeleton.py`
