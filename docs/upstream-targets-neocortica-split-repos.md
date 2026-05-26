# Neocortica Split Repo Watch Targets

TuringResearch Plus now watches Neocortica split repositories rather than
treating the umbrella name as a required target.

## Active Targets

| Repository | Focus | Required |
| --- | --- | --- |
| `Pthahnix/Neocortica-Scholar` | scholar pipeline, cached paper markdown, references, reading methods | false |
| `Pthahnix/Neocortica-Web` | Apify client, web tools, MCP server, env config | false |
| `Pthahnix/Neocortica-Session` | Git context handoff, pod workflow, durable context | false |

## Legacy Alias

`Pthahnix/Neocortica` is a legacy alias / historical umbrella name. It is not a
required scan target. If it is missing, renamed, private, or unresolved, that is
not a watch failure.

## Adoption Boundary

TuringResearch Plus may adopt architecture ideas, interface patterns, test
strategy, and documentation structure. It must not copy incompatible code or
claim upstream features as implemented without local evidence.
