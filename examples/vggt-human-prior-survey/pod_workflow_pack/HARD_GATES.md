# Modal SparseConv3D Hard Gates



Status: planned gate checklist. No gate has passed from this route pack alone.



## Required Gates



| Gate | Required Evidence | Failure If Missing |

| --- | --- | --- |

| real sparse backend required | Real `spconv`, `MinkowskiEngine`, or `TorchSparse` probe log from Modal Linux GPU | `REAL_BACKEND_UNAVAILABLE` / `SPARSE_BACKEND_UNAVAILABLE` |

| not report-only | Code path produces artifacts, not only narrative text | `REPORT_ONLY` |

| not fast-return | Controller cannot stop after a shallow summary | `FAST_RETURN` |

| not fallback-only | Sparse route is actually attempted when backend exists | `FALLBACK_ONLY` |

| not identity copy | Candidate output is not unchanged VGGT output copied as success | `IDENTITY_COPY` |

| no promotion | Planned route cannot be promoted without hard evidence | `PROMOTION_FORBIDDEN` |

| candidate predictions included | Candidate outputs or thin summaries are present | `MISSING_ASSETS` |

| visual boards included | Full-body, hairline, and hand/object boards are present | `VISUAL_PROOF_INSUFFICIENT` |

| NPZ diff included | NPZ diff or thin summary compares baseline vs candidate | `NOT_ENOUGH_EVIDENCE` |

| sha256 manifest included | Hash manifest covers key artifacts | `PACKAGE_INCOMPLETE` |

| zip test clean | Bundle extracts cleanly and expected files exist | `PACKAGE_INCOMPLETE` |

| cleanup report included | Temporary and private paths are excluded | `PACKAGE_INCOMPLETE` |

| hairline checked | Hairline comparison is included | `HAIRLINE_REGRESSION` |

| hand/object checked | Hand/object confusion check is included | `HAND_OBJECT_CONFUSION` |

| full body checked | Full-body visual board is included | `VISUAL_PROOF_INSUFFICIENT` |



## Promotion Rule



Do not mark SparseConv3D as successful unless all required artifacts exist and

the evidence ledger records the result as observed or local-observed. `planned`,

`requires-real-experiment`, and `not-enough-evidence` never pass promotion.
