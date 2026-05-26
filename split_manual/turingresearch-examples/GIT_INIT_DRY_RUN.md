# Git Init Dry-run: turingresearch-examples

Status: dry-run only.

This file describes how a human may initialize a future
`turingresearch-examples` repository after approval. It does not run `git init`,
create a repository, add a remote, or push.

## Files To Include

- `README.md`
- `QUICKSTART.md`
- `examples_manifest.yaml`
- `PRIVACY.md`
- `safety_report.md`
- `.gitignore`

## Files To Exclude

- raw data;
- private local paths;
- secrets, tokens, credentials, or `.env` values;
- API keys;
- private logs;
- generated huge artifacts;
- cache directories;
- unreviewed local files;
- benchmark result payloads.

## Initial Commit Message Suggestion

```text
Initial public-safe examples bundle
```

## Branch Suggestion

```text
main
```

## Remote URL Placeholder

```text
<approved-real-repository-url>
```

Do not replace this placeholder until a human confirms that the external
repository exists and the URL is real.

## Manual Commands

These commands are commented reference notes only:

```sh
# cd <manual-local-copy-of-turingresearch-examples>
# git init
# git add README.md QUICKSTART.md examples_manifest.yaml PRIVACY.md safety_report.md .gitignore
# git commit -m "Initial public-safe examples bundle"
# git branch -M main
# git remote add origin <approved-real-repository-url>
# git push -u origin main
```

## Safety Warnings

- Do not run this from the flagship repository root.
- Do not use a placeholder URL as a remote.
- Do not create a repository automatically.
- Do not push before human approval.
- Do not include raw data, API keys, private paths, or huge artifacts.
- Do not present demo output as observed evidence.
