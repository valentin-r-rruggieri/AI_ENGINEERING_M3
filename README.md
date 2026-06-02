# M3L1 Extras - AI Agents, Tools y ReAct

Esta carpeta contiene notebooks extra para practicar los conceptos centrales de agentes de IA en el módulo 3. Cada ejercicio es autocontenido: se puede abrir y resolver de forma independiente, sin depender de haber completado otro notebook.

Los ejercicios están pensados para trabajar en Jupyter Notebook o Google Colab.

## Estructura general

Cada carpeta de ejercicio contiene dos notebooks:

- `*_Starter.ipynb`: versión para alumnos, con explicaciones, teoría breve, TODOs y checks.
- `*_Resolution.ipynb`: versión resuelta, para comparar al final después de intentar resolver el Starter.

La dinámica recomendada es:

1. Abrir el notebook `Starter`.
2. Leer el objetivo y el diagrama inicial.
3. Ejecutar las celdas en orden.
4. Completar los TODOs.
5. Revisar los prints/checks.
6. Comparar con `Resolution` solo al final.

## Requisitos

Para la mayoría de los notebooks alcanza con Python estándar.

Requisitos opcionales:

- `E00` necesita conexión a internet para consultar DolarAPI.
- `E11` y `E12` incluyen una parte opcional con OpenAI API real.
- Para usar OpenAI, se carga la API key desde el notebook con `getpass`, sin guardarla en el archivo.

En Colab, si falta el paquete `openai`, los notebooks `E11` y `E12` intentan instalarlo automáticamente. Si no funciona, ejecutar:

```python
!pip install -U openai
```

## Orden sugerido

| Orden | Ejercicio | Tema principal | Duración sugerida |
|---|---|---|---|
| 1 | `E00_pipeline_vs_react_dolar` | Pipeline vs agente con una API real simple | 20 min |
| 2 | `E01_tool_contracts` | Contratos de tools | 20 min |
| 3 | `E02_react_loop` | Loop ReAct mínimo | 20 min |
| 4 | `E03_react_clima_calculo` | ReAct con dos tools encadenadas | 20 min |
| 5 | `E10_sales_pipeline_vs_agent` | Pipeline vs agente en reporte de ventas | 20-25 min |
| 6 | `E11_sales_tool_use` | Tool use, seguridad y descripción de tools | 25-35 min |
| 7 | `E12_sales_react_loop` | Trace ReAct y tool calling | 30-40 min |
| 8 | `E13_sales_custom_tools_robust` | Custom tools robustas y errores estructurados | 25-30 min |

## Qué contiene cada ejercicio

### E00 - Pipeline vs agente con DolarAPI

Carpeta:

`E00_pipeline_vs_react_dolar`

Notebooks:

- [M3L1_E00_Starter.ipynb](E00_pipeline_vs_react_dolar/M3L1_E00_Starter.ipynb)
- [M3L1_E00_Resolution.ipynb](E00_pipeline_vs_react_dolar/M3L1_E00_Resolution.ipynb)

Objetivo:

Comparar una respuesta tipo pipeline, que responde sin consultar datos actuales, contra un agente ReAct mínimo que consulta DolarAPI antes de responder.

Qué se practica:

- Diferencia entre pipeline y agente.
- Uso de una tool externa.
- Normalización del payload de una API.
- Observación antes de responder.
- Respuesta grounded en datos reales.

Entregable esperado:

Un agente que consulta el valor del dólar blue, calcula cuántos pesos representan 100 USD y devuelve una respuesta basada en la cotización observada.

### E01 - Tool contracts

Carpeta:

`E01_tool_contracts`

Notebooks:

- [M3L1_E01_Starter.ipynb](E01_tool_contracts/M3L1_E01_Starter.ipynb)
- [M3L1_E01_Resolution.ipynb](E01_tool_contracts/M3L1_E01_Resolution.ipynb)

Objetivo:

Entender que una tool debe tener un contrato claro: inputs definidos, validación mínima, output estable y una sola responsabilidad.

Qué se practica:

- Normalización de inputs.
- Validación antes de actuar.
- Salidas estructuradas.
- Manejo de casos inválidos.
- Separación entre búsqueda de datos y cálculo.

Entregable esperado:

Tools que reciben un período de ventas, lo normalizan, buscan datos y calculan revenue manteniendo un formato de salida consistente.

### E02 - ReAct loop mínimo

Carpeta:

`E02_react_loop`

Notebooks:

- [M3L1_E02_Starter.ipynb](E02_react_loop/M3L1_E02_Starter.ipynb)
- [M3L1_E02_Resolution.ipynb](E02_react_loop/M3L1_E02_Resolution.ipynb)

Objetivo:

Implementar la mecánica base de un agente ReAct sin depender de una API externa ni de un modelo real.

Qué se practica:

- Estado del agente.
- Selección de la próxima acción.
- Ejecución de tools por nombre.
- Actualización del estado con observaciones.
- Condición de parada.

Entregable esperado:

Un loop que decide qué tool ejecutar según el estado actual y finaliza cuando ya tiene la información necesaria.

### E03 - ReAct con clima y cálculo

Carpeta:

`E03_react_clima_calculo`

Notebooks:

- [M3L1_E03_Starter.ipynb](E03_react_clima_calculo/M3L1_E03_Starter.ipynb)
- [M3L1_E03_Resolution.ipynb](E03_react_clima_calculo/M3L1_E03_Resolution.ipynb)

Objetivo:

Practicar un flujo ReAct donde una tool produce una observación y esa observación alimenta una segunda tool.

Qué se practica:

- Thought, Action, Observation y Final Answer.
- Encadenamiento de tools.
- Manejo de fallo de tool.
- Trace visible por consola.
- Respuesta final basada en observaciones.

Entregable esperado:

Un agente que consulta la temperatura mockeada de una ciudad, multiplica ese valor por 5 y responde sin inventar datos si la ciudad no existe.

### E10 - Reporte de ventas: pipeline vs agente

Carpeta:

`E10_sales_pipeline_vs_agent`

Notebooks:

- [M3L1_E10_Starter.ipynb](E10_sales_pipeline_vs_agent/M3L1_E10_Starter.ipynb)
- [M3L1_E10_Resolution.ipynb](E10_sales_pipeline_vs_agent/M3L1_E10_Resolution.ipynb)

Objetivo:

Comparar el mismo pedido de negocio resuelto por un pipeline hardcodeado y por un flujo tipo agente con tools mockeadas.

Qué se practica:

- Diferencia entre respuesta plausible y respuesta basada en datos.
- Búsqueda de datos mockeados.
- Cálculo determinístico.
- Decisión sobre cuándo conviene usar agente y cuándo no.

Entregable esperado:

Un agente simple que busca filas de ventas, calcula el ingreso total y genera un reporte semanal breve.

### E11 - Tool use y descripciones

Carpeta:

`E11_sales_tool_use`

Notebooks:

- [M3L1_E11_Starter.ipynb](E11_sales_tool_use/M3L1_E11_Starter.ipynb)
- [M3L1_E11_Resolution.ipynb](E11_sales_tool_use/M3L1_E11_Resolution.ipynb)

Objetivo:

Construir tools seguras y entender cómo la descripción de una herramienta afecta la decisión del modelo.

Qué se practica:

- Riesgo de usar `eval()`.
- Implementación de una calculadora segura.
- Tool local de ventas.
- Schema de tools para OpenAI.
- Diferencia entre función Python real y descripción enviada al modelo.
- Comparación entre descripción vaga y descripción precisa.

Entregable esperado:

Una calculadora segura y una tool de ventas con schema claro para que un modelo pueda decidir cuándo usarla.

Nota:

La parte con OpenAI es opcional. Si no hay API key, el notebook sigue siendo útil hasta la parte local y de schemas.

### E12 - ReAct paso a paso con tool calling

Carpeta:

`E12_sales_react_loop`

Notebooks:

- [M3L1_E12_Starter.ipynb](E12_sales_react_loop/M3L1_E12_Starter.ipynb)
- [M3L1_E12_Resolution.ipynb](E12_sales_react_loop/M3L1_E12_Resolution.ipynb)

Objetivo:

Hacer visible un trace ReAct completo y conectar ese patrón con tool calling.

Qué se practica:

- Tools locales de ventas.
- Registro de herramientas.
- Trace determinístico.
- Completar observaciones faltantes.
- Schemas de tools para OpenAI.
- Límite de pasos con `pasos_maximos`.

Entregable esperado:

Un flujo ReAct que busca datos, calcula total, resume tendencias y devuelve una respuesta final basada en observaciones.

Nota:

La parte con OpenAI es opcional. El núcleo del ejercicio se puede resolver sin API key.

### E13 - Custom tools robustas

Carpeta:

`E13_sales_custom_tools_robust`

Notebooks:

- [M3L1_E13_Starter.ipynb](E13_sales_custom_tools_robust/M3L1_E13_Starter.ipynb)
- [M3L1_E13_Resolution.ipynb](E13_sales_custom_tools_robust/M3L1_E13_Resolution.ipynb)

Objetivo:

Pasar de tools frágiles a tools más cercanas a producción, con validaciones y errores estructurados.

Qué se practica:

- Casos rotos intencionales.
- Validación defensiva.
- Errores interpretables por el agente.
- Outputs estructurados.
- Diseño de una custom tool propia.
- Checklist de seguridad.

Entregable esperado:

Tools que devuelven `exito`, `datos` y `codigo_error`, más el diseño de una custom tool de un dominio elegido por el alumno.

## Cómo subir o usar en GitHub

Los notebooks ya incluyen las imágenes como attachments embebidos. Esto significa que las imágenes viajan dentro del `.ipynb` y no dependen de una URL externa.

Para publicar esta carpeta en GitHub:

1. Subir la carpeta `extras/M3L1`.
2. Mantener cada `Starter` junto a su `Resolution`.
3. No separar los notebooks de sus carpetas.
4. Revisar que GitHub renderice los notebooks; si no, abrirlos en Colab o Jupyter.

## Cómo usar en Google Colab

Opción simple:

1. Abrir el notebook desde GitHub.
2. Elegir `Open in Colab`.
3. Ejecutar las celdas en orden.

Para `E11` y `E12`, si se quiere usar OpenAI:

1. Ejecutar la celda que pide la API key.
2. Pegar la key cuando Colab la solicite.
3. Continuar con la demo de tool calling.

## Recomendación para alumnos

No mirar `Resolution` antes de intentar el `Starter`.

La forma correcta de resolver estos ejercicios es:

1. Ejecutar una tool aislada.
2. Leer qué input espera.
3. Leer qué output devuelve.
4. Completar un TODO.
5. Ejecutar el check inmediato.
6. Recién al final comparar con la solución.
