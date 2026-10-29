"""记忆读写模块，不导入模型调用模块。

函数结构与调用关系：
├─ read_memory(path) → common.read_json → common.read_text_file
│                   → common.validate_memory
└─ write_memory(memory, path) → common.validate_memory → common.write_json
调用：由外部入口编排两个独立函数，不自动执行读改写流程。
数据流：prototype/Memory/memories.json ↔ 校验后的完整记忆文档。
读取返回：{"version": 1, "memories": list}；文件不存在时返回空文档，不创建文件。
写入返回：{"path": str, "count": int}；原子覆盖完整快照，不自动追加或合并。
"""

from pathlib import Path
from typing import Any

from prototype.Core.common import read_json, validate_memory, write_json
from prototype.Core.paths import MEMORY_FILE


def read_memory(path: Path = MEMORY_FILE) -> dict[str, Any]:
    """读取完整记忆文档；由调用方编排，路径可显式替换。"""
    path = Path(path)
    try:
        data = read_json(path)
    except FileNotFoundError:
        return {"version": 1, "memories": []}
    return validate_memory(data)


def write_memory(memory: dict[str, Any], path: Path = MEMORY_FILE) -> dict[str, Any]:
    """校验并保存完整记忆文档；由调用方负责读改写与单写入者协调。"""
    path = Path(path)
    data = validate_memory(memory)
    write_json(path, data)
    return {"path": str(path), "count": len(data["memories"])}
