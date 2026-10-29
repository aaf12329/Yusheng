"""路径地址簿：纯常量，无文件读写。

结构：PROJECT_ROOT → ENV_FILE / INITIAL_PROMPT_FILE / MEMORY_DIR → MEMORY_FILE。
调用：common、memory_read、memory_write、core 只读取这些常量。
数据流：模块位置 → 项目根目录 → 各本地文件位置。
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
INITIAL_PROMPT_FILE = PROJECT_ROOT / "PromptSQL" / "initial_prompt.md"
MEMORY_DIR = PROJECT_ROOT / "Memory"
MEMORY_FILE = MEMORY_DIR / "memories.json"
