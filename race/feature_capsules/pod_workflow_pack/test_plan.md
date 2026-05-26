# Test Plan: pod_workflow_pack

- Validate required output files exist.
- Verify missing outputs are listed, not ignored.
- Verify checksums cover included files.
- Verify report-only outputs fail promotion gates.
- Verify run ingest creates proposed evidence updates only.
- Verify no remote execution is triggered by import.
