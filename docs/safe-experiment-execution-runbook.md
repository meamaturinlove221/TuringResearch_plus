# Safe Experiment Execution Runbook

Status: implemented minimal.

Round: 247.

The safe experiment execution runbook turns a planned route into a local,
review-only checklist. It is designed to prepare a human-run experiment without
letting TuringResearch run it automatically.

## Runbook Flow

1. Review the route and confirm a human owner.
2. Prepare artifact requirements.
3. Validate hard gates.
4. Human operator runs the experiment outside TuringResearch if approved.
5. Ingest exported run bundle with the run ingest contract.
6. Review proposed evidence updates.
7. Keep observed-result writes manual and evidence-backed.

## Required Outputs

- run manifest
- artifact index
- hard gate report
- missing artifact list
- source metadata
- proposed evidence updates

## Non-goals

- No automatic experiment execution.
- No remote execution.
- No Modal invocation.
- No GPU invocation.
- No observed result write.
- No private path read.
- No replacement for human review.

## Safety Rule

The runbook can say what a human should prepare and inspect. It must not claim
that an experiment has run, succeeded, or produced observed evidence.
