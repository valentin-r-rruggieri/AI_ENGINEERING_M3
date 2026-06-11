from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from src.config import get_settings
from src.langfuse_setup import invoke_config, score_current_trace
from src.rag import retrieve_context


Intent = Literal["hr", "tech", "finance", "unknown"]


class RouteDecision(BaseModel):
    intent: Intent = Field(description="Selected route.")
    reason: str = Field(description="Short explanation for the route.")


class Evaluation(BaseModel):
    relevance: int = Field(ge=1, le=10)
    completeness: int = Field(ge=1, le=10)
    accuracy: int = Field(ge=1, le=10)
    clarity: int = Field(ge=1, le=10)
    overall: float = Field(ge=1, le=10)
    feedback: str


KEYWORDS = {
    "hr": ["vacacion", "licencia", "beneficio", "bono", "desempeno", "onboarding", "estudio"],
    "tech": ["vpn", "2fa", "doble factor", "contrasena", "correo", "notebook", "soporte", "acceso"],
    "finance": ["factura", "pago", "reembolso", "reintegro", "gasto", "viaje", "finanzas", "metodo"],
}


def classify_intent(query: str) -> RouteDecision:
    """Classify with LangChain when keys exist; otherwise use a transparent fallback."""
    settings = get_settings()
    if not settings.has_openai:
        return keyword_route(query)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Clasifica la consulta en hr, tech, finance o unknown. "
                "Si mezcla areas importantes, usa unknown. Devuelve salida estructurada.",
            ),
            ("human", "{query}"),
        ]
    )
    llm = ChatOpenAI(model=settings.openai_model, temperature=0, api_key=settings.openai_api_key)
    chain = prompt | llm.with_structured_output(RouteDecision)
    return chain.invoke({"query": query}, config=invoke_config({"step": "routing"}))


def keyword_route(query: str) -> RouteDecision:
    q = query.lower()
    matched = [domain for domain, words in KEYWORDS.items() if any(word in q for word in words)]
    if len(matched) == 1:
        return RouteDecision(intent=matched[0], reason=f"Ruta local por palabras clave: {matched[0]}.")
    return RouteDecision(intent="unknown", reason="Consulta ambigua o fuera de alcance.")


def answer_domain(domain: str, query: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.has_openai:
        return {
            "answer": "Routing disponible, pero falta OPENAI_API_KEY para ejecutar RAG real.",
            "context": "",
            "sources": [],
        }

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    context, sources = retrieve_context(domain, query)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Sos un agente especialista de {domain}. "
                "Responde usando unicamente el contexto provisto. "
                "Si el contexto no alcanza, deci que no tenes informacion suficiente.",
            ),
            ("human", "Contexto:\n{context}\n\nConsulta:\n{query}\n\nRespuesta:"),
        ]
    )
    llm = ChatOpenAI(model=settings.openai_model, temperature=0.2, api_key=settings.openai_api_key)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke(
        {"domain": domain, "context": context, "query": query},
        config=invoke_config({"step": "rag_generation", "domain": domain}),
    )
    return {"answer": answer, "context": context, "sources": sources}


def fallback_answer() -> dict[str, Any]:
    return {
        "answer": "No tengo documentacion interna suficiente. Puedo ayudar con HR, Tech o Finance.",
        "context": "",
        "sources": [],
    }


def evaluate_answer(query: str, intent: str, context: str, answer: str) -> Evaluation:
    settings = get_settings()
    if not settings.has_openai:
        return Evaluation(
            relevance=6,
            completeness=5,
            accuracy=6,
            clarity=7,
            overall=6.0,
            feedback="Evaluacion local simple porque falta OPENAI_API_KEY.",
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
            ("human", "Query:\n{query}\n\nIntent:\n{intent}\n\nContexto:\n{context}\n\nRespuesta:\n{answer}"),
        ]
    )
    llm = ChatOpenAI(model=settings.openai_model, temperature=0, api_key=settings.openai_api_key)
    chain = prompt | llm.with_structured_output(Evaluation)
    evaluation = chain.invoke(
        {"query": query, "intent": intent, "context": context, "answer": answer},
        config=invoke_config({"step": "evaluation"}),
    )
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
    return evaluation


def handle_query(query: str) -> dict[str, Any]:
    route = classify_intent(query)

    if route.intent in {"hr", "tech", "finance"}:
        rag_result = answer_domain(route.intent, query)
        evaluation = evaluate_answer(query, route.intent, rag_result["context"], rag_result["answer"])
    else:
        rag_result = fallback_answer()
        evaluation = {}

    return {
        "query": query,
        "intent": route.intent,
        "reason": route.reason,
        "answer": rag_result["answer"],
        "sources": rag_result["sources"],
        "evaluation": evaluation.model_dump() if hasattr(evaluation, "model_dump") else evaluation,
    }
