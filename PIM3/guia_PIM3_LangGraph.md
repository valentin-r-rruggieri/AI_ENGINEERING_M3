# Guia paso a paso - construir PIM3 con LangGraph, RAG, Langfuse, uv y evaluator bonus

Esta guia esta escrita para construir el PIM3 desde cero, archivo por archivo.

No es solo una explicacion conceptual: en cada paso vas a ver:

- que archivo crear;
- que codigo pegar;
- que hace cada funcion;
- por que usamos esa pieza;
- como probar que funciona;
- como se conecta con la rubrica.

## 0. Que vamos a construir

El PIM3 es un sistema multiagente simple:

```txt
pregunta del usuario
  -> orquestador clasifica intent
  -> LangGraph elige ruta
  -> agente especialista recupera documentos con RAG
  -> LLM responde usando contexto
  -> Langfuse registra trazas
  -> evaluator bonus registra scores en Langfuse
```

Dominios:

- `hr`: vacaciones, licencias, beneficios, bonos, onboarding.
- `tech`: VPN, 2FA, correo, contrasenas, notebooks, accesos.
- `finance`: facturas, pagos, reembolsos, gastos.
- `unknown`: fuera de alcance o mezcla de dominios.

Importante:

- El evaluator bonus no es un nodo del grafo principal.
- El grafo principal solo orquesta y responde.
- La evaluacion bonus corre aparte con `src/evaluator.py` y registra scores en Langfuse.

## 1. Estructura final

Crear esta estructura:

```txt
PIM3/
|-- README.md
|-- pyproject.toml
|-- .python-version
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- test_queries.json
|-- eval_dataset.json
|-- guia_PIM3_LangGraph.md
|
|-- data/
|   |-- hr_docs/
|   |-- tech_docs/
|   `-- finance_docs/
|
`-- src/
    |-- __init__.py
    |-- config.py
    |-- rag.py
    |-- agents.py
    |-- graph.py
    |-- langfuse_setup.py
    |-- main.py
    `-- evaluator.py
```

Comandos iniciales desde PowerShell:

```powershell
cd C:\Users\Usuario\Desktop\Clases\AI_ENGINEERING_M3
mkdir PIM3
cd PIM3
mkdir src
mkdir data
mkdir data\hr_docs
mkdir data\tech_docs
mkdir data\finance_docs
```

## 2. Crear entorno con uv

### Archivo: `.python-version`

Crear:

```txt
3.12
```

Por que:

- Usamos Python 3.12 para mantener compatibilidad estable con el stack de LangChain, ChromaDB y Langfuse.
- `uv` usa este archivo para elegir una version compatible.
- Esto evita depender del Python global de la computadora.

### Archivo: `pyproject.toml`

Crear:

```toml
[project]
name = "pim3-langgraph-rag-langfuse"
version = "0.1.0"
description = "PIM3: multi-agent RAG with LangGraph and Langfuse tracing"
requires-python = ">=3.11,<3.13"
dependencies = [
    "chromadb",
    "ipykernel",
    "jupyter",
    "langchain",
    "langchain-chroma",
    "langchain-community",
    "langchain-openai",
    "langchain-text-splitters",
    "langfuse",
    "openai",
    "pydantic",
    "pypdf",
    "python-dotenv",
    "rich",
    "tiktoken",
]

[dependency-groups]
dev = [
    "pytest",
]

[tool.uv]
package = false
```

Por que usamos cada dependencia:

- `langchain`: prompts, mensajes y composicion de chains.
- `langchain-openai`: `ChatOpenAI` y `OpenAIEmbeddings`.
- `langchain-chroma`: integracion LangChain con ChromaDB.
- `langchain-community`: integraciones auxiliares del ecosistema LangChain.
- `langchain-text-splitters`: partir documentos en chunks.
- `langgraph`: crear el grafo de agentes.
- `langfuse`: tracing y Score API.
- `chromadb`: vector store local.
- `python-dotenv`: cargar `.env`.
- `pydantic`: salida estructurada del router.
- `rich`, `jupyter`, `ipykernel`: soporte de demo y entorno.

Instalar:

```powershell
uv sync
```

Validar:

```powershell
uv run python --version
```

## 3. Variables de entorno y archivos ignorados

### Archivo: `.env.example`

Crear:

```env
OPENAI_API_KEY=your-key-here

LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_BASE_URL=https://cloud.langfuse.com

OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Para region US de Langfuse usar:

```env
LANGFUSE_BASE_URL=https://us.cloud.langfuse.com
```

Por que:

- `.env.example` documenta las variables necesarias.
- No guarda secretos reales.
- Cada alumno crea su propio `.env`.

Crear `.env`:

```powershell
Copy-Item .env.example .env
```

### Archivo: `.gitignore`

Crear:

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
GUION_GRABACION_PIM3.md
```

Por que:

- `.env` contiene claves y no se sube.
- `.venv/` es entorno local.
- `vectorstores/` se regenera desde documentos.
- `GUION_GRABACION_PIM3.md` es material privado de grabacion, no entrega publica.

## 4. Crear documentos para RAG

El RAG necesita documentos reales por dominio.

Crear varios `.md` en:

```txt
data/hr_docs/
data/tech_docs/
data/finance_docs/
```

Ejemplo HR:

```md
# Manual interno de Recursos Humanos - Parte 1

## Vacaciones por antiguedad

Los empleados con menos de un ano tienen 10 dias habiles proporcionales.
Entre 1 y 3 anos tienen 15 dias habiles. Desde 3 anos cumplidos y hasta
5 anos tienen 18 dias habiles. Desde 5 anos en adelante tienen 22 dias
habiles. La solicitud debe cargarse con 15 dias corridos de anticipacion.
```

Ejemplo Tech:

```md
# Manual interno de Soporte Tecnico - Parte 1

## Conexion VPN

Para problemas de VPN se debe verificar primero conexion a internet, estado
del cliente VPN, version instalada y vencimiento del certificado. Si el error
indica credenciales invalidas, el usuario debe reiniciar sesion despues de
cambiar contrasena. Si el error indica tunnel timeout, se debe probar otra red.
```

Ejemplo Finance:

```md
# Manual interno de Finanzas - Parte 1

## Reembolsos y facturas

Los reembolsos de facturas aprobadas se procesan en el siguiente ciclo de pago.
El colaborador debe cargar comprobante, monto, fecha y centro de costo. Finanzas
rechaza comprobantes duplicados o fuera del periodo informado.
```

Por que:

- Sin documentos no hay RAG.
- Cada agente debe consultar solo su dominio.
- Esto permite mostrar fuentes recuperadas.

## 5. Crear paquete Python

### Archivo: `src/__init__.py`

Crear:

```python
"""PIM3 multi-agent RAG package."""
```

Por que:

- Convierte `src` en paquete Python.
- Permite ejecutar `uv run python -m src.main`.

## 6. Configuracion central

### Archivo: `src/config.py`

Crear:

```python
"""Configuracion central del PIM3.

Este modulo concentra rutas, variables de entorno y parametros de RAG para que
el resto del proyecto no tenga configuracion duplicada.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


# Raiz del proyecto PIM3. Se calcula desde este archivo para que el codigo
# funcione igual si se ejecuta desde VS Code, PowerShell o `uv run`.
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
VECTORSTORE_DIR = ROOT_DIR / "vectorstores"

# Mapa entre el intent elegido por el router y la carpeta documental usada
# por cada agente RAG.
DOMAIN_DIRS = {
    "hr": DATA_DIR / "hr_docs",
    "tech": DATA_DIR / "tech_docs",
    "finance": DATA_DIR / "finance_docs",
}


def load_env() -> None:
    # Carga variables desde PIM3/.env si python-dotenv esta instalado.
    # Si falta la dependencia, no rompemos imports ni validaciones simples.
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    # Settings centraliza credenciales, modelos y parametros de retrieval.
    # `frozen=True` evita modificar la configuracion por accidente durante el flujo.
    openai_api_key: str
    openai_model: str
    openai_embedding_model: str
    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_base_url: str
    chunk_size: int = 900
    chunk_overlap: int = 120
    retriever_k: int = 4

    @property
    def has_openai(self) -> bool:
        # Permite separar demo offline de RAG real con embeddings y LLM.
        return bool(self.openai_api_key and self.openai_api_key != "your-key-here")

    @property
    def has_langfuse(self) -> bool:
        # Langfuse es necesario para tracing real, pero no para validar routing.
        return bool(
            self.langfuse_public_key
            and self.langfuse_secret_key
            and self.langfuse_public_key != "pk-lf-xxx"
            and self.langfuse_secret_key != "sk-lf-xxx"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    # Se cachea para leer `.env` una sola vez por proceso.
    load_env()
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        openai_embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
        langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
        langfuse_base_url=os.getenv(
            "LANGFUSE_BASE_URL",
            # Compatibilidad: si un .env viejo usa LANGFUSE_HOST, tambien funciona.
            os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        ),
    )
```

Que explicar:

- `ROOT_DIR`: evita errores de rutas.
- `DOMAIN_DIRS`: conecta router con carpetas.
- `Settings`: centraliza configuracion.
- `has_openai`: activa o desactiva RAG real.
- `has_langfuse`: activa o desactiva tracing.
- `get_settings`: cachea configuracion.

Validar:

```powershell
uv run python -c "from src.config import get_settings; print(get_settings())"
```

## 7. RAG real

### Archivo: `src/rag.py`

Crear:

```python
"""Funciones de RAG real para el PIM3.

Aca viven la carga de documentos, chunking, embeddings, ChromaDB y retrieval.
Los agentes consumen este modulo para obtener contexto antes de responder.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import SecretStr

from src.config import DOMAIN_DIRS, VECTORSTORE_DIR, get_settings


# Versionamos el indice local para no reutilizar vector store viejo si cambia
# la estrategia de chunking.
VECTORSTORE_VERSION = "v2"


def load_documents(folder: Path) -> list:
    """Carga documentos reales desde disco. Para el PI usamos .md/.txt/.csv."""
    from langchain_core.documents import Document

    docs = []
    for path in sorted(folder.rglob("*")):
        # Solo indexamos archivos de texto que el sistema RAG puede leer.
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".csv"}:
            continue
        docs.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                # La metadata permite mostrar fuentes recuperadas en consola.
                metadata={"source": str(path), "file_name": path.name},
            )
        )
    if not docs:
        raise ValueError(f"No hay documentos en {folder}")
    return docs


def split_documents(documents: list) -> list:
    settings = get_settings()
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        # Fallback simple para que la validacion no dependa de todos los extras.
        return split_documents_simple(documents, settings.chunk_size, settings.chunk_overlap)

    # Usamos chunks suficientemente grandes para conservar la politica completa
    # alrededor de cada titulo. Esto evita recuperar solo encabezados.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def split_documents_simple(documents: list, chunk_size: int, chunk_overlap: int) -> list:
    """Fallback para validacion offline si falta el paquete de splitters."""
    from langchain_core.documents import Document

    chunks = []
    for doc in documents:
        text = doc.page_content
        start = 0
        chunk_index = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()
            if chunk_text:
                # Preservamos metadata original y agregamos indice de chunk.
                metadata = {**doc.metadata, "chunk_index": chunk_index}
                chunks.append(Document(page_content=chunk_text, metadata=metadata))
            if end == len(text):
                break
            # El overlap mantiene continuidad entre chunks consecutivos.
            start = max(end - chunk_overlap, start + 1)
            chunk_index += 1
    return chunks


def count_chunks(domain: str) -> int:
    # Usado por `--validate` para comprobar que cada dominio tiene corpus suficiente.
    return len(split_documents(load_documents(DOMAIN_DIRS[domain])))


def build_embeddings():
    settings = get_settings()
    if not settings.has_openai:
        raise RuntimeError("Falta OPENAI_API_KEY para crear embeddings reales.")

    from langchain_openai import OpenAIEmbeddings

    # Embeddings convierte chunks en vectores para busqueda semantica con ChromaDB.
    return OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=SecretStr(settings.openai_api_key),
    )


@lru_cache(maxsize=3)
def get_retriever(domain: str):
    """Crea o carga un retriever ChromaDB por dominio."""
    from langchain_chroma import Chroma

    settings = get_settings()
    folder = DOMAIN_DIRS[domain]
    store_path = VECTORSTORE_DIR / VECTORSTORE_VERSION / domain
    collection_name = f"pim3_{domain}"
    embeddings = build_embeddings()

    if store_path.exists() and any(store_path.iterdir()):
        # Cargar ChromaDB evita recalcular embeddings en cada corrida.
        vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=str(store_path),
            embedding_function=embeddings,
        )
    else:
        chunks = split_documents(load_documents(folder))
        if len(chunks) < 50:
            raise ValueError(f"{domain} tiene {len(chunks)} chunks; minimo esperado: 50")
        # Primera ejecucion: se crean embeddings y se guarda el indice local de ChromaDB.
        store_path.mkdir(parents=True, exist_ok=True)
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=collection_name,
            persist_directory=str(store_path),
        )

    # k define cuantas fuentes se recuperan por pregunta.
    return vectorstore.as_retriever(search_kwargs={"k": settings.retriever_k})


def retrieve_context(domain: str, query: str) -> tuple[str, list[dict[str, Any]]]:
    # Punto de entrada usado por los agentes: dominio + query -> contexto + fuentes.
    retriever = get_retriever(domain)
    docs = retriever.invoke(query)

    context_parts = []
    sources = []
    for index, doc in enumerate(docs, start=1):
        source = doc.metadata.get("file_name") or doc.metadata.get("source") or "documento"
        context_parts.append(f"[{index}] {source}\n{doc.page_content}")
        sources.append({"source": source, "content": doc.page_content, "metadata": doc.metadata})

    # El contexto va al prompt; sources se imprime para trazabilidad local.
    return "\n\n".join(context_parts), sources
```

Que explicar:

- `load_documents`: transforma archivos en objetos `Document`.
- `split_documents`: parte texto para retrieval.
- `chunk_size=900`: evita recuperar solo encabezados.
- `VECTORSTORE_VERSION`: fuerza reconstruccion cuando cambia chunking.
- `build_embeddings`: requiere OpenAI.
- `get_retriever`: crea/carga ChromaDB.
- `retrieve_context`: arma contexto y fuentes.

Validar chunks:

```powershell
uv run python -c "from src.rag import count_chunks; print(count_chunks('hr'))"
```

## 8. Agentes y router

### Archivo: `src/agents.py`

Crear:

```python
"""Nodos y logica de agentes del PIM3.

Define el estado compartido de LangGraph, el router/orquestador y los agentes
especialistas de HR, Tech, Finance y Unknown.
"""

from __future__ import annotations

import unicodedata
from typing import Any, Literal, TypedDict, cast

from pydantic import BaseModel, Field, SecretStr

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
    trace_steps: list[dict[str, Any]]


class RouteDecision(BaseModel):
    # Salida estructurada del router: dominio elegido + explicacion breve.
    intent: Intent = Field(description="Dominio elegido: hr, tech, finance o unknown.")
    reason: str = Field(description="Motivo breve del ruteo.")


# Reglas estables para que la demo no dependa de que el LLM clasifique bien
# consultas basicas como "vacaciones" o "VPN".
KEYWORDS: dict[Intent, list[str]] = {
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
    # Normaliza minusculas y tildes para matchear "contrasena" y variantes.
    normalized = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def keyword_matches(query: str) -> list[Intent]:
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
                api_key=SecretStr(settings.openai_api_key),
            ).with_structured_output(RouteDecision)
            return cast(RouteDecision, (prompt | llm).invoke({"query": query}))
        except Exception:
            # Si falla el router LLM, caemos a unknown en vez de romper la app.
            pass

    return RouteDecision(intent="unknown", reason="La consulta es ambigua o esta fuera de alcance.")


def orchestrator_node(state: AgentState) -> dict[str, Any]:
    # Nodo inicial: clasifica la query y escribe intent + reason en el estado.
    decision = route_query(state["query"])
    trace_steps = [
        {
            "step": "Entrada",
            "detail": "Recibi la consulta del usuario y la prepare para clasificarla.",
        },
        {
            "step": "Clasificacion",
            "detail": f"El orquestador eligio el dominio '{decision.intent}'. Motivo: {decision.reason}",
        },
    ]
    return {"intent": decision.intent, "reason": decision.reason, "trace_steps": trace_steps}


def answer_with_rag(domain: str, state: AgentState) -> dict[str, Any]:
    trace_steps = list(state.get("trace_steps", []))
    trace_steps.append(
        {
            "step": "Agente seleccionado",
            "detail": f"La consulta pasa al agente especialista '{domain}'.",
        }
    )

    settings = get_settings()
    if not settings.has_openai:
        # Modo demo offline: prueba routing y LangGraph sin gastar OpenAI.
        trace_steps.append(
            {
                "step": "Modo offline",
                "detail": "No hay OPENAI_API_KEY disponible; se omite embeddings, ChromaDB y LLM real.",
            }
        )
        return {
            "context": "",
            "sources": [],
            "answer": (
                "El orquestador ya puede rutear esta consulta, pero falta OPENAI_API_KEY "
                "para ejecutar RAG real con embeddings, ChromaDB y LLM."
            ),
            "trace_steps": trace_steps,
        }

    # Recupera contexto real desde el vector store del dominio elegido.
    context, sources = retrieve_context(domain, state["query"])
    source_names = [source["source"] for source in sources]
    trace_steps.append(
        {
            "step": "Busqueda RAG",
            "detail": (
                f"Busque en ChromaDB dentro del dominio '{domain}' y recupere "
                f"{len(sources)} fragmentos relevantes."
            ),
        }
    )
    trace_steps.append(
        {
            "step": "Fuentes",
            "detail": ", ".join(source_names) if source_names else "No se recuperaron fuentes.",
        }
    )

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
    llm = ChatOpenAI(model=settings.openai_model, temperature=0.2, api_key=SecretStr(settings.openai_api_key))
    response = (prompt | llm).invoke({"context": context, "query": state["query"]})
    trace_steps.append(
        {
            "step": "Generacion",
            "detail": "El LLM redacto la respuesta usando solamente el contexto recuperado.",
        }
    )
    # Devolvemos campos parciales; LangGraph los fusiona con el estado existente.
    return {"context": context, "sources": sources, "answer": response.content, "trace_steps": trace_steps}


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
    trace_steps = list(state.get("trace_steps", []))
    trace_steps.append(
        {
            "step": "Fallback",
            "detail": "No se encontro un dominio interno suficientemente claro; no se consulta RAG.",
        }
    )
    return {
        "context": "",
        "sources": [],
        "answer": (
            "No tengo documentacion interna suficiente para responder esa consulta. "
            "Puedo ayudarte con RR. HH., soporte tecnico o finanzas."
        ),
        "trace_steps": trace_steps,
    }
```

Que explicar:

- `AgentState`: contrato del grafo.
- `trace_steps`: log didactico que explica los pasos visibles de ejecucion.
- `RouteDecision`: salida estructurada.
- `KEYWORDS`: router deterministico para casos basicos.
- `route_query`: primero reglas, luego LLM si hace falta.
- `orchestrator_node`: no responde, solo decide.
- `answer_with_rag`: recupera contexto y llama al LLM.
- `unknown_node`: evita inventar.

Validar router:

```powershell
uv run python -c "from src.agents import route_query; print(route_query('que dia salgo de vacaciones'))"
```

## 9. LangGraph

### Archivo: `src/graph.py`

Crear:

```python
"""Definicion del grafo LangGraph del PIM3.

El grafo conecta el orquestador con los agentes especialistas mediante routing
condicional. La evaluacion bonus vive fuera del grafo principal.
"""

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
        "trace_steps": [],
    }
```

Que explicar:

- `StateGraph`: constructor del grafo.
- `START`: punto de entrada.
- `END`: punto final.
- `add_node`: registra funciones como nodos.
- `add_conditional_edges`: pieza central de routing.
- `next_node`: devuelve string, no ejecuta agente.
- No hay evaluator dentro del grafo principal.

Validar grafo:

```powershell
uv run python -c "from src.graph import build_graph; print(build_graph())"
```

## 10. Langfuse

### Archivo: `src/langfuse_setup.py`

Crear:

```python
"""Integracion de Langfuse para tracing.

Este modulo inicializa el cliente de Langfuse, crea el CallbackHandler de
LangChain/LangGraph y fuerza el envio de trazas al cerrar la CLI.
"""

from __future__ import annotations

from typing import Any, cast

from langchain_core.runnables import RunnableConfig

from src.config import get_settings


# Nombre con el que buscamos las ejecuciones en Langfuse.
TRACE_NAME = "pim3-multiagent-rag"
# Cliente global reutilizable: evita crear un cliente por nodo o por callback.
_LANGFUSE_CLIENT: Any | None = None


def get_langfuse_callback(trace_id: str | None = None) -> Any | None:
    # El CallbackHandler conecta LangChain/LangGraph con Langfuse.
    client = get_langfuse_client()
    if client is None:
        return None

    try:
        from langfuse.langchain import CallbackHandler
    except ImportError:
        return None

    settings = get_settings()
    # En langfuse 4.x el callback usa el cliente ya inicializado por public_key.
    trace_context = {"trace_id": trace_id} if trace_id else None
    return CallbackHandler(public_key=settings.langfuse_public_key, trace_context=cast(Any, trace_context))


def get_langfuse_client() -> Any | None:
    global _LANGFUSE_CLIENT
    if _LANGFUSE_CLIENT is not None:
        return _LANGFUSE_CLIENT

    settings = get_settings()
    if not settings.has_langfuse:
        # Sin credenciales reales, la app corre sin tracing remoto.
        return None

    try:
        from langfuse import Langfuse
    except ImportError:
        return None

    # Inicializa el cliente con la region correcta: EU, US, Japan, etc.
    _LANGFUSE_CLIENT = Langfuse(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        base_url=settings.langfuse_base_url,
    )
    return _LANGFUSE_CLIENT


def graph_config(trace_id: str | None = None, metadata: dict[str, Any] | None = None) -> RunnableConfig | None:
    # Config que se pasa a graph.invoke(..., config=config).
    callback = get_langfuse_callback(trace_id=trace_id)
    if callback is None:
        return None
    final_metadata = {"project": "PIM3", "trace_name": TRACE_NAME}
    if metadata:
        final_metadata.update(metadata)
    return {
        "callbacks": [callback],
        "run_name": TRACE_NAME,
        "metadata": final_metadata,
    }


def flush_langfuse() -> None:
    # La CLI termina rapido; flush fuerza el envio antes de cerrar el proceso.
    client = get_langfuse_client()
    if client is not None:
        client.flush()
```

Que explicar:

- `Langfuse`: cliente.
- `CallbackHandler`: conecta LangGraph con Langfuse.
- `trace_id`: permite asociar scores del evaluator bonus al trace correcto.
- `metadata`: permite filtrar en Langfuse.
- `flush_langfuse`: evita perder trazas al cerrar la CLI.

## 11. CLI principal

### Archivo: `src/main.py`

Crear:

```python
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
```

Que explicar:

- `run_query`: ejecuta el grafo.
- `graph_config`: agrega Langfuse si hay credenciales.
- `evidence_preview`: limpia el texto recuperado para mostrar evidencia clara.
- `print_result`: muestra la salida didactica tipo chat con pasos, fuentes y respuesta final.
- `validate`: prueba chunks y routing.
- `main`: CLI con tres modos.

Validar:

```powershell
uv run python -m src.main --validate
uv run python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

## 12. Dataset de routing

### Archivo: `test_queries.json`

Crear:

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

Por que:

- Es un golden dataset minimo.
- Prueba que el router no se rompe.
- Incluye dominios validos y casos `unknown`.

## 13. Evaluator bonus con Score API

### Archivo: `eval_dataset.json`

Crear:

```json
[
  {
    "id": "pim3-001",
    "query": "No puedo conectarme a la VPN desde mi notebook",
    "expected_intent": "tech",
    "expected_keywords": ["vpn", "cliente vpn", "certificado", "credenciales"]
  },
  {
    "id": "pim3-002",
    "query": "que dia salgo de vacaciones",
    "expected_intent": "hr",
    "expected_keywords": ["vacaciones", "antiguedad", "dias habiles", "15 dias"]
  },
  {
    "id": "pim3-003",
    "query": "Cuando se procesa el reembolso de una factura aprobada?",
    "expected_intent": "finance",
    "expected_keywords": ["reembolso", "factura", "aprobada", "pago"]
  },
  {
    "id": "pim3-004",
    "query": "Necesito cambiar mi contrasena del correo corporativo",
    "expected_intent": "tech",
    "expected_keywords": ["contrasena", "correo", "portal", "identidad"]
  },
  {
    "id": "pim3-005",
    "query": "Como se calcula el bono anual de desempeno?",
    "expected_intent": "hr",
    "expected_keywords": ["bono", "desempeno", "objetivos", "compania"]
  },
  {
    "id": "pim3-006",
    "query": "Que documentacion necesito para cargar un gasto de viaje?",
    "expected_intent": "finance",
    "expected_keywords": ["gasto", "viaje", "comprobante", "documentacion"]
  },
  {
    "id": "pim3-007",
    "query": "Cual es la capital de Francia?",
    "expected_intent": "unknown",
    "expected_keywords": ["no tengo documentacion", "rr. hh.", "soporte tecnico", "finanzas"]
  },
  {
    "id": "pim3-008",
    "query": "Tengo un problema con la VPN y ademas quiero pedir vacaciones",
    "expected_intent": "unknown",
    "expected_keywords": ["no tengo documentacion", "rr. hh.", "soporte tecnico", "finanzas"]
  }
]
```

### Archivo: `src/evaluator.py`

Crear:

```python
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
```

Que explicar:

- `eval_dataset.json`: casos esperados.
- `routing_correct`: mide si el router acerto.
- `has_expected_sources`: mide si hubo fuentes cuando debia haberlas.
- `answer_generated`: mide si hubo respuesta.
- `keyword_coverage`: mide cobertura basica de contenido.
- `create_score`: Score API de Langfuse.
- No es nodo del grafo; es evaluacion externa.

Ejecutar:

```powershell
uv run python -m src.evaluator
```

Enviar dataset y scores a Langfuse:

```powershell
uv run python -m src.evaluator --upload-dataset --run-name pim3-demo
```

## 14. Validacion final

Compilar:

```powershell
uv run python -m compileall src
```

Validar routing y chunks:

```powershell
uv run python -m src.main --validate
```

Resultado esperado:

```txt
Chunks por dominio
- hr: 150
- tech: 150
- finance: 150

Routing con test_queries.json
- OK ...
```

Probar query puntual:

```powershell
uv run python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

Probar modo interactivo:

```powershell
uv run python -m src.main
```

Salir:

```txt
salir
```

## 15. Que mostrar en Langfuse

Despues de ejecutar con credenciales reales:

```powershell
uv run python -m src.main --query "Cuando se procesa el reembolso de una factura aprobada?"
```

Mostrar:

- trace `pim3-multiagent-rag`;
- input del usuario;
- ruta elegida;
- llamada al modelo;
- respuesta;
- metadata.

Despues de ejecutar:

```powershell
uv run python -m src.evaluator --upload-dataset --run-name pim3-demo
```

Mostrar:

- dataset `pim3-routing-rag`;
- traces filtrados por `dataset_run=pim3-demo`;
- scores:
  - `routing_correct`;
  - `has_expected_sources`;
  - `answer_generated`;
  - `keyword_coverage`.

## 16. Checklist de rubrica

| Rubrica | Donde se evidencia |
|---|---|
| Multiagente | `src/agents.py`, nodos HR/Tech/Finance/Unknown |
| LangGraph | `src/graph.py`, `StateGraph`, `add_conditional_edges` |
| RAG real | `src/rag.py`, documentos, chunks, embeddings, ChromaDB |
| Fuentes | `retrieve_context()` y salida de consola |
| Langfuse tracing | `src/langfuse_setup.py`, `CallbackHandler` |
| Dataset | `test_queries.json` y `eval_dataset.json` |
| Evaluator bonus | `src/evaluator.py`, `create_score()` |
| Ejecucion con uv | `pyproject.toml`, `.python-version`, `uv run ...` |
| Seguridad | `.env` ignorado por `.gitignore` |

## 17. Orden recomendado para grabar

1. Mostrar estructura final.
2. Crear `.python-version`.
3. Crear `pyproject.toml`.
4. Ejecutar `uv sync`.
5. Crear `.env.example` y `.gitignore`.
6. Mostrar carpetas `data/`.
7. Crear `src/config.py`.
8. Crear `src/rag.py`.
9. Crear `src/agents.py`.
10. Crear `src/graph.py`.
11. Crear `src/langfuse_setup.py`.
12. Crear `src/main.py`.
13. Crear `test_queries.json`.
14. Validar con `uv run python -m src.main --validate`.
15. Ejecutar una query Tech.
16. Ejecutar una query HR.
17. Crear `eval_dataset.json`.
18. Crear `src/evaluator.py`.
19. Ejecutar `uv run python -m src.evaluator`.
20. Mostrar Langfuse.


