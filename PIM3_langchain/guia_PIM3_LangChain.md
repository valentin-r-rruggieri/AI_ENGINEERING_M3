# Guia Notion exacta - PIM3_langchain

Esta guia esta pensada para copiar y pegar. No asume que el alumno sepa programar.

El proyecto usa solo LangChain + Langfuse. No usa LangGraph.

## 1. Crear carpeta y estructura

Crear una carpeta llamada `PIM3_langchain` con esta estructura:

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
src/chains.py
src/config.py
src/langfuse_setup.py
src/main.py
src/rag.py
test_queries.json
```

## 2. Crear `.env.example`

Archivo: `PIM3_langchain/.env.example`

```env
OPENAI_API_KEY=your-key-here

LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=https://cloud.langfuse.com

OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## 3. Crear `.gitignore`

Archivo: `PIM3_langchain/.gitignore`

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

## 4. Crear `requirements.txt`

Archivo: `PIM3_langchain/requirements.txt`

```txt
langchain
langchain-openai
langchain-community
langchain-text-splitters
langfuse
openai
faiss-cpu
tiktoken
python-dotenv
pydantic
rich
```

## 5. Crear `test_queries.json`

Archivo: `PIM3_langchain/test_queries.json`

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

## 6. Copiar documentos

Crear estas carpetas y copiar los documentos `.md` incluidos en el proyecto:

```txt
data/hr_docs/
data/tech_docs/
data/finance_docs/
```

Estos documentos son la base del RAG. Sin documentos no hay retrieval.

## 7. Crear `src/__init__.py`

Copiar este archivo completo:

```python
"""PIM3 LangChain-only project."""
```

Que hace este archivo:

## 8. Crear `src/config.py`

Copiar este archivo completo:

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
        langfuse_host=os.getenv("LANGFUSE_HOST", os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")),
    )
```

Que hace este archivo:

- Define rutas del proyecto.
- Carga variables desde `.env`.
- Centraliza nombres de modelos y credenciales.

## 9. Crear `src/rag.py`

Copiar este archivo completo:

```python
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from src.config import DOMAIN_DIRS, VECTORSTORE_DIR, get_settings


def load_documents(folder: Path) -> list:
    """Load real documents from disk using LangChain Document objects."""
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
        raise ValueError(f"No documents found in {folder}")
    return docs


def split_documents(documents: list) -> list:
    """Split documents into chunks before embedding them."""
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
    """Offline fallback for validation if the splitter package is missing."""
    from langchain_core.documents import Document

    chunks = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.page_content):
            end = min(start + chunk_size, len(doc.page_content))
            text = doc.page_content[start:end].strip()
            if text:
                chunks.append(Document(page_content=text, metadata={**doc.metadata, "chunk_index": index}))
            if end == len(doc.page_content):
                break
            start = max(end - chunk_overlap, start + 1)
            index += 1
    return chunks


def count_chunks(domain: str) -> int:
    return len(split_documents(load_documents(DOMAIN_DIRS[domain])))


def build_embeddings():
    settings = get_settings()
    if not settings.has_openai:
        raise RuntimeError("OPENAI_API_KEY is required for real embeddings.")

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(model=settings.openai_embedding_model, api_key=settings.openai_api_key)


@lru_cache(maxsize=3)
def get_retriever(domain: str):
    """Build or load a FAISS retriever for one domain."""
    from langchain_community.vectorstores import FAISS

    settings = get_settings()
    store_path = VECTORSTORE_DIR / domain
    embeddings = build_embeddings()

    if store_path.exists():
        vectorstore = FAISS.load_local(
            str(store_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )
    else:
        chunks = split_documents(load_documents(DOMAIN_DIRS[domain]))
        if len(chunks) < 50:
            raise ValueError(f"{domain} has only {len(chunks)} chunks; expected at least 50.")
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
        source = doc.metadata.get("file_name") or doc.metadata.get("source") or "internal_doc"
        context_parts.append(f"[{index}] {source}\n{doc.page_content}")
        sources.append({"source": source, "content": doc.page_content, "metadata": doc.metadata})

    return "\n\n".join(context_parts), sources
```

Que hace este archivo:

- Carga documentos reales.
- Divide documentos en chunks.
- Crea embeddings.
- Crea o carga FAISS.
- Devuelve contexto recuperado para una query.

## 10. Crear `src/langfuse_setup.py`

Copiar este archivo completo:

```python
from __future__ import annotations

from typing import Any

from src.config import get_settings


TRACE_NAME = "pim3-langchain-rag"


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


def invoke_config(metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    callback = get_langfuse_callback()
    if callback is None:
        return {}
    return {
        "callbacks": [callback],
        "run_name": TRACE_NAME,
        "metadata": metadata or {},
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
        return
```

Que hace este archivo:

- Crea callback de Langfuse.
- Arma config para traces.
- Registra scores del evaluator.

## 11. Crear `src/chains.py`

Copiar este archivo completo:

```python
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from src.config import get_settings
from src.langfuse_setup import invoke_config, score_current_trace
from src.rag import retrieve_context


Intent = Literal["hr", "tech", "finance", "unknown"]


class RouteDecision(BaseModel):
    intent: Intent = Field(description="Selected route.")
    reason: str = Field(description="Short explanation for the route.")


class Evaluation(BaseModel):
    relevance: int = Field(ge=1, le=10)
    completeness: int = Field(ge=1, le=10)
    accuracy: int = Field(ge=1, le=10)
    clarity: int = Field(ge=1, le=10)
    overall: float = Field(ge=1, le=10)
    feedback: str


KEYWORDS = {
    "hr": ["vacacion", "licencia", "beneficio", "bono", "desempeno", "onboarding", "estudio"],
    "tech": ["vpn", "2fa", "doble factor", "contrasena", "correo", "notebook", "soporte", "acceso"],
    "finance": ["factura", "pago", "reembolso", "reintegro", "gasto", "viaje", "finanzas", "metodo"],
}


def classify_intent(query: str) -> RouteDecision:
    """Classify with LangChain when keys exist; otherwise use a transparent fallback."""
    settings = get_settings()
    if not settings.has_openai:
        return keyword_route(query)

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
    llm = ChatOpenAI(model=settings.openai_model, temperature=0, api_key=settings.openai_api_key)
    chain = prompt | llm.with_structured_output(RouteDecision)
    return chain.invoke({"query": query}, config=invoke_config({"step": "routing"}))


def keyword_route(query: str) -> RouteDecision:
    q = query.lower()
    matched = [domain for domain, words in KEYWORDS.items() if any(word in q for word in words)]
    if len(matched) == 1:
        return RouteDecision(intent=matched[0], reason=f"Ruta local por palabras clave: {matched[0]}.")
    return RouteDecision(intent="unknown", reason="Consulta ambigua o fuera de alcance.")


def answer_domain(domain: str, query: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.has_openai:
        return {
            "answer": "Routing disponible, pero falta OPENAI_API_KEY para ejecutar RAG real.",
            "context": "",
            "sources": [],
        }

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    context, sources = retrieve_context(domain, query)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Sos un agente especialista de {domain}. "
                "Responde usando unicamente el contexto provisto. "
                "Si el contexto no alcanza, deci que no tenes informacion suficiente.",
            ),
            ("human", "Contexto:\n{context}\n\nConsulta:\n{query}\n\nRespuesta:"),
        ]
    )
    llm = ChatOpenAI(model=settings.openai_model, temperature=0.2, api_key=settings.openai_api_key)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke(
        {"domain": domain, "context": context, "query": query},
        config=invoke_config({"step": "rag_generation", "domain": domain}),
    )
    return {"answer": answer, "context": context, "sources": sources}


def fallback_answer() -> dict[str, Any]:
    return {
        "answer": "No tengo documentacion interna suficiente. Puedo ayudar con HR, Tech o Finance.",
        "context": "",
        "sources": [],
    }


def evaluate_answer(query: str, intent: str, context: str, answer: str) -> Evaluation:
    settings = get_settings()
    if not settings.has_openai:
        return Evaluation(
            relevance=6,
            completeness=5,
            accuracy=6,
            clarity=7,
            overall=6.0,
            feedback="Evaluacion local simple porque falta OPENAI_API_KEY.",
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
            ("human", "Query:\n{query}\n\nIntent:\n{intent}\n\nContexto:\n{context}\n\nRespuesta:\n{answer}"),
        ]
    )
    llm = ChatOpenAI(model=settings.openai_model, temperature=0, api_key=settings.openai_api_key)
    chain = prompt | llm.with_structured_output(Evaluation)
    evaluation = chain.invoke(
        {"query": query, "intent": intent, "context": context, "answer": answer},
        config=invoke_config({"step": "evaluation"}),
    )
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
    return evaluation


def handle_query(query: str) -> dict[str, Any]:
    route = classify_intent(query)

    if route.intent in {"hr", "tech", "finance"}:
        rag_result = answer_domain(route.intent, query)
        evaluation = evaluate_answer(query, route.intent, rag_result["context"], rag_result["answer"])
    else:
        rag_result = fallback_answer()
        evaluation = {}

    return {
        "query": query,
        "intent": route.intent,
        "reason": route.reason,
        "answer": rag_result["answer"],
        "sources": rag_result["sources"],
        "evaluation": evaluation.model_dump() if hasattr(evaluation, "model_dump") else evaluation,
    }
```

Que hace este archivo:

- Clasifica la consulta.
- Ejecuta RAG segun dominio.
- Genera respuesta con LangChain.
- Evalua respuesta.

## 12. Crear `src/main.py`

Copiar este archivo completo:

```python
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
```

Que hace este archivo:

- Expone CLI.
- Permite `--validate`.
- Permite `--query`.

## Ejecutar

```bash
cd PIM3_langchain
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m src.main --validate
python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

## Resultado esperado

El alumno debe ver routing, respuesta, fuentes y evaluator. Si no hay API key, el sistema debe avisar que falta `OPENAI_API_KEY`.
