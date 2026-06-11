# Guia Notion - M3_EXAMPLES E07/E08/E09

## Objetivo

Entender la progresion:

```txt
LangChain puro -> LangGraph -> LangGraph + Langfuse
```

Antes de ir al PI, los alumnos deben ver el mismo problema en tres niveles.

Para profundizar solo en observabilidad, usar tambien:

```txt
../M3L4/guia_Langfuse_Lecture4.md
```

Esa guia explica Langfuse desde instalacion hasta lectura de traces, generations, spans y scores en la interfaz.

## E07 - Anatomia de un grafo

### Paso 1 - LangChain puro

Notebook:

```txt
E07_01_LangChain_Starter.ipynb
```

Concepto:

```txt
prompt -> LLM -> parser -> funcion de formateo
```

### Paso 2 - LangGraph

Notebook:

```txt
E07_02_LangGraph_Starter.ipynb
```

Concepto:

```txt
START -> greet_node -> format_node -> END
```

### Paso 3 - Langfuse

Notebook:

```txt
E07_03_LangGraph_Langfuse_Starter.ipynb
```

Concepto:

```txt
mismo grafo + CallbackHandler -> trace visible
```

## E08 - Router condicional

### Paso 1 - LangChain puro

Concepto:

```txt
query -> clasificador -> if/else -> respuesta
```

### Paso 2 - LangGraph

Concepto:

```txt
query -> classify_node -> add_conditional_edges -> agente
```

### Paso 3 - Langfuse

Concepto:

```txt
mismo router + trace para ver la ruta tomada
```

## Uso recomendado

1. Resolver Starter.
2. Ejecutar celdas.
3. Comparar con Resolution.
4. Repetir el patron en el PI.

## Cierre

Estos ejemplos preparan a los alumnos para entender por que el PI usa LangGraph y Langfuse. Ahora tambien incluyen un primer puente a RAG con `E09_rag_agentes`.

## E09 - RAG y agentes

La carpeta `E09_rag_agentes` agrega el primer puente hacia el PI.

### Paso 1 - RAG con LangChain

Notebook:

```txt
E09_01_LangChain_RAG_Starter.ipynb
```

Concepto:

```txt
Document -> splitter -> embeddings -> ChromaDB -> retriever -> prompt -> LLM
```

### Paso 2 - RAG con LangGraph

Notebook:

```txt
E09_02_LangGraph_RAG_Agentes_Starter.ipynb
```

Concepto:

```txt
query -> router_node -> add_conditional_edges -> agente RAG -> respuesta
```

### Paso 3 - RAG con LangGraph + Langfuse

Notebook:

```txt
E09_03_LangGraph_Langfuse_RAG_Agentes_Starter.ipynb
```

Concepto:

```txt
mismo grafo RAG + CallbackHandler -> trace visible en Langfuse
```

### Que debe poder explicar el alumno

- Que es un `Document`.
- Por que partimos documentos en chunks.
- Que hace un embedding.
- Para que sirve ChromaDB.
- Que es un retriever.
- Por que el prompt RAG recibe contexto.
- Como un agente especializado usa solo su dominio.
- Que agrega LangGraph respecto de LangChain puro.
- Que agrega Langfuse respecto de ejecutar sin observabilidad.
