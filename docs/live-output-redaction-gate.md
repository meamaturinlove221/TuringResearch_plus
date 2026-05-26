# Live Output Redaction Gate

Round: 376
Status: active

## Objective

Create a redaction gate for optional live outputs. Even if a maintainer
manually enables live Scholar, Web / Apify, or SFTP smoke later, live output
must not be written into reports with secrets, private paths, cookies, SSH host
aliases, local usernames, passwords, or raw private content intact.

This round does not run live providers and does not enable live mode by default.

## Required Redactions

- API keys
- tokens
- passwords
- private paths
- SSH host aliases
- local usernames
- cookies
- raw private content

## Runtime Surface

- `turing_research_plus.live_safety.redaction.redact_live_output`
- `turing_research_plus.live_safety.live_report_guard.guard_live_report`
- `turing_research_plus.live_safety.live_report_guard.render_live_report_guard`

## Gate Behavior

- No raw live output is retained.
- No automatic Evidence Ledger write.
- Human review is always required.
- Redactions produce typed findings.
- Reports with redactions are blocked until reviewed.
- Clean summaries are still review-only.

## Contract

See `contracts/live_output_redaction_gate.yaml`.

## Non-goals

- no live provider execution;
- no SSH or SFTP connection;
- no remote command execution;
- no raw payload archival;
- no proof of live provider correctness;
- no automatic claim verification.

## Decision

The live output redaction gate is ready for optional live smoke follow-up work.
It remains a guardrail, not approval to run live providers by default.
