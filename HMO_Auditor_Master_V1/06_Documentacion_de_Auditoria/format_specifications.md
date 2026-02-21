# Especificación Técnica de Formatos y Prompts AI

Este documento sirve como la "hoja de ruta" para los desarrolladores y el motor de generación AI, definiendo qué datos se extraen y cómo se presentan.

## 1. Mapeo de Campos por Formato

### A. Lista de Verificación (Checklist)
| Campo | Origen | Tipo de Dato | Protección |
| :--- | :--- | :--- | :--- |
| `ID_Requisito` | RAG (Norma) | String | Bloqueado |
| `Texto_Normativo` | RAG (Norma) | Text Area | Bloqueado |
| `Pregunta_Orientadora` | LLM (Ollama) | Text Area | Bloqueado |
| `Estado_Cumplimiento` | Auditor | Dropdown (C, NC, NA) | **Editable** |
| `Evidencia_Objetiva` | Auditor | Text Area | **Editable** |

### B. Programa de Auditoría (Audit Program)
| Campo | Origen | Tipo de Dato | Protección |
| :--- | :--- | :--- | :--- |
| `Ciclo_Auditoria` | Usuario | Integer (Año/Mes) | Bloqueado |
| `Proceso_Auditado` | Usuario | String | Bloqueado |
| `Objetivo_Auditoria` | LLM (Basado en Proceso) | Text | Bloqueado |
| `Fecha_Ejecucion` | Auditor | Date | **Editable** |
| `Auditor_Lider` | Usuario | String | **Editable** |

---

## 2. Ingeniería de Prompts (Ollama System Prompts)

Para asegurar que Ollama genere contenido consistente con las normas locales e internacionales, se deben usar los siguientes perfiles de prompt.

### Prompt de Generación de Checklist (Internal Audit Expert)
```text
System: Eres un Auditor Senior certificado en [NORMA_SELECCIONADA].
Contexto RAG: [FRAGMENTO_NORMA_RECUPERADO]
Tarea: Genera una lista de 3 preguntas de auditoría específicas y técnicas basadas estrictamente en el fragmento normativo proporcionado.
Restricciones:
1. No inventes requisitos adicionales.
2. Usa lenguaje formal y profesional.
3. Formato de salida: JSON con campos "id", "requisito", "preguntas".
```

### Prompt de Análisis de Hallazgos (Compliance Validator)
```text
System: Eres un experto en control interno (estilo IFAC).
Entrada: Hallazgo del auditor: "[DESCRIPCION_HALLAZGO]"
Norma: "[REFERENCIA_NORMA]"
Tarea: Genera el análisis de Causa Raíz y recomienda una Acción Correctiva.
Formato:
- Causa: Analiza por qué falló el control.
- Riesgo: Impacto potencial en la certificación.
- Recomendación: Acción inmediata.
```

---

## 3. Lógica de Protección de Documentos (Python Pseudocode)

Para implementar el requerimiento de "estructura no editable", el aplicativo seguirá esta lógica:

```python
def generate_protected_word(data):
    doc = Document()
    # Sección Bloqueada
    section = doc.add_section()
    doc.add_heading('Lista de Verificación de Auditoría', 0)
    
    for item in data['requisitos']:
        table = doc.add_table(rows=1, cols=2)
        # Celda de solo lectura (Criterio Normativo)
        table.cell(0, 0).text = item['norma']
        
        # Celda editable (Hallazgo del Auditor)
        # Se inserta un Content Control de tipo Rich Text
        cell_editable = table.cell(0, 1)
        insert_content_control(cell_editable, "Escriba aquí la evidencia...")

    # Aplicar protección de contraseña al nivel de documento
    doc.protect(WD_PROTECT.READ_ONLY, password="HMO_AUDIT_SAFE")
```

---

## 4. Casos de Uso Prioritarios (Backlog de Implementación)

1. **Sprint 1**: ISO 9001:2015 (Sistemas de Gestión de Calidad).
2. **Sprint 2**: NIA (Normas Internacionales de Auditoría - IFAC).
3. **Sprint 3**: ISO 27001 (Seguridad de la Información).
4. **Sprint 4**: Formatos Personalizados (Carga de Normas Locales/Empresariales vía archivos localmente).
