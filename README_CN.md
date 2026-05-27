<p align="center">
  <img src="./assets/turingresearch_mascot.svg" width="260" alt="TuringResearch mascot" />
</p>

<h1 align="center">TuringResearch</h1>

<p align="center">
  <b>面向 AI 辅助科研迭代的 local-first 研究操作系统。</b>
</p>

<p align="center">
  把混乱的科研目标整理成证据台账、方法卡、实验路线、artifact 审计和导师汇报包。
</p>

<p align="center">
  <a href="./README.md">English</a> ·
  <a href="#为什么需要-turingresearch">为什么需要</a> ·
  <a href="#它能做什么">功能</a> ·
  <a href="#架构">架构</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#安全边界">安全边界</a>
</p>

---

## 为什么需要 TuringResearch

很多 AI 工具能总结论文、写计划。

但真实科研推进更麻烦：

- 导师目标会变化；
- 实验证据经常不完整；
- bundle、图、日志、报告会越来越碎；
- planned、observed、fake demo 容易混在一起；
- 长线 Codex 任务容易偏离最初目标；
- 汇报材料不仅要漂亮，还要足够诚实。

**TuringResearch 就是为这个缝隙设计的。**

它围绕这条科研循环展开：

```text
意图 → 文献 → gap → 假设 → 路线 → 实验 → 产物 → 汇报 → 下一轮 sprint
```

---

## 它能做什么

| 能力 | 作用 |
|---|---|
| Research intake | 把模糊目标拆成约束、非目标、blocker 和下一步。 |
| Evidence ledger | 区分 observed、planned、fake fixtures、缺论文、缺实验。 |
| Literature workflow | 整理 survey plan、method card、reference map 和相关工作定位。 |
| Hypothesis planning | 把 gap 转成假设树和路线树。 |
| Experiment runbook | 生成带硬门和 fallback 的 Codex 长线执行计划。 |
| Artifact audit | 审计 bundle、日志、board、report、hash、缺失文件和 unsupported claim。 |
| Advisor pack | 输出导师可读的摘要、架构图、边界和下一步计划。 |
| Community intake | 允许朋友提交 idea / skill 文档，但不直接改代码。 |

---

## 架构

<p align="center">
  <img src="assets/turingresearch_architecture_overview.svg" alt="TuringResearch Architecture" width="100%">
</p>

这个仓库坚持三件事：

- docs-first；
- evidence-first；
- contract-first。

---

## 已完成、部分完成、计划中怎么区分

| 状态 | 含义 |
|---|---|
| Implemented | 仓库里已有代码 / 文档 / 测试。 |
| Partial | 有骨架或工作流，但没到完整 production 范围。 |
| Planned | 只是路线规划。 |
| Reference | 来自外部公开项目的启发，不包装成自己的成果。 |

README 里不能把 planned 写成已经验证的科研成果。

---

## 仓库结构

```text
TuringResearch/
├─ assets/                     # 吉祥物和视觉资源
├─ community/                  # idea / skill proposal 入口
├─ docs/                       # 说明书、策略、release、路线文档
├─ examples/                   # public-safe 示例和 fake-mode demos
├─ lanes/                      # round 级别 ledger 和 decision log
├─ src/                        # Python 包
│  ├─ turing_research/
│  └─ turing_research_plus/
├─ tests/                      # contract / workflow tests
├─ README.md
└─ README_CN.md
```

改名期间可能仍保留历史包名兼容。

---

## 快速开始

```bash
git clone https://github.com/meamaturinlove221/TuringResearch_plus.git
cd TuringResearch_plus
python -m pip install -e .[dev]
python -m pytest
```

可选 MCP smoke check：

```bash
python -m tuling_research.mcp_server --manifest
```

默认工作流应当不依赖 live API key。

---

## 典型工作流

1. **论文路线规划**：从论文集合生成 method card、gap analysis 和实验想法。  
2. **长线 Codex 计划**：把路线树和硬门编译成不乱返回的 prompt。  
3. **Artifact review**：检查输出包和结论是否匹配。  
4. **导师汇报生成**：整理范围、证据、失败原因和下一步。  
5. **社区 idea intake**：允许朋友提交 idea / skill 文档，不改实现代码。  

---

## 安全边界

TuringResearch 不应该：

- 伪造 benchmark；
- 无来源地声称论文结论；
- 默认调用 live API；
- 泄露私有路径、token、`.env`、cookie 或日志；
- 分发受限数据或模型资产；
- 把参考项目的想法包装成未署名原创；
- 把 planning-only 工作流写成 production-ready。

宁可保守写 `planned`，也不要把没完成的东西包装成 `done`。

---

## 参考项目

部分公开项目给了 TuringResearch 工作流设计和文档结构上的启发。它们应该被理解为 **reference / inspiration**，不是被静默迁移的论文成果，也不是隐藏实现来源。

如果一个模块受到上游项目影响，文档里应该诚实说明。

---

## 路线图

近期方向：

- 更强的 artifact audit；
- 更好用的 evidence ledger；
- figure / table extraction 规划；
- 更完整的 advisor pack；
- 更清晰的模块化开源呈现；
- 朋友 / 社区 skill proposal 入口；
- explicit gate 后的 optional live adapters。

延后：

- ARIS-like homepage generation；
- 自动公开 release；
- 默认远程自动执行；
- 未验证的上游“学术成果”迁移。

---

## 贡献

实现型贡献请走维护者审核分支。

idea / skill proposal 可以走：

```text
community/ideas/<github-username>/<idea-title>.md
community/skills/<github-username>/<skill-name>.md
```

被接受的提案后续可以转成 feature capsule、skill、SOP、campaign 或 roadmap item。

---

## License

请以仓库中的 `LICENSE` 为准。如果本地没有 license 文件，不要默认认为项目已经正式授权再分发。

---

<p align="center">
  <b>TuringResearch 让科研迭代更清楚、更可审计、更不容易跑偏。</b>
</p>
