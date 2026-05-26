# VGGT Local Project Links



This example documents local co-location for the VGGT human-prior dogfood path.

It is a template only. The real `local_project_links.yaml` stays machine-private

and is ignored by Git.



## Boundary



- Mode: `local-colocation`

- Access: read-only

- Writes inside VGGT: forbidden

- VGGT experiments: not run by this configuration

- Network access: not required

- Missing candidate paths: record `missing` and continue



The example config contains only the local candidate paths needed for this

machine's VGGT dogfood layout. It does not contain API keys, tokens, remote

hosts, private datasets beyond the listed local candidates, or experiment

results.



## Expected Use



Round 34 may use the private config to inspect allow-listed local files and build

a status summary. It should keep all summaries under TuringResearch Plus, use

`summary-only` handling for `.npz`, and mark any claim that needs real evidence

as `requires-real-experiment` or `requires-human-review`.



Round 33.5 only commits the template, README, docs, and tests.
