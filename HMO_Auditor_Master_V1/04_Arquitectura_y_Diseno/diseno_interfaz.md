# Diseño Conceptual: Interfaz "HMO Auditor Professional"

Para que el aplicativo sea vendible y fácil de usar para no expertos, la interfaz seguirá este diseño:

## 1. El Tablero de Control (Dashboard)
- **Mapa de Nodos de Progreso**: Un gráfico interactivo que muestra el camino hacia la certificación.
    - **Nodos Verdes**: Tareas completadas y auditadas.
    - **Nodos Azules**: Tarea actual en proceso.
    - **Nodos Grises**: Pasos pendientes.
    - **Nodos de Alerta (Rojo)**: Requisitos que no pasaron la validación de integridad o coherencia.
- **Barra de Progreso Circular**: Indica el porcentaje de avance hacia la certificación.

## 2. Módulo de Ingesta "Drag & Drop"
- Una zona central de diseño premium donde el usuario suelta sus archivos (PDF, Word).
- **Validación Visual**: Al cargar un archivo, la IA muestra una etiqueta verde de "Procesado" y extrae automáticamente campos clave (Ej: Detectó el NIT de la empresa).

## 3. Asistente "Paso a Paso" (Wizard)
- El aplicativo no muestra todos los formatos a la vez para no abrumar.
- **Flujo**: "¿Empezamos con el Acta de Inicio? Sube el acta o redactémosla aquí mismo con ayuda de Ollama".

## 4. El Botón de Ayuda Inteligente (Help Bot)
- Ubicado en la esquina inferior derecha con un diseño minimalista.
- **Función**: Al hacer clic, abre un chat local que explica el requisito de la norma en "lenguaje sencillo" (sin tecnicismos legales).

## 5. Vista Previa de Documentos Protegidos
- Una ventana dividida:
    - **Izquierda**: Lo que propone la IA.
    - **Derecha**: Lo que el usuario edita o aprueba.
- **Botón Final**: "Emitir Documento Oficial Protegido".
