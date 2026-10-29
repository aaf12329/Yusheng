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

## 当前状态 / Current status

**筹备阶段：已完成本地仓库初始化，原型使用 Python，尚无可运行程序。** Python 环境由所有者创建，具体版本与路径待确认；模型服务、存储方案与硬件配置尚未确定。

**Planning stage: the local repository has been initialized, and the prototype will use Python; no runnable application exists yet.** The owner is setting up the Python environment; its version and path are pending confirmation. The model provider, storage, and hardware remain undecided.

## 初步方向 / Initial direction

以下是待实现、待验证的方向，不代表已有功能。

The following items are planned explorations, not implemented features.

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
└── .gitignore     本地数据与生成物忽略规则 / Local data and generated-file exclusions
```

后续实现随技术方案确定再加入。真实聊天记录、记忆库、凭据和运行数据存放在本地，不提交到仓库。

Implementation files will be added once the technical approach is chosen. Real conversations, memory stores, credentials, and runtime data stay local and are excluded from version control.
