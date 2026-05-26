# Skill SOP Style Guide

Status: v1.2 style guide.

Round: 240.

Use this guide when adding or hardening repo-scoped `turingresearch-*` skills.

## Required Sections

Every repo skill keeps the baseline structure:

- `Role`
- `When to use`
- `Inputs`
- `Outputs`
- `Required files`
- `Related contracts`
- `Related lanes`
- `Required tests`
- `Rules / constraints`
- `Done criteria`

Priority workflow skills also include a `Round 240 SOP Parity` section.

## SOP Field Style

Use lower_snake_case labels inside the SOP parity section:

- `workflow`
- `when_to_use`
- `inputs`
- `outputs`
- `safety`
- `non-goals`
- `handoff`
- `tests`
- `related_docs`

Keep each field short, concrete, and action-oriented. A skill should tell the
operator when to invoke it, what it consumes, what it returns, what it must not
do, and how to hand off results.

## Non-goals

Skill SOPs are not runtime code. They must not:

- execute skills automatically;
- enable live adapters by default;
- enable plugin execution;
- create releases, tags, or child repositories;
- read private paths without explicit round permission;
- claim planned or fake/demo work as observed.

## Tests

Each priority SOP must be covered by `tests/contract/test_skill_sop_parity.py`.
The existing skill integrity and routing tests must continue to pass.
