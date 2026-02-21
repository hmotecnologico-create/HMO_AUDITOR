# Mockup de Interfaz: Validación de Ingesta (OCR + Manual)

Esta es la representación visual de la pantalla de "Doble Vista" con capacidad de **Anulación y Adición Manual**.

| Vista Original (Documento) | Texto Extraído e Interacción Manual |
| :--- | :--- |
| ![Imagen de Acta Original](https://placehold.co/400x300/f0f0f0/333333?text=Acta+de+Reunion+Escaneada) | **Texto Reconocido AI**: [Editable] |
| | **+ Añadir Dato Omitido**: [Botón para campos nuevos] |
| | **Metadatos Críticos Manuales**: <br> - Fecha Manual: [Input] <br> - Cargo Responsable: [Input] |

---

## Panel de Control de Ingesta (Control Total Humano)
1. **[Reconocer Texto]**: La IA extrae lo que puede.
2. **[Corrección Directa]**: Puedes editar directamente cualquier palabra que la IA lea mal.
3. **[Formulario de Datos Faltantes]**: Si el documento tiene una cláusula o política importante que la IA ignoró, presiona este botón para escribirla manualmente.
4. **[Autorizar e Indexar]**: El humano da fe de que el texto final (IA + Manual) es fiel al documento real.

### Lógica de Ayuda (Help Bot)
> "¿La IA no leyó una página o un párrafo? No hay problema. Usa el botón **'Añadir Dato Omitido'** para completar la información manualmente. Recuerda que tú tienes la última palabra antes de que esta información alimente los formatos de auditoría."
