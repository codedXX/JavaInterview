# LangGraph 面试题

---

## LangGraph 基础概念

### Q1【基础】LangGraph 和 LangChain 的定位有什么区别？在实际项目中如何选择？

**参考答案：**

| 对比维度 | LangChain | LangGraph |
| --- | --- | --- |
| 定位 | Agent 高层开发框架 | 底层编排框架 & Agent Runtime |
| 核心入口 | `create_agent` | `StateGraph` / `@entrypoint` |
| 适用场景 | 结构直接的 Agent 应用 | 复杂工作流、持久化状态、长时间运行、人工介入 |
| 流程控制 | Agent 循环自动管理 | 精细控制节点、边、条件分支 |
| 学习成本 | 较低 | 较高 |

选择建议：对于大多数 Agent 项目，从 LangChain 的 `create_agent` 开始即可；需要复杂工作流编排、确定性步骤与 Agent 步骤混合、长时间运行或底层状态控制时，再引入 LangGraph。`create_agent` 底层也基于 LangGraph 实现。

---

### Q2【基础】LangGraph 的三个基本要素是什么？分别说明它们的作用。

**参考答案：**

1. **State（状态）**：运行过程中的共享数据结构，承载图运行所需的上下文信息、中间结果和后续节点需要读取的数据，是节点之间传递信息的核心载体。

2. **Node（节点）**：具体执行单元，通常实现为一个函数。节点读取当前 State，执行业务逻辑，返回对 State 的局部更新。节点本身不直接修改全局状态，状态的合并与提交由运行时统一完成。

3. **Edge（边）**：定义节点之间的流转关系，决定一个节点执行完成后下一步进入哪个节点。Edge 可以是固定流转，也可以根据当前 State 进行条件判断，实现分支、循环等复杂控制流程。

---

### Q3【基础】描述 LangGraph 的 Superstep（超步）机制，一个超步包含哪几个阶段？

**参考答案：**

Superstep 是图运行过程中的一次"单步循环"。一次图运行从开始到结束由一系列连续的 Superstep 串联而成。每个 Superstep 包含三个阶段：

1. **计划/路由阶段（Plan/Routing）**：根据当前 State 和 Edge 的逻辑，确定本轮超步中应该被执行的节点。

2. **执行阶段（Execution）**：运行本轮被选中的节点。如果多个节点同时被触发，它们会并行执行。每个节点基于本轮开始时的状态快照进行计算，输出对状态的局部更新。一个节点产生的更新不会立即被其他节点读取到。

3. **状态更新/提交阶段（Update/Commit）**：当本轮所有节点都执行完成后，LangGraph 将它们的输出统一合并到 State 中，生成新的状态快照，作为下一轮 Superstep 的输入。

---

### Q4【进阶】Graph API 和 Functional API 的区别是什么？如何选型？

**参考答案：**

| 对比项 | Graph API | Functional API |
| --- | --- | --- |
| 编程风格 | 声明式图结构 | 命令式函数流程 |
| 核心抽象 | State、Node、Edge | entrypoint、task |
| 状态管理 | 显式定义全局 State | 更多依赖函数参数和返回值 |
| 流程表达 | 通过节点和边表达 | 通过普通 Python 控制流表达 |
| 可视化能力 | 强，天然适合画图和调试 | 弱，更像普通代码流程 |
| 适合场景 | 复杂工作流、多分支、多节点协作 | 简单流程、快速原型、已有代码改造 |
| 学习成本 | 相对更高 | 相对更低 |

选型建议：从零构建或流程结构复杂，用 Graph API；现有代码改造、快速原型验证或流程逻辑简单，用 Functional API。学习 LangGraph 建议优先掌握 Graph API，因为它更能体现 LangGraph 的核心思想。

---

## 状态管理

### Q5【基础】LangGraph 中定义 State Schema 有哪三种方式？各自的特点是什么？

**参考答案：**

1. **TypedDict**：将状态字段视为字典的 Key，字段访问方式为 `state["字段名"]`。不匹配时抛出 `KeyError`。写法简洁、结构清晰，是官方推荐的首选方式。

2. **dataclass**：将状态字段视为类的属性，字段访问方式为 `state.字段名`。不匹配时抛出 `TypeError`。

3. **Pydantic BaseModel**：字段访问方式同 dataclass。不匹配时抛出 `ValidationError`，对输入字段进行校验，格式要求最严格。

三种方式都要求字段名称完全一致。对于节点返回字段不匹配的情况，三种方式的行为统一：状态更新会被忽略。

推荐优先使用 TypedDict，因为大多数官方案例也采用此方式，写法简洁且不会引入额外的数据校验开销。

---

### Q6【进阶】什么是 State Reducer？如何定义和使用？默认行为是什么？

**参考答案：**

State Reducer 是 LangGraph 中用于合并状态更新的核心机制，定义了如何将多个节点对同一状态键的更新合并。

- **函数签名**：`(Value, Value) -> Value`，接收当前值和更新值，返回合并后的新值。

- **定义方式**：通过 `Annotated[Type, reducer_function]` 为状态键指定 Reducer。

- **默认行为**：未指定 Reducer 的状态键使用覆盖策略（Last-Write-Wins），即后一次更新值直接覆盖原有值。

常用内置 Reducer：

- `operator.add`：对列表执行拼接合并，对数字执行加法。

- `add_messages`：专用于合并消息列表，基于消息 `id` 进行合并——新消息追加，相同 `id` 的消息会被覆盖。

---

### Q7【进阶】Overwrite 的作用是什么？它和 Reducer 的关系如何？

**参考答案：**

`Overwrite` 用于在特定更新中绕过 Reducer，告诉 LangGraph 本次状态更新不走该字段原本定义的 Reducer，而是直接用新值覆盖旧值。

关键特性：

- `Overwrite` 只影响当前这一次更新，不会修改状态字段本身的 Reducer 定义。

- 后续节点如果继续正常返回该字段的更新值，仍然按照原来的 Reducer 逻辑进行合并。

使用方式：

```python
from langgraph.types import Overwrite
return {"logs": Overwrite(["node_b"])}
```

如果某字段绑定了 `operator.add`，正常情况下会追加合并；使用 `Overwrite` 后，当前状态的该字段会被直接覆盖为指定值。

---

### Q8【进阶】LangGraph 支持哪四种状态类型？它们各自的用途是什么？

**参考答案：**

1. **全局状态/内部状态（OverAllState）**：图内部主要使用的状态，创建 `StateGraph` 时传递给 `state_schema` 参数，包含运行过程中需要读写的大部分字段。

2. **输入状态（InputState）**：图对外接收输入时使用的状态，传递给 `input_schema` 参数，约束调用图时允许传入哪些字段。

3. **输出状态（OutputState）**：图最终对外返回结果时使用的状态，传递给 `output_schema` 参数，约束图运行结束后只返回哪些字段。

4. **私有状态（PrivateState）**：图内部节点之间传递的临时状态，不作为图的输入也不作为图的最终输出，通过节点函数的入参类型注解声明。

设计规范：输入状态和输出状态通常应是全局状态的子集；私有状态和全局状态应尽量避免字段重名；节点函数应明确声明入参状态类型和返回状态类型。

---

### Q9【进阶】`MessagesState` 和 `AgentState` 的区别是什么？

**参考答案：**

**MessagesState** 是 LangGraph 官方提供的预定义状态类型，适合构建聊天机器人、Agent 等需要维护消息列表的场景：

```python
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

开发者可以直接继承并在其基础上扩展自定义字段。

**AgentState** 是 LangChain Agent 内部使用的状态类型（`langchain.agents.middleware.types.AgentState`），包含三个字段：

- `messages`：存储消息列表，使用 `add_messages` 作为 Reducer。

- `jump_to`：Agent 中间件体系内部使用的控制字段，用于表示运行流程的跳转意图。普通 StateGraph 不会因该字段自动跳转。

- `structured_response`：存储 Agent 的结构化输出，使用 `OmitFromInput` 标注不应作为外部输入字段暴露。

在普通自定义 LangGraph 项目中，一般不建议直接基于 `AgentState` 扩展图状态，推荐使用 `MessagesState`。

---

## 控制流

### Q10【基础】LangGraph 中构建顺序结构有哪两种方式？

**参考答案：**

1. `add_edge`：在两个节点之间添加有向边，是最基本的控制流构建方式。

```python
builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", END)
```

2. `add_sequence`：传入可执行对象列表，LangGraph 会按列表顺序依次添加节点，并在相邻节点之间自动添加边。

```python
builder.add_sequence([node_a, node_b])
```

`add_sequence` 更适合构建简单的线性执行流程，等价于手动调用多次 `add_node` 和 `add_edge`。

---

### Q11【基础】START 和 END 是否可以省略？为什么？

**参考答案：**

- **END 可以省略**：END 不是运行阶段真正执行的节点，而是终止标记。当最后一个节点执行完成后没有新节点被触发，图运行会自然结束。但在分支、条件跳转、循环退出等场景中，显式指向 END 更利于阅读和维护。

- **START 通常不能省略**：START 不只是语义上的起点标记，还用于告诉 LangGraph 图运行时应从哪些节点开始执行。如果没有从 START 出发的边，LangGraph 就无法确定图的初始执行节点。

建议在实际开发中保留指向 END 的边，让图结构更完整、语义更清晰。

---

### Q12【进阶】静态分支和动态分支的区别是什么？

**参考答案：**

- **静态分支**：节点的下游候选节点在图编译阶段就完全确定，运行时根据条件选择哪条边执行。核心判断：编译期知道下游集合。典型 API：`add_conditional_edges`、并行节点。

- **动态分支**：运行时决定后续执行目标或任务数量。可以为同一个下游节点动态创建多个执行任务。核心判断：运行时决定下游目标和数量。典型 API：`Send` + `add_conditional_edges`（动态扇出）、`Command(goto=...)`（动态跳转）。

"动态"不是指运行时临时创建新的节点定义，节点本身仍需要在图编译前注册。动态性主要体现在运行时决定触发哪些节点以及创建多少个执行任务。

---

### Q13【进阶】`add_conditional_edges` 的 `path` 和 `path_map` 参数分别是什么？如何使用？

**参考答案：**

- `source`：条件分支的起始节点。

- `path`：路由规则，是一个可执行对象（通常为函数），返回值表示跳转的目标节点，可以是单个目标或多个目标的序列。

- `path_map`：路由规则返回值到真实节点名之间的映射。

`path_map` 的三种用法：

1. **省略（None）**：`path` 返回值必须是合法的节点名称。

2. **字典**：`{"业务标签": "节点名"}`，路由函数返回业务标签，通过映射找到真实节点。

3. **列表**：`["node_a", "node_b"]`，等价于 `{"node_a": "node_a", "node_b": "node_b"}`。

使用 `path_map` 的好处：路由函数可以返回业务含义更清晰的标签，图节点名称可以保持工程化命名，渲染图结构时边上可以显示路由标签。

---

### Q14【进阶】`Send` 的作用是什么？使用时有什么注意事项？

**参考答案：**

`Send` 用于动态扇出场景（Map-Reduce），运行时创建多个任务并行执行。

构造器：

```python
Send(node: str, arg: Any)
```

- `node`：待启动的下游节点名称，必须已注册。

- `arg`：传递给下游节点的信息，仅对该节点可见，通常应是私有状态。

路由函数返回 `Sequence[Send]`，运行时根据每个 `Send` 实例创建对应任务，多个任务通常在同一个超步中并行执行。

注意事项：

1. 使用 `Send` 时必须配置 `path_map`，否则图渲染器无法正确展示条件边关系。

2. 如果多个并行任务写入同一个状态字段，通常需要为该字段定义 Reducer，否则可能出现 `InvalidUpdateError`。

3. 每个 `Send` 实例接收到的 `arg` 是独立的，互不相干。

---

### Q15【进阶】`Command` 的作用是什么？它和 `add_conditional_edges` 有什么区别？

**参考答案：**

`Command` 用于在节点返回值中同时实现状态更新和控制流跳转。

构造参数：

- `update`：更新图状态，效果等同于节点直接返回状态更新字典。

- `goto`：指定节点执行完成后的跳转目标。

- `graph`：存在子图时，指定跳转发生在哪一层图中。

- `resume`：用于恢复被中断的图执行。

区别：

| 维度 | `Command(goto=...)` | `add_conditional_edges` |
| --- | --- | --- |
| 路由位置 | 路由逻辑写在节点返回值中 | 路由逻辑在独立的 router 函数中 |
| 内聚性 | 更内聚，节点根据执行结果决定下一跳 | 控制逻辑与节点执行逻辑分离 |
| 适合场景 | 节点执行结果直接决定下一跳 | 路由规则独立、希望图结构更清晰 |

注意事项：如果某个节点使用 `Command(goto=...)` 控制后续跳转，一般不要再给该节点额外添加普通下游边，否则多个路径可能同时生效。

`Command` 的类型注解 `Command[Literal["node_a", "node_b"]]` 不是运行时限制，而是为了让 LangGraph 和类型检查工具知道可能的跳转目标，对图结构渲染很重要。

---

### Q16【进阶】Fan-in 的"与触发"和"或触发"有什么区别？

**参考答案：**

- **"与"触发（静态扇入）**：使用列表作为边的起点，等待所有上游分支全部完成后才触发下游节点，且只触发一次。

```python
builder.add_edge(["node_c", "node_d"], "node_e")
```

`node_e` 需要等待 `node_c` 和 `node_d` 全部完成后才会被触发一次。

- **"或"触发（独立触发）**：使用多条独立边，多个上游分支分别独立触发下游节点，下游节点可能被触发多次。

```python
builder.add_edge("node_c", "node_e")
builder.add_edge("node_d", "node_e")
```

`node_c` 完成后触发 `node_e`，`node_d` 完成后再次触发 `node_e`。

关键：`add_edge(["node_c", "node_d"], "node_e")` 不等于 `add_edge("node_c", "node_e")` + `add_edge("node_d", "node_e")`。

---

### Q17【进阶】`defer=True` 的作用和底层实现机制是什么？

**参考答案：**

`defer=True` 使节点延迟到常规图运行流程结束后，在额外的超步中触发执行。适合用于日志记录、审计检查、结果汇总、收尾清理等场景。

底层实现机制：

1. **编译阶段**：为延迟节点的边创建 `LastValueAfterFinish` 类型通道（普通节点使用 `EphemeralValue`）。

2. **常规运行阶段**：该通道可以被写入但不可用，不会触发下游节点。首次写入时不添加到 `updated_channels` 列表。

3. **常规流程结束后**：运行时调用所有 Channel 的 `finish()` 方法。`LastValueAfterFinish` 通道在 `finish()` 首次调用后变为可用。

4. **触发延迟节点**：变为可用的通道被加入 `updated_channels`，在额外超步中触发延迟节点执行。

---

### Q18【实战】ReAct 循环的静态实现和动态实现有什么区别？

**参考答案：**

ReAct（Reason + Action）是典型的 `LLM → Tool → LLM → Tool → ... → LLM` 循环结构。

| 维度 | 静态实现 | 动态实现 |
| --- | --- | --- |
| 路由位置 | 路由逻辑在独立的 `router()` 函数中 | 路由逻辑写在节点返回值中 |
| 核心 API | `add_conditional_edges("llm_node", router)` | `Command(goto=..., update=...)` |
| 图结构表达 | 显式声明条件边，更直观 | 控制逻辑更内聚，代码更紧凑 |
| 适合场景 | 路由规则独立、希望图结构更清晰 | 节点执行结果直接决定下一跳 |

两种方式本质区别不在于是否能循环，而在于路由逻辑写在哪里。静态实现把控制逻辑放在图结构定义阶段；动态实现把控制逻辑放在节点返回值中。

---

### Q19【实战】如何处理循环结构中的递归限制问题？

**参考答案：**

`recursion_limit` 表示单次图运行过程中允许执行的最大 SuperStep 数量。处理方式有两种：

**主动方法——使用** `RemainingSteps`：

```python
from langgraph.managed import RemainingSteps

class OverAllState(TypedDict):
    remaining_steps: RemainingSteps

def router(state: OverAllState) -> Literal["loop_node", END]:
    if state["remaining_steps"] < 3:
        return END
    return "loop_node"
```

优势：在图内部实现优雅降级，可以保存中间状态到检查点，图可以正常结束不抛异常。

**被动方法——捕获** `GraphRecursionError`：

```python
from langgraph.errors import GraphRecursionError
try:
    graph.invoke({}, config={"recursion_limit": 10})
except GraphRecursionError as e:
    logger.info("超步数量达到最大限制: {}", e)
```

优势：实现更简单，不需要修改图内部逻辑，可以集中处理错误。

最佳实践：循环结构是业务逻辑的一部分时（如 ReAct 循环、多轮反思），推荐主动方法在图内部处理；被动方法可作为兜底防线。

---

## 节点执行与容错

### Q20【基础】LangGraph 节点容错机制有哪几种？

**参考答案：**

| 机制 | 类型 | 说明 |
| --- | --- | --- |
| 重试 Retry | 节点容错 | 网络抖动、接口偶发失败时重新执行节点 |
| 超时 Timeout | 节点容错 | 限制单次节点执行时间，避免图被长时间阻塞 |
| 异常处理 Error Handling | 节点容错 | 节点最终失败后执行兜底逻辑 |
| 缓存 Cache | 执行优化 | 相同输入时直接返回缓存结果，避免重复计算 |

执行优先级：节点执行失败 → RetryPolicy 判断是否重试 → 重试次数耗尽 → error\_handler 兜底 → 无 error\_handler 则异常继续向外抛出。

---

### Q21【进阶】`RetryPolicy` 的核心参数有哪些？指数退避策略如何工作？

**参考答案：**

| 参数 | 默认值 | 描述 |
| --- | --- | --- |
| `max_attempts` | 3 | 最大尝试次数（包括首次执行） |
| `initial_interval` | 0.5 | 第一次重试前的等待时间（秒） |
| `backoff_factor` | 2.0 | 每次重试后等待时间的放大倍数 |
| `max_interval` | 128.0 | 相邻两次重试之间的最大等待时间（秒） |
| `jitter` | True | 是否为重试间隔添加随机抖动 |
| `retry_on` | `default_retry_on` | 哪些异常需要触发重试 |

指数退避：`0.5s → 1.0s → 2.0s → 4.0s → ...`，`max_interval` 限制最大等待时间。

`max_attempts=3` 表示总共调用 3 次（包括首次执行），不是失败后的 3 次重试。

`jitter=True` 在并发场景下打散重试时间，避免大量任务同时重试导致服务被打爆。

---

### Q22【进阶】`default_retry_on` 默认重试策略的规则是什么？

**参考答案：**

默认策略会对大多数异常进行重试，但以下异常及其子类通常不触发重试：

- `ValueError`、`TypeError`、`ArithmeticError`、`ImportError`、`LookupError`、`NameError`、`SyntaxError`、`RuntimeError`、`ReferenceError`、`StopIteration`、`StopAsyncIteration`、`OSError`

这些异常通常更像代码逻辑错误，单纯重试没有意义。

对于 HTTP 库异常：

- `requests` 和 `httpx` 的 `HTTPError`：只对 5xx 状态码重试，不对 4xx 重试。因为 4xx 通常表示客户端请求错误（参数错误、鉴权失败等），5xx 表示服务端异常更适合重试。

- `ConnectionError`：直接重试。

`retry_on` 支持三种写法：指定单个异常类型、指定多个异常类型的元组、自定义判断函数 `Callable[[Exception], bool]`。

---

### Q23【实战】节点缓存的使用场景和配置方式是什么？

**参考答案：**

**适用场景**（需同时满足）：

1. 节点函数具有确定性（相同输入产生相同输出）

2. 节点执行成本较高（大模型调用、API 请求、复杂计算等）

3. 相同输入会重复出现

4. 输入能被缓存键函数稳定处理

**配置两步**：

```python
# 第一步：为节点配置 cache_policy
builder.add_node("node_a", node_a, cache_policy=CachePolicy(ttl=10))

# 第二步：编译图时启用缓存后端
graph = builder.compile(cache=InMemoryCache())
```

`CachePolicy` 参数：

- `key_func`：缓存键生成函数，默认使用 `default_cache_key`（基于 `pickle` 序列化节点输入）。

- `ttl`：缓存存活时间（秒），`None` 表示不会因时间原因自动过期。

如果只配置 `cache_policy` 但编译时没有传入 `cache=`，缓存不会真正生效。

如果节点依赖外部状态（当前时间、API 数据、数据库查询等），应根据业务场景设置合适的 `ttl`，或把这些变量纳入缓存 Key 的计算逻辑。

---

### Q24【进阶】Timeout 和 Error Handling 的使用限制是什么？

**参考答案：**

两者都要求 `langgraph>=1.2`（课程环境为 1.1.2，无法使用）。

**Timeout**：

- 仅适用于异步节点（`async def` 定义的节点）

- 同步节点一旦开始执行会阻塞当前线程，Python 进程内缺少通用机制从外部安全终止正在运行的同步函数

- 通过 `TimeoutPolicy(run_timeout=60)` 配置，超时后抛出 `NodeTimeoutError`，该异常交给 `RetryPolicy` 判断是否重试

**Error Handling**：

- 通过 `error_handler=` 设置兜底逻辑

- 执行顺序：节点失败 → RetryPolicy 判断重试 → 重试次数耗尽 → 调用 error\_handler

- `error_handler` 可以返回状态更新，也可以通过 `Command` 路由到其他节点

---

## 持久化与记忆管理

### Q25【基础】什么是 Durable Execution？它和 Persistence 的关系是什么？

**参考答案：**

- **Durable Execution（可恢复执行）**：将任务执行过程中的关键进度、状态、结果保存到可靠存储中，使任务可以在中断、失败、等待外部输入后继续执行。解决的是"执行过程能否恢复"的问题。

- **Persistence（持久化）**：在图执行过程中，将每个关键阶段的图状态保存为检查点，并按照线程进行组织。

关系：Persistence 是基础，Durable Execution 是建立在 Persistence 之上的能力。

使用场景：多轮会话、中断恢复、失败恢复、Time Travel。

---

### Q26【基础】如何启用可恢复执行？

**参考答案：**

两步配置：

```python
# 第一步：编译图时传入 checkpointer
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 第二步：调用时传递带有 thread_id 的配置
config = {"configurable": {"thread_id": "unique_session_id"}}
graph.invoke(input, config=config)
```

`thread_id` 是会话的唯一标识，用于区分不同会话。

---

### Q27【进阶】Checkpoint 后端有哪些实现？InMemorySaver 和 PostgresSaver 的关键区别是什么？

**参考答案：**

| 类名 | 后端 |
| --- | --- |
| `InMemorySaver` | 内存（In-memory） |
| `SqliteSaver` | SQLite |
| `PostgresSaver` | PostgreSQL |
| `MongoDBSaver` | MongoDB |
| `RedisSaver` | Redis |

所有后端都继承自 `langgraph.checkpoint.base.BaseCheckpointSaver`。

`InMemorySaver` vs `PostgresSaver`：

- `InMemorySaver`：状态保存在当前进程内存中，进程结束或对象重建后丢失。

- `PostgresSaver`：状态保存在 PostgreSQL 中，程序重启后仍可读取，多个 Python 进程可共享。

---

### Q28【进阶】三种持久化模式（durability）的区别是什么？

**参考答案：**

| 模式 | 写入时机 | 性能开销 | 响应延迟 | 容灾能力 |
| --- | --- | --- | --- | --- |
| `exit` | 运行退出时写入 | 低 | 最低 | 最弱 |
| `async`（默认） | 每个超步末尾写入主检查点，后台异步写入 | 高 | 较高 | 较强 |
| `sync` | 和 async 一样，但等待写入完成后才进入下一个超步 | 高 | 最高 | 最强 |

`durability` 控制的是检查点写入策略，不改变图本身的执行逻辑。

---

### Q29【进阶】如何查看历史检查点？`StateSnapshot` 包含哪些字段？

**参考答案：**

**查看方式**：

```python
# 查看完整历史检查点（从最新到最旧）
history = list(graph.get_state_history(config=config))

# 查看最新检查点
latest = graph.get_state(config=config)

# 根据 ID 查看指定检查点
target_config = {"configurable": {"thread_id": "123", "checkpoint_id": "xxx"}}
snapshot = graph.get_state(config=target_config)
```

**StateSnapshot 字段**：

- `values`：当前检查点的状态值

- `next`：下一步将要执行的节点

- `config`：当前检查点配置（含 `thread_id`、`checkpoint_ns`、`checkpoint_id`）

- `metadata`：包含 `source`（`input`/`loop`）、`step`、`parents` 等

- `created_at`：创建时间

- `parent_config`：父检查点配置

- `tasks`：当前检查点关联的待执行任务（`PregelTask` 实例元组）

- `interrupts`：当前图的中断信息

`step=-1` 为输入检查点（`source="input"`），`step=0+` 为循环检查点（`source="loop"`）。

---

### Q30【实战】如何在失败后恢复运行？恢复时的行为是什么？

**参考答案：**

**恢复条件**：

1. 启用检查点存储器（跨进程需用数据库后端）

2. 再次运行时用 `None` 作为输入

3. 配置信息包含 `thread_id` 但不能包含 `checkpoint_id`

```python
new_graph = builder.compile(checkpointer=checkpointer)
res = new_graph.invoke(None, config=config)
```

**恢复时的行为**：

- 根据 `thread_id` 从 checkpointer 读取该会话的最新检查点，从该检查点继续推进

- 如果某个超步中部分任务成功、部分失败，已经成功完成的任务结果会作为 `pending_writes` 被保存，恢复运行时不会重复执行

---

### Q31【实战】Time Travel 的 Replay 和 Fork 有什么区别？

**参考答案：**

**Replay（重放）**：

- 回到某个历史检查点，沿着原先的执行路径重新执行后续节点

- 配置中包含 `checkpoint_id`

- 检查点之后的 LLM 调用、API 请求等都会重新触发

- 检查点之前的节点不会重新执行

```python
res = graph.invoke(None, config=target_checkpoint.config)
```

**Fork（分叉）**：

- 回到某个历史检查点，修改状态，从该位置创建一条新的执行分支

- 依赖 `graph.update_state()` 方法

- `update_state()` 不会修改原来的历史检查点，而是基于某个历史检查点创建一个新的检查点

```python
change_input_config = graph.update_state(
    config=before_checkpoint.config,
    values={"user_input": "新输入"},
    as_node=START
)
graph.invoke(None, change_input_config)
```

`as_node` 参数指定状态更新应被视为哪个节点的输出。设置为 `START` 则从 START 的后继节点继续推进。

---

### Q32【进阶】Agent 的三种记忆类型是什么？

**参考答案：**

| 记忆类型 | 存储位置 | 访问方式 | 持久化 | 范围 |
| --- | --- | --- | --- | --- |
| 短期记忆 | 运行时状态 State，由 Checkpointer 保存 | State 字段 | 按 thread\_id 组织 | 同一会话内跨调用共享 |
| 长期记忆 | Store（长期记忆存储器） | `runtime.store` | 跨会话共享 | 跨会话 |
| 运行时上下文 | Context 对象 | `runtime.context` | 不持久化 | 仅当次调用有效 |

---

### Q33【实战】Store API 的核心概念和使用方式是什么？

**参考答案：**

Store 用于长期记忆管理，跨会话共享数据。

**核心概念**：

- **命名空间**：使用元组表达层级结构，如 `("users", "Alice")`

- **Item 对象**：包含 `namespace`、`key`、`value`、`created_at`、`updated_at`、`score`（配置了 embedding 时才有值）

**关键 API**：

```python
from langgraph.store.postgres import PostgresStore

with PostgresStore.from_conn_string(DB_URL) as store:
    store.setup()  # 幂等，创建表结构
    store.put(namespace, key, value)  # 写入
    item = store.get(namespace, key)  # 精确检索
    items = store.search(namespace)   # 按命名空间检索
```

**编译图时传入**：

```python
graph = builder.compile(checkpointer=checkpointer, store=store)
```

**节点中访问**：

```python
def node(state, runtime):
    store = runtime.store
    item = store.get(namespace, key)
```

未配置 embedding 索引时，`search()` 只能按命名空间和过滤条件检索；配置后支持语义检索。

---

### Q34【进阶】Runtime Context 的特点和使用方式是什么？

**参考答案：**

Runtime Context 仅对本次调用生效，不会被持久化，也不会在同一会话的下一次调用中自动恢复。

**使用步骤**：

1. 初始化状态图时使用 `context_schema` 定义上下文类型

2. 调用图时通过 `context` 参数传入

3. 节点中通过 `runtime.context` 访问

```python
@dataclass
class UserContext:
    username: str
    membership_level: str

builder = StateGraph(state_schema=OverAllState, context_schema=UserContext)
graph.invoke(input, config=config, context=UserContext(username="Alice", membership_level="VIP"))

# 节点中访问
def llm_node(state: OverAllState, runtime: Runtime[UserContext]) -> OverAllState:
    runtime_context = runtime.context
```

适合放入运行时上下文的信息：当前登录用户信息、请求来源、调用方标识、Trace ID、本次调用的功能开关。

---

### Q35【进阶】节点函数的完整形态是什么？有哪些参数？

**参考答案：**

```python
def node(state: State, config: RunnableConfig, runtime: Runtime[Context]) -> State:
    ...
```

四个参数：

- `state`（位置传参）：接收图状态

- `config`：`RunnableConfig` 实例，包含 `thread_id`、`recursion_limit`、`metadata`（含 `langgraph_step`）等

- `runtime`：运行时对象，可访问 `runtime.context`（上下文）和 `runtime.store`（长期记忆）

- `writer`：流式写入器

---

## 中断与人在环（HITL）

### Q36【基础】LangGraph 的两种中断机制是什么？有什么区别？

**参考答案：**

1. **动态中断**：在图的任意节点中调用 `interrupt()` 函数实现。可以放在代码任意位置，可以根据业务逻辑条件触发，是**动态**的。提供了人机交互接口，是**业务逻辑的一部分**。

2. **静态中断**：在编译或调用状态图时通过 `interrupt_before` 和 `interrupt_after` 参数设置断点。在运行前确定，不能根据业务逻辑条件触发，是**静态**的。主要用于调试，**不是业务逻辑的一部分**。

区别：动态断点能向调用者传递信息和接收反馈；静态断点只是暂停计算图的运行，不能向调用者传递信息也不能接收反馈。动态断点在超步内部中断，静态断点在超步边界中断。

---

### Q37【基础】如何启用和恢复动态中断？

**参考答案：**

**启用中断**：

1. 配置检查点存储器

2. 设置 `thread_id`

3. 在需要中断的位置调用 `interrupt()`

**恢复中断**：

- 基于相同的配置再次调用计算图

- 将输入替换为 `Command(resume=用户反馈)` 实例

```python
# 首次调用，触发中断
config = {"configurable": {"thread_id": "123"}}
interrupt_res = graph.invoke({}, config=config)
# 获取中断信息
prompt = interrupt_res['__interrupt__'][0].value
# 获取用户输入后恢复
resume_res = graph.invoke(Command(resume=user_input), config=config)
```

恢复后，`Command` 传递的反馈会作为 `interrupt()` 函数的返回值参与后续计算。整个被中断的节点函数会被重新执行。

---

### Q38【进阶】动态中断有哪些常见使用模式？

**参考答案：**

1. **基础 HITL 模式**：图触发一次中断，获取人类输入后继续执行。

2. **多个并行中断**：多个并行任务分别产生中断，根据中断 ID 接收各自的恢复数据。恢复时传入 `resume_map`（中断 ID 到恢复值的映射）。

3. **审批模式**：根据人类审批结果，使用 `Command(goto=...)` 决定后续执行路径。

4. **审核与编辑模式**：将模型生成的内容交给人类检查，允许人类直接修改后继续处理。

5. **工具执行审批模式**：在调用工具之前由人类确认是否允许执行，中断放在工具函数内部。

6. **单节点串行中断模式**：在同一个节点内多次触发中断，上一个中断恢复后才能触发下一个。

7. **人类输入验证模式**：对人类输入进行校验，不符合要求时再次中断并要求重新输入。

---

### Q39【进阶】动态中断有哪些使用规范？

**参考答案：**

1. **不要用** `try/catch` **包裹** `interrupt()` **调用**：中断通过抛出 `GraphInterrupt` 异常实现，被 catch 后运行时无法感知断点。

2. **不要更改单个节点内** `interrupt` **的调用顺序**：恢复运行时整个节点函数会重新执行，历史 resume 记录按顺序加载。如果中断恢复前后断点顺序或数量不一致，会导致语义混乱。

3. **不要在** `interrupt()` **中传递复杂类型**：`interrupt()` 的参数会经过 JSON 序列化传递。传递函数、类实例等不支持序列化的类型会抛出异常。应传递简单类型或仅包含基本数据类型的可序列化字典。

4. **断点之前的副作用操作必须是幂等的**：中断恢复时断点所在函数会被重复执行，如果断点之前存在不满足幂等性的副作用操作（如写数据库追加记录），会导致多次调用结果不一致。解决方案：使用幂等操作（如 upsert）、将副作用操作放在断点之后、或将副作用操作和断点置于不同节点。

---

### Q40【进阶】单节点串行中断的恢复机制是怎样的？

**参考答案：**

在同一个节点内多次调用 `interrupt()` 时：

1. 检查点存储器会记录历史的 resume 信息

2. LangGraph 运行时读取这些信息，在 `interrupt()` 函数中维护索引

3. 按照节点内调用 `interrupt()` 的顺序，逐个取出历史 resume 的值作为 `interrupt()` 的返回值

4. 已被恢复的 `interrupt()` 不会被重复触发

5. 当历史 resume 耗尽后，本次恢复运行时传入的 resume 会作为本次中断的返回值

6. 所有中断都触发并恢复后，计算图正常结束

关键约束：必须保证中断恢复前后的多次 `interrupt()` 相对顺序保持不变。不能基于可变状态条件性地跳过断点，不能基于不确定数据循环设置断点。

---

### Q41【进阶】静态断点的底层原理是什么？

**参考答案：**

1. 编译时设置的静态断点保存在编译图的 `interrupt_before_nodes` 和 `interrupt_after_nodes` 中。运行时采用调用参数优先、编译配置兜底的规则：调用时传入非空列表会完全覆盖编译配置。

2. `interrupt_before` 在超步的第一阶段检查：任务列表计算完成后、节点开始执行前。如果状态有变化且任务列表与 `interrupt_before` 列表存在交集，则抛出 `GraphInterrupt`。

3. `interrupt_after` 在超步的第三阶段检查：任务全部执行完成、写入应用到通道并创建检查点之后。如果状态有变化且任务列表与 `interrupt_after` 列表存在交集，则抛出 `GraphInterrupt`。

4. 如果 `node_a` 之后和 `node_b` 之前都设置了断点，只会中断一次，因为二者对应同一个超步边界。

恢复方式：传入相同配置并将 `None` 作为输入，再次调用计算图即可从断点位置继续运行。

---

## 工具节点

### Q42【基础】手动实现工具节点的基本流程是什么？

**参考答案：**

1. 使用 `@tool` 装饰器定义工具函数

2. 使用 `model.bind_tools(tools)` 让模型感知可用工具

3. 在 `llm_node` 中调用模型，返回 `AIMessage`（可能包含 `tool_calls`）

4. 在 `tool_node` 中：

    - 读取 `messages[-1].tool_calls`

    - 根据工具名称查找对应工具

    - 调用工具并封装结果为 `ToolMessage`（包含 `name`、`content`、`tool_call_id`）

5. 通过路由函数判断：有 `tool_calls` → `tool_node`；无 `tool_calls` → `END`

6. `tool_node` 执行完后回到 `llm_node`，形成 ReAct 循环

---

### Q43【进阶】`ToolNode` 相比手动实现有什么优势？

**参考答案：**

`ToolNode`（`langgraph.prebuilt.tool_node.ToolNode`）封装了实际项目需要的通用逻辑：

- 无效工具名处理

- 参数校验

- 异常处理

- 运行时参数注入

- `Command` 传播

- 多个工具调用的并行执行

手动实现按 `tool_calls` 顺序串行执行工具；`ToolNode` 在同步调用中可通过执行器并行处理，在异步调用中使用 `asyncio.gather()` 并发执行。

使用方式：

```python
from langgraph.prebuilt.tool_node import ToolNode
tool_node = ToolNode(tools=[get_weather, get_news])
builder.add_node("tool_node", tool_node)
```

---

### Q44【进阶】`ToolRuntime` 是什么？如何在工具中更新状态？

**参考答案：**

`ToolRuntime` 提供了在工具函数内部访问图运行时信息的能力，支持在工具执行时更新图状态。

在工具中更新状态的方式：通过 `ToolRuntime` 获取运行时上下文，在工具函数内部直接读写图状态，而不仅仅是返回字符串结果。这使得工具可以在执行过程中修改全局状态字段，实现更灵活的状态管理。

适合场景：工具执行后需要同时更新多个状态字段、工具需要根据运行时上下文决定行为、工具执行结果需要以结构化方式写入状态。

---

## 部署

### Q45【基础】LangGraph 本地部署需要哪些文件？`langgraph.json` 的作用是什么？

**参考答案：**

项目结构：

```text
project/
├── src
│   ├── __init__.py
│   └── agent.py
├── .env
└── langgraph.json
```

`langgraph.json` 是项目配置文件：

```json
{
  "dependencies": ["."],
  "graphs": {
    "graph": "./src/agent.py:graph"
  },
  "env": ".env"
}
```

- `dependencies`：本地服务的依赖项，`["."]` 表示从当前 conda 环境加载依赖

- `graphs`：计算图或 Agent 对象的映射，Key 是在 Studio 中显示的应用名称，Value 是应用实例路径（`文件路径:变量名`）

- `env`：环境变量文件路径

注意：`langgraph-cli` 启动的本地服务会管理检查点，代码中不要传递检查点存储器，否则启动时会报错。

---

### Q46【基础】如何启动 LangGraph 本地服务并对接 LangSmith？

**参考答案：**

**启动命令**：

```powershell
langgraph dev
```

**对接 LangSmith 的配置**：

1. 在 `.env` 文件中配置：

```text
LANGSMITH_API_KEY=xxx
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT="项目名称"
```

2. 启动后，在 LangSmith 云服务的 Studio 中可以调试图应用

3. Studio 支持查看图结构、运行图、查看中间状态、恢复中断等

**Windows 下的编码问题**：如果代码中有中文注释，可能遇到 `UnicodeDecodeError`。解决方法：设置环境变量 `$env:PYTHONUTF8 = "1"`，或永久修复 `conda env config vars set PYTHONUTF8=1`。

---

### Q47【进阶】如何对接 AgentChatUI？

**参考答案：**

1. **准备文件**：编写基于 `MessagesState` 的对话 Agent，使用 `create_react_agent` 或自定义 ReAct 循环

2. **更改** `langgraph.json`：将新的 Agent 注册到 graphs 映射中

3. **重启本地服务**：`langgraph dev`

4. **访问 AgentChatUI**：通过 LangSmith 云服务提供的 AgentChatUI 界面连接本地服务

5. **测试功能**：支持对话、工具调用（含 HITL 审批——同意调用、修改参数后调用、拒绝调用）、查看历史记录

---

## 流式执行

### Q48【基础】LangGraph 的两套流式执行 API 是什么？

**参考答案：**

1. `stream/astream`：获取执行过程中的业务数据或运行时数据。`stream` 是同步 API，`astream` 是异步 API。通过 `stream_mode` 选择消费内容。

2. `astream_events`：获取图运行过程中产生的 Runnable 标准事件（组件生命周期、父子调用关系、输入输出等）。

`invoke` 在内部会消费 `stream` 并把流式执行结果汇总为最终返回值。

---

### Q49【进阶】`stream_mode` 支持哪些模式？各自输出什么内容？

**参考答案：**

| 模式 | 输出内容 | 适用场景 |
| --- | --- | --- |
| `values` | 每个超步后的完整状态 | 需要完整状态快照 |
| `updates` | 节点产生的状态更新（增量） | 只关心节点输出变化 |
| `messages` | `messages` 状态字段的增量更新 | LLM 对话流式输出 |
| `checkpoints` | 检查点更新事件（需检查点存储器） | 持久化监控、中断调试 |
| `tasks` | 任务开始/结果事件（含触发通道、异常） | 运行时观测、任务追踪 |
| `debug` | `checkpoints` + `tasks` 的统一封装，附加超步编号、时间戳 | 调试排错 |
| `custom` | 节点/工具通过 `stream_writer` 主动写出的自定义数据 | 进度通知、阶段说明 |

从 LangGraph 1.1 开始支持两种输出格式版本：`v1`（默认）和 `v2`（统一返回 `StreamPart` 字典，包含 `type`、`ns`、`data` 三个字段）。

---

### Q50【进阶】`values` 模式和 `updates` 模式的输出有什么区别？

**参考答案：**

以 `START → node_a → node_b → END` 为例：

`values` **模式**——输出每个超步后的完整状态：

```text
('values', {'initial_state': '初始状态'})
('values', {'initial_state': '初始状态', 'node_a_output': '节点A的输出'})
('values', {'initial_state': '初始状态', 'node_a_output': '节点A的输出', 'node_b_output': '节点B的输出'})
```

`updates` **模式**——只输出节点产生的增量更新：

```text
('updates', {'node_a': {'node_a_output': '节点A的输出'}})
('updates', {'node_b': {'node_b_output': '节点B的输出'}})
```

`values` 适合需要完整状态快照的场景；`updates` 适合只关心节点输出变化的场景。

---

## 子图

### Q51【基础】LangGraph 中子图的两种嵌入方式是什么？

**参考答案：**

| 方式 | 用法 | 适用场景 | 通信方式 |
| --- | --- | --- | --- |
| 节点函数中调用子图 | 在节点函数内 `subgraph.invoke()` | 父子图状态完全隔离 | 手动做输入输出映射 |
| 子图直接作为父图节点 | `add_node("name", compiled_subgraph)` | 父子图共享状态字段 | 通过共享字段自动通信 |

方式一中，父图和子图使用不同的 State Schema，需要手动映射字段。方式二中，父图和子图使用相同的 State Schema，通过共享字段自动通信。

---

### Q52【进阶】子图的持久化策略有哪些？

**参考答案：**

当父图配置了 checkpointer 时：

1. **节点函数中调用子图**：子图如果没有独立配置 checkpointer，其内部执行不会被独立持久化。但 LangGraph 可以通过解析节点函数代码感知子图的存在，从而在父图检查点中记录子图的执行信息。调用子图时不要链式调用（如 `subgraph.invoke(...)["messages"][-1].content`），否则 LangGraph 无法感知子图。

2. **子图作为父图节点**：子图的执行会被父图的 checkpointer 自动持久化。子图检查点使用独立的命名空间（`checkpoint_ns`），格式为 `节点名:任务ID`。

**查看子图检查点**：

- 父图检查点的 `PregelTask` 的 `state` 字段中包含子图的 `checkpoint_ns`

- 可以使用该命名空间配置查询子图的检查点快照

---

### Q53【进阶】子图流式运行和动态路由如何实现？

**参考答案：**

**子图流式运行**：通过 `subgraphs=True` 参数在 `stream/astream` 中获取子图的流式输出。输出中会增加命名空间信息，用于区分事件来自哪个子图。

**子图动态路由**：子图内部可以使用 `Command(goto=..., graph=...)` 实现从子图向父图的跳转。`graph` 参数指定跳转发生在哪一层图中，例如从子图跳转到父图的某个节点。这使得子图可以在执行过程中根据条件将控制权交还给父图。

---

## 设计模式

### Q54【进阶】LangGraph 官方总结了哪些常用设计模式？

**参考答案：**

| 模式 | 图结构 | 运行时动态性 | 核心能力 |
| --- | --- | --- | --- |
| Prompt Chaining | 顺序链 | 低 | 静态边、条件边 |
| Parallelization | 固定 Fan-out/Fan-in | 低 | 并行超步、汇聚 |
| Routing | 条件分支 | 中 | 结构化输出、条件边 |
| Orchestrator-worker | 动态 Fan-out/Fan-in | 高 | Send、WorkerState、Reducer |
| Evaluator-optimizer | 反馈循环 | 中 | 条件边、循环、反馈状态 |
| Agent | 自主决策循环 | 最高 | MessagesState、工具调用、ToolNode |

---

### Q55【实战】Prompt Chaining 模式的核心思想和适用场景是什么？

**参考答案：**

**核心思想**：将复杂任务拆解为可独立验证的阶段，把每一阶段的结果记录下来向后传递。流程固定，后一节点依赖前一节点的结果。

**典型结构**：

```text
输入 → 任务A → 任务B → 任务C → 输出
```

也可以在中间加入"质量门控节点"（Gate）：

```text
生成笑话 → 检查是否合格
           ├─ 合格 → END
           └─ 不合格 → 改进笑话 → 最终润色 → END
```

**适用场景**：翻译→校对→润色、生成内容→检查一致性→修订、提取信息→分类→格式化、需求分析→生成代码→代码解释。

**优点**：执行过程稳定且易于调试。**缺点**：流程固定，无法处理未知数量或高度动态的任务。

---

### Q56【场景设计】设计一个支持人工审批的文档生成与审核系统，描述图结构和关键实现。

**参考答案：**

**图结构**：

```text
START → generate_node → review_node → END
                            ↑ (interrupt)
                            ↓ (人工审核)
                       approve/reject
```

**关键实现**：

1. `generate_node`：调用 LLM 生成文档内容，写入 state

2. `review_node`：使用 `interrupt()` 暴露生成内容给人工审核

```python
def review_node(state):
    reviewed = interrupt({
        "instruction": "请审核并修改文档",
        "document": state['document']
    })
    return {"reviewed_document": reviewed}
```

3. 配置 `checkpointer=InMemorySaver()` 确保中断可恢复

4. 调用方获取中断信息后展示给用户，用户审核修改后通过 `Command(resume=修改后内容)` 恢复

**注意事项**：

- `generate_node` 中的副作用操作必须在 `review_node` 的中断之前完成且幂等

- 审核内容通过 `interrupt()` 传递时必须是 JSON 可序列化的

- 多轮审核可使用单节点串行中断模式

---

### Q57【场景设计】如何用 LangGraph 实现 Map-Reduce 模式的批量文本处理？

**参考答案：**

**图结构**：

```text
START → [router_map (Send)] → mapper_node (并行N个实例) → reducer_node → END
```

**关键实现**：

1. **Map 阶段**——路由函数动态创建任务：

```python
def router_map(state):
    return [Send("mapper_node", {"input_value": v}) for v in state["input_values"]]
```

配置条件边：`builder.add_conditional_edges(START, router_map, path_map=["mapper_node"])`

2. **Mapper 节点**：接收独立的输入值，产生中间结果

```python
def mapper_node(state):
    # 处理单个输入
    return {"entries": [(word, 1) for word in state["input_value"].split()]}
```

3. **Reduce 阶段**：合并所有 mapper 的结果

```python
def reducer_node(state):
    # 归约合并
    return {"word_counts": reduce_dict}
```

4. **状态字段**：`entries` 使用 `Annotated[list, add]` 作为 Reducer，自动合并多个 mapper 的输出

5. **图连接**：

```python
builder.add_conditional_edges(START, router_map, path_map=["mapper_node"])
builder.add_edge("mapper_node", "reducer_node")
builder.add_edge("reducer_node", END)
```

注意：`display(graph)` 展示的是节点级计算图，实际运行时 `Send` 会根据输入数据动态创建多个 mapper 任务实例。

---

### Q58【场景设计】设计一个带工具调用重试和容错的 ReAct Agent。

**参考答案：**

**图结构**：

```text
START → llm_node → [router] → tool_node → llm_node (循环)
                       ↓
                      END (无 tool_calls)
```

**关键实现**：

1. **工具节点配置重试策略**：

```python
from langgraph.types import RetryPolicy
builder.add_node("tool_node", tool_node, retry_policy=RetryPolicy(max_attempts=3))
```

2. **工具调用失败处理**：工具返回包含错误信息的 `ToolMessage`，通过 SystemPrompt 引导模型重试：

```python
SystemMessage("如果工具调用失败，必须重新调用直至成功")
```

3. **递归限制保护**：

```python
graph.invoke(input, config={"recursion_limit": 25})
```

或使用 `RemainingSteps` 在路由函数中主动检测剩余步数，不足时优雅退出。

4. **使用 ToolNode 替代手动实现**：获得参数校验、异常处理、并行执行等能力。

5. **可选缓存**：对相同输入的工具调用配置 `CachePolicy` 避免重复计算。

---

## 附录：关键 API 速查表

| API / 概念 | 说明 |
| --- | --- |
| `StateGraph(state_schema, input_schema, output_schema, context_schema)` | 创建状态图 |
| `builder.add_node(name, func, retry_policy, timeout, error_handler, cache_policy, defer)` | 添加节点 |
| `builder.add_edge(source, target)` | 添加普通边 |
| `builder.add_conditional_edges(source, path, path_map)` | 添加条件边 |
| `builder.add_sequence(funcs)` | 添加顺序节点序列 |
| `builder.set_entry_point(node)` | 设置入口节点 |
| `builder.set_finish_point(node)` | 设置终止节点 |
| `builder.set_node_defaults(retry_policy=..., ...)` | 设置全图默认配置（≥1.2） |
| `builder.compile(checkpointer, store, cache, interrupt_before, interrupt_after)` | 编译状态图 |
| `graph.invoke(input, config, durability, context)` | 同步调用图 |
| `graph.stream(input, config, stream_mode, subgraphs)` | 同步流式调用 |
| `graph.astream(input, config, stream_mode, subgraphs)` | 异步流式调用 |
| `graph.get_state(config)` | 获取最新/指定检查点快照 |
| `graph.get_state_history(config)` | 获取历史检查点迭代器 |
| `graph.update_state(config, values, as_node)` | 基于历史检查点创建分叉 |
| `interrupt(value)` | 动态中断 |
| `Command(goto, update, graph, resume)` | 控制流跳转 + 状态更新 |
| `Send(node, arg)` | 动态扇出任务 |
| `Overwrite(value)` | 绕过 Reducer 直接覆盖 |
| `RetryPolicy(max_attempts, initial_interval, backoff_factor, max_interval, jitter, retry_on)` | 重试策略 |
| `TimeoutPolicy(run_timeout, idle_timeout)` | 超时策略（≥1.2） |
| `CachePolicy(key_func, ttl)` | 缓存策略 |
| `InMemorySaver()` | 内存检查点存储器 |
| `PostgresSaver.from_conn_string(url)` | PostgreSQL 检查点存储器 |
| `PostgresStore.from_conn_string(url)` | PostgreSQL 长期记忆存储器 |
| `RemainingSteps` | 剩余可用步数（托管值） |
| `MessagesState` | 预定义消息状态 |
| `ToolNode(tools)` | 预构建工具节点 |
| `add_messages` | 消息列表合并 Reducer |
| `InMemoryCache()` | 内存缓存后端 |
| `langgraph dev` | 启动本地开发服务器 |
