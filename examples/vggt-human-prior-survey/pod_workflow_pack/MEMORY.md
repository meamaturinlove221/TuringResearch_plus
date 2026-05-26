# MEMORY



Route `modal_sparseconv_real_v0` is planned and requires a real experiment.

SparseConv3D success is not observed.

Evidence Ledger, Artifact Audit, Run Ingest, and Handoff Manifest remain source of truth.

Future pod outputs must return structured artifacts for review.



# Memory Policy



`MEMORY.md` is a handoff-safe summary, not the only source of truth.



## Allowed Content



- project summary

- route summary

- evidence-backed status

- known blockers

- handoff-safe next actions



## Forbidden Content



- API key

- .env

- raw data path with secret

- SMPL-X body model files

- private data

- unreviewed session transcript



## Source of Truth



Evidence Ledger, Artifact Audit, Run Ingest, and Handoff Manifest



- Bidirectional sync: `false`

- Review required: `true`
