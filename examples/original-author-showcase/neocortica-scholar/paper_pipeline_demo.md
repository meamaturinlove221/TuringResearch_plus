# Scholar Paper Pipeline Showcase

## Source

- Upstream repository: `Pthahnix/Neocortica-Scholar`
- Source basis: README, scholar tool list, MCP usage guide, and paper workflow notes
- Upstream reference commit: `105ab8b7aa8d8db4b9c296e3c1c339b5952eabb1`
- Migration type: `adapted_with_authorization`
- Code migration: none

## Summary

This academic workflow output organizes paper work into a sequence of tool-facing operations rather than a single summary step. The workflow separates paper discovery, content access, reference extraction, structured reading, method-card creation, and downstream research planning.

## Pipeline

### 1. Paper Search

Collect candidate papers from a live or fake source. The output should retain title, authors, venue/date if available, source URL, and verification status.

### 2. Paper Content

Fetch or load public-safe content. This may come from cached markdown, abstracts, project pages, or user-provided notes. It must not silently import unauthorized full PDFs.

### 3. Paper Reference

Extract references and citations when available. Fake/demo references must remain labeled as fake or unverified.

### 4. Paper Reading

Run a structured reading process that records contribution, method, assumptions, experiments, limitations, and reproducibility notes.

### 5. Method Card

Turn the paper into a reusable method card: input, representation, model modules, training signal, evaluation, limitations, and what can be borrowed.

### 6. Research Route Input

Feed method cards into TuringResearch route planning, collision checks, experiment matrices, and advisor summaries.

## TuringResearch Demonstration

This showcase maps to:

- scholar tool surface;
- fake/live paper adapters;
- paper content and reference reports;
- three-pass reading template;
- method-card and related-work generation;
- collision risk detector;
- experiment route compiler.

## Safety Boundary

No paid paper, unauthorized PDF, API key, private note, or unverified citation is included here. Live paper lookup must be explicitly enabled.

## Attribution

Adapted with attribution from authorized Neocortica-Scholar workflow materials.
