# 🤖 AI Engineering M3 - Agentes, LLMs y RAG

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=for-the-badge&logo=jupyter)](https://jupyter.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge)](https://langchain.com/)
[![Colab](https://img.shields.io/badge/Google-Colab-yellow?style=for-the-badge&logo=google-colab)](https://colab.research.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

> 🎓 Módulo completo sobre **Agentes de IA**, **Tools**, **ReAct**, **LangChain** y **RAG**

Bienvenido al **Módulo 3** de AI Engineering. Este repositorio contiene todos los ejercicios prácticos para dominar:

| | |
|---|---|
| 🤖 **M3L1** | Agentes de IA, Tools y Loop ReAct |
| 🦜 **M3L2** | LangChain, LCEL, RAG y Embeddings |
| 🧩 **M3L3** | Sistemas Multiagente, Orquestación, Handoff y Estado |
| 📊 **M3L4** | Tracing, Observabilidad y Producción |

✨ **Todos los ejercicios son autocontenidos** — resuelve cada uno independientemente  
🚀 **Compatible con Jupyter Notebook y Google Colab**

---

## � Estructura de Ejercicios

```
extras/
├── M3L1/
│   ├── E00 → Pipeline vs ReAct
│   ├── E01 → Tool Contracts
│   ├── E02 → ReAct Loop
│   ├── E03 → Múltiples Tools
│   ├── E10 → Sales: Pipeline vs Agent
│   ├── E11 → Sales: Tool Use
│   ├── E12 → Sales: ReAct Trace
│   └── E13 → Custom Tools Robustas
│
├── M3L2/
    ├── E00 → LLM Wrapper
    ├── E01 → PromptTemplate
    ├── E02 → Output Parser
    ├── E03 → LCEL Chain
    ├── E04 → Chat + Memory
    ├── E05 → Tools + API
    ├── E06 → De Manual a LangChain
    ├── E07 → Embeddings
    ├── E08 → FAISS
    ├── E09 → Retriever
    ├── E10 → RAG Mini
    ├── E11 → RAG + Memory
    ├── E12 → RAG desde Cero
    ├── E13 → Refactor Code
    └── E14 → LangChain vs Manual (extra, solo Resolution)
│
└── M3L3/
    ├── E00 → El problema del agente único
    ├── E01 → Intent Classifier
    ├── E02 → Agentes especialistas con RAG
    ├── E03 → Orquestador básico
    ├── E04 → Consulta mixta y delegación paralela
    ├── E05 → Handoff con contexto
    ├── E06 → Protocolos de output estructurado
    ├── E10 → Support Bot Baseline
    ├── E11 → Support Bot Multiagente
    ├── E12 → Orquestador con OpenAI Functions
    └── E13 → Sistema completo con estado
│
├── M3L4/
    ├── E00 → Logs vs Tracing
    ├── E01 → MiniTracer en Python
    ├── E02 → Tracing multiagente mock
    ├── E03 → Debugging con traces
    ├── E04 → Golden Dataset para routing
    ├── E05 → Router v1 vs v2
    ├── E06 → Evaluator Agent simple
    ├── E07 → Dashboard local de métricas
    ├── E08 → LangGraph básico + Langfuse
    ├── E09 → LangGraph router + Langfuse
    ├── E10 → LangGraph supervisor + Langfuse
    ├── E11 → Golden Dataset + Langfuse Scores
    └── E12 → Ciclo de mejora iterativa
```

### 📖 Formato de cada Ejercicio

Cada carpeta contiene dos notebooks complementarios:

| Archivo | Descripción |
|---------|------------|
| `*_Starter.ipynb` | 📝 Versión para alumnos con TODOs, checks y explicaciones |
| `*_Resolution.ipynb` | ✅ Versión resuelta para comparación |

---

## 🎯 Flujo de Trabajo Recomendado

```
1️⃣  Abre el Starter
   ↓
2️⃣  Lee objetivo y diagrama
   ↓
3️⃣  Ejecuta celdas en orden
   ↓
4️⃣  Completa TODOs
   ↓
5️⃣  Revisa checks
   ↓
6️⃣  Compara con Resolution
```

---

## 📦 Requisitos & Dependencias

### ✅ Mínimo Requerido
```
Python 3.8+
Jupyter Notebook
```

### 📦 Paquetes por Módulo

**M3L1**
```bash
# Básico (incluido)
pip install requests

# Opcional (para algunos ejercicios)
pip install openai  # E11, E12
```

**M3L2**
```bash
pip install langchain langchain-community langchain-openai
pip install faiss-cpu  # O faiss-gpu para GPU
pip install python-dotenv
```

**M3L3**
```bash
# Los notebooks actuales corren con Python estándar y mocks determinísticos.
# Opcional, si quieres reemplazar los mocks por LangChain/OpenAI real:
pip install langchain langchain-community langchain-openai faiss-cpu python-dotenv
```

### 🌐 En Google Colab
```
✨ Las dependencias se instalan automáticamente
⚡ Ejecuta: !pip install -q langchain faiss-cpu
```

---

## �📖 Estructura General

Cada carpeta de ejercicio contiene dos notebooks:

- `*_Starter.ipynb` → versión para alumnos (con TODOs, checks y explicaciones)
- `*_Resolution.ipynb` → versión resuelta (para comparar al final)

## 🚀 Flujo Recomendado de Trabajo

1. Abre el notebook `Starter`
2. Lee el objetivo y diagrama inicial
3. Ejecuta las celdas en orden
4. Completa los TODOs
5. Revisa los prints/checks
6. Compara con `Resolution` solo al final

---

## 📦 Requisitos

**Básico**: Python 3.8+

**Paquetes opcionales**:
- M3L1 E00: conexión a internet (DolarAPI)
- M3L1 E11/E12: OpenAI API (opcional)
- M3L2: LangChain, FAISS, embeddings
- M3L3: Python estándar; LangChain/OpenAI opcional para llevar los mocks a producción

En Google Colab, los notebooks instalan dependencias automáticamente.

---

# 🤖 M3L1 - Agentes, Tools y Loop ReAct

Aprende a construir **agentes inteligentes** que usen tools, implementa el **loop ReAct** y entiende cuándo usar un agente vs un pipeline.

> 🎯 **Objetivo**: Domina la construcción de agentes con herramientas y el ciclo Reason-Act-Observe

## 🎯 Ejercicios M3L1

| # | 📌 Ejercicio | 📖 Tema | ⏱️ Duración | 🎓 Nivel |
|---|-----------|------|----------|---------|
| 1 | **E00** | Pipeline vs agente con DolarAPI | 20 min | 🟢 Básico |
| 2 | **E01** | Contratos de tools | 20 min | 🟢 Básico |
| 3 | **E02** | Loop ReAct mínimo | 20 min | 🟢 Básico |
| 4 | **E03** | ReAct con dos tools encadenadas | 20 min | 🟠 Intermedio |
| 5 | **E10** | Pipeline vs agente (ventas) | 20-25 min | 🟠 Intermedio |
| 6 | **E11** | Tool use, seguridad y descriptions | 25-35 min | 🟠 Intermedio |
| 7 | **E12** | Trace ReAct y tool calling | 30-40 min | 🟠 Intermedio |
| 8 | **E13** | Custom tools robustas y errores | 25-30 min | 🔴 Avanzado |

### E00 - Pipeline vs ReAct con DolarAPI

**Carpeta**: `M3L1/E00_pipeline_vs_react_dolar`

**Objetivo**: Comparar una respuesta pipeline (sin observación) vs un agente ReAct que consulta datos en tiempo real.

**Qué aprenderás**:
- Diferencia entre pipeline y agente
- Llamadas a APIs externas
- Normalización de payloads
- Respuestas grounded en datos reales

**Notebooks**: 
- [M3L1_E00_Starter.ipynb](M3L1/E00_pipeline_vs_react_dolar/M3L1_E00_Starter.ipynb)
- [M3L1_E00_Resolution.ipynb](M3L1/E00_pipeline_vs_react_dolar/M3L1_E00_Resolution.ipynb)

---

### E01 - Contratos de Tools

**Carpeta**: `M3L1/E01_tool_contracts`

**Objetivo**: Entender que una tool debe tener un contrato claro y bien definido.

**Qué aprenderás**:
- Normalización de inputs
- Validación antes de actuar
- Salidas estructuradas
- Una responsabilidad por tool

**Notebooks**: 
- [M3L1_E01_Starter.ipynb](M3L1/E01_tool_contracts/M3L1_E01_Starter.ipynb)
- [M3L1_E01_Resolution.ipynb](M3L1/E01_tool_contracts/M3L1_E01_Resolution.ipynb)

---

### E02 - Loop ReAct Mínimo

**Carpeta**: `M3L1/E02_react_loop`

**Objetivo**: Implementar el ciclo ReAct (Reason-Act-Observe) desde cero.

**Qué aprenderás**:
- Ciclo completo de un agente
- Decision taking del LLM
- Tool execution
- Observation y step

**Notebooks**: 
- [M3L1_E02_Starter.ipynb](M3L1/E02_react_loop/M3L1_E02_Starter.ipynb)
- [M3L1_E02_Resolution.ipynb](M3L1/E02_react_loop/M3L1_E02_Resolution.ipynb)

---

### E03 - ReAct con Dos Tools Encadenadas

**Carpeta**: `M3L1/E03_react_clima_calculo`

**Objetivo**: Encadenar dos tools dentro del loop ReAct.

**Qué aprenderás**:
- Orquestación de múltiples tools
- Manejo de estado entre steps
- Composición de acciones

**Notebooks**: 
- [M3L1_E03_Starter.ipynb](M3L1/E03_react_clima_calculo/M3L1_E03_Starter.ipynb)
- [M3L1_E03_Resolution.ipynb](M3L1/E03_react_clima_calculo/M3L1_E03_Resolution.ipynb)

---

### E10 - Pipeline vs Agente en Ventas

**Carpeta**: `M3L1/E10_sales_pipeline_vs_agent`

**Objetivo**: Aplicar el concepto pipeline vs agente en un dominio de ventas.

**Qué aprenderás**:
- Análisis de reportes de ventas
- Cuándo un pipeline es suficiente
- Cuándo necesitas un agente

**Notebooks**: 
- [M3L1_E10_Starter.ipynb](M3L1/E10_sales_pipeline_vs_agent/M3L1_E10_Starter.ipynb)
- [M3L1_E10_Resolution.ipynb](M3L1/E10_sales_pipeline_vs_agent/M3L1_E10_Resolution.ipynb)

---

### E11 - Tool Use y Seguridad

**Carpeta**: `M3L1/E11_sales_tool_use`

**Objetivo**: Implementar tool use seguro con descripciones claras.

**Qué aprenderás**:
- Function calling con modelos
- Descripción efectiva de tools
- Validación de inputs
- Errores estructurados

**Notebooks**: 
- [M3L1_E11_Starter.ipynb](M3L1/E11_sales_tool_use/M3L1_E11_Starter.ipynb)
- [M3L1_E11_Resolution.ipynb](M3L1/E11_sales_tool_use/M3L1_E11_Resolution.ipynb)

---

### E12 - Trace ReAct y Tool Calling

**Carpeta**: `M3L1/E12_sales_react_loop`

**Objetivo**: Trazar y entender el flujo completo ReAct con tool calling.

**Qué aprenderás**:
- Debugging de agentes
- Visualización de traces
- Analysis de decisiones del LLM

**Notebooks**: 
- [M3L1_E12_Starter.ipynb](M3L1/E12_sales_react_loop/M3L1_E12_Starter.ipynb)
- [M3L1_E12_Resolution.ipynb](M3L1/E12_sales_react_loop/M3L1_E12_Resolution.ipynb)

---

### E13 - Custom Tools Robustas

**Carpeta**: `M3L1/E13_sales_custom_tools_robust`

**Objetivo**: Construir tools production-ready con manejo de errores.

**Qué aprenderás**:
- Error handling en tools
- Structured outputs
- Validación robusta
- Best practices

**Notebooks**: 
- [M3L1_E13_Starter.ipynb](M3L1/E13_sales_custom_tools_robust/M3L1_E13_Starter.ipynb)
- [M3L1_E13_Resolution.ipynb](M3L1/E13_sales_custom_tools_robust/M3L1_E13_Resolution.ipynb)

---

---

# 🦜 M3L2 - LangChain, LCEL, RAG y Embeddings

Aprende a construir sistemas complejos con **LangChain**, implementa **RAG (Retrieval Augmented Generation)** y trabaja con **embeddings** y **FAISS**.

> 🎯 **Objetivo**: Domina LangChain y construye sistemas RAG production-ready

## 🎯 Ejercicios M3L2

> 📐 **La numeración sigue el orden de dictado recomendado para una clase de 45 min**: fundamentos del modelo (E00-E03) → memoria y tools (E04-E06) → RAG en profundidad (E07-E12) → refactor de cierre (E13).

| # | 📌 Ejercicio | 📖 Tema | ⏱️ Duración | 🎓 Nivel |
|---|-----------|------|----------|---------|
| 1 | **E00** | LLM Wrapper (`ChatOpenAI` como objeto) | 20 min | 🟠 Intermedio |
| 2 | **E01** | PromptTemplate | 20 min | 🟠 Intermedio |
| 3 | **E02** | Output Parser | 20 min | 🟠 Intermedio |
| 4 | **E03** | LCEL Chain | 25 min | 🟠 Intermedio |
| 5 | **E04** | Chat con memoria en LangChain | 25 min | 🟠 Intermedio |
| 6 | **E05** | Tools con LangChain y API | 25 min | 🟠 Intermedio |
| 7 | **E06** | De manual a LangChain | 25 min | 🟠 Intermedio |
| 8 | **E07** | Embeddings | 25 min | 🟠 Intermedio |
| 9 | **E08** | FAISS | 30 min | 🟠 Intermedio |
| 10 | **E09** | Retriever | 25 min | 🟠 Intermedio |
| 11 | **E10** | RAG mini | 20 min | 🟢 Básico |
| 12 | **E11** | RAG con memoria | 35 min | 🟠 Intermedio |
| 13 | **E12** | RAG desde cero | 45 min | 🔴 Avanzado |
| 14 | **E13** | Refactor code | 30 min | 🟠 Intermedio |

> ➕ **Extra**: **E14 - LangChain vs Manual**, un repaso comparativo de todo el módulo (solo Resolution, sin Starter). Ver ficha al final de esta sección.

### E00 - LLM Wrapper

**Carpeta**: `M3L2/E00_llm_wrapper`

**Objetivo**: Envuelve un modelo como una herramienta reutilizable.

**Qué aprenderás**:
- LangChain LLM interface
- Custom wrappers
- Model abstraction
- Reusable components

**Notebooks**: 
- [M3L2_E00_Starter.ipynb](M3L2/E00_llm_wrapper/M3L2_E00_Starter.ipynb)
- [M3L2_E00_Resolution.ipynb](M3L2/E00_llm_wrapper/M3L2_E00_Resolution.ipynb)

---

### E01 - PromptTemplate

**Carpeta**: `M3L2/E01_prompt_template`

**Objetivo**: Del string manual al `ChatPromptTemplate`: variables explícitas, inspección y reutilización.

**Qué aprenderás**:
- Variables dinámicas
- Few-shot examples
- Template formatting
- Prompt engineering

**Notebooks**: 
- [M3L2_E01_Starter.ipynb](M3L2/E01_prompt_template/M3L2_E01_Starter.ipynb)
- [M3L2_E01_Resolution.ipynb](M3L2/E01_prompt_template/M3L2_E01_Resolution.ipynb)

---

### E02 - Output Parser

**Carpeta**: `M3L2/E02_output_parser`

**Objetivo**: Parsea y estructura outputs del LLM.

**Qué aprenderás**:
- Output parsing
- JSON structuring
- Error recovery
- Custom parsers

**Notebooks**: 
- [M3L2_E02_Starter.ipynb](M3L2/E02_output_parser/M3L2_E02_Starter.ipynb)
- [M3L2_E02_Resolution.ipynb](M3L2/E02_output_parser/M3L2_E02_Resolution.ipynb)

---

### E03 - LCEL Chain

**Carpeta**: `M3L2/E03_lcel_chain`

**Objetivo**: Componer `prompt | llm | parser` con el operador `|` de LCEL.

**Qué aprenderás**:
- Advanced LCEL patterns
- Branching and routing
- Conditional chains
- Parallel processing

**Notebooks**: 
- [M3L2_E03_Starter.ipynb](M3L2/E03_lcel_chain/M3L2_E03_Starter.ipynb)
- [M3L2_E03_Resolution.ipynb](M3L2/E03_lcel_chain/M3L2_E03_Resolution.ipynb)

---

### E04 - Chat con Memoria en LangChain

**Carpeta**: `M3L2/E04_chat_con_memoria_langchain`

**Objetivo**: Implementa un chat que recuerda la conversación.

**Qué aprenderás**:
- Memory types
- ConversationBufferMemory
- Message history
- Context management

**Notebooks**: 
- [M3L2_E04_Starter.ipynb](M3L2/E04_chat_con_memoria_langchain/M3L2_E04_Starter.ipynb)
- [M3L2_E04_Resolution.ipynb](M3L2/E04_chat_con_memoria_langchain/M3L2_E04_Resolution.ipynb)

---

### E05 - Tools con LangChain y API

**Carpeta**: `M3L2/E05_tools_langchain_api_dolar`

**Objetivo**: Integra tools externas (APIs) con LangChain.

**Qué aprenderás**:
- Tool definition en LangChain
- API integration
- Function calling
- Tool validation

**Notebooks**: 
- [M3L2_E05_Starter.ipynb](M3L2/E05_tools_langchain_api_dolar/M3L2_E05_Starter.ipynb)
- [M3L2_E05_Resolution.ipynb](M3L2/E05_tools_langchain_api_dolar/M3L2_E05_Resolution.ipynb)

---

### E06 - De Manual a LangChain

**Carpeta**: `M3L2/E06_manual_to_langchain`

**Objetivo**: Refactoriza código manual a LangChain.

**Qué aprenderás**:
- LangChain advantages
- Migration patterns
- Simplification
- Best practices

**Notebooks**: 
- [M3L2_E06_Starter.ipynb](M3L2/E06_manual_to_langchain/M3L2_E06_Starter.ipynb)
- [M3L2_E06_Resolution.ipynb](M3L2/E06_manual_to_langchain/M3L2_E06_Resolution.ipynb)

---

### E07 - Embeddings

**Carpeta**: `M3L2/E07_embeddings`

**Objetivo**: Trabajar con embeddings para representación semántica.

**Qué aprenderás**:
- Embedding models
- Vector representation
- Similarity search
- Embedding basics for RAG

**Notebooks**: 
- [M3L2_E07_Starter.ipynb](M3L2/E07_embeddings/M3L2_E07_Starter.ipynb)
- [M3L2_E07_Resolution.ipynb](M3L2/E07_embeddings/M3L2_E07_Resolution.ipynb)

---

### E08 - FAISS

**Carpeta**: `M3L2/E08_faiss`

**Objetivo**: Vector store con FAISS para búsqueda eficiente.

**Qué aprenderás**:
- FAISS library
- Index creation
- Similarity search at scale
- Vector DB basics

**Notebooks**: 
- [M3L2_E08_Starter.ipynb](M3L2/E08_faiss/M3L2_E08_Starter.ipynb)
- [M3L2_E08_Resolution.ipynb](M3L2/E08_faiss/M3L2_E08_Resolution.ipynb)

---

### E09 - Retriever

**Carpeta**: `M3L2/E09_retriever`

**Objetivo**: Implementa retrievers personalizados.

**Qué aprenderás**:
- Retriever interface
- Custom retrieval logic
- Multi-source retrieval
- Retriever evaluation

**Notebooks**: 
- [M3L2_E09_Starter.ipynb](M3L2/E09_retriever/M3L2_E09_Starter.ipynb)
- [M3L2_E09_Resolution.ipynb](M3L2/E09_retriever/M3L2_E09_Resolution.ipynb)

---

### E10 - RAG Mini

**Carpeta**: `M3L2/E10_rag_mini`

**Objetivo**: RAG minimalista y eficiente.

**Qué aprenderás**:
- Minimalist RAG design
- Essential components only
- Performance optimization
- Simple but effective

**Notebooks**: 
- [M3L2_E10_Starter.ipynb](M3L2/E10_rag_mini/M3L2_E10_Starter.ipynb)
- [M3L2_E10_Resolution.ipynb](M3L2/E10_rag_mini/M3L2_E10_Resolution.ipynb)

---

### E11 - RAG con Memoria

**Carpeta**: `M3L2/E11_rag_chat_con_memoria`

**Objetivo**: Combina RAG con memoria para conversaciones contextuales.

**Qué aprenderás**:
- RAG + memory
- Context preservation
- History management
- Multi-turn RAG

**Notebooks**: 
- [M3L2_E11_Starter.ipynb](M3L2/E11_rag_chat_con_memoria/M3L2_E11_Starter.ipynb)
- [M3L2_E11_Resolution.ipynb](M3L2/E11_rag_chat_con_memoria/M3L2_E11_Resolution.ipynb)

---

### E12 - RAG desde Cero

**Carpeta**: `M3L2/E12_rag_desde_cero`

**Objetivo**: Construye un RAG completo desde cero integrando todo lo aprendido.

**Qué aprenderás**:
- End-to-end RAG system
- Document processing
- Retrieval + generation
- Production considerations

**Notebooks**: 
- [M3L2_E12_Starter.ipynb](M3L2/E12_rag_desde_cero/M3L2_E12_Starter.ipynb)
- [M3L2_E12_Resolution.ipynb](M3L2/E12_rag_desde_cero/M3L2_E12_Resolution.ipynb)

---

### E13 - Refactor Code

**Carpeta**: `M3L2/E13_refactor_chaos`

**Objetivo**: Refactoriza código desordenado a una estructura limpia (taller grupal de cierre).

**Qué aprenderás**:
- Code organization
- Best practices
- Modularity
- Maintainability

**Notebooks**: 
- [M3L2_E13_Starter.ipynb](M3L2/E13_refactor_chaos/M3L2_E13_Starter.ipynb)
- [M3L2_E13_Resolution.ipynb](M3L2/E13_refactor_chaos/M3L2_E13_Resolution.ipynb)

---

### E14 - LangChain vs Manual (extra)

**Carpeta**: `M3L2/E14_langchain_vs_manual`

**Objetivo**: Recorrido comparativo de todo M3L2 — cada concepto (modelo, prompt, parser, LCEL, memoria, tools, embeddings, vector store, retriever y el pipeline RAG completo) implementado dos veces, a mano con el SDK de `openai` y con LangChain, lado a lado.

Es un notebook **extra**, solo Resolution (no tiene Starter con TODOs): sirve como repaso integrador antes de pasar a M3L3.

**Qué aprenderás**:
- Qué reemplaza exactamente cada componente de LangChain
- Por qué esas abstracciones importan cuando el sistema crece
- A debuggear entendiendo qué hay "debajo" de cada pieza del framework

**Notebook**:
- [M3L2_E14_Resolution.ipynb](M3L2/E14_langchain_vs_manual/M3L2_E14_Resolution.ipynb)

---

# 🧩 M3L3 - Sistemas Multiagente, Orquestación y Estado

Aprende a construir **sistemas multiagente** sobre lo aprendido en M3L2: clasificación de intención, agentes especialistas, orquestadores, handoffs, protocolos de salida y conversación con estado.

> 🎯 **Objetivo**: Domina la coordinación de agentes especializados y diseña arquitecturas multiagente auditables

## 🎯 Ejercicios M3L3

| # | 📌 Ejercicio | 📖 Tema | ⏱️ Duración | 🎓 Nivel |
|---|-----------|------|----------|---------|
| 1 | **E00** | El problema del agente único | 25 min | 🟢 Básico |
| 2 | **E01** | Intent classifier | 25 min | 🟢 Básico |
| 3 | **E02** | Agentes especialistas con RAG | 30 min | 🟠 Intermedio |
| 4 | **E03** | Orquestador básico | 30 min | 🟠 Intermedio |
| 5 | **E04** | Consulta mixta y delegación paralela | 30 min | 🟠 Intermedio |
| 6 | **E05** | Handoff con contexto | 30 min | 🟠 Intermedio |
| 7 | **E06** | Protocolos de output estructurado | 30 min | 🟠 Intermedio |
| 8 | **E10** | Support bot baseline | 35 min | 🟠 Intermedio |
| 9 | **E11** | Support bot multiagente | 40 min | 🔴 Avanzado |
| 10 | **E12** | Orquestador con OpenAI Functions | 35 min | 🔴 Avanzado |
| 11 | **E13** | Sistema completo con estado | 45 min | 🔴 Avanzado |

### E00 - El Problema del Agente Único

**Carpeta**: `M3L3/E00_el_problema_del_agente_unico`

**Objetivo**: Entender por qué un solo agente empieza a fallar cuando debe responder sobre múltiples dominios.

**Qué aprenderás**:
- Diferencia entre agente generalista y especialista
- Concepto de dominio
- Errores típicos por mezclar responsabilidades
- Motivación para arquitectura multiagente

**Notebooks**:
- [M3L3_E00_Starter.ipynb](M3L3/E00_el_problema_del_agente_unico/M3L3_E00_Starter.ipynb)
- [M3L3_E00_Resolution.ipynb](M3L3/E00_el_problema_del_agente_unico/M3L3_E00_Resolution.ipynb)

---

### E01 - Intent Classifier

**Carpeta**: `M3L3/E01_intent_classifier`

**Objetivo**: Clasificar la intención de una consulta para decidir a qué agente enviarla.

**Qué aprenderás**:
- Intents y routing
- Salidas JSON estructuradas
- Parsing y validación de outputs
- Fallback a `unknown`

**Notebooks**:
- [M3L3_E01_Starter.ipynb](M3L3/E01_intent_classifier/M3L3_E01_Starter.ipynb)
- [M3L3_E01_Resolution.ipynb](M3L3/E01_intent_classifier/M3L3_E01_Resolution.ipynb)

---

### E02 - Agentes Especialistas con RAG

**Carpeta**: `M3L3/E02_agentes_especialistas_con_rag`

**Objetivo**: Construir agentes especialistas, cada uno con su propio conocimiento por dominio.

**Qué aprenderás**:
- Separación de índices por dominio
- Retrieval especializado
- Encapsulación de agentes como funciones
- Comparación entre índice correcto e incorrecto

**Notebooks**:
- [M3L3_E02_Starter.ipynb](M3L3/E02_agentes_especialistas_con_rag/M3L3_E02_Starter.ipynb)
- [M3L3_E02_Resolution.ipynb](M3L3/E02_agentes_especialistas_con_rag/M3L3_E02_Resolution.ipynb)

---

### E03 - Orquestador Básico

**Carpeta**: `M3L3/E03_orquestador_basico`

**Objetivo**: Combinar clasificador, registro de agentes y función principal de ruteo.

**Qué aprenderás**:
- Responsabilidad del orquestador
- Registro de agentes
- Trace visible de decisiones
- Flujo classify → route → execute

**Notebooks**:
- [M3L3_E03_Starter.ipynb](M3L3/E03_orquestador_basico/M3L3_E03_Starter.ipynb)
- [M3L3_E03_Resolution.ipynb](M3L3/E03_orquestador_basico/M3L3_E03_Resolution.ipynb)

---

### E04 - Consulta Mixta y Delegación Paralela

**Carpeta**: `M3L3/E04_consulta_mixta_delegacion_paralela`

**Objetivo**: Detectar múltiples intenciones y delegar una misma consulta a varios agentes.

**Qué aprenderás**:
- Multi-intent classification
- Delegación paralela conceptual
- Merge de respuestas
- Manejo de consultas mixtas

**Notebooks**:
- [M3L3_E04_Starter.ipynb](M3L3/E04_consulta_mixta_delegacion_paralela/M3L3_E04_Starter.ipynb)
- [M3L3_E04_Resolution.ipynb](M3L3/E04_consulta_mixta_delegacion_paralela/M3L3_E04_Resolution.ipynb)

---

### E05 - Handoff con Contexto

**Carpeta**: `M3L3/E05_handoff_con_contexto`

**Objetivo**: Transferir una tarea de un agente a otro sin perder contexto.

**Qué aprenderás**:
- Handoff entre agentes
- `TypedDict` como contrato
- Payloads de transferencia
- Buena UX sin repetir información

**Notebooks**:
- [M3L3_E05_Starter.ipynb](M3L3/E05_handoff_con_contexto/M3L3_E05_Starter.ipynb)
- [M3L3_E05_Resolution.ipynb](M3L3/E05_handoff_con_contexto/M3L3_E05_Resolution.ipynb)

---

### E06 - Protocolos de Output Estructurado

**Carpeta**: `M3L3/E06_protocolos_output_estructurado`

**Objetivo**: Estandarizar la respuesta de todos los agentes con un contrato común.

**Qué aprenderás**:
- `AgentResponse`
- Estados `success`, `needs_clarification` y `out_of_scope`
- Orquestación basada en status
- Respuestas auditables

**Notebooks**:
- [M3L3_E06_Starter.ipynb](M3L3/E06_protocolos_output_estructurado/M3L3_E06_Starter.ipynb)
- [M3L3_E06_Resolution.ipynb](M3L3/E06_protocolos_output_estructurado/M3L3_E06_Resolution.ipynb)

---

### E10 - Support Bot Baseline

**Carpeta**: `M3L3/E10_support_bot_baseline`

**Objetivo**: Medir el punto de partida de un bot único antes del refactor multiagente.

**Qué aprenderás**:
- Baselines y benchmarks
- Documentos mezclados
- Métricas simples de accuracy
- Patrones de error

**Notebooks**:
- [M3L3_E10_Starter.ipynb](M3L3/E10_support_bot_baseline/M3L3_E10_Starter.ipynb)
- [M3L3_E10_Resolution.ipynb](M3L3/E10_support_bot_baseline/M3L3_E10_Resolution.ipynb)

---

### E11 - Support Bot Multiagente

**Carpeta**: `M3L3/E11_support_bot_multi_agent`

**Objetivo**: Refactorizar el baseline con agentes especialistas y comparar resultados.

**Qué aprenderás**:
- Arquitectura multiagente end-to-end
- Reutilización de `AgentResponse`
- Comparación E10 vs E11
- Aha moment con benchmark fijo

**Notebooks**:
- [M3L3_E11_Starter.ipynb](M3L3/E11_support_bot_multi_agent/M3L3_E11_Starter.ipynb)
- [M3L3_E11_Resolution.ipynb](M3L3/E11_support_bot_multi_agent/M3L3_E11_Resolution.ipynb)

---

### E12 - Orquestador con OpenAI Functions

**Carpeta**: `M3L3/E12_orquestador_openai_functions`

**Objetivo**: Entender cómo el LLM puede elegir agentes mediante function calling/tool use.

**Qué aprenderás**:
- Tools como agentes
- Descripciones efectivas de tools
- Tool choice
- Routing manual vs function calling

**Notebooks**:
- [M3L3_E12_Starter.ipynb](M3L3/E12_orquestador_openai_functions/M3L3_E12_Starter.ipynb)
- [M3L3_E12_Resolution.ipynb](M3L3/E12_orquestador_openai_functions/M3L3_E12_Resolution.ipynb)

---

### E13 - Sistema Completo con Estado

**Carpeta**: `M3L3/E13_sistema_completo_con_estado`

**Objetivo**: Integrar sesión, historial, guardrails, fallback y conversación multi-turno.

**Qué aprenderás**:
- `SessionState`
- Estado conversacional
- Guardrails y fallback
- Sistema multiagente completo

**Notebooks**:
- [M3L3_E13_Starter.ipynb](M3L3/E13_sistema_completo_con_estado/M3L3_E13_Starter.ipynb)
- [M3L3_E13_Resolution.ipynb](M3L3/E13_sistema_completo_con_estado/M3L3_E13_Resolution.ipynb)

---

# 📊 M3L4 - Tracing, Observabilidad y Producción

Aprende a instrumentar, tracear y mejorar agentes en producción. Desde MiniTracer en Python puro hasta integración con Langfuse para observabilidad profesional.

> 🎯 **Objetivo**: Domina la observabilidad de agentes: tracing, golden datasets, evaluadores, dashboards y ciclos de mejora iterativa

## 🎯 Ejercicios M3L4

| # | 📌 Ejercicio | 📖 Tema | ⏱️ Duración | 🎓 Nivel |
|---|-----------|------|----------|---------|
| 1 | **E00** | Logs tradicionales vs Tracing estructurado | 15 min | 🟢 Básico |
| 2 | **E01** | MiniTracer en Python puro | 20 min | 🟢 Básico |
| 3 | **E02** | Tracing de sistema multiagente mock | 20 min | 🟠 Intermedio |
| 4 | **E03** | Debugging con traces | 25 min | 🟠 Intermedio |
| 5 | **E04** | Golden Dataset para routing | 20 min | 🟠 Intermedio |
| 6 | **E05** | Router v1 vs v2 | 20 min | 🟠 Intermedio |
| 7 | **E06** | Evaluator Agent simple | 20 min | 🟠 Intermedio |
| 8 | **E07** | Dashboard local de métricas | 20 min | 🟠 Intermedio |
| 9 | **E08** | LangGraph básico + Langfuse | 25 min | 🟠 Intermedio |
| 10 | **E09** | LangGraph router + Langfuse | 25 min | 🟠 Intermedio |
| 11 | **E10** | LangGraph supervisor + Langfuse | 30 min | 🔴 Avanzado |
| 12 | **E11** | Golden Dataset + Langfuse Scores | 30 min | 🔴 Avanzado |
| 13 | **E12** | Ciclo completo de mejora iterativa | 30 min | 🔴 Avanzado |

### E00 - Logs vs Tracing

**Carpeta**: M3L4/E00_logs_vs_tracing

**Objetivo**: Entender por qué los logs tradicionales no alcanzan para debuggear agentes y cómo el tracing estructurado resuelve esas limitaciones.

**Qué aprenderás**:
- Diferencias entre logs planos y traces estructurados
- Jerarquía de spans con input, output y duración
- Detección de misclassification con metadata
- Por qué el tracing es esencial para agentes en producción

**Notebooks**:
- [M3L4_E00_Starter.ipynb](M3L4/E00_logs_vs_tracing/M3L4_E00_Starter.ipynb)
- [M3L4_E00_Resolution.ipynb](M3L4/E00_logs_vs_tracing/M3L4_E00_Resolution.ipynb)

---

### E01 - MiniTracer en Python

**Carpeta**: M3L4/E01_mini_tracer_python

**Objetivo**: Construir una clase MiniTracer desde cero que automatiza la creación de traces, spans y cálculos de duración.

**Qué aprenderás**:
- Clase MiniTracer con start_trace, add_span, update_trace_output
- Generación automática de trace_id y span_id con UUID
- Cálculo automático de duración total
- Fundamentos de cómo funcionan Langfuse y LangSmith por debajo

**Notebooks**:
- [M3L4_E01_Starter.ipynb](M3L4/E01_mini_tracer_python/M3L4_E01_Starter.ipynb)
- [M3L4_E01_Resolution.ipynb](M3L4/E01_mini_tracer_python/M3L4_E01_Resolution.ipynb)

---

### E02 - Tracing Multiagente Mock

**Carpeta**: M3L4/E02_tracing_multiagente_mock

**Objetivo**: Integrar el MiniTracer dentro de un sistema multiagente real para tracear cada request automáticamente.

**Qué aprenderás**:
- Instrumentación de un sistema con tracing
- Medición de duración real con time.time()
- Metadata de entorno y versión del router
- Traces automáticos para cada consulta

**Notebooks**:
- [M3L4_E02_Starter.ipynb](M3L4/E02_tracing_multiagente_mock/M3L4_E02_Starter.ipynb)
- [M3L4_E02_Resolution.ipynb](M3L4/E02_tracing_multiagente_mock/M3L4_E02_Resolution.ipynb)

---

### E03 - Debugging con Traces

**Carpeta**: M3L4/E03_debugging_con_traces

**Objetivo**: Aprender a diagnosticar problemas comunes en agentes usando traces: misclassification, retrieval vacío, latencia alta, loops y errores silenciosos.

**Qué aprenderás**:
- Firmas de cada problema en la estructura del trace
- Función diagnose_trace con reglas de detección
- Suggested fixes para cada tipo de problema
- Debugging sistemático de agentes

**Notebooks**:
- [M3L4_E03_Starter.ipynb](M3L4/E03_debugging_con_traces/M3L4_E03_Starter.ipynb)
- [M3L4_E03_Resolution.ipynb](M3L4/E03_debugging_con_traces/M3L4_E03_Resolution.ipynb)

---

### E04 - Golden Dataset para Routing

**Carpeta**: M3L4/E04_golden_dataset_routing

**Objetivo**: Crear un conjunto de casos etiquetados manualmente para medir objetivamente la precisión del routing.

**Qué aprenderás**:
- Concepto de golden dataset y ground truth
- Evaluación de routing accuracy
- Análisis de fallos por dominio
- Precisión por intent

**Notebooks**:
- [M3L4_E04_Starter.ipynb](M3L4/E04_golden_dataset_routing/M3L4_E04_Starter.ipynb)
- [M3L4_E04_Resolution.ipynb](M3L4/E04_golden_dataset_routing/M3L4_E04_Resolution.ipynb)

---

### E05 - Router v1 vs v2

**Carpeta**: M3L4/E05_router_v1_vs_v2

**Objetivo**: Comparar dos versiones del router contra el mismo golden dataset para decidir cuál es mejor.

**Qué aprenderás**:
- A/B testing de routers
- Keywords expandidas vs básicas
- Detección de multi_intent y clarification
- Mejora cuantificable con datos

**Notebooks**:
- [M3L4_E05_Starter.ipynb](M3L4/E05_router_v1_vs_v2/M3L4_E05_Starter.ipynb)
- [M3L4_E05_Resolution.ipynb](M3L4/E05_router_v1_vs_v2/M3L4_E05_Resolution.ipynb)

---

### E06 - Evaluator Agent Simple

**Carpeta**: M3L4/E06_evaluator_agent_simple

**Objetivo**: Construir un evaluador que califica la calidad de las respuestas del agente según keywords esperadas.

**Qué aprenderás**:
- Evaluación de calidad de respuestas
- Keyword matching para scoring
- Limitaciones del enfoque basado en keywords
- Preparación para LLM-as-judge

**Notebooks**:
- [M3L4_E06_Starter.ipynb](M3L4/E06_evaluator_agent_simple/M3L4_E06_Starter.ipynb)
- [M3L4_E06_Resolution.ipynb](M3L4/E06_evaluator_agent_simple/M3L4_E06_Resolution.ipynb)

---

### E07 - Dashboard Local de Métricas

**Carpeta**: M3L4/E07_dashboard_metricas_local

**Objetivo**: Consolidar todas las métricas del sistema en un dashboard con pandas: accuracy, latencia, P95, calidad y detección de anomalías.

**Qué aprenderás**:
- Métricas globales del sistema
- P95 latency y su importancia
- Precisión y latencia por dominio
- Detección de casos anómalos

**Notebooks**:
- [M3L4_E07_Starter.ipynb](M3L4/E07_dashboard_metricas_local/M3L4_E07_Starter.ipynb)
- [M3L4_E07_Resolution.ipynb](M3L4/E07_dashboard_metricas_local/M3L4_E07_Resolution.ipynb)

---

### E08 - LangGraph Básico + Langfuse

**Carpeta**: M3L4/E08_langgraph_basico_langfuse

**Objetivo**: Integrar LangGraph con Langfuse mediante CallbackHandler para tracing automático.

**Qué aprenderás**:
- StateGraph básico con un nodo
- CallbackHandler de Langfuse
- Traces automáticos en cloud.langfuse.com
- Diferencias con MiniTracer manual

**Notebooks**:
- [M3L4_E08_Starter.ipynb](M3L4/E08_langgraph_basico_langfuse/M3L4_E08_Starter.ipynb)
- [M3L4_E08_Resolution.ipynb](M3L4/E08_langgraph_basico_langfuse/M3L4_E08_Resolution.ipynb)

---

### E09 - LangGraph Router + Langfuse

**Carpeta**: M3L4/E09_langgraph_router_langfuse

**Objetivo**: Construir un grafo con routing condicional y tracear la ruta elegida en Langfuse.

**Qué aprenderás**:
- Conditional edges en LangGraph
- Router node + specialist nodes
- Tags y metadata en traces de Langfuse
- Visualización de la ruta ejecutada

**Notebooks**:
- [M3L4_E09_Starter.ipynb](M3L4/E09_langgraph_router_langfuse/M3L4_E09_Starter.ipynb)
- [M3L4_E09_Resolution.ipynb](M3L4/E09_langgraph_router_langfuse/M3L4_E09_Resolution.ipynb)

---

### E10 - LangGraph Supervisor + Langfuse

**Carpeta**: M3L4/E10_langgraph_multiagente_supervisor_langfuse

**Objetivo**: Agregar un supervisor que controla el flujo entre agentes, registra agentes visitados y previene loops.

**Qué aprenderás**:
- Supervisor node separado del router
- visited_agents para prevención de loops
- Handoff controlado entre agentes
- Estado compartido con TypedDict

**Notebooks**:
- [M3L4_E10_Starter.ipynb](M3L4/E10_langgraph_multiagente_supervisor_langfuse/M3L4_E10_Starter.ipynb)
- [M3L4_E10_Resolution.ipynb](M3L4/E10_langgraph_multiagente_supervisor_langfuse/M3L4_E10_Resolution.ipynb)

---

### E11 - Golden Dataset + Langfuse Scores

**Carpeta**: M3L4/E11_langgraph_golden_dataset_scores

**Objetivo**: Ejecutar el golden dataset contra LangGraph y registrar scores automáticos en Langfuse.

**Qué aprenderás**:
- Integración de golden dataset con LangGraph
- langfuse.create_score() para cada caso
- Trazabilidad completa por caso de prueba
- Dashboard de accuracy en Langfuse

**Notebooks**:
- [M3L4_E11_Starter.ipynb](M3L4/E11_langgraph_golden_dataset_scores/M3L4_E11_Starter.ipynb)
- [M3L4_E11_Resolution.ipynb](M3L4/E11_langgraph_golden_dataset_scores/M3L4_E11_Resolution.ipynb)

---

### E12 - Ciclo de Mejora Iterativa

**Carpeta**: M3L4/E12_ciclo_mejora_iterativa

**Objetivo**: Completar el ciclo completo: medir, diagnosticar, fixear, re-medir y documentar con un fix report.

**Qué aprenderás**:
- Ciclo completo Medir-Diagnosticar-Fixear-Re-medir-Documentar
- Fix report con causa raíz, cambio y métricas
- Before/After con golden dataset
- Ingeniería de IA basada en datos

**Notebooks**:
- [M3L4_E12_Starter.ipynb](M3L4/E12_ciclo_mejora_iterativa/M3L4_E12_Starter.ipynb)
- [M3L4_E12_Resolution.ipynb](M3L4/E12_ciclo_mejora_iterativa/M3L4_E12_Resolution.ipynb)

---

---

## 🗺️ Roadmap Completo del Módulo

```
┌─────────────────────────────────────────────────────────────────┐
│                        M3L1: Agentes                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  E00 ──► E01 ──► E02 ──► E03                                   │
│  Pipeline  Tools  ReAct   Chains                                │
│    vs      &       Loop   Multiple                              │
│  Agents   Contracts         Tools                               │
│                                                                 │
│         ▼────────────────────▼                                  │
│                                                                 │
│  E10 ──► E11 ──► E12 ──► E13                                   │
│  Sales    Tool     ReAct   Custom                               │
│  Pipeline Use    Trace    Tools                                 │
│    vs    Security Trace   Robusto                               │
│  Agent                                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              M3L2: LangChain, LCEL, RAG                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FUNDAMENTALES          CADENAS              RAG                │
│  ──────────────         ────────────         ─────              │
│  E00: LLM Wrapper       E01: Prompt      E07: Embeddings        │
│  E02: Output Parser     E03: LCEL        E08: FAISS             │
│  E04: Memory            E06: Manual→LC   E09: Retriever         │
│  E05: Tools API                          E10: RAG Mini          │
│                                          E11: RAG Memory         │
│                                          E12: RAG Full           │
│                                                                 │
│       ▼─────────────────▼─────────────────▼                    │
│                                                                 │
│  CIERRE                                                         │
│  ────────                                                       │
│  E13: Refactor (taller grupal de integracion)                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              M3L3: Sistemas Multiagente                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FUNDAMENTOS             ORQUESTACIÓN          SISTEMA FINAL     │
│  ───────────             ─────────────         ─────────────     │
│  E00: Agente único       E03: Router           E10: Baseline     │
│  E01: Intent classifier  E04: Multi-intent     E11: Multi-agent  │
│  E02: Specialists RAG    E05: Handoff          E12: Functions    │
│                          E06: Protocolos       E13: Estado       │
│                                                                 │
│       ▼─────────────────▼─────────────────▼                    │
│                                                                 │
│  De un bot generalista a un sistema con agentes especialistas,  │
│  contratos explícitos, handoff, tool choice y guardrails.       │

┌─────────────────────────────────────────────────────────────────┐
│              M3L4: Tracing, Observabilidad y Producción          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FUNDAMENTOS              MÉTRICAS              PRODUCCIÓN       │
│  ───────────              ─────────             ──────────       │
│  E00: Logs vs Tracing     E04: Golden Dataset   E08: LangGraph   │
│  E01: MiniTracer          E05: Router v1 vs v2  E09: Router LG   │
│  E02: Tracing multiagente E06: Evaluator Agent  E10: Supervisor  │
│  E03: Debugging           E07: Dashboard        E11: Scores LG   │
│                                                 E12: Mejora      │
│                                                                  │
│       ▼─────────────────▼─────────────────▼                     │
│                                                                  │
│  De logs planos a trazabilidad completa con Langfuse,            │
│  golden datasets y mejora continua basada en datos.              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎓 Conceptos Clave Cubiertos

### 🤖 M3L1: Agentes
- ✅ **Agentes vs Pipelines**: Cuándo usar cada uno
- ✅ **Loop ReAct**: Reason → Act → Observe
- ✅ **Tool Design**: Contratos claros y robustos
- ✅ **Tool Calling**: Function calling con LLMs
- ✅ **Error Handling**: Manejo de errores estructurado
- ✅ **Agent Traces**: Debugging y observabilidad

### 🦜 M3L2: LangChain & RAG
- ✅ **LangChain Framework**: Componentes y patrones
- ✅ **LCEL**: Composición declarativa de cadenas
- ✅ **Prompts**: Templates y few-shot engineering
- ✅ **Memory**: Gestión de contexto conversacional
- ✅ **RAG**: Retrieval-Augmented Generation
- ✅ **Embeddings**: Representaciones semánticas
- ✅ **Vector Stores**: FAISS y otros
- ✅ **Retrievers**: Búsqueda y ranking
- ✅ **Output Parsing**: Estructuración de outputs

### 🧩 M3L3: Sistemas Multiagente
- ✅ **Intent Classification**: Clasificación de intención para routing
- ✅ **Specialist Agents**: Agentes por dominio con conocimiento separado
- ✅ **Orchestration**: Clasificar, rutear, ejecutar y trazar decisiones
- ✅ **Multi-intent Delegation**: Consultas mixtas y merge de respuestas
- ✅ **Handoff**: Transferencia de contexto entre agentes
- ✅ **AgentResponse**: Protocolos de salida estructurada
- ✅ **Tool Choice**: Orquestación con function calling/tools
- ✅ **Session State**: Estado, historial, guardrails y fallback

### 📊 M3L4: Tracing y Observabilidad
- ✅ **Logs vs Traces**: Por qué los logs no alcanzan para agentes
- ✅ **MiniTracer**: Implementación de tracing desde cero
- ✅ **Debugging con Traces**: Diagnóstico de misclassification, loops, latencia
- ✅ **Golden Dataset**: Evaluación objetiva con casos etiquetados
- ✅ **Router A/B Testing**: Comparación de versiones con datos
- ✅ **Evaluator Agent**: Scoring de calidad de respuestas
- ✅ **Dashboard de Métricas**: Accuracy, P95 latency, calidad por dominio
- ✅ **LangGraph + Langfuse**: Tracing automático en producción
- ✅ **Langfuse Scores**: Calificación automática por trace
- ✅ **Ciclo de Mejora Iterativa**: Medir, diagnosticar, fixear, documentar

---

## 💡 Tips para Maximizar el Aprendizaje

| 💡 Tip | 📝 Descripción |
|--------|----------------|
| **📚 Lee primero** | Abre el Starter, no vayas directo a Resolution |
| **🤔 Experimenta** | Modifica el código, rompe cosas, aprende |
| **⏱️ Sigue el orden** | Cada ejercicio se basa en conceptos previos |
| **✅ Haz los checks** | Los tests validan tu comprensión |
| **🔍 Compara** | Lee Resolution después para entender mejoras |
| **📝 Toma notas** | Escribe lo que aprendes en cada sección |
| **🎨 Experimenta** | Adapta a tus casos de uso después |

---

## 🆘 Troubleshooting & FAQ

### ❌ Errores Comunes

**ImportError: No module named 'langchain'**
```bash
pip install -U langchain langchain-community
```

**API Key Issues**
```python
# Siempre usa getpass para credentials
from getpass import getpass
api_key = getpass("Enter your API key: ")
# Nunca guardes keys en el notebook
```

**FAISS Installation**
```bash
# CPU (recomendado para desarrollo)
pip install faiss-cpu

# GPU (opcional, requiere CUDA)
pip install faiss-gpu
```

**En Google Colab**
```python
# Instala todo de una vez
!pip install -q langchain langchain-community langchain-openai faiss-cpu python-dotenv
```

### ✅ En Colab
- ✨ Las dependencias se instalan automáticamente en la mayoría de notebooks
- ⚡ Si algo falla: ejecuta `!pip install --upgrade [paquete]`
- 📁 Usa `/content/` para rutas de archivo

---

## 🎓 Conceptos Clave Cubiertos

### M3L1
- ✅ Agentes y automonía
- ✅ Loop ReAct
- ✅ Tool design y contratos
- ✅ Tool calling y function calling
- ✅ Error handling en tools
- ✅ Agent traces y debugging

### M3L2
- ✅ LangChain framework
- ✅ LCEL (LangChain Expression Language)
- ✅ Prompts y templates
- ✅ Memory management
- ✅ RAG (Retrieval-Augmented Generation)
- ✅ Embeddings y vector stores
- ✅ FAISS para búsqueda eficiente
- ✅ Output parsing
- ✅ Retrievers personalizados

### M3L3
- ✅ Sistemas multiagente
- ✅ Intent classification y routing
- ✅ Agentes especialistas con RAG
- ✅ Orquestadores y traces
- ✅ Handoff con contexto
- ✅ Output estructurado con `AgentResponse`
- ✅ Function calling / tool choice
- ✅ Estado conversacional y guardrails

---

## 💡 Tips para Maximizar el Aprendizaje

1. **Sigue el orden sugerido**: Cada ejercicio se basa en conceptos previos
2. **Lee el Starter primero**: No saltes directo a Resolution
3. **Intenta resolver sin copiar**: El error es parte del aprendizaje
4. **Experimenta después**: Modifica y juega con los notebooks
5. **Compara soluciones**: Entiende por qué Resolution es diferente
6. **Toma notas**: Escribe lo que aprendes en cada sección

---


## 📊 Estadísticas del Módulo

| Métrica | Valor |
|---------|-------|
| **Ejercicios Totales** | 46 |
| **Notebooks** | 92 (46 Starter + 46 Resolution) |
| **Tiempo Total Estimado** | ~32-38 horas |
| **Tópicos Cubiertos** | 40+ |
| **Líneas de Código** | 9,000+ |




