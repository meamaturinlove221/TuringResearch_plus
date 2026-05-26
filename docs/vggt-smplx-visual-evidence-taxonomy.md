# VGGT / SMPL-X Visual Evidence Taxonomy



Status legend: `observed`, `local-observed`, `planned`, `fake-data`,

`requires-real-paper`, `requires-real-experiment`, `requires-human-review`,

`missing`.



Round 34 distinguishes visual proxies from visual evidence that could support

human review. No visual result is claimed as advisor-approved.



## Evidence Types



| Evidence type | Status | Use |

| --- | --- | --- |

| Proxy heatmap | planned | Useful for adapter debugging, but not enough for advisor visual readiness. |

| Rasterized pose feature preview | planned | Helps inspect HumanRAM-style token inputs. |

| Tri-plane feature slice | planned | Helps inspect neural texture features, not geometry quality by itself. |

| Sparse voxel / latent field preview | planned | Helps validate sparse backend wiring. |

| True region pointcloud closeup | requires-human-review | Required for H5 and visual readiness; currently not local-observed. |

| Full-body reconstruction board | requires-real-experiment | Needs real VGGT run and artifact-backed outputs. |

| Head-face / hairline / hands closeups | requires-real-experiment | Needed to test known failure areas. |



## Required Visual Gates



| Gate | Status | Notes |

| --- | --- | --- |

| Proxy versus true closeup separation | planned | Visual inventory must name which kind of artifact each image is. |

| Region labels | planned | full body, head-face, hairline, left hand, right hand, background leakage. |

| Source artifact reference | missing | `local_scan_visual_inventory.md` is absent. |

| Reviewer decision | requires-human-review | Human review must stay separate from local-observed artifact presence. |



## V121 Boundary



V121 is `requires-human-review` in Round 34. It can only become

`local-observed` if a later local scan explicitly confirms true region

pointcloud visual evidence. Even then, it is review-ready proxy evidence, not

promotion and not final advisor acceptance.
