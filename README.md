# 吸引子 · Attractor

**给大肥鱼完整的一生。**

*A full life for Dafeiyu.*

CH:探索持续记忆、按需回忆与受控自主活动的 AI 陪伴原型。

EN:An AI companion prototype exploring persistent memory, on-demand recall, and controlled autonomy.

## 项目设想 / Vision

吸引子（Attractor）是一个探索 AI 持续记忆与日常活动的个人陪伴项目。希望大肥鱼能记得聊过的事情，把过去的经历带到下一天，也能在允许的范围内找一些自己想做的事情。

Attractor is a personal AI companion project exploring persistent memory and everyday activities. It aims to help Dafeiyu recall past conversations, carry experiences into the next day, and choose activities within defined limits.

项目名取自动力系统中的“吸引子”，寓意记忆与互动不断累积，逐渐形成稳定的性格与自我。这是项目的设计寓意；陪伴角色仍叫大肥鱼（Dafeiyu）。项目于 2026-11-12 从“鱼生 / Yusheng”更名。

The name comes from attractors in dynamical systems, expressing the design ambition that accumulated memories and interactions gradually shape a stable personality and sense of self. The companion remains Dafeiyu. The project was renamed from Yusheng on 2026-11-12.

最初的设想来自 CoMind 中的[《给大肥鱼完整的一生》](https://github.com/aaf12329/CoMind/blob/main/02_%E6%80%9D%E8%80%83%E4%B8%8E%E5%86%99%E4%BD%9C/articles/%E7%BB%99%E5%A4%A7%E8%82%A5%E9%B1%BC%E5%AE%8C%E6%95%B4%E7%9A%84%E4%B8%80%E7%94%9F.html)。项目从保存经历开始，逐步尝试近期缓存、长期记忆、整理压缩与按需检索。原始记录保留，回忆中的重新表达与原始事实分开。

The idea began with the essay [“A Full Life for Dafeiyu”](https://github.com/aaf12329/CoMind/blob/main/02_%E6%80%9D%E8%80%83%E4%B8%8E%E5%86%99%E4%BD%9C/articles/%E7%BB%99%E5%A4%A7%E8%82%A5%E9%B1%BC%E5%AE%8C%E6%95%B4%E7%9A%84%E4%B8%80%E7%94%9F.html) in CoMind. The project starts with recording experiences, then explores recent context, long-term memory, consolidation, and retrieval. Original records are preserved separately from reconstructed recollections.

## 前身项目 / Predecessor projects

Attractor 的前身项目是 **DeepSeek_port** 与 **My_Agent**，均可在 `history_code` 仓库中查看。

Attractor's predecessor projects are **DeepSeek_port** and **My_Agent**, both available in the `history_code` repository.

- [DeepSeek_port](https://github.com/aaf12329/history_code/tree/main/DeepSeek_port)
- [My_Agent](https://github.com/aaf12329/history_code/tree/main/My_Agent)

## 当前状态 / Current status

**当前处于 Python 原型验证阶段。** 本阶段用于验证陪伴、记忆与受控自主活动的设计，独立运行版和 DSH 插件版均为后续交付目标。已编写命令行聊天、JSON 聊天记忆持久化、Markdown Prompt 读写、路径保护和 DeepSeek 调用。当前模型为 `deepseek-flash`，关闭思考，非流式返回；使用所有者创建的 Python 3.12.0 环境及 `openai==3.41.0`。按要求未运行测试、程序或真实 API 调用，运行效果尚未验证。

**Currently in the Python prototype validation stage.** This stage is intended to validate the design of companionship, memory, and controlled autonomy; the standalone and DSH plugin editions are future deliverables. Command-line chat, persistent JSON conversation memory, Markdown prompt I/O, path protection, and DeepSeek calls have been written. Defaults use `deepseek-flash` with thinking disabled and non-streaming output. The owner's environment uses Python 3.12.0 and `openai==3.41.0`. No tests, program execution, or live API calls were performed as requested; runtime behavior remains unverified.

当前“记忆”先用于恢复完整聊天。长期事实记忆、压缩检索、自主活动及模型工具注册与执行循环仍待实现。

Memory currently restores full conversations. Long-term factual memory, compression/retrieval, autonomous activities, and model tool registration/execution remain future work.

## 两种运行形态（规划） / Planned runtime forms

项目计划提供独立运行版与 [DeepSeek Harness（DSH）](https://github.com/deepseek-ai/deepseek-harness) 插件版。当前继续开发 Python 原型，现有命令行入口作为独立运行版的起点；DSH 插件尚未实现，具体插件接口、目标版本和加载方式待开发时确认。

The project will offer a standalone edition and a [DeepSeek Harness (DSH)](https://github.com/deepseek-ai/deepseek-harness) plugin edition. Development continues with the Python prototype, whose command-line entry is the starting point for the standalone edition. The DSH plugin is not implemented; its specific plugin interface, target version, and loading mechanism will be confirmed during development.

| 形态 / Form | 职责 / Responsibility | 状态 / Status |
| --- | --- | --- |
| 独立运行版 / Standalone | 自行启动并管理对话循环、输入输出及模型调用。 / Own startup, the conversation loop, I/O, and model calls. | 已编写命令行原型，尚未运行验证。 / CLI prototype written, runtime unverified. |
| DSH 插件版 / DSH plugin | 通过 DSH 的插件接口接收消息、返回回复并接入宿主生命周期。 / Receive messages, return replies, and integrate with the host lifecycle through its plugin interface. | 待确认 DSH 接口后设计实现。 / Design and implementation pending confirmation of the DSH interface. |

实现方向是共用记忆、Prompt、路径保护等核心逻辑，为两种形态分别提供入口适配。模型调用由独立版直接管理，插件版是否使用宿主提供的调用能力，要按 DSH 接口决定。两份交付物优先从同一份核心代码构建；运行数据默认各自保存，暂不设计跨进程共享写入。当前目录结构和现有调用链保持原型状态，尚未拆出共享包或插件目录。

The intended design shares core memory, prompt, and path-protection logic with a separate entry adapter for each form. The standalone edition manages model calls directly; whether the plugin uses host-provided model access depends on DSH's interface. Prefer building both deliverables from one core codebase. Runtime data stays separate by default, with no cross-process shared writes planned. The current prototype layout and call chain remain in place; no shared package or plugin directory has been extracted yet.

## 仓库结构 / Repository layout

```text
<project-root>/
├── README.md
├── AGENTS.md
├── .gitignore
├── .env.example
├── requirements.txt
├── Copolient.png
└── prototype/
    ├── __init__.py
    ├── main.py                    对话循环 / Conversation orchestration
    ├── PromptSQL/
    │   ├── initial_prompt.md      初始 Prompt / Initial prompt
    │   └── README.md              用途与参考 / Usage and sources
    ├── Memory/
    │   └── .gitkeep               实际数据忽略 / Runtime data ignored
    └── Core/
        ├── __init__.py
        ├── File_read_and_write.py JSON 记忆与 Markdown Prompt 读写 / File I/O
        ├── Tools_protect.py       路径保护名单检查 / Protected-path checks
        ├── core.py                模型调用核 / Model adapter
        ├── paths.py               路径与保护名单 / Paths and protected lists
        └── common.py              保留，不调用 / Retained, currently unused
```

`Core/`、启动入口及包加载代码由人维护，运行中的大肥鱼不得自主修改。独立扩展放在内核之外。真实聊天记录、记忆、凭据和运行数据仅存本地，不提交到 Git；导入模块不会创建数据文件或请求模型。

The core, startup entry, and package-loading code are maintained by humans and are not modified autonomously by the companion. Extensions belong outside the core. Conversations, memories, credentials, and runtime data stay local and are excluded from Git. Importing modules does not create data files or call the model.

## 启动 / Run

从仓库根目录执行。本机目录仍为 `Yusheng/`，本次更名保留现有目录与虚拟环境位置。仅在没有 `.env` 时，将 `.env.example` 复制为 `.env`，填写 `DEEPSEEK_API_KEY`，不要提交密钥。现有环境无需本次安装；其他环境可按 `requirements.txt` 安装依赖。

Run from the repository root. The local folder remains `Yusheng/`, preserving the existing directory and virtual environment locations. If `.env` does not exist, copy `.env.example` to `.env` and fill in `DEEPSEEK_API_KEY`. Never commit credentials. The existing environment needs no installation for this change; other environments can install from `requirements.txt`.

```powershell
.\myvenv\Scripts\python.exe -m prototype.main
```

每轮执行：读取记忆 → 读取 Prompt → 获取输入 → 调用 core → 打印回复 → 写入记忆。请求包含当前 Prompt、已保存历史和本轮 user 消息，成功后保存原始 assistant 消息。重新启动会恢复历史，修改 Prompt 在下一轮读取时生效；system Prompt 不写入聊天记忆。

Each turn reads memory and the prompt, accepts input, calls the model, prints the reply, and saves memory. Requests include the current prompt, saved history, and new input. Successful turns preserve the original assistant message. Restarts restore history, and prompt edits take effect on the next read. The system prompt is not stored in conversation memory.

- `/exit`、Ctrl+C 或输入结束可退出；空输入跳过。 / Exit with `/exit`, Ctrl+C, or end-of-input; empty input is skipped.
- 请求失败不保存本轮，可以重新输入；不自动重试模型请求。 / Failed requests are not saved; enter the message again to retry.
- 保存失败时暂停对话，`/retry` 只重试写入；`/exit` 放弃未保存的本轮并退出。 / If saving fails, `/retry` retries only the write; `/exit` leaves the turn unsaved and exits.
- 长度截断的文本回复提示并保存；上下文暂不压缩或裁剪，按单进程、单写入者使用。 / Truncated text replies are retained with a notice. Context is not compressed or trimmed; use a single process/writer.

## 文件格式与读写 / File format and I/O

默认聊天记忆为 `prototype/Memory/conversation.json`，首次成功写入时创建。旧 `memories.json` 保留原样，当前入口不读取、转换或覆盖它；聊天记录与后续长期事实记忆分开。

The conversation store is `prototype/Memory/conversation.json`, created on the first successful save. The old `memories.json` is left untouched and is not loaded or converted. Conversation records remain separate from future long-term factual memory.

```json
{
  "version": 1,
  "messages": [
    {
      "role": "user",
      "content": "你好！",
      "embedding": null,
      "embedding_model": null
    },
    {
      "role": "assistant",
      "content": "你好，我是大肥鱼。",
      "embedding": null,
      "embedding_model": null
    }
  ]
}
```

`version` 必须为整数 `1`；用户输入和模型回复各为一条独立记录，按顺序交替保存完整成功轮次。每条正文为非空字符串，保留原始 assistant 的额外字段。每条记录分别拥有 `embedding` 和 `embedding_model`，调用聊天接口时移除这两个本地字段，只传消息本身。当前只支持文本聊天，不接受未处理的工具调用记录；格式错误报错，不当作空库覆盖。

`version` is the integer `1`. Each user input and assistant reply is a separate record; complete successful turns are saved in order, preserving extra assistant fields. Each record has its own `embedding` and `embedding_model`. Both local fields are removed before sending messages to the chat API. Only text chat is supported; unresolved tool calls and malformed history raise errors rather than becoming an empty store.

| 向量字段 / Embedding field | 含义 / Meaning |
| --- | --- |
| `embedding` | 当前为 `null`；生成后保存非空数值数组。 / Currently `null`; later a nonempty numeric vector. |
| `embedding_model` | 当前为 `null`；有向量时记录实际生成该向量的模型名称或版本。 / Currently `null`; identifies the model/version that produced the stored vector. |

两个字段一起为空，或一起填写；向量不接受非有限数值或布尔值。入口读取记录后统一校验；旧记录缺少字段时，在校验返回的副本中补为 `null`，正常写入时才保存到磁盘。当前不生成向量、不调用 embedding 服务、不执行相似度检索。以后更换向量模型时，保留旧向量对应的模型标识，并按模型与向量维度区分比较。

Both fields are null together or populated together. Vector values must be finite numbers, not booleans. The entry validates loaded records, filling missing fields with nulls in the returned copy; these reach disk only on a normal write. No embedding generation, service calls, or similarity retrieval are implemented. When changing embedding models, retain each stored vector's producer identity and compare compatible models and dimensions.

| 函数 / Function | 行为与返回 / Behavior and return |
| --- | --- |
| `Memory_json_read(path=MEMORY_FILE)` | 读取记忆，缺失返回 `{"version": 1, "messages": []}`。 / Read memory, or an empty store if missing. |
| `Memory_json_write(memory, path=MEMORY_FILE)` | 序列化并覆盖 JSON，返回 `{"path": str, "count": 消息数}`。 / Serialize and replace JSON; count is the number of messages. |
| `file_read(path)` | 读取 `.md` 正文，返回 `str`；缺失报错。 / Read Markdown text; missing files raise an error. |
| `file_write(path, content)` | 覆盖 `.md`，返回 `{"path": str, "characters": int}`。 / Replace Markdown text and return its character count. |

`File_read_and_write.py` 仅定义上面四个函数，各自直接完成读写，不额外定义辅助函数。路径保护由 `Tools_protect.py` 负责，聊天结构与向量校验由 `main.py` 负责。读取兼容 UTF-8/BOM 和 GB18030；写入使用 UTF-8、同目录临时文件和原子替换，按需创建父目录，不自动合并或处理并发。Markdown 不额外解析，不自动追加换行。

`File_read_and_write.py` defines only the four functions above, with I/O implemented directly inside them. `Tools_protect.py` handles path protection, while `main.py` validates conversation structure and embeddings. Reading supports UTF-8/BOM and GB18030. Writes use UTF-8 and a same-directory temporary file, creating parent directories as needed without merging or concurrency coordination. Markdown is plain text, with no automatic newline.

## 路径保护 / Path protection

`Tools_protect.check_tool_path(path, operation)` 只检查路径，返回 `{"allowed": bool, "path": str, "reason": str}`。相对路径以项目根目录为基准；解析真实路径后检查范围和保护名单，解析失败时 `path` 为空。

`Tools_protect.check_tool_path(path, operation)` returns an allow/deny result with a resolved path and reason. Relative paths use the project root. The check resolves the path before enforcing boundaries and protected lists; an unresolvable path is returned as an empty string.

保护名单集中在 `paths.py`：Core、启动入口、包加载代码、Git、环境和依赖缓存禁止工具读写，`.env` 凭据同样禁止访问。当前入口在读取与保存前调用检查；后续 LLM 文件工具入口必须先检查，再把通过的真实绝对路径交给读写函数。

Protected lists live in `paths.py`: the core, startup/package-loading code, Git, environments, dependency caches, and `.env` credentials are unavailable to file tools. The entry checks before reading or saving. Future LLM file-tool dispatch must also check first, then pass the approved absolute path to the I/O function.

四个读写函数只负责文件后缀、基本输入类型和 I/O，不自行调用保护模块或校验聊天业务结构。以下展示先检查、再读取的入口编排；写入时使用 `"write"` 检查。`MARKDOWN_FILE` 是忽略目录下可选的 `Memory/notes.md` 示例路径。

The four I/O functions handle suffixes, basic input types, and I/O without importing protection or validating conversation semantics. The example shows entry-level checks before reading; use `"write"` before writing. `MARKDOWN_FILE` optionally points to the ignored `Memory/notes.md` example location.

```python
from prototype.Core.File_read_and_write import file_read
from prototype.Core.Tools_protect import check_tool_path
from prototype.Core.paths import INITIAL_PROMPT_FILE

check = check_tool_path(INITIAL_PROMPT_FILE, "read")
if not check["allowed"]:
    raise PermissionError(check["reason"])
prompt = file_read(check["path"])
```

这些是文件操作前的应用层检查；模型工具执行尚未接入，也不提供进程隔离。

These are application-level checks before file operations. Model tool execution is not connected, and process isolation is not provided.

## 模型调用与模块关系 / Model calls and module relationships

`core.py` 只负责模型请求及本地 `.env` 密钥配置。手动修改文件顶部的 `MODEL`、`BASE_URL`、`THINKING_TYPE`、`TIMEOUT` 调整参数；当前关闭思考、非流式、超时 60 秒且不自动重试。密钥加载器读取 UTF-8/BOM `.env` 中的单行 `DEEPSEEK_API_KEY`，支持成对引号，不处理插值或行尾注释。执行 `call_model()` 会产生实际 API 用量。

`core.py` handles model requests and local `.env` configuration. Edit `MODEL`, `BASE_URL`, `THINKING_TYPE`, and `TIMEOUT` at the top to adjust settings. Defaults disable thinking, use non-streaming output, set a 60-second timeout, and disable retries. The UTF-8/BOM key loader supports matching quotes, with no interpolation or inline comments. Calling `call_model()` incurs API usage.

| 返回字段 / Field | 类型 / Type | 含义 / Meaning |
| --- | --- | --- |
| `content` | `str` | 回复正文 / Response text |
| `reasoning` | `str` | 可选推理内容，无内容为空 / Optional reasoning, empty when absent |
| `usage` | `dict` 或 `None` | 原始 API 用量 / API usage |
| `tool_calls` | `list` | 工具请求，当前不执行 / Tool requests, currently not executed |
| `finish_reason` | `str` | 结束原因 / Stop reason |
| `message` | `dict` | 原始 assistant 消息 / Original assistant message |

```text
main（每轮 / each turn）
├── _read_context
│   ├── Tools_protect.check_tool_path → 允许路径 / approved path
│   └── File_read_and_write.Memory_json_read / file_read
│       → _validate_memory → _validate_embedding
├── 获取输入 / input
├── _reply → core.call_model → DeepSeek
├── 打印回复 / print
└── _save_memory
    ├── _validate_memory → _validate_embedding
    ├── Tools_protect.check_tool_path → 允许路径 / approved path
    └── File_read_and_write.Memory_json_write

paths.py → 路径与保护名单 / paths and protected lists
common.py → 保留，不在运行链路中 / retained, not used by the runtime
```

三个功能模块互不导入，由 main 编排。初始 Prompt 来源与项目设定见 [PromptSQL 说明](prototype/PromptSQL/README.md)。

The three functional modules do not import one another; main coordinates them. Prompt sources and project-specific behavior are documented in the [PromptSQL notes](prototype/PromptSQL/README.md).

接口依据：[DeepSeek 首次调用](https://api-docs.deepseek.com/)、[思考模式开关](https://api-docs.deepseek.com/guides/thinking_mode/)、[Chat Completions 返回结构](https://api-docs.deepseek.com/api/create-chat-completion/)。
