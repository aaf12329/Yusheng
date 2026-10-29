"""记忆读取模块，不导入记忆写入或模型调用模块。

结构：read_memory(path) → common.read_json → common.read_text_file；
                         → common.validate_memory。
调用：由外部入口或手动 Python 调用 read_memory。
数据流：Memory/memories.json → JSON 对象 → 校验后的完整记忆文档。
返回：{"version": 1, "memories": list}；文件不存在时返回空文档，不创建文件。
"""

from pathlib import Path
from typing import Any

from prototype.common import read_json, validate_memory
from prototype.paths import MEMORY_FILE


def read_memory(path: Path = MEMORY_FILE) -> dict[str, Any]:
    """读取完整记忆文档；由调用方编排，路径可显式替换。"""
    path = Path(path)
    try:
        data = read_json(path)
    except FileNotFoundError:
        return {"version": 1, "memories": []}
    return validate_memory(data)
