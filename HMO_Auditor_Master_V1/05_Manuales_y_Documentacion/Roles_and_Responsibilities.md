# Roles y Responsabilidades: Sistema HMO Auditor

Para que el proceso de auditoría sea exitoso y cumpla con la **ISO 19011**, es necesario definir claramente quiénes interactúan con el sistema y cuáles son sus facultades.

## 1. Perfiles del Sistema

| Rol | Responsabilidad Principal | Facultades en el Aplicativo |
| :--- | :--- | :--- |
| **Director de Calidad / Líder de Auditoría** | Supervisar la integridad del programa de auditoría y aprobar los reportes finales. | Selección de norma, aprobación final de hallazgos, emisión de certificados de integridad. |
| **Auditor Interno / Auxiliar** | Ejecutar la ingesta de documentos, validar el OCR y recolectar evidencias. | Carga de archivos, validación HITL, diligenciamiento de checklists, edición de borradores. |
| **Administrador del Sistema (TI)** | Garantizar la operatividad local del aplicativo y el motor Ollama. | Configuración de modelos LLM, gestión de copias de seguridad de la base de datos RAG, mantenimiento de hardware. |
| **Auditado (Personal Involucrado)** | Proveer los documentos y evidencias solicitadas por el auditor. | Entrega de archivos para ingesta (fase previa al aplicativo). |

## 2. Matriz RACI del Proceso HMO

| Actividad | Director de Calidad | Auditor Auxiliar | Administrador TI |
| :--- | :---: | :---: | :---: |
| Configuración de Ollama/RAG | I | I | **A/R** |
| Ingesta de Documentos (OCR) | I | **A/R** | C |
| Validación de Texto Extraído | C | **A/R** | I |
| Generación de Programa de Auditoría | **A/R** | C | I |
| Ejecución de Checklist (Hallazgos) | C | **A/R** | I |
| Aprobación de Reporte Final | **A/R** | C | I |
| Verificación de Integridad (SHA-256) | **A** | **R** | C |

*Leyenda: **R**: Responsable (Ejecuta), **A**: Aprobador (Rinde cuentas), **C**: Consultado, **I**: Informado.*

## 3. Justificación de Roles según ISO 19011
La norma exige que el equipo auditor sea competente y que las responsabilidades estén asignadas para evitar conflictos de interés. El aplicativo HMO Auditor separa las funciones de ejecución (Auxiliar) de las de aprobación (Director), garantizando la transparencia del proceso ante entes externos.
