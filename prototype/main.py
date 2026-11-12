"""命令行入口：读取记忆 → 读取 Prompt → 用户输入 → 模型调用 → 打印 → 保存。

函数结构与真实调用关系：
main()（每轮）
├─ _read_context → _checked_path → Tools_protect.check_tool_path
│                → File_read_and_write.Memory_json_read / file_read
│                → _validate_memory → _validate_embedding
├─ _reply → core.call_model
└─ _save_memory → _validate_memory → _validate_embedding
                → _checked_path → File_read_and_write.Memory_json_write
数据流：conversation.json + initial_prompt.md + user_input → DeepSeek
        → 原始 assistant 消息 → 终端 → conversation.json。
契约：user 与 assistant 各为独立记录，分别含 embedding / embedding_model；
      只保存完整成功轮次，system Prompt 不写入记忆，向量元数据不发送给聊天接口。
保存失败只重试本地写入，不重新请求模型；common 保留但不调用。
运行：从仓库根目录执行 python -m prototype.main；导入本模块不读写文件或请求 API。
"""

import math
from pathlib import Path
from typing import Any

from prototype.Core.File_read_and_write import Memory_json_read, Memory_json_write, file_read
from prototype.Core.Tools_protect import check_tool_path
from prototype.Core.core import call_model
from prototype.Core.paths import INITIAL_PROMPT_FILE, MEMORY_FILE


# ① 文件编排：保护检查与实际 I/O 分开，由入口串联。
def _checked_path(path: Path, operation: str) -> str:
    """检查路径并返回真实绝对路径；供本入口的读取和保存流程调用。"""
    result = check_tool_path(path, operation)
    if not result["allowed"]:
        raise PermissionError(str(result["reason"]))
    return str(result["path"])


def _validate_embedding(message: dict[str, Any], index: int) -> None:
    """检查向量与其生成模型是否配套且数值有限；由记忆校验调用，不生成向量。"""
    vector = message.get("embedding")
    model = message.get("embedding_model")
    if vector is None and model is None:
        return
    if not isinstance(model, str) or not model.strip():
        raise ValueError(f"第 {index} 条消息有向量时，embedding_model 必须填写生成模型名称。")
    if not isinstance(vector, list) or not vector:
        raise ValueError(f"第 {index} 条消息的 embedding 必须是非空数值列表，并与模型名称一起填写。")
    for value in vector:
        if type(value) not in (int, float) or (type(value) is float and not math.isfinite(value)):
            raise ValueError(f"第 {index} 条消息的 embedding 只能包含有限数值，不能包含布尔值。")


def _validate_memory(memory: Any) -> dict[str, Any]:
    """校验完整文本对话与向量字段，返回补齐字段的副本；由入口读取与保存流程共用。"""
    if not isinstance(memory, dict) or type(memory.get("version")) is not int or memory["version"] != 1:
        raise ValueError("聊天记忆必须是 version 为整数 1 的 JSON 对象。")
    messages = memory.get("messages")
    if not isinstance(messages, list):
        raise ValueError("聊天记忆需要 messages 列表；旧 memories 格式请保留另存，不自动转换。")
    if len(messages) % 2:
        raise ValueError("聊天记忆需要完整的 user/assistant 消息对；请修复后再继续。")
    records = []
    for index, message in enumerate(messages):
        expected_role = "user" if index % 2 == 0 else "assistant"
        if not isinstance(message, dict) or message.get("role") != expected_role:
            raise ValueError(f"第 {index + 1} 条消息的 role 应为 {expected_role}。")
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"第 {index + 1} 条消息的 content 必须是非空字符串。")
        if message.get("tool_calls") or message.get("function_call"):
            raise ValueError("当前聊天记忆只支持文本对话；工具调用记录需接入工具循环后处理。")
        _validate_embedding(message, index + 1)
        records.append({
            **message,
            "embedding": message.get("embedding"),
            "embedding_model": message.get("embedding_model"),
        })
    return {**memory, "messages": records}


def _read_context() -> tuple[dict[str, Any], str]:
    """每轮先读取聊天记忆，再读取初始 Prompt；由 main 调用。"""
    memory = _validate_memory(Memory_json_read(_checked_path(MEMORY_FILE, "read")))
    prompt = file_read(_checked_path(INITIAL_PROMPT_FILE, "read"))
    if not prompt.strip():
        raise ValueError("初始 Prompt 为空；请补充 prototype/PromptSQL/initial_prompt.md。")
    return memory, prompt


def _save_memory(memory: dict[str, Any]) -> bool:
    """保存本轮完整记忆；由 main 调用，失败时允许只重试文件写入。"""
    memory = _validate_memory(memory)
    while True:
        try:
            Memory_json_write(memory, _checked_path(MEMORY_FILE, "write"))
            return True
        except (OSError, ValueError, TypeError) as exc:
            print(f"回复已生成，但记忆尚未保存：{exc}")
        try:
            command = input("输入 /retry 重试保存，或 /exit 放弃未保存的本轮并退出：").strip()
            while command not in {"/retry", "/exit"}:
                command = input("此时仅支持 /retry 或 /exit：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n本轮未保存，已退出。")
            return False
        if command == "/exit":
            print("本轮未保存，已退出。")
            return False


# ② 模型编排：只发送文本消息，工具执行循环后续再接入。
def _reply(memory: dict[str, Any], prompt: str, text: str) -> dict[str, Any]:
    """去除向量元数据，再组装原始消息调用模型；由 main 调用，不修改记忆。"""
    history = [
        {key: value for key, value in record.items() if key not in {"embedding", "embedding_model"}}
        for record in memory["messages"]
    ]
    messages = [
        {"role": "system", "content": prompt},
        *history,
        {"role": "user", "content": text},
    ]
    result = call_model(messages)
    if result["tool_calls"]:
        raise RuntimeError("当前尚未接入模型工具循环；本轮工具请求未执行、未写入记忆。")
    if not result["content"].strip():
        raise RuntimeError("模型未返回文本回复；本轮未写入记忆，可重新输入。")
    return result


# ③ 简单对话循环：六步顺序直接体现在 main 中。
def main() -> int:
    """循环读文件、获取输入、调用模型、打印和保存；由模块启动入口调用。"""
    print("吸引子 Attractor · 大肥鱼 | 输入 /exit 退出；Ctrl+C 或输入结束也可退出。")
    print("每轮读取 Prompt 和聊天记忆，回复后保存；发送消息会调用 DeepSeek API。\n")
    while True:
        try:
            memory, prompt = _read_context()
        except (OSError, ValueError) as exc:
            print(f"读取失败：{exc}；请修复文件或路径配置后重新启动。")
            return 1
        try:
            text = input("你：").strip()
            if text == "/exit":
                print("已退出。")
                return 0
            if not text:
                continue
            result = _reply(memory, prompt, text)
            print(f"\n大肥鱼：{result['content']}\n")
            if result["finish_reason"] == "length":
                print("提示：回复因长度限制截断；可继续输入让大肥鱼接着说。")
            memory["messages"].extend([
                {"role": "user", "content": text, "embedding": None, "embedding_model": None},
                {**result["message"], "embedding": None, "embedding_model": None},
            ])
            if not _save_memory(memory):
                return 1
        except (EOFError, KeyboardInterrupt):
            print("\n已退出。")
            return 0
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"本轮失败：{exc}；本轮未保存，可重新输入。")


if __name__ == "__main__":
    raise SystemExit(main())
