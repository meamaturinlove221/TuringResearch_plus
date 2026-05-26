# Open Source Blockers

Round: 360.6
Status: no active blockers for local open source hygiene gate

## No Active Blockers

The current local hygiene gate found no active blocker for continuing the
public-readiness preparation line.

## Human Review Remains Required

These items are not automated blockers for this local hygiene gate, but they
remain required before an actual public release:

- final license selection and approval;
- security contact process;
- maintainer approval for any public release;
- maintainer approval for any PyPI publication;
- maintainer approval for any GitHub release or tag;
- maintainer approval for any split repository publication.

## Standing No-go Conditions

The gate must become no-go if any of the following appear:

- old public project name on public surfaces;
- fake GitHub URL;
- secret or token-like value;
- committed `.env`;
- raw data;
- restricted model payload;
- private local path;
- live mode enabled by default;
- ARIS described as implemented;
- fake/demo output described as observed evidence.
