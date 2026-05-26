# Remote Return Verifier Runtime

Status: v1.3 fake-first runtime parity.

Round: 267.

The Remote Return Verifier validates a structured return package from a fake or
remote pod before any ingest review. It checks required files, unsafe paths,
checksum mismatches, and proposed evidence updates.

It does not trust remote claims and does not write to the Evidence Ledger.

## Required Files

- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `SHA256SUMS.txt`

## Safety Rules

- Remote claims are review inputs, not trusted evidence.
- Proposed evidence updates remain proposed-only.
- No automatic Evidence Ledger write.
- Fake/demo results cannot become observed results.
- Missing artifacts are reported.
- Unsafe returned files are blocked.
- Checksum mismatch blocks ingest review.
- Human review remains required.

## Runtime API

```python
from pathlib import Path

from turing_research_plus.session_runtime import verify_return_package

report = verify_return_package(
    Path("examples/session_runtime/return_fixture"),
    return_id="return-fixture",
)
```

The report contains missing artifacts, unsafe files, checksum mismatches,
proposed updates, and safety findings.

## Non-goals

- No remote command execution.
- No automatic experiment execution.
- No automatic Evidence Ledger mutation.
- No proof that a fake or remote result is observed.
- No bypass of human review.
