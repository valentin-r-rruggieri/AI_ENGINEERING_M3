from __future__ import annotations

import unicodedata
from typing import Any, Literal, TypedDict

from pydantic import BaseModel, Field

from src.config import get_settings
from src.rag import retrieve_context


# Dominios disponibles en el grafo. Si el router devuelve otra cosa, no hay nodo.
Intent = Literal["hr", "tech", "finance", "unknown"]


class AgentState(TypedDict):
    # Estado compartido que LangGraph mueve entre nodos.
    query: str
    intent: str
    reason: str
    context: str
    sources: list[dict[str, Any]]
    answer: str


class RouteDecision(BaseModel):
    # Salida estructurada del router: dominio elegido + explicacion breve.
    intent: Intent = Field(description="Dominio elegido: hr, tech, finance o unknown.")
    reason: str = Field(description="Motivo breve del ruteo.")


# Reglas estables para que la demo no dependa de que el LLM clasifique bien
# consultas basicas como "vacaciones" o "VPN".
KEYWORDS = {
    "hr": [
        "vacacion",
        "vacaciones",
        "licencia",
        "beneficio",
        "bono",
        "desempeno",
        "rrhh",
        "recursos humanos",
        "onboarding",
        "estudio",
    ],
    "tech": [
        "vpn",
        "2fa",
        "doble factor",
        "contrasena",
        "password",
        "correo",
        "notebook",
        "soporte",
        "acceso",
    ],
    "finance": [
        "factura",
        "pago",
        "reembolso",
        "reintegro",
        "gasto",
        "viaje",
        "finanzas",
        "metodo",
    ],
}


def normalize_text(text: str) -> str:
    # Normaliza minusculas y tildes para matchear "contraseña" y "contrasena".
    normalized = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def keyword_matches(query: str) -> list[str]:
    # Devuelve todos los dominios detectados por keywords.
    q = normalize_text(query)
    return [domain for domain, words in KEYWORDS.items() if any(word in q for word in words)]


def route_query(query: str) -> RouteDecision:
    """Router simple como E23. Prioriza reglas estables y usa LLM solo como apoyo."""
    matched = keyword_matches(query)
    if len(matched) == 1:
        # Caso ideal: una sola area clara.
        return RouteDecision(intent=matched[0], reason=f"Se detectaron senales claras de {matched[0]}.")
    if len(matched) > 1:
        # Si mezcla areas, evitamos responder desde un agente incorrecto.
        return RouteDecision(intent="unknown", reason="La consulta mezcla mas de un dominio interno.")

    settings = get_settings()
    if settings.has_openai:
        try:
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_openai import ChatOpenAI

            # El LLM solo se usa cuando las reglas no detectan un dominio claro.
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Clasifica la consulta interna en hr, tech, finance o unknown. "
                        "hr incluye vacaciones, licencias, beneficios, bonos, desempeno y onboarding. "
                        "tech incluye VPN, correo, contrasenas, 2FA, notebooks, soporte y accesos. "
                        "finance incluye facturas, pagos, reembolsos, reintegros, gastos y viajes. "
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
            # Si falla el router LLM, caemos a unknown en vez de romper la app.
            pass

    return RouteDecision(intent="unknown", reason="La consulta es ambigua o esta fuera de alcance.")


def orchestrator_node(state: AgentState) -> dict[str, Any]:
    # Nodo inicial: clasifica la query y escribe intent + reason en el estado.
    decision = route_query(state["query"])
    return {"intent": decision.intent, "reason": decision.reason}


def answer_with_rag(domain: str, state: AgentState) -> dict[str, Any]:
    settings = get_settings()
    if not settings.has_openai:
        # Modo demo offline: prueba routing y LangGraph sin gastar OpenAI.
        return {
            "context": "",
            "sources": [],
            "answer": (
                "El orquestador ya puede rutear esta consulta, pero falta OPENAI_API_KEY "
                "para ejecutar RAG real con embeddings, FAISS y LLM."
            ),
        }

    # Recupera contexto real desde el vector store del dominio elegido.
    context, sources = retrieve_context(domain, state["query"])

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    # El prompt obliga a responder con el contexto y a ser util si hay fuentes.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"Sos un agente especialista de {domain}. "
                "Responde en espanol usando unicamente el contexto provisto. "
                "Si el contexto contiene una politica relacionada, da una respuesta util y accionable. "
                "Si falta un dato personal o puntual, explica que dato falta y responde igual con la politica aplicable. "
                "No digas solamente 'No tengo informacion suficiente' si hay fuentes recuperadas relevantes. "
                "Inclui 2 a 4 pasos concretos cuando corresponda.",
            ),
            ("human", "Contexto:\n{context}\n\nConsulta:\n{query}\n\nRespuesta:"),
        ]
    )
    llm = ChatOpenAI(model=settings.openai_model, temperature=0.2, api_key=settings.openai_api_key)
    response = (prompt | llm).invoke({"context": context, "query": state["query"]})
    # Devolvemos campos parciales; LangGraph los fusiona con el estado existente.
    return {"context": context, "sources": sources, "answer": response.content}


def hr_agent_node(state: AgentState) -> dict[str, Any]:
    # Agente especialista en Recursos Humanos.
    return answer_with_rag("hr", state)


def tech_agent_node(state: AgentState) -> dict[str, Any]:
    # Agente especialista en Soporte Tecnico.
    return answer_with_rag("tech", state)


def finance_agent_node(state: AgentState) -> dict[str, Any]:
    # Agente especialista en Finanzas.
    return answer_with_rag("finance", state)


def unknown_node(state: AgentState) -> dict[str, Any]:
    # Fallback seguro: si no hay dominio claro, no inventamos respuesta.
    return {
        "context": "",
        "sources": [],
        "answer": (
            "No tengo documentacion interna suficiente para responder esa consulta. "
            "Puedo ayudarte con RR. HH., soporte tecnico o finanzas."
        ),
    }
