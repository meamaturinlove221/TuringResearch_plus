# Dataset / License Compliance Assistant

Status: v0.7 minimal implementation.

Round 138 adds a local compliance assistant for datasets, models, papers, and
code repositories. It creates a checklist and risk report; it does not provide
legal advice and does not download license text.

## Inputs

- Dataset records.
- Model records.
- Paper / figure reuse records.
- Code repository records.
- Known license labels and usage restrictions.

## Output

`ComplianceReport` contains:

- `datasets`
- `models`
- `papers`
- `code_repos`
- `licenses`
- `usage_restrictions`
- `redistribution_risk`
- `publication_risk`
- `missing_license_info`
- `requires_human_review`

## VGGT Case Rules

- SMPL-X model files are marked license restricted and not bundled.
- Raw datasets are not public packaged by default.
- Third-party paper figures require human review before reuse.
- GitHub code with missing license metadata is marked unknown.
- Compliance reports are not legal advice.

## Risk Hints

- Unknown licenses are publication and release risks.
- Restricted or proprietary assets are release blockers until reviewed.
- Bundled assets require explicit public-release permission.
- Raw datasets are not public-release safe by default.
- Third-party paper figures require reuse permission review.

## Safety Boundary

- No network access.
- No automatic license download.
- No restricted data packaging.
- No legal advice.
- No private VGGT path reads.
- Human review remains required.

## Related Documents

- [Compliance Disclaimer](compliance-disclaimer.md)
- [License Review](license-review.md)
- [Privacy / Data Policy Layer](privacy-data-policy-layer.md)
- [Public Release Hardening](public-release-hardening.md)
