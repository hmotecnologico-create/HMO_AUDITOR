# Estrategia de Validación Robusta: Integridad y Cumplimiento Normativo

Para dar fe de que la documentación generada es válida y cumple con las normativas (ISO, IFAC, leyes locales), el **HMO Auditor** implementará una capa de validación basada en tres pilares: **Integridad Técnica**, **Trazabilidad de la Inteligencia** y **Certificación de Origen**.

## 1. Integridad de Documentos y Procedimientos
Para cumplir con normativas de control documental (como ISO 9001:2015 cláusula 7.5), el sistema garantiza que los documentos no sean alterados posterior a su emisión.

- **Huella Digital (Hash SHA-256)**: Al momento de generar cualquier PDF, Word o Excel, el sistema calcula un "Hash" único basado en el contenido.
- **Metadatos de Inalterabilidad**: Este Hash se incrusta en las propiedades del archivo y se guarda en un "Log de Integridad" local. Si un auditor externo duda, el aplicativo puede recalcular el Hash y demostrar que el archivo es el original.
- **Marca de Tiempo Protegida**: Cada documento lleva una estampa de tiempo sincronizada con el reloj del sistema, impidiendo la alteración de fechas de auditoría.

## 2. Trazabilidad de la Inteligencia (Audit Trail)
¿Cómo sabemos que la IA no se equivocó? El sistema implementa una **Bitácora de Decisiones**:

- **ID de Fragmento Normativo**: Todo texto generado por la IA en un formato (ej: un hallazgo) llevará una referencia oculta al ID exacto del párrafo de la norma en el RAG.
- **Registro de Edición Humana**: El sistema registra: *"La IA sugirió X, el Auditor Humano (ID: 001) modificó a Y el día DD/MM/AAAA"*. Esta transparencia es vital para validaciones de entes externos.

## 3. Protocolo "Audit-on-Audit" (Segunda Opinión AI)
Antes de que el usuario vea un borrador, el sistema realiza una validación interna:
- **Agente Verificador**: Un segundo proceso independiente del LLM analiza si la respuesta generada contradice la norma recuperada por el RAG.
- **Compliance Score**: Cada formato incluye un "Índice de Coherencia Normativa" (0-100%). Si el índice es menor a 85%, el sistema marca el campo para revisión manual obligatoria.

## 4. Reporte de Cumplimiento (Certificate of Origin)
Al final de cada ciclo de auditoría, el aplicativo genera un documento adicional: el **Reporte de Validación de HMO Auditor**.
- Este reporte certifica:
    1. Que se usó la versión vigente de la norma (ISO 27001, etc.).
    2. Que el 100% de los documentos ingeridos pasaron por validación humana OCR/HITL.
    3. Que los archivos finales están protegidos estructuralmente.

---

### Ejemplo de Bloque de Validación en Formatos
Al final de cada documento (Word/Excel), se inserta un cuadro de control:
> **CONTROL DE INTEGRIDAD HMO**
> - **Generado por**: HMO Auditor v1.0
> - **Hash ID**: `5f3c...8a12`
> - **Validación Humana**: REVISADO Y APROBADO (ID: Steiner-001)
> - **Estatus Normativo**: 100% Coherente con ISO 9001:2015
