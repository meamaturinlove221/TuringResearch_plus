# Split Go / No-Go

Status: no-go for actual split.

Round: 162.

## Decision

Actual repository split: `NO-GO`.

Design continuation: `GO`.

## Reasons For No-Go

- No target branch/repository extraction plan is approved.
- No exact export file set is frozen.
- No independent CI/release ownership is defined.
- Main repo should remain the flagship and star entry point.
- Plugin split needs stronger standalone review infrastructure.

## Reasons Design Can Continue

- Candidate skeletons are complete.
- README files point back to the flagship.
- Safety boundaries are explicit.
- No private payloads are included.
- No unsupported success claims are present.

## Required Before Future Go

- maintainer approval;
- exact export manifests;
- privacy and compliance scans on exact export set;
- claim safety review;
- no-secrets and no-raw-data scan;
- independent smoke tests;
- README flagship link review;
- release ownership decision.
