# Yusheng · AI 接手入口

## 项目事实

- 项目名：鱼生 / Yusheng；陪伴角色名：大肥鱼 / Dafeiyu。
- 远程仓库：[aaf12329/Yusheng](https://github.com/aaf12329/Yusheng)，本地远程名为 `origin`。
- 目标：探索持续记忆、按需回忆与受控的自主活动。
- 当前阶段：Python 原型阶段，运行核心集中在 `prototype/Core/`，提示词与记忆目录位于其同级；已编写文件读写、路径保护、DeepSeek 调用及持久化命令行聊天，按当前指令未运行测试、程序或真实 API 调用。
- 原型语言与环境：Python 3.12.0，所有者创建的 venv；项目内解释器为 `myvenv/Scripts/python.exe`，已安装 `openai==3.41.0`。
- 模型调用：`deepseek-flash`，关闭思考（`thinking.type="disabled"`），非流式（`stream=False`）。
- 文件工具层：`prototype/Core/File_read_and_write.py`，仅定义 `Memory_json_write()`、`Memory_json_read()`、`file_read()`、`file_write()` 四个函数，不额外添加辅助函数；只承担文件后缀、基本输入类型和实际 I/O，聊天结构与向量校验在 `main.py`。后两者暂时只支持 `.md`，尚未注册给模型。
- 聊天记忆：JSON，由所有者明确指定；当前将记忆用于可恢复聊天，默认文件为 `prototype/Memory/conversation.json`，格式为 `{"version": 1, "messages": [...]}`。用户输入和模型回复各自独立记录，完整成功轮次一起保存，保留原始 assistant 字段。每条记录另含 `embedding` 与 `embedding_model`，初始均为 `null`；已有向量时记录数值数组及其实际生成模型，两字段必须一起填写。旧记录缺少字段时只在返回副本补齐，正常写入时才保存；聊天请求移除这两个本地字段，当前不生成向量或执行相似度检索。旧 `memories.json` 不读取、不转换、不覆盖；长期事实记忆另行设计，暂不实现并发写入。
- Markdown 数据示例路径登记为 `prototype/Memory/notes.md`，写入时才创建；初始 Prompt 默认从 `prototype/PromptSQL/initial_prompt.md` 读取。
- 提示词：`prototype/PromptSQL/initial_prompt.md`，按社区大肥鱼二创特征编写；来源见 `prototype/PromptSQL/README.md`，由调用方读取后作为 system 消息传入。
- 命令行入口：从仓库根目录执行 `myvenv/Scripts/python.exe -m prototype.main`；每轮读取聊天记忆、读取 Prompt、获取输入、调用 core、打印回复、写入记忆。支持 `/exit`；保存失败时可用 `/retry` 只重试写入，不重新请求模型。初始 Prompt 不写入聊天记忆，当前无清空聊天命令。
- 项目状态、调用方式与数据契约以 `README.md` 为准；命令行聊天入口已编写，尚未运行验证；自动检索和工具循环尚未实现。
- 初始化日期：2026-10-29。

## 参考入口

CoMind 与本仓库在本机上是同级目录。协作标准只引用 CoMind 中的唯一出处，不复制正文。

| 用途 | 路径 |
| --- | --- |
| 总入口与权限边界 | `../CoMind/AGENTS.md` |
| 开工前的子代理与效率判断 | `../CoMind/01_AI项目协作参考/00_子代理与效率.md` |
| 编程规范入口 | `../CoMind/01_AI项目协作参考/01_编程规范/代码规范.md` |
| Python 代码标准 | `../CoMind/01_AI项目协作参考/01_编程规范/语言规范/Python/代码规范.md` |
| 工程架构标准 | `../CoMind/01_AI项目协作参考/01_编程规范/工程架构规范.md` |
| LLM / Agent 专项标准 | `../CoMind/01_AI项目协作参考/01_编程规范/专项规范/LLM_Agent项目规范.md` |
| Git 权限、提交格式与检查 | `../CoMind/01_AI项目协作参考/02_提交与协作规范.md` |
| 项目接手手册写法 | `../CoMind/01_AI项目协作参考/03_项目接手手册_模板与写法.md` |
| 原始设想 | `../CoMind/02_思考与写作/seed/给大肥鱼完整的一生.md` |
| 整理文章 | `../CoMind/02_思考与写作/articles/给大肥鱼完整的一生.md` |

换机器后如 CoMind 不在同级目录，应先定位真实路径；不能把缺失的引用解释为权限放宽。

## 原型开发适用范围

本项目按 Python 工程项目开展原型开发。写代码前从上表的编程规范入口进入，并读取 Python、工程架构及 LLM / Agent 专项标准；规则正文以对应文件为准。

`prototype/Core/` 集中存放运行核心；`prototype/main.py` 是入口编排层，也属于运行内核。独立行动的大肥鱼不得自行修改这些文件及原型包加载代码。`prototype/Core/paths.py` 是文件位置与保护名单的地址簿；`common.py` 暂时保留，当前运行链路不导入、不调用。实际文件 I/O 在 `File_read_and_write.py`，聊天结构与向量校验在 `main.py`；`core.py` 只负责模型调用及本地 `.env` 密钥配置，模型参数手动修改该文件顶部常量。

路径保护在 `Tools_protect.py`，通过 `check_tool_path()` 返回允许或拒绝结果。入口先检查、再把允许的真实绝对路径交给文件读写层；两个功能模块互不导入。相对路径以项目根目录为基准；保护检查限制在项目内，禁止访问 Core、启动代码、凭据、Git、环境及依赖缓存。四个读写函数本身不执行保护名单检查，后续任何 LLM 文件工具执行入口必须先接入该检查。当前尚无模型工具注册与执行循环，路径检查不代表已有进程隔离。实际密钥只写本地 `.env`；聊天记录及环境均被忽略。

## 仓库卫生标准

新增文件、引入运行数据或提交前，必须读取并遵守 [CoMind《提交与协作规范》](../CoMind/01_AI项目协作参考/02_提交与协作规范.md) 的 **§07「仓库卫生」**。凭据、身份信息、聊天与记忆数据、环境、缓存、生成物和大文件的处理，以该节为唯一标准。

本项目的忽略规则维护在 `.gitignore`；引入新的数据目录或文件类型时，同步检查其忽略效果，并核对本次实际暂存的文件清单。
