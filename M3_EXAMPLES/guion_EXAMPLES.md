# Guion docente - M3_EXAMPLES

Este guion es para explicar los notebooks de `M3_EXAMPLES` en clase.

Objetivo general:

```txt
Mostrar la misma idea en tres niveles:

1. LangChain puro
2. LangGraph
3. LangGraph + Langfuse
```

Y despues aplicar ese mismo patron a RAG y agentes.

---

# 0. Apertura de la clase

## Mensaje inicial para decir

> Hoy no vamos a aprender una herramienta aislada. Vamos a ver una progresion.
> Primero resolvemos un problema con LangChain puro.
> Despues lo pasamos a LangGraph para ver el flujo como grafo.
> Finalmente le agregamos Langfuse para observar que paso por dentro.

## Mapa mental en el pizarron

```txt
E07: chain lineal -> grafo simple -> grafo traceado

E08: router manual -> router en LangGraph -> router traceado

E09: RAG con LangChain -> RAG con agentes en LangGraph -> RAG traceado
```

## Aclaracion importante

> No estamos intentando hacer un PI gigante todavia.
> Estos ejemplos son escalones.
> Si entienden estos escalones, despues el PIM3 deja de parecer magico.

---

# 1. Como usar Starter y Resolution

## Decir antes de empezar

> Cada ejercicio tiene dos archivos:
>
> - Starter: para que ustedes completen.
> - Resolution: para revisar despues.
>
> En clase vamos a leer el Starter, completar mentalmente o en vivo los TODOs, y despues comparar con Resolution.

## Regla de clase

```txt
No mirar Resolution antes de intentar el Starter.
```

## Como corregir

Cuando un alumno se traba, pedirle que identifique:

- que recibe la funcion;
- que devuelve;
- que parte del flujo representa;
- si es logica de negocio, orquestacion o observabilidad.

---

# 2. E07 - Anatomia de un grafo

Carpeta:

```txt
M3_EXAMPLES/E07_anatomia_grafo/
```

Objetivo:

```txt
Entender como una chain lineal se convierte en un grafo.
```

## 2.1 E07_01 - LangChain puro

Notebook:

```txt
E07_01_LangChain_Starter.ipynb
```

## Que decir

> Antes de usar LangGraph, necesitamos ver el flujo lineal.
> Una chain de LangChain es una tuberia:
>
> input -> prompt -> modelo -> parser -> salida

## Dibujar

```txt
name
  |
  v
prompt
  |
  v
llm
  |
  v
parser
  |
  v
format_output
```

## Explicar componentes

### `ChatPromptTemplate`

> Es la forma ordenada de construir el prompt.
> En vez de concatenar strings sueltos, definimos mensajes.

### `ChatOpenAI`

> Es el modelo. Es la parte que realmente llama a OpenAI.

### `StrOutputParser`

> El modelo devuelve un objeto mensaje.
> El parser lo transforma en texto comun.

### `RunnableLambda`

> Permite meter una funcion Python dentro de la chain.
> Esto nos sirve para mostrar que una funcion simple tambien puede ser parte del flujo.

## Que ejecutar en vivo

1. Instalacion.
2. Credenciales.
3. Imports.
4. Completar `prompt`.
5. Completar `parser`.
6. Completar `format_output`.
7. Armar `chain`.
8. Ejecutar `chain.invoke({"name": "Ada"})`.

## Pregunta para alumnos

> Donde esta el estado en este ejemplo?

Respuesta esperada:

> No hay un estado compartido formal. Hay una entrada que va pasando por la chain.

## Cierre de E07_01

> LangChain puro nos da una secuencia clara.
> Pero si el flujo crece, empieza a ser dificil ver pasos, rutas y estado.
> Ahi entra LangGraph.

---

## 2.2 E07_02 - LangGraph

Notebook:

```txt
E07_02_LangGraph_Starter.ipynb
```

## Que decir

> Ahora tomamos la misma idea y la convertimos en grafo.
> No cambiamos el problema.
> Cambiamos la forma de organizarlo.

## Dibujar

```txt
START -> greet_node -> format_node -> END
```

## Explicar diferencias con LangChain puro

| LangChain puro | LangGraph |
|---|---|
| Flujo lineal con `|` | Flujo declarado con nodos y edges |
| La entrada pasa de paso en paso | Hay un `State` compartido |
| No hay nodos nombrados | Cada paso tiene nombre |
| Dificil ver bifurcaciones | Preparado para routing |

## Explicar `State`

> El State es la mochila del flujo.
> Todo lo que el grafo necesita transportar vive ahi.

Campos:

- `name`: entrada.
- `message`: resultado del primer nodo.
- `formatted`: resultado del segundo nodo.

## Explicar nodos

### `greet_node`

> Lee `name`, llama al LLM y escribe `message`.

### `format_node`

> Lee `message` y escribe `formatted`.

## Explicar regla clave

```python
return {"message": response.content}
```

> Un nodo no devuelve todo el state.
> Devuelve solo lo que cambia.
> LangGraph se encarga de fusionarlo.

## Que ejecutar en vivo

1. Definir `GreetState`.
2. Leer `greet_node`.
3. Completar `format_node`.
4. Crear `StateGraph`.
5. Agregar nodos.
6. Agregar edges.
7. Compilar.
8. Invocar.

## Pregunta para alumnos

> Que pasa si `format_node` intenta leer `state["formatted"]`?

Respuesta esperada:

> Todavia no existe. Ese campo lo tiene que producir ese mismo nodo.

## Cierre de E07_02

> LangGraph no es para reemplazar cualquier chain simple.
> LangGraph sirve cuando queremos estado, pasos nombrados, rutas y control del flujo.

---

## 2.3 E07_03 - LangGraph + Langfuse

Notebook:

```txt
E07_03_LangGraph_Langfuse_Starter.ipynb
```

## Que decir

> Ahora el grafo ya funciona.
> El problema es que solo vemos el resultado final.
> Con Langfuse queremos ver que paso por dentro.

## Dibujar

```txt
graph.invoke(...)
  |
  +-- config callbacks
        |
        v
      Langfuse trace
```

## Explicar que agregamos

Antes:

```python
result = graph.invoke({"name": "Ada"})
```

Despues:

```python
result = graph.invoke(
    {"name": "Ada"},
    config={"callbacks": [langfuse_handler]}
)
```

## Explicar `CallbackHandler`

> Es un observador.
> No cambia la logica del grafo.
> Mira la ejecucion y la manda a Langfuse.

## Que mostrar en Langfuse

Abrir la interfaz y mostrar:

- trace generado;
- nombre del run;
- input;
- output;
- llamada al LLM;
- metadata.

## Lugar para captura en Notion/slides

```txt
[PEGAR CAPTURA: trace de E07_03 con greet_node y format_node]
```

## Cierre de E07

> E07 nos deja la anatomia:
>
> - chain lineal;
> - grafo;
> - grafo observable.

---

# 3. E08 - Router condicional

Carpeta:

```txt
M3_EXAMPLES/E08_router_condicional/
```

Objetivo:

```txt
Entender routing: elegir que agente responde.
```

## 3.1 E08_01 - Router con LangChain puro

Notebook:

```txt
E08_01_LangChain_Starter.ipynb
```

## Que decir

> En E07 no habia decision.
> Siempre era START -> nodo 1 -> nodo 2.
> En E08 aparece una pregunta nueva:
>
> A que area mando esta consulta?

## Dibujar

```txt
query
  |
  v
classifier_chain
  |
  v
intent
  |
  v
if/else
  |
  v
respuesta
```

## Explicar conceptos

### Intent

> Es la categoria elegida por el router.

Ejemplos:

- `hr`;
- `tech`;
- `finance`;
- `unknown`.

### Router

> Es el componente que decide la ruta.
> No deberia responder la consulta final.

### Agente especialista

> Es quien responde dentro de su dominio.

## Que ejecutar en vivo

1. Cargar `knowledge_base`.
2. Crear `classification_prompt`.
3. Crear `classifier_chain`.
4. Completar `classify_intent`.
5. Completar `handle_query`.
6. Probar:

```python
handle_query("No puedo conectarme a la VPN")
```

## Pregunta para alumnos

> Que problema tiene este enfoque con `if/else`?

Respuesta esperada:

> Funciona, pero la orquestacion queda mezclada con la logica.

## Cierre de E08_01

> LangChain puede clasificar.
> Python puede rutear.
> Pero el flujo no queda visible como grafo.

---

## 3.2 E08_02 - Router con LangGraph

Notebook:

```txt
E08_02_LangGraph_Starter.ipynb
```

## Que decir

> Ahora vamos a pasar el if/else manual a LangGraph.
> La decision sigue existiendo, pero se declara como conditional edge.

## Dibujar

```txt
START
  |
  v
classify_node
  |
  v
add_conditional_edges
  |       |        |          |
  v       v        v          v
hr_node tech_node finance_node unknown_node
  |       |        |          |
  +-------+--------+----------+
          |
          v
         END
```

## Explicar `classify_node`

> Es un nodo.
> Lee `query`.
> Escribe `intent`.

## Explicar `route_to_node`

> No responde.
> No llama agentes.
> Solo mira `state["intent"]` y devuelve el nombre del siguiente nodo.

## Explicar `add_conditional_edges`

> Es el punto central del ejercicio.
> Le dice al grafo:
>
> "Despues de classify_node, llama esta funcion para decidir a donde ir".

## Que ejecutar en vivo

1. Definir `RouterState`.
2. Revisar nodos.
3. Completar `route_to_node`.
4. Crear `StateGraph`.
5. Agregar nodos.
6. Agregar `START -> classify_node`.
7. Agregar `add_conditional_edges`.
8. Conectar agentes a `END`.
9. Invocar.

## Error comun

Error:

```txt
KeyError en mapping de conditional edges
```

Causa:

> `route_to_node` devuelve un nombre que no existe en el mapping.

## Cierre de E08_02

> Ahora el flujo es visible.
> El routing ya no esta escondido dentro de un if/else largo.

---

## 3.3 E08_03 - Router con LangGraph + Langfuse

Notebook:

```txt
E08_03_LangGraph_Langfuse_Starter.ipynb
```

## Que decir

> Ahora queremos responder una pregunta de debugging:
>
> Si el sistema respondio mal, que ruta tomo?

Langfuse nos permite ver:

- input;
- intent;
- nodo ejecutado;
- output;
- metadata.

## Que ejecutar en vivo

1. Crear `CallbackHandler`.
2. Ejecutar `graph.invoke` con callbacks.
3. Abrir Langfuse.
4. Buscar el trace.
5. Mostrar la ruta.

## Captura sugerida

```txt
[PEGAR CAPTURA: trace donde se vea classify_node y tech_node]
```

## Cierre de E08

> E08 nos deja routing.
> Primero manual.
> Despues declarativo con LangGraph.
> Finalmente observable con Langfuse.

---

# 4. E09 - RAG y agentes

Carpeta:

```txt
M3_EXAMPLES/E09_rag_agentes/
```

Objetivo:

```txt
Entender RAG basico y combinarlo con agentes.
```

## 4.1 E09_01 - RAG con LangChain

Notebook:

```txt
E09_01_LangChain_RAG_Starter.ipynb
```

## Que decir

> Hasta ahora los agentes respondian con textos en memoria.
> Ahora aparece RAG.
> RAG significa que antes de responder recuperamos contexto.

## Dibujar

```txt
Document
  |
  v
splitter
  |
  v
chunks
  |
  v
embeddings
  |
  v
ChromaDB
  |
  v
retriever
  |
  v
context
  |
  v
prompt + LLM
```

## Explicar herramientas

### `Document`

> Unidad basica de texto en LangChain.
> Tiene `page_content` y `metadata`.

### Splitter

> Divide documentos en fragmentos.
> Esto evita mandar documentos enormes al modelo.

### Embeddings

> Transforman texto en vectores.
> Permiten buscar por significado.

### ChromaDB

> Guarda vectores y permite busqueda semantica.

### Retriever

> Interfaz que recibe una query y devuelve documentos relevantes.

## Que ejecutar en vivo

1. Crear documentos.
2. Crear splitter.
3. Crear chunks.
4. Crear Chroma.
5. Crear retriever.
6. Crear prompt RAG.
7. Crear `rag_chain`.
8. Completar `rag_answer`.
9. Probar con VPN.

## Pregunta para alumnos

> Por que no le pasamos todos los documentos al LLM?

Respuesta esperada:

> Porque es costoso, puede exceder contexto y mete ruido. Recuperamos solo lo relevante.

## Cierre E09_01

> LangChain ya puede hacer RAG completo.
> Pero todavia no tenemos agentes ni routing grafico.

---

## 4.2 E09_02 - RAG + agentes con LangGraph

Notebook:

```txt
E09_02_LangGraph_RAG_Agentes_Starter.ipynb
```

## Que decir

> Ahora combinamos E08 y RAG.
> El router decide dominio.
> El agente de ese dominio ejecuta RAG.

## Dibujar

```txt
query
  |
  v
router_node
  |
  v
conditional edge
  |
  +--> hr_node -> RAG HR
  +--> tech_node -> RAG Tech
  +--> finance_node -> RAG Finance
  +--> unknown_node
```

## Explicar diferencia con E08

| E08 | E09 |
|---|---|
| Agentes devuelven texto fijo | Agentes recuperan contexto |
| No hay vector store | Hay ChromaDB |
| No hay embeddings | Hay embeddings |
| La respuesta no esta fundamentada | La respuesta usa contexto |

## Que ejecutar en vivo

1. Reusar retriever.
2. Definir `RAGState`.
3. Completar `route_query`.
4. Completar `router_node`.
5. Completar `rag_node`.
6. Crear nodos especialistas.
7. Crear `route_to_node`.
8. Armar grafo.
9. Invocar.

## Error comun

Error:

```txt
El agente responde con documentos de otro dominio.
```

Explicacion:

> El ejemplo filtra por metadata de dominio despues de recuperar.
> En un PI mas completo conviene tener retrievers separados por dominio.

## Cierre E09_02

> Ya tenemos la base conceptual del PI:
>
> router + agentes + RAG.

---

## 4.3 E09_03 - RAG + agentes + Langfuse

Notebook:

```txt
E09_03_LangGraph_Langfuse_RAG_Agentes_Starter.ipynb
```

## Que decir

> Ahora queremos observar el flujo RAG.
> No solo importa la respuesta.
> Importa saber que ruta tomo y que contexto uso.

## Que ejecutar en vivo

1. Crear `CallbackHandler`.
2. Ejecutar el grafo con callbacks.
3. Abrir Langfuse.
4. Mostrar trace.
5. Buscar generation.
6. Mostrar input/output.

## Capturas sugeridas

```txt
[PEGAR CAPTURA: trace E09 RAG]
[PEGAR CAPTURA: generation con prompt RAG]
[PEGAR CAPTURA: metadata o ruta ejecutada]
```

## Que explicar en la interfaz

- trace = ejecucion completa;
- span = paso del grafo;
- generation = llamada al LLM;
- input = query/contexto;
- output = respuesta;
- metadata = informacion para filtrar.

## Cierre E09

> E09 es el puente directo al PIM3.
> Ya tenemos RAG, agentes, routing y observabilidad.

---

# 5. Cierre general de la secuencia

## Mensaje final

> Lo importante no es memorizar codigo.
> Lo importante es reconocer el patron:
>
> - LangChain construye cadenas y RAG.
> - LangGraph ordena flujos con estado y rutas.
> - Langfuse permite observar, debuggear y medir.

## Mapa final

```txt
E07:
chain -> graph -> trace

E08:
manual router -> conditional graph -> trace

E09:
RAG chain -> RAG agents graph -> RAG trace
```

## Puente al PI

> El PIM3 no aparece de golpe.
> Es la suma de estos patrones:
>
> - router de E08;
> - RAG de E09;
> - graph de E07/E08;
> - Langfuse de Lecture 4.

---

# 6. Checklist para dar la clase

Antes de clase:

- abrir notebooks Starter;
- tener OpenAI API key;
- tener Langfuse project;
- probar un trace;
- tener capturas listas por si internet falla.

Durante clase:

- no mostrar Resolution al principio;
- hacer que los alumnos predigan el output;
- comparar LangChain vs LangGraph;
- mostrar Langfuse solo despues de que el flujo funcione;
- repetir siempre: que recibe, que devuelve, que responsabilidad tiene.

Despues de clase:

- pedir que completen Starter;
- pedir que comparen con Resolution;
- pedir que expliquen en palabras propias E07, E08 y E09.

