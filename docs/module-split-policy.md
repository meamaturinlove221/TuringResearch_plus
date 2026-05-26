# Module Split Policy

Status: planning policy.

Round: 151.

This policy defines when a TuringResearch module may become a separate
repository. It is a policy only; no module is split in this round.

## Split Admission Criteria

A module may be proposed for repository split only when it satisfies all of the
following:

- stable API;
- docs complete;
- tests pass;
- no private data;
- no license risk;
- demo available;
- independent value;
- independent install path;
- independent test command;
- clear owner and maintenance plan;
- main repo can still run without confusion.

## Required Artifacts

Before a split:

- split proposal;
- module API inventory;
- public README draft;
- install guide;
- example or demo;
- test summary;
- license review;
- privacy scan;
- security scan;
- compatibility notes;
- migration path from the main repo;
- rollback plan.

## Allowed Early Split Types

| Module type | Split readiness | Notes |
| --- | --- | --- |
| Case study | earliest | Presentation-heavy and can link back to the flagship. |
| Examples | early after demo refresh | Must stay demo-safe and fake/default. |
| Plugins | after registry policy | Must be disabled by default and safety-reviewed. |
| Dashboard | after local server scope stabilizes | Needs install and privacy boundaries. |
| Paper tools | later | Needs stable section contracts and citation safety. |
| Artifact tools | later | Needs stable privacy/compliance policy. |
| Core | last | Moving core too early weakens the flagship repo. |

## Main Repo Requirements After A Split

The main repo must retain:

- overview docs;
- quickstart;
- integration demo;
- compatibility tests;
- release gates;
- dependency story;
- links to satellite repositories;
- fallback fake/default workflows;
- clear explanation of what moved and why.

## Split Review Checklist

1. Does the module have independent value?
2. Is the API stable enough?
3. Are docs and examples complete?
4. Do tests pass independently?
5. Are private data and license risks cleared?
6. Does the split avoid confusing users?
7. Does the split preserve flagship star growth?
8. Is the migration path documented?
9. Is there a maintenance owner?
10. Is rollback possible?

## Prohibited Splits

- Splits that expose private data.
- Splits that bypass license review.
- Splits that make fake/demo results look observed.
- Splits that enable unknown plugin execution.
- Splits that leave the flagship repository empty.
- Splits that create unclear install paths.
- Splits that remove safety gates from the main repo.

## Review Cadence

Review split candidates during roadmap or scope-lock rounds. Do not split in
implementation or release-prep rounds unless explicitly requested and approved.
