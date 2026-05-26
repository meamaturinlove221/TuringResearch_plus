# Session Context Pack Fixture

Status: fake/demo fixture.

This fixture demonstrates a review-only session context pack. It is not a pod
execution bundle and does not contain raw data, credentials, private paths, or
remote execution scripts.

Files:

- `context_pack_manifest.yaml`
- `RETURN_MANIFEST.yaml`

Boundaries:

- no SSH provision;
- no tmux attach;
- no remote command execution;
- no automatic git push;
- no bidirectional memory sync;
- proposed updates only.
