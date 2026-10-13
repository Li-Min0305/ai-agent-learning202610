# AI Agent 独立工程师全景通关大纲与实战进度追踪表 (Master Syllabus)

> **当前状态**：第三阶段（Phase 3）进行中（已进入第 6 章）  
> **核心定位**：AI Agent / 大模型后端开发工程师（校招/暑期实习标准）  
> **使用原则**：按章节推进，每完成一个里程碑打勾 `[x]`。遇到新需求与代码迭代均以本文档为核心锚点，杜绝上下文断层。

---

## 🗺️ 全景章节结构（8 大核心通关章节）

| 阶段 | 章节 | 核心主题 | 预期交付物 | 状态 |
| :--- | :--- | :--- | :--- | :---: |
| **第一阶段：基座与协议** (10月-11月) | **第 1 章** | 现代 Python 工具链与 LLM 底层通信协议 | 第一个流式对话脚本 & API 连通性测试 | 🟢 **已完成 (2026-10-07)** |
| **第一阶段：基座与协议** (10月-11月) | **第 2 章** | Pydantic v2、结构化输出与原生 Function Calling | 原生手写 ReAct 范式命令行 Agent（零框架） | 🟢 **已完成 (2026-10-07)** |
| **第二阶段：RAG 与服务化** (12月-1月上) | **第 3 章** | 高性能异步后端与流式推送 (FastAPI + SSE) | 具备 SSE 打字机流式 API 的后端服务 | 🟢 **已完成 (2026-10-08)** |
| **第二阶段：RAG 与服务化** (12月-1月上) | **第 4 章** | 生产级 RAG 检索体系 (多路召回 + 混合重排 + 评测) | **简历项目一**：企业级文档问答 RAG 知识库系统 | 🟢 **已完成 (2026-10-09)** |
| **第三阶段：Agent 架构** (1月中-2月底) | **第 5 章** | LangGraph 状态机编排与工作流设计模式 | 支持 Plan-and-Solve 与自纠错的状态机 Agent | 🟢 **已完成 (2026-10-11)** |
| **第三阶段：Agent 架构** (1月中-2月底) | **第 6 章** | MCP (Model Context Protocol) 与工具沙箱隔离 | 基于官方 MCP 的工具服务与 Docker 执行沙箱 | 🟡 **当前进行中** |
| **第三阶段：Agent 架构** (1月中-2月底) | **第 7 章** | 综合大项目与全链路可观测性 (Langfuse 监控) | **简历项目二**：自主代码/数据分析多智能体系统 | ⚪ 待解锁 |
| **第四阶段：求职与冲刺** (3月-5月) | **第 8 章** | 简历 STAR 包装、大模型/后端高频八股与算法手撕 | 拿下大二下暑期 AI Agent / 大模型后端实习 Offer | ⚪ 待解锁 |

---

## 🔗 官方权威与高质量开源项目清单（精准导航）

在学习各章节时，必须以官方文档与以下经过验证的高质量开源仓库为标准：

1. **包管理与工具链**：
   * [Astral uv 官方文档](https://docs.astral.sh/uv/) - 全球最快的 Python 依赖管理工具。
   * [Pydantic v2 官方文档](https://docs.pydantic.dev/latest/) - 数据验证与 LLM Schema 基石。
2. **大模型核心 SDK 与教程**：
   * [OpenAI Python SDK 仓库](https://github.com/openai/openai-python) - 通用大模型调用标准。
   * [DeepSeek 官方 API 文档](https://api-docs.deepseek.com/) - 极高性价比推理与对话 API。
   * [Datawhale Hello-Agents 开源教程](https://github.com/datawhalechina/hello-agents) - 国内系统级智能体开源教程。
   * [didilili/ai-agents-from-zero](https://github.com/didilili/ai-agents-from-zero) - 结构化 AI Agent 零基础实战。
3. **框架与协议**：
   * [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/) - 循环状态机 Agent 框架。
   * [Anthropic MCP 官方协议与规范](https://modelcontextprotocol.io/) - 2025/2026 前沿上下文与工具协议。
   * [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/) - 现代异步后端开发标准。
4. **评测与可观测性**：
   * [Ragas 评估框架](https://github.com/explodinggradients/ragas) - RAG 量化评估金标准。
   * [Langfuse 开源 LLM 监控平台](https://github.com/langfuse/langfuse) - 全链路追踪与成本分析。

---

## 📌 当前推进记录

* **[2026-10-07]** 初始化大纲，完成第 1 章（底层流式通信）与第 2 章（Pydantic 原生工具调用）。
* **[2026-10-08]** 完成第 3 章（FastAPI + SSE 异步打字机流式 Web 服务端与前端对接）。
* **[2026-10-09]** 完成第 4 章（ChromaDB 向量检索、分块与防幻觉 RAG 知识库系统）。
* **[2026-10-11]** 完成第 5 章（LangGraph 状态机编排与自纠错自愈代码智能体）。
* **[当前状态]** 解锁进入第 6 章（MCP 协议与工具沙箱隔离）。
