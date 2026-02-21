# Gestión de Controles Normativos (HMO Auditor)

El manejo de los controles es el motor de precisión del aplicativo. No tratamos las normas como texto plano, sino como una **Estructura Jerárquica de Controles** que permite la trazabilidad completa.

## 1. Arquitectura de Datos de Controles
Cada norma (ISO 9001, 27001, etc.) se descompone en objetos técnicos en nuestra base de datos vectorial (ChromaDB):

- **ID de Control**: Identificador único (ej: `ISO-27001-A.5.1`).
- **Dominio/Cláusula**: El macro-proceso (ej: `Políticas de Seguridad`).
- **Criterio de Auditoría**: El texto exacto de la norma ("El debe").
- **Evidencia Sugerida**: Lo que el RAG espera encontrar (ej: "Manual de Seguridad").
- **Pregunta de Verificación**: Generada por Ollama para el checklist.

## 2. Gestión Multi-Norma (Cross-Mapping)
HMO Auditor utiliza un motor de **Mapeo Cruzado** para encontrar redundancias. Si estás auditando Calidad (9001) y Seguridad (27001) simultáneamente:

- El sistema identifica que el control de **"Información Documentada" (9001:7.5)** es equivalente al de **"Gestión de Documentos" (27001:A.5.33)**.
- **Beneficio**: Al cargar un solo documento (ej: Listado Maestro), el sistema "marca" el cumplimiento en ambas normas automáticamente, ahorrando tiempo al auditor.

## 3. Motor de Verificación de Controles (RAG Workflow)
Cuando el usuario sube un documento, el sistema ejecuta este proceso para cada control:

1.  **Extracción semántica**: ¿De qué trata este documento subido por el usuario?
2.  **Matching Vectorial**: Se compara contra el "Criterio de Auditoría" del control en ChromaDB.
3.  **Scoring de Cumplimiento**: 
    - **Alto (90-100%)**: Cumple totalmente. Sugiere "C" (Conforme).
    - **Medio (40-89%)**: Cumple parcialmente. Sugiere revisar.
    - **Bajo (<40%)**: No se encontró relación. Sugiere "NC" (No Conforme).

## 4. Visualización de Controles (Dashboard)
Los controles se visualizan en el Dashboard de Trazabilidad como **Nodos**:
- **Verde**: Control verificado y aprobado por el auditor.
- **Amarillo**: Documento cargado pero requiere validación humana (HITL).
- **Rojo**: Requisito normativo sin evidencia detectada.

## 5. Salida Legal
En los formatos **GAD-LIST-02 (Excel)**, cada fila representa un control con su respectivo **Hash de Verificación**, garantizando que el hallazgo está anclado a un control veraz de la norma interna cargada.

> [!IMPORTANT]
> Esta gestión de controles asegura que el auditor no olvide ningún punto crítico de la norma, actuando como un "copiloto experto" que vigila el 100% de los requisitos legales.
