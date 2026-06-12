"""CLI del PIM3.

Permite validar el proyecto, ejecutar una consulta puntual o abrir un modo
interactivo desde terminal usando `uv run python -m src.main`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


if __package__ is None or __package__ == "":
    # Permite ejecutar tanto `python -m src.main` como `python src/main.py`.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents import route_query
from src.config import DOMAIN_DIRS, ROOT_DIR
from src.graph import build_graph, initial_state
from src.langfuse_setup import flush_langfuse, graph_config
from src.rag import count_chunks


def evidence_preview(content: str, limit: int = 180) -> str:
    # Para la demo conviene mostrar contenido util, no notas administrativas.
    skipped_prefixes = (
        "Notas de control documental",
        "- La informacion de esta seccion",
        "- Si el caso no coincide",
        "- Mantener actualizada",
        "- Las respuestas a clientes internos",
    )
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    useful_lines = [line for line in lines if not line.startswith(skipped_prefixes)]
    preview = " ".join(useful_lines[:3] or lines[:3])
    if len(preview) > limit:
        preview = preview[: limit - 3] + "..."
    return preview


def run_query(query: str) -> dict[str, Any]:
    # Construye el grafo por corrida para mantener la demo simple y explicita.
    graph = build_graph()
    config = graph_config()
    try:
        # Si Langfuse esta configurado, graph.invoke recibe callbacks.
        if config:
            return graph.invoke(initial_state(query), config=config)
        return graph.invoke(initial_state(query))
    finally:
        # Asegura que las trazas se envien antes de que cierre la CLI.
        flush_langfuse()


def print_result(result: dict[str, Any]) -> None:
    # Salida pensada para clase: muestra que hizo el sistema antes de responder.
    print("\n" + "=" * 70)
    print("CHAT PIM3 - RAG MULTIAGENTE")
    print("=" * 70)
    print(f"Usuario: {result['query']}")

    print("\n1) Decision del orquestador")
    print(f"- Intent detectado: {result.get('intent')}")
    print(f"- Motivo visible: {result.get('reason')}")

    if result.get("trace_steps"):
        print("\n2) Pasos ejecutados")
        for index, step in enumerate(result["trace_steps"], start=1):
            print(f"- {index}. {step['step']}: {step['detail']}")

    print("\n3) Busqueda y fuentes")
    if result.get("sources"):
        for index, source in enumerate(result["sources"], start=1):
            preview = evidence_preview(source.get("content", ""))
            print(f"- Fuente {index}: {source['source']}")
            print(f"  Evidencia: {preview}")
    else:
        print("- No se recuperaron fuentes porque la consulta quedo fuera de alcance o falta configuracion.")

    print("\n4) Respuesta final")
    print(result.get("answer", ""))
    print("=" * 70)


def validate() -> int:
    # Validacion offline: no necesita OpenAI si el router resuelve por keywords.
    print("Chunks por dominio")
    ok = True
    for domain in DOMAIN_DIRS:
        total = count_chunks(domain)
        print(f"- {domain}: {total}")
        ok = ok and total >= 50

    print("\nRouting con test_queries.json")
    queries = json.loads((ROOT_DIR / "test_queries.json").read_text(encoding="utf-8"))
    for item in queries:
        # Golden dataset minimo: compara intent esperado vs detectado.
        decision = route_query(item["query"])
        passed = decision.intent == item["expected_intent"]
        ok = ok and passed
        status = "OK" if passed else "FAIL"
        print(f"- {status} expected={item['expected_intent']} detected={decision.intent} query={item['query']}")

    return 0 if ok else 1


def main() -> None:
    # CLI con tres modos: validate, query unica o loop interactivo.
    parser = argparse.ArgumentParser(description="PIM3 multiagente RAG simple")
    parser.add_argument("--query", "-q", help="Consulta para ejecutar.")
    parser.add_argument("--validate", action="store_true", help="Valida chunks y routing offline.")
    args = parser.parse_args()

    if args.validate:
        # `SystemExit` devuelve codigo 0 si ok, 1 si fallo.
        raise SystemExit(validate())

    if args.query:
        print_result(run_query(args.query))
        return

    print("PIM3 multiagente RAG. Escribi 'salir' para terminar.")
    while True:
        # Modo interactivo para probar varias preguntas en una sola corrida.
        query = input("\nPregunta: ").strip()
        if query.lower() in {"salir", "exit", "quit"}:
            break
        if query:
            print_result(run_query(query))


if __name__ == "__main__":
    main()
