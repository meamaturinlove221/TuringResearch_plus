# Long-term Strategy

Status: planning.

Round: 102.

TuringResearch Plus should become a research operating system: a local-first
workflow layer for organizing research intent, evidence, artifacts, experiments,
related work, advisors, dashboards, and release packages. It should not become a
black-box claim generator.

## Strategic Thesis

Modern research work fails less often from missing ideas than from missing
coordination:

- evidence is scattered across notes, logs, dashboards, and figures;
- remote artifacts arrive without provenance;
- paper reading and related-work positioning drift away from experiments;
- advisor updates become disconnected from hard gates;
- project templates are reinvented for each new direction.

TuringResearch Plus should make these pieces explicit, typed, reviewable, and
portable across projects.

## Strategic Pillars

### 1. Evidence-first Research

Every claim should connect to a source, artifact, run, paper, or explicit
unknown. Imported, retrieved, planned, and fake material must stay separate from
observed evidence.

### 2. Project Templates as Operating Units

The general research project template should become the unit of work. A project
contains intent, evidence ledger, artifact plan, route specs, related work,
advisor material, dashboards, and release boundaries.

### 3. Review-first Automation

Automation should assemble, check, compare, and summarize. It should not decide
truth. The human remains responsible for final evidence promotion, paper claims,
advisor-facing decisions, and public release approval.

### 4. Portable Artifact Ingest

Remote artifacts should enter through safe metadata and structured reports.
Remote sync, remote read, and remote execution outputs must remain safety-gated
and review-required.

### 5. Public Extension Boundaries

Plugins, MCP tools, and adapters should have explicit capability manifests,
contracts, test policies, and safety levels before marketplace-style exposure.

## Near-term Strategy

- Stabilize the v0.5 alpha product surfaces.
- Add multi-project workspace primitives.
- Generalize the VGGT knowledge pack into a reusable project package pattern.
- Build privacy/data/license gates into workspace workflows.
- Keep all live, remote, and binary export paths opt-in.

## Long-term Strategy

- Support a multi-project research dashboard.
- Support advisor communication suites across projects.
- Support plugin and MCP marketplace readiness.
- Support evidence-backed case studies.
- Add paper writing support as a claim-checked assistant, not an author.

## Decision Rules

- Prefer local deterministic workflows before live or remote workflows.
- Prefer manifests and proposed imports before copying large artifacts.
- Prefer Markdown/JSON/YAML outputs before binary exports.
- Prefer explicit limitations over polished but ambiguous outputs.
- Prefer project-level privacy gates before cross-project comparison.

## Hard Boundaries

- Do not promote planned, fake, retrieved, or imported material to observed.
- Do not treat remote artifacts as verified evidence.
- Do not automate paper conclusions.
- Do not transfer evidence between projects without review.
- Do not package secrets, raw data, or private model files.
- Do not claim experiment success without artifact-backed evidence.
