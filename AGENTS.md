# Yusheng · AI 接手入口

## 项目事实

- 项目名：鱼生 / Yusheng；陪伴角色名：大肥鱼 / Dafeiyu。
- 远程仓库：[aaf12329/Yusheng](https://github.com/aaf12329/Yusheng)，本地远程名为 `origin`。
- 目标：探索持续记忆、按需回忆与受控的自主活动。
- 当前阶段：Python 原型阶段，运行核心集中在 `prototype/Core/`，提示词与记忆目录位于其同级；已编写 JSON 记忆读写与 DeepSeek 调用模块，按当前指令未运行测试或真实 API 调用。
- 原型语言与环境：Python 3.12.0，所有者创建的 venv；项目内解释器为 `myvenv/Scripts/python.exe`，已安装 `openai==3.41.0`。
- 模型调用：`deepseek-flash`，关闭思考（`thinking.type="disabled"`），非流式（`stream=False`）。
- 记忆存储：JSON，由所有者明确指定；默认文件为 `prototype/Memory/memories.json`。读写函数分开，暂不实现并发写入。
- 提示词：`prototype/PromptSQL/initial_prompt.md`，按社区大肥鱼二创特征编写；来源见 `prototype/PromptSQL/README.md`，由调用方读取后作为 system 消息传入。
- 项目状态、调用方式与数据契约以 `README.md` 为准；入口编排、自动检索和工具循环尚未实现。
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

`prototype/Core/` 集中存放运行核心，独立行动的大肥鱼不得自行修改该目录及原型包加载代码。`prototype/Core/paths.py` 是文件位置的唯一地址簿；共用 I/O 与格式校验在 `prototype/Core/common.py`。三个功能模块互不导入，协作由后续入口编排。实际密钥只写本地 `.env`；记忆文件及环境均被忽略。

## 仓库卫生标准

新增文件、引入运行数据或提交前，必须读取并遵守 [CoMind《提交与协作规范》](../CoMind/01_AI项目协作参考/02_提交与协作规范.md) 的 **§07「仓库卫生」**。凭据、身份信息、聊天与记忆数据、环境、缓存、生成物和大文件的处理，以该节为唯一标准。

本项目的忽略规则维护在 `.gitignore`；引入新的数据目录或文件类型时，同步检查其忽略效果，并核对本次实际暂存的文件清单。
