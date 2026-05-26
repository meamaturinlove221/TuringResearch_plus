# VGGT / SMPL-X Evidence Ledger



Status legend: `observed`, `local-observed`, `planned`, `fake-data`,

`requires-real-paper`, `requires-real-experiment`, `requires-human-review`,

`missing`.



This ledger documents how Round 34 separates user-provided engineering context

from local scan evidence. It is not a promotion ledger and does not contain

final advisor approval.



## Evidence Sources



| Source | Status | Notes |

| --- | --- | --- |

| User-provided engineering context | observed | May describe historical VGGT engineering facts, but is not local scan evidence. |

| `local_scan_summary.md` | local-observed | Present; records root candidates and missing private config. |

| `local_scan_artifact_index.md` | local-observed | Present; records no scanned artifacts. |

| `local_scan_missing_items.md` | local-observed | Present; records missing private config. |

| `local_scan_evidence_ledger.json` | missing | Required before V120/V121 can become local-observed. |

| `local_scan_visual_inventory.md` | missing | Required before true visual readiness can be discussed. |



## Milestone Ledger



| Milestone | Status | Evidence class | Boundary |

| --- | --- | --- | --- |

| V770 crop residual | observed | engineering context | Not full-body completion; local artifact confirmation missing. |

| V129 SMPL-X anchored completion | observed | engineering context | Local positive signal was reported, but full body / hairline regression remains relevant. |

| V260 semantic-temporal fusion | observed | engineering context | Audit only; adjacent predictions and strong semantic assets were hard-blocked. |

| V900 feature adapter entrypoint | observed | engineering context | Architecture entrypoint reportedly ran; local scan did not confirm artifacts. |

| V930 HumanRAM-style tri-plane adapter | observed | engineering context | Short training signal reportedly existed; local scan did not confirm artifacts. |

| V999 long-run triplane-only | observed | engineering context | Long-run reportedly completed; true SparseConv3D backend was unavailable then. |

| V120 Modal real spconv backend success | requires-human-review | missing | Cannot be local-observed without local scan or evidence ledger confirmation. |

| V121 true region pointcloud visual gate | requires-human-review | missing | Cannot be local-observed without visual inventory or evidence ledger confirmation. |



## Promotion Boundary



| Claim | Status | Rule |

| --- | --- | --- |

| Review-ready proxy | planned | May be recorded later if local evidence exists. |

| Promotion | requires-human-review | Must not be inferred from review-ready status. |

| Final advisor acceptance | requires-human-review | Not claimed in Round 34. |

| Paper result | requires-real-paper | Requires real citations and paper-writing evidence. |

| Experiment result | requires-real-experiment | Requires real VGGT run evidence and artifact-backed metrics. |
