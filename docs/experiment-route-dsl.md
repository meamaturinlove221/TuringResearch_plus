# TuringResearch Plus Experiment Route DSL

Status: implemented minimal for v0.2 Sprint 2.

The Experiment Route DSL turns VGGT long-running plans into structured,
serializable route specs. It is a planning and validation layer only. It does
not run VGGT, run Modal, read private `D:/vggt` paths, or claim experiment
completion.

## Core Models

- `ExperimentRouteSpec`
- `ExperimentRouteStage`
- `ControllerPromptDraft`
- `ExperimentRouteCompileInput`

## Minimal Route Fields

- `route_id`
- `goal`
- `context`
- `allowed_inputs`
- `forbidden_actions`
- `stages`
- `hard_gates`
- `fallback_routes`
- `final_states`
- `artifact_requirements`
- `cleanup_requirements`
- `advisor_outputs`

## VGGT Fixture

- `examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml`
- `examples/vggt-human-prior-survey/route_specs/modal_sparseconv_prompt.md`

The fixture is explicitly `planned`, `requires-real-experiment`, and `not
executed by TuringResearch`.

## Tool Boundary

Proposed capsule-local tool:

- command: `turing route compile`
- tool: `experiment.route_compile`
- output: `ExperimentRouteSpec / ControllerPromptDraft`

This is not a frozen public MCP API until root contracts and `docs/mcp-tools.md`
accept it.
