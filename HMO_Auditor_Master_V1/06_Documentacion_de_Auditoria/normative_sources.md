# Matriz de Fuentes y Veracidad Normativa (HMO Auditor)

La base de conocimiento del aplicativo se sustenta en tres capas de veracidad para garantizar que el "corazón" del sistema sea inexpugnable.

## 1. Fuentes Oficiales (Prototipo V1.2)
Para la lógica de las **"Cartas de Navegación"**, se han utilizado las siguientes fuentes públicas y oficiales:

| Sistema | Referencia Principal | Origen de la Fuente |
| :--- | :--- | :--- |
| **Calidad** | ISO 9001:2015 | Estándar Internacional de Calidad |
| **Seguridad** | ISO 27001:2022 | Estándar Internacional de Ciberseguridad |
| **Ambiental** | ISO 14001:2015 | Estándar Internacional Gestión Ambiental |
| **Académico** | Ley 115 (Gral de Educación) | Ministerio de Educación Nacional (Colombia) |
| **Académico** | Decreto 1330 de 2019 | Regulación Registro Calificado (Colombia) |
| **Metodología**| ISO 19011:2018 | Directrices para la auditoría de S.G. |

## 2. Protocolo de Veracidad RAG (Root of Trust)
Para asegurar que el sistema no "alucine", el motor RAG opera bajo el principio de **"Anclaje en Evidencia"**:

- **Capa A (Biblioteca Normativa)**: El sistema NO depende solo de lo que la IA "sabe". El auditor debe cargar los PDFs oficiales de la norma en la carpeta de configuración. El RAG extrae los párrafos exactos (ej: "Cláusula 4.1") antes de sugerir cualquier hallazgo.
- **Capa B (Contexto Empresa)**: Los documentos cargados por el usuario (Misión, PEI, Políticas) se pasan por un proceso de hashing (SHA-256) para asegurar que el análisis se haga sobre la versión veraz y verificada.

## 3. Validación de Autoridad (HITL)
El modelo **Human-In-The-Loop** permite que el auditor profesional vea la fuente:
- En cada respuesta del bot de ayuda o en los formatos auto-diligenciados, el sistema está diseñado para citar el **Numeral Específico** de la norma que justifica la acción.

> [!CAUTION]
> Para auditorías de certificación legal, se recomienda que el administrador del sistema cargue las versiones pagas y oficiales de ICONTEC / ISO en la base de datos vectorial para garantizar cumplimiento 100%.
