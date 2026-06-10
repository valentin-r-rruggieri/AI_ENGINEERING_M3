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
