# Plugin Review Checklist

Status: design checklist.

Round: 161.

Use this checklist before accepting a plugin into any future plugin catalog.

## Manifest

- [ ] Manifest exists.
- [ ] Plugin id is unique.
- [ ] Plugin type is valid.
- [ ] Version is declared.
- [ ] Capabilities are declared.
- [ ] Inputs and outputs are declared.
- [ ] Required permissions are declared.
- [ ] Safety level is declared.
- [ ] Status is declared.

## Safety

- [ ] Third-party plugin is disabled by default.
- [ ] Sandbox policy report exists.
- [ ] Extension safety report exists.
- [ ] Compatibility report exists.
- [ ] Human review is required.
- [ ] No `core.*` tool override.
- [ ] No unknown dynamic entrypoint is loaded.

## Forbidden Or Blocked By Default

- [ ] No secrets access.
- [ ] No `execute_code` by default.
- [ ] No shell access by default.
- [ ] No remote write by default.
- [ ] No hidden network requirement.
- [ ] No raw data access without restricted review.

## Docs And Tests

- [ ] README or docs exist.
- [ ] Test plan exists.
- [ ] Fake/demo mode is documented.
- [ ] Live mode, if any, is opt-in.
- [ ] Required environment variables are documented without real values.

## Release Decision

- [ ] Accepted as disabled metadata.
- [ ] Maintainer review complete.
- [ ] No release blocker remains.

If any forbidden item is present, block the contribution until a future approved
sandbox gate explicitly allows it.
