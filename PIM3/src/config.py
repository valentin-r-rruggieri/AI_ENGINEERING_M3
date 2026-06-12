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
    langfuse_base_url: str
    chunk_size: int = 900
    chunk_overlap: int = 120
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
        langfuse_base_url=os.getenv(
            "LANGFUSE_BASE_URL",
            os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        ),
    )
