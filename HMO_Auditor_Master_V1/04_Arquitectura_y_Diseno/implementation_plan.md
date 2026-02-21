# Plan de Implementación: HMO Auditor Local (RAG-Audit)

Este documento detalla la estrategia técnica para construir una aplicación de auditoría que opera 100% en local, utilizando Ollama para el procesamiento de lenguaje natural y una arquitectura RAG para el cumplimiento normativo.

## User Review Required

> [!IMPORTANT]
> El sistema requiere que el hardware tenga capacidad suficiente para ejecutar Ollama (mínimo 8GB RAM para modelos 7B).
> La protección de documentos PDF, Word y Excel impedirá cambios estructurales pero permitirá el llenado de campos específicos (formularios).
> 3. **Auto-Diligenciamiento Inteligente**: Cruce de información entre la norma y los documentos de la empresa para pre-llenar campos de texto.
> 4. **Flujo de Validación Humana**: Interfaz para que el usuario acepte, edite o rechace lo sugerido por la AI antes de la generación final del documento protegido.

## Arquitectura Técnica

### Componentes Core
1. **Interfaz de Usuario**: Aplicación Desktop (Electron/Vite) o Web Local (FastAPI + React). Incluye **Motor de Grafos para Visualización de Nodos** (ej: React Flow o D3.js).
2. **Motor LLM**: Ollama ejecutando Llama 3 o Mistral 7B.
3. **Motor RAG Híbrido**: 
   - **Knowledge Base A (Biblioteca Normativa Multi-Sistemas)**: 
       - **SGC**: ISO 9001 (Calidad).
       - **SGSI**: ISO 27001 (Seguridad).
       - **SGA**: ISO 14001 (Ambiental).
       - **Académico**: Normas institucionales, Decretos sectoriales (ej: Dec. 1330), Modelos de Acreditación.
       - **Carga de Normas**: El sistema permite inyectar cualquier PDF normativo para entrenar al RAG.
   - **Knowledge Base B (Contexto Organizacional)**: Almacena Misión, Visión, Organigrama, Políticas y procesos internos.
   - **Pipeline de Ingesta (OCR)**: Integración con `Tesseract OCR` o `PaddleOCR` (ejecución local) para digitalizar documentos escaneados o imágenes corporativas.
   - **Embeddings**: Sentence-Transformers ejecutado en local.
   - **Vector Store**: ChromaDB con colecciones separadas.
4. **Capa de Integridad y Validación**:
   - **Módulo de Trazabilidad**: Database SQL local (SQLite) para registrar cada interacción Humano-AI (Log de cambios).
   - **Módulo de Firmas Digitales/Hashing**: Generación de Checksums SHA-256 por cada documento emitido.
   - **Agente de Verificación Cruzada**: Una instancia secundaria de Ollama para el control de calidad (Compliance Scoring).

### Estrategia RAG e Ingesta Guiada
- **Digitalización (OCR)**: Conversión de imágenes/PDFs escaneados a texto estructurado operando localmente.
- **Flujo de Ingesta Secuencial**: El sistema no permite avanzar sin la validación previa del documento actual.
- **Cartas de Navegación Normativa**: Por cada documento solicitado, el sistema entrega una ficha técnica con:
    - Referencia ISO vinculada.
    - Justificación de la importancia para el negocio.
    - Requisitos de validez jurídica (Firmas, Fechas, Evidencias).
- **Validación Humana (HITL)**: 
    - **Reconocimiento**: El usuario confirma el texto extraído.
    - **Inclusión Manual**: Interfaz para añadir datos que la IA omitió por problemas de resolución.
- **Autorización Final**: Solo lo validado por el humano entra al motor RAG, garantizando que el "Cerebro" del aplicativo sea 100% veraz.

---

## Diseño de Salida Protegida

### PDF (Formularios AcroForms)
- **Tecnología**: `ReportLab` o `PyFPDF`.
- **Protección**: Uso de permisos estándar de PDF (Standard Security Handler) para deshabilitar edición de contenido y permitir solo "Form Filling".

### Word (.docx)
- **Tecnología**: `python-docx`.
- **Protección**: Inserción de *Content Controls* (SDTs) en áreas editables. Aplicación de `document protection` con tipo `wdAllowOnlyFormFields`.

### Excel (.xlsx)
- **Tecnología**: `openpyxl`.
- **Protección**: Bloqueo de todas las celdas por defecto. Desbloqueo de celdas específicas para entrada de datos. Aplicación de `SheetProtection` con contraseña (fija o configurable).

---

## Flujo de Información (Ejemplo)

```mermaid
sequenceDiagram
    participant U as Usuario
    participant A as Aplicativo (OCR/App)
    participant V as Validación Humana
    participant R as RAG (Normas + Empresa)
    participant O as Ollama (LLM)
    participant G as Generador Docs

    U->>A: Carga Doc Corporativo (PDF/Img)
    A->>V: Muestra Texto Extraído (OCR)
    V-->>A: Usuario Aprueba/Corrige
    A->>R: Indexa en Contexto Empresa
    U->>A: Solicita Generación Audit
    A->>R: Consulta Norma + Contexto
    R-->>A: Fragmentos Relevantes
    A->>O: Prompt: Diligencia Formato con Contexto
    O-->>A: Datos Producidos
    A->>G: Renderiza PDF/Word/Excel Protegido
    G-->>U: Documentos Listos
```

---

## Metodología de Auditoría (HMO-Method)

El sistema seguirá el ciclo PHVA (Planear, Hacer, Verificar, Actuar) basado en la **ISO 19011:2018**:

1. **Planificación Automatizada**: Generación del Programa y Plan de Auditoría basados en el alcance definido por el usuario.
2. **Ejecución Asistida**: Listas de verificación dinámicas que incluyen el "Debería" de la norma recuperado por RAG.
3. **Hallazgos y Evidencias**: Formatos vinculados directamente a los criterios normativos para asegurar trazabilidad.
4. **Cierre y Reporte**: Consolidación automática para auditorías externas.

---

## Plan de Desarrollo (Roadmap)

### Fase 1: MVP y Refinamiento Profesional (ISO 9001)
- Setup de Ollama + Interfaz de Ingesta (OCR/Manual).
- Implementación de RAG para ISO 9001 y Contexto Empresa.
- Generador de "Lista de Verificación de Auditoría" en Excel protegido y Word profesional.
- Implementación de la Capa de Integridad (SHA-256) y Bitácora de Auditoría.
- Conversión de toda la documentación corporativa a formatos .docx y PDF para presentaciones comerciales.
