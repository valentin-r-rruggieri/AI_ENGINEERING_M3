# PIM3_STARTER - Construyendo el PI paso a paso

Este starter es la version guiada para que los alumnos lleguen al `PIM3` final sin copiar una arquitectura gigante.

La idea es tomar el E23 multiagente simple y evolucionarlo:

```txt
E23:
query -> orquestador -> agente especialista -> docs en memoria -> respuesta

PIM3:
query -> LangGraph -> agente RAG especializado -> documentos reales -> FAISS -> respuesta -> Langfuse
```

## Objetivo del starter

Construir de a poco un sistema multiagente con:

- orquestador;
- routing condicional con LangGraph;
- agentes `hr`, `tech`, `finance` y `unknown`;
- RAG real con LangChain + FAISS;
- trazabilidad con Langfuse;
- evaluator bonus.

## Estructura

```txt
PIM3_STARTER/
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

## Que archivos editan los alumnos

| Archivo | Se edita | Que se aprende |
|---|---:|---|
| `src/config.py` | Poco | Variables de entorno y rutas del proyecto |
| `src/rag.py` | Si | Loaders, chunks, embeddings, FAISS y retrievers |
| `src/agents.py` | Si | Orquestador, agentes especialistas y prompts RAG |
| `src/graph.py` | Si | `StateGraph`, nodos y `add_conditional_edges` |
| `src/langfuse_setup.py` | Si | Callback de Langfuse y trazabilidad |
| `src/evaluator.py` | Bonus | Scores automaticos de calidad |
| `src/main.py` | Poco | CLI simple para probar el flujo |

## Paso 0 - Preparar entorno

```bash
cd PIM3_STARTER
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Completar `.env` con las keys.

Sin `OPENAI_API_KEY`, se puede leer el codigo y compilar, pero no se puede ejecutar RAG real.

## Paso 1 - Entender los documentos

Revisar:

- `data/hr_docs`
- `data/tech_docs`
- `data/finance_docs`

Cada carpeta representa el conocimiento de un agente. Esto reemplaza los `DOCS = {...}` en memoria del E23.

## Paso 2 - Completar `rag.py`

Objetivo:

1. cargar archivos desde cada carpeta;
2. dividir texto en chunks;
3. crear embeddings;
4. crear o cargar FAISS;
5. devolver contexto recuperado.

Checkpoint esperado:

```bash
python -m compileall src
```

## Paso 3 - Completar `agents.py`

Objetivo:

1. definir el estado compartido;
2. crear el router;
3. crear `hr_agent_node`, `tech_agent_node`, `finance_agent_node`;
4. crear `unknown_node`;
5. hacer que cada agente use `retrieve_context(...)`.

## Paso 4 - Completar `graph.py`

Objetivo:

1. crear `StateGraph`;
2. agregar nodos;
3. conectar `START -> orchestrator`;
4. usar `add_conditional_edges`;
5. conectar agentes a `evaluator`;
6. compilar el grafo.

Este es el corazon de LangGraph.

## Paso 5 - Completar Langfuse

En `langfuse_setup.py`, configurar el callback para que cada corrida quede trazada.

El trace debe mostrar:

- query original;
- decision del orquestador;
- agente usado;
- retrieval;
- generacion del LLM;
- score del evaluator si se completa el bonus.

## Paso 6 - Probar desde consola

```bash
python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

Otros casos:

```bash
python -m src.main --query "Cuantos dias de vacaciones tengo si llevo 3 anos?"
python -m src.main --query "Cuando se procesa el reembolso de una factura aprobada?"
python -m src.main --query "Cual es la capital de Francia?"
```

## Criterio de finalizacion

El starter esta resuelto cuando:

- el grafo usa `add_conditional_edges`;
- cada dominio usa documentos propios;
- el RAG usa chunks, embeddings, FAISS y retriever;
- las respuestas usan contexto recuperado;
- Langfuse recibe traces;
- `test_queries.json` cubre HR, Tech, Finance y Unknown.

Para comparar, mirar la carpeta `../PIM3` solo despues de intentar resolverlo.
