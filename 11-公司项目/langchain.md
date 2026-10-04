# LangChain 面试题

### 一、LangChain 概述与生态

#### Q1【八股】【LangChain 概述】【L1】LangChain 的定位与核心价值

**题目**：为什么需要 LangChain？它在 LLM 应用架构中扮演什么角色？

**思考方向**：从单一 LLM 的局限性切入，再讲 LangChain 作为中间层解决了什么问题。

**考察点**：LangChain 定位、LLM 应用场景认知。

**参考答案**：

- 单一 LLM 局限：无法直接连接外部工具/数据源/记忆机制，无法构建智能体系统。

- LangChain 定位：大模型与应用的**中间层**，统一接口对接数据库/检索引擎/API/文件系统，封装底层复杂逻辑，支撑多智能体协作。

- 六大应用场景：RAG 开发、Agent 智能体构建、对话系统、多模态应用、自动化写作、数据连接与结构化处理。

**评分要点**：

- 优秀：能讲清中间层抽象的价值（屏蔽模型差异、统一接口、模块化）、能列举至少 3 个应用场景。

- 及格：能说出 LangChain 是大模型与应用之间的中间层，能说出 2 个场景。

- 不足：只说"帮开发者用大模型"。

**常见追问**：1) LangChain 和直接调 OpenAI API 有什么本质区别？2) 哪些场景不适合用 LangChain？

---

#### Q2【八股】【LangChain 概述】【L1】LangChain 家族四大支柱

**题目**：LangChain 生态包含哪四大核心组件？各自承担什么职责？

**思考方向**：从"能力抽象 → 执行编排 → 高级智能 → 监控调试"四个层次理解。

**考察点**：LangChain 生态全景认知。

**参考答案**：

1. **LangChain**：智能体开发基石，统一模型抽象层（屏蔽 OpenAI/Anthropic/Ollama 差异），高度模块化设计。

2. **LangGraph**：复杂工作流编排引擎，核心是有向图（Node 节点、Edge 边、State 状态），负责执行与编排。

3. **Deep Agent**：智能体执行框架（Agent Harness），构建于 LangChain + LangGraph 之上，提供显式规划、虚拟文件系统、子智能体、长期记忆、可扩展中间件。

4. **LangSmith**：可视化监控与测试平台，提供全链路追踪、调试优化、评测质控、团队协作。

**评分要点**：

- 优秀：能讲清四者的层次关系（LangChain=能力层，LangGraph=编排层，Deep Agent=高级执行框架，LangSmith=监控层）。

- 及格：能说出四大组件名称及各自一句话职责。

- 不足：只说"LangChain 是框架，LangSmith 是工具"。

**常见追问**：1) LangGraph 和 LangChain 是什么关系？2) Deep Agent 相比普通 Agent 有什么提升？

---

#### Q3【八股】【LangChain 概述】【L1】大模型应用开发的四个场景

**题目**：大模型应用开发有哪四个层次？它们的成本和适用场景有何差异？

**思考方向**：从简单到复杂、从低成本到高成本递进理解。

**考察点**：LLM 应用开发全景、技术选型认知。

**参考答案**：

1. **纯 Prompt**：最简单，直接给模型提示词，适合原型验证和简单任务。

2. **Agent + Function Calling**：让模型调用外部工具，适合需要与外部系统交互的场景。

3. **RAG（检索增强生成）**：接入外部知识库，适合知识密集型问答、客服系统。

4. **Fine-tuning（微调）**：成本最高，修改模型权重，适合定制化风格/领域能力。

**评分要点**：

- 优秀：能讲清四个层次的成本递增关系、各自适用场景的边界、什么时候选 RAG 什么时候选微调。

- 及格：能说出四个层次名称及基本场景。

- 不足：只说"可以用 RAG 或微调"。

**常见追问**：1) RAG 和微调什么时候该选哪个？2) 如果要给模型注入企业内部知识，首选哪个方案？

---

#### Q4【八股】【LangChain 概述】【L2】LangChain v0.3 与 v1.2 的核心差异

**题目**：LangChain v0.3 和 v1.2 有什么本质区别？为什么要升级到 v1.2？

**思考方向**：从"链式调用范式"到"智能体框架范式"的转变切入。

**考察点**：LangChain 版本演进、架构范式理解。

**参考答案**：

- v0.3：过渡性版本，核心是链式调用（Chain），API 设计碎片化。

- v1.2：生产级稳定版本，智能体框架范式转变。承诺 2.0 前无破坏性变更，1.2 亿美元融资，估值超 12 亿美元。

- v1.2 主要模块变化：

    - `langchain-core`：官方推荐核心 API（Runnable, BaseMessage 等）。

    - `langchain-classic`：0.x 遗留冗余代码，不推荐。

    - `langchain-community`：第三方集成（langchain-openai, langchain-anthropic 等）。

    - `langgraph`：深度整合 LangGraph 1.0。

**评分要点**：

- 优秀：能讲清从"链式调用"到"Agent 优先"的范式转变、模块拆分的意义（core/classic/community 分层）、对生产稳定性的承诺。

- 及格：能说出 v1.2 是生产级版本、模块拆分的基本结构。

- 不足：只知道"版本升级了"。

**常见追问**：1) langchain-core 和 langchain-classic 的区别对开发者有什么实际影响？2) v1.2 中 Agent 的创建方式发生了什么变化？

---

#### Q5【八股】【LangChain 概述】【L3】Agent 公式与组件层级

**题目**：Agent = LLM + Planning + Tools + Memory + Action，请解释每个组件的必要性层级和在 v1.2 中的体现。

**思考方向**：从"必须"到"可选"的递减层级分析，结合 v1.2 create\_agent 的参数设计。

**考察点**：Agent 架构理解、组件依赖关系、版本特性。

**参考答案**：

- **Action（行动）**：必须存在，是 Agent 的基本执行能力，对应 `create_agent` 的核心调用机制。

- **Tools（工具）**：几乎总是存在，对应 `tools` 参数，赋予 Agent 与外部世界交互能力。

- **Planning（规划决策）**：有条件存在，简单任务不需要显式规划，复杂任务通过 ReAct 循环或中间件（To-do list）实现。

- **Memory（记忆）**：最容易被省略，对应 `checkpointer` 参数，需要显式配置才有短期记忆。

- 短期记忆受限于上下文窗口（GPT-5.5 Pro 支持 100 万 Token，Claude Opus 4.7 支持 200 万 Token），长期记忆可通过模型微调/知识图谱/向量数据库实现。

**评分要点**：

- 优秀：能讲清组件的必要性递减关系、在 v1.2 API 中的对应参数、短期/长期记忆的边界与实现方式。

- 及格：能说出公式各组件含义及基本层级关系。

- 不足：只列出公式不知各组件深度。

**常见追问**：1) 在什么场景下 Memory 可以省略？2) Planning 在 v1.2 中如何通过中间件实现？

---

### 二、模型创建与调用

#### Q6【八股】【模型调用】【L1】Model I/O 流程

**题目**：LangChain 中 Model I/O 的完整流程是什么？三个阶段分别做什么？

**思考方向**：从输入到输出的流水线角度理解。

**考察点**：Model I/O 核心概念。

**参考答案**：

1. **Format（格式化）**：通过 PromptTemplate 将用户输入格式化为模型可接受的输入。

2. **Predict（预测）**：将格式化后的输入传给 Model，模型返回响应。

3. **Parse（解析）**：通过 Output Parser 将模型响应解析为程序可消费的结构化数据。

**评分要点**：

- 优秀：能讲清三阶段在代码中的对应（ChatPromptTemplate → ChatModel → Output Parser）、与 LangChain 1.x 组件的映射。

- 及格：能说出三阶段名称和基本职责。

- 不足：只说"调用模型"。

**常见追问**：1) Format 阶段在 v1.2 中推荐用什么组件？2) Parse 阶段除了 Output Parser 还有什么方式？

---

#### Q7【八股】【模型调用】【L2】模型初始化的三种方式

**题目**：LangChain 1.x 中初始化聊天模型有哪几种方式？各有什么优劣？

**思考方向**：从"调用谁家 API""参数位置""模型位置"三个维度对比。

**考察点**：模型初始化、Provider 适配、init\_chat\_model 统一接口。

**参考答案**：

1. **使用模型提供商库**：如 `ChatDeepSeek`、`ChatZhipuAI`、`ChatTongyi`，直接使用专用 SDK，灵活但需记不同类名。

2. **init\_chat\_model() 统一接口**（推荐）：LangChain 1.x 统一入口，根据 model 名自动选择对应类。支持 `model_provider` 前缀指定供应商（如 `"deepseek:deepseek-v4-flash"`）。支持 20+ providers。

3. **本地模型部署（Ollama）**：通过 `ChatOllama` 或 `init_chat_model(model="ollama:deepseek-r1:1.5b")` 调用本地部署的模型。

- 大多数平台支持 OpenAI API 规范，可通过 `ChatOpenAI` 统一调用 DeepSeek/智谱/千问等。

**评分要点**：

- 优秀：能讲清三种方式的适用场景、init\_chat\_model 的 provider 路由机制、OpenAI 兼容协议的便利性。

- 及格：能说出三种方式名称和基本用法。

- 不足：只知道一种初始化方式。

**常见追问**：1) init\_chat\_model 是怎么根据模型名路由到对应类的？2) 千问大模型为什么不能用 OpenAI 兼容 URL 调用？

---

#### Q8【八股】【模型调用】【L1】Token 概念与 temperature 参数

**题目**：什么是 Token？temperature 参数如何影响模型输出？不同 temperature 适合什么场景？

**思考方向**：从分词机制和采样温度两个维度回答。

**考察点**：Token 机制、temperature 调参。

**参考答案**：

- **Token**：文本拆分后的最小语义单元，不同模型分词算法不同。1 个中文 Token ≈ 1-1.8 个汉字，1 个英文 Token ≈ 3-4 个字符。Token 是模型计费依据。

- **temperature**：控制输出随机性，范围 0.0-2.0，默认 0.7。

    - 0.0-0.3：一致性任务（代码生成、数据提取、结构化输出）。

    - 0.5-0.7：平衡场景（通用对话、问答）。

    - 0.8-1.5：创造性场景（创意写作、头脑风暴）。

    - 1.5-2.0：高度创造性（实验性用途）。

**评分要点**：

- 优秀：能讲清 Token 与字符的区别、temperature 底层原理（logits/softmax 温度缩放）、各场景的选值依据。

- 及格：能说出 Token 定义和 temperature 的基本范围与场景对应。

- 不足：只知道 temperature 控制随机性。

**常见追问**：1) 为什么 temperature=0 也不一定每次输出完全一样？2) Token 数和字符数的关系对成本估算有什么影响？

---

#### Q9【八股】【模型调用】【L2】invoke() 的三种输入形式与返回值

**题目**：model.invoke() 支持哪三种输入形式？返回的 AIMessage 对象包含哪些关键字段？

**思考方向**：从最简单到最规范递进，再分析返回值结构。

**考察点**：模型调用接口、消息类型、AIMessage 结构。

**参考答案**：
三种输入形式：

1. **文本输入**：最简单，`model.invoke("你好")`，无法设置 system prompt。

2. **字典列表（推荐）**：`[{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]`。

3. **消息对象列表**：`[SystemMessage(...), HumanMessage(...)]`。

AIMessage 返回值关键字段：

- `content`：最终文本答案。

- `additional_kwargs`：如 refusal（拒绝回答信息）。

- `response_metadata`：token\_usage、latency\_checkpoint、model\_provider 等。

- `tool_calls`：工具调用信息列表（name、args、id、type）。

- `usage_metadata`：input\_tokens、output\_tokens、total\_tokens 等用量信息。

**评分要点**：

- 优秀：能讲清三种形式的优劣对比、tool\_calls 的结构及在 Agent 中的作用、usage\_metadata 用于成本监控。

- 及格：能说出三种输入形式和 AIMessage 的关键字段。

- 不足：只知道文本输入方式。

**常见追问**：1) tool\_calls 在什么情况下会非空？2) 如何从 response\_metadata 获取延迟信息？

---

#### Q10【八股】【模型调用】【L2】模型调用方式对比：invoke / stream / batch

**题目**：LangChain 提供了哪些模型调用方式？各自适用什么场景？

**思考方向**：从同步/异步、单次/批量、阻塞/流式三个维度对比。

**考察点**：调用接口全貌、异步编程、流式输出。

**参考答案**：

| 方法 | 特性 | 适用场景 |
| --- | --- | --- |
| `invoke()` | 阻塞式，一次性返回完整结果 | 简单场景、调试 |
| `ainvoke()` | 非阻塞式，异步 | 高并发场景 |
| `stream()` | 流式输出，实时返回每个 token | 打字机效果、前端实时展示 |
| `astream()` | 非阻塞式流式 | 高并发流式场景 |
| `batch()` | 批量处理多个输入 | 批量推理、数据处理 |
| `abatch()` | 非阻塞式批量 | 高并发批量 |

- config 参数可控制 `max_concurrency`（最大并发数）和 `recursion_limit`（递归深度限制）。

- `configurable` 参数可动态替换模型、temperature 等。

**评分要点**：

- 优秀：能讲清同步/异步的底层差异、stream 的 token 级推送机制、batch + max\_concurrency 的并发控制。

- 及格：能说出 6 种方法名称和基本场景。

- 不足：只知道 invoke。

**常见追问**：1) stream() 返回的是什么类型？如何遍历？2) batch() 如何控制并发数？

---

#### Q11【八股】【模型调用】【L3】config 参数与运行时动态配置

**题目**：invoke() 的 config 参数有哪些？如何实现运行时动态切换模型？

**思考方向**：从初始化参数 vs 运行时参数的优先级、configurable 机制切入。

**考察点**：config 参数体系、动态配置、并发控制。

**参考答案**：
config 关键参数：

- `run_name`：运行名称（LangSmith 追踪用）。

- `tags`：标签（分类查找）。

- `callbacks`：回调处理器。

- `metadata`：元数据（user\_id, session\_id）。

- `max_concurrency`：最大并发数。

- `recursion_limit`：递归深度限制。

- `configurable`：可配置参数字典，可动态替换模型、temperature 等。

运行时动态切换：

```python
config = {"configurable": {"model": "deepseek-v4-pro"}}
response = model.invoke(input, config=config)
```

- 运行时 config 优先级高于初始化默认参数。

- 需要 `configurable_fields` 参数指定可替换参数。

**评分要点**：

- 优秀：能讲清 config 优先级机制、configurable\_fields 的声明方式、max\_concurrency 与 recursion\_limit 在 Agent 场景的应用。

- 及格：能说出 config 的主要参数和 configurable 的基本用法。

- 不足：只知道 config 可以传参。

**常见追问**：1) configurable 切换模型的底层机制是什么？2) recursion\_limit 在 Agent 中为什么重要？

---

### 三、LangSmith

#### Q12【八股】【LangSmith】【L1】LangSmith 核心功能

**题目**：LangSmith 有哪些核心功能？它在 LLM 应用开发中解决什么问题？

**思考方向**：从"开发-调试-监控-评估"全生命周期理解。

**考察点**：LangSmith 功能全景、LLM 应用可观测性。

**参考答案**：
LangSmith 是 LangChain 生态中专门用于 LLM 应用调试、监控、评估和管理的平台。

三组核心功能：

1. **核心应用与开发**：Tracing（追踪每次 LLM 调用链路）、Monitoring（生产环境可视化看板）、Datasets & Experiments（数据集与实验）、Evaluators（规则/LLM-as-a-judge 评估）、Annotation Queues（人工反馈与数据清洗）。

2. **提示词与调试工具**：Prompts（版本控制）、Playground（Prompt 测试）、Studio（LangGraph 可视化状态机）、Context Hub（全局上下文管理）。

3. **部署与沙盒**：Deployments（一键部署 API）、Sandboxes（在线测试环境）。

**评分要点**：

- 优秀：能讲清 Tracing 的全链路追踪机制、Evaluators 的两种模式（规则 vs LLM-as-a-judge）、与 LangGraph Studio 的集成。

- 及格：能说出三组功能名称和基本用途。

- 不足：只说"LangSmith 是监控工具"。

**常见追问**：1) Tracing 能追踪到什么粒度？2) LLM-as-a-judge 评估怎么实现？

---

#### Q13【八股】【LangSmith】【L2】LangSmith 环境配置与自动追踪

**题目**：如何配置 LangSmith 的自动追踪？追踪的粒度是什么？

**思考方向**：从环境变量配置到自动记录机制的链路。

**考察点**：LangSmith 集成方式、Tracing 机制。

**参考答案**：
环境变量配置：

```text
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=<YOUR_API_KEY>
LANGSMITH_PROJECT="pr-clear-harmony-32"
```

- 添加环境变量后运行 LangChain 代码，LangSmith 自动记录，无需修改业务代码。

- 追踪粒度：完整记录每次 LLM 调用链路，查看 Prompt、返回、Token 消耗、节点耗时。

- 监控指标：Token 消耗趋势、QPS、错误率、延迟、成本预估。

**评分要点**：

- 优秀：能讲清零侵入追踪的底层原理（callbacks 机制）、多项目隔离（LANGSMITH\_PROJECT）、与 LangGraph 节点级追踪的关系。

- 及格：能说出 4 个环境变量和自动追踪机制。

- 不足：只知道需要配置 API Key。

**常见追问**：1) 不加 LANGSMITH\_TRACING=true 会怎样？2) 如何在多项目间切换追踪？

---

#### Q14【八股】【LangSmith】【L3】LangSmith 评估体系设计

**题目**：如果你要为一个 RAG 系统设计 LangSmith 评估方案，你会怎么设计？用到哪些功能？

**思考方向**：从"评测集构建 → 评估器配置 → 对比实验 → 持续优化"闭环设计。

**考察点**：评估体系设计、Evaluators、Datasets & Experiments。

**参考答案**：

1. **评测集构建**：用 Datasets 管理测试数据集，包含 question-expected\_answer 对。

2. **评估器配置**：

    - 规则评估：检查答案是否包含关键词/格式是否正确。

    - LLM-as-a-judge：用更强模型评判答案质量、忠实度、相关性。

3. **对比实验**：用 Experiments 运行不同 Prompt/模型/参数，自动打分对比。

4. **人工反馈**：用 Annotation Queues 收集人工标注，清洗数据。

5. **持续优化**：通过 Monitoring 看板追踪线上效果，Badcase 回流到评测集。

**评分要点**：

- 优秀：能设计完整评估闭环（评测集→评估器→对比→优化）、能区分规则评估与 LLM-as-a-judge 的适用场景、能讲清 Badcase 闭环。

- 及格：能说出评估的基本流程和 2-3 个功能点。

- 不足：只说"用 LangSmith 测试"。

**常见追问**：1) LLM-as-a-judge 的评估 prompt 怎么写？2) 如何避免评估中的数据泄漏？

---

### 四、Message 与提示词模板

#### Q15【八股】【Message】【L1】四种消息类型

**题目**：LangChain 中有哪四种消息类型？各自的作用是什么？

**思考方向**：从角色分工（系统/用户/AI/工具）理解。

**考察点**：消息类型体系、角色定义。

**参考答案**：

| 角色 | JSON 格式 | 对象格式 | 用途 |
| --- | --- | --- | --- |
| System | `{"role": "system", ...}` | `SystemMessage(...)` | 设定 AI 行为、角色、规则 |
| User | `{"role": "user", ...}` | `HumanMessage(...)` | 用户输入 |
| Assistant | `{"role": "assistant", ...}` | `AIMessage(...)` | AI 回复 |
| Tool | `{"role": "tool", ...}` | `ToolMessage(...)` | 工具执行结果 |

- 大模型 API 是"无状态"的，需要程序维护消息列表。

- 每次调用必须传递完整对话历史。

**评分要点**：

- 优秀：能讲清 AIMessage 的 tool\_calls 字段与 ToolMessage 的 tool\_call\_id 的关联关系、无状态设计的影响。

- 及格：能说出四种消息类型和基本用途。

- 不足：只知道 user 和 assistant。

**常见追问**：1) ToolMessage 的 tool\_call\_id 有什么作用？2) 为什么大模型 API 要设计成无状态？

---

#### Q16【八股】【Message】【L1】ChatPromptTemplate 的使用

**题目**：ChatPromptTemplate 的 from\_messages() 方法支持哪些参数类型？如何创建一个带变量的提示词模板？

**思考方向**：从参数类型的多样性理解模板的灵活性。

**考察点**：ChatPromptTemplate、模板参数类型。

**参考答案**：
from\_messages() 支持 6 种参数类型：

1. **str 列表**：默认角色为 human。

2. **tuple 列表**（推荐）：`[("system", "..."), ("human", "...")]`。

3. **dict 列表**：`[{"role": "system", "content": "..."}]`。

4. **Message 列表**：Message 中不能有占位符。

5. **MessagePromptTemplate 列表**。

6. **BaseChatPromptTemplate 列表**：支持嵌套。

创建带变量的模板：

```python
from langchain_core.prompts import ChatPromptTemplate
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，服务于{audience}。"),
    ("human", "{question}")
])
result = template.invoke({"role": "客服专员", "audience": "普通用户", "question": "你好"})
```

三种调用方式：`invoke()`（返回 ChatPromptValue）、`format()`（返回字符串）、`format_messages()`（返回消息列表）。

**评分要点**：

- 优秀：能讲清 6 种参数类型的差异与约束、invoke/format/format\_messages 的返回值区别、与 PromptTemplate 旧版的对比。

- 及格：能说出 from\_messages 的基本用法和变量填充。

- 不足：只知道字符串模板。

**常见追问**：1) Message 列表为什么不能有占位符？2) ChatPromptValue 是什么类型？

---

#### Q17【八股】【Message】【L2】对话历史管理与常见陷阱

**题目**：在多轮对话中管理消息历史有哪些常见错误？正确做法是什么？

**思考方向**：从"无状态 API"的特性出发，分析历史丢失的根因。

**考察点**：对话历史管理、无状态机制、消息追加。

**参考答案**：
常见错误：

1. **重新创建新列表**：每次调用都创建新的 messages 列表，丢失历史。

2. **忘记保存 AI 回复**：只追加了 HumanMessage，没有 append AIMessage。

3. **不传递完整历史**：只传最新消息，不传之前的历史。

正确做法：

```python
conversation = [
    {"role": "system", "content": "你是助手"},
    {"role": "human", "content": "你好"}
]
response = model.invoke(conversation)
conversation.append({"role": "assistant", "content": response.content})  # 保存AI回复
conversation.append({"role": "human", "content": "下一个问题"})
```

优化策略：保留 system 消息 + 最近 N 轮对话，避免上下文过长。

**评分要点**：

- 优秀：能讲清无状态 API 的本质、AI 回复保存的重要性、截断策略（保留 system + 最近 N 轮）的设计思路。

- 及格：能说出至少 2 个常见错误和正确做法。

- 不足：不知道历史会丢失。

**常见追问**：1) 上下文过长怎么截断？截断后丢失关键信息怎么办？2) 如何实现 keep\_recent\_messages()？

---

#### Q18【八股】【Message】【L2】partial() 与 MessagesPlaceholder

**题目**：ChatPromptTemplate 的 partial() 和 MessagesPlaceholder 各解决什么问题？给出使用场景。

**思考方向**：从"变量预填充"和"动态消息列表插入"两个不同需求理解。

**考察点**：模板高级特性、部分填充、消息占位符。

**参考答案**：
**partial()**：部分变量预填充，创建模板变体。

```python
template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，服务于{audience}。"),
    ("human", "{question}")
])
# 预填充部分变量
customer_service = template.partial(role="客服专员", audience="普通用户")
# 调用时只需传 question
result = customer_service.invoke({"question": "退货流程"})
```

适用场景：为不同部门/角色创建专用模板，减少重复传参。

**MessagesPlaceholder**：动态插入消息列表。

```python
template = ChatPromptTemplate.from_messages([
    ("system", "你是助手"),
    ("placeholder", "{conversation}"),  # 或 MessagesPlaceholder("conversation")
    ("human", "{question}")
])
result = template.invoke({
    "conversation": [HumanMessage("之前的问题"), AIMessage("之前的回答")],
    "question": "新问题"
})
```

适用场景：多轮对话系统存储历史消息、Agent 中间步骤处理。

**评分要点**：

- 优秀：能讲清 partial 的变体创建思想、MessagesPlaceholder 在 Agent 中间步骤中的应用、两者组合使用的场景。

- 及格：能说出两者的基本用法和各自适用场景。

- 不足：只知道变量填充。

**常见追问**：1) partial 后还能修改已填充的变量吗？2) MessagesPlaceholder 在 Agent 中如何接收中间步骤消息？

---

#### Q19【八股】【Message】【L3】content 与 content\_blocks

**题目**：LangChain 1.x 中消息的 content 和 content\_blocks 有什么区别？为什么要引入 content\_blocks？

**思考方向**：从多模态数据标准化的需求理解。

**考察点**：多模态消息结构、跨模型标准化。

**参考答案**：

- **content**：弱类型，支持字符串和列表（多模态），但不同供应商格式不统一。

- **content\_blocks**：LangChain 1.x 重大升级，跨模型供应商标准化多模态数据结构。

    - 类型：text、image、audio、video、tool\_call、reasoning。

    - 支持懒加载。

    - 建议优先检查 `response.content_blocks` 而非 `response.content`，特别是获取思维链或引用信息时。

```python
# 多模态消息
HumanMessage(content_blocks=[
    {'type': 'text', 'text': '这张图片是什么？'},
    {'type': 'image', 'base64': '...', 'mime_type': 'image/png'}
])
```

**评分要点**：

- 优秀：能讲清 content\_blocks 的跨供应商标准化设计、懒加载机制、获取思维链（reasoning 类型）的场景、与 content 的优先使用建议。

- 及格：能说出 content\_blocks 的存在和基本类型。

- 不足：只知道 content。

**常见追问**：1) 如何从 content\_blocks 中提取思维链？2) 不同模型的图片格式差异在 content\_blocks 中如何统一？

---

### 五、Tools 工具

#### Q20【八股】【Tools】【L1】工具的定义与 @tool 装饰器

**题目**：LangChain 中如何定义一个工具？@tool 装饰器的工作原理是什么？

**思考方向**：从函数到工具的自动转换机制理解。

**考察点**：工具定义、@tool 装饰器、docstring 解析。

**参考答案**：
两种定义方式：

1. **不使用 @tool**：普通函数 + bind\_tools，函数签名和 docstring 会被解析为 tool\_schema。

2. **使用 @tool 装饰器**（推荐）：

```python
from langchain_core.tools import tool

@tool(parse_docstring=True)
def get_weather(city: str) -> str:
    """
    获取指定城市的天气信息
    Args:
        city: 城市名称，如"北京"、"上海"
    Returns:
        天气信息字符串
    """
    return f"{city}晴天，温度 15°C"
```

- @tool 从 docstring 自动生成工具描述。

- `parse_docstring=True`：将 docstring 解析并填充到各字段描述。

- `description` 参数可覆盖 docstring，优先级更高。

- `name_or_callable` 参数可自定义工具名称。

- docstring 采用 Google 风格（`Args:`、`Returns:`、`Raises:`）。

**评分要点**：

- 优秀：能讲清 @tool 的 docstring → JSON Schema 转换机制、parse\_docstring 的作用、description 覆盖优先级、与不使用 @tool 的差异。

- 及格：能写出 @tool 的基本用法和 docstring 规范。

- 不足：只知道函数能当工具用。

**常见追问**：1) 如果 docstring 写得不好会怎样？2) 能否给一个工具自定义 name？

---

#### Q21【八股】【Tools】【L1】工具调用的完整四步骤

**题目**：工具绑定到模型后的完整调用流程是什么？四个步骤分别做什么？

**思考方向**：从"绑定→请求→执行→回传"的闭环理解。

**考察点**：工具调用流程、bind\_tools、ToolMessage。

**参考答案**：

1. **模型绑定工具**：`model_with_tools = model.bind_tools([tool1, tool2])`

2. **模型生成工具调用请求**：`response = model_with_tools.invoke("北京天气如何？")`，response.tool\_calls 包含工具名和参数。

3. **开发者手动执行工具**：`tool_result = get_weather.invoke(response.tool_calls[0])`，返回 ToolMessage。

4. **将工具执行结果传递给模型**：将 ToolMessage 追加到消息列表，再次调用模型生成最终结果。

```python
message_list = [{"role": "user", "content": "北京天气如何？"}]
response = model_with_tools.invoke(message_list)
message_list.append(response)
if response.tool_calls:
    for tc in response.tool_calls:
        result = get_weather.invoke(tc)
        message_list.append(result)
final = model_with_tools.invoke(message_list)
```

**评分要点**：

- 优秀：能讲清 tool\_calls 的结构（name/args/id/type）、ToolMessage 与 tool\_call\_id 的关联、多工具并发调用的循环处理。

- 及格：能说出四步骤的基本流程。

- 不足：只知道"模型调用工具"。

**常见追问**：1) 如果模型一次返回多个 tool\_calls 怎么处理？2) 工具执行失败怎么处理？

---

#### Q22【八股】【Tools】【L2】args\_schema 三种定义方式

**题目**：工具的 args\_schema 有哪三种定义方式？各自的特点是什么？

**思考方向**：从类型安全性和使用便利性对比。

**考察点**：工具参数 Schema、Pydantic、JSON Schema。

**参考答案**：

1. **Pydantic 模型**（推荐）：

```python
from pydantic import BaseModel, Field
class WeatherInput(BaseModel):
    city: str = Field(description="城市名称")
    is_forecast: bool = Field(default=False, description="是否包含预报")
```

支持 Literal 枚举、类型校验、运行时强校验。

2. **JSON Schema 字典**：直接传递符合 JSON Schema 标准的字典。

3. **工具函数签名**：通过函数参数类型注解自动推断。

- convert\_to\_openai\_tool 生成的 Schema 包含：`type`（数据类型）、`properties`（属性及类型）、`required`（必填字段）。

**评分要点**：

- 优秀：能讲清三种方式的校验强度差异（Pydantic 有运行时校验）、Field 的 description 如何影响模型选择工具的准确性、Literal 枚举的应用。

- 及格：能说出三种方式名称和 Pydantic 的基本用法。

- 不足：只知道函数参数类型注解。

**常见追问**：1) Field 的 description 对工具有什么影响？2) 如何让工具参数支持枚举值？

---

#### Q23【八股】【Tools】【L2】tool\_choice 参数

**题目**：tool\_choice 参数有哪几个取值？各自如何控制模型的行为？

**思考方向**：从"不调用→自动决定→强制调用→指定调用"的递进理解。

**考察点**：工具调用控制、tool\_choice。

**参考答案**：

- `none`：模型不会调用任何工具，只生成文本回复。

- `auto`（默认值）：模型自主决定是否调用工具。

- `required` / `any`：模型必须调用工具，数量不限。

- 指定工具名：如 `tool_choice="get_weather"`，强制调用特定工具。

**评分要点**：

- 优秀：能讲清各取值的适用场景（none 用于纯对话、auto 用于智能路由、required 用于必须执行外部操作的场景）、与 Agent 中间件的 interrupt\_before 的关系。

- 及格：能说出 4 种取值和基本行为。

- 不足：只知道有这个参数。

**常见追问**：1) 什么场景下应该用 required？2) tool\_choice 和 Agent 的 system\_prompt 中"必须使用工具"的指令有什么区别？

---

#### Q24【八股】【Tools】【L3】工具设计最佳实践

**题目**：设计 Agent 工具时有哪些最佳实践？工具失败的三层防护是什么？

**思考方向**：从工具描述规范、功能粒度、错误处理三个维度回答。

**考察点**：工具工程化、错误处理、实践经验。

**参考答案**：
最佳实践：

1. **清晰描述**：使用 Google 风格 docstring，description 越清晰模型选择越准确。

2. **功能单一**：每个工具只做一件事，避免多功能混合。

3. **工具返回字符串**：不要返回字典，模型更容易理解字符串。

4. **同步 vs 异步选择**：IO 密集型用异步工具。

工具失败三层防护：

1. **工具内部处理**：try-except 在工具函数内部捕获异常，返回友好错误信息。

2. **Agent 级重试**：通过 system\_prompt 引导 Agent 自主重试。

3. **调用级重试**：使用 @retry 装饰器或中间件（Tool retry）实现自动重试。

**评分要点**：

- 优秀：能讲清三层防护的分工、为什么返回字符串而非字典、工具数量建议（2-5 个最佳）、与中间件 Tool retry 的配合。

- 及格：能说出 2-3 个最佳实践和三层防护的基本概念。

- 不足：只知道工具需要写 docstring。

**常见追问**：1) 工具太多（如 20+）时怎么处理？2) Agent 级重试的 system\_prompt 怎么写？

---

### 六、结构化输出

#### Q25【八股】【结构化输出】【L1】结构化输出的概念与价值

**题目**：什么是结构化输出？相比传统方式有什么优势？

**思考方向**：从"自然语言→程序可消费数据"的转变理解。

**考察点**：结构化输出概念、with\_structured\_output。

**参考答案**：

- 结构化输出：要求模型返回符合预定义结构的数据对象（固定字段 JSON、Pydantic 模型、TypedDict），而非无格式自然语言文本。

- 核心目标：把"自然语言回答"变成"程序可以稳定消费的数据"。

传统方式 vs 结构化输出：

- 传统：提示词要求 JSON → json.loads() → 手动验证类型 → 手动创建对象。

- 结构化输出：`model.with_structured_output(Person)` 一步到位。

```python
structured_llm = model.with_structured_output(Person)
result = structured_llm.invoke("张三是一名 30 岁的软件工程师")
# result: Person(name='张三', age=30, occupation='软件工程师')
```

**评分要点**：

- 优秀：能讲清传统方式的痛点（JSON 格式不保证、类型不校验、多步处理）、with\_structured\_output 的底层流程（Pydantic → JSON Schema → Grammar-based sampling → 自动解析）。

- 及格：能说出结构化输出的定义和基本用法。

- 不足：只知道"让模型返回 JSON"。

**常见追问**：1) with\_structured\_output 底层是怎么约束模型输出的？2) 如果模型返回的 JSON 格式不对会怎样？

---

#### Q26【八股】【结构化输出】【L2】四种 Schema 模式对比

**题目**：结构化输出有哪四种 Schema 模式？各自的校验强度和返回值有什么区别？

**思考方向**：从类型安全和便利性对比四种模式。

**考察点**：Pydantic / TypedDict / JSON Schema / @dataclass。

**参考答案**：

| 模式 | 返回值 | 运行时校验 | 特点 |
| --- | --- | --- | --- |
| Pydantic（首选） | Pydantic 实例 | 强校验（抛 ValidationError） | 类型提示、Field 描述、枚举、嵌套 |
| TypedDict | 字典 | 不校验 | 轻量，Python 3.8+，Annotated 语法 |
| JSON Schema | 字典 | 不校验 | 直接拼 JSON Schema 字典，method="json\_schema" |
| @dataclass | 字典 | 不校验 | Python 标准库，Field 提供描述 |

- Pydantic 高级特性：Optional 可选字段、默认值、Enum/Literal 枚举、List 嵌套、限制条件（min\_length/max\_length/ge/le）。

- 嵌套建议 ≤ 3 层。

**评分要点**：

- 优秀：能讲清 Pydantic 强校验的价值（ValidationError 捕获）、TypedDict 的 Annotated 语法、嵌套层级限制的工程考量、四种模式在生产 vs 原型中的选型。

- 及格：能说出四种模式名称和 Pydantic 的基本特性。

- 不足：只知道 Pydantic。

**常见追问**：1) Pydantic 校验失败时抛什么异常？如何捕获？2) TypedDict 为什么不做运行时校验？

---

#### Q27【八股】【结构化输出】【L2】with\_structured\_output vs 输出解析器

**题目**：with\_structured\_output 和 JsonOutputParser 有什么区别？为什么推荐前者？

**思考方向**：从"一步到位"vs"链式调用"的复杂度对比。

**考察点**：结构化输出获取方式、Output Parser。

**参考答案**：

- **with\_structured\_output**（最新、最简洁）：

    - `model.with_structured_output(Person).invoke("...")`

    - 一步到位，直接返回 Pydantic 对象。

    - `include_raw=True` 可返回原始 AIMessage，包含 `raw`、`parsed`、`parsing_error` 三个字段。

- **输出解析器**（不推荐）：

    - `JsonOutputParser` + `ChatPromptTemplate` 链式调用。

    - 需要手动拼接 prompt、解析输出、处理异常。

    - 代码量大、易出错。

**评分要点**：

- 优秀：能讲清 include\_raw 的三个字段及使用场景（解析失败时回退到 raw）、with\_structured\_output 的底层 Grammar-based sampling 机制、为什么输出解析器被标记为不推荐。

- 及格：能说出两种方式的基本区别和推荐选择。

- 不足：只知道一种方式。

**常见追问**：1) include\_raw=True 在什么场景下有用？2) parsing\_error 什么时候会非空？

---

#### Q28【八股】【结构化输出】【L3】Agent 结构化输出策略

**题目**：Agent 的结构化输出有哪四种策略？ToolStrategy 和 ProviderStrategy 有什么本质区别？

**思考方向**：从"解析时机"和"实现机制"两个维度对比。

**考察点**：Agent 结构化输出、ProviderStrategy / ToolStrategy / AutoStrategy。

**参考答案**：

| 维度 | 模型结构化输出 | Agent 结构化输出 |
| --- | --- | --- |
| 操作对象 | 大模型对象 | Agent 对象 |
| 解析时机 | 每次模型调用 | Agent 决定"任务结束"时 |
| 绑定方式 | with\_structured\_output | response\_format 参数 |

四种策略：

1. **ProviderStrategy**：使用模型提供商的原生结构化输出功能。

2. **ToolStrategy**：动态创建"虚拟工具"，通过 Function Calling 实现。

    - 参数：`schema`、`tool_message_content`、`handle_errors`。

    - 支持 Union 联合模式：`ToolStrategy(Union[ContactInfo, EventInfo])`，LLM 智能选择 Schema。

3. **AutoStrategy**：自动选择 Provider 或 Tool 策略。

4. **None**：默认，自然语言响应。

handle\_errors 错误处理：True（默认捕获重试）/ False（抛异常）/ 自定义字符串 / 异常类型 / 自定义函数。

**评分要点**：

- 优秀：能讲清 ProviderStrategy 与 ToolStrategy 的底层差异（原生约束 vs Function Calling）、Union 联合模式的应用场景、handle\_errors 的多种配置策略。

- 及格：能说出四种策略名称和 ToolStrategy 的基本用法。

- 不足：只知道 Agent 能结构化输出。

**常见追问**：1) ToolStrategy 的"虚拟工具"是什么意思？2) Union 联合模式在什么场景下有用？

---

### 七、智能体 Agents

#### Q29【八股】【Agents】【L1】Agent 的定义与 create\_agent 统一入口

**题目**：什么是 Agent？LangChain 1.x 的 create\_agent() 相比 0.x 有什么改进？

**思考方向**：从 Agent 定义和 API 演进两个角度回答。

**考察点**：Agent 概念、create\_agent、版本对比。

**参考答案**：

- Agent 定义：以大语言模型为推理与决策核心，结合记忆、工具调用与环境交互能力，能够进行规划决策并执行复杂任务以达成目标的软件系统。

- Agent 关键能力：理解用户问题 → 拆解任务 → 判断是否需要工具 → 调用哪些工具 → 利用工具结果生成回答并推进任务。

v0.x vs v1.x：

- v0.x：碎片化，每种 Agent 单独 API（`create_react_agent`、`create_structured_chat_agent`、`create_tool_calling_agent`）。

- v1.x：统一入口 `create_agent()`，取代所有分支函数。Agent 本质是 LangGraph 的 `CompiledStateGraph` 实例。

```python
agent = create_agent(
    model=model,
    tools=[tool1, tool2],
    system_prompt="...",
    middleware=[...],
    interrupt_before=None,
    interrupt_after=None,
    debug=False,
    name="my_agent"
)
```

**评分要点**：

- 优秀：能讲清统一入口的设计哲学（降低认知负担）、Agent 本质是 CompiledStateGraph（与 LangGraph 的关系）、各参数的作用。

- 及格：能说出 Agent 定义和 create\_agent 的基本参数。

- 不足：只知道"Agent 能调工具"。

**常见追问**：1) Agent 本质是 CompiledStateGraph 对开发者有什么影响？2) v0.x 的 create\_react\_agent 还能用吗？

---

#### Q30【八股】【Agents】【L1】Agent 的调用与返回值

**题目**：如何调用 Agent？返回值的结构是什么？如何获取最终答案？

**思考方向**：从输入消息到输出字典的完整链路。

**考察点**：Agent invoke、返回值结构、消息提取。

**参考答案**：

```python
response = agent.invoke({"messages": [{"role": "user", "content": "问题"}]})
```

- 返回值是字典，包含 `messages` 列表。

- 最终答案：`response['messages'][-1].content`

- 消息列表包含完整的交互历史：HumanMessage → AIMessage(tool\_calls) → ToolMessage → AIMessage(最终答案)。

- 可通过 config 限制工具调用次数：`config = {"recursion_limit": 5}`。

**评分要点**：

- 优秀：能讲清返回字典的完整结构、messages 列表中的消息序列、recursion\_limit 的作用与默认值、与直接调 model.invoke 的区别。

- 及格：能说出 invoke 的基本用法和获取最终答案的方式。

- 不足：只知道能调用 Agent。

**常见追问**：1) recursion\_limit 设太小会有什么问题？2) 如何从 messages 中提取工具调用历史？

---

#### Q31【八股】【Agents】【L2】ReAct 循环与工具选择

**题目**：什么是 ReAct 循环？Agent 是如何选择和调用工具的？

**思考方向**：从"思考→行动→观察"的循环理解 Agent 的推理过程。

**考察点**：ReAct 框架、工具选择机制、推理循环。

**参考答案**：
ReAct 循环流程：

```text
用户问题 → AI 思考 → 调用工具 → 观察结果 → 继续思考 → ... → 最终答案
```

工具选择依据：

1. 工具的 docstring（描述 + 参数说明）。

2. 问题内容。

3. 模型自动选择最匹配的工具。

重试机制：通过 system\_prompt 引导 Agent 自主重试：

```python
system_prompt="""当工具返回以 'TEMP_UNAVAILABLE:' 开头的结果时，
说明是临时故障，不要立即放弃；你应再次调用同一个工具，最多重试 3 次。"""
```

工具数量建议：2-5 个最佳，过多会降低选择准确性。

**评分要点**：

- 优秀：能讲清 ReAct 的 Thought-Action-Observation 循环、工具选择基于 docstring 的匹配机制、重试策略的 prompt 工程、工具过多的降级方案（LLM tool selector 中间件）。

- 及格：能说出 ReAct 循环流程和工具选择依据。

- 不足：只知道"Agent 会调工具"。

**常见追问**：1) ReAct 和 Plan-and-Execute 有什么区别？2) 工具超过 10 个时怎么优化选择？

---

#### Q32【八股】【Agents】【L2】Agent 流式输出的 8 种 stream\_mode

**题目**：Agent 的 stream() 方法有哪 8 种 stream\_mode？各自输出什么内容？

**思考方向**：从不同监控需求（状态/进度/Token/任务/调试）理解。

**考察点**：流式输出、stream\_mode、多模式组合。

**参考答案**：

| 模式 | 输出内容 | 使用场景 |
| --- | --- | --- |
| `values` | 完整状态信息 | 状态持久化 |
| `updates`（默认） | 增量更新 | 监控执行进度 |
| `messages` | Token 流式输出 | 打字机效果 |
| `tasks` | 任务生命周期 | 监控任务 |
| `debug` | 任务步骤 + 时间戳 | 调试 |
| `checkpoints` | 检查点状态 | 工作流恢复 |
| `custom` | 自定义业务数据 | 进度/日志 |

多模式组合：

```python
for stream_mode, chunk in agent.stream(
    {"messages": [...]},
    stream_mode=["tasks", "updates"]
):
    print(f"模式: {stream_mode}, 数据: {chunk}")
```

**评分要点**：

- 优秀：能讲清多模式组合的机制、messages 模式的 Token 级推送、checkpoints 模式与工作流恢复的关系、与模型级 stream() 的区别。

- 及格：能说出 5+ 种模式及基本场景。

- 不足：只知道 stream 能流式输出。

**常见追问**：1) messages 模式和模型级的 stream() 有什么区别？2) 如何同时获取 Token 流和任务进度？

---

#### Q33【八股】【Agents】【L3】Agent 系统提示词与工具动态绑定

**题目**：Agent 的系统提示词有哪两种设置方式？如何实现工具的动态绑定？

**思考方向**：从静态配置 vs 运行时动态注入的角度理解。

**考察点**：系统提示词、工具动态绑定、中间件。

**参考答案**：
系统提示词两种方式：

1. **静态设置**：`create_agent(model=model, system_prompt="你是助手")`

2. **动态设置**：通过中间件在运行时注入/修改系统提示词。

工具绑定：

- **静态绑定**：创建时传入 `tools=[tool1, tool2]`。

- **动态绑定**：使用中间件在运行时根据上下文动态选择/添加工具。

系统提示词的作用：

- 明确说明 Agent 角色和职责。

- 定义输出格式规范。

- 说明何时使用工具（工具使用规则）。

- 提供行为约束（如重试策略、拒答规则）。

**评分要点**：

- 优秀：能讲清动态绑定中间件的实现原理、静态 vs 动态的适用场景、系统提示词对工具选择准确性的影响。

- 及格：能说出两种设置方式和动态绑定的概念。

- 不足：只知道 system\_prompt 参数。

**常见追问**：1) 动态绑定工具的中间件怎么实现？2) 系统提示词如何影响工具选择准确率？

---

#### Q34【八股】【Agents】【L3】Agent name 参数与多 Agent 场景

**题目**：create\_agent 的 name 参数有什么作用？在多 Agent 系统中如何使用？

**思考方向**：从单 Agent 标识到多 Agent 协作的场景递进。

**考察点**：Agent 标识、多 Agent 系统、可观测性。

**参考答案**：
name 参数的作用：

1. 多 Agent 场景区分不同 Agent。

2. 流式输出归因（区分哪个 Agent 产出了什么内容）。

3. 消息身份标记。

4. 调试与 trace 可读性。

5. 组件化封装。

6. 前端展示与运行态可观测性。

7. 运行时身份 ID。

**评分要点**：

- 优秀：能讲清 name 在 LangSmith Tracing 中的归因作用、多 Agent 编排中的角色标识、与 LangGraph 节点名称的关系。

- 及格：能说出 name 的 3+ 个作用。

- 不足：只知道 name 是名字。

**常见追问**：1) 多 Agent 场景如何编排？2) 流式输出中如何区分不同 Agent 的输出？

---

### 八、中间件 Middleware

#### Q35【八股】【中间件】【L1】中间件的概念与价值

**题目**：什么是 LangChain 中间件？为什么需要中间件？

**思考方向**：从"钩子函数"概念和"横切需求分离"的价值理解。

**考察点**：中间件定义、钩子机制、横切关注点。

**参考答案**：

- 中间件：Agent 执行过程中的**钩子函数**，在"模型调用前""模型调用后""工具调用前后"等关键节点进行拦截、控制和增强。

- 核心价值：把与业务无关、但与执行过程强相关的**横切逻辑**从 Agent 主流程中分离出来。

    - 日志与分析、转换、容错（重试/降级）、安全（限流/PII 检测）。

- 解决的问题：

    1. 主流程变乱（日志/鉴权/重试/风控/审计塞进主逻辑）。

    2. 横切逻辑难以复用（多个 Agent 需要相同逻辑）。

    3. 流程控制粒度不够细（需要精确到"模型调用前""工具调用后"）。

    4. 后期维护成本高（新增规则需修改多处代码）。

**评分要点**：

- 优秀：能讲清钩子函数的拦截机制、横切关注点的概念（类比 AOP/装饰器）、与传统 try-except 错误处理的区别。

- 及格：能说出中间件是钩子函数和 2-3 个价值点。

- 不足：只说"中间件是扩展功能"。

**常见追问**：1) 中间件和 Python 装饰器有什么区别？2) 中间件能修改 Agent 的输入输出吗？

---

#### Q36【八股】【中间件】【L2】六大分类与代表中间件

**题目**：LangChain 内置中间件分为哪六大类别？每类举一个代表中间件并说明适用场景。

**思考方向**：从解决的问题类型分类理解。

**考察点**：中间件分类、内置中间件、场景映射。

**参考答案**：

| 类别 | 核心目标 | 代表中间件 | 适用场景 |
| --- | --- | --- | --- |
| 成本与资源控制 | 控成本/配额/避免无限调用 | Model call limit, Tool call limit, Summarization | 生产环境成本治理、SaaS 控费 |
| 稳定性与容错保障 | 保证服务不中断/自动恢复 | Model fallback, Model retry, Tool retry | 线上生产、多模型多工具依赖 |
| 安全与合规风控 | 让 Agent 可控/可审/合规 | Human-in-the-loop, PII detection | 企业内部系统、审批流、客服 |
| 决策增强与智能编排 | 提升决策质量/任务拆解 | To-do list, LLM tool selector, Subagent | 研究型 Agent、多步骤分析 |
| 执行能力扩展 | 给 Agent 更多"手脚" | Shell tool, File search, Filesystem | 工程 Agent、运维 Agent |
| 开发调试与测试 | 方便开发/测试/验证 | LLM tool emulator | 开发阶段 mock、快速验证 |

LangChain 1.0 提供了 16 个预置中间件。

**评分要点**：

- 优秀：能讲清各类别的业务场景映射、SummarizationMiddleware 同时属于成本控制与调试辅助的跨类别特性、16 个预置中间件的开箱即用。

- 及格：能说出 6 大类别和至少 3 个代表中间件。

- 不足：只知道有中间件但说不清分类。

**常见追问**：1) SummarizationMiddleware 属于哪个类别？2) LLM tool selector 如何解决工具过多问题？

---

#### Q37【八股】【中间件】【L2】SummarizationMiddleware 参数详解

**题目**：SummarizationMiddleware 的 trigger 和 keep 参数有什么区别？如何配置触发条件？

**思考方向**：从"什么时候触发摘要"和"保留多少原始消息"两个维度理解。

**考察点**：SummarizationMiddleware、上下文压缩、参数配置。

**参考答案**：
**trigger（触发条件）**：列表，任一条件满足即触发。

- `("tokens", N)`：历史 token 累计达到 N 触发。

- `("messages", N)`：历史消息条数达到 N 触发。

- `("fraction", F)`：历史 token 达到 `max_input_tokens * F` 触发。需要模型的 profile 包含 max\_input\_tokens。

**keep（保留消息）**：同时只接收一种条件。

- `("tokens", N)`：保留 N 个 token 的消息。

- `("messages", N)`：保留 N 条最近消息。

- `("fraction", F)`：保留 `max_input_tokens * F` 个 token。

其他参数：

- `model`：用于摘要的模型。

- `summary_prompt`：自定义摘要提示词，需包含 `{messages}` 占位符。

- `trim_token_to_summarize`：摘要时历史消息最大 token 数，默认 4000。

```python
SummarizationMiddleware(
    model=model,
    trigger=[("tokens", 100), ("messages", 6), ("fraction", 0.001)],
    keep=("messages", 2)
)
```

摘要结果作为 HumanMessage 放入消息列表头部。

**评分要点**：

- 优秀：能讲清 trigger 是 OR 逻辑、keep 是单选、fraction 需要 max\_input\_tokens 的原因（DeepSeek 需要手动配置 profile）、摘要结果作为 HumanMessage 的设计。

- 及格：能说出 trigger 和 keep 的基本用法和 3 种条件。

- 不足：只知道有摘要功能。

**常见追问**：1) trigger 设三个条件是 OR 还是 AND？2) DeepSeek 模型为什么需要手动配置 max\_input\_tokens？

---

#### Q38【八股】【中间件】【L3】HumanInTheLoopMiddleware 精细控制

**题目**：HumanInTheLoopMiddleware 的 interrupt\_on 参数如何实现工具级别的精细控制？三种人工决策是什么？

**思考方向**：从"不同工具不同策略"和"审批/编辑/拒绝"两个维度理解。

**考察点**：人机协作、interrupt\_on 配置、审批流程。

**参考答案**：
三种人工决策：**approve**（同意执行）、**edit**（编辑调用配置后执行）、**reject**（拒绝执行）。

interrupt\_on 配置：

```python
interrupt_on={
    "get_weather": True,  # 所有决策都可选
    "read_email_tool": False,  # 不中断，无需审批
    "send_email_tool": {  # 精细控制
        "allowed_decisions": ["approve", "reject"],  # 只允许同意/拒绝
        "description": "发送邮件中断啦"
    }
}
```

- `True`：所有决策（approve, edit, reject）都可选。

- `False`：不中断。

- `InterruptOnConfig`：精细控制 `allowed_decisions` 和 `description`。

需要配合 `checkpointer` 实现中断后继续运行。

**评分要点**：

- 优秀：能讲清不同工具不同策略的设计思路、allowed\_decisions 的精细控制价值、checkpointer 在中断恢复中的作用、与 Agent 的 interrupt\_before 参数的关系。

- 及格：能说出三种决策和 interrupt\_on 的基本配置。

- 不足：只知道有"人工审核"功能。

**常见追问**：1) 中断后如何恢复 Agent 执行？2) edit 决策能修改什么？3) 如果所有工具都设 True 会有什么问题？

---

#### Q39【八股】【中间件】【L3】自定义中间件设计

**题目**：如果需要实现一个"敏感信息检测中间件"（检测用户输入中的 PII 并脱敏），你会怎么设计？

**思考方向**：从"拦截点选择→检测逻辑→脱敏处理→流程放行/阻断"设计。

**考察点**：自定义中间件、安全合规、工程设计。

**参考答案**：
设计思路：

1. **拦截点**：在模型调用前拦截，检查用户输入消息。

2. **检测逻辑**：用正则/NER 模型检测 PII（手机号、身份证、邮箱等）。

3. **处理策略**：

    - 脱敏：替换敏感信息为掩码（如 `138****1234`），放行流程。

    - 阻断：严重敏感信息直接中断，返回提示。

4. **日志记录**：记录检测到的 PII 类型和处理方式（脱敏不记录原文）。

5. **可配置**：通过参数控制不同敏感级别的处理策略。

也可直接使用 LangChain 内置的 PII detection 中间件。

**评分要点**：

- 优秀：能设计完整的拦截→检测→处理→放行链路、考虑误判场景（如用户主动提供手机号）、与内置 PII detection 的对比选型。

- 及格：能说出基本设计思路和 2-3 个处理步骤。

- 不足：只说"检测敏感词"。

**常见追问**：1) 脱敏后的信息如何还原给模型？2) 正则和 NER 模型各有什么优劣？

---

### 九、上下文与记忆

#### Q40【八股】【记忆】【L1】大模型的无状态特性与记忆需求

**题目**：为什么大模型需要记忆？大模型的"无状态"是什么意思？

**思考方向**：从大模型 API 的设计本质理解记忆的必要性。

**考察点**：无状态机制、记忆概念、上下文工程。

**参考答案**：

- 大模型本身是"无状态"的，不会记忆任何上下文。每次调用 `agent.invoke()` 都是全新的开始。

- 如果不传递历史消息，模型不知道之前说了什么。

- 记忆（Memory）：专门负责"存储历史交互信息"的组件，核心作用是「保存上下文」和「提供上下文」。

- 上下文工程（Context Engineering）：负责"合理组织"记忆和任务信息，让 LLM 的响应更连贯。

**评分要点**：

- 优秀：能讲清无状态的设计原因（水平扩展/无状态服务）、上下文工程与记忆的关系、在 Agent 场景中的体现。

- 及格：能说出无状态概念和记忆的基本作用。

- 不足：不知道模型是无状态的。

**常见追问**：1) 为什么大模型 API 要设计成无状态？2) 上下文工程和提示词工程有什么区别？

---

#### Q41【八股】【记忆】【L1】短期记忆与长期记忆

**题目**：LangChain 中记忆分为哪两类？各自的作用范围和实现方式是什么？

**思考方向**：从作用域（会话内 vs 跨会话）和持久化方式理解。

**考察点**：记忆分类、短期记忆、长期记忆。

**参考答案**：

- **短期记忆（Short-term memory，会话级记忆）**：

    - 作用范围：单个对话线程（Thread）内。

    - 一旦开启新对话（更换 thread\_id），记忆即消失。

    - 实现：State（消息列表）+ Checkpointer（持久化）+ Thread ID（会话标识）。

- **长期记忆（Long-term memory，跨会话级记忆）**：

    - 在会话间存储用户特定或应用级数据，并在会话线程间共享。

    - 可以在任何线程中被调用。

    - 实现：store 对象 + 向量数据库/外部存储。

- v0.x 通过专用 xxxMemory 类管理；v1.x 通过 state 和 store 构建，更统一。

**评分要点**：

- 优秀：能讲清 v0.x 与 v1.x 记忆管理的演进、state 和 store 的分工、长期记忆的自定义命名空间。

- 及格：能说出两类记忆的定义和基本实现方式。

- 不足：只知道"有记忆功能"。

**常见追问**：1) 长期记忆的命名空间和 thread\_id 有什么区别？2) v1.x 为什么废弃 xxxMemory 类？

---

#### Q42【八股】【记忆】【L2】三种上下文类型

**题目**：LangGraph 提供了哪三种管理上下文的方法？各自的可变性、生命周期和访问方式是什么？

**思考方向**：从可变性和生命周期两个维度分类。

**考察点**：上下文类型、state/store/context。

**参考答案**：

| 上下文类型 | 描述 | 可变性 | 生命周期 | 访问方法 |
| --- | --- | --- | --- | --- |
| 动态运行时上下文 | 单次运行中会演变的可变数据 | 动态 | 单次运行 | state 对象 |
| 动态跨会话上下文 | 对话间共享的持久数据（用户偏好、历史洞察、知识条目） | 动态 | 跨对话 | store 对象 |
| 静态运行时上下文 | 启动时传入的用户元数据、工具、数据库连接 | 静态 | 单次运行 | context 对象 |

**评分要点**：

- 优秀：能讲清三种类型的实际应用场景（state 存消息历史、store 存用户画像、context 存数据库连接）、可变性对设计的影响。

- 及格：能说出三种类型名称和基本属性。

- 不足：只知道 state。

**常见追问**：1) store 如何实现跨会话数据共享？2) 静态上下文在什么场景下有用？

---

#### Q43【八股】【记忆】【L2】Checkpointer 与 Thread ID 机制

**题目**：如何使用 InMemorySaver 实现多轮对话记忆？Thread ID 如何隔离不同会话？

**思考方向**：从代码实现和会话隔离两个角度回答。

**考察点**：Checkpointer、Thread ID、会话隔离。

**参考答案**：

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
agent = create_agent(model=model, tools=[], checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}
# 第一轮
response1 = agent.invoke({"messages": [HumanMessage("我叫张三")]}, config=config)
# 第二轮（自动带入历史）
response2 = agent.invoke({"messages": [HumanMessage("我叫什么？")]}, config=config)
# Agent: 你叫张三。
```

Thread ID 隔离：

- 同一 thread\_id 共享记忆，不同 thread\_id 完全隔离。

- 更新 thread\_id 即重新开启对话。

- 生产环境：多用户不同 thread\_id = 不同会话；同一用户不同任务不同 thread\_id。

Checkpointer 自动管理：

1. 读取之前历史 → 2. 追加新消息 → 3. 调用模型（传入完整历史） → 4. 保存新历史。

生产环境可用 SqliteSaver、PostgresSaver 替代 InMemorySaver。

常见错误：没有 checkpointer / 没有 config / thread\_id 不同。

**评分要点**：

- 优秀：能讲清 checkpointer 的自动管理流程、get\_state() 的用途、InMemorySaver 的局限性（进程结束丢失）、生产环境持久化方案。

- 及格：能写出基本代码和 Thread ID 隔离机制。

- 不足：只知道"传 checkpointer"。

**常见追问**：1) InMemorySaver 进程重启后会怎样？2) 如何查看 Agent 当前状态？3) 如何实现同一用户多个独立任务？

---

#### Q44【八股】【记忆】【L3】记忆系统的生产化设计

**题目**：生产环境中如何设计 Agent 的记忆系统？InMemorySaver 有什么局限？如何替代？

**思考方向**：从持久化、多用户、性能、扩展性四个维度思考。

**考察点**：生产化记忆、持久化方案、多用户场景。

**参考答案**：
InMemorySaver 局限：

- 内存存储，进程结束即丢失。

- 不支持多进程共享。

- 无容量管理，可能导致内存溢出。

生产化设计：

1. **持久化**：使用 SqliteSaver（轻量）或 PostgresSaver（生产级）替代。

2. **多用户隔离**：每个用户分配唯一 thread\_id，自动隔离会话。

3. **上下文压缩**：配合 SummarizationMiddleware 自动压缩长会话。

4. **长期记忆**：通过 store + 向量数据库实现跨会话记忆（如用户偏好、历史摘要）。

5. **容量管理**：限制消息列表长度、定期清理过期会话。

6. **监控**：通过 LangSmith 监控 Token 消耗、会话长度、记忆命中率。

**评分要点**：

- 优秀：能设计完整的生产化方案（持久化+压缩+长期记忆+监控+容量管理）、讲清 SqliteSaver vs PostgresSaver 的选型、与 SummarizationMiddleware 的配合。

- 及格：能说出 InMemorySaver 的局限和 2-3 个替代方案。

- 不足：只知道 InMemorySaver 不适合生产。

**常见追问**：1) PostgresSaver 如何保证并发安全？2) 如何实现"记住用户偏好"的长期记忆？3) 会话过多导致存储膨胀怎么处理？

---

### 十、RAG 检索增强生成

#### Q45【八股】【RAG】【L1】RAG 的定义与价值

**题目**：什么是 RAG？它解决了大模型的哪些局限？

**思考方向**：从大模型三大局限切入，再讲 RAG 如何解决。

**考察点**：RAG 概念、大模型局限、知识增强。

**参考答案**：
RAG（Retrieval-Augmented Generation，检索增强生成）：结合信息检索与文本生成的技术，提升大模型在回答专业问题时的准确性和可靠性。

解决的大模型三大局限：

1. **知识滞后**：LLM 训练数据有截止日期，无法反映最新信息。

2. **知识缺失**：训练依赖公开数据，缺乏企业内部资料/私有数据。

3. **幻觉**：LLM 可能编造不存在的信息，在金融/医疗等场景致命。

RAG 优缺点：

- 优点：丰富上下文、提升时效性和可靠性、保护数据隐私。

- 缺点：响应时延较高、消耗大量 Token 资源。

**评分要点**：

- 优秀：能讲清幻觉产生的四个原因（训练偏差/过度泛化/深层含义缺失/领域知识缺失）、RAG 与微调的对比选型、隐私保护的价值。

- 及格：能说出 RAG 定义和三大局限。

- 不足：只说"RAG 是检索+生成"。

**常见追问**：1) RAG 能完全解决幻觉吗？2) RAG 和微调什么时候选哪个？

---

#### Q46【八股】【RAG】【L1】RAG 工作流程

**题目**：RAG 的完整工作流程包含哪些环节？每个环节做什么？

**思考方向**：从数据源到最终答案的完整链路。

**考察点**：RAG 工作流程、各环节职责。

**参考答案**：
六个环节：

1. **Source（数据源）**：RAG 外挂的知识库，支持多种格式（文本/图片/代码/文档/API/网站）。

2. **Load（加载）**：Document Loaders 将非结构化文本加载为 Document 对象（page\_content + metadata）。

3. **Transform（转换）**：Text Splitters 将长文本切分为小块（Chunk），以适应模型上下文窗口。

4. **Embed（嵌入）**：Text Embedding Models 将文本转换为向量表示。

5. **Store（存储）**：将向量存入向量数据库，支持高效搜索。

6. **Retrieve（检索）**：根据用户查询，从向量库中检索最相关的文档块。

7. **Generate（生成）**：将检索结果 + 用户查询组合为 Prompt，传给 LLM 生成答案。

**评分要点**：

- 优秀：能讲清每个环节的技术选型、切分是最具挑战性的环节、嵌入的双向应用（文档写入和查询匹配）。

- 及格：能说出六个环节名称和基本职责。

- 不足：只说"检索文档+生成"。

**常见追问**：1) 哪个环节对最终效果影响最大？2) 延迟主要花在哪个环节？

---

#### Q47【八股】【RAG】【L2】文档加载器与 BaseLoader

**题目**：LangChain 提供了哪些常用文档加载器？BaseLoader 的设计有什么好处？

**思考方向**：从统一接口设计和多数据源支持理解。

**考察点**：文档加载器、BaseLoader、Document 类。

**参考答案**：
常用加载器：

- TextLoader：文本文件

- CSVLoader：CSV 文件（每行一个 Document）

- JSONLoader：JSON 文件（使用 jq schema 解析）

- PyPDFLoader：PDF 文件（支持 plain/layout 提取模式）

- UnstructuredMarkdownLoader：Markdown

- UnstructuredHTMLLoader：HTML

- DirectoryLoader：批量加载文件夹

- MinerU：在线 PDF/Word/PPT/图片解析服务

BaseLoader 设计：

- 所有加载器继承 BaseLoader，统一 `load()` 和 `lazy_load()` 方法。

- 支持 `load_and_split()` 一站式加载+切分。

- Document 类：`page_content`（字符串文本）+ `metadata`（字典元数据）。

- 支持 lazy\_load 延迟加载，缓解大文件内存压力。

JSONLoader 的 jq\_schema：

- `.[]`：遍历数组

- `.[].text`：提取数组元素的 text 字段

- `.key[].text`：提取嵌套字段

**评分要点**：

- 优秀：能讲清 BaseLoader 的继承体系与统一接口价值、lazy\_load 的内存优化、jq schema 的灵活性、PDF 解析的挑战（扫描版/电子版/多列布局）。

- 及格：能说出 4+ 种加载器和 BaseLoader 的基本设计。

- 不足：只知道 TextLoader。

**常见追问**：1) CSVLoader 每行一个 Document 有什么好处？2) PDF 双列布局怎么处理？3) jq schema 如何提取嵌套 JSON？

---

#### Q48【八股】【RAG】【L2】文本切分策略对比

**题目**：LangChain 提供了哪几种文本切分策略？各有什么优劣？哪个是首选？

**思考方向**：从"简单→灵活→智能"的递进理解，对比语义完整性和计算成本。

**考察点**：文本切分、Chunk 策略、RecursiveCharacterTextSplitter。

**参考答案**：
五种切分策略：

1. **按句子切分**：保持语义完整性，但块大小不均。

2. **按固定字符数**：简单，但可能切断句子。

3. **按固定字符数 + 重叠窗口**：避免切断关键内容，确保信息连贯。

4. **递归字符切分（RecursiveCharacterTextSplitter）**：首选策略，动态确定切分点，根据文档复杂性和内容密度调整块大小。

5. **语义切分（SemanticChunker）**：基于嵌入向量相似度，最精确，但计算成本高。

递归字符切分的底层逻辑：

- 先拆分：按分隔符列表 `["\n\n", "\n", " ", ""]` 顺序尝试，超出 chunk\_size 则递归用下一个分隔符。

- 后合并：遍历切分后的块，按 chunk\_size 合并，保留 chunk\_overlap 重叠区域。

- 支持自定义中文分隔符：`["\n\n", "\n", "。", "！", "？", "……", "，", ""]`

其他切分器：

- TokenTextSplitter：按 Token 数分割，与 LLM 计费一致。

- SemanticChunker：基于嵌入向量余弦距离，设置阈值切断。

- HTMLHeaderTextSplitter：按 HTML 标题层级分割。

- CodeTextSplitter：按代码语法结构分割。

- MarkdownTextSplitter：按 Markdown 标题分割。

TextSplitter 核心参数：`chunk_size`（默认 4000）、`chunk_overlap`（默认 200）、`separator`、`length_function`、`keep_separator`、`add_start_index`。

**评分要点**：

- 优秀：能讲清递归切分的"先拆分后合并"底层逻辑、SemanticChunker 的 breakpoint\_threshold\_type 四种类型、中文分隔符自定义的必要性、chunk\_size 和 chunk\_overlap 的调参思路。

- 及格：能说出 3+ 种切分策略和 RecursiveCharacterTextSplitter 是首选。

- 不足：只知道按字符切分。

**常见追问**：1) chunk\_overlap 设多大合适？2) SemanticChunker 的 percentile 阈值怎么调？3) 中文文本为什么需要自定义分隔符？

---

#### Q49【八股】【RAG】【L2】嵌入模型选型与初始化

**题目**：常用的嵌入模型有哪些？如何通过 LangChain 初始化嵌入模型？

**思考方向**：从模型选型维度（向量维度/序列长度/多语言）和初始化方式理解。

**考察点**：嵌入模型、init\_embeddings、向量维度。

**参考答案**：
常用嵌入模型：

| 模型 | 机构 | 向量维度 | 序列长度 | 特点 |
| --- | --- | --- | --- | --- |
| bge-large-zh | BAAI | 1024 | 512 | 开源，中文 |
| bge-m3 | BAAI | 1024 | 8192 | 开源，多语言 |
| text-embedding-3-small | OpenAI | 1536 | 8192 | 多语言 |
| text-embedding-3-large | OpenAI | 3072 | 8192 | 多语言 |

初始化方式：

```python
from langchain.embeddings import init_embeddings
embedding_model = init_embeddings(
    model="openai:text-embedding-3-large",
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)
```

LangChain 提供两种向量化接口：

- `embed_query(text)`：对用户查询向量化。

- `embed_documents(docs)`：对文档列表向量化。

选型考量：向量维度影响存储和检索速度，序列长度影响能处理的最大文本长度，多语言能力影响跨语言场景效果。

**评分要点**：

- 优秀：能讲清向量维度与存储/检索性能的权衡、序列长度对分块策略的影响、bge-m3 在中文场景的优势、embed\_query 与 embed\_documents 的区别。

- 及格：能说出 2-3 种嵌入模型和 init\_embeddings 的用法。

- 不足：只知道"把文本变向量"。

**常见追问**：1) 向量维度越高越好吗？2) bge-m3 为什么序列长度 8192 很重要？3) embed\_query 和 embed\_documents 有什么区别？

---

#### Q50【八股】【RAG】【L3】分块参数实验设计

**题目**：如何设计一个分块参数（chunk\_size / chunk\_overlap）的 A/B 实验？如何评估效果？

**思考方向**：从变量控制、评估指标、实验流程三个维度设计。

**考察点**：分块参数调优、实验设计、RAG 评估。

**参考答案**：
实验设计：

1. **变量控制**：固定嵌入模型、检索 TopK、生成模型，只变 chunk\_size（如 256/512/1024）和 chunk\_overlap（如 0/50/100）。

2. **评测集构建**：准备 question-expected\_answer 对，覆盖不同类型问题（事实型/推理型/多跳型）。

3. **评估指标**：

    - Recall@K：相关文档是否在 TopK 检索结果中。

    - MRR：相关文档的排名倒数。

    - Faithfulness：答案是否忠实于检索内容（不产生幻觉）。

    - Answer Relevance：答案是否回答了用户问题。

4. **实验流程**：不同参数组合 → 检索 → 生成 → 评估 → 对比 → 选最优。

5. **LangSmith 集成**：用 Datasets & Experiments 管理评测集，Evaluators 自动打分。

**评分要点**：

- 优秀：能设计完整实验方案（变量控制→评测集→指标→对比）、能讲清 Recall@K/MRR/Faithfulness 的计算方式、能识别 Badcase 并归因到分块参数。

- 及格：能说出基本实验思路和 2-3 个评估指标。

- 不足：只知道"调参试试"。

**常见追问**：1) chunk\_size 太大或太小各有什么问题？2) 如何避免评测集的数据泄漏？3) Recall@K 的 K 怎么选？

---

#### Q51【八股】【RAG】【L3】SemanticChunker 语义分块深入

**题目**：SemanticChunker 的工作原理是什么？breakpoint\_threshold\_type 有哪几种？各自的适用场景是什么？

**思考方向**：从嵌入向量相似度计算和阈值算法理解。

**考察点**：语义分块、嵌入向量距离、阈值类型。

**参考答案**：
工作原理：

1. 用正则表达式将文本切分为句子。

2. 对每个句子计算嵌入向量。

3. 计算相邻句子的嵌入向量余弦距离。

4. 按照设定的阈值类型和阈值量确定切分点。

5. 在切分点处合并相邻块。

breakpoint\_threshold\_type 四种类型：

| 类型 | 原理 | 适用场景 |
| --- | --- | --- |
| percentile | 取距离分布的第 N 百分位值为阈值 | 常规文本（文章、报告） |
| standard\_deviation | 均值 + N 倍标准差为阈值 | 语义变化剧烈的文档 |
| interquartile | 用四分位距（IQR）定义异常值边界 | 长文档（如书籍） |
| gradient | 基于嵌入向量变化的梯度检测 | 实验性需求 |

breakpoint\_threshold\_amount：

- percentile 模式：0.0~100.0，默认 95.0。值越小切分越敏感（碎片多），值越大切分越粗（块大）。

- standard\_deviation 模式：浮点数（如 1.5 = 均值+1.5 倍标准差）。

SemanticChunker vs RecursiveCharacterTextSplitter：

| 特性 | SemanticChunker | RecursiveCharacter |
| --- | --- | --- |
| 分割依据 | 嵌入向量相似度 | 固定字符/换行符 |
| 语义完整性 | 保持主题连贯 | 可能切断句子逻辑 |
| 计算成本 | 高（需嵌入模型） | 低 |
| 块大小 | 不均匀 | 基本均匀 |

**评分要点**：

- 优秀：能讲清余弦距离的计算流程、四种阈值类型的数学原理、percentile 值与切分敏感度的关系、与传统切分的计算成本对比。

- 及格：能说出工作原理和 2-3 种阈值类型。

- 不足：只知道"按语义切分"。

**常见追问**：1) percentile 默认 95.0 意味着什么？2) 语义分块为什么块大小不均匀？3) 什么场景下语义分块明显优于递归切分？

---

#### Q52【八股】【RAG】【L3】RAG 系统的端到端优化

**题目**：如果一个 RAG 系统的检索质量不好（用户问题与检索文档不匹配），你会从哪些环节排查和优化？

**思考方向**：从"分块→嵌入→检索→重排→生成"全链路排查。

**考察点**：RAG 全链路优化、Badcase 归因、系统调优。

**参考答案**：
全链路排查：

1. **分块环节**：

    - chunk\_size 是否合适（太大信息冗余，太小语义断裂）。

    - chunk\_overlap 是否保留上下文。

    - 切分策略是否匹配文档类型（代码/Markdown/纯文本）。

2. **嵌入环节**：

    - 嵌入模型是否适配语言（中文选 bge-m3）。

    - 向量维度是否足够。

    - 序列长度是否覆盖 chunk。

3. **检索环节**：

    - TopK 是否太小（漏召回）或太大（噪声多）。

    - 是否需要混合召回（向量 + BM25）。

    - 是否需要 Query Rewrite（用户问题表达不清）。

4. **重排环节**：

    - 是否加 Rerank（cross-encoder 精排）。

    - Rerank 模型选型。

5. **生成环节**：

    - Prompt 是否提供了足够上下文。

    - 是否有拒答策略（检索质量低时不回答）。

6. **评估闭环**：

    - 用 LangSmith 追踪每步效果。

    - Badcase 归因到具体环节。

    - 用评测集持续迭代。

**评分要点**：

- 优秀：能设计完整的排查流程（分块→嵌入→检索→重排→生成）、能讲清每个环节的常见问题和优化手段、能结合 LangSmith 做全链路追踪。

- 及格：能说出 3+ 个排查方向和基本优化手段。

- 不足：只说"换模型"。

**常见追问**：1) 如何判断是分块问题还是检索问题？2) Query Rewrite 在什么场景下有用？3) Rerank 的延迟代价如何权衡？

---

## 项目深挖题

#### Q53【项目深挖】【Agent 项目】技术选型题

**题目**：你项目中选择 LangChain 1.x 的 create\_agent 而非直接用 LangGraph 搭建，选型依据是什么？两者有什么区别？

**思考方向**：从"开箱即用 vs 灵活定制"的权衡切入。

**考察点**：框架选型、create\_agent vs LangGraph、技术决策。

**参考答案**：

- create\_agent 是 LangGraph 的上层封装，本质返回 CompiledStateGraph。

- 选 create\_agent：快速搭建、内置 ReAct 循环、内置中间件支持、代码量少。

- 选 LangGraph 直接搭建：需要自定义节点/边/条件边、非标准工作流、需要精确控制执行流程。

- 实际项目中：标准 Agent 用 create\_agent，复杂多 Agent 编排用 LangGraph。

**评分要点**：

- 优秀：能讲清 create\_agent 的底层是 CompiledStateGraph、何时该"降级"到直接用 LangGraph、两者的灵活性与开发效率权衡。

- 及格：能说出两者的基本区别和选型理由。

- 不足：只说"create\_agent 更简单"。

**常见追问**：1) create\_agent 能实现 LangGraph 的所有功能吗？2) 什么场景必须用 LangGraph？

---

#### Q54【项目深挖】【RAG 项目】实现难点题

**题目**：在你的 RAG 项目中，文档切分参数（chunk\_size/overlap）是怎么确定的？遇到了什么问题？

**思考方向**：从实际调参经历和 Badcase 分析回答。

**考察点**：分块调优、实际问题解决、量化思维。

**参考答案**：

- 初始参数：chunk\_size=500, chunk\_overlap=50（经验值）。

- 遇到问题：中文文档按字符切分导致语义断裂，检索到不完整的上下文。

- 优化：

    1. 换用 RecursiveCharacterTextSplitter + 中文分隔符 `["。", "！", "？", "……"]`。

    2. A/B 测试不同 chunk\_size（256/512/1024），用 Recall@5 评估。

    3. 最终选 chunk\_size=512, chunk\_overlap=100。

- 进一步优化：对结构化文档（Markdown/代码）使用对应的切分器。

**评分要点**：

- 优秀：能讲清调参的完整流程（初始值→问题→实验→选优）、能说出具体的评估指标和数值、能结合文档类型选切分策略。

- 及格：能说出基本调参过程和遇到的问题。

- 不足：只说"试了几次选了个好的"。

**常见追问**：1) chunk\_overlap=100 是怎么定的？2) 如果文档类型混合（文本+表格+代码）怎么处理？

---

#### Q55【项目深挖】【Agent 项目】边界与故障题

**题目**：你的 Agent 在工具调用失败时怎么处理？有没有遇到过 Agent 陷入死循环的情况？

**思考方向**：从错误处理机制和循环防护两个维度回答。

**考察点**：错误处理、死循环防护、生产经验。

**参考答案**：
工具失败处理：

1. 工具内部 try-except 返回友好错误信息（如 `TEMP_UNAVAILABLE: 服务暂时不可用`）。

2. system\_prompt 引导 Agent 重试（最多 3 次）。

3. 中间件 Tool retry 自动重试。

4. Model fallback 切换备用模型。

死循环防护：

1. `recursion_limit` 限制最大步数（如 25 步）。

2. Tool call limit 中间件限制工具调用次数。

3. 监控日志发现重复调用模式。

4. Model call limit 限制模型调用次数。

**评分要点**：

- 优秀：能讲清三层防护的分工、recursion\_limit 的合理设置、Tool call limit 中间件的应用、死循环的常见原因（工具返回模糊结果导致 Agent 反复尝试）。

- 及格：能说出基本错误处理和 recursion\_limit。

- 不足：只说"加了 try-except"。

**常见追问**：1) recursion\_limit 设多少合适？2) 什么情况会导致 Agent 死循环？3) Model fallback 切换后上下文怎么处理？

---

#### Q56【项目深挖】【Agent 项目】反思优化题

**题目**：如果让你重新做这个 LangChain Agent 项目，你会做哪些改进？

**思考方向**：从架构、性能、可维护性、用户体验四个维度反思。

**考察点**：架构视野、成长性、改进思维。

**参考答案**：

1. **架构**：引入 SummarizationMiddleware 自动压缩长会话，避免 Token 超限。

2. **安全**：加 HumanInTheLoopMiddleware 对敏感操作（发邮件/调数据库）人工审批。

3. **性能**：用 astream() 替代 invoke() 实现流式输出，提升用户体验。

4. **可维护性**：抽取可复用模板库（PromptLibrary），集中管理提示词。

5. **监控**：接入 LangSmith 全链路追踪，建立评估闭环。

6. **扩展性**：通过中间件实现工具动态绑定，避免硬编码。

**评分要点**：

- 优秀：能从多维度提出改进方案、讲清每个改进的价值和实现方式、体现架构视野和工程化思维。

- 及格：能说出 3+ 个改进方向。

- 不足：只说"代码重构"。

**常见追问**：1) SummarizationMiddleware 会不会丢失关键信息？2) 如何平衡安全审批和用户体验？

---

#### Q57【项目深挖】【RAG 项目】量化数据题

**题目**：你说 RAG 系统提升了问答准确率，怎么测的？基准是什么？

**思考方向**：从评测集构建、评估指标、对比实验回答。

**考察点**：量化思维、评估方法、数据真实性。

**参考答案**：

- 评测集：人工标注 100 个 question-expected\_answer 对，覆盖常见/边缘/歧义问题。

- 基准：纯 LLM 直答（无 RAG）作为 baseline。

- 指标：Faithfulness（忠实度）、Answer Relevance（答案相关性）、Recall@5（召回率）。

- 对比：RAG vs 纯 LLM，Faithfulness 从 45% 提升到 82%，Recall@5 达到 78%。

- 工具：LangSmith Datasets & Experiments 自动评估。

**评分要点**：

- 优秀：能讲清评测集构建方法、三种指标的含义、baseline 的选择依据、用 LangSmith 自动化评估。

- 及格：能说出基本评估方法和 1-2 个指标。

- 不足：只说"测试了一下效果好"。

**常见追问**：1) 100 个问题够吗？2) Faithfulness 怎么计算？3) 评测集会不会有偏差？

---

#### Q58【项目深挖】【综合】LangChain 版本升级题

**题目**：从 LangChain 0.x 迁移到 1.x，你遇到了哪些 breaking changes？怎么处理的？

**思考方向**：从具体 API 变化和迁移策略回答。

**考察点**：版本迁移、API 变化、工程实践。

**参考答案**：
主要 breaking changes：

1. **Agent 创建**：`create_react_agent` / `create_tool_calling_agent` 等统一为 `create_agent()`。

2. **记忆管理**：xxxMemory 类废弃，改用 state + checkpointer + thread\_id。

3. **消息类型**：引入 content\_blocks 标准化多模态数据。

4. **提示词**：推荐 ChatPromptTemplate 替代 PromptTemplate。

5. **模块拆分**：langchain-core / langchain-classic / langchain-community 分层。

迁移策略：

1. 逐模块迁移，先 Agent 后 Memory。

2. 用 langchain-classic 兼容旧代码，逐步替换。

3. 参考 LangSmith Tracing 对比迁移前后行为。

**评分要点**：

- 优秀：能讲清具体 API 变化、迁移策略、langchain-classic 的兼容作用、测试验证方法。

- 及格：能说出 2-3 个 breaking changes 和基本处理方式。

- 不足：只说"改了 API"。

**常见追问**：1) langchain-classic 会一直保留吗？2) 迁移后性能有变化吗？

---

## 场景 / 系统设计题

---

#### Q59【系统设计】【Agent + RAG】设计企业知识库问答 Agent

**题目**：基于 LangChain 设计一个企业内部知识库问答 Agent，支持多部门、多文档类型、权限隔离。给出架构与关键决策。

**思考方向**：从"数据接入→切分→向量化→检索→Agent 编排→权限→监控"全链路设计。

**考察点**：RAG + Agent 系统设计、权限隔离、工程化。

**参考答案框架**：

1. **数据接入**：TextLoader/PyPDFLoader/MinerU 加载多格式文档，DirectoryLoader 批量处理。

2. **切分**：RecursiveCharacterTextSplitter + 中文分隔符，chunk\_size=512, overlap=100。结构化文档用对应切分器。

3. **向量化**：bge-m3 嵌入模型（多语言、序列长度 8192）。

4. **存储**：向量数据库按部门分 collection，metadata 存部门标签实现权限过滤。

5. **检索**：向量检索 TopK + BM25 混合召回，Rerank 精排。

6. **Agent 编排**：create\_agent + 知识检索工具 + system\_prompt 约束回答范围。

7. **权限隔离**：检索时按用户部门过滤 metadata，多租户 thread\_id 隔离会话。

8. **监控**：LangSmith 全链路追踪，Faithfulness/Recall@K 评估。

**评分要点**：

- 优秀：能讲清混合召回策略、权限隔离的多层设计（metadata 过滤 + collection 分离）、拒答策略（检索质量低不回答）、成本控制（缓存/小模型预筛）。

- 及格：架构完整、讲清检索和 Agent 编排、有权限意识。

- 不足：只画框图无决策依据。

**常见追问**：1) 知识库更新后旧版本怎么处理？2) 如何控制大模型调用成本？3) 敏感问题怎么处理？

---

#### Q60【系统设计】【Agent + 中间件】设计高可用 AI 客服 Agent

**题目**：基于 LangChain 设计一个支撑 1000+ 并发的 AI 客服 Agent，要求高可用、可降级、有人工接管。给出架构与关键决策。

**思考方向**：从"接入→会话管理→Agent 编排→容灾降级→人工接管→监控"全链路设计。

**考察点**：高并发 Agent、中间件组合、容灾降级、人机协作。

**参考答案框架**：

1. **接入层**：FastAPI + SSE 流式输出，按用户分流 thread\_id。

2. **会话管理**：PostgresSaver 持久化会话状态，SummarizationMiddleware 自动压缩长会话。

3. **Agent 编排**：create\_agent + 知识检索工具 + 工单系统工具。

4. **容灾**：

    - Model fallback：主模型（DeepSeek）失败切备用模型（GPT）。

    - Model retry / Tool retry：自动重试。

    - Model call limit / Tool call limit：防止无限调用。

5. **人工接管**：HumanInTheLoopMiddleware 对敏感操作（退款/修改订单）人工审批。

6. **降级**：模型超时降级到规则引擎/转人工，知识库未命中拒答。

7. **监控**：LangSmith Tracing + Monitoring（Token 消耗/QPS/错误率/延迟/成本）。

**评分要点**：

- 优秀：能讲清中间件组合策略（容灾+成本+安全三类配合）、PostgresSaver 的并发安全、SSE 流式 + astream 的并发控制、人工接管的流程设计。

- 及格：架构完整、讲清并发与会话管理、有降级思路。

- 不足：只画框图无并发/容灾考量。

**常见追问**：1) 1000 并发时 PostgresSaver 会不会成为瓶颈？2) Model fallback 切换后上下文怎么处理？3) 如何评估人工接管的比例是否合理？

---

#### Q61【系统设计】【多 Agent】设计多 Agent 协作系统

**题目**：基于 LangChain + LangGraph 设计一个多 Agent 协作系统，如"研究型 Agent + 写作 Agent + 审核 Agent"的文档生成流水线。

**思考方向**：从"角色分工→编排方式→状态传递→错误处理→人工审核"设计。

**考察点**：多 Agent 编排、LangGraph、Agent 协作。

**参考答案框架**：

1. **角色定义**：

    - 研究 Agent：检索资料、整理要点（create\_agent + RAG 工具）。

    - 写作 Agent：基于研究要点生成文档（create\_agent + 文件写入工具）。

    - 审核 Agent：检查文档质量、合规性（create\_agent + 结构化输出）。

2. **编排**：LangGraph StateGraph，Node 为各 Agent，Edge 为条件路由。

    - 研究 Agent → 写作 Agent → 审核 Agent

    - 审核不通过 → 回到写作 Agent 修改

3. **状态传递**：State 存储中间产物（研究要点/草稿/审核意见）。

4. **中间件**：

    - Subagent：复杂任务拆给子 Agent。

    - To-do list：任务规划和进度跟踪。

    - HumanInTheLoopMiddleware：关键节点人工审核。

5. **Checkpointer**：持久化工作流状态，支持中断恢复。

6. **Agent name**：区分不同 Agent 的流式输出和 Tracing。

**评分要点**：

- 优秀：能讲清 LangGraph 的条件路由设计、State 数据结构设计、审核不通过的回环机制、Checkpointer 的工作流恢复。

- 及格：能给出基本架构和角色分工。

- 不足：只说"多个 Agent 合作"。

**常见追问**：1) 审核 Agent 的结构化输出怎么设计？2) 如果写作 Agent 反复修改不通过怎么办？3) 如何追踪多 Agent 间的数据传递？

---

## 手撕代码题

Q62【手撕代码】【Tools】手写简化版工具调用流程

**题目**：用 LangChain 1.x API 实现一个完整的工具调用流程：定义一个天气查询工具，绑定到模型，用户提问"北京天气如何"，模型生成工具调用请求，手动执行工具，将结果回传模型生成最终答案。

**思考方向**：按四步骤实现：定义→绑定→执行→回传。

**考察点**：@tool 装饰器、bind\_tools、tool\_calls、ToolMessage、消息列表管理。

**参考答案骨架**：

```python
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model

# 1. 定义工具
@tool
def get_weather(city: str) -> str:
    """
    获取指定城市的天气信息
    Args:
        city: 城市名称
    Returns:
        天气信息字符串
    """
    return f"{city}今天晴天，温度 15°C"

# 2. 绑定工具到模型
model = init_chat_model(model="deepseek:deepseek-v4-flash", api_key="...")
model_with_tools = model.bind_tools([get_weather])

# 3. 模型生成工具调用请求
messages = [{"role": "user", "content": "北京天气如何？"}]
response = model_with_tools.invoke(messages)
messages.append(response)  # 追加 AI 回复（含 tool_calls）

# 4. 手动执行工具并回传
if response.tool_calls:
    for tc in response.tool_calls:
        tool_result = get_weather.invoke(tc)  # 返回 ToolMessage
        messages.append(tool_result)
    # 5. 最终答案
    final = model_with_tools.invoke(messages)
    print(final.content)
else:
    print(response.content)
```

**评分要点**：

- 优秀：代码可运行、处理多 tool\_calls、消息列表管理正确（append AIMessage 和 ToolMessage）、有错误处理。

- 及格：四步骤逻辑正确，代码基本可运行。

- 不足：只写了工具定义或遗漏回传步骤。

**常见追问**：1) 如果模型返回多个 tool\_calls 怎么处理？2) 工具执行失败怎么处理？

---

#### Q63【手撕代码】【结构化输出】手写 Agent 结构化输出

**题目**：用 LangChain 1.x 实现一个 Agent，要求最终输出结构化的 ContactInfo 对象（name, phone, email），使用 ToolStrategy 策略，并包含错误处理。

**思考方向**：定义 Schema → 创建 Agent → 配置 ToolStrategy → 处理结果。

**考察点**：Pydantic、create\_agent、ToolStrategy、Agent 结构化输出。

**参考答案骨架**：

```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.tools import tool

class ContactInfo(BaseModel):
    """联系人信息"""
    name: str = Field(description="姓名")
    phone: str = Field(description="电话号码")
    email: str = Field(description="邮箱地址")

@tool
def search_contact(name: str) -> str:
    """搜索联系人信息"""
    return f"找到联系人：{name}，电话 138xxxx1234，邮箱 test@example.com"

agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    tools=[search_contact],
    response_format=ToolStrategy(
        ContactInfo,
        handle_errors=True  # 捕获异常自动重试
    )
)

response = agent.invoke({
    "messages": [{"role": "user", "content": "帮我查一下张三的联系方式"}]
})

# 提取结构化结果
structured = response["structured_response"]
print(structured.name, structured.phone, structured.email)
```

**评分要点**：

- 优秀：代码结构完整、ToolStrategy 配置正确、handle\_errors 处理、Pydantic Field description 规范。

- 及格：基本逻辑正确，能创建带结构化输出的 Agent。

- 不足：只定义了 Pydantic 模型。

**常见追问**：1) ToolStrategy 和 ProviderStrategy 有什么区别？2) handle\_errors=False 会怎样？

---

#### Q64【手撕代码】【RAG】手写简化版 RAG 检索流程

**题目**：用 LangChain API 实现一个简化版 RAG：加载文本文件 → 递归切分 → 向量化 → 存入向量库 → 检索 → 组装 Prompt → 调用模型生成答案。

**思考方向**：按 RAG 六环节实现：Load → Split → Embed → Store → Retrieve → Generate。

**考察点**：文档加载、文本切分、嵌入、向量检索、Prompt 组装。

**参考答案骨架**：

```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import init_embeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

# 1. Load
loader = TextLoader("knowledge.txt", encoding="utf-8")
docs = loader.load()

# 2. Split
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "，", ""]
)
chunks = splitter.split_documents(docs)

# 3. Embed
embeddings = init_embeddings(model="openai:text-embedding-3-small", api_key="...")

# 4. Store
vectorstore = FAISS.from_documents(chunks, embeddings)

# 5. Retrieve
query = "LangChain是什么？"
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
retrieved_docs = retriever.invoke(query)
context = "\n".join([doc.page_content for doc in retrieved_docs])

# 6. Generate
model = init_chat_model(model="deepseek:deepseek-v4-flash", api_key="...")
prompt = ChatPromptTemplate.from_messages([
    ("system", "根据以下上下文回答问题。上下文：\n{context}"),
    ("human", "{question}")
])
response = model.invoke(prompt.invoke({"context": context, "question": query}))
print(response.content)
```

**评分要点**：

- 优秀：代码可运行、中文分隔符配置、检索 TopK 合理、Prompt 组装规范、有错误处理。

- 及格：六环节逻辑正确，代码基本可运行。

- 不足：遗漏存储或检索环节。

**常见追问**：1) 如何加 Rerank？2) 向量库选 FAISS 还是 Milvus？3) 如何实现混合召回？

---

#### Q65【手撕代码】【记忆】手写多轮对话记忆 Agent

**题目**：用 LangChain 1.x 实现一个带短期记忆的多轮对话 Agent，使用 InMemorySaver，支持 thread\_id 隔离，能记住用户姓名并在后续对话中引用。

**思考方向**：create\_agent + checkpointer + thread\_id + invoke。

**考察点**：记忆机制、Checkpointer、Thread ID、多轮对话。

**参考答案骨架**：

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

model = init_chat_model(model="deepseek:deepseek-v4-flash", api_key="...")

# 创建带记忆的 Agent
agent = create_agent(
    model=model,
    tools=[],
    checkpointer=InMemorySaver()
)

# 会话1：用户A
config_alice = {"configurable": {"thread_id": "user_alice"}}
agent.invoke(
    {"messages": [HumanMessage("你好，我叫Alice")]},
    config=config_alice
)
response = agent.invoke(
    {"messages": [HumanMessage("我叫什么名字？")]},
    config=config_alice
)
print(response["messages"][-1].content)  # "你叫Alice"

# 会话2：用户B（完全隔离）
config_bob = {"configurable": {"thread_id": "user_bob"}}
response = agent.invoke(
    {"messages": [HumanMessage("你还记得我叫什么吗？")]},
    config=config_bob
)
print(response["messages"][-1].content)  # "不知道你的名字"

# 查看状态
state = agent.get_state(config_alice)
print(state.values["messages"])
```

**评分要点**：

- 优秀：代码可运行、thread\_id 隔离正确、get\_state() 查看状态、能讲清 checkpointer 自动管理历史的流程。

- 及格：基本逻辑正确，能实现多轮记忆。

- 不足：没有 checkpointer 或没有 config。

**常见追问**：1) 如何在生产环境替换 InMemorySaver？2) 如何实现长期记忆（跨会话记住用户偏好）？

---

## 非技术类问题

---

#### Q66【行为面】你为什么从传统开发转 AI 方向？

**思考方向**：讲主动性与学习路径，把"经历短"转化为"学习力强"。

**参考答案要点**：

- 观察到 AI 技术的产业趋势和大模型应用爆发。

- 主动系统学习 LangChain 全链路（从概述到 RAG 到 Agent 到中间件）。

- 用项目验证学习成果（Agent 工具调用/RAG 知识库/多轮对话记忆）。

- 转型的核心优势：工程化思维 + AI 框架能力 = 能落地 AI 应用。

---

#### Q67【行为面】你觉得自己在这个方向最大的优势是什么？

**思考方向**：结合传统开发经验 + LangChain 全栈能力。

**参考答案要点**：工程化能力（系统设计/容灾/监控）+ AI 框架理解（LangChain 全链路）+ 快速学习能力。

---

#### Q68【HR 面】你的职业规划是什么？

**参考答案要点**：短期深耕 AI Agent 开发，成为团队 AI 技术骨干；中期向 AI 架构师发展，负责企业级 AI 系统设计。

---

#### Q69【行为面】学习中遇到最大的挑战是什么？怎么解决的？

**思考方向**：用 STAR 法回答，展示学习力和解决问题能力。

**参考答案要点**：可讲 LangChain 版本迁移（0.x → 1.x API 变化大）、Agent 死循环排查、RAG 检索质量调优等真实经历。

---

#### Q70【行为面】如果团队中技术选型有分歧（如选 LangChain 还是直接用 LangGraph），你怎么处理？

**参考答案要点**：先理清需求约束（快速交付 vs 精细控制）→ 做技术对比（create\_agent 是 LangGraph 封装）→ 快速原型验证 → 用数据决策 → 尊重团队共识。

---

#### Q71【行为面】项目 deadline 很紧，Agent 效果不达标怎么办？

**参考答案要点**：优先保证核心链路可用 → 降级方案（规则兜底/人工接管）→ 分阶段交付（先上基础版再迭代）→ 用 LangSmith 快速定位瓶颈。

---

#### Q72【行为面】AI 技术更新很快，你如何保持学习？

**参考答案要点**：持续关注 LangChain 官方文档和版本更新、动手做项目验证、参加技术社区讨论、复盘 Badcase 持续优化。
