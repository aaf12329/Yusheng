"""路径地址簿：纯常量，无文件读写。

结构：CORE_ROOT → PROTOTYPE_ROOT → PROJECT_ROOT → ENV_FILE；
      PROTOTYPE_ROOT → INITIAL_PROMPT_FILE / MEMORY_DIR → MEMORY_FILE / MARKDOWN_FILE。
调用：File_read_and_write、Tools_protect、core 及外部入口只读取这些常量。
数据流：模块位置 → 项目根目录 → 各本地文件位置。
"""

from pathlib import Path


CORE_ROOT = Path(__file__).resolve().parent
PROTOTYPE_ROOT = CORE_ROOT.parent
PROJECT_ROOT = PROTOTYPE_ROOT.parent
ENV_FILE = PROJECT_ROOT / ".env"
INITIAL_PROMPT_FILE = PROTOTYPE_ROOT / "PromptSQL" / "initial_prompt.md"
MEMORY_DIR = PROTOTYPE_ROOT / "Memory"
MEMORY_FILE = MEMORY_DIR / "conversation.json"
MARKDOWN_FILE = MEMORY_DIR / "notes.md"
TOOL_EXCLUDED_DIRS = tuple(
    PROJECT_ROOT / name
    for name in (".git", "myvenv", ".venv", "venv", ".conda", "node_modules", "__pycache__")
)
TOOL_PROTECTED_DIRS = (CORE_ROOT, *TOOL_EXCLUDED_DIRS)
TOOL_PROTECTED_FILES = (
    ENV_FILE,
    PROTOTYPE_ROOT / "main.py",
    PROTOTYPE_ROOT / "__init__.py",
)
