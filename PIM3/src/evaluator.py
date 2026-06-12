"""Evaluator bonus del PIM3 con Langfuse Score API.

Este archivo no forma parte del grafo principal. Ejecuta un dataset de casos,
corre el grafo para cada input y registra scores numericos en Langfuse.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.config import ROOT_DIR
from src.graph import build_graph, initial_state
from src.langfuse_setup import flush_langfuse, get_langfuse_client, graph_config


DATASET_NAME = "pim3-routing-rag"
# Dataset local versionado con el repo. Se puede subir a Langfuse con
# `uv run python -m src.evaluator --upload-dataset`.
DEFAULT_DATASET_PATH = ROOT_DIR / "eval_dataset.json"


def load_eval_dataset(path: Path = DEFAULT_DATASET_PATH) -> list[dict[str, Any]]:
    # Dataset bonus para evaluar routing y calidad minima de respuesta.
    # Cada caso trae query, expected_intent y keywords esperadas en la respuesta.
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    # Normalizacion simple para evaluar keywords sin depender de mayusculas.
    # No usamos una metrica semantica aca: queremos un score facil de explicar.
    return text.lower()


def keyword_coverage(answer: str, expected_keywords: list[str]) -> float:
    # Score deterministico: proporcion de keywords esperadas presentes en la respuesta.
    if not expected_keywords:
        return 1.0
    answer_text = normalize(answer)
    # Cuenta cuantas keywords aparecen literalmente en la respuesta generada.
    hits = sum(1 for keyword in expected_keywords if normalize(keyword) in answer_text)
    return hits / len(expected_keywords)


def evaluate_result(case: dict[str, Any], result: dict[str, Any]) -> dict[str, float]:
    # Scores simples y trazables para Langfuse Score API.
    # La idea es cubrir la rubrica sin crear un judge opaco o dificil de explicar.
    expected_intent = case["expected_intent"]
    actual_intent = result.get("intent", "")
    answer = result.get("answer", "")
    sources = result.get("sources", [])

    # Para unknown esperamos que no haya fuentes RAG; para dominios reales si.
    expected_unknown = expected_intent == "unknown"
    has_expected_sources = bool(sources) if not expected_unknown else not sources

    # Todos los scores son numericos 0..1 para que Langfuse pueda agregarlos.
    return {
        "routing_correct": 1.0 if actual_intent == expected_intent else 0.0,
        "has_expected_sources": 1.0 if has_expected_sources else 0.0,
        "answer_generated": 1.0 if len(answer.strip()) > 20 else 0.0,
        "keyword_coverage": keyword_coverage(answer, case.get("expected_keywords", [])),
    }


def upload_dataset_to_langfuse(cases: list[dict[str, Any]]) -> None:
    # Crea/actualiza el dataset en Langfuse para que quede visible en la UI.
    langfuse = get_langfuse_client()
    if langfuse is None:
        raise RuntimeError("Faltan credenciales reales de Langfuse para subir dataset.")

    try:
        # El dataset queda disponible en la seccion Datasets de Langfuse.
        langfuse.create_dataset(
            name=DATASET_NAME,
            description="PIM3 bonus: dataset de routing, RAG y respuestas basicas.",
            metadata={"project": "PIM3", "type": "bonus-evaluator"},
        )
    except Exception:
        # Si el dataset ya existe, seguimos y actualizamos/creamos items por id.
        pass
    for case in cases:
        # Usar id estable permite re-ejecutar sin duplicar casos conceptualmente.
        langfuse.create_dataset_item(
            dataset_name=DATASET_NAME,
            id=case["id"],
            input={"query": case["query"]},
            expected_output={
                "expected_intent": case["expected_intent"],
                "expected_keywords": case.get("expected_keywords", []),
            },
            metadata={"case_id": case["id"]},
        )
    # Flush fuerza el envio de operaciones pendientes a Langfuse.
    flush_langfuse()


def run_case(case: dict[str, Any], run_name: str) -> dict[str, Any]:
    # Cada caso usa trace_id propio para poder asociarle scores via Score API.
    langfuse = get_langfuse_client()
    trace_id = langfuse.create_trace_id(seed=f"{run_name}:{case['id']}") if langfuse else None
    # Metadata del trace: despues sirve para filtrar por dataset, run o caso.
    config = graph_config(
        trace_id=trace_id,
        metadata={
            "dataset": DATASET_NAME,
            "dataset_run": run_name,
            "case_id": case["id"],
            "expected_intent": case["expected_intent"],
        },
    )

    # Reutilizamos el grafo real del proyecto. No evaluamos un sistema distinto.
    graph = build_graph()
    if config:
        result = graph.invoke(initial_state(case["query"]), config=config)
    else:
        result = graph.invoke(initial_state(case["query"]))

    # Guardamos trace_id en el resultado local para que score_case pueda puntuar.
    result["trace_id"] = trace_id
    return result


def score_case(case: dict[str, Any], result: dict[str, Any], run_name: str) -> dict[str, float]:
    # Registra scores numericos en Langfuse sobre el trace del caso.
    scores = evaluate_result(case, result)
    langfuse = get_langfuse_client()
    if langfuse is None or not result.get("trace_id"):
        # Sin Langfuse real, igual devolvemos scores locales para poder practicar.
        return scores

    for name, value in scores.items():
        # Score API: asocia cada metrica al trace generado por este caso.
        langfuse.create_score(
            trace_id=result["trace_id"],
            name=name,
            value=value,
            data_type="NUMERIC",
            comment=f"PIM3 bonus evaluator - {case['id']} - {run_name}",
            metadata={
                "case_id": case["id"],
                "expected_intent": case["expected_intent"],
                "actual_intent": result.get("intent"),
            },
        )
    # Aseguramos que los scores se vean en la UI antes de terminar.
    flush_langfuse()
    return scores


def run_evaluation(cases: list[dict[str, Any]], run_name: str) -> int:
    # Ejecuta el dataset completo, imprime resumen local y manda scores a Langfuse.
    rows = []
    for case in cases:
        # 1. Ejecutar caso contra el grafo real.
        result = run_case(case, run_name)
        # 2. Calcular y registrar scores.
        scores = score_case(case, result, run_name)
        rows.append((case, result, scores))

        # Log compacto para clase: expected vs actual y scores principales.
        print(
            f"{case['id']} expected={case['expected_intent']} "
            f"actual={result.get('intent')} routing={scores['routing_correct']:.0f} "
            f"keywords={scores['keyword_coverage']:.2f}"
        )

    # Promedios simples para saber si la corrida bonus paso o necesita revision.
    routing_avg = sum(row[2]["routing_correct"] for row in rows) / len(rows)
    keyword_avg = sum(row[2]["keyword_coverage"] for row in rows) / len(rows)
    print("\nResumen")
    print(f"- casos: {len(rows)}")
    print(f"- routing_correct promedio: {routing_avg:.2%}")
    print(f"- keyword_coverage promedio: {keyword_avg:.2%}")

    # Si falla routing, devolvemos codigo 1 para que tambien sirva en CI/clase.
    return 0 if routing_avg == 1.0 else 1


def main() -> None:
    # CLI del evaluator bonus. Se ejecuta separado de `src.main`.
    parser = argparse.ArgumentParser(description="PIM3 bonus evaluator con Langfuse Score API")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET_PATH), help="Ruta al dataset JSON.")
    parser.add_argument("--run-name", default="pim3-local-eval", help="Nombre del run de evaluacion.")
    parser.add_argument("--upload-dataset", action="store_true", help="Crea/actualiza dataset en Langfuse.")
    args = parser.parse_args()

    cases = load_eval_dataset(Path(args.dataset))
    if args.upload_dataset:
        # Opcional: crea el dataset en Langfuse antes de correr los casos.
        upload_dataset_to_langfuse(cases)
    raise SystemExit(run_evaluation(cases, args.run_name))


if __name__ == "__main__":
    main()
