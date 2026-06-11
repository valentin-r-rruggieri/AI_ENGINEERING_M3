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
