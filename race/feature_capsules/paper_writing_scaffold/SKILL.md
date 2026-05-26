# Paper Writing Scaffold Skill



Status: planning skill draft.



Use this skill when a task is about `paper_writing_scaffold` planning, contract alignment, test

planning, or review. This skill does not execute live services, upload private

research data, or promote proposed evidence to observed evidence.



## When to Use



- The user asks for `Paper Writing Scaffold` scope, docs, contracts, tests, or review.

- The task needs v0.6 planning consistency.

- The output should remain local-first and review-required.



## Inputs



- paper digests

- method cards

- citation graph

- collision report

- evidence ledger



## Outputs



- PaperWritingScaffold

- ClaimCheckReport

- SectionOutline



## Safety Rules



- Do not use network access by default.

- Do not read private VGGT paths.

- Do not package secrets, raw data, or private model files.

- Do not mark fake/demo/planned results as observed.

- Do not claim experiment success without evidence.



## Related Contracts



- paper_writing_scaffold.yaml

- paper_digest.yaml

- related_work_positioning.yaml
