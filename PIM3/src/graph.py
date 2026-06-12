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


def next_node(state: AgentState) -> str:
    # LangGraph llama esta funcion despues del orquestador.
    # Devuelve el nombre del nodo destino, no ejecuta el agente.
    intent = state.get("intent", "unknown")
    if intent in {"hr", "tech", "finance"}:
        return intent
    return "unknown"


def build_graph():
    # StateGraph usa AgentState como contrato del flujo completo.
    graph = StateGraph(AgentState)

    # Cada funcion se registra como nodo con un nombre estable.
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("hr", hr_agent_node)
    graph.add_node("tech", tech_agent_node)
    graph.add_node("finance", finance_agent_node)
    graph.add_node("unknown", unknown_node)

    # Toda ejecucion empieza clasificando la consulta.
    graph.add_edge(START, "orchestrator")
    # Routing condicional: el intent decide a que agente ir.
    graph.add_conditional_edges(
        "orchestrator",
        next_node,
        {
            "hr": "hr",
            "tech": "tech",
            "finance": "finance",
            "unknown": "unknown",
        },
    )
    # En esta version no hay agente evaluador: la evaluacion se hace en Langfuse.
    graph.add_edge("hr", END)
    graph.add_edge("tech", END)
    graph.add_edge("finance", END)
    graph.add_edge("unknown", END)

    # compile valida la estructura y devuelve un grafo ejecutable.
    return graph.compile()


def initial_state(query: str) -> AgentState:
    # Estado inicial predecible para que todos los nodos encuentren sus campos.
    return {
        "query": query,
        "intent": "",
        "reason": "",
        "context": "",
        "sources": [],
        "answer": "",
    }
