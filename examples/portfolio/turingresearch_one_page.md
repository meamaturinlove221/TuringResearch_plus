# TuringResearch One-Page Portfolio

## What It Is

TuringResearch is a local-first Research OS for evidence-led research
workflows. It helps organize evidence, artifacts, routes, paper review,
dashboards, advisor packs, plugins, privacy gates, and replay checks.

## Why It Matters

Research project state often scatters across notes, run folders, papers,
dashboards, and messages. TuringResearch makes that state explicit and
reviewable.

## Core Capabilities

- Evidence Ledger: track claim status and missing evidence.
- Artifact Auditor: check whether files and outputs are ready to support work.
- Route DSL: describe experiment plans, hard gates, failures, and next actions.
- Paper Intelligence: digest papers and build review-first writing scaffolds.
- Dashboard: static local project status surfaces.
- Advisor Pack: summarize current state and decisions needed.
- Plugin System: manifest-first plugin registry and sandbox policy.
- Privacy/Safety: scans, redaction plans, compliance checklists, release gates.

## VGGT Dogfooding

The VGGT case shows how the system organizes a real research workflow:
intent, evidence, route changes, failures, advisor communication, dashboard,
paper scaffold, redaction, and claim safety.

It does not claim experiment success.

## Engineering Highlights

- monorepo to modular facade namespaces;
- legacy compatibility layer;
- contract tests and import compatibility checks;
- fake/live boundary;
- privacy-first public demos;
- plugin safety before runtime execution;
- full fake replay and release gates.

## What It Does Not Do

- no automatic research completion;
- no automatic experiment execution;
- no final paper writing;
- no replacement for human review;
- no legal compliance guarantee;
- no default live networking.

## Interview Hook

> I built this as a local-first research operating system: not to replace the
> researcher, but to make evidence, artifacts, routes, paper claims, and safety
> boundaries visible enough to review.
