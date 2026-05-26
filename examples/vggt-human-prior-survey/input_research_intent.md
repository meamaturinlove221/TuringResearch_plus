# Input Research Intent



Status legend: `observed`, `local-observed`, `planned`, `fake-data`,

`requires-real-paper`, `requires-real-experiment`, `requires-human-review`,

`missing`.



## Intent



| Field | Status | Content |

| --- | --- | --- |

| Project | observed | VGGT / SMPL-X Human Prior dogfooding inside TuringResearch Plus. |

| North Star | observed | Shift from SMPL-X direct replacement to SMPL-X feature encoding for VGGT. |

| Local mode | local-observed | TuringResearch Plus and VGGT roots are co-located on this machine, but private artifact scan config is missing. |

| Real experiment boundary | requires-real-experiment | Round 34 does not run VGGT or claim experiment results. |

| Human review boundary | requires-human-review | Advisor readiness and promotion are not claimed. |



## Engineering Context Provided By User



| Item | Status | Notes |

| --- | --- | --- |

| V770 crop residual | observed | Local changes were observed in prior engineering context, but not full-body completion. |

| V129 SMPL-X anchored completion | observed | Local positive signal was reported, but full body / hairline degraded before. |

| V260 semantic-temporal fusion | observed | Audit only; adjacent predictions and strong semantic assets were hard-blocked. |

| V900 feature adapter entry | observed | Architecture entrypoint reportedly ran. |

| V930 tri-plane adapter | observed | Short training reportedly had signal. |

| V999 long-run | observed | Completed with triplane-only as best candidate; true SparseConv3D backend unavailable at that time. |

| V120 / V121 | requires-human-review | Not confirmed by local scan inputs; cannot be marked local-observed. |



## Desired Research Shape



| Track | Status | Notes |

| --- | --- | --- |

| HumanRAM route | planned | Canonical SMPL-X point, tri-plane neural texture, rasterized pose feature, transformer token. |

| NeuralBody route | planned | SMPL structured latent code, SMPL 3D point, voxel feature, SparseConvNet encoding. |

| VGGT integration route | planned | Convert SMPL-X structure into VGGT-readable tokens/features without direct patch replacement. |

| Evidence requirement | planned | Use local scan ledger and visual inventory before any promotion discussion. |
