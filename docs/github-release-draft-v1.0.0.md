# GitHub Release Draft: v1.0.0

Status: draft text only.

Round: 196.

This file is a draft for a future GitHub Release. It does not create a tag,
publish a release, upload artifacts, or publish to PyPI.

## Title

TuringResearch Plus v1.0.0-rc0 - Local-first Research OS

## Summary

TuringResearch Plus v1.0.0-rc0 is a release-candidate snapshot of a
local-first Research OS for evidence-led research workflows. It focuses on
reviewable research state: evidence ledgers, artifact audits, paper
intelligence, route planning, advisor packs, dashboards, plugin safety,
public demos, and release gates.

The default path is fake/demo-first. Live adapters are optional and disabled by
default. Human review remains required for claims, compliance, release actions,
and any real experiment interpretation.

## Highlights

- Local-first Research OS.
- Multi-project workspace.
- Evidence / Artifact / Visual / Advisor surfaces.
- Paper / Citation / Related Work / Collision Risk workflows.
- Experiment Route DSL / Hard Gates / Failure Taxonomy.
- Remote Artifact / Handoff / Run Ingest review surfaces.
- Dashboard / Advisor Export with optional PDF/PPTX backends.
- Plugin Manifest / Safety / MCP registry.
- Campaign Catalog and MCP fake/live configuration polish.
- Pod Context Lifecycle Safety Plan.
- Public Demo suite.
- VGGT public-safe case study.
- Modular monorepo and future split strategy.

## Quickstart

```bash
python -m pip install -e .[dev]
python -m pytest tests/workflow/test_v1_public_quickstart_fake.py -q
```

See:

- `docs/v1.0.0-quickstart.md`
- `examples/public_demo/QUICKSTART.md`

## Demo Link

Use the local public demo:

- `examples/public_demo/README.md`
- `examples/public_demo/WALKTHROUGH.md`
- `examples/public_demo/dashboard/index.html`

The demo is demo-only. It does not require API keys, private VGGT data,
restricted model files, or network access.

## VGGT Case Study Note

The VGGT case study is a public-safe dogfooding example. It demonstrates how
TuringResearch organizes evidence, artifacts, advisor packs, dashboards, and
claim-safety review.

It is not a VGGT experiment source repository and does not claim final
experiment success.

See:

- `docs/vggt-case-study-public.md`
- `examples/vggt-human-prior-survey/public_case_study/`
- `split_ready/turingresearch-vggt-case/`

## Installation

```bash
python -m pip install -e .[dev]
```

For MCP-oriented local checks:

```bash
python -m pip install -e .[dev,mcp]
```

Package identity:

- package: `turingresearch-plus`
- compatibility namespace: `turing_research_plus`
- MCP command: `turingresearch-plus-mcp`

## Changelog

See:

- `CHANGELOG.md`
- `docs/v1.0.0-release-notes.md`
- `docs/v1.0.0-feature-list.md`

## Safety Note

- No SaaS.
- No cloud user system.
- No default live networking.
- No automatic experiment execution.
- No automatic final paper writing.
- No unknown third-party plugin execution.
- No physical split repositories by default.
- Compliance assistant output is not legal advice.
- Fake/demo outputs must not be treated as observed results.

## Known Issues

- Optional PDF/PPTX backends may skip gracefully when dependencies are missing.
- Plugin sandboxing is policy-level, not OS-level sandboxing.
- Live adapters require explicit opt-in and user-supplied credentials.
- Campaign routing is deterministic and does not replace the master
  orchestrator.
- Pod context lifecycle is safety planning only and does not run SSH, Modal,
  tmux, or remote commands.

## Next Roadmap

- Final public launch review.
- Human review of README, quickstart, release notes, and safety posture.
- Optional post-launch creation of `turingresearch-vggt-case` after approval.
- Optional post-launch creation of `turingresearch-examples` after feedback.
- Longer-term plugin ecosystem review before any standalone plugins repo.
- Continued API stability and public demo hardening.
