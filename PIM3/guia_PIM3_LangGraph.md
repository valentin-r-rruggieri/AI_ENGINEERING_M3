# Guia paso a paso - PIM3 con LangGraph, RAG real, Langfuse y uv

Esta guia acompania la construccion del PIM3 desde VS Code usando `uv`.

Objetivo: crear un sistema simple y funcional donde una consulta entra por consola, un orquestador clasifica el dominio, LangGraph enruta al agente correcto, el agente recupera contexto documental con RAG y Langfuse traza la ejecucion.

No usamos un agente evaluador dentro del grafo. La evaluacion se revisa directamente en Langfuse mediante traces, datasets, scores o revision manual en la plataforma.

## 0. Resultado final

Flujo:

```txt
query
  |
  v
orquestador
  |
  v
LangGraph add_conditional_edges
  |
  +--> HR RAG Agent ------+
  +--> Tech RAG Agent ----+--> END
  +--> Finance RAG Agent -+
  +--> Unknown -----------+
  |
  v
Langfuse observa la ejecucion con callbacks
```

Estructura:

```txt
PIM3/
|-- README.md
|-- pyproject.toml
|-- .python-version
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- test_queries.json
|-- guia_PIM3_LangGraph.md
|-- GUION_GRABACION_PIM3.md
|
|-- data/
|   |-- hr_docs/
|   |-- tech_docs/
|   `-- finance_docs/
|
`-- src/
    |-- __init__.py
    |-- config.py
    |-- rag.py
    |-- agents.py
    |-- graph.py
    |-- langfuse_setup.py
    `-- main.py
```

## 1. Abrir en VS Code y preparar uv

Abrir VS Code en:

```txt
C:\Users\Usuario\Desktop\Clases\AI_ENGINEERING_M3\PIM3
```

Verificar `uv`:

```powershell
uv --version
```

Sincronizar dependencias:

```powershell
uv sync
```

El proyecto usa:

- `.python-version`: pide Python 3.12.
- `pyproject.toml`: declara dependencias.
- `uv.lock`: lo genera `uv sync`.

Si VS Code pregunta que interprete usar, elegir el de `.venv` creado por `uv`.

Tambien hay tareas listas en `.vscode/tasks.json`:

- `PIM3: uv sync`
- `PIM3: validate`
- `PIM3: query tech`
- `PIM3: query unknown`

En VS Code se pueden ejecutar desde `Terminal > Run Task...`.

## 2. Archivos base

### `.python-version`

```txt
3.12
```

Sirve para que `uv` use una version compatible con `faiss-cpu`.

### `pyproject.toml`

Contiene las dependencias principales:

- `langchain`
- `langchain-openai`
- `langchain-community`
- `langchain-text-splitters`
- `langgraph`
- `langfuse`
- `openai`
- `faiss-cpu`
- `python-dotenv`
- `pydantic`
- `rich`

### `.env.example`

```env
OPENAI_API_KEY=your-key-here

LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_BASE_URL=https://cloud.langfuse.com

OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Crear `.env`:

```powershell
Copy-Item .env.example .env
```

Para validacion offline se puede dejar `OPENAI_API_KEY=your-key-here`.

Para RAG real hay que completar `OPENAI_API_KEY`.

Para trazabilidad completa hay que completar las tres variables de Langfuse. Si tu proyecto esta en la region US, usar `https://us.cloud.langfuse.com`.

## 3. Datos del RAG

Carpetas:

```txt
data/hr_docs
data/tech_docs
data/finance_docs
```

Idea:

- HR responde sobre vacaciones, beneficios, licencias y onboarding.
- Tech responde sobre VPN, correo, contrasenas, soporte y accesos.
- Finance responde sobre facturas, reembolsos, gastos y pagos.

Cada dominio tiene documentos propios. Esto permite demostrar separacion de responsabilidades.

## 4. `src/config.py`

Responsabilidad: centralizar rutas, modelos y credenciales.

Bloques importantes:

```python
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
VECTORSTORE_DIR = ROOT_DIR / "vectorstores"
```

Explicacion: todas las rutas salen de la ubicacion real de `config.py`. Asi el proyecto corre desde VS Code, terminal o `uv run`.

```python
DOMAIN_DIRS = {
    "hr": DATA_DIR / "hr_docs",
    "tech": DATA_DIR / "tech_docs",
    "finance": DATA_DIR / "finance_docs",
}
```

Explicacion: conecta cada intent con su corpus documental.

```python
@dataclass(frozen=True)
class Settings:
```

Explicacion: agrupa configuracion en una clase inmutable.

```python
def has_openai(self) -> bool:
```

Explicacion: permite distinguir demo offline de RAG real.

```python
def has_langfuse(self) -> bool:
```

Explicacion: permite activar Langfuse solo cuando hay credenciales reales.

## 5. `src/rag.py`

Responsabilidad: cargar documentos, partirlos en chunks, crear embeddings, construir FAISS y recuperar contexto.

Flujo:

```txt
documentos -> chunks -> embeddings -> FAISS -> retriever -> contexto
```

Funciones:

### `load_documents(folder)`

Lee `.md`, `.txt` y `.csv`.

Devuelve objetos `Document` de LangChain con:

- `page_content`: texto.
- `metadata`: fuente y nombre de archivo.

### `split_documents(documents)`

Parte documentos largos en chunks.

Usa:

```python
RecursiveCharacterTextSplitter
```

Con separadores pensados para Markdown, parrafos, lineas y oraciones.

### `count_chunks(domain)`

Cuenta chunks por dominio.

Se usa en:

```powershell
uv run python -m src.main --validate
```

### `build_embeddings()`

Crea:

```python
OpenAIEmbeddings
```

Requiere `OPENAI_API_KEY`.

### `get_retriever(domain)`

Crea o carga un indice FAISS por dominio.

Punto clave:

```python
store_path = VECTORSTORE_DIR / VECTORSTORE_VERSION / domain
```

Cada dominio tiene su propio vector store.

`VECTORSTORE_VERSION` evita reutilizar indices viejos cuando cambia la forma de partir documentos.

### `retrieve_context(domain, query)`

Es lo que usan los agentes.

Devuelve:

- contexto textual para el prompt;
- fuentes recuperadas para mostrar trazabilidad local.

## 6. `src/agents.py`

Responsabilidad: definir estado, router, orquestador y agentes especialistas.

### `Intent`

```python
Intent = Literal["hr", "tech", "finance", "unknown"]
```

Limita las rutas validas. El router no puede inventar dominios.

### `AgentState`

Campos:

- `query`
- `intent`
- `reason`
- `context`
- `sources`
- `answer`

No hay `evaluation`. La evaluacion queda fuera del grafo y se hace en Langfuse.

### `RouteDecision`

Salida estructurada del router:

- `intent`
- `reason`

### `KEYWORDS`

Fallback local para validar sin API key.

Ejemplo:

- `vpn` -> tech
- `vacacion` -> hr
- `factura` -> finance

### `route_query(query)`

Primero intenta clasificar con LLM si hay `OPENAI_API_KEY`.

Si no hay API key o la llamada falla, usa keywords.

Regla:

- un dominio claro -> ruta a ese dominio;
- cero dominios -> `unknown`;
- varios dominios mezclados -> `unknown`.

### `orchestrator_node(state)`

Lee:

```python
state["query"]
```

Escribe:

```python
{"intent": decision.intent, "reason": decision.reason}
```

### `answer_with_rag(domain, state)`

Es la funcion comun para HR, Tech y Finance.

Si no hay OpenAI:

- no intenta embeddings;
- no inventa respuesta;
- avisa que falta `OPENAI_API_KEY`.

Si hay OpenAI:

1. llama `retrieve_context(domain, query)`;
2. arma prompt con contexto;
3. llama `ChatOpenAI`;
4. devuelve respuesta y fuentes.

### Nodos especialistas

```python
def hr_agent_node(state):
    return answer_with_rag("hr", state)
```

Misma idea para Tech y Finance.

### `unknown_node(state)`

Responde fuera de alcance.

Esto es importante: cuando no hay contexto confiable, el sistema no inventa.

## 7. `src/langfuse_setup.py`

Responsabilidad: configurar observabilidad.

### `TRACE_NAME`

```python
TRACE_NAME = "pim3-multiagent-rag"
```

Nombre visible en Langfuse.

### `get_langfuse_callback()`

Si no hay credenciales reales:

```python
return None
```

Si hay credenciales:

```python
CallbackHandler(...)
```

Esto permite que LangGraph/LangChain envien trazas a Langfuse.

### `graph_config()`

Devuelve la config que se pasa a:

```python
graph.invoke(...)
```

Con Langfuse activo incluye:

- callbacks;
- run name;
- metadata.

La evaluacion no se implementa como nodo Python. Se realiza en Langfuse revisando traces, datasets, scores o evaluaciones manuales de la plataforma.

## 8. `src/graph.py`

Responsabilidad: conectar nodos con LangGraph.

### `next_node(state)`

Lee:

```python
state.get("intent", "unknown")
```

Devuelve el nombre del siguiente nodo:

- `hr`
- `tech`
- `finance`
- `unknown`

No ejecuta agentes. Solo decide la ruta.

### `build_graph()`

Crea:

```python
graph = StateGraph(AgentState)
```

Registra nodos:

```python
graph.add_node("orchestrator", orchestrator_node)
graph.add_node("hr", hr_agent_node)
graph.add_node("tech", tech_agent_node)
graph.add_node("finance", finance_agent_node)
graph.add_node("unknown", unknown_node)
```

Conecta entrada:

```python
graph.add_edge(START, "orchestrator")
```

Pieza principal de LangGraph:

```python
graph.add_conditional_edges(
    "orchestrator",
    next_node,
    {
        "hr": "hr",
        "tech": "tech",
        "finance": "finance",
        "unknown": "unknown",
    },
)
```

Explicacion:

1. corre `orchestrator`;
2. llama `next_node`;
3. usa el string devuelto para elegir el nodo siguiente.

Finaliza:

```python
graph.add_edge("hr", END)
graph.add_edge("tech", END)
graph.add_edge("finance", END)
graph.add_edge("unknown", END)
```

No hay nodo evaluator.

### `initial_state(query)`

Crea el estado inicial con campos vacios.

## 9. `src/main.py`

Responsabilidad: ejecutar desde consola.

### `run_query(query)`

1. construye el grafo;
2. obtiene config de Langfuse;
3. ejecuta `graph.invoke`.

### `print_result(result)`

Muestra:

- pregunta;
- intent;
- razon;
- respuesta;
- fuentes recuperadas si existen.

No muestra evaluator porque no existe como nodo.

### `validate()`

Comprueba dos cosas:

1. chunks por dominio;
2. routing contra `test_queries.json`.

### `main()`

Modos:

```powershell
uv run python -m src.main --validate
```

```powershell
uv run python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

```powershell
uv run python -m src.main
```

## 10. Validar que funciona

Desde `PIM3`:

```powershell
uv sync
uv run python -m compileall src
uv run python -m src.main --validate
```

Resultado esperado:

```txt
Chunks por dominio
- hr: mas de 50
- tech: mas de 50
- finance: mas de 50

Routing con test_queries.json
- OK ...
```

En esta version del material, la validacion local con `uv run` dio:

```txt
hr: 150
tech: 150
finance: 150
routing: 12/12 OK
```

## 11. Demo offline

Sin API key real:

```powershell
$env:OPENAI_API_KEY='your-key-here'
uv run python -m src.main --query "No puedo conectarme a la VPN desde mi notebook"
```

Resultado esperado:

- intent `tech`;
- razon de routing;
- mensaje indicando que falta `OPENAI_API_KEY` para RAG real.

Esto prueba:

- router;
- LangGraph;
- flujo de consola;
- fallback seguro.

## 12. Demo con OpenAI y Langfuse

Completar `.env`:

```env
OPENAI_API_KEY=...
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

Ejecutar:

```powershell
uv run python -m src.main --query "Cuando se procesa el reembolso de una factura aprobada?"
```

Mostrar en consola:

- intent `finance`;
- respuesta;
- fuentes recuperadas.

Mostrar en Langfuse:

- trace `pim3-multiagent-rag`;
- pasos del grafo;
- llamada al LLM;
- inputs y outputs;
- metadata.

La evaluacion de calidad se hace en Langfuse, no en el grafo.

## 13. Checklist de entrega

El PIM3 esta listo si:

- `uv sync` funciona.
- `uv run python -m compileall src` funciona.
- `uv run python -m src.main --validate` funciona.
- Hay mas de 50 chunks por dominio.
- `test_queries.json` pasa.
- `src/graph.py` usa `add_conditional_edges`.
- `src/langfuse_setup.py` mantiene `CallbackHandler`.
- No existe agente evaluador en el grafo.
- `.env` no se sube.
- Con OpenAI se activa RAG real.
- Con Langfuse se ven trazas.
