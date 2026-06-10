from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from src.config import get_settings
from src.langfuse_setup import score_current_trace


class Evaluation(BaseModel):
    relevance: int = Field(ge=1, le=10)
    completeness: int = Field(ge=1, le=10)
    accuracy: int = Field(ge=1, le=10)
    clarity: int = Field(ge=1, le=10)
    overall: float = Field(ge=1, le=10)
    feedback: str


def evaluator_node(state: dict[str, Any]) -> dict[str, Any]:
    evaluation = evaluate(state)
    score_current_trace(
        {
            "relevance": float(evaluation.relevance),
            "completeness": float(evaluation.completeness),
            "accuracy": float(evaluation.accuracy),
            "clarity": float(evaluation.clarity),
            "overall": float(evaluation.overall),
        },
        evaluation.feedback,
    )
    return {"evaluation": evaluation.model_dump()}


def evaluate(state: dict[str, Any]) -> Evaluation:
    settings = get_settings()
    if not settings.has_openai:
        return Evaluation(
            relevance=6,
            completeness=5,
            accuracy=6,
            clarity=7,
            overall=6.0,
            feedback="Evaluacion local simple: para score real configurar OPENAI_API_KEY.",
        )

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Evalua la respuesta RAG de 1 a 10 en relevance, completeness, accuracy, clarity y overall. "
                "Si inventa informacion no presente en el contexto, baja accuracy. Devuelve salida estructurada.",
            ),
            (
                "human",
                "Query:\n{query}\n\nIntent:\n{intent}\n\nContexto:\n{context}\n\nRespuesta:\n{answer}",
            ),
        ]
    )
    llm = ChatOpenAI(
        model=settings.openai_model,
        temperature=0,
        api_key=settings.openai_api_key,
    ).with_structured_output(Evaluation)
    return (prompt | llm).invoke(state)
