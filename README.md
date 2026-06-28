<!-- Profile README for https://github.com/suzike -->

<div align="center">
  <img src="./assets/profile-hero-light.svg#gh-light-mode-only" width="100%" alt="南珠 / Suzike GitHub 个人主页浅色横幅" />
  <img src="./assets/profile-hero-dark.svg#gh-dark-mode-only" width="100%" alt="南珠 / Suzike GitHub 个人主页深色横幅" />
</div>

## 定位

我目前的工作重点集中在 **汽车热管理应用层软件**、**MATLAB/Simulink MBD** 与 **AI Native 研发平台**。

我的目标是构建一套能够覆盖 PRD/SOR、SWRS、Architecture、SWDD、Simulink Model、MIL/HIL、标定、交付证据和 Knowledge Base 的研发闭环，让 LLM、Agent、MCP、Toolchain 和企业知识真正进入工程开发流程。

<div align="center">
  <img src="./assets/platform-loop-light.svg#gh-light-mode-only" width="100%" alt="AI Native 研发闭环浅色" />
  <img src="./assets/platform-loop-dark.svg#gh-dark-mode-only" width="100%" alt="AI Native 研发闭环深色" />
</div>

## 当前主线

| 方向 | 重点内容 | 交付标准 |
| --- | --- | --- |
| 汽车热管理 | 热舒适控制、热管理控制算法、智能座舱场景 | 面向量产的 SWRS、控制逻辑、Model Design、验证证据 |
| 智慧空调 Agent | 个性化控制、自学习、用户偏好建模、AI 控制算法 | Agent Demo、场景逻辑、数据流、模型策略、车端约束 |
| AI Native 研发平台 | PRD/SOR -> SWRS -> Architecture -> SWDD -> Model -> Test -> 标定 -> Knowledge Loop | 企业级 Role、Skill、Tool、MCP、Knowledge Base、SOP |
| MATLAB/Simulink Workflow | MATLAB/Simulink Engine 嵌入、Model 开发、Script、MIL/HIL、文档生成 | 工具内 Agent 交互、多模型 Context、权限模式、可复现 Automation |

## 项目控制台

| 系统 | 仓库 | 作用 |
| --- | --- | --- |
| MATLAB/Simulink AI Sidecar | [matlab-simulink-copilot](https://github.com/suzike/matlab-simulink-copilot) | 将 AI Assistant 嵌入 MATLAB/Simulink Workflow |
| MATLAB DeepSeek Copilot | [DeepSeekMatlabCopilot](https://github.com/suzike/DeepSeekMatlabCopilot) | 面向 MATLAB 工程研发的 DeepSeek Copilot 探索 |
| AI 训练平台 | [AITrain_Platform](https://github.com/suzike/AITrain_Platform) | 预测模型训练、评估和平台化流程 |
| TMS Agent Workflow | [tms-agent-workflow](https://github.com/suzike/tms-agent-workflow) | 面向 TMS、Simulink、SWDD 的多 Agent 工程任务编排 |
| AI 图形编辑 | [next-ai-draw-io](https://github.com/suzike/next-ai-draw-io) | 自然语言驱动图形创建与编辑 |
| Embedded Knowledge Base | [EmbedSummary](https://github.com/suzike/EmbedSummary) | 嵌入式工程资源与知识整理 |

## 技术栈

| Layer | Stack |
| --- | --- |
| MBD | MATLAB, Simulink, Stateflow, MIL/HIL, Model Check |
| AI / Agent | LLM Runtime, Agent, MCP, Tool, Skill, Knowledge Base |
| Software | Python, TypeScript, Next.js, GitHub Actions |
| Engineering | SWRS, Architecture, SWDD, Test Case, Calibration Evidence |

## 工程笔记

<details>
  <summary><b>AI Native 研发平台蓝图</b></summary>
  <br />

平台底座应优先采用成熟的 LLM Runtime 和 Agent 能力，在其上构建企业自己的 Role、Skill、Tool、MCP Service、Knowledge Base 和 Agent Loop Engineering（智能体的循环工程），而不是重新实现底层 Agent Engine。

核心闭环：

1. PRD / SOR 输入
2. Functional Requirement 拆解
3. SWRS 分析
4. Architecture 与 SWDD
5. Simulink Model 与 Model Check
6. MIL/HIL Test Case 生成与结果分析
7. 标定证据与发布包
8. 知识沉淀与流程改进
</details>

<details>
  <summary><b>智慧空调 Agent 方向</b></summary>
  <br />

智慧空调 Agent 方向结合热舒适控制、个性化用户偏好学习、智能座舱场景和 AI 控制算法。工程落地需要同时关注车端约束、控制稳定性、标定工作量、验证证据和量产软件边界。
</details>

## 持续关注

| 方向 | 关注内容 |
| --- | --- |
| Agent 工程 | Agent 产品化、Agent Loop Engineering（智能体的循环工程）、MCP、企业 Skill/Tool 体系 |
| 汽车 AI | 智能座舱、热舒适、智慧空调、个性化控制、自学习 |
| 工程平台 | Polarion、Harness Engineering（约束工程）、从需求到交付的研发闭环 |
| MBD 自动化 | Simulink Toolchain、MIL/HIL Automation、文档生成、Test Case 生成 |

## 联系

- GitHub: [@suzike](https://github.com/suzike)
- 微信公众号: 林南橘
- 项目讨论: 优先在对应仓库提交 Issue。
