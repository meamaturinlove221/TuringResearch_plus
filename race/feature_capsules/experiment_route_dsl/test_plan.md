# Test Plan: experiment_route_dsl

## Unit tests

- `test_route_spec_requires_name_goal_and_steps`
- `test_route_step_requires_expected_evidence`
- `test_unknown_gate_label_rejected`
- `test_controller_prompt_draft_marks_planned_work`

## Contract tests

- `test_experiment_route_contract_fields`
- `test_route_tool_is_capsule_local_until_public_contract_acceptance`

## Workflow tests

- Compile a V260 hard-blocked fixture.
- Compile a V999 planned route fixture.
- Compile a Modal Real SparseConv3D next-action fixture.

## Non-goals

- No VGGT execution.
- No Modal live execution.
- No private path read.
- No planned-to-observed promotion.
