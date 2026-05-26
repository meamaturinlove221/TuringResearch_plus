# Interview Storyline

Status: draft.

Round: 157.

This storyline explains TuringResearch Plus as an engineering and research
workflow project.

## 1. Background Problem

Research projects do not fail only because a model is wrong. They also fail
because evidence, artifacts, paper notes, run status, advisor feedback, and
next actions drift apart.

The problem is not simply automation. The problem is keeping a complex research
state honest.

## 2. Why Build This

TuringResearch Plus was built to make research status explicit:

- planned vs observed;
- evidence present vs missing;
- artifact ready vs incomplete;
- route viable vs blocked;
- claim safe vs unsafe;
- public-safe vs private.

The project favors review-first tooling over black-box automation.

## 3. Architecture

The system is a local-first Python monorepo with:

- workspace and project registry;
- evidence ledger and artifact audit;
- route DSL, hard gates, and failure taxonomy;
- paper digest, method cards, related work, and writing scaffold;
- dashboard and advisor export surfaces;
- plugin manifests, MCP registry, capability catalog, and sandbox policy;
- privacy, compliance, quality, and replay gates;
- modular namespace facades for future split readiness.

## 4. Engineering Difficulties

Important engineering challenges included:

- keeping fake/demo paths separate from live paths;
- preventing planned work from becoming observed evidence;
- preserving legacy imports while adding new namespace facades;
- making plugin loading useful without executing unknown code;
- designing privacy and compliance reports without pretending to provide legal
  advice;
- building public demos without leaking private project material;
- keeping release gates repeatable.

## 5. VGGT Dogfooding

VGGT is the dogfooding case. TuringResearch helped organize:

- research intent;
- evidence management;
- route changes;
- failures and blockers;
- advisor packs;
- dashboard summaries;
- paper scaffold;
- public case-study redaction.

The case is not presented as proof that VGGT experiments succeeded. SparseConv3D
success is not claimed.

## 6. Modular Evolution

The project started as one package and evolved toward internal module
boundaries:

- API contracts;
- namespace refactor plan;
- facade packages such as `turing_research_core` and
  `turing_research_plugins`;
- compatibility layer through `turing_research_plus`;
- readiness gates before any repository split.

## 7. Future Split Strategy

The short-term strategy is to keep the flagship repo complete. Future satellite
repos should appear only when they have stable APIs, complete docs, passing
tests, no private data, no license risk, and independent demo value.

Likely first split candidates:

1. `turingresearch-vggt-case`
2. `turingresearch-examples`

Core should not split early, because it carries the main research OS semantics.
