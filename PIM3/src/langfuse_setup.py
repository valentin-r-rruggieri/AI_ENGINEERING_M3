"""Integracion de Langfuse para tracing.

Este modulo inicializa el cliente de Langfuse, crea el CallbackHandler de
LangChain/LangGraph y fuerza el envio de trazas al cerrar la CLI.
"""

from __future__ import annotations

from typing import Any, cast

from langchain_core.runnables import RunnableConfig

from src.config import get_settings


# Nombre con el que buscamos las ejecuciones en Langfuse.
TRACE_NAME = "pim3-multiagent-rag"
# Cliente global reutilizable: evita crear un cliente por nodo o por callback.
_LANGFUSE_CLIENT: Any | None = None


def get_langfuse_callback(trace_id: str | None = None) -> Any | None:
    # El CallbackHandler conecta LangChain/LangGraph con Langfuse.
    client = get_langfuse_client()
    if client is None:
        return None

    try:
        from langfuse.langchain import CallbackHandler
    except ImportError:
        return None

    settings = get_settings()
    # En langfuse 4.x el callback usa el cliente ya inicializado por public_key.
    trace_context = {"trace_id": trace_id} if trace_id else None
    return CallbackHandler(public_key=settings.langfuse_public_key, trace_context=cast(Any, trace_context))


def get_langfuse_client() -> Any | None:
    global _LANGFUSE_CLIENT
    if _LANGFUSE_CLIENT is not None:
        return _LANGFUSE_CLIENT

    settings = get_settings()
    if not settings.has_langfuse:
        # Sin credenciales reales, la app corre sin tracing remoto.
        return None

    try:
        from langfuse import Langfuse
    except ImportError:
        return None

    # Inicializa el cliente con la region correcta: EU, US, Japan, etc.
    _LANGFUSE_CLIENT = Langfuse(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        base_url=settings.langfuse_base_url,
    )
    return _LANGFUSE_CLIENT


def graph_config(trace_id: str | None = None, metadata: dict[str, Any] | None = None) -> RunnableConfig | None:
    # Config que se pasa a graph.invoke(..., config=config).
    callback = get_langfuse_callback(trace_id=trace_id)
    if callback is None:
        return None
    final_metadata = {"project": "PIM3", "trace_name": TRACE_NAME}
    if metadata:
        final_metadata.update(metadata)
    return {
        "callbacks": [callback],
        "run_name": TRACE_NAME,
        "metadata": final_metadata,
    }


def flush_langfuse() -> None:
    # La CLI termina rapido; flush fuerza el envio antes de cerrar el proceso.
    client = get_langfuse_client()
    if client is not None:
        client.flush()
