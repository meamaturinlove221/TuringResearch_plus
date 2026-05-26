# Original Repo Parity Dashboard v2

Status: v1.4 public dashboard.

Round: 323.

This dashboard shows original reference repo parity progress across four
levels:

- structural parity;
- runtime parity;
- production parity;
- deferred items.

Data source:

- `examples/public_demo/parity_dashboard_v2.json`

## Progress Matrix

| Area | Structural parity | Runtime parity | Production parity | Deferred |
| --- | --- | --- | --- | --- |
| Neocortica Session | complete | complete | complete with deferred live gaps | live SSH/SFTP by default, remote command execution, SSH/tmux/provision |
| Neocortica Scholar | complete | complete | complete fake/default | MinerU, OCR default, automatic paper download, live provider proof |
| Neocortica Web | complete | complete | complete fake/default | default live network, private scraping, cookie storage, live Apify proof |
| yogsoth-ai | complete | complete | complete with review | autonomous agent runtime, automatic experiment execution, final paper automation |
| ARIS | deferred | deferred | deferred | cross-model review, proof-checker, meta-optimize, paper-claim-audit, ARIS runtime |

## Production Evidence

- `docs/session-production-parity-gate-report.md`
- `docs/scholar-production-parity-gate-report.md`
- `docs/web-production-parity-gate-report.md`
- `docs/yogsoth-production-parity-gate-report.md`
- `docs/v1.4.0-full-production-replay-report.md`

## Structural vs Runtime vs Production

Structural parity means the repository has matching docs, contracts, examples,
or public surfaces for the stable reference repo idea.

Runtime parity means the fake/default local workflow can run through a tested
path without live providers or private data.

Production parity means the fake/default local workflow has operator-facing
docs, E2E coverage, safety boundaries, and gate reports.

Deferred means the feature remains deliberately out of scope for v1.4.

## Safety Boundary

- fake/default dashboard only;
- no core runtime added by this dashboard;
- no unsafe live default;
- no default network;
- no remote command execution;
- no automatic experiment execution;
- no Evidence Ledger mutation;
- no fake/demo result promotion;
- privacy-first defaults;
- human review required.
