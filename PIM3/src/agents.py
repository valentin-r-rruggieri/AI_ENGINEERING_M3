from __future__ import annotations

from typing import Any, Literal, TypedDict

from pydantic import BaseModel, Field

from src.config import get_settings
from src.rag import retrieve_context


Intent = Literal["hr", "tech", "finance", "unknown"]


class AgentState(TypedDict):
    query: str
    intent: str
    reason: str
    context: str
    sources: list[dict[str, Any]]
    answer: str
    evaluation: dict[str, Any]


class RouteDecision(BaseModel):
    intent: Intent = Field(description="Dominio elegido: hr, tech, finance o unknown.")
    reason: str = Field(description="Motivo breve del ruteo.")


KEYWORDS = {
    "hr": ["vacacion", "licencia", "beneficio", "bono", "desempeno", "onboarding", "estudio"],
    "tech": ["vpn", "2fa", "doble factor", "contrasena", "correo", "notebook", "soporte", "acceso"],
    "finance": ["factura", "pago", "reembolso", "reintegro", "gasto", "viaje", "finanzas", "metodo"],
}


def route_query(query: str) -> RouteDecision:
    """Router simple como E23. Si hay API key, se puede apoyar en LLM."""
    settings = get_settings()
    if settings.has_openai:
        try:
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
            llm = ChatOpenAI(
                model=settings.openai_model,
                temperature=0,
                api_key=settings.openai_api_key,
            ).with_structured_output(RouteDecision)
            return (prompt | llm).invoke({"query": query})
        except Exception:
            pass

    q = query.lower()
    matched = [domain for domain, words in KEYWORDS.items() if any(word in q for word in words)]
    if len(matched) == 1:
        return RouteDecision(intent=matched[0], reason=f"Se detectaron senales claras de {matched[0]}.")
    return RouteDecision(intent="unknown", reason="La consulta es ambigua o esta fuera de alcance.")


def orchestrator_node(state: AgentState) -> dict:
    decision = route_query(state["query"])
    return {"intent": decision.intent, "reason": decision.reason}


def answer_with_rag(domain: str, state: AgentState) -> dict:
    settings = get_settings()
    if not settings.has_openai:
        return {
            "context": "",
            "sources": [],
            "answer": (
                "El orquestador ya puede rutear esta consulta, pero falta OPENAI_API_KEY "
                "para ejecutar RAG real con embeddings, FAISS y LLM."
            ),
        }

    context, sources = retrieve_context(domain, state["query"])

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"Sos un agente especialista de {domain}. "
                "Responde usando unicamente el contexto provisto. "
                "Si el contexto no alcanza, deci que no tenes informacion suficiente.",
            ),
            ("human", "Contexto:\n{context}\n\nConsulta:\n{query}\n\nRespuesta:"),
        ]
    )
    llm = ChatOpenAI(model=settings.openai_model, temperature=0.2, api_key=settings.openai_api_key)
    response = (prompt | llm).invoke({"context": context, "query": state["query"]})
    return {"context": context, "sources": sources, "answer": response.content}


def hr_agent_node(state: AgentState) -> dict:
    return answer_with_rag("hr", state)


def tech_agent_node(state: AgentState) -> dict:
    return answer_with_rag("tech", state)


def finance_agent_node(state: AgentState) -> dict:
    return answer_with_rag("finance", state)


def unknown_node(state: AgentState) -> dict:
    return {
        "context": "",
        "sources": [],
        "answer": (
            "No tengo documentacion interna suficiente para responder esa consulta. "
            "Puedo ayudarte con RR. HH., soporte tecnico o finanzas."
        ),
    }
