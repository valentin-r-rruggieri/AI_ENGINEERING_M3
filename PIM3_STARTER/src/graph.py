from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from src.agents import (
    AgentState,
    finance_agent_node,
    hr_agent_node,
    orchestrator_node,
    tech_agent_node,
    unknown_node,
)
from src.evaluator import evaluator_node


def next_node(state: AgentState) -> str:
    """TODO 13: decidir el proximo nodo segun state["intent"].

    Esta funcion es la que usa add_conditional_edges.
    No ejecuta agentes; solo devuelve el nombre de la ruta.
    """
    # TODO:
    # intent = state.get("intent", "unknown")
    # if intent in {"hr", "tech", "finance"}: return intent
    # return "unknown"
    raise NotImplementedError("Completar next_node(state)")


def build_graph():
    """TODO 14: construir el StateGraph.

    Este archivo es el corazon de LangGraph.
    Aca conectamos nodos, rutas y fin del flujo.

    Pasos:
    1. graph = StateGraph(AgentState)
    2. add_node para orchestrator, hr, tech, finance, unknown, evaluator
    3. add_edge START -> orchestrator
    4. add_conditional_edges desde orchestrator usando next_node
    5. hr/tech/finance -> evaluator
    6. unknown -> END
    7. evaluator -> END
    8. return graph.compile()
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar build_graph()")


def initial_state(query: str) -> AgentState:
    """Estado inicial antes de ejecutar el grafo.

    Este helper ya esta completo para que los alumnos se concentren en el grafo.
    """
    return {
        "query": query,
        "intent": "",
        "reason": "",
        "context": "",
        "sources": [],
        "answer": "",
        "evaluation": {},
    }
