# Guía M3L2 - LangChain, LCEL, RAG y Embeddings

Esta guía acompaña los ejercicios de la carpeta `M3L2`. Sirve para saber, de un vistazo, **qué se ve en cada ejercicio**, en qué orden conviene recorrerlos y cómo se conectan entre sí.

Objetivo del módulo:

```txt
Pasar de "llamar al modelo con requests sueltos" (estilo M3L1)
a construir pipelines LangChain modulares, reemplazables y con RAG.
```

La numeración de las carpetas (`E00` a `E13`) **ya sigue el orden de dictado recomendado**. `E14` es un ejercicio extra fuera de esa secuencia.

Cada carpeta trae dos notebooks (salvo E14):

- `*_Starter.ipynb` — versión con TODOs para completar.
- `*_Resolution.ipynb` — versión resuelta, con teoría y explicación bloque por bloque.

---

## Mapa rápido

| # | Carpeta | Tema | Se conecta con |
|---|---|---|---|
| E00 | `E00_llm_wrapper` | El modelo como objeto (`ChatOpenAI`) | base de todo lo que sigue |
| E01 | `E01_prompt_template` | El prompt como componente (`ChatPromptTemplate`) | E00 |
| E02 | `E02_output_parser` | Normalizar la salida (`StrOutputParser`) | E00, E01 |
| E03 | `E03_lcel_chain` | Componer con `\|` (LCEL) | E00 + E01 + E02 juntos |
| E04 | `E04_chat_con_memoria_langchain` | Memoria conversacional | E03 |
| E05 | `E05_tools_langchain_api_dolar` | Tools con `@tool` | E03 |
| E06 | `E06_manual_to_langchain` | Agente completo (`AgentExecutor`) | E00, E01, E02, E05 |
| E07 | `E07_embeddings` | Convertir texto en vectores | base del bloque RAG |
| E08 | `E08_faiss` | Guardar y buscar vectores (FAISS) | E07 |
| E09 | `E09_retriever` | Interfaz estándar de búsqueda | E08 |
| E10 | `E10_rag_mini` | Pipeline RAG completo (script legacy vs LangChain) | E07, E08, E09, E01, E02, E03 |
| E11 | `E11_rag_chat_con_memoria` | RAG + memoria combinados | E04, E10 |
| E12 | `E12_rag_desde_cero` | RAG completo, capstone integrador | todo lo anterior |
| E13 | `E13_refactor_chaos` | Taller grupal: refactorizar un script caótico | todo el módulo |
| E14 | `E14_langchain_vs_manual` | Extra: repaso comparativo de todo el módulo | todo el módulo |

---

## E00 - LLM Wrapper

**Carpeta**: `E00_llm_wrapper`

**Qué vemos**:
- La diferencia entre llamar `openai` directamente (`client.chat.completions.create(...)`) y usar `ChatOpenAI`.
- Que `llm.invoke()` devuelve un `AIMessage`, no un string — y por qué (guarda metadata: tokens, id, modelo).
- Cómo configurar el modelo en un solo lugar y crear distintas configuraciones (`temperature=0` vs `temperature=1.0`).
- **Bonus**: el mismo patrón funciona con otros proveedores — `ChatAnthropic` (Claude), `ChatGoogleGenerativeAI` (Gemini) y `ChatOllama` (modelo local, sin costo ni API key). Se muestra que la única línea que cambia es la que crea el objeto `llm`.

**Por qué importa**: es el punto de entrada a todo el módulo. Sin este concepto (el modelo como objeto configurable, no una llamada hardcodeada) nada de lo que sigue tiene sentido.

---

## E01 - PromptTemplate

**Carpeta**: `E01_prompt_template`

**Qué vemos**:
- El problema del prompt como string manual (f-strings, concatenación): variables implícitas, imposible de inspeccionar, difícil de reutilizar.
- `ChatPromptTemplate.from_messages()` con mensajes `system` / `human` y variables explícitas (`{context}`, `{question}`).
- `.format_messages()` para ver exactamente qué le llega al modelo, antes de invocarlo (debugging).
- (En la Resolution) tipos adicionales: `from_template()`, `MessagesPlaceholder`, `.partial()`, composición de templates con `+`.

**Por qué importa**: separa "qué le decimos al modelo" de "cómo lo llamamos". Es la pieza que en E04 (memoria) y E10-E12 (RAG) se combina con el resto del pipeline.

---

## E02 - Output Parser

**Carpeta**: `E02_output_parser`

**Qué vemos**:
- Por qué `llm.invoke()` devuelve `AIMessage` y no texto plano, y el costo de tener que escribir `.content` en todos lados.
- `StrOutputParser`: extrae el texto automáticamente como último paso de una chain.
- Comparación `llm.invoke(q)` vs `(llm | parser).invoke(q)`.
- (En la Resolution) otros parsers: `JsonOutputParser`, `CommaSeparatedListOutputParser`.

**Por qué importa**: es la pieza que cierra el patrón `prompt | llm | parser` que se usa en todo el resto del módulo.

---

## E03 - LCEL Chain

**Carpeta**: `E03_lcel_chain`

**Qué vemos**:
- Comparación explícita: script imperativo (4 pasos sueltos con `openai` crudo) vs `prompt | llm | parser` en una línea.
- El operador `|` (LCEL, LangChain Expression Language) y por qué es "composición declarativa".
- Que el modelo es reemplazable sin tocar el resto de la chain (cambiar solo la variable `llm`).
- Capacidades que vienen gratis con LCEL: `.stream()`, `.batch()`, trazabilidad.

**Por qué importa**: junta las tres piezas de E00, E01 y E02 en un solo flujo. A partir de acá, "armar una chain" es el patrón que se repite en memoria, tools y RAG.

---

## E04 - Chat con memoria

**Carpeta**: `E04_chat_con_memoria_langchain`

**Qué vemos**:
- Por qué un LLM no recuerda nada por sí solo (es *stateless*): cada llamada es independiente.
- La idea de "memoria" = guardar el historial y reenviarlo en cada llamada.
- `MessagesPlaceholder` para marcar dónde se inyecta el historial en el prompt.
- `InMemoryChatMessageHistory` + `RunnableWithMessageHistory` + `session_id` para manejar múltiples conversaciones en paralelo, cada una con su propio historial.

**Por qué importa**: es la base de E11 (RAG + memoria). El concepto de `session_id` separado por conversación se reutiliza tal cual.

---

## E05 - Tools con `@tool`

**Carpeta**: `E05_tools_langchain_api_dolar`

**Qué vemos**:
- Cómo convertir una función Python en una tool con el decorador `@tool` (usa el docstring como descripción y el type hint para el schema).
- `bind_tools()` para que el modelo pueda pedir ejecutar una tool.
- `tool_calls`: qué pide el modelo (no lo ejecuta solo) y cómo se interpreta.
- Una tool real conectada a una API externa (DolarAPI) con manejo de errores.

**Por qué importa**: es el primer paso hacia agentes reales. E06 toma este mismo concepto y arma un agente completo con loop automático.

---

## E06 - De manual a LangChain (agente completo)

**Carpeta**: `E06_manual_to_langchain`

**Qué vemos**:
- El mismo ejercicio de M3L1 (agente clima + cálculo) implementado dos veces: a mano (loop ReAct manual, con `[Thought]/[Action]/[Observation]` escritos por el programador) y con `AgentExecutor`.
- `create_tool_calling_agent()` + `AgentExecutor(..., verbose=True, max_iterations=5)`: el LLM decide solo qué tool usar, con cuántos pasos y cuándo terminar.
- Tabla de equivalencias completa M3L1 (manual) → M3L2 (LangChain): prompt, modelo, parser, loop, trace, tools.

**Por qué importa**: es el puente explícito entre M3L1 y M3L2 — conecta todo lo aprendido en el módulo anterior con los componentes que se vieron en E00-E05.

---

## E07 - Embeddings

**Carpeta**: `E07_embeddings`

**Qué vemos**:
- Qué es un embedding: un vector que representa el significado de un texto (textos parecidos → vectores cercanos).
- `OpenAIEmbeddings`: `embed_query()` (una consulta) vs `embed_documents()` (una lista de documentos).
- Similitud del coseno para comparar vectores a mano, y verificar que textos relacionados dan valores altos y textos distintos dan valores bajos.

**Por qué importa**: es el fundamento de todo RAG. Sin embeddings no hay forma de "buscar por significado" en vez de por palabras exactas.

---

## E08 - FAISS

**Carpeta**: `E08_faiss`

**Qué vemos**:
- El problema de comparar un vector contra miles de documentos uno por uno (no escala).
- `FAISS.from_texts(docs, embeddings)`: crea el índice, embebe los textos y los guarda en un solo paso.
- `vectorstore.similarity_search(query, k)` para traer los `k` documentos más parecidos.
- (En la Resolution) persistencia con `save_local()` / `load_local()`.

**Por qué importa**: reemplaza la búsqueda "naive" (mandar todo el contexto siempre) por retrieval real y eficiente.

---

## E09 - Retriever

**Carpeta**: `E09_retriever`

**Qué vemos**:
- Por qué `similarity_search()` es específico de FAISS: si mañana cambiás a Chroma o Pinecone, hay que cambiar todas las llamadas.
- `vectorstore.as_retriever(search_kwargs={"k": N})`: envuelve cualquier vector store en la interfaz estándar `.invoke(query)`.
- Comparación de distintos valores de `k` (tradeoff entre contexto y costo/ruido).
- Cómo el retriever se conecta directamente en una chain LCEL con `\|`.

**Por qué importa**: es la pieza que permite que "cambiar de vector store" sea una sola línea, y la que se usa directamente dentro del pipeline RAG de E10-E12.

---

## E10 - RAG mini: el pipeline completo

**Carpeta**: `E10_rag_mini`

**Qué vemos**:
- Un script "legacy" que manda **todo** el contexto siempre (sin retrieval real) vs el mismo chatbot con un pipeline RAG modular.
- Las dos fases del RAG: **ingestión** (documentos → embeddings → vector store, se hace una vez) y **consulta** (pregunta → retriever → prompt → LLM → parser, se hace por cada pregunta).
- La chain RAG completa con LCEL: `{"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | parser`.
- Un framework de debugging: inspeccionar retriever, contexto formateado y prompt final por separado cuando la respuesta es mala.

**Por qué importa**: es el ejercicio donde todo lo de E00-E09 converge en un pipeline real y completo.

---

## E11 - RAG con memoria

**Carpeta**: `E11_rag_chat_con_memoria`

**Qué vemos**:
- Cómo combinar retrieval (E07-E10) con memoria conversacional (E04) para responder preguntas de seguimiento sobre documentos ("¿y qué dije recién?").
- Loader + Splitter (`TextLoader`, `RecursiveCharacterTextSplitter`) además de embeddings y vector store — carga documentos reales en vez de textos hardcodeados.
- `MessagesPlaceholder` + `RunnableWithMessageHistory` conviviendo con el retriever en la misma chain.

**Por qué importa**: es la combinación de las dos piezas más complejas del módulo (RAG y memoria) en un solo sistema, como haría un chatbot de producción.

---

## E12 - RAG desde cero

**Carpeta**: `E12_rag_desde_cero`

**Qué vemos**:
- Un RAG completo armado paso a paso desde cero, sin bundling previo: `Document` (con metadata), splitter, embeddings, `FAISS.from_documents()`, retriever, `format_docs`, prompt, chain LCEL.
- Un glosario mínimo de todos los términos del pipeline (corpus, chunk, embedding, retriever, k, contexto).
- Debugging con preguntas dentro y fuera del corpus, para ver cómo se comporta el sistema cuando no tiene la respuesta.

**Por qué importa**: es el capstone del bloque RAG — el ejercicio más largo e independiente, pensado para hacerlo sin scaffolding, integrando todo lo visto en E07-E11.

---

## E13 - Refactorizar el Caos

**Carpeta**: `E13_refactor_chaos`

**Qué vemos**:
- Un chatbot "caótico" ya armado (cliente creado en cada llamada, prompt como string manual, sin retrieval, modelo y temperatura hardcodeados, idioma mezclado con el prompt) que hay que identificar y refactorizar.
- Es el único ejercicio **abierto**: no tiene TODOs guiados, hay que decidir qué componente de LangChain reemplaza cada problema.
- Un checklist de producción para autoevaluar la refactorización (ingestión separada de consulta, retriever encapsulado, prompt como `ChatPromptTemplate`, modelo configurable, etc.).

**Por qué importa**: es el cierre del módulo — un taller grupal que obliga a aplicar todo (E00-E12) sin andamiaje, tal como se haría con código real de producción.

---

## E14 - LangChain vs Manual (extra)

**Carpeta**: `E14_langchain_vs_manual`

**Qué vemos**:
- Un repaso comparativo de **todo el módulo**, solo Resolution (sin TODOs): cada concepto implementado dos veces, a mano con el SDK de `openai` y con LangChain, uno al lado del otro.
- Recorre en orden: modelo, prompt, output parser, LCEL, memoria, tools, embeddings, vector store, retriever y el pipeline RAG completo — cerrando con las dos versiones del mismo chatbot de RRHH respondiendo las mismas preguntas.
- Checks automáticos que validan que ambas implementaciones (manual y LangChain) funcionan y devuelven resultados consistentes.

**Por qué importa**: no enseña nada nuevo — sirve para consolidar, viendo en un solo lugar qué reemplaza exactamente cada componente de LangChain y por qué esas abstracciones importan cuando el sistema crece.

---

## Orden de dictado recomendado (clase de 45 min)

```txt
E00 (LLM Wrapper) -> E01 (PromptTemplate) -> E02 (Output Parser) -> E03 (LCEL)
   -> E04 (Memoria) -> E05 (Tools) -> [E06 opcional: agente completo]
   -> E07 (Embeddings) -> E08 (FAISS) -> E09 (Retriever) -> E10 (RAG mini)
   -> E11 (RAG + memoria) -> E12 (RAG desde cero, capstone)
   -> E13 (Refactor, cierre grupal)
```

`E14` queda como material de repaso, fuera de esta secuencia — se puede asignar como autoestudio antes de pasar a M3L3.
