# Post-launch Monitoring Plan

Status: planning policy.

Round: 198.

This plan defines how to monitor TuringResearch Plus after a future public
launch. It is not a release action and does not enable telemetry.

## Monitoring Principles

- Do not collect private user data.
- Prefer public issue discussion unless the report is security-sensitive.
- Keep the project local-first, fake/demo-first, and review-first.
- Treat privacy, security, plugin safety, and claim confusion as high priority.
- Patch docs quickly when users misunderstand setup, scope, or limitations.

## First 24 Hours

- Watch for install failures.
- Watch for quickstart failures.
- Check whether README and quickstart wording cause confusion.
- Check whether users understand fake/live defaults.
- Check whether public demo files open locally.
- Check whether any security/privacy report arrives.

## First 7 Days

- Review issue themes.
- Update FAQ or troubleshooting docs if the same question repeats.
- Track demo breakage reports.
- Track live adapter confusion.
- Track plugin safety questions.
- Record star/fork/watch trend as a public-interest signal, not a success
  guarantee.
- Record interview/demo usage notes if the project is used in applications.

## First 30 Days

- Decide whether a patch release is needed.
- Decide whether docs need a clarity pass.
- Decide whether `turingresearch-vggt-case` should be created after human
  approval.
- Decide whether public demo examples need refresh.
- Revisit v1.1 roadmap priorities based on real feedback.

## Monitoring Items

| Item | Signal | Action |
| --- | --- | --- |
| Install failures | pip/editable install errors | Patch install docs or package metadata |
| Quickstart failures | public quickstart test does not run | Patch quickstart or demo fixtures |
| Docs confusion | repeated questions | Add FAQ/troubleshooting note |
| Privacy/security issue | secret/private data concern | Private triage and hotfix if needed |
| Live adapter issue | API key/live opt-in confusion | Clarify fake/live guide |
| Plugin safety issue | permission or execution concern | Re-run plugin safety review |
| Demo breakage | missing files or broken dashboard | Refresh public demo |
| User feedback | issue/discussion notes | Label and route to roadmap |
| Star/fork/watch trend | public GitHub metrics | Use as interest signal only |
| Interview usage notes | recruiter/interviewer questions | Update portfolio and demo script |

## What Not To Track

- Private research data.
- Private advisor feedback.
- API keys or environment values.
- Raw data paths.
- User identity beyond public GitHub issue/discussion context.

## Escalation

Escalate immediately if a report mentions:

- secrets or credential exposure;
- private paths or private data;
- raw data or restricted model payloads;
- unsafe plugin execution;
- fake/demo output being interpreted as observed evidence.
