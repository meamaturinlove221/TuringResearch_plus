# TulingResearch Plus FAQ

## What is TulingResearch Plus?

TulingResearch Plus is a Python MCP-first research workflow engine. It turns research intent, sources, and intermediate findings into typed, evidence-backed artifacts.

## Is it a live web research agent?

Not by default in `v0.1.0`. Default tests and examples use fake services, dry-run workflows, local fixtures, and adapter boundaries.

## What is the MCP server name?

`tulingresearch-plus`.

## Which Python packages are used?

- `tuling_research` for Core tools and PDF Markdown.
- `tuling_research_plus` for workflow layers.

## Does it require API keys?

No default test, example, or CI job requires real API keys. Future live tests must be marked `live` or `manual` and skipped by default.

## Does PDF Markdown require OCR?

No. Phase A uses a minimal local PyMuPDF route for local PDFs. Heavy OCR and complex layout parsing are future work.

## Why single-window multi-lane development?

The project coordinates parallel work through `lanes/`, `contracts/`, and `.agents/skills/` while keeping one repository, one package boundary, and one release ledger.

## What blocks paper draft generation?

The paper draft gate blocks full drafts until required artifacts are present, especially `ExperimentReport`.

## What blocks Race Mode implementation work?

Source Hygiene blocks private, leaked, NDA, proprietary, or incompatible-license material from becoming implementation tasks.

## Is this inspired by other public projects?

TulingResearch Plus references public research-tooling ideas, including Neocortica and Yogsoth AI references. They are references only; this project uses TulingResearch naming, packages, tools, docs, and skills.
