# Web Fetching Usage Guide

Status: v1.2 usage guide.

Round: 238.

`web_fetching` is the public-safe tool surface for retrieving web page context.
It wraps the existing fake-first web fetch adapter and keeps default runs
offline.

## Default Mode

Default requests are dry-run and do not access the network:

- `dry_run: true`
- `live_enabled: false`
- `default_network: false`
- `stores_cookies: false`
- `requires_api_key: false`
- `requires_human_review: true`

The default result is useful for workflow tests and demo wiring. It is not
observed external web evidence.

## Live Mode

Live mode is opt-in only and requires private local configuration. Public tests
must keep live mode disabled.

Live fetched material remains source context. It must be reviewed before it is
used in evidence ledgers, advisor packs, or paper-related outputs.

## Source Hygiene

The tool must not fetch private or restricted sources. Source hygiene values
that indicate private or restricted content return a blocked result.

Blocked or dry-run results are treated as graceful skips, not failures.

## Output Boundary

`web_fetching` output records retrieval status, source type, source metadata,
hashes, warnings, and limitations. It does not store cookies, secrets, raw
private content, or provider credentials.
