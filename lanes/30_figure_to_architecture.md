# Lane 30: Figure-to-Architecture

Round 49 implements the minimal Figure-to-Architecture text diagram workflow.

## Implemented

- `src/turing_research_plus/architecture/`
- `contracts/architecture_diagram.yaml`
- `docs/figure-to-architecture.md`
- `examples/vggt-human-prior-survey/architecture_diagrams/`
- focused unit and workflow tests

## Boundaries

- No image understanding model.
- No third-party graph API.
- No network.
- No fabricated paper figure content.
- Fixture-derived diagrams require human review.
- Outputs are text only: Mermaid, DOT, Markdown.

## Consumes

- Paper Method Cards.
- Experiment Route DSL specs.
- PDF Phase B / figure registry concepts.

## Next Step

Use architecture specs as inputs for advisor packs or future paper figure
registry updates only after human review.
