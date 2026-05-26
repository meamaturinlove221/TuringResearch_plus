# Split Safety Report: turingresearch-examples



- safe_to_export: `true`

- release_blocker: `false`

- requires_human_review: `true`



## Checked Files



- `examples_manifest.yaml`

- `README.md`



## Omitted Files



- none



## Findings



- `medium` `policy-mention:private_advisor_feedback` `README.md`: Safety policy text mentions an excluded private item.



## Limitations



- Dry-run export does not create repositories.

- Dry-run export does not push git remotes.

- Safety checks are pattern based and require human review.

- Public split candidates must still pass privacy and compliance review.
