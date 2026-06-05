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
└── M3L2/
    ├── E00 → Chat + PromptTemplate
    ├── E01 → LCEL Chains
    ├── E02 → Chat + Memory
    ├── E03 → Tools + API
    ├── E04 → RAG Básico
    ├── E05 → RAG + Memory
    ├── E06 → De Manual a LangChain
    ├── E07 → PromptTemplate Avanzado
    ├── E08 → LCEL Avanzado
    ├── E09 → RAG Mini
    ├── E10 → LLM Wrapper
    ├── E11 → Output Parser
    ├── E12 → Embeddings
    ├── E13 → FAISS
    ├── E14 → Retriever
    ├── E15 → Refactor Code
    └── E16 → RAG desde Cero
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

| # | 📌 Ejercicio | 📖 Tema | ⏱️ Duración | 🎓 Nivel |
|---|-----------|------|----------|---------|
| 1 | **E00** | Chat básico con PromptTemplate | 20 min | 🟢 Básico |
| 2 | **E01** | LCEL y cadenas en LangChain | 20 min | 🟢 Básico |
| 3 | **E02** | Chat con memoria en LangChain | 25 min | 🟠 Intermedio |
| 4 | **E03** | Tools con LangChain y API | 25 min | 🟠 Intermedio |
| 5 | **E04** | RAG básico con LangChain | 30 min | 🟠 Intermedio |
| 6 | **E05** | RAG con memoria | 35 min | 🟠 Intermedio |
| 7 | **E06** | De manual a LangChain | 25 min | 🟠 Intermedio |
| 8 | **E07** | PromptTemplate avanzado | 20 min | 🟠 Intermedio |
| 9 | **E08** | LCEL Chain avanzado | 25 min | 🟠 Intermedio |
| 10 | **E09** | RAG mini | 20 min | 🟢 Básico |
| 11 | **E10** | LLM Wrapper | 20 min | 🟠 Intermedio |
| 12 | **E11** | Output Parser | 20 min | 🟠 Intermedio |
| 13 | **E12** | Embeddings | 25 min | 🟠 Intermedio |
| 14 | **E13** | FAISS | 30 min | 🟠 Intermedio |
| 15 | **E14** | Retriever | 25 min | 🟠 Intermedio |
| 16 | **E15** | Refactor code | 30 min | 🟠 Intermedio |
| 17 | **E16** | RAG desde cero | 45 min | 🔴 Avanzado |

### E00 - Chat Básico con PromptTemplate

**Carpeta**: `M3L2/E00_chat_basico_prompt_template`

**Objetivo**: Primer encuentro con LangChain. Construye un chat simple usando PromptTemplate.

**Qué aprenderás**:
- LangChain basics
- PromptTemplate
- LLM calls
- Simple conversation flow

**Notebooks**: 
- [M3L2_E00_Starter.ipynb](M3L2/E00_chat_basico_prompt_template/M3L2_E00_Starter.ipynb)
- [M3L2_E00_Resolution.ipynb](M3L2/E00_chat_basico_prompt_template/M3L2_E00_Resolution.ipynb)

---

### E01 - LCEL y Cadenas en LangChain

**Carpeta**: `M3L2/E01_lcel_cadenas_langchain`

**Objetivo**: Aprende LCEL (LangChain Expression Language) para componer cadenas.

**Qué aprenderás**:
- LCEL syntax
- Pipe operator (|)
- Chain composition
- Runnable interfaces

**Notebooks**: 
- [M3L2_E01_Starter.ipynb](M3L2/E01_lcel_cadenas_langchain/M3L2_E01_Starter.ipynb)
- [M3L2_E01_Resolution.ipynb](M3L2/E01_lcel_cadenas_langchain/M3L2_E01_Resolution.ipynb)

---

### E02 - Chat con Memoria en LangChain

**Carpeta**: `M3L2/E02_chat_con_memoria_langchain`

**Objetivo**: Implementa un chat que recuerda la conversación.

**Qué aprenderás**:
- Memory types
- ConversationBufferMemory
- Message history
- Context management

**Notebooks**: 
- [M3L2_E02_Starter.ipynb](M3L2/E02_chat_con_memoria_langchain/M3L2_E02_Starter.ipynb)
- [M3L2_E02_Resolution.ipynb](M3L2/E02_chat_con_memoria_langchain/M3L2_E02_Resolution.ipynb)

---

### E03 - Tools con LangChain y API

**Carpeta**: `M3L2/E03_tools_langchain_api_dolar`

**Objetivo**: Integra tools externas (APIs) con LangChain.

**Qué aprenderás**:
- Tool definition en LangChain
- API integration
- Function calling
- Tool validation

**Notebooks**: 
- [M3L2_E03_Starter.ipynb](M3L2/E03_tools_langchain_api_dolar/M3L2_E03_Starter.ipynb)
- [M3L2_E03_Resolution.ipynb](M3L2/E03_tools_langchain_api_dolar/M3L2_E03_Resolution.ipynb)

---

### E04 - RAG Básico con LangChain

**Carpeta**: `M3L2/E04_rag_basico_langchain`

**Objetivo**: Implementa tu primer RAG (Retrieval-Augmented Generation).

**Qué aprenderás**:
- Vector stores
- Document loaders
- Retrievers
- RAG pipeline básico

**Notebooks**: 
- [M3L2_E04_Starter.ipynb](M3L2/E04_rag_basico_langchain/M3L2_E04_Starter.ipynb)
- [M3L2_E04_Resolution.ipynb](M3L2/E04_rag_basico_langchain/M3L2_E04_Resolution.ipynb)

---

### E05 - RAG con Memoria

**Carpeta**: `M3L2/E05_rag_chat_con_memoria`

**Objetivo**: Combina RAG con memoria para conversaciones contextuales.

**Qué aprenderás**:
- RAG + memory
- Context preservation
- History management
- Multi-turn RAG

**Notebooks**: 
- [M3L2_E05_Starter.ipynb](M3L2/E05_rag_chat_con_memoria/M3L2_E05_Starter.ipynb)
- [M3L2_E05_Resolution.ipynb](M3L2/E05_rag_chat_con_memoria/M3L2_E05_Resolution.ipynb)

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

### E07 - PromptTemplate Avanzado

**Carpeta**: `M3L2/E07_prompt_template`

**Objetivo**: Técnicas avanzadas de PromptTemplate.

**Qué aprenderás**:
- Variables dinámicas
- Few-shot examples
- Template formatting
- Prompt engineering

**Notebooks**: 
- [M3L2_E07_Starter.ipynb](M3L2/E07_prompt_template/M3L2_E07_Starter.ipynb)
- [M3L2_E07_Resolution.ipynb](M3L2/E07_prompt_template/M3L2_E07_Resolution.ipynb)

---

### E08 - LCEL Chain Avanzado

**Carpeta**: `M3L2/E08_lcel_chain`

**Objetivo**: Cadenas complejas con LCEL.

**Qué aprenderás**:
- Advanced LCEL patterns
- Branching and routing
- Conditional chains
- Parallel processing

**Notebooks**: 
- [M3L2_E08_Starter.ipynb](M3L2/E08_lcel_chain/M3L2_E08_Starter.ipynb)
- [M3L2_E08_Resolution.ipynb](M3L2/E08_lcel_chain/M3L2_E08_Resolution.ipynb)

---

### E09 - RAG Mini

**Carpeta**: `M3L2/E09_rag_mini`

**Objetivo**: RAG minimalista y eficiente.

**Qué aprenderás**:
- Minimalist RAG design
- Essential components only
- Performance optimization
- Simple but effective

**Notebooks**: 
- [M3L2_E09_Starter.ipynb](M3L2/E09_rag_mini/M3L2_E09_Starter.ipynb)
- [M3L2_E09_Resolution.ipynb](M3L2/E09_rag_mini/M3L2_E09_Resolution.ipynb)

---

### E10 - LLM Wrapper

**Carpeta**: `M3L2/E10_llm_wrapper`

**Objetivo**: Envuelve un modelo como una herramienta reutilizable.

**Qué aprenderás**:
- LangChain LLM interface
- Custom wrappers
- Model abstraction
- Reusable components

**Notebooks**: 
- [M3L2_E10_Starter.ipynb](M3L2/E10_llm_wrapper/M3L2_E10_Starter.ipynb)
- [M3L2_E10_Resolution.ipynb](M3L2/E10_llm_wrapper/M3L2_E10_Resolution.ipynb)

---

### E11 - Output Parser

**Carpeta**: `M3L2/E11_output_parser`

**Objetivo**: Parsea y estructura outputs del LLM.

**Qué aprenderás**:
- Output parsing
- JSON structuring
- Error recovery
- Custom parsers

**Notebooks**: 
- [M3L2_E11_Starter.ipynb](M3L2/E11_output_parser/M3L2_E11_Starter.ipynb)
- [M3L2_E11_Resolution.ipynb](M3L2/E11_output_parser/M3L2_E11_Resolution.ipynb)

---

### E12 - Embeddings

**Carpeta**: `M3L2/E12_embeddings`

**Objetivo**: Trabajar con embeddings para representación semántica.

**Qué aprenderás**:
- Embedding models
- Vector representation
- Similarity search
- Embedding basics for RAG

**Notebooks**: 
- [M3L2_E12_Starter.ipynb](M3L2/E12_embeddings/M3L2_E12_Starter.ipynb)
- [M3L2_E12_Resolution.ipynb](M3L2/E12_embeddings/M3L2_E12_Resolution.ipynb)

---

### E13 - FAISS

**Carpeta**: `M3L2/E13_faiss`

**Objetivo**: Vector store con FAISS para búsqueda eficiente.

**Qué aprenderás**:
- FAISS library
- Index creation
- Similarity search at scale
- Vector DB basics

**Notebooks**: 
- [M3L2_E13_Starter.ipynb](M3L2/E13_faiss/M3L2_E13_Starter.ipynb)
- [M3L2_E13_Resolution.ipynb](M3L2/E13_faiss/M3L2_E13_Resolution.ipynb)

---

### E14 - Retriever

**Carpeta**: `M3L2/E14_retriever`

**Objetivo**: Implementa retrievers personalizados.

**Qué aprenderás**:
- Retriever interface
- Custom retrieval logic
- Multi-source retrieval
- Retriever evaluation

**Notebooks**: 
- [M3L2_E14_Starter.ipynb](M3L2/E14_retriever/M3L2_E14_Starter.ipynb)
- [M3L2_E14_Resolution.ipynb](M3L2/E14_retriever/M3L2_E14_Resolution.ipynb)

---

### E15 - Refactor Code

**Carpeta**: `M3L2/E15_refactor_chaos`

**Objetivo**: Refactoriza código desordenado a una estructura limpia.

**Qué aprenderás**:
- Code organization
- Best practices
- Modularity
- Maintainability

**Notebooks**: 
- [M3L2_E15_Starter.ipynb](M3L2/E15_refactor_chaos/M3L2_E15_Starter.ipynb)
- [M3L2_E15_Resolution.ipynb](M3L2/E15_refactor_chaos/M3L2_E15_Resolution.ipynb)

---

### E16 - RAG desde Cero

**Carpeta**: `M3L2/E16_rag_desde_cero`

**Objetivo**: Construye un RAG completo desde cero integrando todo lo aprendido.

**Qué aprenderás**:
- End-to-end RAG system
- Document processing
- Retrieval + generation
- Production considerations

**Notebooks**: 
- [M3L2_E16_Starter.ipynb](M3L2/E16_rag_desde_cero/M3L2_E16_Starter.ipynb)
- [M3L2_E16_Resolution.ipynb](M3L2/E16_rag_desde_cero/M3L2_E16_Resolution.ipynb)

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
│  E00: Chat Basic        E07: Prompt      E04: RAG Basic         │
│  E01: LCEL             E08: LCEL         E05: RAG Memory       │
│  E02: Memory           E06: Refactor     E09: RAG Mini         │
│                                          E16: RAG Full         │
│                                                                 │
│       ▼─────────────────▼─────────────────▼                    │
│                                                                 │
│  COMPONENTES AVANZADOS                                         │
│  ────────────────────────                                      │
│  E10: LLM Wrapper  E12: Embeddings   E14: Retriever           │
│  E11: Output Parser E13: FAISS       E15: Refactor            │
│  E03: Tools API                                                │
│                                                                 │
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

---

## 💡 Tips para Maximizar el Aprendizaje

1. **Sigue el orden sugerido**: Cada ejercicio se basa en conceptos previos
2. **Lee el Starter primero**: No saltes directo a Resolution
3. **Intenta resolver sin copiar**: El error es parte del aprendizaje
4. **Experimenta después**: Modifica y juega con los notebooks
5. **Compara soluciones**: Entiende por qué Resolution es diferente
6. **Toma notas**: Escribe lo que aprendes en cada sección

---

## 🆘 Troubleshooting

### En Colab
- Algunos paquetes se instalan automáticamente
- Si algo falla, ejecuta: `!pip install --upgrade langchain openai faiss-cpu`

### Errores comunes
- **ImportError**: Instala el paquete faltante
- **API keys**: Usa `getpass` para inputs seguros
- **Timeout en API**: Intenta de nuevo, algunos endpoints pueden estar lentos

---

## 📧 Contacto & Feedback

¿Encontraste un bug? ¿Sugerencias de mejora?

📬 Reporta en el repositorio o contacta al instructor.

---

## 📊 Estadísticas del Módulo

| Métrica | Valor |
|---------|-------|
| **Ejercicios Totales** | 25 |
| **Notebooks** | 50 (25 Starter + 25 Resolution) |
| **Tiempo Total Estimado** | ~18-20 horas |
| **Tópicos Cubiertos** | 20+ |
| **Líneas de Código** | 5,000+ |

---

## 🙋 ¿Necesitas Ayuda?

```
📖 Documentación: Revisa el README de cada ejercicio
💬 Discusiones: Abre un issue con tu pregunta
🐛 Bugs: Reporta en el repositorio
💡 Mejoras: Sugerencias siempre bienvenidas
```

---

## 📄 Licencia

Este proyecto está bajo licencia **MIT**. Úsalo libremente para aprender y enseñar.

---

<div align="center">

### 🌟 ¡Happy Learning! 🌟

Construye agentes inteligentes y sistemas RAG increíbles.

**Made with ❤️ for AI Engineers**

</div>

---

**Last Updated**: 2026-06-04  
**Version**: 1.0  
**Status**: ✅ Completo
