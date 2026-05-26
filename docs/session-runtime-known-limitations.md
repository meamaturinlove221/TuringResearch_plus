# Session Runtime Known Limitations

Round: 270.

The v1.3 Session runtime gate confirms fake/default parity, not live remote
orchestration.

## Limitations

- Live SSH is not enabled by default.
- SSH / tmux / provision workflows are not implemented as runtime defaults.
- Optional SFTP transfer remains a guarded live-test surface, not a default
  operator workflow.
- Remote command execution is not implemented.
- Automatic pod cleanup is not implemented.
- Automatic Evidence Ledger writes are not implemented.
- Fake or remote return claims are not trusted as observed evidence.
- Raw data, private paths, secrets, and restricted model payloads are excluded
  from safe context packs.
- Human review remains required before any proposed evidence update is accepted.

## Why These Limits Remain

These limits preserve TuringResearch's local-first safety boundary. The current
goal is to make the original Session workflow shape runnable in fake mode
without creating an unsafe remote automation surface.

## Future Work

Future live transfer or remote lifecycle work must happen in a dedicated round
with:

- explicit live-test opt-in;
- credential handling review;
- no-secret logging checks;
- remote write/delete restrictions;
- separate regression and privacy gates.
