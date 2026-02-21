# Manual de Desarrollo: Guía Técnica HMO Auditor

Este manual está dirigido a desarrolladores y arquitectos de software encargados de mantener, escalar o arrendar el sistema **HMO Auditor**.

## 1. Stack Tecnológico (Stack-on-Local)
- **Frontend**: React.js / Vite (para alta velocidad de renderizado).
- **Backend API**: FastAPI (Python) - Proporciona documentación Swagger automática.
- **Motor AI**: Ollama (Ejecutándose como un servicio local en el puerto 11434).
- **Base Vectorial**: ChromaDB (Almacenamiento persistente en la carpeta `/db/vectors`).
- **Base Relacional**: SQLite (Almacenamiento de logs de trazabilidad y configuración).

## 2. Setup del Entorno de Desarrollo
1. **Instalar Dependencias**: `pip install -r requirements.txt`.
2. **Habilitar Ollama**: `ollama serve`.
3. **Descargar Modelos**: `ollama pull llama3` o `mistral`.
4. **Ejecutar API**: `uvicorn main:app --reload`.

## 3. Estructura de Prompts (Prompt Engineering)
Los prompts se encuentran centralizados en el módulo `core/prompts.py`. Para cumplir con la normativa, cada prompt de generación sigue esta estructura:
- **System**: "Eres un auditor líder certificado en ISO 9001..."
- **Context**: [Fragmentos recuperados del RAG].
- **Constraint**: "Responde solo basándote en la evidencia provista. No inventes datos."

## 4. Extensibilidad: Añadir Nuevas Normas
Para añadir una norma (ej: ISO 14001):
1. Cargue el PDF de la norma en la carpeta `data/regulations/`.
2. Ejecute el script `ingest_norm.py`.
3. El sistema creará una nueva colección en ChromaDB.
4. El usuario verá la nueva opción en el Selector de Norma del aplicativo.

## 5. Mantenimiento y Seguridad
- **Copias de Seguridad**: Resguardar periódicamente el archivo `hmo_audit_trail.db` (SQLite).
- **Protección de Archivos**: La lógica de Hashing SHA-256 se encuentra en `utils/security.py`. No modificar a menos que se requiera un nuevo estándar de cifrado.

---

### HMO Auditor - "Built to Last"
Este sistema ha sido diseñado con una arquitectura desacoplada, permitiendo que el motor de IA (Ollama) pueda ser actualizado sin afectar la lógica de negocio ni la integridad documental.
