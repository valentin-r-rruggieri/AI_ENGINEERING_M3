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
