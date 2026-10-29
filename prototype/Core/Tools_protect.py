"""工具路径保护层：只检查路径，不执行文件读写，不导入功能模块。

函数结构：check_tool_path(path, operation)。
调用关系：main 在文件操作前调用；后续 LLM 工具执行入口同样先检查，再调用文件工具。
数据流：原始路径 + read/write → 真实绝对路径 + 保护名单 → 允许或拒绝结果。
契约：{"allowed": bool, "path": str, "reason": str}；path 为解析结果，解析失败时为空。
边界：仅允许项目内路径，Core、启动代码、Git、环境、缓存及 .env 凭据禁止读写。
本模块不注册工具、不执行工具，也不提供操作系统层面的进程隔离。
"""

from pathlib import Path

from prototype.Core.paths import PROJECT_ROOT, TOOL_PROTECTED_DIRS, TOOL_PROTECTED_FILES


def check_tool_path(path: Path | str, operation: str = "read") -> dict[str, bool | str]:
    """检查工具路径和读写动作；供入口调用，拒绝时返回原因而不执行文件操作。"""
    if operation not in {"read", "write"}:
        return {"allowed": False, "path": "", "reason": "operation 只支持 read 或 write。"}
    try:
        resolved = Path(path)
        if not resolved.is_absolute():
            resolved = PROJECT_ROOT / resolved
        resolved = resolved.resolve()
    except (OSError, ValueError, TypeError, RuntimeError):
        return {"allowed": False, "path": "", "reason": "路径无法解析；请检查路径格式。"}
    result: dict[str, bool | str] = {"allowed": False, "path": str(resolved), "reason": ""}
    if not resolved.is_relative_to(PROJECT_ROOT):
        result["reason"] = "工具仅允许访问项目目录内的文件。"
    elif any(resolved.is_relative_to(folder) for folder in TOOL_PROTECTED_DIRS):
        result["reason"] = "路径位于受保护目录中，工具不得读写。"
    elif resolved in TOOL_PROTECTED_FILES:
        result["reason"] = "路径命中受保护文件，工具不得读写。"
    elif any(part.lower().startswith(".env") for part in resolved.relative_to(PROJECT_ROOT).parts):
        result["reason"] = "工具不得访问 .env 凭据文件或目录。"
    else:
        result["allowed"] = True
        result["reason"] = "路径检查通过。"
    return result
