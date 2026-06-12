from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents import route_query
from src.config import DOMAIN_DIRS, ROOT_DIR
from src.graph import build_graph, initial_state
from src.langfuse_setup import flush_langfuse, graph_config
from src.rag import count_chunks


def run_query(query: str) -> dict[str, Any]:
    graph = build_graph()
    config = graph_config()
    try:
        if config:
            return graph.invoke(initial_state(query), config=config)
        return graph.invoke(initial_state(query))
    finally:
        flush_langfuse()


def print_result(result: dict[str, Any]) -> None:
    print("\n" + "=" * 70)
    print(f"Pregunta: {result['query']}")
    print(f"Intent: {result.get('intent')}")
    print(f"Razon: {result.get('reason')}")
    print("\nRespuesta:")
    print(result.get("answer", ""))

    if result.get("sources"):
        print("\nFuentes recuperadas:")
        for source in result["sources"]:
            print(f"- {source['source']}")
    print("=" * 70)


def validate() -> int:
    print("Chunks por dominio")
    ok = True
    for domain in DOMAIN_DIRS:
        total = count_chunks(domain)
        print(f"- {domain}: {total}")
        ok = ok and total >= 50

    print("\nRouting con test_queries.json")
    queries = json.loads((ROOT_DIR / "test_queries.json").read_text(encoding="utf-8"))
    for item in queries:
        decision = route_query(item["query"])
        passed = decision.intent == item["expected_intent"]
        ok = ok and passed
        status = "OK" if passed else "FAIL"
        print(f"- {status} expected={item['expected_intent']} detected={decision.intent} query={item['query']}")

    return 0 if ok else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="PIM3 multiagente RAG simple")
    parser.add_argument("--query", "-q", help="Consulta para ejecutar.")
    parser.add_argument("--validate", action="store_true", help="Valida chunks y routing offline.")
    args = parser.parse_args()

    if args.validate:
        raise SystemExit(validate())

    if args.query:
        print_result(run_query(args.query))
        return

    print("PIM3 multiagente RAG. Escribi 'salir' para terminar.")
    while True:
        query = input("\nPregunta: ").strip()
        if query.lower() in {"salir", "exit", "quit"}:
            break
        if query:
            print_result(run_query(query))


if __name__ == "__main__":
    main()
