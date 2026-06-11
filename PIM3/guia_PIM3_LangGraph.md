# Guia lecture exacta - PIM3 LangGraph + RAG real + Langfuse

Esta guia esta escrita para que una persona pueda crear el proyecto integrador sin tener que decidir arquitectura ni inventar codigo.

La idea es construir una version profesional pero simple del E23:

```txt
Usuario pregunta
  -> orquestador clasifica
  -> LangGraph enruta
  -> agente RAG especializado recupera contexto
  -> LLM responde usando documentos
  -> evaluator puntua
  -> Langfuse traza el flujo
```

## 0. Que vamos a construir

El proyecto se llama `PIM3`.

La estructura final sera:

```txt
PIM3/
|-- README.md
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- test_queries.json
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
    |-- evaluator.py
    |-- langfuse_setup.py
    `-- main.py
```

## 1. Crear archivos base

### 1.1 Crear `.env.example`

Este archivo no guarda claves reales. Es una plantilla para que cada alumno cree su propio `.env`.

Archivo: `PIM3/.env.example`

```env
OPENAI_API_KEY=your-key-here

LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=https://cloud.langfuse.com

OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Explicacion:

- `OPENAI_API_KEY`: permite usar `ChatOpenAI` y `OpenAIEmbeddings`.
- `LANGFUSE_PUBLIC_KEY`: identifica el proyecto de Langfuse.
- `LANGFUSE_SECRET_KEY`: autoriza el envio de traces y scores.
- `LANGFUSE_HOST`: URL de Langfuse Cloud.
- `OPENAI_MODEL`: modelo usado para clasificar, responder y evaluar.
- `OPENAI_EMBEDDING_MODEL`: modelo usado para convertir texto en vectores.

### 1.2 Crear `.gitignore`

Archivo: `PIM3/.gitignore`

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

Explicacion:

- `.env`: no se sube porque contiene secretos.
- `.venv/` y `venv/`: entornos locales, no forman parte del codigo.
- `__pycache__/` y `*.py[cod]`: cache de Python.
- `vectorstores/`: se regenera desde documentos, no hace falta versionarlo.
- `*.log`: logs locales.

### 1.3 Crear `requirements.txt`

Archivo: `PIM3/requirements.txt`

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
rich
```

Explicacion de dependencias:

- `langchain`: prompts, parsers, documentos y composicion.
- `langchain-openai`: `ChatOpenAI` y `OpenAIEmbeddings`.
- `langchain-community`: vector store FAISS.
- `langchain-text-splitters`: splitters de texto.
- `langgraph`: grafo multiagente.
- `langfuse`: tracing y scores.
- `openai`: cliente base de OpenAI.
- `faiss-cpu`: vector store local.
- `tiktoken`: conteo/tokenizacion usada por ecosistema OpenAI.
- `python-dotenv`: carga `.env`.
- `pydantic`: modelos estructurados.
- `rich`: salida opcional mas linda en consola.

## 2. Crear documentos

Crear estas carpetas:

```txt
PIM3/data/hr_docs/
PIM3/data/tech_docs/
PIM3/data/finance_docs/
```

Cada carpeta debe tener documentos `.md`, `.txt` o `.csv`.

Idea:

- HR responde con documentos de RR. HH.
- Tech responde con documentos de soporte tecnico.
- Finance responde con documentos de finanzas.

Esto es importante porque un agente especialista no deberia responder usando documentos de otro dominio.

## 3. Crear `src/__init__.py`

Archivo: `PIM3/src/__init__.py`

```python
"""PIM3 multi-agent RAG package."""
```

Explicacion:

- El archivo puede estar casi vacio.
- Su existencia convierte `src` en un paquete Python.
- Eso permite ejecutar `python -m src.main`.

## 4. Crear `src/config.py`

Este archivo centraliza rutas y configuracion.

Si no existiera, cada archivo tendria que leer variables de entorno por separado. Eso vuelve el proyecto desordenado.

Archivo completo:

```python
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
VECTORSTORE_DIR = ROOT_DIR / "vectorstores"

DOMAIN_DIRS = {
    "hr": DATA_DIR / "hr_docs",
    "tech": DATA_DIR / "tech_docs",
    "finance": DATA_DIR / "finance_docs",
}


def load_env() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
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
        return bool(self.openai_api_key and self.openai_api_key != "your-key-here")

    @property
    def has_langfuse(self) -> bool:
        return bool(
            self.langfuse_public_key
            and self.langfuse_secret_key
            and self.langfuse_public_key != "pk-lf-xxx"
            and self.langfuse_secret_key != "sk-lf-xxx"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
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

### 4.1 Imports

```python
from __future__ import annotations
```

Permite usar type hints modernos sin problemas de evaluacion temprana.

```python
import os
```

Sirve para leer variables de entorno como `OPENAI_API_KEY`.

```python
from dataclasses import dataclass
```

Permite definir una clase de configuracion sin escribir constructor manual.

```python
from functools import lru_cache
```

Sirve para cachear `get_settings()` y no reconstruir settings muchas veces.

```python
from pathlib import Path
```

Maneja rutas de archivos de forma portable.

### 4.2 Rutas del proyecto

```python
ROOT_DIR = Path(__file__).resolve().parents[1]
```

`__file__` es la ruta de `config.py`.

`resolve()` la convierte en ruta absoluta.

`parents[1]` sube desde `src/config.py` hasta `PIM3/`.

```python
DATA_DIR = ROOT_DIR / "data"
```

Construye la ruta `PIM3/data`.

```python
VECTORSTORE_DIR = ROOT_DIR / "vectorstores"
```

Define donde guardar los indices FAISS.

```python
DOMAIN_DIRS = {...}
```

Relaciona cada intent con su carpeta documental.

Ejemplo:

- `hr` usa `data/hr_docs`;
- `tech` usa `data/tech_docs`;
- `finance` usa `data/finance_docs`.

### 4.3 Carga de `.env`

```python
def load_env() -> None:
```

Define una funcion que no devuelve nada.

```python
try:
    from dotenv import load_dotenv
except ImportError:
    return
```

Si `python-dotenv` no esta instalado, el programa no explota. Simplemente no carga `.env`.

```python
load_dotenv(ROOT_DIR / ".env")
```

Lee variables desde `PIM3/.env`.

### 4.4 Clase `Settings`

```python
@dataclass(frozen=True)
class Settings:
```

`@dataclass` crea automaticamente `__init__`.

`frozen=True` hace que la configuracion no se modifique por accidente.

Campos:

- `openai_api_key`: clave de OpenAI.
- `openai_model`: modelo de chat.
- `openai_embedding_model`: modelo de embeddings.
- `langfuse_public_key`: public key de Langfuse.
- `langfuse_secret_key`: secret key de Langfuse.
- `langfuse_host`: host de Langfuse.
- `chunk_size`: tamano maximo de chunks.
- `chunk_overlap`: solapamiento entre chunks.
- `retriever_k`: cuantos chunks recuperar.

### 4.5 Propiedad `has_openai`

```python
@property
def has_openai(self) -> bool:
```

Permite preguntar `settings.has_openai` como si fuera atributo.

```python
return bool(self.openai_api_key and self.openai_api_key != "your-key-here")
```

Devuelve `True` solo si hay una key real y no el placeholder.

### 4.6 Propiedad `has_langfuse`

Valida que existan las dos keys de Langfuse y que no sean placeholders.

Esto permite que el proyecto corra sin Langfuse en modo local.

### 4.7 Funcion `get_settings`

```python
@lru_cache(maxsize=1)
```

Guarda el resultado. La configuracion se crea una sola vez.

```python
load_env()
```

Antes de leer variables, carga `.env`.

```python
os.getenv("OPENAI_MODEL", "gpt-4o-mini")
```

Lee variable de entorno. Si no existe, usa valor por defecto.

## 5. Crear `src/rag.py`

Este archivo implementa RAG real.

RAG significa:

```txt
Documentos -> chunks -> embeddings -> FAISS -> retriever -> contexto -> LLM
```

Archivo completo:

```python
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from src.config import DOMAIN_DIRS, VECTORSTORE_DIR, get_settings


def load_documents(folder: Path) -> list:
    """Carga documentos reales desde disco. Para el PI usamos .md/.txt/.csv."""
    from langchain_core.documents import Document

    docs = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".csv"}:
            continue
        docs.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
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
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
        except ImportError:
            return split_documents_simple(documents, settings.chunk_size, settings.chunk_overlap)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
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
                metadata = {**doc.metadata, "chunk_index": chunk_index}
                chunks.append(Document(page_content=chunk_text, metadata=metadata))
            if end == len(text):
                break
            start = max(end - chunk_overlap, start + 1)
            chunk_index += 1
    return chunks


def count_chunks(domain: str) -> int:
    return len(split_documents(load_documents(DOMAIN_DIRS[domain])))


def build_embeddings():
    settings = get_settings()
    if not settings.has_openai:
        raise RuntimeError("Falta OPENAI_API_KEY para crear embeddings reales.")

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
    )


@lru_cache(maxsize=3)
def get_retriever(domain: str):
    """Crea o carga un retriever FAISS por dominio."""
    from langchain_community.vectorstores import FAISS

    settings = get_settings()
    folder = DOMAIN_DIRS[domain]
    store_path = VECTORSTORE_DIR / domain
    embeddings = build_embeddings()

    if store_path.exists():
        vectorstore = FAISS.load_local(
            str(store_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )
    else:
        chunks = split_documents(load_documents(folder))
        if len(chunks) < 50:
            raise ValueError(f"{domain} tiene {len(chunks)} chunks; minimo esperado: 50")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        store_path.mkdir(parents=True, exist_ok=True)
        vectorstore.save_local(str(store_path))

    return vectorstore.as_retriever(search_kwargs={"k": settings.retriever_k})


def retrieve_context(domain: str, query: str) -> tuple[str, list[dict[str, Any]]]:
    retriever = get_retriever(domain)
    docs = retriever.invoke(query)

    context_parts = []
    sources = []
    for index, doc in enumerate(docs, start=1):
        source = doc.metadata.get("file_name") or doc.metadata.get("source") or "documento"
        context_parts.append(f"[{index}] {source}\n{doc.page_content}")
        sources.append({"source": source, "content": doc.page_content, "metadata": doc.metadata})

    return "\n\n".join(context_parts), sources
```

### 5.1 `load_documents`

Funcion:

```python
def load_documents(folder: Path) -> list:
```

Recibe una carpeta y devuelve una lista de `Document`.

```python
from langchain_core.documents import Document
```

`Document` es el formato estandar de LangChain para texto recuperable.

```python
docs = []
```

Lista donde se acumulan documentos.

```python
for path in sorted(folder.rglob("*")):
```

Recorre todos los archivos dentro de la carpeta y subcarpetas.

```python
if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".csv"}:
    continue
```

Ignora carpetas y archivos no soportados.

```python
page_content=path.read_text(encoding="utf-8")
```

Lee el contenido textual.

```python
metadata={"source": str(path), "file_name": path.name}
```

Guarda fuente para poder mostrar de donde salio la respuesta.

```python
if not docs:
    raise ValueError(...)
```

Si no hay documentos, el RAG no puede funcionar.

### 5.2 `split_documents`

Objetivo: partir documentos largos en fragmentos.

Por que:

- un LLM no debe recibir toda la documentacion;
- el vector store busca por fragmentos;
- fragmentos mas chicos mejoran retrieval.

```python
settings = get_settings()
```

Lee `chunk_size` y `chunk_overlap`.

```python
RecursiveCharacterTextSplitter
```

Splitter de LangChain que intenta cortar respetando separadores.

```python
separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""]
```

Orden de preferencia:

1. titulos markdown;
2. parrafos;
3. lineas;
4. oraciones;
5. espacios;
6. cualquier caracter.

### 5.3 `split_documents_simple`

Fallback local.

Existe para que `--validate` pueda contar chunks incluso si falta el paquete de splitters.

No reemplaza el splitter real en produccion, pero evita que una clase se bloquee por una dependencia.

### 5.4 `build_embeddings`

```python
if not settings.has_openai:
    raise RuntimeError(...)
```

Sin API key no hay embeddings reales.

```python
OpenAIEmbeddings(...)
```

Convierte cada chunk en un vector numerico.

Ese vector permite buscar por significado, no solo por palabras exactas.

### 5.5 `get_retriever`

```python
@lru_cache(maxsize=3)
```

Cachea un retriever por dominio:

- HR;
- Tech;
- Finance.

```python
store_path = VECTORSTORE_DIR / domain
```

Cada dominio tiene su propio indice FAISS.

```python
if store_path.exists():
    FAISS.load_local(...)
```

Si ya existe, no recalcula embeddings.

```python
FAISS.from_documents(chunks, embeddings)
```

Si no existe, crea el vector store desde cero.

```python
vectorstore.as_retriever(search_kwargs={"k": settings.retriever_k})
```

Convierte FAISS en retriever.

`k` indica cuantos chunks devuelve por consulta.

### 5.6 `retrieve_context`

```python
retriever = get_retriever(domain)
```

Obtiene el retriever correcto segun dominio.

```python
docs = retriever.invoke(query)
```

Busca chunks relevantes para la query.

```python
context_parts.append(...)
```

Convierte chunks en texto para el prompt.

```python
sources.append(...)
```

Guarda fuentes para mostrar/debuggear.

```python
return "\n\n".join(context_parts), sources
```

Devuelve dos cosas:

- contexto textual para el LLM;
- fuentes para inspeccion humana.

## 6. Crear `src/agents.py`

Este archivo contiene los nodos del grafo.

En LangGraph un nodo es una funcion que recibe `state` y devuelve un `dict`.

Archivo completo:

```python
from __future__ import annotations

from typing import Any, Literal, TypedDict

from pydantic import BaseModel, Field

from src.config import get_settings
from src.rag import retrieve_context


Intent = Literal["hr", "tech", "finance", "unknown"]


class AgentState(TypedDict):
    query: str
    intent: str
    reason: str
    context: str
    sources: list[dict[str, Any]]
    answer: str
    evaluation: dict[str, Any]


class RouteDecision(BaseModel):
    intent: Intent = Field(description="Dominio elegido: hr, tech, finance o unknown.")
    reason: str = Field(description="Motivo breve del ruteo.")


KEYWORDS = {
    "hr": ["vacacion", "licencia", "beneficio", "bono", "desempeno", "onboarding", "estudio"],
    "tech": ["vpn", "2fa", "doble factor", "contrasena", "correo", "notebook", "soporte", "acceso"],
    "finance": ["factura", "pago", "reembolso", "reintegro", "gasto", "viaje", "finanzas", "metodo"],
}


def route_query(query: str) -> RouteDecision:
    """Router simple como E23. Si hay API key, se puede apoyar en LLM."""
    settings = get_settings()
    if settings.has_openai:
        try:
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_openai import ChatOpenAI

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Clasifica la consulta en hr, tech, finance o unknown. "
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
            pass

    q = query.lower()
    matched = [domain for domain, words in KEYWORDS.items() if any(word in q for word in words)]
    if len(matched) == 1:
        return RouteDecision(intent=matched[0], reason=f"Se detectaron senales claras de {matched[0]}.")
    return RouteDecision(intent="unknown", reason="La consulta es ambigua o esta fuera de alcance.")


def orchestrator_node(state: AgentState) -> dict:
    decision = route_query(state["query"])
    return {"intent": decision.intent, "reason": decision.reason}


def answer_with_rag(domain: str, state: AgentState) -> dict:
    settings = get_settings()
    if not settings.has_openai:
        return {
            "context": "",
            "sources": [],
            "answer": (
                "El orquestador ya puede rutear esta consulta, pero falta OPENAI_API_KEY "
                "para ejecutar RAG real con embeddings, FAISS y LLM."
            ),
        }

    context, sources = retrieve_context(domain, state["query"])

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"Sos un agente especialista de {domain}. "
                "Responde usando unicamente el contexto provisto. "
                "Si el contexto no alcanza, deci que no tenes informacion suficiente.",
            ),
            ("human", "Contexto:\n{context}\n\nConsulta:\n{query}\n\nRespuesta:"),
        ]
    )
    llm = ChatOpenAI(model=settings.openai_model, temperature=0.2, api_key=settings.openai_api_key)
    response = (prompt | llm).invoke({"context": context, "query": state["query"]})
    return {"context": context, "sources": sources, "answer": response.content}


def hr_agent_node(state: AgentState) -> dict:
    return answer_with_rag("hr", state)


def tech_agent_node(state: AgentState) -> dict:
    return answer_with_rag("tech", state)


def finance_agent_node(state: AgentState) -> dict:
    return answer_with_rag("finance", state)


def unknown_node(state: AgentState) -> dict:
    return {
        "context": "",
        "sources": [],
        "answer": (
            "No tengo documentacion interna suficiente para responder esa consulta. "
            "Puedo ayudarte con RR. HH., soporte tecnico o finanzas."
        ),
    }
```

### 6.1 `Intent`

```python
Intent = Literal["hr", "tech", "finance", "unknown"]
```

Limita las rutas validas.

No queremos que el router invente `sales`, `legal` o `billing` si no existen en el grafo.

### 6.2 `AgentState`

`AgentState` es el contrato del grafo.

Campos:

- `query`: pregunta original.
- `intent`: dominio elegido.
- `reason`: razon del routing.
- `context`: chunks recuperados.
- `sources`: fuentes recuperadas.
- `answer`: respuesta final.
- `evaluation`: scores del evaluator.

### 6.3 `RouteDecision`

Pydantic model para salida estructurada del router.

```python
intent: Intent
```

Obliga a usar una ruta valida.

```python
reason: str
```

Explica por que se tomo esa ruta.

### 6.4 `KEYWORDS`

Fallback local.

Sirve para:

- validar sin API key;
- mostrar comportamiento basico;
- evitar que todo el proyecto dependa de OpenAI para una demo simple.

### 6.5 `route_query`

Primero intenta usar LLM si hay API key.

```python
if settings.has_openai:
```

Si hay credenciales, se usa router con modelo.

```python
ChatPromptTemplate.from_messages(...)
```

Define instruccion del clasificador.

```python
.with_structured_output(RouteDecision)
```

Hace que el modelo devuelva algo compatible con `RouteDecision`.

```python
except Exception:
    pass
```

Si falla el LLM, cae al fallback por keywords.

Luego:

```python
q = query.lower()
```

Normaliza texto.

```python
matched = [...]
```

Detecta dominios mencionados.

```python
if len(matched) == 1:
```

Solo acepta ruta si hay un unico dominio claro.

Si hay cero o mas de uno, devuelve `unknown`.

### 6.6 `orchestrator_node`

```python
decision = route_query(state["query"])
```

Lee la pregunta del estado y clasifica.

```python
return {"intent": decision.intent, "reason": decision.reason}
```

Devuelve solo los campos que modifica.

LangGraph fusiona este dict con el estado.

### 6.7 `answer_with_rag`

Funcion comun para HR, Tech y Finance.

Evita repetir logica.

```python
if not settings.has_openai:
```

Sin API key no intenta embeddings ni LLM.

```python
context, sources = retrieve_context(domain, state["query"])
```

Hace retrieval real.

```python
prompt = ChatPromptTemplate.from_messages(...)
```

Construye prompt con contexto.

```python
f"Sos un agente especialista de {domain}."
```

Especializa el comportamiento por dominio.

```python
"Responde usando unicamente el contexto provisto."
```

Guardrail anti hallucination.

```python
response = (prompt | llm).invoke(...)
```

Ejecuta chain LangChain.

```python
return {"context": context, "sources": sources, "answer": response.content}
```

Devuelve campos que el grafo necesita.

### 6.8 Nodos especialistas

```python
def hr_agent_node(state): return answer_with_rag("hr", state)
```

Cada nodo fija su dominio.

No hay logica duplicada.

### 6.9 `unknown_node`

Responde sin RAG.

Se usa para:

- fuera de alcance;
- ambiguedad;
- consultas no internas.

## 7. Crear `src/evaluator.py`

El evaluator mide la calidad de la respuesta.

Archivo completo:

```python
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from src.config import get_settings
from src.langfuse_setup import score_current_trace


class Evaluation(BaseModel):
    relevance: int = Field(ge=1, le=10)
    completeness: int = Field(ge=1, le=10)
    accuracy: int = Field(ge=1, le=10)
    clarity: int = Field(ge=1, le=10)
    overall: float = Field(ge=1, le=10)
    feedback: str


def evaluator_node(state: dict[str, Any]) -> dict[str, Any]:
    evaluation = evaluate(state)
    score_current_trace(
        {
            "relevance": float(evaluation.relevance),
            "completeness": float(evaluation.completeness),
            "accuracy": float(evaluation.accuracy),
            "clarity": float(evaluation.clarity),
            "overall": float(evaluation.overall),
        },
        evaluation.feedback,
    )
    return {"evaluation": evaluation.model_dump()}


def evaluate(state: dict[str, Any]) -> Evaluation:
    settings = get_settings()
    if not settings.has_openai:
        return Evaluation(
            relevance=6,
            completeness=5,
            accuracy=6,
            clarity=7,
            overall=6.0,
            feedback="Evaluacion local simple: para score real configurar OPENAI_API_KEY.",
        )

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Evalua la respuesta RAG de 1 a 10 en relevance, completeness, accuracy, clarity y overall. "
                "Si inventa informacion no presente en el contexto, baja accuracy. Devuelve salida estructurada.",
            ),
            (
                "human",
                "Query:\n{query}\n\nIntent:\n{intent}\n\nContexto:\n{context}\n\nRespuesta:\n{answer}",
            ),
        ]
    )
    llm = ChatOpenAI(
        model=settings.openai_model,
        temperature=0,
        api_key=settings.openai_api_key,
    ).with_structured_output(Evaluation)
    return (prompt | llm).invoke(state)
```

### 7.1 `Evaluation`

Define score estructurado:

- `relevance`: responde a la pregunta.
- `completeness`: cubre suficiente informacion.
- `accuracy`: esta soportada por contexto.
- `clarity`: es entendible.
- `overall`: score general.
- `feedback`: comentario cualitativo.

`Field(ge=1, le=10)` fuerza escala 1 a 10.

### 7.2 `evaluator_node`

Es un nodo de LangGraph.

```python
evaluation = evaluate(state)
```

Calcula evaluacion.

```python
score_current_trace(...)
```

Intenta registrar scores en Langfuse.

```python
return {"evaluation": evaluation.model_dump()}
```

Agrega evaluacion al estado final.

### 7.3 `evaluate`

Si no hay OpenAI:

```python
return Evaluation(...)
```

Devuelve score local fijo para que la demo no falle.

Si hay OpenAI:

```python
ChatPromptTemplate.from_messages(...)
```

Construye prompt de evaluacion.

```python
.with_structured_output(Evaluation)
```

Obliga al LLM a devolver el formato esperado.

## 8. Crear `src/langfuse_setup.py`

Este archivo separa observabilidad de logica de negocio.

Archivo completo:

```python
from __future__ import annotations

from typing import Any

from src.config import get_settings


TRACE_NAME = "pim3-multiagent-rag"


def get_langfuse_callback() -> Any | None:
    settings = get_settings()
    if not settings.has_langfuse:
        return None

    try:
        from langfuse.langchain import CallbackHandler
    except ImportError:
        return None

    try:
        return CallbackHandler(public_key=settings.langfuse_public_key)
    except TypeError:
        return CallbackHandler(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )


def graph_config() -> dict[str, Any]:
    callback = get_langfuse_callback()
    if callback is None:
        return {}
    return {
        "callbacks": [callback],
        "run_name": TRACE_NAME,
        "metadata": {"project": "PIM3", "trace_name": TRACE_NAME},
    }


def score_current_trace(scores: dict[str, float], comment: str) -> None:
    settings = get_settings()
    if not settings.has_langfuse:
        return

    try:
        from langfuse import Langfuse

        client = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )
        for name, value in scores.items():
            client.score_current_trace(name=name, value=value, comment=comment)
    except Exception:
        # Langfuse no debe romper la demo del PI si falta contexto de trace.
        return
```

### 8.1 `TRACE_NAME`

Nombre que aparece en Langfuse.

### 8.2 `get_langfuse_callback`

```python
if not settings.has_langfuse:
    return None
```

Permite correr sin Langfuse.

```python
from langfuse.langchain import CallbackHandler
```

Callback que LangChain/LangGraph usan para enviar traces.

```python
try ... except TypeError
```

Compatibilidad entre versiones de Langfuse.

### 8.3 `graph_config`

Devuelve config para `graph.invoke`.

Si no hay callback:

```python
return {}
```

Si hay callback:

```python
{"callbacks": [callback], "run_name": ..., "metadata": ...}
```

### 8.4 `score_current_trace`

Registra scores del evaluator.

Si falla, no rompe la demo.

Observabilidad nunca debe tirar abajo el flujo principal de clase.

## 9. Crear `src/graph.py`

Este archivo es el corazon de LangGraph.

Archivo completo:

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
    intent = state.get("intent", "unknown")
    if intent in {"hr", "tech", "finance"}:
        return intent
    return "unknown"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("hr", hr_agent_node)
    graph.add_node("tech", tech_agent_node)
    graph.add_node("finance", finance_agent_node)
    graph.add_node("unknown", unknown_node)
    graph.add_node("evaluator", evaluator_node)

    graph.add_edge(START, "orchestrator")
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
    graph.add_edge("hr", "evaluator")
    graph.add_edge("tech", "evaluator")
    graph.add_edge("finance", "evaluator")
    graph.add_edge("unknown", END)
    graph.add_edge("evaluator", END)

    return graph.compile()


def initial_state(query: str) -> AgentState:
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

### 9.1 Imports

```python
from langgraph.graph import END, START, StateGraph
```

Tres piezas clave:

- `StateGraph`: constructor del grafo.
- `START`: entrada.
- `END`: salida.

### 9.2 `next_node`

```python
intent = state.get("intent", "unknown")
```

Lee intent producido por `orchestrator`.

```python
if intent in {"hr", "tech", "finance"}:
    return intent
```

Si el intent es valido, devuelve el nombre de la ruta.

```python
return "unknown"
```

Fallback seguro.

Importante:

`next_node` no ejecuta agentes. Solo devuelve un string.

### 9.3 `build_graph`

```python
graph = StateGraph(AgentState)
```

Crea grafo con contrato de estado.

```python
graph.add_node("orchestrator", orchestrator_node)
```

Registra nodo.

```python
graph.add_edge(START, "orchestrator")
```

Todo empieza en orquestador.

```python
graph.add_conditional_edges(...)
```

Esta es la pieza mas importante de E08/PIM3.

Traduccion:

```txt
Despues de orchestrator, llama next_node.
Si next_node devuelve "hr", ir a nodo "hr".
Si devuelve "tech", ir a nodo "tech".
...
```

```python
graph.add_edge("hr", "evaluator")
```

Las rutas RAG pasan por evaluator.

```python
graph.add_edge("unknown", END)
```

Unknown termina directo, no evalua RAG porque no hubo contexto.

```python
return graph.compile()
```

Valida y compila el grafo.

### 9.4 `initial_state`

Define estado inicial para cada query.

Todos los campos existen desde el inicio.

Eso hace que la salida sea predecible.

## 10. Crear `src/main.py`

Este archivo permite ejecutar desde consola.

Archivo completo:

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents import route_query
from src.config import DOMAIN_DIRS, ROOT_DIR
from src.graph import build_graph, initial_state
from src.langfuse_setup import graph_config
from src.rag import count_chunks


def run_query(query: str) -> dict:
    graph = build_graph()
    config = graph_config()
    if config:
        return graph.invoke(initial_state(query), config=config)
    return graph.invoke(initial_state(query))


def print_result(result: dict) -> None:
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
```

### 10.1 Imports

```python
argparse
```

Permite `--query` y `--validate`.

```python
json
```

Lee `test_queries.json`.

```python
sys` y `Path`
```

Permiten ejecutar tanto `python -m src.main` como `python src/main.py`.

### 10.2 Ajuste de path

```python
if __package__ is None or __package__ == "":
```

Detecta ejecucion directa.

```python
sys.path.insert(...)
```

Agrega raiz del proyecto al import path.

### 10.3 `run_query`

```python
graph = build_graph()
```

Construye grafo.

```python
config = graph_config()
```

Obtiene callbacks de Langfuse si existen.

```python
if config:
    return graph.invoke(..., config=config)
```

Ejecuta con tracing.

```python
return graph.invoke(...)
```

Ejecuta sin tracing.

### 10.4 `print_result`

Imprime:

- pregunta;
- intent;
- razon;
- respuesta;
- fuentes;
- evaluator.

Esto ayuda a debuggear sin abrir Langfuse.

### 10.5 `validate`

Comprueba:

- chunks por dominio;
- routing esperado.

```python
ok = ok and total >= 50
```

El PI exige suficiente corpus para RAG.

```python
passed = decision.intent == item["expected_intent"]
```

Compara salida del router contra dataset esperado.

### 10.6 `main`

Define tres modos:

```bash
python -m src.main --validate
```

Valida.

```bash
python -m src.main --query "..."
```

Ejecuta una pregunta.

```bash
python -m src.main
```

Modo interactivo.

## 11. Crear `test_queries.json`

Archivo:

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

Explicacion:

- Cada objeto tiene query y resultado esperado.
- Sirve como golden dataset minimo.
- Incluye casos HR, Tech, Finance, Unknown y ambiguos.

## 12. Instalar y ejecutar

```bash
cd PIM3
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Completar `.env`.

Validar:

```bash
python -m src.main --validate
```

Ejecutar:

```bash
python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

## 13. Como explicar el flujo completo en clase

Una query entra por `main.py`.

`main.py` llama:

```python
run_query(query)
```

`run_query` construye el grafo:

```python
build_graph()
```

El grafo arranca en:

```txt
START -> orchestrator
```

El orquestador llama:

```python
route_query(...)
```

El resultado decide:

```txt
hr -> hr_agent_node
tech -> tech_agent_node
finance -> finance_agent_node
unknown -> unknown_node
```

Los agentes RAG llaman:

```python
retrieve_context(domain, query)
```

`retrieve_context` usa:

```txt
FAISS retriever -> chunks relevantes -> contexto
```

El agente responde con LLM.

Luego pasa por evaluator.

Langfuse observa todo si hay credenciales.

## 14. Checklist final

El proyecto esta completo si:

- `python -m compileall src` no falla.
- `python -m src.main --validate` pasa.
- Hay minimo 50 chunks por dominio.
- `add_conditional_edges` existe en `graph.py`.
- No hay API keys hardcodeadas.
- `.env` no se sube.
- Langfuse se activa solo si hay credenciales.
- Unknown responde sin inventar.

