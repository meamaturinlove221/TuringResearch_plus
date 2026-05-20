# Hypothesis Status

Status legend: `observed`, `local-observed`, `planned`, `fake-data`,
`requires-real-paper`, `requires-real-experiment`, `requires-human-review`,
`missing`.

Round 34 uses user-provided engineering context as `observed` and local scan
files as `local-observed`. The current local scan did not confirm V120/V121, so
SparseConv3D / Modal success and true region pointcloud visual gate remain
`requires-human-review`.

| ID | Hypothesis | Hypothesis status | Evidence label | Notes |
| --- | --- | --- | --- | --- |
| H1 | HumanRAM-style tri-plane feature token improves human-region VGGT geometry. | observed-positive | observed | V930/V999 are user-provided engineering context; local artifact confirmation is missing. |
| H2 | NeuralBody-style SMPL-X voxel feature + SparseConv3D improves beyond tri-plane. | planned / requires-real-experiment | requires-human-review | V120/V121 were not confirmed by local scan. |
| H3 | Hybrid sparse latent field to VGGT token gives stronger full-body / hand / hairline completion. | planned | requires-real-experiment | No hybrid evidence exists in current local scan. |
| H4 | Uncertainty gate prevents SMPL-X alignment errors from harming full body / hairline. | planned | requires-real-experiment | Needs ablation against known hairline/full-body regressions. |
| H5 | True region pointcloud closeup is required for advisor visual readiness. | planned | requires-human-review | Visual inventory is missing; review-ready is not promotion. |

## Conditional Update Rule

If a later local scan explicitly confirms V120/V121 in
`local_scan_summary.md` or `local_scan_evidence_ledger.json`, update only these
evidence labels:

| ID | Conditional status | Boundary |
| --- | --- | --- |
| H1 | observed-positive | May remain based on V930/V999 context. |
| H2 | local-observed-positive-proxy | Review-ready proxy only; not advisor final acceptance. |
| H3 | planned / requires-real-experiment | Unless hybrid evidence is explicitly found. |
| H4 | planned | Requires its own experiment. |
| H5 | local-observed-positive-proxy | True pointcloud closeup gate may be review-ready, not promotion. |

