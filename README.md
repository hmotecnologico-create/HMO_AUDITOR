# HMO Auditor

**Asistente de auditoría de sistemas de gestión con IA local.** Organiza el expediente de una empresa, valida que cada documento tenga el contenido mínimo exigido y apoya el análisis del auditor con un modelo de lenguaje que corre en el propio equipo. Los documentos no salen de la máquina.

> Autor: **Heyder Medrano Olier** · Estado: prototipo funcional en evolución (2026)

## Problema que resuelve

Preparar una auditoría ISO toma tiempo: hay que reunir los documentos base de la empresa (Cámara de Comercio, RUT, políticas, matrices), revisar que cada uno tenga lo que pide la norma y redactar hallazgos con evidencia. HMO Auditor guía ese proceso por fases y automatiza la parte repetitiva, mientras el criterio final queda en manos del auditor.

## Funcionalidades

| Módulo | Archivo | Qué hace |
|---|---|---|
| Consola web | `streamlit_app.py` | Recorre la auditoría en tres fases: **A** identidad corporativa, **B** dimensión de la organización y **C** revisión. Incluye el control del expediente, el centro de emisión de documentos, la guía de usuario, la base normativa y un asistente de IA |
| Extracción OCR | `HMO_OCR_Extractor.py` | Saca los campos del certificado de Cámara de Comercio y del RUT de la DIAN |
| Validación documental | `HMO_Document_Validator.py` | Revisa contenido, estructura y pertinencia según ISO 19011, ISO 9001, ISO 27001 e ISO 14001 |
| Motor de IA | `HMO_AI_Engine.py` | Análisis semántico con [Ollama](https://ollama.com) (por defecto `llama3:8b`): ISO 19011 como metodología y la norma elegida como criterio |
| Simulación | `HMO_Simulation_Engine.py` | Genera documentos de una empresa ficticia (*Innovatech*) para practicar |
| Autenticación | `HMO_Auth.py` | Usuarios locales con roles `admin`, `auditor` y `visitante`, contraseñas con hash y cambio obligatorio en el primer acceso |

## Stack

Python 3.11 · Streamlit · pandas · Plotly · python-docx · openpyxl · fpdf2 · pdfplumber · Tesseract OCR · Poppler · Ollama.

## Instalación

**En Windows, con el script:** ejecuta `instalar_hmo.bat`. Comprueba que estén Git y Python y luego instala la aplicación en `%USERPROFILE%\HMO_Auditor`.

**Manual:**

```bash
git clone https://github.com/hmotecnologico-create/HMO_AUDITOR.git
cd HMO_AUDITOR
python -m venv .venv && .venv\Scripts\activate      # en Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Requisitos del sistema:
- **Tesseract OCR** con el idioma español y **Poppler**. En Linux, los paquetes están en `packages.txt`.
- **Ollama** con el modelo descargado: `ollama pull llama3:8b`.

## Ejecución

```bash
streamlit run streamlit_app.py
```

**Primer acceso:**
- Al arrancar por primera vez se crean las cuentas `admin`, `auditor` y `visitante`.
- Cada clave temporal se toma de su variable de entorno, si está definida: `HMO_ADMIN_PASS`, `HMO_AUDITOR_PASS` y `HMO_VISITANTE_PASS`.
- Las claves que no estén definidas se generan al azar y se guardan en `hmo_credenciales_iniciales.txt`. Git ignora ese archivo.
- `admin` y `auditor` deben cambiar su clave al entrar. Después, borra el archivo.

## Estructura

```
streamlit_app.py              Consola principal
HMO_*.py                      Módulos (IA, OCR, validación, simulación, autenticación)
HMO_Auditor_Master_V1/        Normativa y metodología, formatos, simulación y scripts generadores
Auditorias_HMO/               Expedientes de ejemplo (empresa ficticia Innovatech)
mecanismo_aprendizaje.md      Cómo evoluciona el asistente
```

## Seguridad

- Todo se procesa en local: el modelo corre en Ollama y no hay llamadas a servicios externos de IA.
- `hmo_users.json`, el estado de las auditorías y los registros están en `.gitignore`.
- No subas documentos reales de clientes a este repositorio. Los ejemplos corresponden a una empresa ficticia.

## Estado

Prototipo funcional. Lo que se puede mejorar:
- Pruebas automatizadas.
- Separar la interfaz de `streamlit_app.py` en módulos.
- Una licencia explícita.
