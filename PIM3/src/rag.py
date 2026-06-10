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
