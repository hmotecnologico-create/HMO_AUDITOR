"""
HMO_Document_Validator.py  —  V15.0 Motor de Validación Documental
====================================================================
Valida que cada documento subido cumpla los REQUISITOS MÍNIMOS
de contenido, estructura y pertinencia establecidos por:
  - ISO 19011:2018 (Directrices para auditoría)
  - ISO 9001:2015  (Calidad)
  - ISO 27001:2022 (Seguridad de la Información)
  - ISO 14001:2015 (Ambiental)

Arquitectura:
  SCHEMA → describe qué debe tener cada tipo de documento
  validate_document() → evalúa el texto contra el esquema
  generate_report() → produce el informe de validación para el auditor

Autor: HMO Auditor Elite V15.0
"""

import re


# ═══════════════════════════════════════════════════════════════════════════
#  ESQUEMAS DE DOCUMENTOS  —  Requisitos Mínimos por Tipo
# ═══════════════════════════════════════════════════════════════════════════

DOCUMENT_SCHEMAS = {

    # ──────────────────────────────────────────────────────────────────────
    "acta_compromiso": {
        "nombre": "Acta de Compromiso Directivo",
        "norma_ref": "ISO 9001:2015 cláusula 5.1 / ISO 19011 §6.2",
        "descripcion": "Documento que formaliza el compromiso de la alta dirección con el sistema de gestión.",

        # Palabras clave de MEMBRETE / ENCABEZADO — al menos 2 de estas
        "membrete": [
            "ACTA", "COMPROMISO", "COMPANY", "NIT", "RAZON SOCIAL",
            "LOGO", "NOMBRE DE LA EMPRESA"
        ],
        "membrete_minimo": 2,

        # Secciones que DEBEN existir (al menos el 70%)
        "secciones_requeridas": [
            "OBJETO",            # Propósito del acta
            "ASISTENTES",        # Lista de participantes
            "COMPROMISOS",       # Compromisos adquiridos
            "RECURSOS",          # Asignación de recursos
            "RESPONSABLE",       # Designación de responsables
            "FIRMA",             # Firmas
        ],
        "secciones_minimo": 4,   # mínimo 4 de 6 secciones

        # Keywords de CONTENIDO que verifican pertinencia del documento
        "keywords_contenido": [
            "sistema de gestion", "auditoria", "compromiso", "gestion",
            "calidad", "responsable", "gerente", "director", "objetivo",
            "cumplimiento", "procesos", "mejora continua"
        ],
        "keywords_contenido_minimo": 4,

        # Campos específicos a extraer
        "campos_extraer": {
            "fecha": r"(?:fecha|date|cartagena|bogota|medellin)[,\s]+(\d{1,2}\s+de\s+\w+\s+de\s+\d{4}|\d{4}[\-/]\d{2}[\-/]\d{2})",
            "empresa": r"(?:empresa|razon social|entidad|organizacion)[\s:]+([A-ZÁÉÍÓÚÑ][^\n]{3,60})",
            "director": r"(?:gerente|director|representante\s+legal|cargo)[\s:]*\n?([A-ZÁÉÍÓÚÑ][^\n]{5,50})",
        },

        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "estados_financieros": {
        "nombre": "Estados Financieros",
        "norma_ref": "ISO 9001:2015 cláusula 7.1.1",
        "descripcion": "Reportes financieros que evidencian capacidad de recursos.",

        "membrete": [
            "ESTADOS FINANCIEROS", "BALANCE", "NIT", "CONTADOR",
            "RAZON SOCIAL", "PERIODO", "VIGENCIA"
        ],
        "membrete_minimo": 2,

        "secciones_requeridas": [
            "BALANCE GENERAL",   # o "SITUACION FINANCIERA"
            "ESTADO DE RESULTADO",
            "ACTIVO",
            "PASIVO",
            "PATRIMONIO",
            "CONTADOR",          # Nombret del contador
            "TARJETA PROFESIONAL",
        ],
        "secciones_minimo": 4,

        "keywords_contenido": [
            "activo", "pasivo", "patrimonio", "utilidad", "perdida",
            "inventario", "cartera", "efectivo", "capital", "deuda",
            "ingreso", "egreso", "cuentas", "balance"
        ],
        "keywords_contenido_minimo": 5,

        "campos_extraer": {
            "periodo": r"(?:periodo|vigencia|año fiscal|ejercicio)[^\d]*(\d{4})",
            "contador": r"(?:contador|revisor)[\s:]+([A-ZÁÉÍÓÚÑ][^\n]{5,50})",
            "tarjeta_pro": r"(?:T\.P\.|tarjeta\s+profesional|T\.P)[^\d]*([\d\-]+)",
            "total_activo": r"total\s+activo[^\d]*\$?([\d\.,]+)",
        },

        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "mision_vision": {
        "nombre": "Misión y Visión Corporativa",
        "norma_ref": "ISO 9001:2015 cláusula 4.1",
        "descripcion": "Declaración formal del propósito y horizonte estratégico de la organización.",

        "membrete": [
            "MISION", "VISION", "NIT", "EMPRESA", "RAZON SOCIAL"
        ],
        "membrete_minimo": 2,

        "secciones_requeridas": [
            "MISION",       # Declaración de misión
            "VISION",       # Declaración de visión
            "VALORES",      # Valores corporativos
            "APROBADO POR", # Firma o aprobación
        ],
        "secciones_minimo": 2,

        "keywords_contenido": [
            "clientes", "calidad", "servicios", "productos", "trabajadores",
            "liderazgo", "crecimiento", "excelencia", "compromiso",
            "sociedad", "futuro", "comunidad", "integridad"
        ],
        "keywords_contenido_minimo": 3,

        # La visión DEBE tener un horizonte temporal
        "reglas_especiales": [
            {
                "id": "vision_temporal",
                "descripcion": "La Visión debe indicar un horizonte temporal (año futuro)",
                "patron": r"20[2-9]\d|para\s+el\s+año|en\s+\d+\s+años",
                "requerido": True,
                "puntos": 15,
            }
        ],

        "campos_extraer": {
            "texto_mision": r"(?:MISI[ÓO]N[\s:]+)(.{50,500}?)(?=VISI[ÓO]N|VALORES|$)",
            "texto_vision": r"(?:VISI[ÓO]N[\s:]+)(.{50,500}?)(?=MISI[ÓO]N|VALORES|APROBADO|$)",
            "horizonte": r"(20[2-9]\d)",
        },

        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "manual_funciones": {
        "nombre": "Manual de Funciones y Perfiles",
        "norma_ref": "ISO 9001:2015 cláusula 7.2",
        "descripcion": "Descripción de cargos, funciones y competencias del talento humano.",

        "membrete": [
            "MANUAL DE FUNCIONES", "PERFIL", "CARGO", "NIT", "EMPRESA"
        ],
        "membrete_minimo": 2,

        "secciones_requeridas": [
            "CARGO",            # Nombre del cargo
            "MISION DEL CARGO", # O "PROPOSITO"
            "FUNCIONES",        # Listado de funciones
            "PERFIL",           # Perfil requerido
            "EDUCACION",        # O "FORMACION ACADEMICA"
            "EXPERIENCIA",      # Experiencia requerida
            "APROBADO",         # Aprobación RRHH
        ],
        "secciones_minimo": 4,

        "keywords_contenido": [
            "cargo", "funciones", "responsabilidades", "habilidades",
            "competencias", "experiencia", "educacion", "formacion",
            "perfil", "requisitos", "titulo", "conocimientos"
        ],
        "keywords_contenido_minimo": 4,

        "campos_extraer": {
            "nombre_cargo": r"(?:CARGO|DENOMINACION)[\s:]+([A-ZÁÉÍÓÚÑ][^\n]{3,50})",
            "nivel_educativo": r"(?:EDUCACION|FORMACION|TITULO)[\s:]+([^\n]{5,80})",
            "experiencia": r"(?:EXPERIENCIA)[\s:]+([^\n]{5,60})",
        },

        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "politica_seguridad": {
        "nombre": "Política de Seguridad de la Información",
        "norma_ref": "ISO 27001:2022 cláusula 5.2",
        "descripcion": "Directriz de alto nivel que establece el compromiso con la seguridad de la información.",

        "membrete": [
            "POLITICA", "SEGURIDAD", "INFORMACION", "NIT", "EMPRESA", "SGSI"
        ],
        "membrete_minimo": 3,

        "secciones_requeridas": [
            "ALCANCE",           # Alcance del SGSI
            "OBJETIVOS",         # Objetivos de seguridad
            "CONFIDENCIALIDAD",  # Triada CID
            "INTEGRIDAD",
            "DISPONIBILIDAD",
            "RESPONSABILIDADES", # Roles y responsabilidades
            "VIGENCIA",          # Fecha de vigencia
            "FIRMA",             # Aprobación de dirección
        ],
        "secciones_minimo": 5,

        "keywords_contenido": [
            "seguridad", "informacion", "confidencialidad", "integridad",
            "disponibilidad", "activos", "riesgo", "control", "acceso",
            "datos", "sistema", "proteccion", "incidente", "politica"
        ],
        "keywords_contenido_minimo": 6,

        "reglas_especiales": [
            {
                "id": "triada_cid",
                "descripcion": "Debe mencionar la Triada CID: Confidencialidad, Integridad y Disponibilidad",
                "patron": r"confidencialidad.{0,200}integridad.{0,200}disponibilidad",
                "requerido": True,
                "puntos": 20,
            },
            {
                "id": "version_fecha",
                "descripcion": "Debe tener versión y fecha de aprobación",
                "patron": r"(?:versi[oó]n|version|v\.?\s*\d)\s*[\d\.]+",
                "requerido": False,
                "puntos": 10,
            }
        ],

        "campos_extraer": {
            "alcance": r"(?:ALCANCE[\s:]+)(.{20,300}?)(?=OBJETIVO|RESPONSABILIDAD|$)",
            "fecha_vigencia": r"(?:vigente|vigencia|aprobado)[^\d]*(\d{1,2}\s+de\s+\w+\s+de\s+\d{4}|\d{4}[\-/]\d{2})",
            "responsable_sgsi": r"(?:CISO|Responsable\s+de\s+Seguridad|Oficial)[\s:]+([A-ZÁÉÍÓÚÑ][^\n]{5,50})",
        },

        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "inventario_activos": {
        "nombre": "Inventario y Clasificación de Activos",
        "norma_ref": "ISO 27001:2022 Anexo A - Control 5.9",
        "descripcion": "Registro y clasificación de activos de información con sus propietarios y valoración.",

        "membrete": [
            "INVENTARIO", "ACTIVOS", "INFORMACION", "NIT", "EMPRESA",
            "CLASIFICACION"
        ],
        "membrete_minimo": 3,

        "secciones_requeridas": [
            "ACTIVO",
            "TIPO",              # Tipo de activo (hardware, software, datos, personas)
            "PROPIETARIO",       # Responsable del activo
            "CLASIFICACION",     # Confidencialidad del activo
            "VALOR",             # Valoración o criticidad
            "RESPONSABLE",
        ],
        "secciones_minimo": 4,

        "keywords_contenido": [
            "hardware", "software", "datos", "informacion", "servidor",
            "clasificacion", "confidencial", "critico", "propietario",
            "activo", "inventario", "red", "base de datos", "aplicacion"
        ],
        "keywords_contenido_minimo": 4,

        "reglas_especiales": [
            {
                "id": "categorias_activos",
                "descripcion": "Debe incluir al menos 2 categorías de activos (hardware, software, datos, personas, servicios)",
                "patron": r"(?:hardware|software|datos|personas|servicios|red|nube|documento)",
                "requerido": True,
                "puntos": 15,
                "minimo_matches": 2,
            }
        ],

        "campos_extraer": {
            "propietario": r"(?:propietario|responsable)[\s:]+([A-ZÁÉÍÓÚÑ][^\n]{5,50})",
            "total_activos": r"(?:total|numero\s+de\s+activos)[^\d]*(\d+)",
        },

        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "organigrama": {
        "nombre": "Organigrama Funcional",
        "norma_ref": "ISO 9001:2015 cláusula 5.3",
        "descripcion": "Estructura jerárquica y funcional de la organización.",

        "membrete": [
            "ORGANIGRAMA", "ESTRUCTURA", "EMPRESA", "NIT", "ORGANIZACIONAL"
        ],
        "membrete_minimo": 2,

        "secciones_requeridas": [
            "GERENCIA", "GERENTE",      # Nivel directivo máximo
            "AREA", "DEPARTAMENTO",     # Áreas funcionales
            "CARGO",                    # Cargos identificados
        ],
        "secciones_minimo": 2,

        "keywords_contenido": [
            "gerente", "director", "jefe", "coordinador", "supervisor",
            "area", "departamento", "cargo", "nivel", "reporte",
            "asistente", "operario", "tecnico", "analista"
        ],
        "keywords_contenido_minimo": 3,

        "nota_especial": "El organigrama puede ser una imagen. Si es imagen, validar que contenga nombres de cargos visibles.",

        "campos_extraer": {
            "nivel_maximo": r"(?:gerente|representante\s+legal|presidente|ceo)[\s:]+([A-ZÁÉÍÓÚÑ][^\n]{5,50})",
        },

        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "mapa_procesos": {
        "nombre": "Mapa de Procesos",
        "norma_ref": "ISO 9001:2015 cláusula 4.4",
        "descripcion": "Identificación e interacción de los procesos del sistema de gestión.",

        "membrete": [
            "MAPA DE PROCESOS", "PROCESOS", "EMPRESA", "NIT"
        ],
        "membrete_minimo": 2,

        "secciones_requeridas": [
            "PROCESO ESTRATEGICO",  # Nivel estratégico
            "PROCESO MISIONAL",     # Nivel misional / core
            "PROCESO APOYO",        # Nivel de soporte
            "CLIENTE",              # Input/output del cliente
            "INTERACCION",
        ],
        "secciones_minimo": 2,

        "keywords_contenido": [
            "proceso", "estrategico", "misional", "apoyo", "soporte",
            "cliente", "satisfaccion", "entrada", "salida", "interaccion",
            "gestion", "operativo"
        ],
        "keywords_contenido_minimo": 3,

        "campos_extraer": {
            "procesos_identificados": r"(?:proceso\s+de\s+)([A-ZÁÉÍÓÚÑA-Z][a-záéíóúña-z\s]{3,30})",
        },

        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "contexto_dofa": {
        "nombre": "Contexto Organizacional - Matriz DOFA",
        "norma_ref": "ISO 9001:2015 cláusula 4.1 / ISO 14001:2015 cláusula 4.1",
        "descripcion": "Análisis del contexto interno y externo de la organización.",

        "membrete": [
            "DOFA", "FODA", "CONTEXTO", "EMPRESA", "NIT", "ANALISIS"
        ],
        "membrete_minimo": 2,

        "secciones_requeridas": [
            "DEBILIDAD",    # D
            "OPORTUNIDAD",  # O
            "FORTALEZA",    # F
            "AMENAZA",      # A
        ],
        "secciones_minimo": 3,

        "keywords_contenido": [
            "interno", "externo", "estrategia", "mercado", "competencia",
            "tecnologia", "recursos", "personal", "financiero"
        ],
        "keywords_contenido_minimo": 3,

        "campos_extraer": {},
        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "matriz_ambiental": {
        "nombre": "Matriz de Aspectos e Impactos Ambientales",
        "norma_ref": "ISO 14001:2015 cláusula 6.1.2",
        "descripcion": "Identificación de aspectos ambientales significativos y sus impactos.",

        "membrete": [
            "MATRIZ", "ASPECTOS", "IMPACTOS", "AMBIENTAL", "NIT", "EMPRESA"
        ],
        "membrete_minimo": 3,

        "secciones_requeridas": [
            "ASPECTO AMBIENTAL",
            "IMPACTO AMBIENTAL",
            "SIGNIFICANCIA",    # O "EVALUACION"
            "CONTROL",
            "PROCESO",
        ],
        "secciones_minimo": 3,

        "keywords_contenido": [
            "agua", "aire", "suelo", "residuo", "energia", "vertimiento",
            "emision", "ruido", "contaminacion", "significativo",
            "ambiental", "criterio", "evaluacion", "impacto"
        ],
        "keywords_contenido_minimo": 4,

        "campos_extraer": {
            "proceso_fuente": r"proceso[\s:]+([A-ZÁÉÍÓÚÑ][^\n]{3,40})",
        },

        "puntuacion_maxima": 100,
    },

    # ──────────────────────────────────────────────────────────────────────
    "cronograma_auditoria": {
        "nombre": "Cronograma de Actividades de Auditoría",
        "norma_ref": "ISO 19011:2018 §6.3.2",
        "descripcion": "Programa de actividades y fechas del proceso de auditoría.",

        "membrete": [
            "CRONOGRAMA", "AUDITORIA", "EMPRESA", "NIT", "ACTIVIDADES"
        ],
        "membrete_minimo": 2,

        "secciones_requeridas": [
            "ACTIVIDAD",
            "FECHA",        # O "SEMANA" O "MES"
            "RESPONSABLE",
            "ESTADO",       # O "AVANCE"
        ],
        "secciones_minimo": 3,

        "keywords_contenido": [
            "auditoria", "fecha", "actividad", "responsable", "plazo",
            "entrega", "revision", "semana", "mes", "hito"
        ],
        "keywords_contenido_minimo": 3,

        "campos_extraer": {
            "fecha_inicio": r"(?:inicio|fecha\s+inicio)[^\d]*(\d{4}[\-/]\d{2}[\-/]\d{2}|\d{1,2}\s+de\s+\w+)",
            "fecha_fin": r"(?:fin|fecha\s+fin|entrega)[^\d]*(\d{4}[\-/]\d{2}[\-/]\d{2}|\d{1,2}\s+de\s+\w+)",
        },

        "puntuacion_maxima": 100,
    },
}


# ═══════════════════════════════════════════════════════════════════════════
#  MOTOR DE VALIDACIÓN
# ═══════════════════════════════════════════════════════════════════════════

def validate_document(text: str, doc_type: str) -> dict:
    """
    Valida el contenido de un documento contra su esquema.

    Args:
        text:     Texto extraído del documento (OCR o pdfplumber)
        doc_type: Clave del esquema en DOCUMENT_SCHEMAS

    Returns:
        dict con:
          - score: 0-100
          - nivel: "APROBADO" | "OBSERVACION" | "RECHAZADO"
          - cumplidos: Lista de requisitos cumplidos
          - faltantes: Lista de requisitos faltantes
          - campos_extraidos: Datos encontrados
          - informe: Texto del informe para el auditor
    """
    if doc_type not in DOCUMENT_SCHEMAS:
        return {
            "score": 0, "nivel": "RECHAZADO",
            "cumplidos": [], "faltantes": [f"Tipo '{doc_type}' no reconocido"],
            "campos_extraidos": {}, "informe": "Tipo de documento no definido en el motor."
        }

    schema = DOCUMENT_SCHEMAS[doc_type]
    text_upper = text.upper()
    cumplidos = []
    faltantes = []
    campos_extraidos = {}
    puntuacion = 0
    max_score = 100

    # ── 1. VERIFICACIÓN DE MEMBRETE / ENCABEZADO (15 puntos) ──────────────
    membrete_encontrados = [kw for kw in schema["membrete"] if kw in text_upper]
    minimo_membrete = schema.get("membrete_minimo", 2)
    puntos_membrete = 15

    if len(membrete_encontrados) >= minimo_membrete:
        puntuacion += puntos_membrete
        cumplidos.append(f"✅ Membrete/encabezado válido ({len(membrete_encontrados)}/{len(schema['membrete'])} indicadores)")
    else:
        faltantes.append(
            f"❌ Membrete incompleto — faltan indicadores de encabezado. "
            f"Encontrados: {membrete_encontrados}. "
            f"Esperados: {schema['membrete']}"
        )

    # ── 2. VERIFICACIÓN DE SECCIONES (40 puntos) ──────────────────────────
    secciones_req = schema["secciones_requeridas"]
    secciones_min = schema.get("secciones_minimo", len(secciones_req) // 2)
    secciones_encontradas = []
    secciones_faltantes = []

    for seccion in secciones_req:
        if seccion in text_upper:
            secciones_encontradas.append(seccion)
        else:
            secciones_faltantes.append(seccion)

    pct_secciones = len(secciones_encontradas) / max(len(secciones_req), 1)
    puntos_secciones = int(40 * pct_secciones)
    puntuacion += puntos_secciones

    if len(secciones_encontradas) >= secciones_min:
        cumplidos.append(
            f"✅ Secciones principales presentes ({len(secciones_encontradas)}/{len(secciones_req)}): "
            f"{', '.join(secciones_encontradas)}"
        )
    else:
        faltantes.append(
            f"❌ Secciones insuficientes ({len(secciones_encontradas)}/{len(secciones_req)} — mínimo {secciones_min}). "
            f"Faltan: {', '.join(secciones_faltantes)}"
        )

    # ── 3. VERIFICACIÓN DE CONTENIDO / PERTINENCIA (25 puntos) ───────────
    keywords_contenido = schema["keywords_contenido"]
    keywords_min = schema.get("keywords_contenido_minimo", 3)
    kw_encontrados = [kw for kw in keywords_contenido if kw in text_upper.lower()]

    pct_kw = min(1.0, len(kw_encontrados) / max(keywords_min, 1))
    puntos_kw = int(25 * pct_kw)
    puntuacion += puntos_kw

    if len(kw_encontrados) >= keywords_min:
        cumplidos.append(
            f"✅ Contenido pertinente verificado ({len(kw_encontrados)} términos clave encontrados)"
        )
    else:
        faltantes.append(
            f"❌ Contenido no pertinente al tipo de documento. "
            f"Solo {len(kw_encontrados)}/{keywords_min} términos clave detectados: {kw_encontrados}"
        )

    # ── 4. REGLAS ESPECIALES (variable, máx 20 puntos) ────────────────────
    reglas_especiales = schema.get("reglas_especiales", [])
    for regla in reglas_especiales:
        patron = regla.get("patron", "")
        flags = re.IGNORECASE | re.DOTALL
        matches = re.findall(patron, text, flags)

        min_matches = regla.get("minimo_matches", 1)
        cumple = len(matches) >= min_matches

        if cumple:
            puntuacion += regla.get("puntos", 10)
            cumplidos.append(f"✅ {regla['descripcion']}")
        else:
            if regla.get("requerido", False):
                faltantes.append(f"❌ CRÍTICO: {regla['descripcion']}")
            else:
                faltantes.append(f"⚠️ {regla['descripcion']} (recomendado)")

    # ── 5. EXTRACCIÓN DE CAMPOS ────────────────────────────────────────────
    for campo, patron in schema.get("campos_extraer", {}).items():
        m = re.search(patron, text, re.IGNORECASE | re.DOTALL)
        if m:
            valor = m.group(1).strip()
            valor = re.sub(r"\s+", " ", valor)[:200]
            campos_extraidos[campo] = valor

    # ── 6. NORMALIZACIÓN Y NIVEL ───────────────────────────────────────────
    puntuacion = min(100, puntuacion)

    if puntuacion >= 75:
        nivel = "APROBADO"
        nivel_emoji = "✅"
    elif puntuacion >= 50:
        nivel = "OBSERVACION"
        nivel_emoji = "⚠️"
    else:
        nivel = "RECHAZADO"
        nivel_emoji = "❌"

    # ── 7. GENERACIÓN DEL INFORME ──────────────────────────────────────────
    informe_lines = [
        f"═══════════════════════════════════════════════════",
        f"  VALIDACIÓN DOCUMENTAL HMO V15.0",
        f"  Documento: {schema['nombre']}",
        f"  Referencia normativa: {schema['norma_ref']}",
        f"═══════════════════════════════════════════════════",
        f"  RESULTADO: {nivel_emoji} {nivel}  |  Score: {puntuacion}/100",
        f"",
        f"📋 REQUISITOS CUMPLIDOS ({len(cumplidos)}):",
    ]
    for c in cumplidos:
        informe_lines.append(f"   {c}")

    if faltantes:
        informe_lines.append(f"")
        informe_lines.append(f"⚠️  REQUISITOS FALTANTES / OBSERVACIONES ({len(faltantes)}):")
        for f_ in faltantes:
            informe_lines.append(f"   {f_}")

    if campos_extraidos:
        informe_lines.append(f"")
        informe_lines.append(f"🔍 CAMPOS EXTRAÍDOS:")
        for k, v in campos_extraidos.items():
            informe_lines.append(f"   • {k}: {v[:80]}")

    informe_lines.append(f"")
    informe_lines.append(f"Descripción documento esperado: {schema['descripcion']}")

    return {
        "score": puntuacion,
        "nivel": nivel,
        "nivel_emoji": nivel_emoji,
        "doc_name": schema["nombre"],
        "norma_ref": schema["norma_ref"],
        "cumplidos": cumplidos,
        "faltantes": faltantes,
        "campos_extraidos": campos_extraidos,
        "informe": "\n".join(informe_lines),
        "secciones_encontradas": secciones_encontradas,
        "secciones_faltantes": secciones_faltantes,
    }


def detectar_tipo_por_contenido(text: str) -> str:
    """
    Detecta automáticamente el tipo de documento a partir del contenido
    cuando el usuario no especifica qué tipo está subiendo.
    """
    text_upper = text.upper()
    scores = {}

    for doc_type, schema in DOCUMENT_SCHEMAS.items():
        score = 0
        # Contar membrete hits
        score += sum(2 for kw in schema["membrete"] if kw in text_upper)
        # Contar sección hits
        score += sum(3 for sec in schema["secciones_requeridas"] if sec in text_upper)
        scores[doc_type] = score

    if not scores:
        return "desconocido"

    mejor = max(scores, key=scores.get)
    if scores[mejor] < 4:
        return "desconocido"
    return mejor


# Mapeo de nombres de expediente → key de esquema
EXPEDIENTE_A_SCHEMA = {
    "Camara de Comercio (Existencia Legal)": "camara_comercio",  # manejado por OCR_Extractor
    "RUT (Registro Unico Tributario)": "rut",                    # manejado por OCR_Extractor
    "Acta de Compromiso Directivo": "acta_compromiso",
    "Cronograma de Actividades de Preparacion": "cronograma_auditoria",
    "Mision y Vision Corporativa": "mision_vision",
    "Organigrama Funcional": "organigrama",
    "Mapa de Procesos": "mapa_procesos",
    "Manual de Funciones": "manual_funciones",
    "Estados Financieros": "estados_financieros",
    "Politica de Seguridad": "politica_seguridad",
    "Inventario de Activos": "inventario_activos",
    "Contexto Organizacional (DOFA)": "contexto_dofa",
    "Aspectos e Impactos Ambientales": "matriz_ambiental",
}
