# Launch Risk Register

Status: planning risk register.

Round: 163.

## Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| README overclaims autonomous research | high | Keep "What It Does Not Do" section near the top. |
| Fake demo mistaken as benchmark | high | Label demo/replay outputs as fake/default and not research success. |
| VGGT case mistaken as experiment success | high | Keep dogfooding and no SparseConv3D success language explicit. |
| Private data leak | high | Run privacy, secret, raw-data, model-payload, and private-path scans. |
| Plugin safety misunderstood | high | State unknown third-party plugins are disabled and not executed. |
| License posture unclear | medium | Link license review and compliance disclaimer. |
| Star strategy becomes hype | medium | Avoid star promises and fake social proof. |
| Split candidates confuse users | medium | Keep flagship as install/star entry point and mark split skeletons design-only. |
| Screenshots leak sensitive data | high | Use only public-safe screenshot plan and review assets before publish. |
| Roadmap read as shipped | medium | Separate shipped features from planned v0.8 work. |

## No-Go Conditions

- secrets detected;
- raw data included;
- private paths included;
- model payloads included;
- unsupported VGGT success claim;
- fake benchmark claim;
- fake user or offer claim;
- live adapters implied as default;
- license posture unresolved.
