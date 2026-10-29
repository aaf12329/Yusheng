"""文件读写层：仅四个函数，负责 JSON 聊天记忆与 Markdown Prompt 的实际 I/O。

函数结构与真实调用关系：
├─ Memory_json_read(path) → 文件读取 → 文本解码 → json.loads
├─ Memory_json_write(memory, path) → json.dumps → 临时文件 → 原子替换
├─ file_read(path) → 文件读取 → 文本解码
└─ file_write(path, content) → 临时文件 → 原子替换
调用：入口先通过 Tools_protect 检查路径，再调用本层；common 暂不使用。
数据流：.json ↔ 聊天记忆文档；.md ↔ str。
契约：JSON 读返回对象，缺失返回空库；写返回 {"path": str, "count": 消息数}。
      Markdown 读返回 str，缺失报错；写返回 {"path": str, "characters": 字符数}。
本层检查文件后缀和基本输入类型；聊天结构与向量字段由入口校验。
按当前四函数约定，各函数内直接完成 I/O；UTF-8 原子覆盖，单写入者。
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from prototype.Core.paths import MEMORY_FILE, PROJECT_ROOT


def Memory_json_read(path: Path | str = MEMORY_FILE) -> dict[str, Any]:
    """读取 JSON 对象；由入口在路径检查后调用，结构校验由入口负责。"""
    path = Path(path)
    path = (path if path.is_absolute() else PROJECT_ROOT / path).resolve()
    if path.suffix.lower() != ".json":
        raise ValueError("记忆读取仅支持 .json 文件。")
    try:
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = raw.decode("gb18030")
        memory = json.loads(text)
    except FileNotFoundError:
        return {"version": 1, "messages": []}
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError(f"聊天记忆 JSON 无法解析：{path}；请修正格式或从备份恢复。") from exc
    if not isinstance(memory, dict):
        raise ValueError("聊天记忆 JSON 顶层必须是对象。")
    return memory


def Memory_json_write(memory: dict[str, Any], path: Path | str = MEMORY_FILE) -> dict[str, Any]:
    """原子覆盖 JSON 记忆；由入口完成路径、消息与向量校验后调用。"""
    path = Path(path)
    path = (path if path.is_absolute() else PROJECT_ROOT / path).resolve()
    if path.suffix.lower() != ".json":
        raise ValueError("记忆写入仅支持 .json 文件。")
    if not isinstance(memory, dict) or not isinstance(memory.get("messages"), list):
        raise ValueError("写入的记忆必须是含 messages 列表的 JSON 对象。")
    content = json.dumps(memory, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
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
    return {"path": str(path), "count": len(memory["messages"])}


def file_read(path: Path | str) -> str:
    """读取 .md 正文；由入口在路径检查通过后调用，缺失时报错。"""
    path = Path(path)
    path = (path if path.is_absolute() else PROJECT_ROOT / path).resolve()
    if path.suffix.lower() != ".md":
        raise ValueError("Prompt 读取仅支持 .md 文件。")
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("gb18030")


def file_write(path: Path | str, content: str) -> dict[str, Any]:
    """UTF-8 原子覆盖 .md 正文；由入口在路径检查通过后调用。"""
    path = Path(path)
    path = (path if path.is_absolute() else PROJECT_ROOT / path).resolve()
    if path.suffix.lower() != ".md":
        raise ValueError("Prompt 写入仅支持 .md 文件。")
    if not isinstance(content, str):
        raise ValueError("Markdown 正文 content 必须是字符串。")
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
    return {"path": str(path), "characters": len(content)}
