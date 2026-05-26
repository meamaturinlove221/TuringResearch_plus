# Paper Reference E2E Demo

Status: fake/demo only.

This demo shows the local `scholar.paper_reference` workflow:

1. Start with public paper metadata.
2. Resolve fake/default references.
3. Resolve fake/default citations for review context.
4. Build a related-work seed.
5. Build a collision matrix input.

The outputs are review scaffolds. They are not verified citations, not complete
related work, and not final novelty or collision claims.

Files:

- `paper_metadata.json`: fake public paper metadata.
- `related_work_seed.json`: references/citations converted to review seed data.
- `collision_matrix_input.json`: conservative input for collision screening.
- `reference_e2e_report.md`: human-readable E2E report.
