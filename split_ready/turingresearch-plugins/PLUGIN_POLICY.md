# Plugin Policy

Status: skeleton policy.

This policy applies to the future `turingresearch-plugins` split candidate.

## Required For Every Plugin

- plugin manifest;
- permissions declaration;
- safety level;
- config schema;
- input and output schema;
- docs;
- tests or test plan;
- sandbox policy review;
- extension safety report;
- compatibility report;
- human review.

## Defaults

- third-party plugins disabled by default;
- no unknown Python entrypoint loading;
- no plugin code execution by default;
- no `execute_code` by default;
- no secrets access;
- no core tool override;
- live/network access opt-in only.

## Release Blockers

- missing manifest;
- missing permissions;
- missing safety level;
- enabled third-party plugin;
- secrets access request;
- execute-code request without approved future sandbox;
- shell access request without approved future sandbox;
- core namespace override;
- failed compatibility report;
- missing human review.

## Flagship Boundary

The main TuringResearch Plus repository keeps the core plugin framework and
policy implementation. This skeleton is a catalog and contribution surface
only.
