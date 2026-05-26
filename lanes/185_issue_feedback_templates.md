# Round 207 - Issue / Feedback Templates

Status: complete.

## Goal

Prepare public feedback and issue templates for post-launch stabilization. This
round does not implement features.

## Output

- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/ISSUE_TEMPLATE/research_case_request.md`
- `.github/ISSUE_TEMPLATE/plugin_proposal.md`
- `.github/ISSUE_TEMPLATE/security_privacy_report.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/v1.1.0-feedback-templates.md`
- `docs/v1.1.0-issue-triage-policy.md`

## Template Coverage

- expected behavior;
- actual behavior;
- reproduction steps;
- environment;
- live mode status;
- data sensitivity;
- safety/privacy notes;
- optional screenshots/logs;
- no-secrets warning.

## Boundaries

- No API keys.
- No raw data.
- No restricted model payloads.
- No private local paths.
- Plugin proposals must declare permissions.
- Research case requests must declare data sensitivity.
