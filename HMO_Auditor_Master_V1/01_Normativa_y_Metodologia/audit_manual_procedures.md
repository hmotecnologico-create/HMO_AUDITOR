# Manual de Auditoría y Procedimientos Técnicos (HMO Auditor)

Este manual define el marco normativo y los procedimientos operativos que el aplicativo y el auditor deben seguir para garantizar la integridad de las certificaciones.

## 1. Manual de Auditoría (MAN-AUD-001)

### 1.1. Propósito
Establecer las directrices para la planificación, ejecución y reporte de auditorías internas asistidas por inteligencia artificial local, asegurando el cumplimiento de los requisitos de ISO 19011.

### 1.2. Responsabilidades
- **Auditor Líder**: Responsable de la carga de contexto corporativo y la validación final de los formatos auto-diligenciados.
- **Sistema HMO Auditor**: Responsable de la recuperación exacta de normas (RAG) y la propuesta técnica de hallazgos.

### 1.3. Marco Ético de la IA
El uso de Ollama en este proceso se rige por el principio de **"Humano en el Bucle" (Human-in-the-loop)**. Ningún documento se considera oficial sin la firma y validación manual del auditor.

---

## 2. Procedimientos de Auditoría (PROC-AUD-001)

### 2.1. Procedimiento de Ingesta y Validación (OCR + HITL)
1. **Recolección**: Identificar documentos vigentes (Misión, Visión, Políticas, etc.).
2. **Carga y Digitalización**: Subir archivos al módulo de "Contexto Empresa". El sistema aplicará **OCR Local** de forma automática.
3. **Validación Visual (Obligatoria)**: El auditor deberá comparar el texto digitalizado con la imagen original en la interfaz del aplicativo.
4. **Autorización**: El humano debe "Autorizar" que el aplicativo reconoció correctamente el contenido. Si hay errores, el auditor puede corregir el texto antes de la indexación.
5. **Indexación**: Solo tras la autorización humana, el sistema fragmenta y almacena la información en la base de datos RAG.

### 2.2. Procedimiento de Generación de Formatos
1. **Selección de Norma**: Elegir la norma específica (ej: ISO 9001) cargada en el RAG.
2. **Mapeo de Procesos**: Vincular el proceso de la empresa con los capítulos de la norma.
3. **Draft AI**: El sistema generará borradores de Programa y Checklist.
4. **Validación**: El auditor debe revisar que las sugerencias de la IA no contradigan la realidad operativa de la empresa.

### 2.3. Procedimiento de Blindaje Documental
1. Tras la aprobación, el sistema aplicará:
    - **Cifrado de Estructura**: Solo celdas de formulario permitidas.
    - **Firma Electrónica**: Estampado de fecha, hora y ID del auditor validado.

---

## 3. Guía de Formatos Oficiales

| Código | Formato | Uso Crítico |
| :--- | :--- | :--- |
| **GAD-PROG-01** | Programa de Auditoría | Demuestra planificación anual y estrategia. |
| **GAD-LIST-02** | Lista de Verificación | Evidencia la exhaustividad de la revisión. |
| **GAD-PAPT-03** | Papeles de Trabajo | Soporte documental de las pruebas realizadas. |
| **GAD-HALL-04** | Formato de Hallazgos | Documenta No Conformidades y Oportunidades de Mejora. |
| **GAD-CERT-05** | Acta de Cierre | Valida la conclusión de la auditoría frente a terceros. |

---

## 4. Control de Cambios y Versiones
Para auditorías externas, el sistema mantiene un log oculto (audit trail) que registra:
- Fecha de generación del formato.
- Fragmentos normativos utilizados.
- Ediciones manuales realizadas después de la sugerencia de la IA.
