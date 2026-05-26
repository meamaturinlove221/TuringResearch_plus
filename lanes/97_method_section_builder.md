# Lane 97 - Method Section Builder

Status: implemented minimal.

## Scope

Round 116 adds a method-section skeleton builder for the paper assembly line.
It links method-card fixtures, architecture diagram placeholders, and route DSL
specs into Markdown skeletons for human review.

## Added

- `src/turing_research_plus/paper_write/method_builder.py`
- `src/turing_research_plus/paper_write/method_templates.py`
- `src/turing_research_plus/paper_write/figure_linker.py`
- `contracts/method_section_builder.yaml`
- `docs/method-section-builder.md`
- VGGT method skeleton examples in
  `examples/vggt-human-prior-survey/paper_scaffold/`
- method section unit and workflow tests

## Outputs

- `method_section_skeleton.md`
- `method_figure_links.md`

## Boundaries

- No final method prose.
- No method verification claim.
- No final contribution claim.
- No fabricated figures or experiments.
- SparseConv3D success is not claimed.
- Human review is required.
