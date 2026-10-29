# PromptSQL · 提示词文件

本目录位于 `prototype/PromptSQL/`，与原型代码、`prototype/Memory/` 一起维护；项目当前处于 Python 原型阶段。

This directory lives at `prototype/PromptSQL/` alongside the Python prototype code and `prototype/Memory/`.

`initial_prompt.md` 保存发给模型的初始系统提示词。`PromptSQL` 按所有者指定命名，目前是 Markdown 提示词目录，不使用 SQL 数据库。

`initial_prompt.md` contains the initial system prompt. The directory name follows the owner's choice; prompts are Markdown files, with no SQL database involved.

## 社区参考 / Community references

查阅日期：2026-10-29。以下为作者各自项目中的社区二创设定，不代表统一的官方人设。本项目参考其中的鲸鱼娘、白饭、俏皮嘴硬和偶尔摸鱼等特征，重新编写文本；记忆真实性、工具能力和资源边界结合鱼生当前原型补充。

Consulted on 2026-10-29. These are community interpretations for their respective projects, not a canonical official persona. Yusheng's prompt is newly written, drawing on shared traits and adding behavior suited to the current memory and tool capabilities.

- [Kaalia0912 / dsh-whale-musume-persona](https://github.com/Kaalia0912/dsh-whale-musume-persona)：鲸鱼娘的性格和语气参考。
- [YunYueSama / codex-deepseek-pet · 角色设定](https://github.com/YunYueSama/codex-deepseek-pet/blob/main/docs/%E8%A7%92%E8%89%B2%E8%AE%BE%E5%AE%9A.md)：贪吃、爱面子、日常交流与认真工作的平衡参考。

来源说明留在本文件；调用时仅读取 `initial_prompt.md` 的正文。核心模块仍由调用方传入 `messages`，不会自动加载本目录。

Only the contents of `initial_prompt.md` should be sent as the system prompt. Source notes stay here. The core adapter still accepts caller-supplied `messages`; it does not automatically load prompts.

## 项目内自主扩展约定 / Project-specific autonomy

`initial_prompt.md` 的「自主工具与运行内核」一节来自所有者于 2026-10-29 的明确指示，定义自主编写工具与独立行动的内核边界，不属于引用的社区角色设定。当前原型尚未实现工具执行、权限隔离或内核写入保护；提示词约定不等于这些机制已经实现。

The autonomy section follows the owner's explicit instruction on 2026-10-29 and is specific to Yusheng. Tool execution, permission isolation, and runtime write protection are not implemented yet; the prompt states the intended behavior rather than enforcing it in code.
