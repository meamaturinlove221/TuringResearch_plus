# Return Import Human Confirmation

Status: v1.4 production parity hardening.

Round: 296.

The Return Import Human Confirmation layer sits after the Remote Return
Verifier. It packages verifier results, proposed updates, a human import
decision, and a proposed-only ledger packet. It never writes to the Evidence
Ledger automatically.

## Decision States

- `accept`
- `reject`
- `partial_accept`
- `requires_more_review`
- `unsafe_blocked`

The safe default is `requires_more_review` when the verifier passes. If the
verifier blocks the return package, the default is `unsafe_blocked`.

## Packet Contents

- verifier report
- import decision
- proposed-only ledger proposal
- human checklist
- safety flags showing remote claims are not trusted
- explicit `Auto-write Evidence Ledger: false`

## Boundaries

- Remote or fake claims are not trusted as observed evidence.
- Proposed updates remain proposed-only.
- No automatic Evidence Ledger write.
- No fake/demo result promotion.
- Unsafe files, missing artifacts, and checksum mismatches block import review.
- Human review remains required.

## Runtime API

```python
from pathlib import Path

from turing_research_plus.session_runtime import (
    build_human_confirmation_packet,
    verify_return_package,
    write_human_confirmation_packet,
)

verifier = verify_return_package(
    Path("examples/session_runtime/return_fixture"),
    return_id="return-fixture",
)
packet = build_human_confirmation_packet(verifier)
write_human_confirmation_packet(packet, Path("tmp/CONFIRMATION_PACKET.md"))
```

The generated packet is a review artifact. A separate human-controlled process
would be required to perform any manual ledger import.
