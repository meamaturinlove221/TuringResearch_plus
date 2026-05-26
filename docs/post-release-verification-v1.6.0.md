# Post-release Verification v1.6.0

Status: manual verification plan.

Round: 388.

Use this plan only after a maintainer intentionally performs a release action.
Round 388 itself does not publish anything.

## If A GitHub Release Is Published Later

Verify:

- release title uses TuringResearch;
- release text matches `docs/github-release-draft-v1.6.0.md`;
- tag points to the intended commit;
- release notes do not claim public docs deployment unless it exists;
- release notes do not claim PyPI publication unless it happened;
- release notes do not claim split repositories exist unless they were created;
- limitations and ARIS deferred sections remain present.

## If GitHub Pages Is Enabled Later

Verify:

- docs bundle was reviewed before deployment;
- real URL is inserted only after deployment exists;
- no fake URL remains;
- no analytics or external tracking is enabled unless separately approved;
- no secrets, raw data, restricted model payloads, or private paths are present.

## If PyPI Publication Happens Later

Verify:

- package name decision is approved;
- version matches the intended release;
- artifacts were inspected before upload;
- README renders safely;
- compatibility import paths remain documented;
- no private files are included in wheel or sdist.

## If Split Repositories Are Created Later

Verify:

- repositories were created manually;
- README files link back to the flagship repository only after real URLs exist;
- no raw data, restricted model payload, private path, secret, or unsupported
  claim was copied;
- split packs remain case/demo spokes, not install targets.

## If Optional Live Smoke Runs Later

Verify:

- live was explicitly enabled in a private environment;
- no credentials were committed;
- output passed redaction;
- no live output was promoted to observed evidence without human review;
- live remains disabled in the default test suite.

## Final Safety Check

After any release action, rerun:

```bash
python -m pytest tests/contract/test_public_name_integrity_turingresearch.py tests/contract/test_open_source_hygiene_gate.py tests/contract/test_public_release_hygiene.py tests/contract/test_name_integrity.py -q
python -m pytest tests/contract/test_v1_6_release_contracts.py tests/workflow/test_v1_6_full_replay.py -q
```

Treat any failure as a release blocker until reviewed.
