# 鱼生 · Yusheng

**给大肥鱼完整的一生。**

*A full life for Dafeiyu.*

CH:探索 AI 的持续记忆、按需回忆与自主活动，给大肥鱼完整的一生。

EN:Exploring persistent memory, on-demand recall, and autonomous activities for an AI companion—a full life for Dafeiyu.

## 项目设想 / Vision

鱼生是一个探索 AI 持续记忆与日常活动的个人陪伴项目。希望大肥鱼能记得聊过的事情，把过去的经历带到下一天，也能在允许的范围内找一些自己想做的事情。

Yusheng is a personal AI companion project exploring persistent memory and everyday activities. It aims to help Dafeiyu recall past conversations, carry experiences into the next day, and choose activities within defined limits.

最初的设想来自 CoMind 中的[《给大肥鱼完整的一生》](https://github.com/aaf12329/CoMind/blob/main/02_%E6%80%9D%E8%80%83%E4%B8%8E%E5%86%99%E4%BD%9C/articles/%E7%BB%99%E5%A4%A7%E8%82%A5%E9%B1%BC%E5%AE%8C%E6%95%B4%E7%9A%84%E4%B8%80%E7%94%9F.html)。项目从保存经历开始，逐步尝试近期缓存、长期记忆、整理压缩与按需检索。原始记录保留，回忆中的重新表达与原始事实分开。

The idea began with the essay [“A Full Life for Dafeiyu”](https://github.com/aaf12329/CoMind/blob/main/02_%E6%80%9D%E8%80%83%E4%B8%8E%E5%86%99%E4%BD%9C/articles/%E7%BB%99%E5%A4%A7%E8%82%A5%E9%B1%BC%E5%AE%8C%E6%95%B4%E7%9A%84%E4%B8%80%E7%94%9F.html) in CoMind. The project starts with recording experiences, then explores recent context, long-term memory, consolidation, and retrieval. Original records are preserved separately from reconstructed recollections.

## 前身项目 / Predecessor projects

Yusheng 的前身项目是 **DeepSeek_port** 与 **My_Agent**，均可在 `history_code` 仓库中查看。

Yusheng's predecessor projects are **DeepSeek_port** and **My_Agent**, both available in the `history_code` repository.

- [DeepSeek_port](https://github.com/aaf12329/history_code/tree/main/DeepSeek_port)
- [My_Agent](https://github.com/aaf12329/history_code/tree/main/My_Agent)

## 当前状态 / Current status

**Python 原型阶段：代码、提示词和记忆目录均放在 `prototype/` 下。** 已编写 JSON 记忆读写和 DeepSeek 核心调用模块。使用所有者创建的 `myvenv`（Python 3.12.0），模型固定 `deepseek-flash`，关闭思考，非流式返回。按本次要求未运行测试、未进行真实 API 调用；尚未接入对话循环、自动检索或工具执行。

**Python prototype stage: code, prompts, and the memory directory live under `prototype/`.** JSON memory read/write and a DeepSeek adapter have been written. The owner's `myvenv` uses Python 3.12.0. The adapter fixes the model to `deepseek-flash`, disables thinking, and returns non-streaming responses. No tests or live API calls were run, as requested. Conversation orchestration, automatic retrieval, and tool execution are not implemented yet.

## 初步方向 / Initial direction

以下是后续方向；当前只提供独立模块，整体流程仍待实现和验证。

The following items describe future work; only standalone modules exist so far, and the full workflow remains to be implemented and validated.

| 方向 / Area | 目标 / Goal |
| --- | --- |
| 经历记录 / Experience recording | 保存对话与活动，重启后仍可读取。 / Persist conversations and activities across restarts. |
| 缓存与记忆 / Context and memory | 区分近期经历与长期记忆，探索整理和压缩方式。 / Separate recent experiences from long-term memory and explore consolidation. |
| 按需回忆 / On-demand recall | 在上下文预算内检索相关记忆，并能追溯原始记录。 / Retrieve relevant memories within a context budget while retaining source traceability. |
| 自主活动 / Autonomous activities | 逐步接入扩展，明确活动权限、资源预算与停止机制。 / Introduce extensions with explicit permissions, resource budgets, and stop controls. |

核心代码由人维护；运行中的大肥鱼不自行修改核心代码。记忆注入比例、活动频率和 token 预算均需通过实际运行确定。

Core code is maintained by humans; the running companion does not modify it autonomously. Memory allocation, activity frequency, and token budgets will be determined through experiments.

## 仓库结构 / Repository layout

```text
Yusheng/
├── README.md      项目说明与进度 / Overview and status
├── AGENTS.md      AI 接手与代码规范入口 / AI handover and coding-standard references
├── .gitignore     本地数据与生成物忽略规则 / Local data and generated-file exclusions
├── .env.example   本地密钥文件模板 / Local credential template
├── requirements.txt
└── prototype/
    ├── __init__.py
    ├── paths.py          路径地址簿 / File locations
    ├── common.py         共用 JSON I/O 与格式校验 / Shared I/O and validation
    ├── memory_read.py    记忆读取 / Memory reading
    ├── memory_write.py   记忆写入 / Memory writing
    ├── core.py           DeepSeek 核心调用 / DeepSeek adapter
    ├── PromptSQL/
    │   ├── initial_prompt.md  大肥鱼初始提示词 / Initial persona prompt
    │   └── README.md          提示词用途与社区参考 / Usage and community references
    └── Memory/
        └── .gitkeep           保留目录，实际记忆忽略 / Tracked placeholder only
```

真实聊天记录、记忆库、凭据和运行数据存放在本地，不提交到仓库。`prototype/Memory/memories.json` 首次写入时才创建；`prototype/Memory/` 仅跟踪占位文件。不会在导入模块时创建文件或发起网络请求。

Real conversations, memory stores, credentials, and runtime data stay local and are excluded from version control. `prototype/Memory/memories.json` is created on the first write; only the directory placeholder is tracked. Importing modules does not create files or make network requests.

## 原型用法 / Prototype usage

以下示例从仓库根目录执行。现有环境已安装 `openai==3.41.0`；其他环境可按 `requirements.txt` 安装依赖。本次未安装或修改环境。

Run the examples from the repository root. The existing environment has `openai==3.41.0`; other environments can install the dependencies from `requirements.txt`. This change did not install or modify the environment.

```powershell
.\myvenv\Scripts\python.exe
```

### 记忆格式与读写 / Memory format and I/O

记忆采用一个 JSON 文档，顶层为对象，`memories` 为条目列表。`version` 固定为整数 `1`；条目 `id` 为唯一正整数，从 `1` 开始；`content` 为非空字符串。可以添加其他 JSON 字段，读写时保留。

Memory is a JSON object containing a list of entries. `version` is the integer `1`; each entry has a unique positive integer `id` and a nonempty string `content`. Additional JSON fields are preserved.

```json
{
  "version": 1,
  "memories": [
    {"id": 1, "content": "今天开始搭建鱼生的 Python 原型。"}
  ]
}
```

```python
from prototype.memory_read import read_memory
from prototype.memory_write import write_memory

memory = read_memory()
next_id = max((item["id"] for item in memory["memories"]), default=0) + 1
memory["memories"].append({"id": next_id, "content": "今天开始搭建原型。"})
result = write_memory(memory)
print(result)  # {"path": 实际文件路径, "count": 当前条目数}
```

`read_memory()` 读取完整文档；文件不存在时返回空文档，文件损坏或格式错误则报错。`write_memory()` 校验并覆盖保存完整文档，不自动追加；采用 UTF-8 写入，先写同目录临时文件，再替换目标。读改写流程暂按单写入者使用，不支持并发合并。聊天流水与记忆库保持分开。

`read_memory()` returns the complete document, or an empty document if no file exists; malformed data raises an error. `write_memory()` validates and replaces the complete snapshot using a same-directory temporary file and UTF-8 encoding. It does not append automatically or coordinate concurrent writers. Conversation logs remain separate from the memory store.

### 模型调用 / Model calls

仅在尚无 `.env` 时，将根目录 `.env.example` 复制为 `.env`，手动填写 `DEEPSEEK_API_KEY=你的密钥`。当前加载器只读取该单行配置，支持成对单/双引号，不处理变量插值或行尾注释。不要提交 `.env`。

If `.env` does not exist, copy `.env.example` to `.env` and fill in `DEEPSEEK_API_KEY`. The loader reads this single-line setting, supports matching quotes, and does not support interpolation or inline comments. Never commit `.env`.

```python
from prototype.core import call_model
from prototype.common import read_text_file
from prototype.paths import INITIAL_PROMPT_FILE

result = call_model([
    {"role": "system", "content": read_text_file(INITIAL_PROMPT_FILE)},
    {"role": "user", "content": "你好！"},
])
print(result["content"])
```

初始提示词保存在 `prototype/PromptSQL/initial_prompt.md`，参考社区的大肥鱼 / 鲸鱼娘形象编写；来源和本项目的调整说明见 [prototype/PromptSQL/README.md](prototype/PromptSQL/README.md)。上例由调用方显式读取 Markdown 作为 system 消息，`core.py` 不自动插入提示词。

The initial prompt is stored in `prototype/PromptSQL/initial_prompt.md`, drawing on community whale-girl personas. Sources and Yusheng-specific choices are documented in [prototype/PromptSQL/README.md](prototype/PromptSQL/README.md). The caller explicitly loads the Markdown into a system message; `core.py` does not insert it automatically.

提示词中已加入用户指定的自主编写工具与运行内核边界，见「自主工具与运行内核」一节。当前尚未实现工具执行和运行时权限隔离，该约定仍是原型阶段的行为设定。

The prompt includes the owner's tool-building autonomy and runtime-core boundaries. Tool execution and runtime permission isolation are not implemented yet; this remains a behavioral specification for the prototype.

执行 `call_model()` 会向 DeepSeek 发送传入消息并产生 API 用量。模型与参数在 `core.py` 中固定：`deepseek-flash`、`thinking.type="disabled"`、`stream=False`，超时 60 秒，暂不自动重试。返回结构如下；`usage` 缺失时为 `None`，调用方需检查 `finish_reason` 是否表示正常结束或长度截断。

Calling `call_model()` sends the supplied messages to DeepSeek and incurs API usage. Settings are fixed in `core.py`: `deepseek-flash`, thinking disabled, non-streaming, a 60-second timeout, and no automatic retries. `usage` is `None` when absent; the caller must inspect `finish_reason` for completion or truncation.

| 返回字段 / Field | 类型 / Type | 含义 / Meaning |
| --- | --- | --- |
| `content` | `str` | 回复正文 / Response text |
| `reasoning` | `str` | 可选推理字段，无内容时为空 / Optional reasoning field, empty when absent |
| `usage` | `dict` 或 `None` | API 用量 / API usage |
| `tool_calls` | `list` | 工具调用请求，当前模块不执行 / Tool requests, not executed by this module |
| `finish_reason` | `str` | 本次生成的结束原因 / Generation stop reason |
| `message` | `dict` | 保留的原始 assistant 消息 / Preserved assistant message |

### 调用关系 / Call structure

```text
调用方 / Future orchestration entry
├── read_memory(path) → read_json → read_text_file
│                    → validate_memory
├── write_memory(memory, path) → validate_memory → write_json
└── call_model(messages) → _load_api_key → read_text_file
                       → DeepSeek chat.completions.create

paths.py → 为各模块提供文件位置 / File locations for all modules
```

读、写、模型三个功能模块互不导入。记忆不会自动送给模型，也不会从模型回复中自动提取；这些由后续入口编排。当前不提供工具注册和 Agent 循环。

The three functional modules do not import one another. Memory is not automatically injected into prompts or extracted from responses; a future entry point will coordinate that behavior. Tool registration and an agent loop are outside this initial implementation.

接口依据：[DeepSeek 首次调用](https://api-docs.deepseek.com/)、[思考模式开关](https://api-docs.deepseek.com/guides/thinking_mode/)、[Chat Completions 返回结构](https://api-docs.deepseek.com/api/create-chat-completion/)。
