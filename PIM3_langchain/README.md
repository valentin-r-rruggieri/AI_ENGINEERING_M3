# PIM3_langchain - PI basico con LangChain + Langfuse

Este proyecto integrador es una version mas simple del PIM3 completo.

La regla de este PI es:

```txt
No LangGraph.
Si LangChain.
Si RAG real.
Si Langfuse.
```

El objetivo es que el alumno entienda como construir un sistema RAG modular antes de pasar a grafos.

## Flujo

```txt
Usuario pregunta
  |
  v
LangChain clasifica intent
  |
  v
Python enruta a HR / Tech / Finance / Unknown
  |
  v
LangChain retriever recupera contexto real
  |
  v
LangChain prompt + LLM generan respuesta
  |
  v
Langfuse registra trace y evaluator
```

## Estructura

```txt
PIM3_langchain/
|-- README.md
|-- NOTION_GUIA_PASO_A_PASO.md
|-- requirements.txt
|-- .env.example
|-- test_queries.json
|-- data/
|   |-- hr_docs/
|   |-- tech_docs/
|   `-- finance_docs/
`-- src/
    |-- main.py
    |-- config.py
    |-- rag.py
    |-- chains.py
    |-- langfuse_setup.py
    `-- __init__.py
```

## Que hace cada archivo

- `config.py`: rutas, variables de entorno, modelos y settings.
- `rag.py`: carga documentos, divide chunks, crea embeddings, crea FAISS y devuelve retrievers.
- `chains.py`: contiene routing, respuesta RAG, fallback, evaluator y `handle_query`.
- `langfuse_setup.py`: configura callbacks y scores de Langfuse.
- `main.py`: CLI para probar consultas y validacion offline.

## Instalacion

```bash
cd PIM3_langchain
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Completar `.env`:

```env
OPENAI_API_KEY=your-key-here

LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=https://cloud.langfuse.com

OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## Ejecutar

Validar chunks y routing offline:

```bash
python -m src.main --validate
```

Ejecutar una consulta:

```bash
python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

Modo interactivo:

```bash
python -m src.main
```

## Que se aprende

- Como usar LangChain para construir un router con salida estructurada.
- Como usar loaders, splitters, embeddings, vectorstores y retrievers.
- Como generar respuestas usando solo contexto recuperado.
- Como integrar Langfuse sin cambiar la logica principal.
- Como evaluar una respuesta RAG con un evaluator simple.

## Diferencia con PIM3

`PIM3` usa LangGraph para declarar el flujo como grafo.

`PIM3_langchain` usa LangChain y Python normal para mantener el foco en:

- cadenas;
- retrievers;
- prompts;
- tracing;
- RAG real.

