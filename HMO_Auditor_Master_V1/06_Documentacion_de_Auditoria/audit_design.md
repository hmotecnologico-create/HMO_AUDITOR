# Diseño de Formatos y Metodología de Auditoría (HMO Auditor)

Este documento define la estructura de contenido de los formatos y el flujo de trabajo sugerido para asegurar el cumplimiento en auditorías externas.

## 1. Metodología de Auditoría: "Local Compliance Flow"

La metodología propuesta se basa en el estándar **ISO 19011:2018** y se divide en 4 fases críticas:

| Fase | Actividad | Herramienta AI/RAG |
| :--- | :--- | :--- |
| **Inicio** | Definición de alcance y criterios. | Selección de Normas en la base RAG. |
| **Preparación** | Creación de Programa y Checklist. | El LLM genera preguntas basadas en los fragmentos de la norma. |
| **Ejecución** | Recolección de evidencias y Papeles de Trabajo. | Comparación en tiempo real de evidencia vs. requisito normativo. |
| **Informe** | Reporte de Hallazgos y Cierre. | Redacción automatizada de hallazgos usando lenguaje técnico contable/auditor. |

---

## 2. Diseño de Formatos Oficiales

Todos los formatos seguirán una estructura de **"Formulario Protegido"**:
- **Cabecera**: Datos fijos (Logo, Nombre de Empresa, Fecha, Auditor).
- **Cuerpo**: Sección de solo lectura (Requisitos normativos recuperados por AI).
- **Campos de Entrada**: Únicos espacios editables para el auditor.

### A. Programa de Auditoría (Audit Program)
*Nombre Técnico: GAD-PROG-01*
- **Objetivo**: Calendario anual/semestral de auditorías.
- **Campos Editables**: Fecha programada, Auditor asignado, Recursos necesarios.
- **Estructura AI**: El LLM sugiere la frecuencia basada en el riesgo del área auditada.

### B. Lista de Verificación / Checklist de Auditoría
*Nombre Técnico: GAD-LIST-02*
- **Estructura AI**:
    - **Columna 1**: Requisito de la Norma (Solo lectura, insertado por RAG).
    - **Columna 2**: Pregunta de Auditoría (Generada por LLM).
    - **Columna 3**: Cumplimiento (Lista desplegable: C / NC / NA).
    - **Columna 4**: Hallazgos/Observaciones (Editable).

### C. Papeles de Trabajo de Auditoría (Audit Working Papers)
*Nombre Técnico: GAD-PAPT-03*
- **Propósito**: Documentar las pruebas realizadas (muestreo, entrevistas).
- **Campos Editables**: Muestra seleccionada, descripción de la prueba, referenciación cruzada con el checklist.
- **Especialización**: Incluye fórmulas en Excel para cálculos de materialidad o muestreo estadístico.

### D. Formato de Hallazgos (Findings Report)
*Nombre Técnico: GAD-HALL-04*
- **Estructura Crucial**:
    - **Criterio**: ¿Qué dice la norma? (RAG).
    - **Condición**: ¿Qué se encontró? (Auditor).
    - **Causa**: ¿Por qué ocurrió? (Análisis asistido por LLM).
    - **Consecuencia**: Riesgo asociado.
    - **Recomendación**: Acción sugerida.

---

## 3. Estrategia para Certificación Externa

Para que este aplicativo "sobrepase" auditorías externas, los formatos generados incluyen:
1. **Trazabilidad**: Cada campo de la norma tiene un "ID de Fragmento" que referencia la fuente original en la base de datos RAG local.
2. **Control de Cambios**: Registro de auditoría (logs) interno que demuestra que la estructura no fue alterada.
3. **Firmas Digitales/Mecánicas**: Espacios dedicados para validación de responsables.

---

## 4. Ejemplos de Nomenclatura Técnica
- **Manual de Auditoría**: `MAN-AUD-V1`
- **Procedimiento de Auditoría Interna**: `PROC-AUD-INT-001`
- **Guía de Formatos**: `GUI-FOR-01`
