# Optional Live Polish Scope

Status: scope locked.

Round: 344.

v1.5 may polish optional live surfaces, but it does not make live behavior the
default and does not implement new live provider functionality in this round.

## Scope

| Surface | v1.5 polish scope | Default |
| --- | --- | --- |
| Scholar live optional | document opt-in env shape, skipped-live tests, fake/live wording | fake |
| Web / Apify live optional | document Apify/Web opt-in env shape, skipped-live tests, token handling boundary | fake |
| SFTP live optional | document opt-in env shape, typed skip behavior, no remote command boundary | fake/local |
| MCP env block | keep live flags explicit and disabled in committed config examples | fake |
| live tests | require explicit `TURINGRESEARCH_ENABLE_LIVE_TESTS=1` | skipped |

## Required Env Shape

Committed examples may show blank placeholders only:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0
TURINGRESEARCH_ENABLE_WEB_LIVE=0
TURINGRESEARCH_ENABLE_APIFY_LIVE=0
SEMANTIC_SCHOLAR_API_KEY=<blank>
APIFY_TOKEN=<blank>

TURINGRESEARCH_SFTP_CREDENTIAL=<blank>
```

Real values belong only in private local configuration.

## Allowed Work

- clarify fake/live docs;
- confirm live tests are skipped by default;
- improve live opt-in instructions;
- keep MCP config examples explicit and disabled;
- improve typed skip messages;
- keep credential placeholders blank.

## Not Allowed In This Round

- default networking;
- default SSH;
- remote command execution;
- real API key requirements;
- credential persistence;
- token logging;
- private scraping;
- paywall bypass;
- automatic evidence promotion.

## Interpretation

Optional live polish is usability polish around private opt-in. It is not proof
that live provider access succeeded and not evidence that any remote execution
path is production-ready.
