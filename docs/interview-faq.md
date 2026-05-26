# Interview FAQ

Status: portfolio draft.

Round: 158.

## 1. 这个项目解决什么问题？

它解决研究项目状态分散的问题：证据、artifact、实验路线、失败记录、论文笔记、advisor 沟通和 dashboard 往往各自漂移。TuringResearch Plus 把这些状态组织成可审查的本地 workflow。

## 2. 和普通文献总结器有什么区别？

普通文献总结器偏向“读论文并生成摘要”。TuringResearch Plus 覆盖更完整的研究操作系统：evidence ledger、artifact audit、route DSL、failure taxonomy、paper scaffold、advisor pack、dashboard、plugin safety、privacy gate 和 replay gate。

## 3. 为什么要 Evidence Ledger？

因为研究中最危险的问题之一是把 planned 写成 observed。Evidence Ledger 强制记录 claim 的状态、来源、缺口和人工复核需求。

## 4. 为什么要 Artifact Auditor？

论文和汇报不能只看文字，还要看支撑它的文件是否存在、是否完整、是否可公开、是否只是 placeholder。Artifact Auditor 用来暴露这些缺口。

## 5. 为什么要 Route DSL？

实验路线如果只存在脑子里或聊天记录里，很难复盘。Route DSL 把路线、hard gate、失败模式和下一步计划变成可检查的结构。

## 6. 怎么保证不伪造结果？

系统层面用 fake/live boundary、evidence status、quality gate、paper assembly gate、result table guard、claim guard 和 privacy/compliance gate 防止 fake/demo/planned 内容被写成 observed。

## 7. 怎么做测试？

测试分层包括 unit tests、workflow tests、contract tests、namespace import tests、privacy/hygiene tests、full fake replay、mypy 和 ruff。默认测试不需要真实 API key、live network、Modal 或私有项目路径。

## 8. 为什么先 monorepo？

因为项目还在形成旗舰体验。monorepo 让 README、quickstart、demo、测试、release gate 和 star 聚合在一个入口，便于面试官或用户理解完整系统。

## 9. 什么时候拆仓？

只有模块具备稳定 API、完整 docs、独立测试、无私有数据、无 license 风险、独立 demo 和明确价值时才考虑拆。优先候选是 case study 和 examples，不是 core。

## 10. 这个项目体现了什么工程能力？

它体现了系统设计、模块边界、测试策略、隐私/安全意识、插件架构、文档和 release 工程、产品定位、以及把复杂研究流程变成可审查系统的能力。
