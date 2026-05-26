# Paper Reference E2E Report

Status: fake/demo pass.

Pipeline:

1. Load `paper_metadata.json`.
2. Run `scholar.paper_reference` in fake/default mode.
3. Collect fake/default citations as review context.
4. Build `related_work_seed.json`.
5. Build `collision_matrix_input.json`.
6. Run conservative collision and related-work planning in tests.

Safety:

- no live provider call;
- no API key required;
- no automatic full paper download;
- no paywall bypass;
- no fake citation is marked as verified;
- no final novelty or collision claim;
- human review required.
