# TulingResearch Plus Example: Citation Graph Demo

Mode: fake adapter.

This example demonstrates semantic graph expansion without a real Semantic Scholar API key.

## Expected Artifacts

- CitationGraph
- recommended_next_reads
- frontier nodes

## Inputs

- `input/request.json` defines seed papers, depth, node budget, and recommendation limit.
- `fake_run_config.yaml` fixes fake adapter mode and no-network execution.

## Outputs

- `expected_outputs/artifact_list.json` lists the required graph artifacts.
- `expected_outputs/expected_summary.md` documents expected nodes, frontier nodes, and recommended next reads.

No real network access, real API key, Semantic Scholar key, or live graph API is required.
