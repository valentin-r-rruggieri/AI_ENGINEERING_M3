from __future__ import annotations

from typing import Any

from src.config import get_settings


# Nombre con el que buscamos las ejecuciones en Langfuse.
TRACE_NAME = "pim3-multiagent-rag"
# Cliente global reutilizable: evita crear un cliente por nodo o por callback.
_LANGFUSE_CLIENT: Any | None = None


def get_langfuse_callback() -> Any | None:
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
    return CallbackHandler(public_key=settings.langfuse_public_key)


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


def graph_config() -> dict[str, Any]:
    # Config que se pasa a graph.invoke(..., config=config).
    callback = get_langfuse_callback()
    if callback is None:
        return {}
    return {
        "callbacks": [callback],
        "run_name": TRACE_NAME,
        "metadata": {"project": "PIM3", "trace_name": TRACE_NAME},
    }


def flush_langfuse() -> None:
    # La CLI termina rapido; flush fuerza el envio antes de cerrar el proceso.
    client = get_langfuse_client()
    if client is not None:
        client.flush()
