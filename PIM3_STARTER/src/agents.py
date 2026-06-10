from __future__ import annotations

from typing import Any, Literal, TypedDict

from pydantic import BaseModel, Field

from src.config import get_settings
from src.rag import retrieve_context


# El router solo puede elegir estas rutas.
# unknown es importante para consultas fuera de alcance o ambiguas.
Intent = Literal["hr", "tech", "finance", "unknown"]


class AgentState(TypedDict):
    """Estado compartido de LangGraph.

    En LangGraph los nodos no se llaman pasando muchos parametros.
    Todos leen y escriben sobre un diccionario de estado.
    """

    query: str
    intent: str
    reason: str
    context: str
    sources: list[dict[str, Any]]
    answer: str
    evaluation: dict[str, Any]


class RouteDecision(BaseModel):
    """Salida estructurada del orquestador.

    Usar un modelo evita respuestas ambiguas como "creo que soporte".
    Queremos campos claros: intent y reason.
    """

    intent: Intent = Field(description="Dominio elegido: hr, tech, finance o unknown.")
    reason: str = Field(description="Motivo breve del ruteo.")


# Router simple, transparente y parecido a E23.
# Mas adelante se puede reemplazar por un router 100% LLM.
KEYWORDS = {
    "hr": ["vacacion", "licencia", "beneficio", "bono", "desempeno", "onboarding", "estudio"],
    "tech": ["vpn", "2fa", "doble factor", "contrasena", "correo", "notebook", "soporte", "acceso"],
    "finance": ["factura", "pago", "reembolso", "reintegro", "gasto", "viaje", "finanzas", "metodo"],
}


def route_query(query: str) -> RouteDecision:
    """TODO 6: clasificar la consulta.

    Objetivo:
    - si detecta solo un dominio, devolver ese intent;
    - si detecta varios dominios o ninguno, devolver unknown;
    - opcional: si hay OPENAI_API_KEY, usar ChatOpenAI con structured output.

    Pistas para version simple:
    - pasar query a minusculas;
    - buscar keywords por dominio;
    - matched = dominios con al menos una keyword;
    - si len(matched) == 1, devolver RouteDecision(...);
    - si no, unknown.
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar route_query(query)")


def orchestrator_node(state: AgentState) -> dict:
    """TODO 7: nodo orquestador.

    Este nodo NO responde la pregunta.
    Solo decide que agente debe trabajar.

    Debe devolver un dict con:
    - intent
    - reason
    """
    # TODO: llamar a route_query(state["query"]) y devolver campos.
    raise NotImplementedError("Completar orchestrator_node(state)")


def answer_with_rag(domain: str, state: AgentState) -> dict:
    """TODO 8: logica comun de los agentes RAG.

    Cada agente hace el mismo proceso:
    1. recuperar contexto del dominio correcto;
    2. construir un prompt;
    3. llamar al LLM;
    4. devolver context, sources y answer.

    Pistas:
    - settings = get_settings();
    - si no hay API key, devolver un mensaje claro;
    - context, sources = retrieve_context(domain, state["query"]);
    - usar ChatPromptTemplate y ChatOpenAI;
    - el prompt debe decir "usa unicamente el contexto".
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar answer_with_rag(domain, state)")


def hr_agent_node(state: AgentState) -> dict:
    """TODO 9: agente de Recursos Humanos."""
    # TODO: return answer_with_rag("hr", state)
    raise NotImplementedError("Completar hr_agent_node(state)")


def tech_agent_node(state: AgentState) -> dict:
    """TODO 10: agente de soporte tecnico."""
    # TODO: return answer_with_rag("tech", state)
    raise NotImplementedError("Completar tech_agent_node(state)")


def finance_agent_node(state: AgentState) -> dict:
    """TODO 11: agente de finanzas."""
    # TODO: return answer_with_rag("finance", state)
    raise NotImplementedError("Completar finance_agent_node(state)")


def unknown_node(state: AgentState) -> dict:
    """TODO 12: fallback.

    Este nodo responde cuando:
    - la pregunta esta fuera de alcance;
    - la pregunta mezcla dominios;
    - el router no esta seguro.
    """
    # TODO: devolver context="", sources=[] y una respuesta clara de fuera de alcance.
    raise NotImplementedError("Completar unknown_node(state)")
