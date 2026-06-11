from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.chains import classify_intent, handle_query
from src.config import DOMAIN_DIRS, ROOT_DIR
from src.rag import count_chunks


def print_result(result: dict) -> None:
    print("\n" + "=" * 70)
    print(f"Pregunta: {result['query']}")
    print(f"Intent: {result['intent']}")
    print(f"Razon: {result['reason']}")
    print("\nRespuesta:")
    print(result["answer"])

    if result["sources"]:
        print("\nFuentes:")
        for source in result["sources"]:
            print(f"- {source['source']}")

    if result["evaluation"]:
        print("\nEvaluator:")
        for key, value in result["evaluation"].items():
            print(f"- {key}: {value}")
    print("=" * 70)


def validate() -> int:
    ok = True
    print("Chunks por dominio")
    for domain in DOMAIN_DIRS:
        total = count_chunks(domain)
        ok = ok and total >= 50
        print(f"- {domain}: {total}")

    print("\nRouting con test_queries.json")
    queries = json.loads((ROOT_DIR / "test_queries.json").read_text(encoding="utf-8"))
    for item in queries:
        decision = classify_intent(item["query"])
        passed = decision.intent == item["expected_intent"]
        ok = ok and passed
        status = "OK" if passed else "FAIL"
        print(f"- {status} expected={item['expected_intent']} detected={decision.intent} query={item['query']}")

    return 0 if ok else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="PIM3 LangChain + Langfuse")
    parser.add_argument("--query", "-q", help="Consulta para ejecutar.")
    parser.add_argument("--validate", action="store_true", help="Valida chunks y routing offline.")
    args = parser.parse_args()

    if args.validate:
        raise SystemExit(validate())

    if args.query:
        print_result(handle_query(args.query))
        return

    print("PIM3 LangChain. Escribi 'salir' para terminar.")
    while True:
        query = input("\nPregunta: ").strip()
        if query.lower() in {"salir", "exit", "quit"}:
            break
        if query:
            print_result(handle_query(query))


if __name__ == "__main__":
    main()
