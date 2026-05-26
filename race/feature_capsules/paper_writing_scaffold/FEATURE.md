# Paper Writing Scaffold



Status: feature capsule draft.



Release target: v0.6 Sprint 3.



## 1. Problem



Paper digest and related-work reports need a safe path toward writing support without generating final paper conclusions.



## 2. VGGT / Research Motivating Example



VGGT related work can produce outline bullets and claim checks, but not final publication prose or unsupported novelty claims.



## 3. Upstream / Internal Inspiration



Future Paper Writing Assistant and existing Paper Digest Engine.



## 4. User Story



As a researcher, I want paper section scaffolds that show evidence references, missing claims, and human-review notes.



## 5. Inputs



- paper digests

- method cards

- citation graph

- collision report

- evidence ledger



## 6. Outputs



- PaperWritingScaffold

- ClaimCheckReport

- SectionOutline



## 7. Data Model



PaperWritingScaffold, SectionPlan, ClaimCheckReport



## 8. Proposed Commands / Tools



- command: `turing paper scaffold`; tool: `paper.writing_scaffold`; output: `PaperWritingScaffold`



## 9. Related Contracts



- paper_writing_scaffold.yaml

- paper_digest.yaml

- related_work_positioning.yaml



## 10. Related Skills



- turingresearch-paper-writing-pipeline

- turingresearch-fusion-literature-survey



## 11. Required Tests



- section scaffold tests

- claim check tests

- fake paper workflow test



## 12. Risks



- draft reads as final paper

- citation fabrication

- copyright leakage



## 13. Done Criteria



- outputs are outlines/plans

- unsupported claims are listed

- requires-human-review is always present



## 14. Release Target



v0.6 Sprint 3



## 15. Non-goals



- no final paper generation

- no automatic submission

- no long copyrighted text copying
