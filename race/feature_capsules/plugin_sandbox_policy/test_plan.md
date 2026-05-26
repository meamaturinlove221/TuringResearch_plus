# Plugin Sandbox Policy Test Plan

Status: planning.

## Unit Tests

- permission model tests
- default-deny tests
- sandbox report tests

## Contract Tests

- requires human review
- forbids secrets access
- forbids remote write by default

## Workflow Tests

- safe local read-only plugin policy
- rejected execute-code plugin policy
- restricted raw-data plugin policy
