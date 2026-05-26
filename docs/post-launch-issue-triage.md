# Post-launch Issue Triage

Status: triage policy.

Round: 198.

## Labels

| Label | Use |
| --- | --- |
| `install` | Install or package setup failure |
| `quickstart` | Quickstart command or demo path failure |
| `docs-confusion` | README/docs wording confusion |
| `privacy` | Private data, raw data, redaction, or path concern |
| `security` | Secrets, unsafe execution, dependency, or permission concern |
| `live-adapter` | Live mode, API key, network, or adapter behavior |
| `plugin-safety` | Plugin manifest, permissions, sandbox, or compatibility |
| `demo-breakage` | Public demo or dashboard fixture issue |
| `feedback` | General product or roadmap feedback |
| `interview-note` | Portfolio/demo/interview usage feedback |

## Severity

| Severity | Examples | Target response |
| --- | --- | --- |
| P0 | secret leak, private data leak, unsafe plugin execution | immediate private triage |
| P1 | quickstart broken, install broken, public demo unusable | patch candidate |
| P2 | docs confusion, live adapter confusion, minor demo issue | docs or fixture update |
| P3 | roadmap idea, nice-to-have feature, wording polish | backlog |

## Triage Flow

1. Confirm whether the report is public-safe.
2. If security/privacy sensitive, move to private handling.
3. Reproduce locally without live adapters when possible.
4. Identify whether this is docs, tests, package metadata, demo fixture, plugin
   policy, or real behavior.
5. Add a short issue summary and next action.
6. If fixed, add or update a regression test when practical.

## Non-goals

- Do not ask users to share private data.
- Do not request API keys in issues.
- Do not debug private VGGT artifacts in public.
- Do not mark planned/fake work as observed to close an issue.
