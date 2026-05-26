# Optional Remote Dry-run Plan: demo-remote-dry-run



- Status: `ready-with-warnings`

- Session: `demo-session`

- Package: `demo-context-pack`

- Route: `demo-route`

- Remote target placeholder: `<manual-target-placeholder>`

- SSH enabled: `false`

- SFTP enabled: `false`

- tmux enabled: `false`

- Modal enabled: `false`

- Remote execution enabled: `false`

- Dry-run only: `true`

- Automatic Evidence Ledger write: `false`

- Requires human review: `true`



## Preflight Result



- Preflight status: `pass-with-warnings`

- Release blocker: `false`



## Files To Transfer



- `ARTIFACT_REQUIREMENTS.md` (26 bytes) `manual-reference-only`

- `FAILURE_TAXONOMY.md` (21 bytes) `manual-reference-only`

- `HARD_GATES.md` (15 bytes) `manual-reference-only`

- `MEMORY.md` (11 bytes) `manual-reference-only`

- `PROJECT_CONTEXT.md` (20 bytes) `manual-reference-only`

- `ROUTE_SPEC.yaml` (17 bytes) `manual-reference-only`



## Forbidden Files Excluded



- `.env`: not-in-context-pack-allowlist, non-text-context-file, hidden-dotfile-excluded, forbidden-dotfile, forbidden-env-file



## Return Artifact Requirements



- `RUN_STATUS.json`

- `FINAL_STATUS.json`

- `ARTIFACT_INDEX.md`

- `FAILURE_REPORT.md`

- `PROPOSED_EVIDENCE_UPDATES.json`

- `SHA256SUMS.txt`



## Manual Command References



These commands are references only. TuringResearch does not execute them.



### Review remote target placeholder



- Step: `manual-review-target`

- Status: `manual-confirmation-required`

- Requires manual confirmation: `true`

- Executes in TuringResearch: `false`

- Remote execution enabled: `false`



```bash

# MANUAL ONLY: confirm target <manual-target-placeholder>

```



Notes:

- Do not run if the target host, directory, or user is unclear.



### Transfer context pack manually



- Step: `manual-transfer-reference`

- Status: `manual-confirmation-required`

- Requires manual confirmation: `true`

- Executes in TuringResearch: `false`

- Remote execution enabled: `false`



```bash

# MANUAL ONLY: sftp put ./context_pack/* <reviewed-target>/

```



Notes:

- This is a reference only; TuringResearch does not run SFTP.



### Launch remote work manually



- Step: `manual-launch-reference`

- Status: `manual-confirmation-required`

- Requires manual confirmation: `true`

- Executes in TuringResearch: `false`

- Remote execution enabled: `false`



```bash

# MANUAL ONLY: run reviewed command in a separate human shell

```



Notes:

- No SSH, tmux, Modal, or remote command is run by this plan.



### Collect structured return manually



- Step: `manual-return-reference`

- Status: `manual-confirmation-required`

- Requires manual confirmation: `true`

- Executes in TuringResearch: `false`

- Remote execution enabled: `false`



```bash

# MANUAL ONLY: copy return files into a local review directory

```



Notes:

- Return files must be verified before any ingest review.



## Rollback Plan



- `stop-before-transfer`: If preflight or context pack review fails, do not transfer files.

- `archive-local-plan`: Keep the local dry-run report for audit instead of deleting remote files.

- `request-human-cleanup`: If a human created remote files, cleanup must be reviewed and run manually.



## Human Confirmation Checklist



- [ ] Preflight report is pass or pass-with-warnings, not blocked.

- [ ] Forbidden files are excluded from the context pack.

- [ ] Remote target placeholder has been replaced outside the repo.

- [ ] No secret, raw data, or restricted model payload will be transferred.

- [ ] Manual commands have been reviewed by a human.

- [ ] Return artifact requirements are understood before remote work starts.

- [ ] No automatic Evidence Ledger write will occur.
