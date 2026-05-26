# Public Release RC Gate

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

Before a public release candidate, TuringResearch needs a single gate that
checks tests, docs, examples, privacy, plugin safety, licensing posture, and
roadmap honesty.

## 2. Research Motivating Example

A release should be blocked if it contains secrets, raw data, private model
files, fake observed results, unsafe plugin enablement, or unsupported paper
claims.

## 3. Inputs

- quality regression report
- privacy scan report
- public demo report
- docs audit
- package metadata
- release notes

## 4. Outputs

- PublicReleaseRCReport
- PublicReleaseGoNoGo
- PublicReleaseBlockerList

## 5. Proposed Commands / Tools

- command: `turing release rc-gate`
- tool: `release.public_rc_gate`
- output: `PublicReleaseRCReport`

## 6. Related Contracts

- public_release_candidate_gate.yaml
- quality_regression_gate.yaml
- privacy_data_policy.yaml

## 7. Related Skills

- turingresearch-qa-release
- turingresearch-master-orchestrator

## 8. Required Tests

- public release gate tests
- blocker detection tests
- no-secret/no-raw-data tests

## 9. Risks

- gate misses private data
- release notes overclaim capabilities
- plugin runtime status unclear

## 10. Done Criteria

- go/no-go report generated
- blockers documented
- release remains unpublished until maintainer approval

## 11. Non-goals

- no automatic release
- no tag creation
- no GitHub release publication
