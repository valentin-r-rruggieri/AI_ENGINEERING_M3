# Extras M3L1 - AI Agents

Estos notebooks son practicas autocontenidas para trabajar agentes, herramientas y trazabilidad.

## Organizaci?n sugerida

Usar estos cuatro notebooks como secuencia principal:

| Orden | Tema | Starter | Resolution |
|---|---|---|---|
| 1 | Pipeline vs AI Agent | `M3L1/E10_sales_pipeline_vs_agent/M3L1_E10_Starter.ipynb` | `M3L1/E10_sales_pipeline_vs_agent/M3L1_E10_Resolution.ipynb` |
| 2 | Tool Use y descripcion de tools | `M3L1/E11_sales_tool_use/M3L1_E11_Starter.ipynb` | `M3L1/E11_sales_tool_use/M3L1_E11_Resolution.ipynb` |
| 3 | ReAct loop | `M3L1/E12_sales_react_loop/M3L1_E12_Starter.ipynb` | `M3L1/E12_sales_react_loop/M3L1_E12_Resolution.ipynb` |
| 4 | Custom tools robustas | `M3L1/E13_sales_custom_tools_robust/M3L1_E13_Starter.ipynb` | `M3L1/E13_sales_custom_tools_robust/M3L1_E13_Resolution.ipynb` |

Todos mantienen el mismo escenario: automatizar un reporte semanal de ventas.

## Demo opcional

El notebook `M3L1/E00_pipeline_vs_react_dolar` queda como demo adicional para
mostrar una tool que consulta DolarAPI real. No es la ruta principal para clase.

## OpenAI API

Algunos notebooks tienen secciones opcionales con OpenAI API real
(`gpt-4o-mini`). Para ejecutarlas:

```python
import os
os.environ["OPENAI_API_KEY"] = "..."
```

Si no hay API key, esas celdas imprimen una indicacion y no bloquean el resto
del notebook.
