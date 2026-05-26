# Skill SOP Parity

Status: v1.2 parity implementation.

Round: 240.

This round aligns TuringResearch's repo-scoped skills with the operator-friendly
SOP style used by the reference split repositories. The goal is to make key
workflows directly callable from `.agents/ENTRY.md` and `.agents/ROUTING_TABLE.md`
without adding a new agent runtime.

## Scope

The following workflows now have explicit SOP parity fields in their primary
`SKILL.md` files:

| Workflow | Primary skill |
| --- | --- |
| master orchestrator | `turingresearch-master-orchestrator` |
| upstream watch | `turingresearch-race-upstream-watch` |
| campaign catalog | `turingresearch-fusion-campaign-engine` |
| scholar pipeline | `turingresearch-fusion-literature-survey` |
| web fetch | `turingresearch-core-reproduction` |
| pod workflow | `turingresearch-fusion-context-management` |
| artifact audit | `turingresearch-cache-and-ledger` |
| advisor pack | `turingresearch-paper-writing-pipeline` |
| release gate | `turingresearch-qa-release` |

## Required SOP Fields

Each priority workflow skill includes:

- `when_to_use`
- `inputs`
- `outputs`
- `safety`
- `non-goals`
- `handoff`
- `tests`
- `related_docs`

## Boundary

This is documentation and routing parity only. It does not execute skills,
start agents, call the network, enable plugins, perform remote execution, or
turn planned work into observed evidence.

## Safety

All SOPs preserve the project-wide public safety rules: no default live
networking, no private VGGT path access without explicit round permission, no
fake observed results, no unknown plugin execution, and no unapproved release
actions.

Short form: no default live networking.
