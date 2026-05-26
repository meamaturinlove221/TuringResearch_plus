# SFTP Live Smoke Skip Report

Status: skipped by default.

## Default Skip Conditions

Live SFTP smoke must skip unless all of these are set outside the repository:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`
- `TURINGRESEARCH_ENABLE_SFTP_LIVE=1`
- `TURINGRESEARCH_SFTP_CREDENTIAL=<private local credential reference>`
- `TURINGRESEARCH_SFTP_KEY_PATH=<private local key path>`
- `TURINGRESEARCH_SFTP_TARGET=/explicit/reviewed/target`

## Safety

- no password in repo;
- no key path in repo;
- no remote command;
- no remote delete;
- transfer target explicit;
- skipped live output is not observed evidence.
