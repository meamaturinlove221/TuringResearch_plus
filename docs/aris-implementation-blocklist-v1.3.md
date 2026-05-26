# ARIS Implementation Blocklist v1.3

Status: active blocklist.

Round: 262.

This blocklist prevents ARIS concepts from slipping into v1.3 full original
parity work.

## Blocked Runtime Features

| Feature | v1.3 status | Reason |
| --- | --- | --- |
| cross-model review loop | blocked | Could create opaque model authority chains. |
| proof-checker | blocked | Could overstate correctness. |
| meta-optimize | blocked | Could silently tune behavior without review. |
| paper-claim-audit | blocked | Could blur review assistance and final claim validation. |
| session stop hook | blocked | Could mutate session state or lifecycle unexpectedly. |
| automated sleep research loop | blocked | Could create autonomous research-loop behavior. |
| paper resubmit pipeline | blocked | Could drift into final paper automation. |
| result-to-claim verification runtime | blocked | Needs design before any runtime. |
| experiment audit runtime | blocked | Must not infer experiment success from missing evidence. |

## Blocked Claims

Do not claim any of the following in v1.3:

- ARIS is implemented.
- Cross-model review is enabled.
- Proof-checker is available.
- Meta-optimize is available.
- Paper-claim audit is available.
- Session stop hook is active.
- Automated sleep research loop is active.
- ARIS replaces human review.

## Guardrail

Any file that introduces ARIS runtime language in v1.3 must first add:

1. a new scope lock;
2. a safety review;
3. fake/default tests;
4. privacy/security gate coverage;
5. release notes that clearly separate study from implementation.

Until that happens, ARIS stays reference-only.
