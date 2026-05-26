# Blocked Sections

## Blocked

- `abstract`: final abstract is blocked until claims, citations, and results are evidence-backed.
- `related_work`: real citation-grade references and human paper review are missing.
- `experiments`: route remains planned / requires-real-experiment.
- `results`: result tables and real run evidence are missing.
- `conclusion`: conclusion is blocked until results and safe claims exist.

## Blocking Evidence

- Citation safety report marks every citation candidate as not citation-grade.
- Result table guard has `result_tables_allowed=false`.
- Run status is `ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS`.
- Backend status is `real_backend_missing`.
- SparseConv3D success is not established.

## Unsafe Claims Still Blocked

- The related work has been completely reviewed.
- There is definitively no collision with existing papers.
- SparseConv3D integration is already successful.
- Planned route execution is completed.
- Dashboard status is a paper result.

## Boundary

- Blocked sections must not be drafted as final paper text.
- Missing evidence must remain visible.
- No planned item is promoted to observed.
