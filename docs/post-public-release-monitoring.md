# Post Public Release Monitoring

Round: 400R
Status: monitoring plan

## First Hour

- Confirm repository is visible only if maintainers intended it.
- Confirm README renders correctly.
- Confirm About section has no fake URL.
- Confirm topics are appropriate.
- Confirm no PR #1 showcase files appeared.
- Confirm no fake user/star/benchmark claims.

## First Day

- Watch issues and PRs for accidental secret/private-data submissions.
- Ask contributors to use community idea / skill proposal templates only.
- Re-run public naming and open-source hygiene checks after any urgent edit.
- Confirm docs bundle links still point to real local or deployed assets.

## First Week

- Review whether PR #2 community intake needs further guardrails.
- Decide whether GitHub Pages should be manually enabled.
- Decide whether split repos should be created manually.
- Decide whether PyPI preparation should continue.
- Record any confusion around upstream reference wording.

## Escalation

Immediately pause public promotion if any of the following appears:

- secret or credential leak;
- raw data or private path leak;
- unsupported VGGT/SparseConv3D success claim;
- migrated academic publication claim without source artifacts;
- fake benchmark or fake usage claim;
- live remote execution accidentally enabled;
- ARIS described as implemented.
