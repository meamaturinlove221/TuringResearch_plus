# Future ARIS Study Roadmap

Status: v1.3+ study roadmap.

Round: 233.

This roadmap captures ARIS as future research input after v1.2 original
reference parity. It does not implement ARIS features.

## Study Phases

### v1.3 Study Phase

Goal: evaluate whether ARIS concepts fit TuringResearch's local-first,
human-review, evidence-ledger design.

Study topics:

- cross-model review loop;
- claim audit;
- result-to-claim verification;
- experiment audit;
- proof checker;
- paper compile audit;
- meta-optimize;
- effort levels;
- session stop hook;
- paper resubmit pipeline.

Expected outputs:

- design notes;
- threat model;
- safety review;
- non-goals;
- test strategy;
- adoption go/no-go.

### v1.4 Selective Adoption Phase

Only a small number of mature ARIS-inspired capabilities may be considered in
v1.4. A candidate must have:

- clear local-first behavior;
- fake/default tests;
- human-review boundary;
- no default live networking;
- no autonomous final claim generation;
- no evidence mutation without review;
- regression coverage.

## Explicit Study Questions

- Can cross-model review be used as review assistance without creating false
  authority?
- Can result-to-claim verification strengthen evidence discipline without
  fabricating missing results?
- Can proof-checking be framed as a checklist rather than a correctness claim?
- Can effort levels improve planning without becoming opaque automation?
- Can paper resubmit workflow remain a checklist, not an automatic paper writer?

## Out Of Scope For v1.3 Study

- production runtime;
- default live networking;
- automatic paper writing;
- automatic experiment execution;
- automatic repository creation;
- unknown plugin execution.
