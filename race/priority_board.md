# TulingResearch Plus Race Priority Board

Idea Radar outputs are staged here after `race.source_hygiene_check` passes or returns documentation-only watch. Implementation work is allowed only when the idea is public or authorized and source hygiene passes.

## Priority Elevator Rules

Formula:

`PriorityScore = 0.30 * value_score + 0.25 * urgency_score + 0.20 * feasibility_score + 0.15 * novelty_score + 0.10 * strategic_fit`

| Level | Action | Rule |
| --- | --- | --- |
| P0 | prototype immediately | score >= 0.85 and source hygiene passed |
| P1 | create feature capsule this sprint | score >= 0.70 and source hygiene passed |
| P2 | document and monitor | score >= 0.45 or source hygiene did not pass |
| P3 | archive | score < 0.45 |

Source hygiene that does not pass forces P0/P1 candidates down to P2.

## v0.2.0 Backlog Priorities

| Priority | Backlog | Candidate work | Owner skill | Source gate | Dependencies |
| --- | --- | --- | --- | --- | --- |
| P0 | BL-04 | API key handling and live test policy | `tulingresearch-qa-release` | no real keys in repo | existing pytest live/manual markers |
| P0 | BL-01 | Live Semantic Scholar adapter | `tulingresearch-fusion-semantic-graph` | provider public docs and terms | BL-04 |
| P0 | BL-02 | Live arXiv adapter | `tulingresearch-core-reproduction` | public arXiv data and terms | BL-04 |
| P0 | BL-05 | PDF figure extraction | `tulingresearch-pdf-markdown-core` | local/public fixture PDFs | PDF Phase A |
| P0 | BL-06 | PDF table extraction | `tulingresearch-pdf-markdown-core` | local/public fixture PDFs | PDF Phase A |
| P0 | BL-07 | PDF section tree and page map upgrade | `tulingresearch-pdf-markdown-core` | local/public fixture PDFs | PDF Phase A |
| P0 | BL-09 | Real citation graph optional expansion | `tulingresearch-fusion-semantic-graph` | live adapter opt-in only | BL-01, BL-04 |
| P0 | BL-13 | Stronger Vault search | `tulingresearch-fusion-wiki-vault` | local artifacts | existing Vault index |
| P0 | BL-14 | Vault graph traversal improvements | `tulingresearch-fusion-wiki-vault` | local artifacts | typed edge schema |
| P1 | BL-03 | Optional Apify web adapter | `tulingresearch-core-reproduction` | public web sources only | BL-04 |
| P1 | BL-08 | Better PDF quality report | `tulingresearch-pdf-markdown-core` | local/public fixture PDFs | BL-05, BL-06, BL-07 |
| P1 | BL-10 | Literature survey screening upgrade | `tulingresearch-fusion-literature-survey` | evidence-backed sources | BL-09 |
| P1 | BL-11 | Evidence matrix upgrade | `tulingresearch-fusion-literature-survey` | EvidenceRef required | BL-10 |
| P1 | BL-12 | Gap extraction improvement | `tulingresearch-fusion-literature-survey` | EvidenceRef required | BL-11 |
| P1 | BL-15 | Vault artifact ingestion improvements | `tulingresearch-fusion-wiki-vault` | local artifacts | BL-11, BL-13 |
| P1 | BL-16 | Upstream watch from public snapshots | `tulingresearch-race-upstream-watch` | public snapshots only | Source Hygiene |
| P1 | BL-17 | Better IdeaCard scoring | `tulingresearch-race-priority-elevator` | hygiene downgrade rules | existing IdeaCard fields |
| P1 | BL-18 | Feature capsule implementation workflow | `tulingresearch-race-feature-capsule-factory` | passed hygiene only | BL-17 |
| P1 | BL-19 | Better figure captions | `tulingresearch-paper-figure-asset-pipeline` | figure provenance required | BL-05 |
| P1 | BL-20 | Paper section status upgrade | `tulingresearch-paper-docflow-article-blocks` | evidence required | existing DocFlow |
| P1 | BL-21 | Method figure linkage | `tulingresearch-paper-writing-pipeline` | required figures present | BL-19, BL-20 |
| P1 | BL-22 | v0.2.0 examples upgrade | `tulingresearch-qa-release` | fake mode default | milestone completion |

## Later Roadmap Watch

| Priority | Target | Candidate work | Source gate | Release lane |
| --- | --- | --- | --- | --- |
| P1 | v0.3.0 | OCR pipeline and layout-aware PDF parsing | local PDF fixtures and public sample documents | Lane 03 PDF Markdown |
| P1 | v0.3.0 | Advanced survey, hypothesis-to-experiment polish, optional LLM-assisted convergence and stress checks | adapter protocol only, live providers manual | Lane 04 fusion |
| P2 | v0.3.0 | Source Hygiene dashboard export | internal Race Mode state | Lane 07 race mode |
| P2 | v0.4.0 | Race Mode upstream watch and automated Feature Capsule generation | public-only upstream snapshots | Lane 07 race mode |
| P2 | v0.4.0 | SOP graph UI/export-friendly artifacts and paper figure pipeline polish | internal contracts and paper assets | Lane 08 paper pipeline |
| P2 | v0.4.0 | Assisted paper writing with ExperimentReport hard gate | internal experiment and evidence artifacts | Lane 08 paper pipeline |
| P3 | v1.0.0 | Optional cloud/GPU execution adapters | explicit user configuration only | Future adapter lane |

## Release Gate Notes

- v0.2.0 must not make live network access the default path.
- v0.2.0 live adapters must be optional, adapterized, and tested with mocks by default.
- v0.2.0 PDF extraction must record provenance and warnings.
- Race Mode implementation promotion remains gated by Source Hygiene.
- Later versions must keep OCR, layout parsing, optional LLM, and cloud/GPU work opt-in and quality-gated.

## v0.2.0 Sprint 1 Feature Capsules

Round 37 creates capsule skeletons for the VGGT dogfooding Top 5. These are P0
planning inputs, not implemented features.

| Priority | Capsule | Proposed command | Proposed tool | Status | Dependency |
| --- | --- | --- | --- | --- | --- |
| P0 | `vggt_smplx_evidence_ledger` | `tuling vggt ledger build` | `vggt.evidence_ledger_build` | skeleton | Round 36 scope |
| P0 | `artifact_auditor` | `tuling audit artifact` | `artifact.audit` | skeleton | Evidence Ledger |
| P0 | `visual_evidence_auditor` | `tuling audit visual` | `visual.audit_evidence` | skeleton | Artifact Auditor |
| P0 | `advisor_pack_builder` | `tuling advisor pack` | `advisor.pack_build` | skeleton | Evidence Ledger and auditors |
| P0 | `pdf_phase_b_figure_table_extraction` | `tuling pdf extract-assets` | `pdf.extract_figures`, `pdf.extract_tables` | skeleton | PDF Phase B contracts |

The non-PDF proposed tool namespaces are capsule-local and must not be treated
as public API until a later contracts-first round accepts them.

## Watch Items

- Provider schema and rate-limit changes for scholarly APIs.
- PDF extraction quality across scanned and publisher-formatted documents.
- Evidence continuity across survey, insight, hypothesis, experiment, and paper artifacts.
- License compatibility for any public reference material.
