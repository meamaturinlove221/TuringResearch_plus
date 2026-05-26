# TuringResearch Plugins

Status: split-repo skeleton / not a real repository.

This skeleton shows what a future `turingresearch-plugins` repository could
look like.

The flagship TuringResearch Plus repository keeps the core plugin framework,
runtime policy, package install path, release gates, and safety tests.

## Purpose

This future repo would host plugin metadata and review artifacts:

- plugin manifests;
- compatibility reports;
- contribution guidelines;
- review checklists;
- disabled-by-default registry drafts;
- fake/demo plugin examples.

## Safety Boundary

- Third-party plugins are disabled by default.
- Plugin manifest is required.
- Sandbox policy review is required.
- Extension safety report is required.
- Compatibility report is required.
- Human review is required.
- `execute_code` is denied by default.
- Secrets access is forbidden.
- Unknown plugin code is not executed.
- Plugin tools cannot override core tools.

## What This Is Not

- Not the core plugin runtime.
- Not an online marketplace.
- Not a trusted execution environment.
- Not an approval to run third-party code.

## Current Status

Design-only. Do not publish or extract this skeleton until plugin safety,
compatibility, and review workflows pass as an independent gate.
