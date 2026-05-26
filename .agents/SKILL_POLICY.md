# TuringResearch Skill Selection Policy

Status: active.

## Purpose

This policy explains how to choose repo-scoped `turingresearch-*` skills. It is
a routing layer, not an agent runtime.

## Selection Rules

1. Prefer the most specific skill for the task category.
2. If a request spans multiple lanes, use `turingresearch-master-orchestrator`.
3. If a request changes contracts, include `turingresearch-architecture-contracts`.
4. If a request is about release, packaging, docs, or tests, include
   `turingresearch-qa-release`.
5. Routing recommendations must not execute tools automatically.

## Safety Rules

- Default workflows must stay offline unless a round explicitly allows live
  access.
- Live results are retrieved, not human verified.
- Planned work must not be written as observed evidence.
- Private paths and secrets must not be routed into public artifacts.
- SparseConv3D success requires evidence-ledger proof.

## Missing Route

If no route matches, use `turingresearch-master-orchestrator` and record the
missing route in the relevant lane or issue ledger.
