# Not Implementing Now

Status: v1.2 scope guard.

Round: 232.

This document lists reference ideas that are intentionally not part of the v1.2
implementation line.

## Deferred To v1.3 Or Later

| Reference | Feature | Reason | Status |
| --- | --- | --- | --- |
| ARIS | cross-model review loop | valuable, but introduces agent runtime and review orchestration beyond v1.2 parity | deferred |
| ARIS | meta-optimize | too speculative for the parity-first line | deferred |
| ARIS | proof-checker | requires a separate threat model and correctness story | deferred |
| ARIS | paper-writing automation | conflicts with v1.2 paper beta human-review boundary | rejected for v1.2 |
| Neocortica-Scholar | MinerU / heavy PDF fallback runtime | dependency/licensing/copyright and reproducibility risk | deferred |
| Neocortica-Web | real Apify integration tests by default | requires token/network/cost controls | deferred |
| Plugin ecosystem | OS-level plugin sandbox | research needed before any promise | deferred |
| Session/pod workflow | unknown remote execution | outside local-first safety scope | rejected for v1.2 |
| Split strategy | automatic child repo creation | requires human approval and manual release action | rejected for v1.2 |

## Rejected For v1.2

- default live networking;
- unknown third-party plugin execution;
- automatic experiment execution;
- automatic final paper writing;
- automatic evidence ledger mutation from pod returns;
- copying upstream source code;
- fake/demo outputs marked as observed evidence.

## Allowed As Study Notes

The deferred ARIS items may appear in the v1.3 ARIS study roadmap. They must not
be represented as implemented, observed, or release-ready in v1.2.
