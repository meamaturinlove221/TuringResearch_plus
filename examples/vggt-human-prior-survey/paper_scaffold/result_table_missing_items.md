# Result Table Missing Items



- Result tables allowed: `false`

- Planned is not executed: `true`

- Dashboard is not result: `true`

- Requires human review: `true`



## Missing Result Tables



- main_quantitative_results

- ablation_results

- failure_case_visual_table



## Missing Artifacts



- `predictions.npz`

- `board_inventory.md`

- `sha256_manifest.txt`

- `cleanup_report.md`



## Blocked Claims



- Do not report quantitative result values without real run evidence.

- Do not claim planned route execution as completed.

- Do not treat dashboard status as a paper result.

- Do not claim SparseConv3D success without backend evidence.

- Run status `ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS` is not ready for result tables.

- Route status `requires-real-experiment` is not executed.



## Boundary



- No result value is generated.

- No figure or table is fabricated.

- Missing tables stay missing until real evidence exists.
