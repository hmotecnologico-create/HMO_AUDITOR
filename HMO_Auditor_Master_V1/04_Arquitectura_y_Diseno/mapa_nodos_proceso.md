# Mapa de Nodos: Trazabilidad del Proceso de Certificación

Este gráfico representa el "Camino Crítico" que el usuario visualiza en el aplicativo. Cada nodo es un hito que requiere insumos de ingesta y validación humana.

```mermaid
graph TD
    %% Nodos de Proceso
    A((1. Inicio: Decisión Directiva)) -->|Acta de Inicio| B((2. Contexto Estratégico))
    B -->|Misión/Visión/Política| C((3. Mapa de Procesos))
    C -->|Identificación de Áreas| D((4. Ingesta de Manuales))
    D -->|OCR + Validación| E{5. Verificación de Integridad}
    
    %% Ramificación de Auditoría
    E -->|Aprobado| F((6. Programa de Auditoría))
    E -->|Pendiente / Faltan Datos| D
    
    F -->|Cronograma AI| G((7. Ejecución: Checklist))
    G -->|Hallazgos AI| H((8. Revisión por Gerencia))
    H -->|Cierre de Brechas| I((9. Auditoría Externa))
    I -->|Validación Final| J((10. CERTIFICACIÓN))

    %% Estilos de Estado (Conceptuales)
    style A fill:#4CAF50,stroke:#388E3C,color:#fff %% Completado
    style B fill:#4CAF50,stroke:#388E3C,color:#fff %% Completado
    style C fill:#2196F3,stroke:#1976D2,color:#fff %% En Proceso (Nodo Azul)
    style D fill:#f3f3f3,stroke:#bbb,color:#666 %% Pendiente (Gris)
    style J fill:#FFD700,stroke:#DAA520,color:#000 %% Meta (Oro)
```

## Trazabilidad por Nodo
Cada nodo en el aplicativo es interactivo. Al hacer clic en un nodo:
1. **Insumos Requeridos**: Muestra qué documentos faltan subir.
2. **Estado de Validación**: Indica si la integridad (Hash) ya fue generada.
3. **Avance Normativo**: Muestra qué cláusulas de la norma (ej: ISO 9001) ya están cubiertas por ese nodo.

### Botón de Ayuda Contextual
Si el aplicativo detecta que estás "atascado" entre el nodo 4 y 5, el **Help Bot** te dirá:
> "He notado que cargaste los manuales operativos, pero aún no has dado el 'Visto Bueno' al texto extraído por el OCR. Haz clic en el Nodo 4 para terminar la validación y poder avanzar al Programa de Auditoría."
