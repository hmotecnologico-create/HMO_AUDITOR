# HMO Auditor - Ecosistema de Auditoría Local Profesional

Este es un producto de ingeniería diseñado para el SENA, enfocado en la automatización de auditorías internas bajo estándares internacionales (ISO) y académicos. El sistema utiliza una arquitectura RAG (Retrieval-Augmented Generation) operando 100% en local para garantizar la privacidad y veracidad normativa.

## 🚀 Funcionalidades Elite
- **Motor Multi-Norma**: Soporte nativo para ISO 9001, 27001, 14001 y Sector Académico.
- **Continuidad Multi-Día**: Sistema de persistencia automática por empresa.
- **Identidad Institucional**: Inyección dinámica de logos en cabeceras de Word y Excel.
- **Blindaje Legal**: Formatos con trazabilidad SHA-256 y firmas de integridad.
- **Root of Trust Normativo**: Anclaje estricto a documentos oficiales sin alucinaciones.

## 🛠️ Instalación y Ejecución

### 1. Dependencias
```powershell
pip install -r HMO_Auditor_Master_V1/requirements.txt
```

### 2. Lanzar Dashboard
```powershell
streamlit run HMO_Auditor_Master_V1/04_Arquitectura_y_Diseno/Scripts_Generadores/HMO_Dashboard_Prototype.py
```

## 📁 Estructura del Repositorio
- `01_Estrategia_y_Planeacion`: Documentos de visión y arquitectura.
- `02_Normatividad_y_Formatos`: Biblioteca de plantillas y fuentes legales.
- `03_Casos_de_Prueba_Innovatech`: Datos simulados para entrenamiento.
- `04_Arquitectura_y_Diseno`: Scripts generadores y Dashboard principal.
- `05_Manuales_y_Documentacion`: Guías completas para usuarios y desarrolladores.

### 📑 Documentación para Auditoría (Root of Trust)
Para fines de verificación y auditoría externa del propio aplicativo, se ha consolidado un expediente técnico en la carpeta:
`06_Documentacion_de_Auditoria/`

Este expediente incluye:
*   **[Matriz de Veracidad Normativa](06_Documentacion_de_Auditoria/normative_sources.md)**: Justificación legal y técnica de las normas ISO y Decretos MEN.
*   **[Plan de Implementación](06_Documentacion_de_Auditoria/implementation_plan.md)**: El "Cerebro" técnico del motor RAG.
*   **[Walkthrough Final](06_Documentacion_de_Auditoria/walkthrough.md)**: Recorrido por los hitos del proyecto.
*   **[Manual de Procedimientos](06_Documentacion_de_Auditoria/audit_manual_procedures.md)**: Protocolos de validación humana (HITL).
*   **[Compendio FAQ Experto](06_Documentacion_de_Auditoria/technical_faq_expert.md)**: Respuestas a consultas técnicas estratégicas (BD Vectorial, Controles, Persistencia).
*   **[Guía de Acceso a DB](06_Documentacion_de_Auditoria/guia_acceso_db.md)**: Cómo inspeccionar el motor vectorial ChromaDB.
*   **[Checklist de Tareas](06_Documentacion_de_Auditoria/task.md)**: Evidencia del proceso de desarrollo.

---
**Resultado Legal**: El aplicativo está documentado al 100% bajo estándares **ISO 19011:2018**, garantizando que el motor RAG es una fuente veraz y auditable.

---

## ⚖️ Aviso Legal
Este software es una herramienta de asistencia profesional. La responsabilidad final de la auditoría recae en el auditor humano certificado. Los documentos generados incluyen hashes de integridad para prevenir manipulaciones no autorizadas.

---
**Desarrollador:** SENA - HMO Auditor Project v1.3 Elite
**Licencia:** Prototipo Maestro de Ingeniería
