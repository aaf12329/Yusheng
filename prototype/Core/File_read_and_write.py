"""文件读写层：JSON 聊天记忆与 Markdown Prompt，不导入模型核或保护模块。

函数结构与真实调用关系：
├─ Memory_json_read(path) → _file_path → _read_text → json.loads → _validate_memory
├─ Memory_json_write(memory, path) → _file_path → _validate_memory → json.dumps → _write_text
├─ file_read(path) → _file_path → _read_text
└─ file_write(path, content) → _file_path → _write_text
调用：入口先通过 Tools_protect 检查路径，再调用四个公开读写函数；common 暂不使用。
数据流：.json ↔ {"version": 1, "messages": [原始 user/assistant 消息]}；.md ↔ str。
契约：JSON 读返回完整文档，缺失返回空库；写返回 {"path": str, "count": 消息数}。
      Markdown 读返回 str，缺失报错；写返回 {"path": str, "characters": 字符数}。
写入完整覆盖、UTF-8 原子替换、单写入者；不自动迁移旧 memories 格式。
本层只检查文件类型与数据格式，路径权限必须由调用入口先行检查。
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from prototype.Core.paths import MEMORY_FILE, PROJECT_ROOT


# ① 私有 I/O 与格式处理：公开函数共享这些实现。
def _file_path(path: Path | str, suffix: str) -> Path:
    """统一解析读写路径并检查文件后缀；供本模块四个公开函数调用。"""
    path = Path(path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path = path.resolve()
    if path.suffix.lower() != suffix:
        raise ValueError(f"此函数仅支持 {suffix} 文件；请检查文件后缀。")
    return path


def _read_text(path: Path) -> str:
    """读取 UTF-8/BOM 文本并兼容旧 GB18030；供 JSON 和 Markdown 读取共用。"""
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("gb18030")


def _write_text(path: Path, content: str) -> None:
    """先写同目录临时文件，再原子替换；供 JSON 与 Markdown 写入共用。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _validate_memory(memory: Any) -> dict[str, Any]:
    """校验完整文本对话且保留消息额外字段；由 JSON 读写共用。"""
    if not isinstance(memory, dict) or type(memory.get("version")) is not int or memory["version"] != 1:
        raise ValueError("聊天记忆必须是 version 为整数 1 的 JSON 对象。")
    messages = memory.get("messages")
    if not isinstance(messages, list):
        raise ValueError("聊天记忆需要 messages 列表；旧 memories 格式请保留另存，不自动转换。")
    if len(messages) % 2:
        raise ValueError("聊天记忆需要完整的 user/assistant 消息对；请修复后再继续。")
    for index, message in enumerate(messages):
        expected_role = "user" if index % 2 == 0 else "assistant"
        if not isinstance(message, dict) or message.get("role") != expected_role:
            raise ValueError(f"第 {index + 1} 条消息的 role 应为 {expected_role}。")
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"第 {index + 1} 条消息的 content 必须是非空字符串。")
        if message.get("tool_calls") or message.get("function_call"):
            raise ValueError("当前聊天记忆只支持文本对话；工具调用记录需接入工具循环后处理。")
    return memory


# ② 四个公开入口：只承担记忆 JSON 与 Prompt Markdown 的读写。
def Memory_json_read(path: Path | str = MEMORY_FILE) -> dict[str, Any]:
    """读取并校验聊天记忆；由入口在路径检查通过后调用，文件缺失返回空库。"""
    path = _file_path(path, ".json")
    try:
        memory = json.loads(_read_text(path))
    except FileNotFoundError:
        return {"version": 1, "messages": []}
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError(f"聊天记忆 JSON 无法解析：{path}；请修正格式或从备份恢复。") from exc
    return _validate_memory(memory)


def Memory_json_write(memory: dict[str, Any], path: Path | str = MEMORY_FILE) -> dict[str, Any]:
    """校验并原子覆盖完整聊天记忆；由入口在路径检查通过后调用。"""
    path = _file_path(path, ".json")
    memory = _validate_memory(memory)
    content = json.dumps(memory, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    _write_text(path, content)
    return {"path": str(path), "count": len(memory["messages"])}


def file_read(path: Path | str) -> str:
    """读取 .md 正文；由入口在路径检查通过后调用，文件缺失时报错。"""
    return _read_text(_file_path(path, ".md"))


def file_write(path: Path | str, content: str) -> dict[str, Any]:
    """UTF-8 原子覆盖 .md 正文；由入口在路径检查通过后调用。"""
    path = _file_path(path, ".md")
    if not isinstance(content, str):
        raise ValueError("Markdown 正文 content 必须是字符串。")
    _write_text(path, content)
    return {"path": str(path), "characters": len(content)}
