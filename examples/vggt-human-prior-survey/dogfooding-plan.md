# Round 34 Dogfooding Plan: VGGT / SMPL-X Human Prior



Status legend: `observed`, `local-observed`, `planned`, `fake-data`,

`requires-real-paper`, `requires-real-experiment`, `requires-human-review`,

`missing`.



Round 34 plans how TuringResearch will dogfood against the local VGGT /

SMPL-X human-prior and feature-adapter line. It does not run VGGT, does not

modify VGGT files, does not use network access, does not fabricate results, and

does not make promotion decisions.



## A. North Star



| Item | Status | Notes |

| --- | --- | --- |

| Research pivot | observed | Move from SMPL-X direct replacement / patch completion to SMPL-X feature encoding that VGGT can consume. |

| Dogfooding goal | planned | Use TuringResearch to organize local evidence, literature questions, hypotheses, and Round 35 sprint selection. |

| Paper conclusion | requires-real-paper | No real paper conclusion is claimed in this plan. |



## B. Local Evidence Intake



Round 34 read these local scan files first:



| Input | Status | Round 34 interpretation |

| --- | --- | --- |

| `local_scan_summary.md` | local-observed | Present. It records local co-location roots and says private config is missing. |

| `local_scan_artifact_index.md` | local-observed | Present. It records that no artifacts were scanned in the current dry run. |

| `local_scan_missing_items.md` | local-observed | Present. It records missing `local_project_links.yaml`. |

| `local_scan_evidence_ledger.json` | missing | Not present; Round 33.6 local evidence intake is incomplete for Round 34. |

| `local_scan_visual_inventory.md` | missing | Not present; visual evidence inventory requires-human-review. |

| `local_project_links.yaml` | missing | Not present; artifact scanning did not start. |



Local status for named VGGT milestones:



| Milestone | Engineering context status | Local scan status | Round 34 use |

| --- | --- | --- | --- |

| V900 feature adapter entrypoint | observed | requires-human-review | User-provided engineering context says the architecture entrypoint ran; local scan did not confirm artifacts. |

| V930 HumanRAM-style tri-plane adapter | observed | requires-human-review | User-provided engineering context says short training had signal; local scan did not confirm artifacts. |

| V999 long-run triplane-only best candidate | observed | requires-human-review | User-provided engineering context says long-run completed and triplane-only was best; local scan did not confirm artifacts. |

| V120 Modal real spconv backend success | requires-human-review | missing | Not local-observed because neither evidence ledger nor scan artifacts confirm it. |

| V121 true region pointcloud visual gate | requires-human-review | missing | Not local-observed because visual inventory and evidence ledger are missing. |



Review-ready is not promotion. V120/V121, even if later confirmed, must remain

review-ready proxy evidence until human review and promotion criteria are

separately recorded.



## C. Literature Survey Plan



| Topic | Status | Purpose |

| --- | --- | --- |

| VGGT / feed-forward geometry | planned | Establish what VGGT-style architectures can ingest as geometry context. |

| SMPL-X feature encoding | planned | Compare direct surface priors with feature-token conditioning. |

| NeuralBody-style sparse voxel / structured latent code | requires-real-paper | Verify structured latent code, SMPL 3D point, voxel feature, and SparseConvNet claims from real papers. |

| HumanRAM-style tri-plane / rasterized pose token | requires-real-paper | Verify canonical SMPL-X point, tri-plane neural texture, rasterized pose feature, and transformer-token routes. |

| HART / HGGT / Fus3D / VGGT-HPE / human reconstruction | requires-real-paper | Map related human reconstruction methods without inventing citations. |

| sparseconv3d / spconv / MinkowskiEngine / TorchSparse | planned | Identify viable sparse backends and fallback risks for VGGT dogfooding. |



## D. Gap Analysis



| Gap question | Status | Round 34 note |

| --- | --- | --- |

| Does a VGGT + SMPL-X feature adapter already exist? | requires-real-paper | Needs paper survey and local code evidence; current evidence is engineering context only. |

| Does SMPL voxel feature to VGGT token exist? | requires-real-paper | NeuralBody-like ideas require source verification before claims. |

| Does VGGT human point completion exist as a tested route? | requires-real-experiment | Current context has proxy signals, not a confirmed full-body completion result. |

| How is this different from HumanRAM / NeuralBody / HART? | planned | Difference should center on VGGT token injection and feed-forward geometry conditioning. |

| Is current evidence single sample / single scene only? | requires-human-review | Local scan did not inventory artifacts, scenes, or sample counts. |

| Is visual evidence proxy heatmap or true pointcloud closeup? | requires-human-review | Visual inventory is missing, so true closeup readiness cannot be claimed. |



## E. Hypotheses



| ID | Hypothesis | Status | Evidence label |

| --- | --- | --- | --- |

| H1 | HumanRAM-style tri-plane feature token improves human-region VGGT geometry. | observed-positive | observed engineering context from V930/V999; local confirmation requires-human-review. |

| H2 | NeuralBody-style SMPL-X voxel feature + SparseConv3D improves beyond tri-plane. | planned | requires-real-experiment; V120/V121 are not local-observed. |

| H3 | Hybrid sparse latent field to VGGT token gives stronger full-body / hand / hairline completion. | planned | requires-real-experiment unless hybrid evidence is later found. |

| H4 | Uncertainty gate prevents SMPL-X alignment errors from harming full body / hairline. | planned | requires-real-experiment. |

| H5 | True region pointcloud closeup is required for advisor visual readiness. | planned | visual evidence inventory is missing; requires-human-review. |



## F. Ideation Pool



| Idea | Status | Notes |

| --- | --- | --- |

| canonical feature raster | planned | Encode canonical SMPL-X cues as VGGT-readable features. |

| body-part token | planned | Add part-aware tokens for hands, hairline, head-face, and full body. |

| tri-plane neural texture | observed | Engineering context says V930/V999 produced signal; local artifact confirmation is missing. |

| sparse voxel feature | planned | Requires sparse backend validation. |

| sparseconv latent field | planned | Requires Modal/spconv local evidence before local-observed status. |

| token injection | planned | Candidate adapter path for VGGT backbone conditioning. |

| residual geometry decoder | planned | Use as an ablation against feature-token conditioning. |

| uncertainty / reliability gate | planned | Gate harmful SMPL-X alignment. |

| Modal sparse backend validation | requires-human-review | V120/V121 not confirmed by local scan. |

| artifact auditor | planned | Needed to turn local files into traceable evidence. |

| visual evidence auditor | planned | Needed to distinguish proxy heatmaps from true pointcloud closeups. |

| local evidence ledger | missing | `local_scan_evidence_ledger.json` is absent. |



## G. Convergence Scoring Plan



Score each idea on a 1-5 scale in Round 35. No score is assigned in Round 34.



| Criterion | Status | Description |

| --- | --- | --- |

| metric benefit | planned | Expected improvement on human-region geometry. |

| implementation cost | planned | Local VGGT engineering effort and backend dependencies. |

| paper contribution clarity | planned | Whether the idea is a clear method contribution. |

| dependency readiness | planned | Availability of VGGT entrypoints, SMPL-X features, and sparse backends. |

| risk | planned | Alignment, artifact, and regression risk. |

| testability | planned | Whether an ablation can isolate the idea. |

| local evidence availability | requires-human-review | Artifact index is empty in the current dry run. |

| advisor visual readiness | requires-human-review | Visual inventory is missing. |



## H. Experiment Plan



| Area | Status | Round 34 plan |

| --- | --- | --- |

| Baselines | planned | V647 / V117 / V770 / V129 / V930 / V999; V120 only if later local-observed. |

| Ablations | planned | raster / tri-plane / voxel / sparseconv / hybrid. |

| Metrics | planned | full body, head-face, hairline, left/right hand, background leakage, depth-normal consistency. |

| Failure cases | planned | SMPL-X weak alignment, sparse backend unavailable, phone-object confusion, hairline degradation. |

| Visual checks | planned | Separate proxy heatmap from true region pointcloud closeup. |

| Real experiment execution | requires-real-experiment | No VGGT experiment is executed in Round 34. |



## I. Future Sync Adapters



These are future plans only and are not implemented in Round 34:



| Adapter route | Status |

| --- | --- |

| v0.3 Handoff Bundle Export / Import | planned |

| v0.4 NAS / SMB Shared Artifact Store | planned |

| v0.5 SSH / SFTP Remote Artifact Reader | planned |

| v0.6 GitHub Artifact Sync | planned |

| cloud object storage adapter | planned |
