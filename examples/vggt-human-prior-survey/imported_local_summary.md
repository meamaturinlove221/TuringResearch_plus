# Imported Local Summary



Status: planned



Round 33.5 establishes the local co-location contract for VGGT dogfooding. No

VGGT output was modified.



No VGGT experiment was run.



No VGGT metric or quality result is claimed in this summary.

This means no VGGT metric or quality result is claimed.



## Source



- Config template:

  `examples/vggt-human-prior-survey/local_project_links.example.yaml`

- Mode: `local-colocation`

- Access: read-only



## Candidate Groups



| Group | Status | Notes |

| --- | --- | --- |

| `vggt_root_candidates` | planned | Round 34 may mark each candidate `observed` or `missing`. |

| `output_candidates` | planned | File presence must not be interpreted as experiment success. |

| `docs_candidates` | planned | Missing docs paths should be recorded as `missing`, not fatal. |



## Evidence Boundary



- Local path existence can be recorded as `observed`.

- Unavailable paths should be recorded as `missing`.

- VGGT paper claims require `requires-real-paper`.

- VGGT experiment claims require `requires-real-experiment`.

- Promotion or quality conclusions require `requires-human-review`.
