# Matriz de Justificación Normativa y Técnica: HMO Auditor

Este documento justifica la existencia de cada formato y procedimiento del aplicativo **HMO Auditor**, vinculándolos directamente con las normas internacionales para asegurar que el sistema no trabaje bajo subjetividades.

## 1. Justificación de Formatos de Auditoría

| Código de Formato | Nombre del Documento | Referencia Normativa (ISO) | Vínculo con el Negocio | Justificación Técnica / Metodológica |
| :--- | :--- | :--- | :--- | :--- |
| **GAD-PROG-01** | Programa de Auditoría | **ISO 19011:2018 Cláusula 5.2** | Planificación Estratégica | Define el calendario y objetivos. Sin esto, la auditoría carece de alcance legal. |
| **GAD-LIST-02** | Lista de Verificación | **ISO 19011:2018 Cláusula 6.3.4** | Operación y Control | Guía al auditor para recolectar evidencia objetiva. Asegura que no se olviden requisitos de la norma. |
| **REPORT-VAL-03**| Certificado de Integridad | **ISO 9001:2015 Cláusula 7.5.3** | Seguridad de la Información | Garantiza la inalterabilidad de los documentos digitales mediante Hash SHA-256. |
| **MAN-AUD-001** | Manual de Procedimientos | **ISO 19011:2018 Cláusula 6.1** | Gobernanza Corporativa | Describe el "Cómo" se realiza la auditoría asistida por IA para estandarizar el proceso. |

## 2. Justificación de Procesos de Ingesta Inteligente

### A. Digitalización OCR y Validación Humana (HITL)
- **Justificación Normativa**: ISO 9001:2015 Cláusula 7.5.1 (Control de Información Documentada).
- **Razón Técnica**: La IA puede cometer errores en la lectura de imágenes. La validación humana y la capacidad de **Entrada Manual de Datos Omitidos** garantizan que la base de conocimientos (RAG) sea 100% verídica.

### B. Trazabilidad de Decisiones (Audit Trail)
- **Justificación Normativa**: ISO 19011:2018 Cláusula 4 (Principios de Auditoría - Basado en la Evidencia).
- **Razón Técnica**: Permite rastrear qué fragmento de la norma se aplicó a cada hallazgo, permitiendo defensas sólidas ante auditores externos.

## 3. Justificación de la Arquitectura RAG Local
- **Justificación Normativa**: ISO 27001:2022 (Seguridad de la Información).
- **Razón Técnica**: Al no usar internet (API externas), se protege la misión de la empresa y su secreto industrial, cumpliendo con la confidencialidad exigida a los auditores.

---

Este ecosistema asegura que **HMO Auditor** sea un sistema de grado industrial, diseñado para superar auditorías de certificación de alto nivel.
