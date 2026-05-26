# TuringResearch Examples

The `examples/` tree contains fake/demo and local fixture material for
TuringResearch. Examples are designed for public-safe walkthroughs and
regression tests. They are not experiment results.

## Public Demo

`examples/public_demo/` is the recommended public walkthrough.

It includes:

- a root demo suite;
- expanded demo projects for VGGT-like, paper survey, and software tooling
  workflows;
- a public demo workspace;
- a static dashboard index.

See [Public Demo Guide](public-demo-guide.md).

For the v1 public path, also see:

- [v1.0 Public Quickstart](v1.0.0-quickstart.md)
- [v1.0 Public Demo Walkthrough](v1.0.0-public-demo-walkthrough.md)
- `examples/public_demo/QUICKSTART.md`
- `examples/public_demo/WALKTHROUGH.md`
- `examples/public_demo/EXPECTED_OUTPUTS.md`

## VGGT Dogfooding Case

`examples/vggt-human-prior-survey/` is a dogfooding case. It demonstrates how
the system organizes evidence, routes, failures, advisor material, compliance
notes, and case-study drafts.

It is not proof of experiment success. See
[VGGT Public Case Study](vggt-case-study-public.md).

## Workspace Demo

`examples/workspaces/demo_workspace/` demonstrates multi-project workspace
indexing and cross-project graph summaries with fake/demo projects.

## Benchmark Replay

`examples/benchmarks/` contains fake/default replay scenario declarations.

## Legacy Release Examples

The older release-candidate dry-run examples remain for regression coverage:

- `examples/citation-graph-demo/`
- `examples/pdf-to-markdown-demo/`
- `examples/smplx-feature-adapter-hypothesis/`
- `examples/vggt-human-prior-survey/`

## Rules

Examples must not require real API keys, live network calls, private sources,
private project folders, private model files, or data payloads. Planned or demo
items must not be marked as observed evidence.

## Split-ready Bundles

`split_ready/` contains local export bundles for future human-approved spoke
repositories. These bundles are not published GitHub repositories and are not
install targets. See [Split-ready Bundles](split-ready-bundles.md).
