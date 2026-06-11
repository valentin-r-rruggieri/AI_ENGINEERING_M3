# M3_EXAMPLES - Puente didactico hacia el PI

Esta carpeta contiene notebooks ultra explicativos para recorrer la progresion del modulo:

```txt
LangChain puro -> LangGraph -> LangGraph + Langfuse
```

La idea es que el alumno vea el mismo problema en tres formas distintas antes de construir un PI completo.

Guia complementaria de observabilidad:

- `../M3L4/guia_Langfuse_Lecture4.md`: instalacion, configuracion, callbacks, scores y lectura de la interfaz de Langfuse.

## E07 - Anatomia de un grafo

Objetivo: entender como una chain lineal se convierte en un grafo.

Orden:

1. `E07_01_LangChain_Starter.ipynb`
2. `E07_01_LangChain_Resolution.ipynb`
3. `E07_02_LangGraph_Starter.ipynb`
4. `E07_02_LangGraph_Resolution.ipynb`
5. `E07_03_LangGraph_Langfuse_Starter.ipynb`
6. `E07_03_LangGraph_Langfuse_Resolution.ipynb`

Conceptos:

- prompt;
- LLM;
- parser;
- funcion de formateo;
- `State`;
- nodos;
- edges;
- `START`;
- `END`;
- `CallbackHandler`.

## E08 - Router condicional

Objetivo: entender como un `if/else` de routing pasa a `add_conditional_edges`.

Orden:

1. `E08_01_LangChain_Starter.ipynb`
2. `E08_01_LangChain_Resolution.ipynb`
3. `E08_02_LangGraph_Starter.ipynb`
4. `E08_02_LangGraph_Resolution.ipynb`
5. `E08_03_LangGraph_Langfuse_Starter.ipynb`
6. `E08_03_LangGraph_Langfuse_Resolution.ipynb`

Conceptos:

- clasificador;
- intent;
- router manual;
- `add_conditional_edges`;
- agentes especialistas simples;
- trace de ruta tomada.

## E09 - RAG y agentes

Objetivo: introducir RAG basico y agentes antes del PI.

Orden:

1. `E09_01_LangChain_RAG_Starter.ipynb`
2. `E09_01_LangChain_RAG_Resolution.ipynb`
3. `E09_02_LangGraph_RAG_Agentes_Starter.ipynb`
4. `E09_02_LangGraph_RAG_Agentes_Resolution.ipynb`
5. `E09_03_LangGraph_Langfuse_RAG_Agentes_Starter.ipynb`
6. `E09_03_LangGraph_Langfuse_RAG_Agentes_Resolution.ipynb`

Conceptos:

- `Document`;
- splitter;
- chunks;
- embeddings;
- ChromaDB;
- retriever;
- prompt RAG;
- agentes por dominio;
- LangGraph con routing;
- Langfuse con trace.

## Como usar

1. Abrir primero el `Starter`.
2. Leer la teoria antes de cada celda.
3. Completar TODOs.
4. Ejecutar en orden.
5. Comparar con `Resolution`.

Los notebooks son autocontenidos y Colab-friendly: instalan dependencias, piden API keys con `getpass` y no dependen de `.env`.
