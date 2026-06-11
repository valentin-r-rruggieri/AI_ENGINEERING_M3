# Guia Lecture 4 - Langfuse desde cero hasta uso avanzado

Esta guia esta pensada para acompaniar la Lecture 4.

Objetivo:

```txt
Entender que agrega Langfuse a un sistema con LangChain y LangGraph.
```

La guia cubre:

1. instalacion;
2. configuracion de credenciales;
3. primer trace;
4. uso con LangChain;
5. uso con LangGraph;
6. metadata, tags y run names;
7. scores/evaluator;
8. como leer la interfaz de Langfuse;
9. que capturas agregar para clase.

No intenta construir un PI completo. Se enfoca solo en Langfuse.

---

# 1. Que es Langfuse

Langfuse es una herramienta de observabilidad para aplicaciones con LLMs.

En una app comun podemos imprimir logs:

```python
print("respuesta:", respuesta)
```

Pero en sistemas con LLM eso no alcanza, porque necesitamos ver:

- que input entro;
- que prompt se envio;
- que modelo respondio;
- cuanto tardo;
- que nodo del grafo corrio;
- que ruta tomo el router;
- que respuesta genero;
- si el evaluator dio buen o mal score.

Langfuse organiza esa informacion en:

```txt
Trace
  -> observations / spans
  -> generations
  -> scores
  -> metadata
```

## 1.1 Trace

Un trace representa una ejecucion completa.

Ejemplo:

```txt
Usuario pregunta: "No puedo conectarme a la VPN"
```

Todo lo que pasa para responder esa consulta vive dentro de un trace.

## 1.2 Span / Observation

Un span representa un paso dentro del flujo.

Ejemplos:

- router;
- agente tecnico;
- retrieval;
- evaluator;
- llamada a una herramienta.

## 1.3 Generation

Una generation es una llamada a un LLM.

Ejemplos:

- clasificar intent;
- generar respuesta final;
- evaluar calidad.

## 1.4 Score

Un score es una metrica asociada a un trace.

Ejemplos:

- `routing_accuracy`;
- `relevance`;
- `accuracy`;
- `clarity`;
- `overall`.

---

# 2. Instalacion

En notebooks:

```python
!pip install -q langfuse langchain langchain-openai langgraph
```

Explicacion:

- `langfuse`: SDK para enviar traces.
- `langchain`: base de prompts/chains/callbacks.
- `langchain-openai`: integracion con OpenAI.
- `langgraph`: grafo de agentes.

En proyecto local:

```bash
pip install langfuse langchain langchain-openai langgraph
```

---

# 3. Credenciales

En Langfuse Cloud:

1. abrir el proyecto;
2. ir a `Settings`;
3. entrar a `API Keys`;
4. copiar:
   - Public Key;
   - Secret Key;
   - Host/Base URL.

En notebook:

```python
import os
from getpass import getpass

os.environ["LANGFUSE_PUBLIC_KEY"] = getpass("Langfuse Public Key: ")
os.environ["LANGFUSE_SECRET_KEY"] = getpass("Langfuse Secret Key: ")
os.environ["LANGFUSE_BASE_URL"] = "https://cloud.langfuse.com"

os.environ["OPENAI_API_KEY"] = getpass("OpenAI API Key: ")

print("Credenciales configuradas.")
```

Explicacion linea por linea:

```python
import os
```

Permite guardar credenciales como variables de entorno.

```python
from getpass import getpass
```

Permite pegar claves sin que aparezcan visibles en la celda.

```python
os.environ["LANGFUSE_PUBLIC_KEY"] = ...
```

Guarda la public key para que el SDK de Langfuse la pueda leer.

```python
os.environ["LANGFUSE_SECRET_KEY"] = ...
```

Guarda la secret key para autorizar escritura de traces.

```python
os.environ["LANGFUSE_BASE_URL"] = "https://cloud.langfuse.com"
```

Define a que servidor enviar traces.

```python
os.environ["OPENAI_API_KEY"] = ...
```

OpenAI es necesario porque los ejemplos llaman al LLM.

> Nota: en algunos proyectos tambien se usa `LANGFUSE_HOST`. En notebooks de clase usamos `LANGFUSE_BASE_URL`, y en proyectos Python puede usarse `LANGFUSE_HOST`. Ambos representan la URL del servidor.

---

# 4. Primer ejemplo: LangChain sin Langfuse

Primero ejecutamos una chain normal.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Sos un asistente breve y claro."),
    ("human", "Explica en una frase que es un trace.")
])

chain = prompt | llm | StrOutputParser()

result = chain.invoke({})
print(result)
```

## Que hace cada parte

```python
ChatPromptTemplate
```

Crea el prompt como mensajes estructurados.

```python
ChatOpenAI
```

Cliente del modelo.

```python
StrOutputParser
```

Convierte `AIMessage` en texto.

```python
prompt | llm | StrOutputParser()
```

LCEL: salida del prompt entra al LLM, salida del LLM entra al parser.

Problema: esto funciona, pero no queda registrado en ningun lugar visual.

---

# 5. Agregar Langfuse a una chain

La diferencia principal es esta:

```python
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

result = chain.invoke(
    {},
    config={
        "callbacks": [langfuse_handler],
        "run_name": "primer_trace_langchain",
        "metadata": {"lecture": "M3L4", "example": "basic_chain"}
    }
)
```

Ejemplo completo:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Sos un asistente breve y claro."),
    ("human", "Explica en una frase que es un trace.")
])

chain = prompt | llm | StrOutputParser()

langfuse_handler = CallbackHandler()

result = chain.invoke(
    {},
    config={
        "callbacks": [langfuse_handler],
        "run_name": "primer_trace_langchain",
        "metadata": {
            "lecture": "M3L4",
            "component": "langchain_chain",
        },
    },
)

print(result)
```

## Que agregamos

```python
from langfuse.langchain import CallbackHandler
```

Importa el callback que conecta LangChain con Langfuse.

```python
langfuse_handler = CallbackHandler()
```

Crea el handler. Lee credenciales desde variables de entorno.

```python
config={"callbacks": [langfuse_handler]}
```

Le dice a LangChain: "cuando ejecutes, avisale a Langfuse".

```python
"run_name": "primer_trace_langchain"
```

Nombre legible del trace/run.

```python
"metadata": {...}
```

Datos extra para filtrar despues en la interfaz.

---

# 6. Espacio para captura: primer trace

Agregar captura de pantalla aca:

```txt
[PEGAR IMAGEN: listado de traces donde aparece primer_trace_langchain]
```

Que mostrar:

- columna de nombre;
- timestamp;
- modelo;
- latencia;
- si aparece metadata.

Explicacion para alumnos:

> Este trace representa una ejecucion completa de la chain. Antes solo veíamos el print en la notebook. Ahora podemos abrir la ejecucion, inspeccionar input, output, modelo y duracion.

---

# 7. Langfuse con LangGraph basico

Ahora usamos el patron de M3L4 E08:

```txt
START -> chatbot_node -> END
```

Codigo completo:

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def chatbot_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(State)
builder.add_node("chatbot", chatbot_node)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()

langfuse_handler = CallbackHandler()

result = graph.invoke(
    {"messages": [HumanMessage(content="Explica que es LangGraph en una frase.")]},
    config={
        "callbacks": [langfuse_handler],
        "run_name": "m3l4_e08_langgraph_basico",
        "metadata": {"lecture": "M3L4", "exercise": "E08"},
    },
)

print(result["messages"][-1].content)
```

## Explicacion bloque por bloque

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
```

Define el estado del grafo.

`messages` guarda historial.

`add_messages` hace que los mensajes se acumulen en lugar de reemplazarse.

```python
def chatbot_node(state: State) -> dict:
```

Nodo del grafo.

Recibe todo el estado.

```python
response = llm.invoke(state["messages"])
```

Llama al LLM con el historial.

```python
return {"messages": [response]}
```

Devuelve solo el nuevo mensaje.

```python
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
```

Declara flujo lineal.

```python
graph.invoke(..., config={"callbacks": [langfuse_handler]})
```

Ejecuta el grafo y envia trace a Langfuse.

---

# 8. Espacio para captura: trace de LangGraph basico

Agregar captura:

```txt
[PEGAR IMAGEN: trace con nodo chatbot y generation del modelo]
```

Que senalar:

- trace completo;
- observation/span del nodo;
- generation del LLM;
- input del usuario;
- output del modelo.

---

# 9. Langfuse con router condicional

Ahora usamos el patron de M3L4 E09:

```txt
START -> router_node -> conditional_edges -> agente -> END
```

Codigo:

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langfuse.langchain import CallbackHandler


class AgentState(TypedDict):
    query: str
    intent: str
    response: str


def route_query(query: str) -> str:
    q = query.lower()
    if "vpn" in q or "login" in q or "contrasena" in q:
        return "tech"
    if "vacaciones" in q or "licencia" in q:
        return "hr"
    if "factura" in q or "pago" in q or "reembolso" in q:
        return "finance"
    return "general"


def router_node(state: AgentState) -> dict:
    return {"intent": route_query(state["query"])}


def tech_node(state: AgentState) -> dict:
    return {"response": "TechAgent: revisa VPN, 2FA y abre ticket si persiste."}


def hr_node(state: AgentState) -> dict:
    return {"response": "HRAgent: revisa el portal de RR. HH. y solicita aprobacion."}


def finance_node(state: AgentState) -> dict:
    return {"response": "FinanceAgent: revisa facturas, pagos y comprobantes."}


def general_node(state: AgentState) -> dict:
    return {"response": "GeneralAgent: necesito mas informacion para ayudarte."}


def route_to_node(state: AgentState) -> str:
    if state["intent"] == "tech":
        return "tech_node"
    if state["intent"] == "hr":
        return "hr_node"
    if state["intent"] == "finance":
        return "finance_node"
    return "general_node"


builder = StateGraph(AgentState)
builder.add_node("router_node", router_node)
builder.add_node("tech_node", tech_node)
builder.add_node("hr_node", hr_node)
builder.add_node("finance_node", finance_node)
builder.add_node("general_node", general_node)

builder.add_edge(START, "router_node")
builder.add_conditional_edges(
    "router_node",
    route_to_node,
    {
        "tech_node": "tech_node",
        "hr_node": "hr_node",
        "finance_node": "finance_node",
        "general_node": "general_node",
    },
)

for node_name in ["tech_node", "hr_node", "finance_node", "general_node"]:
    builder.add_edge(node_name, END)

graph = builder.compile()

langfuse_handler = CallbackHandler()

result = graph.invoke(
    {"query": "No puedo conectarme a la VPN", "intent": "", "response": ""},
    config={
        "callbacks": [langfuse_handler],
        "run_name": "m3l4_e09_router_condicional",
        "metadata": {
            "lecture": "M3L4",
            "exercise": "E09",
            "router_version": "keywords_v1",
        },
    },
)

print(result)
```

## Que tiene que verse en Langfuse

Un trace con:

- input: query del usuario;
- metadata: lecture, exercise, router version;
- ruta ejecutada;
- output final.

En este ejemplo los agentes no llaman LLM, por eso puede no haber generation en cada agente. Lo importante aca es ver la ruta.

---

# 10. Espacio para captura: router condicional

Agregar captura:

```txt
[PEGAR IMAGEN: trace donde se ve router_node y tech_node]
```

Que marcar con flechas:

- `router_node`;
- `intent=tech`;
- `tech_node`;
- metadata `router_version`;
- output final.

---

# 11. Metadata y tags

La metadata permite filtrar traces.

Ejemplo:

```python
config={
    "callbacks": [langfuse_handler],
    "run_name": "router_test",
    "metadata": {
        "lecture": "M3L4",
        "exercise": "E09",
        "router_version": "v1",
        "dataset": "golden_dataset_demo",
        "student_group": "cohort_2026",
    },
}
```

Uso:

- filtrar por lecture;
- comparar versiones de router;
- encontrar ejecuciones de un dataset;
- separar grupos de alumnos.

---

# 12. Scores con Langfuse

Los scores sirven para medir calidad.

Ejemplo conceptual:

```txt
trace de una query
  -> score routing_accuracy = 1
  -> score relevance = 8
  -> score clarity = 9
```

Codigo:

```python
from langfuse import Langfuse

langfuse = Langfuse()

langfuse.score_current_trace(
    name="routing_accuracy",
    value=1.0,
    comment="El router eligio tech y era el intent esperado.",
)

langfuse.score_current_trace(
    name="quality",
    value=0.85,
    comment="La respuesta es util, pero podria incluir pasos mas concretos.",
)
```

## Explicacion

```python
Langfuse()
```

Crea cliente de Langfuse usando variables de entorno.

```python
score_current_trace(...)
```

Agrega score al trace activo.

```python
name="routing_accuracy"
```

Nombre de la metrica.

```python
value=1.0
```

Valor numerico.

```python
comment="..."
```

Explicacion humana del score.

> Nota: `score_current_trace` funciona cuando hay un trace activo. Si no hay contexto activo, se puede usar `create_score(trace_id=...)` con un `trace_id` explicito.

---

# 13. Evaluator automatico + score

En un sistema mas avanzado, el evaluator puede ser una funcion o un LLM-as-judge.

Ejemplo simple:

```python
def evaluate_response(expected_intent: str, actual_intent: str, response: str) -> dict:
    routing_accuracy = 1.0 if expected_intent == actual_intent else 0.0
    has_response = 1.0 if len(response.strip()) > 20 else 0.0
    overall = (routing_accuracy + has_response) / 2
    return {
        "routing_accuracy": routing_accuracy,
        "has_response": has_response,
        "overall": overall,
    }
```

Uso:

```python
scores = evaluate_response(
    expected_intent="tech",
    actual_intent=result["intent"],
    response=result["response"],
)

langfuse = Langfuse()

for score_name, score_value in scores.items():
    langfuse.score_current_trace(
        name=score_name,
        value=score_value,
        comment="Score automatico del evaluator local.",
    )
```

Que ensena:

- primero ejecuto;
- despues mido;
- despues registro;
- luego analizo en Langfuse.

---

# 14. Interfaz de Langfuse: como usarla en clase

## 14.1 Pantalla de traces

Que mostrar:

- lista de traces;
- nombre del run;
- timestamp;
- usuario o sesion si existe;
- latencia;
- modelo;
- costo si aparece;
- scores.

Espacio para imagen:

```txt
[PEGAR IMAGEN: tabla/lista de traces]
```

Explicacion:

> Esta pantalla responde: que ejecuciones ocurrieron y cual quiero inspeccionar.

## 14.2 Vista detalle de trace

Que mostrar:

- input;
- output;
- metadata;
- observations/spans;
- generations;
- scores.

Espacio para imagen:

```txt
[PEGAR IMAGEN: detalle de un trace]
```

Explicacion:

> Esta pantalla responde: que paso dentro de una ejecucion.

## 14.3 Observations / spans

Que mostrar:

- router;
- agente;
- evaluator;
- retrieval si existe.

Espacio para imagen:

```txt
[PEGAR IMAGEN: arbol de observations/spans]
```

Explicacion:

> Cada span representa un paso del sistema. Si una query fue mal ruteada, aca vemos donde se tomo la decision.

## 14.4 Generations

Que mostrar:

- prompt enviado;
- modelo;
- respuesta;
- tokens si estan disponibles;
- latencia.

Espacio para imagen:

```txt
[PEGAR IMAGEN: generation con prompt y output]
```

Explicacion:

> Una generation permite auditar que prompt vio el modelo y que respondio.

## 14.5 Scores

Que mostrar:

- nombre del score;
- valor;
- comentario;
- relacion con el trace.

Espacio para imagen:

```txt
[PEGAR IMAGEN: panel de scores]
```

Explicacion:

> Los scores transforman ejecuciones sueltas en datos medibles.

## 14.6 Filtros

Filtros utiles:

- por `run_name`;
- por metadata `lecture`;
- por metadata `router_version`;
- por score bajo;
- por fecha;
- por modelo.

Espacio para imagen:

```txt
[PEGAR IMAGEN: filtros por metadata o score]
```

Explicacion:

> Los filtros permiten comparar versiones y encontrar fallas rapidamente.

---

# 15. Que exactamente agregamos de Langfuse al codigo

En un ejemplo sin Langfuse:

```python
result = graph.invoke(input_state)
```

Con Langfuse:

```python
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

result = graph.invoke(
    input_state,
    config={
        "callbacks": [langfuse_handler],
        "run_name": "nombre_del_trace",
        "metadata": {"clave": "valor"},
    },
)
```

Eso es lo minimo.

Luego, para scores:

```python
from langfuse import Langfuse

langfuse = Langfuse()
langfuse.score_current_trace(name="overall", value=0.9, comment="Buena respuesta.")
```

Eso es lo adicional avanzado.

---

# 16. Errores comunes

## No aparece ningun trace

Revisar:

- no pasaste `config={"callbacks": [handler]}`;
- faltan keys;
- host incorrecto;
- estas mirando otro proyecto en Langfuse.

## Aparece trace pero sin generation

Posibles causas:

- tus nodos no llaman LLM;
- estas traceando solo funciones Python;
- el callback no llego a la chain del LLM.

## Aparece todo como un solo bloque

Probable causa:

- la app no esta separada en nodos/chains;
- falta estructura en LangGraph.

## No se registran scores

Revisar:

- `score_current_trace` necesita contexto activo;
- si no hay contexto, usar `create_score(trace_id=...)`;
- verificar credenciales de escritura.

---

# 17. Mini checklist para la clase

Antes de mostrar Langfuse:

- ejecutar notebook con credenciales reales;
- verificar que aparece el trace;
- elegir una query clara;
- tener una captura del listado de traces;
- tener una captura del detalle;
- tener una captura de generation;
- tener una captura de scores.

Durante la clase:

1. ejecutar sin Langfuse;
2. mostrar que solo tenemos `print`;
3. agregar `CallbackHandler`;
4. ejecutar otra vez;
5. abrir Langfuse;
6. mostrar trace;
7. mostrar generation;
8. agregar score;
9. mostrar score en interfaz.

---

# 18. Resumen final

Langfuse no cambia la logica del agente.

Langfuse agrega visibilidad.

La diferencia clave es:

```txt
Antes:
ejecuto -> veo print

Despues:
ejecuto -> veo trace -> veo spans -> veo generations -> veo scores -> puedo mejorar
```

Esto conecta directamente con Lecture 4:

- tracing;
- debugging;
- golden dataset;
- evaluator;
- scores;
- mejora iterativa.

