# Especificación de Formatos con Validez Jurídica (Blindaje Legal)

Para que un formato de auditoría generado por **HMO Auditor** sea legalmente válido y sobrepase auditorías de certificación externas, debe cumplir con los siguientes 17 requisitos técnicos-legales basados en **ISO 19011:2018**, **ISO 9001:2015** y la **Ley General de Archivos**.

## 1. Estructura de Encabezado (Identificación Unívoca)
Todo documento debe permitir la individualización inmediata.
- **Nombre de la Organización**: "Innovatech Solutions SAS" (o la empresa configurada).
- **Logo Institucional**: Espacio reservado para el logo oficial.
- **Nombre del Documento**: Título claro (ej: "Lista de Verificación de Auditoría").
- **Código del Formato**: Ej. `AUD-PROG-01`.
- **Versión y Fecha**: Control de vigencia del formato.
- **Paginación**: Formato "Página X de Y".

## 2. Datos Generales y Alcance Legal
Define el contexto jurídico del proceso.
- **Tipo de Auditoría**: Interna, de Calidad, de Procesos.
- **Proceso / Área Auditada**: Especificación de límites.
- **Ubicación y Fecha**: Lugar y momento exacto de la realización del acto.
- **Objetivo y Alcance**: Límites legales de lo que se auditó y lo que no.

## 3. Identificación de Partes y Responsabilidad Jurídica
*Elemento Crítico para la validez de la certificación.*
- **Auditor**: Nombre completo, cargo y espacio para firma.
- **Auditado**: Nombre completo, cargo y espacio para firma de conformidad/notificación.

## 4. Núcleo Técnico: Lista de Verificación y Evidencia
*Sin evidencia, la auditoría carece de valor legal.*
- **Estructura de Tabla**: Ítem | Requisito Normativo | Cumplimiento (C/NC/NA) | Observación | **Evidencia Hallada**.
- **Registro de Evidencias**: Documentos, capturas, reportes analizados por la IA y validados por el humano.

## 5. Registro y Clasificación de Hallazgos
Los hallazgos deben estar categorizados según el riesgo:
- **No Conformidad**: Incumplimiento de requisito.
- **Observación**: Riesgo potencial identificado.
- **Oportunidad de Mejora**: Mejora sugerida.

## 6. Conclusión y Cierre Formal
- **Conclusión Técnica-Legal**: Resumen del estado de cumplimiento.
- **Bloque de Firmas**: Espacio para firmas autógrafas o digitales (obligatorio). *Sin firma, no es legalmente válido.*

## 7. Control de Integridad Digital (Plus HMO)
- **Código Único de Documento**: Generado automáticamente para trazabilidad.
- **Hash SHA-256**: Código de integridad que garantiza que el archivo no fue manipulado tras la firma.
- **Base Legal**: Referencia explícita a ISO 19011 e ISO 9001.

---

> [!WARNING]
> Un formato sin **Firma**, **Evidencia** o **Código de Control** es nulo para procesos de certificación externa. HMO Auditor garantiza la inclusión de estos 17 elementos en cada exportación.
