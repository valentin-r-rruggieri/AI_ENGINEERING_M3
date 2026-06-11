# Guia Notion exacta - PIM3_STARTER

Esta guia sirve para crear la version starter con TODOs guiados.

A diferencia de PIM3, aca no copiamos la solucion: copiamos el scaffold didactico para que el alumno complete.

## 1. Estructura

```txt
.env.example
.gitignore
data/finance_docs/finance_policy_01.md
data/finance_docs/finance_policy_02.md
data/finance_docs/finance_policy_03.md
data/finance_docs/finance_policy_04.md
data/finance_docs/finance_policy_05.md
data/finance_docs/finance_policy_06.md
data/hr_docs/hr_policy_01.md
data/hr_docs/hr_policy_02.md
data/hr_docs/hr_policy_03.md
data/hr_docs/hr_policy_04.md
data/hr_docs/hr_policy_05.md
data/hr_docs/hr_policy_06.md
data/tech_docs/tech_policy_01.md
data/tech_docs/tech_policy_02.md
data/tech_docs/tech_policy_03.md
data/tech_docs/tech_policy_04.md
data/tech_docs/tech_policy_05.md
data/tech_docs/tech_policy_06.md
NOTION_GUIA_PASO_A_PASO.md
README.md
requirements.txt
src/__init__.py
src/agents.py
src/config.py
src/evaluator.py
src/graph.py
src/langfuse_setup.py
src/main.py
src/rag.py
test_queries.json
```

## 2. Archivos base

### `.env.example`
```env
OPENAI_API_KEY=your-key-here

LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=https://cloud.langfuse.com

OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

### `.gitignore`
```gitignore
.env
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ipynb_checkpoints/
vectorstores/
*.log
```

### `requirements.txt`
```txt
langchain
langchain-openai
langchain-community
langchain-text-splitters
langgraph
langfuse
openai
faiss-cpu
tiktoken
python-dotenv
pydantic
jupyter
ipykernel
pypdf
rich
pytest
```

### `test_queries.json`
```json
[
  {
    "query": "Cuantos dias de vacaciones tengo si llevo 3 anos en la empresa?",
    "expected_intent": "hr"
  },
  {
    "query": "No puedo conectarme a la VPN desde mi notebook",
    "expected_intent": "tech"
  },
  {
    "query": "Cuando se procesa el reembolso de una factura aprobada?",
    "expected_intent": "finance"
  },
  {
    "query": "Necesito cambiar mi contrasena del correo corporativo",
    "expected_intent": "tech"
  },
  {
    "query": "Como se calcula el bono anual de desempeno?",
    "expected_intent": "hr"
  },
  {
    "query": "Que documentacion necesito para cargar un gasto de viaje?",
    "expected_intent": "finance"
  },
  {
    "query": "Tengo problemas con el doble factor de autenticacion",
    "expected_intent": "tech"
  },
  {
    "query": "Cuando pagan los reintegros?",
    "expected_intent": "finance"
  },
  {
    "query": "Puedo tomar licencia por estudio?",
    "expected_intent": "hr"
  },
  {
    "query": "Cual es la capital de Francia?",
    "expected_intent": "unknown"
  },
  {
    "query": "Tengo un problema con la VPN y ademas quiero pedir vacaciones",
    "expected_intent": "unknown"
  },
  {
    "query": "Me rechazaron un gasto y no se si hablar con finanzas o soporte",
    "expected_intent": "unknown"
  }
]
```

## 3. Copiar documentos

Copiar las carpetas `data/hr_docs`, `data/tech_docs` y `data/finance_docs`.

## 4. Crear `src/__init__.py`

Copiar este archivo completo:

```python
"""Starter del PIM3.

Este paquete esta incompleto a proposito.
La carpeta PIM3 contiene una posible version final para comparar al final.
"""
```

## 5. Crear `src/config.py`

Copiar este archivo completo:

```python
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


# ROOT_DIR apunta a la carpeta PIM3_STARTER.
# Usamos Path para que el codigo funcione igual en Windows, Linux o Colab.
ROOT_DIR = Path(__file__).resolve().parents[1]

# DATA_DIR contiene los documentos reales que va a consultar el RAG.
DATA_DIR = ROOT_DIR / "data"

# VECTORSTORE_DIR va a guardar los indices FAISS generados localmente.
# No hace falta subir esta carpeta al repo porque se puede regenerar.
VECTORSTORE_DIR = ROOT_DIR / "vectorstores"

# Cada dominio tiene su propia carpeta documental.
# Esto es clave: no queremos que HR responda con documentos de Tech.
DOMAIN_DIRS = {
    "hr": DATA_DIR / "hr_docs",
    "tech": DATA_DIR / "tech_docs",
    "finance": DATA_DIR / "finance_docs",
}


def load_env() -> None:
    """Carga .env si python-dotenv esta instalado.

    No hardcodeamos API keys en codigo.
    El alumno debe copiar .env.example a .env y completar sus credenciales.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    """Configuracion central del proyecto.

    Tener un objeto Settings evita leer os.environ en todos los archivos.
    """

    openai_api_key: str
    openai_model: str
    openai_embedding_model: str
    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_host: str
    chunk_size: int = 280
    chunk_overlap: int = 40
    retriever_k: int = 4

    @property
    def has_openai(self) -> bool:
        """True si hay API key real para ejecutar embeddings y LLM."""
        return bool(self.openai_api_key and self.openai_api_key != "your-key-here")

    @property
    def has_langfuse(self) -> bool:
        """True si hay credenciales reales para enviar traces a Langfuse."""
        return bool(
            self.langfuse_public_key
            and self.langfuse_secret_key
            and self.langfuse_public_key != "pk-lf-xxx"
            and self.langfuse_secret_key != "sk-lf-xxx"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Devuelve configuracion cacheada.

    lru_cache evita reconstruir Settings en cada llamada.
    """
    load_env()
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        openai_embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
        langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
        langfuse_host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    )
```

## 6. Crear `src/rag.py`

Copiar este archivo completo:

```python
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from src.config import DOMAIN_DIRS, VECTORSTORE_DIR, get_settings


def load_documents(folder: Path) -> list:
    """TODO 1: cargar documentos reales desde una carpeta.

    En E23 los documentos estaban en un diccionario en memoria.
    En el PI queremos documentos reales en disco.

    Pistas:
    - importar Document desde langchain_core.documents;
    - recorrer folder.rglob("*");
    - aceptar .md, .txt y .csv;
    - leer cada archivo con encoding="utf-8";
    - guardar metadata con source y file_name.
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar load_documents(folder)")


def split_documents(documents: list) -> list:
    """TODO 2: partir documentos en chunks.

    El LLM no deberia recibir documentos enormes completos.
    El splitter crea fragmentos chicos que despues se indexan en FAISS.

    Pistas:
    - usar RecursiveCharacterTextSplitter;
    - tomar chunk_size y chunk_overlap desde get_settings();
    - devolver splitter.split_documents(documents).
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar split_documents(documents)")


def count_chunks(domain: str) -> int:
    """Cuenta chunks de un dominio.

    Este helper sirve para validar que cada dominio tenga suficiente material.
    Cuando load_documents y split_documents esten listos, esta funcion deberia funcionar.
    """
    documents = load_documents(DOMAIN_DIRS[domain])
    chunks = split_documents(documents)
    return len(chunks)


def build_embeddings():
    """TODO 3: crear embeddings reales con OpenAI.

    Los embeddings convierten texto en vectores.
    FAISS busca similitud entre la pregunta y los chunks usando esos vectores.

    Pistas:
    - validar settings.has_openai;
    - importar OpenAIEmbeddings desde langchain_openai;
    - usar settings.openai_embedding_model.
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar build_embeddings()")


@lru_cache(maxsize=3)
def get_retriever(domain: str):
    """TODO 4: crear o cargar un retriever FAISS por dominio.

    Este es el cambio principal respecto de E23.
    Antes buscabamos con keywords en una lista.
    Ahora:
    documentos -> chunks -> embeddings -> FAISS -> retriever.

    Pistas:
    - importar FAISS desde langchain_community.vectorstores;
    - usar VECTORSTORE_DIR / domain como carpeta local;
    - si existe, cargar con FAISS.load_local(...);
    - si no existe, crear con FAISS.from_documents(...);
    - guardar con vectorstore.save_local(...);
    - devolver vectorstore.as_retriever(search_kwargs={"k": settings.retriever_k}).
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar get_retriever(domain)")


def retrieve_context(domain: str, query: str) -> tuple[str, list[dict[str, Any]]]:
    """TODO 5: recuperar contexto para una pregunta.

    Cada agente va a llamar esta funcion.
    La funcion debe devolver:
    - context: texto listo para poner en el prompt;
    - sources: lista de fuentes para mostrar/debuggear.

    Pistas:
    - retriever = get_retriever(domain);
    - docs = retriever.invoke(query);
    - unir page_content de los docs recuperados;
    - incluir file_name/source en sources.
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar retrieve_context(domain, query)")
```

## 7. Crear `src/agents.py`

Copiar este archivo completo:

```python
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
```

## 8. Crear `src/evaluator.py`

Copiar este archivo completo:

```python
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from src.langfuse_setup import score_current_trace


class Evaluation(BaseModel):
    """Modelo de salida del evaluator.

    El evaluator es bonus, pero ayuda a conectar M3L4:
    no solo respondemos, tambien medimos calidad.
    """

    relevance: int = Field(ge=1, le=10)
    completeness: int = Field(ge=1, le=10)
    accuracy: int = Field(ge=1, le=10)
    clarity: int = Field(ge=1, le=10)
    overall: float = Field(ge=1, le=10)
    feedback: str


def evaluator_node(state: dict[str, Any]) -> dict[str, Any]:
    """TODO 18: evaluar respuesta y registrar scores.

    Para una primera version pueden devolver una evaluacion fija.
    Para version completa:
    - usar ChatOpenAI con structured output;
    - pasar query, intent, context y answer;
    - registrar scores en Langfuse.
    """
    # TODO: reemplazar por evaluate(state) y score_current_trace(...).
    raise NotImplementedError("Completar evaluator_node(state)")


def evaluate(state: dict[str, Any]) -> Evaluation:
    """TODO 19: crear evaluator local o LLM-as-judge.

    Version simple:
    - devolver valores fijos razonables.

    Version bonus:
    - usar ChatPromptTemplate;
    - usar ChatOpenAI.with_structured_output(Evaluation);
    - pedir que baje accuracy si la respuesta inventa.
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar evaluate(state)")
```

## 9. Crear `src/langfuse_setup.py`

Copiar este archivo completo:

```python
from __future__ import annotations

from typing import Any

from src.config import get_settings


TRACE_NAME = "pim3-starter-multiagent-rag"


def get_langfuse_callback() -> Any | None:
    """TODO 15: crear CallbackHandler de Langfuse.

    Langfuse permite ver el flujo completo:
    - entrada del usuario;
    - decision del orquestador;
    - nodo/agente ejecutado;
    - generation del LLM;
    - scores del evaluator.

    Pistas:
    - si no hay settings.has_langfuse, devolver None;
    - importar CallbackHandler desde langfuse.langchain;
    - devolver CallbackHandler(public_key=settings.langfuse_public_key).
    """
    # TODO: reemplazar este raise por una implementacion o devolver None al inicio.
    raise NotImplementedError("Completar get_langfuse_callback()")


def graph_config() -> dict[str, Any]:
    """TODO 16: devolver config para graph.invoke(...).

    Si hay callback:
    {
        "callbacks": [callback],
        "run_name": TRACE_NAME,
        "metadata": {...}
    }

    Si no hay callback, devolver {} para que el proyecto siga corriendo localmente.
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar graph_config()")


def score_current_trace(scores: dict[str, float], comment: str) -> None:
    """TODO 17: registrar scores del evaluator en Langfuse.

    Bonus:
    - crear cliente Langfuse;
    - por cada score, llamar score_current_trace;
    - si falla Langfuse, no romper la demo.
    """
    # TODO: se puede dejar como pass si no hacen el bonus.
    raise NotImplementedError("Completar score_current_trace(scores, comment)")
```

## 10. Crear `src/graph.py`

Copiar este archivo completo:

```python
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
```

## 11. Crear `src/main.py`

Copiar este archivo completo:

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# Permite ejecutar tanto:
# python -m src.main
# como:
# python src/main.py
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents import route_query
from src.config import DOMAIN_DIRS, ROOT_DIR
from src.graph import build_graph, initial_state
from src.langfuse_setup import graph_config
from src.rag import count_chunks


def run_query(query: str) -> dict:
    """TODO 20: ejecutar el grafo para una consulta.

    Pasos:
    - graph = build_graph()
    - config = graph_config()
    - si config existe, graph.invoke(initial_state(query), config=config)
    - si no, graph.invoke(initial_state(query))
    """
    # TODO: reemplazar este raise por la implementacion.
    raise NotImplementedError("Completar run_query(query)")


def print_result(result: dict) -> None:
    """Muestra resultado de forma simple para clase."""
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

    if result.get("evaluation"):
        print("\nEvaluator:")
        for key, value in result["evaluation"].items():
            print(f"- {key}: {value}")
    print("=" * 70)


def validate() -> int:
    """Valida chunks y routing.

    Esta funcion empieza a funcionar cuando los alumnos completan rag.py y agents.py.
    """
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
    parser = argparse.ArgumentParser(description="PIM3 STARTER multiagente RAG")
    parser.add_argument("--query", "-q", help="Consulta para ejecutar.")
    parser.add_argument("--validate", action="store_true", help="Valida chunks y routing offline.")
    args = parser.parse_args()

    if args.validate:
        raise SystemExit(validate())

    if args.query:
        print_result(run_query(args.query))
        return

    print("PIM3 STARTER. Escribi 'salir' para terminar.")
    while True:
        query = input("\nPregunta: ").strip()
        if query.lower() in {"salir", "exit", "quit"}:
            break
        if query:
            print_result(run_query(query))


if __name__ == "__main__":
    main()
```

## Uso en clase

1. Leer `README.md`.
2. Completar `rag.py`.
3. Completar `agents.py`.
4. Completar `graph.py`.
5. Completar `langfuse_setup.py`.
6. Ejecutar `python -m compileall src`.
7. Ejecutar `python -m src.main --validate`.
