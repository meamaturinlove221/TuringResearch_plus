# Neocortica Parity Remaining Gaps

Status: tracked gaps.

Round: 242.

## Partial Gaps

### Upstream Strict Diff

Current state: partial.

Reason: v1.2 strict baseline exists, but public metadata scan was unresolved in
the current environment. No added/modified/deleted upstream claims should be
made until a resolved diff exists.

### Live Provider Coverage

Current state: partial.

Reason: Semantic Scholar, Apify, and Web live paths are optional and skipped by
default. This is intentional for public-safe tests.

### Pod Lifecycle Manager

Current state: partial.

Reason: TuringResearch has safety models, manifests, preflight checks, transfer
policy, and return verification. It does not implement a remote execution
manager.

## Deferred Gaps

- MinerU / heavy PDF fallback.
- Remote execution orchestration.
- SSH/tmux/provision.
- Real Apify workflow templates.
- Full live provider regression.
- ARIS cross-model review, meta-optimize, proof-checker, and paper automation
  study items.

## Rejected Gaps

- Paywall bypass.
- Private content fetching.
- Cookie storage in public workflow.
- Unknown remote execution.
- Automatic evidence ledger mutation.
- Automatic git push.

## Next Practical Step

Proceed to yogsoth parity gates or v1.2 public demo refresh. Do not implement
deferred heavy/live/remote features without a new design round and safety gate.
