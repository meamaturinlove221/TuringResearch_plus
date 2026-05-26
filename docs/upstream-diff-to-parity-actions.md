# Upstream Diff to Parity Actions

Status: planning actions from baseline-created strict diff.

Round: 234.

The v1.2 strict diff created a first machine baseline, but all configured
upstream targets were unresolved. Therefore these actions are parity planning
actions only. They are not claims about newly added or modified upstream work.

## Action Table

| Reference area | Strict diff state | Parity action | Allowed claim | Blocked claim | Next round |
| --- | --- | --- | --- | --- | --- |
| Neocortica Session | baseline-created, unresolved | Continue Pod Context Lifecycle parity planning; require a resolved scan before upstream-change-specific work | local safety plan exists and needs parity gate | upstream Session added or changed files | R234-R235 tentative |
| Neocortica Scholar | baseline-created, unresolved | Keep MCP config and scholar pipeline parity as docs/tests work; do not claim new upstream deltas | current plan covers known manual snapshot themes | Scholar added new pipeline behavior in this diff | R235-R236 tentative |
| Neocortica Web | baseline-created, unresolved | Keep optional web/live and Apify boundaries fake/default; wait for resolved baseline before live-template claims | web parity remains planned and opt-in | Web added new Apify or web content modules in this diff | R236-R237 tentative |
| yogsoth campaign/catalog | baseline-created, unresolved | Keep Campaign Catalog parity gate; route through deterministic local tests | campaign parity is a local v1.2 target | yogsoth added campaign features in this diff | R237-R238 tentative |
| yogsoth vault/ontology | baseline-created, unresolved | Keep vault and ontology parity as local docs/tests and avoid graph truth overclaim | vault/ontology parity remains planned | upstream vault or ontology changed in this diff | R237-R239 tentative |
| yogsoth stress/experiment | baseline-created, unresolved | Keep stress-test and experiment-execution parity gates, with no automatic real execution | route/hard gate parity remains planned | upstream experiment runtime changed in this diff | R238-R239 tentative |
| ARIS future reference | out of v1.2 scope | Keep deferred for v1.3 study and later selective review | ARIS is deferred | ARIS enters v1.2 implementation | v1.3+ |

## Policy

- A parity action can continue when it is based on existing local plans,
  contracts, tests, and previously documented manual snapshots.
- An upstream-change-specific action requires a resolved strict diff.
- Unresolved targets do not block all local parity planning, but they do block
  any precise changed-file or changed-module claim.
- No upstream code is copied into TuringResearch.

## Updated Target Round Meaning

The target rounds in `docs/original-reference-parity-matrix.md` now represent
tentative execution windows after Round 234. They do not mean that Round 234
observed upstream file changes.
