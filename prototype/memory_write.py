"""记忆写入模块，不导入记忆读取或模型调用模块。

结构：write_memory(memory, path) → common.validate_memory → common.write_json。
调用：由外部入口或手动 Python 调用 write_memory。
数据流：完整记忆文档 → 格式校验 → UTF-8 JSON → 原子替换目标文件。
返回：{"path": str, "count": int}；覆盖保存完整快照，不自动追加或合并。
"""

from pathlib import Path
from typing import Any

from prototype.common import validate_memory, write_json
from prototype.paths import MEMORY_FILE


def write_memory(memory: dict[str, Any], path: Path = MEMORY_FILE) -> dict[str, Any]:
    """校验并保存完整记忆文档；由调用方负责读改写与单写入者协调。"""
    path = Path(path)
    data = validate_memory(memory)
    write_json(path, data)
    return {"path": str(path), "count": len(data["memories"])}
