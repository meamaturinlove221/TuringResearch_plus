# Main Repo Public Launch Plan

Status: planning draft.

Round: 163.

This plan prepares the flagship TuringResearch repository for a future
public launch. It does not publish the repository, create a release, tag a
commit, or make any claims about expected stars.

## Launch Goal

Make the main repo easy to understand, evaluate, star, and revisit while
keeping the positioning honest:

- local-first Research OS;
- fake/demo first;
- human review required;
- no automatic research completion;
- privacy-first public examples.

## README First Screen

The first screen should answer:

1. What is this?
   - Local-first Research OS for evidence-led research work.
2. Why should I care?
   - It keeps evidence, artifacts, routes, paper notes, dashboards, advisor
     packs, plugins, and review gates connected.
3. What can I inspect now?
   - public demo, VGGT dogfooding case, dashboard, advisor pack, plugin safety,
     tests.
4. What does it refuse to overclaim?
   - no automatic science, no final paper writing, no fake result success.

## Architecture Diagram

Launch page should point to:

- `examples/portfolio/turingresearch_architecture.mmd`
- `docs/interview-architecture-explanation.md`

The diagram should show:

- workspace registry;
- evidence ledger;
- artifact audit;
- route DSL;
- paper intelligence;
- advisor pack;
- dashboard;
- plugin safety;
- privacy/compliance/quality gates.

## Quickstart

Keep quickstart local and low-risk:

```powershell
python -m pip install -e .[dev]
python -m pytest -q
python -m mypy src
```

Optional MCP smoke path can stay documented, but live services must remain
opt-in.

## Public Demo

Primary demo path:

- `examples/public_demo/`
- `examples/public_demo/dashboard/`
- `examples/workspaces/demo_workspace/`

Public demo must state:

- fake/demo only;
- no raw data;
- no private paths;
- no API keys;
- no result success claims.

## VGGT Case Study

VGGT should be framed as dogfooding:

- useful for showing workflow discipline;
- useful for showing evidence management and claim safety;
- not proof of experiment success;
- no SparseConv3D success claim;
- no private data.

## Comparison With Ordinary Literature Tools

TuringResearch is broader than a literature summarizer:

| Ordinary literature tool | TuringResearch |
| --- | --- |
| summarizes papers | organizes evidence, artifacts, routes, paper review, dashboards, and release gates |
| focuses on text output | tracks status, missing evidence, and unsafe claims |
| may hide uncertainty | keeps planned vs observed explicit |
| rarely handles artifacts | audits artifacts and handoff readiness |
| usually not plugin-safe | uses manifest, sandbox policy, and compatibility checks |

## Fake / Live Boundary

Launch copy must repeat:

- default workflows are fake/demo;
- live adapters are optional;
- live tests are skipped by default;
- no real API key required;
- no default network access;
- no automatic remote experiment execution.

## Screenshots And Demo GIFs

Use the plans:

- `docs/project-screenshot-plan.md`
- `docs/demo-gif-plan.md`

No screenshot or GIF should show:

- private paths;
- raw data;
- model payloads;
- API keys;
- unsupported experiment claims.

## Issues And Discussions

Issue templates should invite:

- bug reports;
- feature requests;
- research workflow requests;
- public demo feedback;
- plugin manifest review questions;
- documentation clarity feedback.

Discussion topics can include:

- local-first research workflows;
- evidence ledger patterns;
- artifact audit patterns;
- plugin safety;
- dashboard/demo feedback;
- paper review workflows.

## Roadmap

Launch roadmap should be honest:

- v0.7: public RC posture, dashboard/export, plugin safety, compliance, case
  study, public demo expansion.
- v0.8: local server dashboard, paper writing beta, public plugin registry
  draft, more case studies, OS-level sandbox research.

Do not present roadmap items as shipped.

## License And Safety

Before launch:

- license posture must be explicit;
- compliance output must be described as not legal advice;
- plugin execution must remain disabled unless explicitly approved;
- public examples must pass privacy and hygiene gates;
- release blockers must be documented.

## Launch Decision

Current status: `planning-only`.

Do not launch until the checklist, safety review, README review, and maintainer
approval are complete.
