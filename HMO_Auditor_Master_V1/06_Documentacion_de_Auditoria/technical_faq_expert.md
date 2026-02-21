# Compendio de Consultas Técnicas y Estratégicas (FAQ Experto)

Este documento recopila las definiciones clave y respuestas técnicas generadas durante la construcción del ecosistema **HMO Auditor V1.3 Elite**. Es el "Manual de Respuestas" para auditores externos o evaluadores del sistema.

---

## 1. Veracidad Normativa (Root of Trust)
**P: ¿De dónde salen las normas y cómo garantizan la veracidad?**
**R:** El sistema utiliza una arquitectura **RAG (Retrieval-Augmented Generation)**. La veracidad se ancla en documentos PDF oficiales (ISO 9001, 27001, 14001, Ley 115, Dec. 1330). El sistema no "alucina" porque está programado para priorizar el texto exacto de la norma cargada sobre su conocimiento general, citando siempre el Numeral o Cláusula correspondiente.

## 2. Base de Datos Vectorial (Motor de Memoria)
**P: ¿Qué base de datos vectorial usa el sistema y por qué?**
**R:** Utilizamos **ChromaDB**. Es una base de datos vectorial de código abierto que opera **100% en local**. Esto es crítico para la privacidad: los datos de la auditoría nunca viajan a servidores externos. Permite una búsqueda semántica ultrarrápida para encontrar evidencias en milisegundos.
- *Acceso*: Se puede inspeccionar mediante el script `inspect_vdb.py` incluido en el expediente.

## 3. Gestión de Controles e Integridad
**P: ¿Cómo se manejan los controles de cada norma?**
**R:** El sistema descompone la norma en una jerarquía de controles. Aplica un **Mapeo Cruzado (Cross-Mapping)** que identifica duplicidades entre diferentes normas (ej: ISO 9001 vs 27001). Al validar un control común, se actualiza el cumplimiento en todo el ecosistema. Cada hallazgo se sella con un hash **SHA-256** para garantizar que el reporte no sea alterado tras su emisión.

## 4. Persistencia y Continuidad
**P: ¿Se puede pausar y retomar una auditoría?**
**R:** Sí. El aplicativo implementa un **Motor de Persistencia Automática**. Cada empresa tiene su propia cápsula de datos (`audit_state.json`) que guarda el paso exacto de la ingesta, la norma elegida y el logo cargado. Al reiniciar el Dashboard, el usuario simplemente selecciona su empresa y retoma el trabajo donde lo dejó.

## 5. Identidad Corporativa (Manejo de Logos)
**P: ¿Cómo se insertan los logos en los formatos?**
**R:** El sistema permite la carga dinámica de logos por empresa. Estos se guardan de forma persistente en el directorio de trabajo corporativo y los scripts generadores de Word/Excel los inyectan automáticamente en la cabecera mediante tablas de encabezado profesionales, asegurando la validez institucional del documento.

---
> [!NOTE]
> Este documento se actualiza dinámicamente según evolucionan las capacidades del aplicativo y las consultas del auditor líder.
