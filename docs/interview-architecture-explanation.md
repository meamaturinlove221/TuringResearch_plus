# Interview Architecture Explanation

Status: portfolio draft.

Round: 158.

## Architecture Summary

TuringResearch Plus is a local-first Python monorepo organized around research
state rather than a single model or paper pipeline.

The system has four main layers:

1. Project state layer:
   - workspace registry;
   - project templates;
   - evidence ledger;
   - artifact index;
   - privacy and quality reports.

2. Research workflow layer:
   - route DSL;
   - hard gates;
   - failure taxonomy;
   - paper digest;
   - method cards;
   - related work;
   - paper writing scaffold.

3. Presentation and review layer:
   - dashboard;
   - advisor pack;
   - optional PDF/PPTX export;
   - vault UI;
   - public case-study builder.

4. Extension and release layer:
   - plugin manifest registry;
   - MCP plugin registry;
   - capability manifest;
   - sandbox policy;
   - compatibility harness;
   - replay and regression gates.

## Monorepo To Modular Architecture

The project stays in one flagship repo while internal modules become clearer.
New facade namespaces provide future boundaries:

- `turing_research_core`
- `turing_research_paper`
- `turing_research_artifact`
- `turing_research_experiment`
- `turing_research_dashboard`
- `turing_research_plugins`
- `turing_research_cases`

The compatibility namespace `turing_research_plus` remains supported.

## Why This Architecture

Research workflows need traceability more than blind automation. The
architecture is designed so a reviewer can ask:

- What is the claim?
- What evidence supports it?
- Which artifact proves it?
- Which route produced it?
- What failed?
- What is still missing?
- Is it public-safe?

## Key Boundary

The system does not treat dashboards, graphs, or paper scaffolds as truth. They
are review surfaces. Human review is required before publication, release, or
experiment claims.
