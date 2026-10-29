"""DeepSeek 模型调用模块，不读取记忆，也不执行工具。

函数结构与调用关系：
├─ _load_api_key() → common.read_text_file；由 call_model 调用
└─ call_model(messages) → _load_api_key → OpenAI.chat.completions.create
数据流：messages → 固定 Flash/关闭思考/非流式请求 → 统一返回字典。
返回契约：content: str，reasoning: str，usage: dict | None，tool_calls: list，
          finish_reason: str，message: dict（保留原始 assistant 消息供后续回存）。
调用方负责后续编排；本模块不会自动保存聊天或记忆。
"""

from typing import Any

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

from prototype.common import read_text_file
from prototype.paths import ENV_FILE


MODEL = "deepseek-flash"
BASE_URL = "https://api.deepseek.com"


def _load_api_key() -> str:
    """从根目录 .env 读取单行 DEEPSEEK_API_KEY；仅由 call_model 调用。"""
    try:
        text = read_text_file(ENV_FILE)
    except FileNotFoundError:
        raise RuntimeError("请将根目录 .env.example 复制为 .env，并填写 DEEPSEEK_API_KEY。") from None
    for line in text.splitlines():
        key, separator, value = line.strip().partition("=")
        if separator and key.strip() == "DEEPSEEK_API_KEY":
            value = value.strip()
            if value.startswith(("'", '"')):
                if len(value) < 2 or value[-1] != value[0]:
                    raise ValueError(".env 中 DEEPSEEK_API_KEY 的引号未闭合。")
                value = value[1:-1]
            if value and value.strip() == value:
                return value
            break
    raise RuntimeError("请在根目录 .env 中填写非空的 DEEPSEEK_API_KEY=你的密钥。")


def call_model(messages: list[dict[str, Any]]) -> dict[str, Any]:
    """调用固定 DeepSeek Flash 并统一返回结构；由外部入口传入完整消息列表。"""
    if not isinstance(messages, list) or not messages:
        raise ValueError("messages 必须是非空消息列表，例如 [{'role': 'user', 'content': '你好'}]。")
    # 暂不自动重试，避免调用方不知情时重复发起请求。
    try:
        with OpenAI(
            api_key=_load_api_key(), base_url=BASE_URL,
            timeout=60.0, max_retries=0,
        ) as client:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=False,
                extra_body={"thinking": {"type": "disabled"}},
            )
    except APITimeoutError:
        raise RuntimeError("DeepSeek 请求超时；请检查网络后按需重试。") from None
    except APIConnectionError:
        raise RuntimeError("无法连接 DeepSeek；请检查网络和代理配置。") from None
    except APIStatusError as exc:
        raise RuntimeError(
            f"DeepSeek 返回 HTTP {exc.status_code}；请核对密钥、账户额度和请求参数。"
        ) from None

    if not response.choices:
        raise RuntimeError("DeepSeek 未返回 choices；请检查服务状态及接口兼容性。")
    choice = response.choices[0]
    message = choice.message
    return {
        "content": message.content or "",
        "reasoning": getattr(message, "reasoning_content", None) or "",
        "usage": response.usage.model_dump() if response.usage is not None else None,
        "tool_calls": [call.model_dump() for call in (message.tool_calls or [])],
        "finish_reason": choice.finish_reason,
        "message": message.model_dump(exclude_none=True),
    }
