"""保留的旧共用实现：按当前原型设计，运行链路不导入或调用本模块。

以下函数及旧记忆契约仅作保留；当前读写在 File_read_and_write，路径保护在 Tools_protect。
历史函数结构与调用说明：

函数结构与调用关系：
├─ resolve_tool_path(path, suffix, writable) ← 文件工具层的四个函数
├─ read_text_file(path) ← read_json、file_read、core._load_api_key、入口提示词加载
├─ write_text_file(path, text) ← write_json、file_write
├─ read_json(path) → read_text_file ← Memory_json_read
├─ write_json(path, data) → write_text_file ← Memory_json_write
└─ validate_memory(data) ← Memory_json_read、Memory_json_write
数据流：文件字节 ↔ JSON 对象 → 校验后的记忆文档。
契约：记忆为 {"version": 1, "memories": [{"id": 正整数, "content": 非空文本}]}。
校验返回原文档；不修改输入，允许保留额外的 JSON 字段。
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from prototype.Core.paths import CORE_ROOT, PROJECT_ROOT, TOOL_EXCLUDED_DIRS


def resolve_tool_path(path: Path | str, suffix: str, writable: bool = False) -> Path:
    """解析工具路径并检查后缀、项目范围及内核写入限制；供文件工具层调用。"""
    path = Path(path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path = path.resolve()
    if not path.is_relative_to(PROJECT_ROOT):
        raise ValueError("文件工具仅允许访问项目目录内的文件；请使用项目内路径。")
    if any(path.is_relative_to(directory) for directory in TOOL_EXCLUDED_DIRS):
        raise ValueError("文件工具不能访问 Git、环境或依赖缓存目录；请使用项目数据目录。")
    if path.suffix.lower() != suffix:
        raise ValueError(f"此工具仅支持 {suffix} 文件；请检查文件后缀。")
    if any(part.lower().startswith(".env") for part in path.relative_to(PROJECT_ROOT).parts):
        raise ValueError("文件工具不能访问 .env 凭据文件或目录。")
    if writable and path.is_relative_to(CORE_ROOT):
        raise ValueError("文件工具不能写入运行内核 Core；请将数据放在 prototype/Memory 中。")
    return path


def read_text_file(path: Path) -> str:
    """读取 UTF-8/BOM 文本，兼容旧 GB18030 文件；供共用读取与密钥加载调用。"""
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("gb18030")


def read_json(path: Path) -> Any:
    """解析本地 JSON；由 Memory_json_read 调用，损坏文件明确报错而不当作空库。"""
    try:
        return json.loads(read_text_file(path))
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError(f"JSON 文件无法解析：{path}；请修正格式或从备份恢复。") from exc


def write_json(path: Path, data: Any) -> None:
    """完整序列化 JSON 后交给共用文本写入口；由 Memory_json_write 调用。"""
    text = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    write_text_file(path, text)


def write_text_file(path: Path, text: str) -> None:
    """UTF-8 原子覆盖文本；由 write_json 和 file_write 调用，失败保留原文件。"""
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
