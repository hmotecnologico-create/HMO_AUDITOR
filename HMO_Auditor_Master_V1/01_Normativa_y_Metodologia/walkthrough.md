# Walkthrough: Experiencia de Usuario "HMO Auditor"

Este documento simula el uso del aplicativo desde la perspectiva del auditor para validar que el diseño cumple con los requerimientos de "Sobrepasar cualquier auditoría externa".

## Paso 1: Ingesta de Información Corporativa (Contexto y OCR)
El auditor abre el aplicativo e inicia la fase de preparación cargando documentos (PDFs, Imágenes de actas, etc.).
- **Acción**: El sistema procesa los documentos usando **OCR Local** (Reconocimiento Óptico de Caracteres).
- **Validación Humana**: El aplicativo muestra una pantalla de "Reconocimiento":
    - *Izquierda*: Imagen original del documento.
    - *Derecha*: Texto extraído por la IA.
- **Visto Bueno**: El humano verifica que el aplicativo reconoció correctamente nombres, fechas y políticas. Solo tras la autorización manual, la información se indexa en el RAG.

## Paso 2: Configuración de la Auditoría (Offline)
- **Acción**: Selecciona "Nueva Auditoría".
- **Entrada**: 
    - Empresa: "Textiles del Norte S.A."
    - Proceso a Auditar: "Gestión de Compras"
    - Norma: "ISO 9001:2015"

## Paso 3: Generación y Auto-Diligenciamiento
El sistema realiza un cruce semántico entre la Norma y el Contexto Corporativo.
- **IA en Acción**: Ollama lee la "Política de Compras" ingerida y el requisito "8.4 Control de Proveedores".
- **Generación**: El sistema pre-diligencia los formatos:
    - *Checklist*: Escribe preguntas basadas en la norma pero adaptadas al nombre del proceso real de la empresa.
    - *Programa*: Autocompleta objetivos y alcance usando la Misión y Visión de la empresa.

## Paso 4: Revisión y Visto Bueno Humano
Antes de la exportación final, el auditor revisa el contenido en pantalla.
- **Interfaz**: El aplicativo muestra los campos auto-llenados por la IA resaltados en color azul.
- **Validación Humana**: El auditor puede corregir, ampliar o simplemente aceptar las sugerencias de la IA. Una vez validado, presiona "Aprobar para Generación".

## Paso 5: Exportación y Verificación de Integridad
- **Resultado**: El sistema genera los archivos finales (PDF, Word, Excel).
- **Protección**: La estructura y el texto aceptado quedan bloqueados con contraseña.
- **Validación Final**: El sistema emite un **Reporte de Validación de Integridad** que contiene el Hash SHA-256 de cada archivo, demostrando que los documentos no pueden ser alterados para auditorías posteriores.

---

### Resultado Final esperado ante Auditoría Externa
Cuando el auditor externo de la entidad certificadora revise estos documentos, encontrará:
1. **Precisión Contextual**: Los formatos hablan el "idioma" de la empresa.
2. **Consistencia Perfecta**: Los textos de la norma citados son literales.
3. **Trazabilidad Total**: Existe un registro inalterable de quién aprobó cada dato y qué fragmento de la norma se aplicó.
4. **Garantía de Integridad**: El sistema puede demostrar matemáticamente que los archivos no han sido modificados desde su creación.
