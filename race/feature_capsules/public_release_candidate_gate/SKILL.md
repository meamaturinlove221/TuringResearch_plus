# Public Release RC Gate Skill

Status: planning skill draft.

Use this skill for public release candidate gate planning. It does not publish,
tag, or push releases.

## Inputs

- quality regression report
- privacy scan report
- public demo report
- docs audit
- package metadata
- release notes

## Outputs

- PublicReleaseRCReport
- PublicReleaseGoNoGo
- PublicReleaseBlockerList

## Safety Rules

- Do not publish automatically.
- Do not tag automatically.
- Do not include secrets, raw data, or private model files.
- Do not mark fake results observed.
- Require maintainer review.

## Related Contracts

- public_release_candidate_gate.yaml
- quality_regression_gate.yaml
- privacy_data_policy.yaml
