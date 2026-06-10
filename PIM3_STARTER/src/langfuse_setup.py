from __future__ import annotations

from typing import Any

from src.config import get_settings


TRACE_NAME = "pim3-starter-multiagent-rag"


def get_langfuse_callback() -> Any | None:
    """TODO 15: crear CallbackHandler de Langfuse.

    Langfuse permite ver el flujo completo:
    - entrada del usuario;
    - decision del orquestador;
    - nodo/agente ejecutado;
    - generation del LLM;
    - scores del evaluator.

    Pistas:
    - si no hay settings.has_langfuse, devolver None;
    - importar CallbackHandler desde langfuse.langchain;
    - devolver CallbackHandler(public_key=settings.langfuse_public_key).
    """
    # TODO: reemplazar este raise por una implementacion o devolver None al inicio.
    raise NotImplementedError("Completar get_langfuse_callback()")


def graph_config() -> dict[str, Any]:
    """TODO 16: devolver config para graph.invoke(...).

    Si hay callback:
    {
        "callbacks": [callback],
        "run_name": TRACE_NAME,
        "metadata": {...}
    }

    Si no hay callback, devolver {} para que el proyecto siga corriendo localmente.
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar graph_config()")


def score_current_trace(scores: dict[str, float], comment: str) -> None:
    """TODO 17: registrar scores del evaluator en Langfuse.

    Bonus:
    - crear cliente Langfuse;
    - por cada score, llamar score_current_trace;
    - si falla Langfuse, no romper la demo.
    """
    # TODO: se puede dejar como pass si no hacen el bonus.
    raise NotImplementedError("Completar score_current_trace(scores, comment)")
