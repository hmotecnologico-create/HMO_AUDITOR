# Ingeniería de Software: Casos de Uso e Historias de Usuario

Este documento detalla los requerimientos funcionales del sistema **HMO Auditor** desde la perspectiva de ingeniería, para facilitar su desarrollo, venta o arrendamiento.

## 1. Actor: Auditor Auxiliar

### Caso de Uso: CU-01 - Ingesta de Documento con OCR
- **Descripción**: El auditor carga un archivo (Img/PDF) y valida el texto extraído.
- **Precondición**: El auditor ha seleccionado una empresa (Simulación o Real).
- **Flujo Principal**:
    1. El sistema recibe el archivo.
    2. El motor OCR procesa la imagen localmente.
    3. El sistema muestra la interfaz de "Doble Vista".
    4. El usuario corrige o añade datos manualmente.
    5. El usuario autoriza la indexación al RAG.
- **Postcondición**: El texto se almacena en la base vectorial con metadatos de origen.

### Historia de Usuario: US-01 - Validación Manual
> "Como Auditor Auxiliar, quiero poder ingresar manualmente los datos que la IA ignora, para garantizar que la base de conocimientos sea 100% exacta y no contenga errores de lectura."

## 2. Actor: Director de Calidad

### Caso de Uso: CU-02 - Emisión de Reporte Protegido
- **Descripción**: El director revisa el borrador generado por la IA y emite el archivo final.
- **Precondición**: La auditoría ha superado el 90% de progreso en los nodos.
- **Flujo Principal**:
    1. El sistema recupera los hallazgos y evidencias del RAG.
    2. El sistema genera un borrador en Word/Excel.
    3. El Director aprueba la coherencia normativa (Audit-on-Audit).
    4. El sistema aplica el bloqueo estructural y calcula el Hash SHA-256.
- **Postcondición**: Se genera el archivo oficial y el Certificado de Integridad.

### Historia de Usuario: US-02 - Trazabilidad Normativa
> "Como Director de Calidad, quiero que cada hallazgo tenga una referencia a la cláusula exacta de la norma, para que los auditores externos validen nuestra rigurosidad técnica."

## 3. Actor: Administrador de TI

### Historia de Usuario: US-03 - Privacidad Local
> "Como Administrador de TI, necesito que el aplicativo funcione 100% offline con Ollama, para cumplir con las políticas de seguridad de la información (ISO 27001) y proteger los datos de la empresa."

## 4. Matriz de Casos de Uso vs Requisitos
| ID Requisito | Descripción | Caso de Uso Asociado |
| :--- | :--- | :---: |
| RF-01 | Procesamiento de imagenes con OCR local | CU-01 |
| RF-02 | Generación de Hash SHA-256 para integridad | CU-02 |
| RF-03 | Navegación visual por mapa de nodos | Dashboard |
| RF-04 | Soporte Multi-empresa (Nueva vs Simulación) | App Init |
