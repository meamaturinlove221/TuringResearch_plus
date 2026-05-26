# Physical Split Human Confirmation

Status: required before any external split.

Round: 337.

Physical split execution requires human confirmation. Automation may prepare
packages and reports, but it must not create repositories or push external
remotes.

## Confirmation States

| State | Meaning |
| --- | --- |
| `not_requested` | No human has requested creation. |
| `reviewing` | Human is reviewing file tree, README, and safety reports. |
| `approved_for_manual_create` | Human approved manual repository creation. |
| `rejected` | Human rejected the split. |
| `blocked_by_safety_gate` | Safety gate found a blocker. |

## Required Human Confirmation Checklist

Before a child repo is created manually, the human reviewer must confirm:

- exact bundle path;
- intended repository owner and name;
- README flagship backlink wording;
- no nonexistent real URL;
- no private data;
- no secrets;
- no raw data;
- no restricted model payloads;
- no unsupported experiment claims;
- no fake/demo output presented as observed evidence;
- no change to flagship install path;
- external push target, if any.

## Approval Text Template

```text
I approve manual creation of <repo-name> from <split_ready/path>.
I confirm the bundle is public-safe, links back to the flagship, contains no
private data or secrets, and does not replace the flagship repository.
```

This template is documentation only. It is not an approval record by itself.
