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
