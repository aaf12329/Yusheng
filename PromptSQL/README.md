# PromptSQL · 提示词文件

`initial_prompt.md` 保存发给模型的初始系统提示词。`PromptSQL` 按所有者指定命名，目前是 Markdown 提示词目录，不使用 SQL 数据库。

`initial_prompt.md` contains the initial system prompt. The directory name follows the owner's choice; prompts are Markdown files, with no SQL database involved.

## 社区参考 / Community references

查阅日期：2026-10-29。以下为作者各自项目中的社区二创设定，不代表统一的官方人设。本项目参考其中的鲸鱼娘、白饭、俏皮嘴硬和偶尔摸鱼等特征，重新编写文本；记忆真实性、工具能力和资源边界结合鱼生当前原型补充。

Consulted on 2026-10-29. These are community interpretations for their respective projects, not a canonical official persona. Yusheng's prompt is newly written, drawing on shared traits and adding behavior suited to the current memory and tool capabilities.

- [Kaalia0912 / dsh-whale-musume-persona](https://github.com/Kaalia0912/dsh-whale-musume-persona)：鲸鱼娘的性格和语气参考。
- [YunYueSama / codex-deepseek-pet · 角色设定](https://github.com/YunYueSama/codex-deepseek-pet/blob/main/docs/%E8%A7%92%E8%89%B2%E8%AE%BE%E5%AE%9A.md)：贪吃、爱面子、日常交流与认真工作的平衡参考。

来源说明留在本文件；调用时仅读取 `initial_prompt.md` 的正文。核心模块仍由调用方传入 `messages`，不会自动加载本目录。

Only the contents of `initial_prompt.md` should be sent as the system prompt. Source notes stay here. The core adapter still accepts caller-supplied `messages`; it does not automatically load prompts.
