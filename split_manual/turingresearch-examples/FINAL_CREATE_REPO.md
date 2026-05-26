# Final Create Repo: turingresearch-examples

Status: final manual creation instructions / not executed.

This file is a human-only checklist for a possible future public-safe examples
repository. It does not create a GitHub repository, does not run commands, does
not write a real URL, and does not push anything outside the flagship
TuringResearch repository.

## Repo Name Suggestion

```text
turingresearch-examples
```

## Initial Branch

```text
main
```

## Initial Commit Message

```text
Initial public-safe examples bundle
```

## Remote URL Placeholder

```text
<approved-real-repository-url>
```

Do not replace this placeholder until a maintainer confirms that the external
repository exists and the URL is real.

## Flagship Link Placeholder

```text
TuringResearch main repository URL goes here after human publication approval
```

The main TuringResearch repository remains the flagship install, docs, release,
public API, and star entry.

## Manual GitHub Creation Steps

1. Review `split_ready/turingresearch-examples/`.
2. Review `split_manual/turingresearch-examples/FINAL_PRIVACY_CHECK.md`.
3. Confirm every item in `FINAL_RELEASE_CHECKLIST.md`.
4. Manually create a GitHub repository named `turingresearch-examples`, if
   approved.
5. Copy only the reviewed demo-only source bundle.
6. Keep the child repository as an optional examples spoke, not the install
   source.
7. Add a real flagship link only after a maintainer approves the real URL.
8. Record the action back in the flagship ledger after completion.

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
- API keys, tokens, credentials, or `.env` values;
- private logs;
- generated huge artifacts;
- cache directories;
- unreviewed local files;
- benchmark result payloads;
- live outputs or provider responses;
- unsupported research or benchmark claims.

## Safety Checklist

- Demo-only content.
- No automatic GitHub repository creation.
- No automatic external push.
- No automatic release creation.
- No fake or placeholder URL used as a real remote.
- No raw data.
- No private path.
- No API key or token.
- No huge artifact.
- No unsupported claim.
- No demo output written as observed evidence.
- Main TuringResearch repository remains the flagship.
