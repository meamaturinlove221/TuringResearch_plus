# VGGT Case Study Outline

Status: outline only.

The VGGT case study should explain how TuringResearch Plus supports a real
research workflow without claiming unsupported experiment success. It should be
written as a dogfooding case study, not as a final paper result.

## North Star

Shift from:

```text
SMPL-X direct replacement
```

to:

```text
SMPL-X feature encoding for VGGT
```

The case study should explain why this shift reduces integration risk and
supports more conservative experiment planning.

## Route Changes

Cover:

- early direct replacement attempts;
- route exhaustion and hard-blocked states;
- SMPL-X feature adapter direction;
- Modal SparseConv3D route planning;
- fallback rules and hard gates;
- why planned routes are not observed results.

## Failures

Document failures as research learning:

- route exhausted;
- hard-blocked experiments;
- local positive result with regression warning;
- missing backend evidence;
- missing board views;
- hand-object / hairline / completion uncertainty;
- SparseConv3D success not established.

## Evidence Management

Show how TuringResearch helped organize:

- evidence ledger statuses;
- artifact audit;
- visual readiness;
- run ingest reports;
- failure taxonomy;
- research knowledge pack;
- replay and quality gates.

## Route DSL

Explain how route DSL made experiment plans reviewable:

- route id;
- backend assumptions;
- artifact requirements;
- hard gates;
- fallback rules;
- next actions;
- missing evidence.

## Advisor Pack

Show how advisor outputs stayed conservative:

- what is done;
- what is missing;
- what is planned;
- what requires human review;
- what should not be claimed.

## What TuringResearch Helped With

- Turning scattered artifacts into reviewable summaries.
- Preventing planned routes from being written as observed results.
- Keeping unsafe claims visible.
- Linking paper scaffold sections to evidence gaps.
- Making advisor communication more concrete.
- Keeping public/demo material separate from private research material.

## What Still Requires Human Research

- Running VGGT experiments.
- Verifying sparse backend behavior.
- Reviewing result tables and visual boards.
- Reading and citing real papers.
- Interpreting failures.
- Approving final claims.
- Deciding whether any SparseConv3D result is real evidence.

## Case Study Output Shape

Recommended sections:

1. Research context.
2. North Star shift.
3. Evidence and artifact timeline.
4. Route DSL and hard gates.
5. Failure taxonomy.
6. Advisor communication.
7. Paper assembly blockers.
8. What changed in the workflow.
9. What remains unresolved.
