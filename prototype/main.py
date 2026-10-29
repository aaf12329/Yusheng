"""命令行聊天入口：编排提示词、会话与模型调用，不自动读写长期记忆。

函数结构与真实调用关系：
main()
├─ ChatSession() → reset() → common.read_text_file（启动时一次）
└─ 输入循环 → _handle_input(session, text)
             ├─ /clear → session.reset() → common.read_text_file
             └─ 普通输入或 /retry → session.reply(text) → core.call_model
数据流：初始 Prompt + 已完成对话 + 当前输入 → DeepSeek → 原始 assistant 消息 → 终端。
契约：reply 返回 core.call_model 的完整字典；只有成功的文本对话加入 messages。
失败输入保留为 pending_text 供手动重试；新输入替换它，不重复追加 user 消息。
运行：从仓库根目录执行 python -m prototype.main；仅导入本模块不会读文件或请求 API。
"""

from typing import Any

from prototype.Core.common import read_text_file
from prototype.Core.core import call_model
from prototype.Core.paths import INITIAL_PROMPT_FILE


# ① 会话状态与入口编排：允许调用共用层和模型功能层。
class ChatSession:
    """保存当前进程的消息和失败输入；供命令行入口使用，不写入磁盘。"""

    def __init__(self) -> None:
        """通过统一 reset 加载初始提示词并建立新会话。"""
        self.reset()

    def reset(self) -> None:
        """重新读取提示词并清空对话；读取失败时保留原会话。"""
        prompt = read_text_file(INITIAL_PROMPT_FILE)
        if not prompt.strip():
            raise ValueError("初始提示词为空；请补充 prototype/PromptSQL/initial_prompt.md。")
        self.messages: list[dict[str, Any]] = [{"role": "system", "content": prompt}]
        self.pending_text: str | None = None

    def reply(self, text: str | None = None) -> dict[str, Any]:
        """发送新输入或重试失败输入；成功后保存原始 assistant 消息并返回结果。"""
        if text is not None:
            if not text.strip():
                raise ValueError("请输入非空消息。")
            self.pending_text = text
        if self.pending_text is None:
            raise ValueError("当前没有待重试的消息。")
        user_message = {"role": "user", "content": self.pending_text}
        # 在临时请求列表中加入本轮输入，失败不会污染已完成的会话。
        result = call_model(self.messages + [user_message])
        if result["tool_calls"]:
            raise RuntimeError("模型请求了工具，但当前入口尚未接入工具执行；本轮未加入会话。")
        if not result["content"].strip():
            raise RuntimeError("模型未返回文本回复；本轮未加入会话，可手动重试。")
        self.messages.extend([user_message, result["message"]])
        self.pending_text = None
        return result


# ② 终端交互：只负责命令分派与显示，不在这里实现模型请求。
def _handle_input(session: ChatSession, text: str) -> bool:
    """处理一条输入并显示结果；由 main 调用，返回是否继续聊天。"""
    if text == "/exit":
        print("已退出。")
        return False
    if text == "/clear":
        session.reset()
        print("已清空当前对话并重新加载初始 Prompt。")
        return True
    if text.startswith("/") and text != "/retry":
        print("未知命令；可用命令：/exit、/clear、/retry。")
        return True
    result = session.reply(None if text == "/retry" else text)
    print(f"\n大肥鱼：{result['content']}\n")
    if result["finish_reason"] == "length":
        print("提示：本次回复因长度限制截断，可继续输入让大肥鱼接着说。")
    return True


# ③ 主流程：启动 → 输入 → 分派 → 显示；每轮失败后继续等待输入。
def main() -> int:
    """启动命令行聊天循环；返回进程退出码，由模块启动入口调用。"""
    try:
        session = ChatSession()
    except (OSError, ValueError) as exc:
        print(f"启动失败：{exc}；请检查初始 Prompt 文件。")
        return 1
    print("鱼生 · 大肥鱼 | DeepSeek Flash · 关闭思考 · 非流式")
    print("命令：/exit 退出，/clear 清空对话，/retry 重试失败输入。")
    print("当前对话仅保留在内存中；发送消息会调用 DeepSeek API。\n")
    while True:
        try:
            text = input("你：").strip()
            if text and not _handle_input(session, text):
                return 0
        except (EOFError, KeyboardInterrupt):
            print("\n已退出。")
            return 0
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"错误：{exc}")
            if session.pending_text is not None:
                print("可输入 /retry 重试；直接输入新消息会替换本次失败输入。")


if __name__ == "__main__":
    raise SystemExit(main())
