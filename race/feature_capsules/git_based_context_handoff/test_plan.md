# Test Plan: git_based_context_handoff

- Validate required context files exist.
- Verify `.env`, secrets, raw data, cache folders, and SMPL-X body model files
  are omitted.
- Verify `MEMORY.md` is summary-only and human-review gated.
- Verify no remote execution is triggered.
- Verify returned outputs generate proposed updates only.
