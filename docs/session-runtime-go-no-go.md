# Session Runtime Go / No-Go

Round: 270.

## GO

The following Session runtime parity surfaces are GO for fake/default use:

- local session preflight;
- safe context pack builder;
- fake/local transfer runner;
- structured return verifier;
- proposed evidence update report;
- full fake pod workflow replay;
- Session parity dashboard.

These surfaces are review-only and local-first.

## GO WITH GUARD

Optional live transfer is GO only as a guarded future live-test surface:

- it is skipped by default;
- it requires explicit environment opt-in;
- it does not run remote commands;
- it must not log credentials;
- it must stay out of public demo workflows.

## NO-GO

The following are not approved by this gate:

- live SSH by default;
- remote command execution;
- SSH / tmux / provision orchestration;
- automatic pod cleanup;
- automatic experiment execution;
- automatic Evidence Ledger write;
- trusting fake or remote claims as observed evidence;
- packaging secrets, raw data, private paths, or restricted model payloads.

## Decision

Session runtime parity is complete for v1.3 fake/default parity.

Live remote orchestration remains deferred and requires a separate scope lock,
safety review, and live-test gate.
