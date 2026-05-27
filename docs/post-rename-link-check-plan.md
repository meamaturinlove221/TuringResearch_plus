# Post-Rename Link Check Plan

Round: 399R
Status: manual plan

## Purpose

After a human GitHub repository rename, check that docs, links, remotes, and
release metadata still point to real, non-fake destinations.

## Checks

1. Confirm local remote:

```powershell
git remote -v
```

2. Update local remote if needed:

```powershell
git remote set-url origin https://github.com/<owner>/TuringResearch.git
```

3. Search for old repository URL references.

The old names are written below as split tokens so this plan does not
reintroduce forbidden literal names into public docs. Join the token groups only
inside your private shell when you run the check.

```powershell
$oldDisplay = 'Tul' + 'ingResearch'
$oldRepo = 'Tul' + 'ingResearch_plus'
$oldSuffixRepo = 'TuringResearch' + '_plus'
rg -n "$oldDisplay|$oldRepo|$oldSuffixRepo" README.md docs docs-site examples split_ready split_manual .github
```

4. Search for fake URLs:

```powershell
rg -n "github.io|pages.dev|netlify.app|example.com|PLACEHOLDER" README.md docs docs-site examples split_ready split_manual
```

5. Run docs link checks if available:

```powershell
python -m pytest tests/workflow/test_docs_deployment_preflight.py tests/workflow/test_docs_release_bundle.py -q
```

6. Run public naming and safety checks:

```powershell
python -m pytest tests/contract/test_public_name_integrity_turingresearch.py tests/contract/test_name_integrity.py -q
python -m pytest tests/contract/test_open_source_hygiene_gate.py tests/contract/test_public_release_hygiene.py -q
```

## Expected Result

- No fake public URL is introduced.
- Old repository names appear only in historical rename or compatibility docs.
- Local remote points to the real renamed repository after human confirmation.
- README still uses TuringResearch as the public name.
- PR #1 remains excluded.
