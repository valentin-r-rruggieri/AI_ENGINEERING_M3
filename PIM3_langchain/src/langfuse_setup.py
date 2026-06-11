from __future__ import annotations

from typing import Any

from src.config import get_settings


TRACE_NAME = "pim3-langchain-rag"


def get_langfuse_callback() -> Any | None:
    settings = get_settings()
    if not settings.has_langfuse:
        return None

    try:
        from langfuse.langchain import CallbackHandler
    except ImportError:
        return None

    try:
        return CallbackHandler(public_key=settings.langfuse_public_key)
    except TypeError:
        return CallbackHandler(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )


def invoke_config(metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    callback = get_langfuse_callback()
    if callback is None:
        return {}
    return {
        "callbacks": [callback],
        "run_name": TRACE_NAME,
        "metadata": metadata or {},
    }


def score_current_trace(scores: dict[str, float], comment: str) -> None:
    settings = get_settings()
    if not settings.has_langfuse:
        return

    try:
        from langfuse import Langfuse

        client = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )
        for name, value in scores.items():
            client.score_current_trace(name=name, value=value, comment=comment)
    except Exception:
        return
