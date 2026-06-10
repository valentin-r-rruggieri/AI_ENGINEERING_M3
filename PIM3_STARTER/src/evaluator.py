from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from src.langfuse_setup import score_current_trace


class Evaluation(BaseModel):
    """Modelo de salida del evaluator.

    El evaluator es bonus, pero ayuda a conectar M3L4:
    no solo respondemos, tambien medimos calidad.
    """

    relevance: int = Field(ge=1, le=10)
    completeness: int = Field(ge=1, le=10)
    accuracy: int = Field(ge=1, le=10)
    clarity: int = Field(ge=1, le=10)
    overall: float = Field(ge=1, le=10)
    feedback: str


def evaluator_node(state: dict[str, Any]) -> dict[str, Any]:
    """TODO 18: evaluar respuesta y registrar scores.

    Para una primera version pueden devolver una evaluacion fija.
    Para version completa:
    - usar ChatOpenAI con structured output;
    - pasar query, intent, context y answer;
    - registrar scores en Langfuse.
    """
    # TODO: reemplazar por evaluate(state) y score_current_trace(...).
    raise NotImplementedError("Completar evaluator_node(state)")


def evaluate(state: dict[str, Any]) -> Evaluation:
    """TODO 19: crear evaluator local o LLM-as-judge.

    Version simple:
    - devolver valores fijos razonables.

    Version bonus:
    - usar ChatPromptTemplate;
    - usar ChatOpenAI.with_structured_output(Evaluation);
    - pedir que baje accuracy si la respuesta inventa.
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar evaluate(state)")
