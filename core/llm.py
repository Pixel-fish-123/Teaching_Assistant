# core/llm.py

# 这一步主要是做接口设计，为后续调用大模型服务打下基础

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Literal, Sequence, TypedDict

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    OpenAIError,
    RateLimitError,
)

# 默认配置与限制

DEFAULT_MODEL = "deepseek-flash"
LEGACY_MODELS = frozenset({"deepseek-chat", "deepseek-reasoner"})
MAX_INPUT_CHARS = 20_000

# 以下为消息结构与异常类

class Message(TypedDict):
    role: Literal["system", "user", "assistant"]  # 约束：只能是 system / user / assistant
    content: str

class LLMError(Exception):
    """模型层错误基类"""

class LLMConfigError(LLMError):
    """key 缺失、模型名非法、配置格式错误"""

class LLMRequestError(LLMError):
    """网络、限流、服务端错误"""

class LLMTimeoutError(LLMRequestError):  # [修正] 超时属于请求错误
    """请求超时"""

class LLMResponseError(LLMError):
    """返回为空、结构异常"""

# 以下为LLM配置类

'''
人为注释一下，本次主要是针对本项目的接口进行设计，现在主要是支持deepseek

未来需要进行一次小重构，加一层兼容层，这样可以支持以OpenAI协议为基础的大模型

接口主要是针对各种异常情况进行检查，也跑了几次测试，目前没看到什么问题

代码应该还是有很多只为deepseek设计的残留，不过先把流程跑通再改
'''

@dataclass(frozen=True)

class LLMConfig:
    api_key: str = field(repr=False)  # [修正] 避免 repr/日志打印出 API key
    base_url: str = "https://api.deepseek.com"  # 默认服务地址；环境变量缺失时使用
    model: str = DEFAULT_MODEL
    timeout_s: float = 30.0
    max_retries: int = 1

    def __post_init__(self):
        errors: list[str] = []

        if not isinstance(self.api_key, str) or not self.api_key.strip():
            errors.append("DEEPSEEK_API_KEY 未配置")

        if not isinstance(self.model, str) or not self.model.strip():
            errors.append("DEEPSEEK_MODEL 不能为空")
        elif self.model in LEGACY_MODELS:
            errors.append(
                f"{self.model} 已停用，请使用 {DEFAULT_MODEL}"
            )

        if not isinstance(self.base_url, str) or not self.base_url.strip():
            errors.append("DEEPSEEK_BASE_URL 不能为空")

        if not isinstance(self.timeout_s, (int, float)) or self.timeout_s <= 0:
            errors.append("timeout_s 必须是大于 0 的数字")

        if not isinstance(self.max_retries, int) or self.max_retries < 0:
            errors.append("max_retries 必须是大于等于 0 的整数")

        if errors:
            raise LLMConfigError(
                "配置错误：\n- " + "\n- ".join(errors)
            )

    @classmethod
    def from_env(cls) -> "LLMConfig":
        load_dotenv()

        api_key = os.getenv("DEEPSEEK_API_KEY", "")

        model = (
            (os.getenv("DEEPSEEK_MODEL") or "").strip()
            or DEFAULT_MODEL
        )
        
        try:
            timeout_s = float(os.getenv("DEEPSEEK_TIMEOUT_S", "30"))
            max_retries = int(os.getenv("DEEPSEEK_MAX_RETRIES", "1"))
        except ValueError as exc:
            raise LLMConfigError("TIMEOUT/RETRIES 必须是数字") from exc

        return cls(
            api_key = api_key,
            base_url = (
                (os.getenv("DEEPSEEK_BASE_URL") or "").strip()
                or "https://api.deepseek.com"
            ),  # [修正] 空值/纯空白回落默认
            model = model,
            timeout_s = timeout_s,
            max_retries = max_retries,
        )

@dataclass(frozen=True)
class ChatResult:
    text: str
    model: str
    finish_reason: str | None
    latency_ms: int
    response_id: str | None
    usage: dict | None
    truncated: bool = False

class DeepSeekClient:
    def __init__(
        self,
        config: LLMConfig,
        *,
        client: OpenAI | None = None,
    ):
        self._config = config
        self._client = client or OpenAI(
            api_key = config.api_key,
            base_url = config.base_url,
            timeout = config.timeout_s,
            max_retries = config.max_retries,
        )

    @classmethod
    def from_env(cls) -> "DeepSeekClient":
        return cls(LLMConfig.from_env())

    def chat(
        self,
        messages: Sequence[Message],
        *,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> ChatResult:
        self._validate(messages)
        started = time.perf_counter()

        try:
            response = self._client.chat.completions.create(
                model = self._config.model,
                messages = list(messages),
                temperature = temperature,
                max_tokens = max_tokens,
            )
        except AuthenticationError as exc:
            raise LLMConfigError("API key 被拒绝") from exc
        except APITimeoutError as exc:
            raise LLMTimeoutError("请求超时") from exc
        except APIConnectionError as exc:
            raise LLMRequestError("网络连接失败") from exc
        except RateLimitError as exc:
            raise LLMRequestError("请求受限/余额不足") from exc
        except APIStatusError as exc:
            raise LLMRequestError(f"模型服务返回 HTTP {exc.status_code}") from exc
        except OpenAIError as exc:  # [修正] 兜底未列出的 SDK 异常
            raise LLMRequestError("模型调用失败") from exc

        if not response.choices:
            raise LLMResponseError("模型没有返回 choices")

        choice = response.choices[0]
        text = (choice.message.content or "").strip()
        if not text:
            raise LLMResponseError("模型返回空内容")

        usage = response.usage.model_dump() if response.usage else None

        return ChatResult(
            text = text,
            model = response.model or self._config.model,
            finish_reason = choice.finish_reason,
            latency_ms = int((time.perf_counter() - started) * 1000),
            response_id = response.id,
            usage = usage,
            truncated = choice.finish_reason == "length",
        )

    @staticmethod
    def _validate(messages: Sequence[Message]) -> None:  # [修正] 原 _vaildate 拼写错误
        if not messages:
            raise ValueError("messages 不能为空")

        total_chars = 0  # [修正] 去掉多余分号
        for message in messages:
            role = message.get("role")  # [修正] 原 messages.get 错误
            content = message.get("content", "")

            if role not in {"system", "user", "assistant"}:
                raise ValueError(f"非法 role: {role}")
            if not isinstance(content, str) or not content.strip():
                raise ValueError("content 必须是非空字符串")

            total_chars += len(content)

        if total_chars > MAX_INPUT_CHARS:
            raise ValueError(
                f"输入过长: {total_chars} 字符, 上限 {MAX_INPUT_CHARS}"  # [修正] 检查的是输入
            )
        
