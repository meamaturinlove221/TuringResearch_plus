# Internship Portfolio Pack

Status: portfolio draft.

Round: 158.

TuringResearch Plus is a local-first Research OS portfolio project. It shows
how to turn a messy research workflow into a structured system for evidence,
artifacts, routes, paper review, dashboards, advisor communication, plugins,
privacy gates, and release checks.

## One-Minute Pitch

TuringResearch Plus helps researchers keep project state honest. It separates
planned work from observed evidence, audits artifacts before they become claims,
tracks route and failure status, scaffolds paper sections without inventing
results, and packages project status into dashboards and advisor packs.

The project is local-first and fake/demo-first by default. Live adapters are
optional, unknown plugins are not executed, and human review remains required.

## What To Show

1. README first screen.
2. Public demo suite.
3. Refined static dashboard.
4. Evidence ledger and artifact audit examples.
5. Route DSL and failure taxonomy.
6. Paper scaffold and deep review mode.
7. Plugin manifest / sandbox / compatibility story.
8. VGGT dogfooding case study with redaction and claim guard.
9. Test and contract gates.
10. Modular monorepo strategy and future split plan.

## Technical Coverage

- Monorepo to modular architecture:
  - `turing_research_plus` remains compatibility namespace.
  - `turing_research_core`, `turing_research_paper`,
    `turing_research_artifact`, `turing_research_experiment`,
    `turing_research_dashboard`, `turing_research_plugins`, and
    `turing_research_cases` act as facade namespaces.
- Evidence:
  - ledgers, claim safety, planned vs observed.
- Artifact:
  - audit, handoff, remote metadata, readiness reports.
- Route:
  - DSL, hard gates, failure taxonomy, next actions.
- Paper:
  - digest, method cards, related work, writing scaffold, deep review.
- Dashboard:
  - static HTML/Markdown project status surfaces.
- Plugin:
  - manifest-only registry, trusted local loading, sandbox policy,
    compatibility harness, MCP mapping.
- Safety:
  - privacy scan, compliance checklist, release hygiene, quality gate.
- Testing:
  - unit tests, workflow tests, contract tests, replay tests, mypy, ruff.

## Interview Angle

This project is strongest when framed as engineering judgment:

- it avoids overclaiming;
- it treats data and privacy as first-class constraints;
- it uses contracts to manage module boundaries;
- it keeps live systems optional;
- it turns research ambiguity into reviewable state.

## What Not To Say

- Do not say it automatically completes research.
- Do not say it writes final papers.
- Do not say it ran or solved VGGT experiments.
- Do not say it replaces advisor or human review.
- Do not say compliance output is legal advice.

## Supporting Documents

- `docs/interview-architecture-explanation.md`
- `docs/interview-technical-highlights.md`
- `docs/interview-star-stories.md`
- `docs/interview-faq.md`
- `docs/interview-demo-script.md`
- `examples/portfolio/turingresearch_one_page.md`
- `examples/portfolio/turingresearch_architecture.mmd`
