# TuringResearch 项目说明书

TuringResearch 是一个 local-first 的 AI 辅助科研工作流系统。

## 1. 定位

它不是单纯的论文总结器，也不是单纯的代码助手。它要管理的是科研循环：

```text
意图 → 证据 → 假设 → 实验 → 产物 → 汇报 → 下一步
```

它适合长对话、长线任务、导师要求变化、产物很多、路线反复调整的科研项目。

## 2. 核心原则

- **Docs-first**：先写清楚目的和边界，再谈推广。
- **Evidence-first**：区分 observed、planned、fake-data、缺论文、缺实验。
- **Contract-first**：先定义输入、输出和硬门，再说工作流稳定。
- **Local-first**：live adapter 默认关闭，必须显式开启。
- **诚实范围**：不能把规划态输出写成已验证科研结果。

## 3. 主要层次

| 层次 | 作用 |
|---|---|
| Intake | 整理目标、约束、blocker、非目标。 |
| Literature | 把论文和引用变成结构化 method card。 |
| Gap / Hypothesis | 把缺口转成可测试路线。 |
| Experiment Route | 定义硬门、fallback 和预期产物。 |
| Artifact Audit | 检查 bundle、日志、图、hash、报告和 unsupported claim。 |
| Advisor Pack | 输出导师可读的摘要和下一步。 |
| Community Intake | 接收只含文档的 idea / skill proposal。 |

## 4. 证据标签

推荐保守使用：

- `observed`：真实验证过；
- `planned`：计划中；
- `fake-data`：演示数据；
- `requires-real-paper`：需要真实论文；
- `requires-real-experiment`：需要真实实验；
- `reference`：来自外部公开项目的启发。

## 5. 禁止事项

不要：

- 编造 publication；
- 夸大上游参考材料；
- 把参考项目源码直接混进主线；
- 发布私有路径或密钥；
- 用漂亮 README 掩盖证据缺失；
- 把 proxy 结果写成导师通过。

## 6. 贡献路径

### 实现型贡献

需要正常 code review、tests 和安全检查。

### idea / skill proposal 贡献

放在 `community/` 下，只提交文档。后续可以转成 feature capsule、skill、SOP、campaign 或 roadmap item。

## 7. 发布前检查

公开前确认：

- README 和 README_CN 一致；
- 吉祥物 SVG 在 README 最前面；
- 没有误导性的 academic-output migration 表述；
- live 功能默认关闭；
- 没有 secrets 和私有路径；
- 上游项目只写 reference / inspiration；
- planned 模块没有写成 finished feature。

## 8. 最后一条规则

不确定时，使用更保守的说法。

TuringResearch 的目标是让科研推进更清楚，而不是更玄学。
