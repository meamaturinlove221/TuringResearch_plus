# Optional Live Safety Gate

Status: gate passed.

Round: 348.

This gate unifies the optional live safety boundary for Scholar, Web, Apify, and
SFTP. It does not run live tests, open network connections, connect to remote
hosts, or require credentials.

## Gate Decision

Decision: `PASS FOR OPTIONAL LIVE POLISH / NO-GO FOR DEFAULT LIVE`.

Optional live surfaces are documented and guarded. They remain disabled by
default and require explicit private configuration.

## Gate Checks

| Check | Result | Evidence |
| --- | --- | --- |
| live disabled by default | pass | `.mcp.example.json`, `pyproject.toml`, live guides |
| env explicit | pass | provider-specific live flags and credential placeholders |
| no secrets | pass | blank placeholders only |
| no live tests in default suite | pass | `addopts = -m 'not live and not manual'` |
| no remote command | pass | SFTP policy and guide |
| no private scraping | pass | Web / Apify policy and guide |
| no old naming | pass | name integrity gate |

## Covered Surfaces

- Scholar live optional.
- Web live optional.
- Apify live optional.
- SFTP live optional.
- MCP env block.
- Live tests skipped by default.

## Required Defaults

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0
TURINGRESEARCH_ENABLE_WEB_LIVE=0
TURINGRESEARCH_ENABLE_APIFY_LIVE=0
TURINGRESEARCH_ENABLE_SFTP_LIVE=0
SEMANTIC_SCHOLAR_API_KEY=<blank>
APIFY_TOKEN=<blank>

TURINGRESEARCH_SFTP_CREDENTIAL=<blank>
```

## NO-GO

- default live networking;
- default SSH or SFTP;
- remote command execution;
- remote delete;
- private scraping;
- login bypass;
- paywall bypass;
- committed secrets;
- token logging;
- automatic evidence promotion;
- live output treated as observed evidence without human review.

## Interpretation

This gate proves the policy surface is locked and testable. It is not proof that
any live provider call succeeded.
