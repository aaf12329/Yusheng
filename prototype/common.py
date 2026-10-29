"""共用层：文件 I/O 与记忆格式校验，不调用功能模块。

函数结构与调用关系：
├─ read_text_file(path) ← read_json、core._load_api_key
├─ read_json(path) → read_text_file ← memory_read.read_memory
├─ write_json(path, data) ← memory_write.write_memory
└─ validate_memory(data) ← memory_read.read_memory、memory_write.write_memory
数据流：文件字节 ↔ JSON 对象 → 校验后的记忆文档。
契约：记忆为 {"version": 1, "memories": [{"id": 正整数, "content": 非空文本}]}。
校验返回原文档；不修改输入，允许保留额外的 JSON 字段。
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def read_text_file(path: Path) -> str:
    """读取 UTF-8/BOM 文本，兼容旧 GB18030 文件；供共用读取与密钥加载调用。"""
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("gb18030")


def read_json(path: Path) -> Any:
    """解析本地 JSON；由 read_memory 调用，损坏文件明确报错而不当作空库。"""
    try:
        return json.loads(read_text_file(path))
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError(f"JSON 文件无法解析：{path}；请修正格式或从备份恢复。") from exc


def write_json(path: Path, data: Any) -> None:
    """先完整序列化，再原子替换文件；由 write_memory 调用，失败保留原文件。"""
    text = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        # 同目录临时文件保证替换不跨磁盘；原子替换不提供多进程写入锁。
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def validate_memory(data: Any) -> dict[str, Any]:
    """检查版本、条目及唯一正整数 ID；由读写模块共同调用。"""
    if not isinstance(data, dict):
        raise ValueError("记忆文档必须是包含 version 和 memories 的 JSON 对象。")
    if type(data.get("version")) is not int or data["version"] != 1:
        raise ValueError("记忆文档的 version 必须为整数 1。")
    if not isinstance(data.get("memories"), list):
        raise ValueError("记忆文档的 memories 必须为列表。")
    seen_ids = set()
    for index, memory in enumerate(data["memories"], start=1):
        if not isinstance(memory, dict):
            raise ValueError(f"第 {index} 条记忆必须是 JSON 对象。")
        memory_id = memory.get("id")
        if type(memory_id) is not int or memory_id < 1 or memory_id in seen_ids:
            raise ValueError(f"第 {index} 条记忆的 id 必须是从 1 开始的唯一正整数。")
        content = memory.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"第 {index} 条记忆的 content 必须是非空字符串。")
        seen_ids.add(memory_id)
    return data
