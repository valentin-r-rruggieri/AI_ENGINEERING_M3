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
trace en Langfuse + evaluator bonus
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
- `test_queries.json` para validar routing;
- evaluator bonus para registrar scores.

## Estructura

```txt
PIM3/
|-- README.md
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
    |-- langfuse_setup.py
    `-- evaluator.py
```

## Archivos principales

- `src/config.py`: carga `.env`, rutas y nombres de modelos.
- `src/rag.py`: carga documentos, divide chunks, crea embeddings, crea FAISS y devuelve retrievers.
- `src/agents.py`: define el orquestador, los agentes HR/Tech/Finance y el fallback Unknown.
- `src/graph.py`: arma el `StateGraph` con routing condicional.
- `src/langfuse_setup.py`: configura callback de Langfuse y registro de scores.
- `src/evaluator.py`: bonus, evalua la respuesta y registra scores.
- `src/main.py`: ejecuta consultas y validacion offline.

## Instalacion

Windows:

```bash
cd PIM3
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Linux/macOS:

```bash
cd PIM3
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Nota: si `faiss-cpu` no instala con Python 3.14, usar Python 3.10, 3.11 o 3.12.

## Configuracion

Completar `.env`:

```env
OPENAI_API_KEY=your-key-here

LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=https://cloud.langfuse.com

OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Sin `OPENAI_API_KEY`, el proyecto puede validar chunks y routing offline, pero no puede ejecutar embeddings, FAISS ni respuestas RAG reales.

## Ejecucion

Modo interactivo:

```bash
python -m src.main
```

Consulta puntual:

```bash
python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

Validacion offline:

```bash
python -m src.main --validate
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
- El evaluator es bonus: mide calidad, pero no agrega complejidad al flujo principal.

## Limitaciones

- La calidad de las respuestas depende de los documentos.
- Las consultas ambiguas se mandan a `unknown`.
- El vector store local se guarda en `vectorstores/` y se puede borrar para regenerar.
- El evaluator no reemplaza revision humana.
