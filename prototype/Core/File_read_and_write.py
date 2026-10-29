"""文件工具层：JSON 记忆与 Markdown 读写，不导入模型调用模块。

函数结构与调用关系：
├─ Memory_json_write(memory, path) → common.resolve_tool_path
│                                → common.validate_memory → common.write_json
├─ Memory_json_read(path) → common.resolve_tool_path → common.read_json
│                        → common.validate_memory
├─ file_read(path) → common.resolve_tool_path → common.read_text_file
└─ file_write(path, content) → common.resolve_tool_path → common.write_text_file
调用：由外部入口显式调用四个函数；尚未注册给模型或接入工具循环。
数据流：项目内 .json ↔ 完整记忆文档；项目内 .md ↔ 字符串正文。
契约：JSON 读取返回文档，文件缺失时返回空库；写入返回 {"path": str, "count": int}。
      Markdown 读取返回 str，文件缺失报错；写入返回 {"path": str, "characters": int}。
边界：相对路径以项目根目录为基准；写入完整覆盖，不自动追加，禁止写入 Core。
"""

from pathlib import Path
from typing import Any

from prototype.Core import common
from prototype.Core.paths import MEMORY_FILE


def Memory_json_write(memory: dict[str, Any], path: Path | str = MEMORY_FILE) -> dict[str, Any]:
    """校验并覆盖保存完整 JSON 记忆；供入口或后续工具执行器调用。"""
    path = common.resolve_tool_path(path, ".json", writable=True)
    data = common.validate_memory(memory)
    common.write_json(path, data)
    return {"path": str(path), "count": len(data["memories"])}


def Memory_json_read(path: Path | str = MEMORY_FILE) -> dict[str, Any]:
    """读取并校验 JSON 记忆；供入口或后续工具执行器调用，缺失返回空库。"""
    path = common.resolve_tool_path(path, ".json")
    try:
        data = common.read_json(path)
    except FileNotFoundError:
        return {"version": 1, "memories": []}
    return common.validate_memory(data)


def file_read(path: Path | str) -> str:
    """读取项目内 .md 正文；供入口或后续工具执行器调用，缺失文件直接报错。"""
    path = common.resolve_tool_path(path, ".md")
    return common.read_text_file(path)


def file_write(path: Path | str, content: str) -> dict[str, Any]:
    """以 UTF-8 原子覆盖项目内 .md 正文；供入口或后续工具执行器调用。"""
    path = common.resolve_tool_path(path, ".md", writable=True)
    if not isinstance(content, str):
        raise ValueError("Markdown 正文 content 必须是字符串。")
    common.write_text_file(path, content)
    return {"path": str(path), "characters": len(content)}
