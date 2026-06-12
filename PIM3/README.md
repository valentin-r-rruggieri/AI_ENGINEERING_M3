# PIM3 - E23 evolucionado con RAG real, LangGraph y Langfuse

Este proyecto es el integrador del Modulo 3. La idea no es construir una mega arquitectura enterprise, sino una version profesional y simple del E23 multiagente:

```txt
query
  |
  v
orquestador
  |
  v
routing condicional con LangGraph
  |
  +--> HR RAG Agent
  +--> Tech RAG Agent
  +--> Finance RAG Agent
  +--> Unknown
  |
  v
respuesta usando documentos recuperados
  |
  v
trace en Langfuse
```

## Que agrega sobre E23

E23 trabajaba la idea central con documentos en memoria y retrieval simple. Este PI mantiene esa forma mental, pero reemplaza el RAG simulado por RAG real:

- documentos reales en `data/hr_docs`, `data/tech_docs` y `data/finance_docs`;
- chunking con LangChain;
- embeddings de OpenAI;
- vector store FAISS;
- retriever por dominio;
- LangGraph con `add_conditional_edges`;
- trazabilidad con Langfuse;
- `test_queries.json` para validar routing.

## Estructura

```txt
PIM3/
|-- README.md
|-- pyproject.toml
|-- .python-version
|-- requirements.txt
|-- .env.example
|-- test_queries.json
|
|-- data/
|   |-- hr_docs/
|   |-- tech_docs/
|   `-- finance_docs/
|
`-- src/
    |-- main.py
    |-- config.py
    |-- rag.py
    |-- agents.py
    |-- graph.py
    `-- langfuse_setup.py
```

## Archivos principales

- `src/config.py`: carga `.env`, rutas y nombres de modelos.
- `src/rag.py`: carga documentos, divide chunks, crea embeddings, crea FAISS y devuelve retrievers.
- `src/agents.py`: define el orquestador, los agentes HR/Tech/Finance y el fallback Unknown.
- `src/graph.py`: arma el `StateGraph` con routing condicional.
- `src/langfuse_setup.py`: configura callback de Langfuse para trazabilidad.
- `src/main.py`: ejecuta consultas y validacion offline.

## Instalacion con uv

Este proyecto esta preparado para ejecutarse desde VS Code usando `uv`.

Desde VS Code:

1. Abrir la carpeta `PIM3`.
2. Abrir la terminal integrada.
3. Ejecutar:

```bash
uv sync
uv run python -m src.main --validate
```

Tambien quedan tareas listas en VS Code:

- `PIM3: uv sync`
- `PIM3: validate`
- `PIM3: query tech`
- `PIM3: query unknown`

Para una consulta puntual:

```bash
uv run python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

`uv` usa `.python-version` y `pyproject.toml`, por eso no depende del Python global de la maquina. El proyecto pide Python 3.11 o 3.12 porque `faiss-cpu` puede fallar en versiones mas nuevas.

`requirements.txt` queda como respaldo para instalaciones tradicionales, pero el flujo recomendado es `uv`.

## Configuracion

Crear `.env` desde `.env.example`:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Luego completar:

```env
OPENAI_API_KEY=your-key-here

LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_BASE_URL=https://cloud.langfuse.com

OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Sin `OPENAI_API_KEY`, el proyecto puede validar chunks y routing offline, pero no puede ejecutar embeddings, FAISS ni respuestas RAG reales.

Langfuse forma parte del proyecto. Para la demo completa, completar `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` y `LANGFUSE_BASE_URL`; la evaluacion de calidad se realiza directamente en Langfuse, no con un agente evaluador dentro del grafo.

## Ejecucion

Modo interactivo:

```bash
uv run python -m src.main
```

Consulta puntual:

```bash
uv run python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

Validacion offline:

```bash
uv run python -m src.main --validate
```

La validacion comprueba:

- minimo 50 chunks por dominio;
- routing esperado de `test_queries.json`.

## Ejemplos esperados

```txt
Input: Cuantos dias de vacaciones tengo si llevo 3 anos?
Intent: hr
Respuesta: basada en documentos de data/hr_docs
```

```txt
Input: No puedo conectarme a la VPN desde mi notebook
Intent: tech
Respuesta: basada en documentos de data/tech_docs
```

```txt
Input: Cuando se procesa el reembolso de una factura aprobada?
Intent: finance
Respuesta: basada en documentos de data/finance_docs
```

```txt
Input: Cual es la capital de Francia?
Intent: unknown
Respuesta: fallback fuera de alcance
```

## Decisiones tecnicas

- El orquestador es simple y visible, como en E23.
- El routing vive dentro de LangGraph con `add_conditional_edges`.
- Cada agente tiene su propio dominio y su propio retriever.
- El RAG usa documentos reales, chunks, embeddings y FAISS.
- Langfuse se integra como callback para que cada request quede trazada.
- La evaluacion se revisa en Langfuse, usando traces, datasets, scores o evaluaciones manuales desde la plataforma.

## Limitaciones

- La calidad de las respuestas depende de los documentos.
- Las consultas ambiguas se mandan a `unknown`.
- El vector store local se guarda en `vectorstores/` y se puede borrar para regenerar.
- La evaluacion de calidad no vive en el grafo: se realiza en Langfuse para no mezclar orquestacion con evaluacion.
