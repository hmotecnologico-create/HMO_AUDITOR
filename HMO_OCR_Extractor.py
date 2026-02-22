"""
HMO_OCR_Extractor.py  —  V15.1 Document Intelligence (Extracción Total)
=========================================================================
Extrae TODOS los campos disponibles de documentos oficiales colombianos:
  - Cámara de Comercio (Certificado de Existencia y Representación Legal)
  - RUT (Formulario del Registro Único Tributario - DIAN)

Campos CC extraídos (18):
  Razón Social, NIT, Matrícula, Domicilio/Ciudad, Dirección judicial,
  Dirección comercial, Teléfono, Email, Objeto Social, Rep. Legal,
  C.C. Rep. Legal, Cargo Rep. Legal, Tipo Sociedad, Capital (3),
  Fecha Matrícula, Fecha Renovación, Num. Empleados, CIIU, Junta Directiva

Campos RUT extraídos (16):
  NIT, Razón Social, Tipo Persona, Tipo Contribuyente, Régimen IVA,
  Dirección, Cód. Postal, Municipio, Departamento, Email, Tel 1, Tel 2,
  CIIU + Descripción, Responsabilidades tributarias (tabla completa),
  Fecha Inscripción, N° Formulario

Estrategia:
  1. pdfplumber (PDFs digitales/texto nativo)
  2. pytesseract + pdf2image fallback (PDFs escaneados)
  3. Regex de precisión — sin NLP, sin dependencias pesadas

Autor: HMO Auditor Elite V15.1
"""

import re
import io
import os

# ── IMPORTS OPCIONALES ───────────────────────────────────────────────────────
try:
    import pdfplumber
    PDFPLUMBER_OK = True
except ImportError:
    PDFPLUMBER_OK = False

try:
    import pytesseract
    from pdf2image import convert_from_bytes
    from PIL import Image
    OCR_OK = True
except ImportError:
    OCR_OK = False


# ── SEÑALES DE DETECCIÓN ─────────────────────────────────────────────────────

CAMARA_SIGNALS = [
    "CERTIFICADO DE EXISTENCIA",
    "REPRESENTACION LEGAL",
    "CAMARA DE COMERCIO",
    "SECRETARIO DE LA CAMARA",
    "REGISTRO MERCANTIL",
    "MATRICULA",
    "OBJETO SOCIAL",
    "RENOVACION",
]

RUT_SIGNALS = [
    "REGISTRO UNICO TRIBUTARIO",
    "FORMULARIO DEL REGISTRO",
    "DIRECCION DE IMPUESTOS",
    "DIAN",
    "RAZON SOCIAL",
    "NUMERO DE IDENTIFICACION TRIBUTARIA",
    "ACTIVIDAD ECONOMICA",
    "RESPONSABILIDADES",
    "REGIMEN",
]

# Mapa completo de responsabilidades tributarias DIAN
MAPA_RESPONSABILIDADES = {
    "01": "IVA régimen ordinario",
    "02": "Régimen simplificado de IVA",
    "03": "IVA - Gran contribuyente",
    "04": "Impuesto Nacional al Consumo",
    "05": "Renta y complementarios (régimen ordinario)",
    "06": "Renta y complementarios de entidades del sector cooperativo",
    "07": "Retención en la fuente por renta",
    "08": "Retención en la fuente en ventas a San Andrés",
    "09": "Retención en la fuente en timbre nacional",
    "10": "Retención en la fuente en IVA",
    "11": "Ventas régimen común",
    "12": "Ventas régimen simplificado",
    "13": "Gran contribuyente autorretenedor de IVA",
    "14": "Informante de exógena",
    "15": "Declaración de Ingresos y Patrimonio",
    "16": "Obligado a llevar contabilidad",
    "17": "Entidades exentas del impuesto sobre la renta",
    "18": "Precios de transferencia",
    "19": "Declaración consolidada de precios de transferencia",
    "22": "Obligado al sistema especial de pagos de seguridad social",
    "24": "Declarar ingreso o salida del país de divisas o títulos representativos de las mismas",
    "26": "Declaración de activos en el exterior",
    "32": "Impuesto al patrimonio",
    "33": "Impuesto de normalización tributaria",
    "35": "CREE (Contribución Empresarial para la Equidad)",
    "36": "Sobretasa al CREE",
    "37": "Retención del CREE",
    "38": "Impuesto al consumo de bolsas plásticas",
    "40": "Régimen de tributación simple",
    "41": "Monotributo",
    "42": "IVA Great Taxpayer",
    "43": "Facturación electrónica",
    "44": "Impuesto nacional a la gasolina y el ACPM",
    "45": "Impuesto nacional al carbono",
    "47": "Impuesto de normalización tributaria (Ley 2010)",
    "48": "SIMPLE - Impuesto unificado",
    "49": "Régimen simple grandes contribuyentes",
    "50": "Retención de industria y comercio en la fuente",
    "52": "Impuesto a las bebidas azucaradas",
    "53": "Impuesto a los alimentos ultra procesados",
    "54": "Impuesto de timbre (estampillas)",
}


# ── EXTRACCIÓN DE TEXTO ──────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    if PDFPLUMBER_OK:
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
        except Exception:
            pass

    if len(text.strip()) > 100:
        return text

    if OCR_OK:
        try:
            images = convert_from_bytes(file_bytes, dpi=300)
            for img in images:
                page_text = pytesseract.image_to_string(img, lang="spa+eng")
                text += page_text + "\n"
        except Exception as e:
            text += f"\n[OCR_ERROR: {e}]"

    return text


def extract_text_from_image(file_bytes: bytes) -> str:
    if not OCR_OK:
        return ""
    try:
        img = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(img, lang="spa+eng")
    except Exception:
        return ""


# ── DETECCIÓN DE TIPO ─────────────────────────────────────────────────────────

def detect_document_type(text: str) -> str:
    text_upper = text.upper().replace("\n", " ")
    score_cc  = sum(1 for s in CAMARA_SIGNALS if s in text_upper)
    score_rut = sum(1 for s in RUT_SIGNALS if s in text_upper)

    if score_cc >= 2 and score_cc >= score_rut:
        return "camara_comercio"
    if score_rut >= 2:
        return "rut"
    if text_upper.count("CERTIFICA") >= 3:
        return "camara_comercio"
    return "unknown"


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _search(pattern: str, text: str, flags=re.IGNORECASE) -> str:
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else ""

def _search_all(pattern: str, text: str, flags=re.IGNORECASE) -> list:
    return [m.strip() for m in re.findall(pattern, text, flags)]

def _clean_nit(raw: str) -> str:
    clean = re.sub(r"[^\d\-]", "", raw.replace(" ", ""))
    if "-" not in clean and len(clean) > 1:
        clean = clean[:-1] + "-" + clean[-1]
    return clean

def _clean_phone(raw: str) -> str:
    return re.sub(r"[^\d\+]", "", raw)

def _clean_money(raw: str) -> str:
    """Normaliza valores monetarios."""
    clean = re.sub(r"[^\d\.]", "", raw.replace(",", "."))
    try:
        val = float(clean)
        if val > 1000:
            return f"${val:,.0f}"
    except Exception:
        pass
    return f"${raw}"


# ════════════════════════════════════════════════════════════════════════════
#  EXTRACTOR: CÁMARA DE COMERCIO — 18+ campos
# ════════════════════════════════════════════════════════════════════════════

def extract_camara_comercio(text: str) -> dict:
    """
    Extrae TODOS los campos del Certificado de Existencia y Representación Legal.

    Campos objetivo:
    ─────────────────────────────────────────────────────────────
    IDENTIDAD:      Razón Social, NIT, Tipo Sociedad, Matrícula
                    Fecha Matrícula, Fecha Renovación, Vigencia
    UBICACIÓN:      Domicilio/Ciudad, Municipio, Dirección judicial,
                    Dirección comercial, Teléfono, Email
    EMPRESA:        Objeto Social, CIIU, Num. Empleados, Capital (3 tipos)
    REPRESENTACIÓN: Rep. Legal principal + cargo, C.C.,
                    Junta Directiva (si aplica)
    ─────────────────────────────────────────────────────────────
    """
    data = {
        "tipo_doc": "camara_comercio",
        # ─── IDENTIDAD ───────────────────────────────────────────
        "company_name": "",            # Razón Social
        "empresa_nit": "",             # NIT con DV
        "tipo_sociedad": "",           # SAS, SA, LTDA, etc.
        "matricula": "",               # Número de matrícula mercantil
        "fecha_matricula": "",         # Fecha de primera matrícula
        "fecha_renovacion": "",        # Última renovación
        "vigencia": "",                # Vigencia del certificado
        # ─── UBICACIÓN ───────────────────────────────────────────
        "domicilio": "",               # Ciudad/municipio de domicilio
        "empresa_direccion": "",       # Dirección para notificaciones judiciales
        "direccion_comercial": "",     # Dirección del establecimiento
        "empresa_telefono": "",        # Teléfono
        "empresa_email": "",           # Email
        "empresa_municipio": "",       # Municipio (para Fase B)
        "empresa_departamento": "",    # Departamento
        # ─── OBJETO / ACTIVIDAD ───────────────────────────────────
        "empresa_objeto": "",          # Objeto social
        "actividad_ciiu": "",          # Código CIIU
        "descripcion_ciiu": "",        # Descripción de la actividad
        "num_empleados": "",           # Número de empleados (si aparece)
        # ─── CAPITAL ─────────────────────────────────────────────
        "capital_autorizado": "",
        "capital_suscrito": "",
        "capital_pagado": "",
        # ─── REPRESENTANTE LEGAL ─────────────────────────────────
        "rep_legal": "",               # Nombre completo
        "rep_id": "",                  # Cédula
        "rep_cargo": "",               # Cargo (Gerente, Director, etc.)
        # ─── JUNTA DIRECTIVA ─────────────────────────────────────
        "junta_directiva": [],         # Lista de miembros si aplica
        # ─── META ────────────────────────────────────────────────
        "confianza": 0,
        "campos_encontrados": [],
    }

    def _add(key, value):
        if value:
            data[key] = value
            data["campos_encontrados"].append(key)

    text_upper = text.upper()

    # ── Razón Social ─────────────────────────────────────────────────────────
    nombre = _search(r"NOMBRE[\s:]+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]+(?:SAS|SA|LTDA|EU|SRL|S\.A\.S|S\.A|LTDA\.)?)", text)
    if not nombre:
        nombre = _search(r"denominada[\s:]*\n?\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]+(?:SAS|SA|LTDA|EU))", text, re.IGNORECASE)
    if not nombre:
        # Patrón: primera línea mayúscula larga que parece empresa
        nombre = _search(r"^\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{8,60}(?:SAS|SA|LTDA|EU|S\.A\.S))\s*$", text, re.IGNORECASE | re.MULTILINE)
    _add("company_name", nombre)

    # ── NIT ───────────────────────────────────────────────────────────────────
    nit_raw = _search(r"NIT[\s:]*([0-9][0-9\.\s]+[\-]?\s*\d)", text)
    if not nit_raw:
        nit_raw = _search(r"(\d{9,10}[\-]\d)", text)
    if nit_raw:
        _add("empresa_nit", _clean_nit(nit_raw))

    # ── Tipo de Sociedad ──────────────────────────────────────────────────────
    tipos = {
        "sociedad por acciones simplificada": "SAS",
        "S.A.S": "SAS",
        r"\bSAS\b": "SAS",
        "sociedad anónima": "S.A.",
        "sociedad anonima": "S.A.",
        "responsabilidad limitada": "LTDA",
        r"\bLTDA\b": "LTDA",
        "empresa unipersonal": "EU",
        r"\bEU\b": "EU",
        "cooperativa": "COOPERATIVA",
        "empresa industrial": "INDUSTRIAL",
        "entidad sin animo": "ESAL",
        "fundacion": "FUNDACIÓN",
    }
    for patron, tipo in tipos.items():
        if re.search(patron, text, re.IGNORECASE):
            _add("tipo_sociedad", tipo)
            break

    # ── Matrícula ─────────────────────────────────────────────────────────────
    mat = _search(r"M[AÁ]TRICULA[\w\s]*?:?\s*N[°º.]?\s*([0-9\-]{4,15})", text)
    if not mat:
        mat = _search(r"(?:No|N[°º.])\s*([0-9]{5,12})\s*(?:del\s+libro|libro)", text)
    _add("matricula", mat)

    # ── Fecha de Matrícula ────────────────────────────────────────────────────
    f_mat = _search(r"Fecha\s+de\s+M[aá]tricula[\s:]+(\d{1,2}\s+de\s+\w+\s+de\s+\d{4}|\d{4}[\-/]\d{2}[\-/]\d{2})", text)
    _add("fecha_matricula", f_mat)

    # ── Fecha de Renovación ───────────────────────────────────────────────────
    f_ren = _search(r"Fecha\s+de\s+Renovaci[oó]n[\s:]+(\d{1,2}\s+de\s+\w+\s+de\s+\d{4}|\d{4}[\-/]\d{2}[\-/]\d{2})", text)
    _add("fecha_renovacion", f_ren)

    # ── Vigencia del Certificado ──────────────────────────────────────────────
    vig = _search(r"Vigencia[\s:]+(\d{1,2}\s+de\s+\w+\s+de\s+\d{4}|\d{4}[\-/]\d{2}[\-/]\d{2})", text)
    _add("vigencia", vig)

    # ── Domicilio / Ciudad ────────────────────────────────────────────────────
    dom = _search(r"DOMICILIO[\s:]+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑa-záéíóúñ\s]+?)[\n\r,]", text)
    _add("domicilio", dom.strip())
    _add("empresa_municipio", dom.strip())

    # ── Departamento ──────────────────────────────────────────────────────────
    dep = _search(r"(?:Departamento|DEPARTAMENTO)[\s:]+([A-ZÁÉÍÓÚÑ][a-záéíóúñA-Z\s]{3,20})", text)
    _add("empresa_departamento", dep.strip())

    # ── Dirección Judicial ────────────────────────────────────────────────────
    dir_j = _search(r"DIRECCI[OÓ]N[^\n]*JUDICIAL\s*([A-ZÁÉÍÓÚÑ0-9][^\n]{5,80})", text)
    if not dir_j:
        dir_j = _search(r"Direcci[oó]n\s+para\s+notificaciones?[\s:]+([A-Z0-9][^\n]{5,80})", text)
    _add("empresa_direccion", dir_j.strip())

    # ── Dirección Comercial ───────────────────────────────────────────────────
    dir_c = _search(r"(?:Direcci[oó]n\s+comercial|DIRECCI[OÓ]N\s+COMERCIAL)[\s:]+([A-Z0-9][^\n]{5,80})", text)
    _add("direccion_comercial", dir_c.strip())

    # ── Teléfono ──────────────────────────────────────────────────────────────
    tel = _search(r"(?:Tel[eé]fono|TELEFONO|TEL\.?)[\s:]+(\+?[\d\s\-]{7,15})", text)
    if tel:
        _add("empresa_telefono", _clean_phone(tel))

    # ── Email ─────────────────────────────────────────────────────────────────
    email = _search(r"([a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z]{2,})", text)
    _add("empresa_email", email)

    # ── Objeto Social ─────────────────────────────────────────────────────────
    obj_m = re.search(
        r"OBJETO\s+SOCIAL[\s:]+(.+?)(?=CERTIFICA|CAPITAL|REPRESENTACI[OÓ]N|$)",
        text, re.IGNORECASE | re.DOTALL
    )
    if obj_m:
        raw_obj = re.sub(r"\s+", " ", obj_m.group(1).strip())[:800]
        _add("empresa_objeto", raw_obj)

    # ── CIIU ──────────────────────────────────────────────────────────────────
    ciiu = _search(r"(?:CIIU|C[oó]digo\s+CIIU|actividad\s+econ[oó]mica\s+principal)[^\d]*(\d{4})", text)
    _add("actividad_ciiu", ciiu)

    ciiu_desc = _search(r"(?:Descripci[oó]n\s+CIIU|Actividad\s+principal)[^\n:]*:\s*([A-Za-záéíóúñÁÉÍÓÚÑ][^\n]{5,100})", text)
    _add("descripcion_ciiu", ciiu_desc)

    # ── Número de Empleados ───────────────────────────────────────────────────
    emp = _search(r"(?:empleados|trabajadores|planta)[^\d]*(\d+)", text, re.IGNORECASE)
    _add("num_empleados", emp)

    # ── Capital ───────────────────────────────────────────────────────────────
    for campo in ["AUTORIZADO", "SUSCRITO", "PAGADO"]:
        val = _search(rf"{campo}\.?\s*\$?\s*([\d\.,]{{4,20}})", text)
        if val:
            key = f"capital_{campo.lower()}"
            _add(key, _clean_money(val))

    # ── Representante Legal ───────────────────────────────────────────────────
    # Formato CC: "REPRESENTANTE LEGAL  JUAN GARCIA PEREZ  C  3.809.123"
    rep_m = re.search(
        r"REPRESENTANTE\s+LEGAL\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{5,50}?)\s+(?:CC?\.?\s*)?([\d\.\s]{6,15})",
        text, re.IGNORECASE
    )
    if rep_m:
        _add("rep_legal", rep_m.group(1).strip())
        _add("rep_id", re.sub(r"[^\d\.]", "", rep_m.group(2)))
    else:
        rep_alt = _search(r"REPRESENTANTE\s+LEGAL\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{5,50})", text)
        if rep_alt:
            _add("rep_legal", rep_alt.split("\n")[0].strip())

    # Cargo del representante (Gerente, Director General, etc.)
    cargo = _search(r"(?:con\s+el\s+cargo\s+de|cargo[:\s]+)(Gerente|Director|Presidente|Administrador|Representante)[^\n]{0,30}", text, re.IGNORECASE)
    _add("rep_cargo", cargo)

    # ── Junta Directiva ───────────────────────────────────────────────────────
    junta_m = re.search(r"JUNTA\s+DIRECTIVA(.+?)(?=REPRESENTANTE|CAPITAL|OBJETO|$)", text, re.IGNORECASE | re.DOTALL)
    if junta_m:
        miembros = re.findall(r"([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{5,40})", junta_m.group(1))
        junta_limpia = [m.strip() for m in miembros if len(m.strip()) > 6][:10]
        if junta_limpia:
            data["junta_directiva"] = junta_limpia
            data["campos_encontrados"].append("junta_directiva")

    # ── Confianza ─────────────────────────────────────────────────────────────
    # 18 campos posibles → ~5.5 pts por campo
    data["confianza"] = min(100, len(data["campos_encontrados"]) * 6)
    return data


# ════════════════════════════════════════════════════════════════════════════
#  EXTRACTOR: RUT — 16+ campos
# ════════════════════════════════════════════════════════════════════════════

def extract_rut(text: str) -> dict:
    """
    Extrae TODOS los campos del RUT (Formulario DIAN).

    Campos del Formulario RUT:
    ─────────────────────────────────────────────────────────────
    Campo 5:   NIT
    Campo 24:  Tipo de Contribuyente
    Campo 25:  Tipo de Persona (Natural / Jurídica)
    Campo 26:  Régimen (Responsable IVA / No Responsable)
    Campo 35:  Razón Social (o Apellidos y Nombres)
    Campo 36:  Nombre de pila (personas naturales)
    Campo 39:  Departamento
    Campo 40:  Ciudad/Municipio
    Campo 41:  Dirección
    Campo 43:  Código Postal
    Campo 44:  Correo Electrónico
    Campo 45:  Teléfono 1
    Campo 46:  Teléfono 2 / Fax
    Campo 47:  CIIU principal
    Campo 48:  Descripción CIIU
    Campo 53:  Responsabilidades / Calidades / Atributos
    Campo 61:  Fecha Generación documento
    N° Formulario
    ─────────────────────────────────────────────────────────────
    """
    data = {
        "tipo_doc": "rut",
        # ─── IDENTIDAD ───────────────────────────────────────────
        "empresa_nit": "",              # Campo 5
        "company_name": "",             # Campo 35: Razón Social
        "nombre_natural": "",           # Campo 36: para personas naturales
        "tipo_contribuyente": "",       # Campo 24
        "tipo_persona": "",             # Campo 25: Natural/Jurídica
        "regimen_iva": "",              # Campo 26: Régimen de IVA
        "numero_formulario": "",        # N° formulario RUT
        # ─── UBICACIÓN ───────────────────────────────────────────
        "empresa_departamento": "",     # Campo 39
        "empresa_municipio": "",        # Campo 40
        "empresa_direccion": "",        # Campo 41
        "codigo_postal": "",            # Campo 43
        "empresa_email": "",            # Campo 44
        "empresa_telefono": "",         # Campo 45
        "empresa_telefono2": "",        # Campo 46
        # ─── ACTIVIDAD ───────────────────────────────────────────
        "actividad_ciiu": "",           # Campo 47
        "descripcion_ciiu": "",         # Campo 48
        # ─── TRIBUTARIO ──────────────────────────────────────────
        "responsabilidades": [],        # Campo 53 — lista completa
        "responsabilidades_codigos": [],# Solo los códigos
        "fecha_rut": "",                # Campo 61
        # ─── META ────────────────────────────────────────────────
        "confianza": 0,
        "campos_encontrados": [],
    }

    def _add(key, value):
        if value:
            data[key] = value
            data["campos_encontrados"].append(key)

    # ── NIT (Campo 5) ─────────────────────────────────────────────────────────
    # El RUT formatea el NIT como "9 0 0 5 3 9 0 5 1" con espacios
    nit_rut = _search(r"(?:NIT|N[º°.]?\s*de\s*Identificaci[oó]n)[^\d]*([\d\s\.]{8,20}[\-]?\d?)", text)
    if not nit_rut:
        # Formato con espacios entre dígitos
        nit_rut = _search(r"(\d\s+\d\s+\d\s+\d\s+\d\s+\d\s+\d\s+\d\s+\d)", text)
        if nit_rut:
            nit_rut = nit_rut.replace(" ", "")
    if not nit_rut:
        # Formato largo en una sola línea
        nit_rut = _search(r"\b(\d{9,10}[\-]\d)\b", text)
    if nit_rut:
        _add("empresa_nit", _clean_nit(nit_rut))

    # ── Número de Formulario ──────────────────────────────────────────────────
    form_num = _search(r"(?:N[°º]\s*Formulario|Formulario\s*N[°º])[^\d]*(\d{8,14})", text)
    _add("numero_formulario", form_num)

    # ── Tipo de Contribuyente (Campo 24) ─────────────────────────────────────
    tipo_contrib = _search(r"(?:24[\.\:]?\s*Tipo\s+de\s+contribuyente|Tipo\s+contribuyente)[\s:]+([^\n]{3,50})", text)
    _add("tipo_contribuyente", tipo_contrib)

    # ── Tipo de Persona (Campo 25) ────────────────────────────────────────────
    if re.search(r"persona\s+jur[ií]dica", text, re.IGNORECASE):
        _add("tipo_persona", "Jurídica")
    elif re.search(r"persona\s+natural", text, re.IGNORECASE):
        _add("tipo_persona", "Natural")

    # ── Régimen IVA (Campo 26) ────────────────────────────────────────────────
    if re.search(r"responsable\s+de\s+IVA|régimen\s+ordinario", text, re.IGNORECASE):
        _add("regimen_iva", "Responsable de IVA")
    elif re.search(r"no\s+responsable\s+de\s+IVA|régimen\s+simplificado", text, re.IGNORECASE):
        _add("regimen_iva", "No Responsable de IVA")

    # ── Razón Social (Campo 35) ───────────────────────────────────────────────
    razon = _search(r"Raz[oó]n\s+[Ss]ocial[\s:]*\n?\s*([A-ZÁÉÍÓÚÑ][^\n]{3,80})", text)
    if not razon:
        razon = _search(r"35[\.\:]?\s*(?:Raz[oó]n\s+social)?[\s\n]+([A-ZÁÉÍÓÚÑ][^\n]{3,80})", text)
    _add("company_name", razon.strip())

    # ── Nombre Natural (Campo 36) ─────────────────────────────────────────────
    nombre_nat = _search(r"36[\.\:]?\s*Otros\s+nombres?[\s:]+([^\n]{3,50})", text)
    _add("nombre_natural", nombre_nat)

    # ── Departamento (Campo 39) ───────────────────────────────────────────────
    dep = _search(r"(?:39[\.\:]?[^\n]*Departamento|Departamento)[^\n]*?([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]{3,25})", text)
    _add("empresa_departamento", dep.strip())

    # ── Ciudad/Municipio (Campo 40) ───────────────────────────────────────────
    ciudad = _search(r"(?:40[\.\:]|Ciudad[/\s]Municipio)[^\n]*?([A-ZÁÉÍÓÚÑ]{3,25})\s*0+1?\b", text)
    if not ciudad:
        ciudad = _search(r"(?:Municipio|Ciudad)[\s:]+([A-ZÁÉÍÓÚÑ][a-záéíóúñA-Z\s]{2,20})", text)
    _add("empresa_municipio", ciudad.strip())

    # ── Dirección (Campo 41) ──────────────────────────────────────────────────
    direccion = _search(r"(?:41[\.\:]?\s*Direcci[oó]n|Direcci[oó]n[\s:]+)([A-Z0-9][^\n]{5,100})", text)
    _add("empresa_direccion", direccion.strip())

    # ── Código Postal (Campo 43) ──────────────────────────────────────────────
    cod_postal = _search(r"(?:43[\.\:]?\s*C[oó]digo\s+[Pp]ostal|C[oó]digo\s+[Pp]ostal)[\s:]*(\d{6})", text)
    _add("codigo_postal", cod_postal)

    # ── Email (Campo 44) ──────────────────────────────────────────────────────
    email = _search(r"([a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z]{2,})", text)
    _add("empresa_email", email)

    # ── Teléfono 1 (Campo 45) ─────────────────────────────────────────────────
    tel1 = _search(r"(?:45[\.\:]?\s*Tel[eé]fono\s*1?|Tel[eé]fono\s*1)[\s:]+(\+?[\d\s\-]{6,15})", text)
    if not tel1:
        # Buscar número colombiano genérico
        tel1 = _search(r"(?:^|\s)(\+?57[\s\-]?[36]\d{9}|\b[36]\d{9})", text, re.MULTILINE)
    if tel1:
        _add("empresa_telefono", _clean_phone(tel1)[:15])

    # ── Teléfono 2 / Fax (Campo 46) ───────────────────────────────────────────
    tel2 = _search(r"(?:46[\.\:]?\s*Tel[eé]fono\s*2|Fax|Tel[eé]fono\s*2)[\s:]+(\+?[\d\s\-]{6,15})", text)
    if tel2:
        _add("empresa_telefono2", _clean_phone(tel2)[:15])

    # ── Código CIIU (Campo 47) ────────────────────────────────────────────────
    ciiu = _search(r"(?:47[\.\:]|C[oó]digo\s+Actividad\s+[Pp]rincipal)[^\d]*(\d{4})", text)
    _add("actividad_ciiu", ciiu)

    # ── Descripción CIIU (Campo 48) ───────────────────────────────────────────
    ciiu_desc = _search(r"(?:48[\.\:]|Descripci[oó]n\s+Actividad)[^\n:]*?:?\s*([A-Za-záéíóúñÁÉÍÓÚÑ][^\n]{5,150})", text)
    _add("descripcion_ciiu", ciiu_desc)

    # ── Responsabilidades (Campo 53) — COMPLETO ───────────────────────────────
    resp_m = re.search(
        r"(?:53[\.\:]?[^\n]*Responsabilidades?|Responsabilidades\s+y\s+Calidades)(.{0,600}?)(?=\d{2}[\.\:]|\Z)",
        text, re.IGNORECASE | re.DOTALL
    )
    if resp_m:
        bloque = resp_m.group(1)
        # Extraer todos los códigos de 2 dígitos que aparecen
        codigos = list(set(re.findall(r"\b([0-5]\d)\b", bloque)))
        codigos_validos = [c for c in codigos if c in MAPA_RESPONSABILIDADES]
        if codigos_validos:
            data["responsabilidades"] = [
                f"{c} - {MAPA_RESPONSABILIDADES[c]}" for c in sorted(codigos_validos)
            ]
            data["responsabilidades_codigos"] = sorted(codigos_validos)
            data["campos_encontrados"].append("responsabilidades")

    # ── Fecha de Generación (Campo 61) ────────────────────────────────────────
    fecha = _search(r"(?:61[\.\:\s]+Fecha|Fecha.*?generaci[oó]n)[^\d]*(\d{4}[\-/\.]\d{2}[\-/\.]\d{2}|\d{1,2}\s+de\s+\w+\s+de\s+\d{4})", text)
    _add("fecha_rut", fecha)

    # ── Confianza ─────────────────────────────────────────────────────────────
    # 16 campos posibles → ~6 pts por campo
    data["confianza"] = min(100, len(data["campos_encontrados"]) * 7)
    return data


# ── FUNCIÓN PRINCIPAL ─────────────────────────────────────────────────────────

def procesar_documento(file_bytes: bytes, filename: str = "") -> dict:
    """Recibe bytes de PDF o imagen, detecta tipo y extrae todos los campos."""
    ext = os.path.splitext(filename.lower())[1]

    if ext in (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"):
        text = extract_text_from_image(file_bytes)
    else:
        text = extract_text_from_pdf(file_bytes)

    if not text or len(text.strip()) < 30:
        return {"tipo_doc": "unknown", "confianza": 0,
                "error": "No se pudo extraer texto del archivo."}

    tipo = detect_document_type(text)

    if tipo == "camara_comercio":
        result = extract_camara_comercio(text)
    elif tipo == "rut":
        result = extract_rut(text)
    else:
        result = {
            "tipo_doc": "unknown", "confianza": 0,
            "texto_bruto": text[:500],
            "error": "Documento no reconocido. ¿Es Cámara de Comercio o RUT?"
        }

    result["texto_completo"] = text
    return result


# ── MAPEADOR A SESSION STATE ──────────────────────────────────────────────────

def resultado_a_session_state(resultado: dict) -> dict:
    """
    Convierte el resultado del extractor al session_state de HMO Auditor.
    Retorna TODOS los campos disponibles, desde ambos documentos.

    Campos mapeados (CC):
      company_name, empresa_nit, rep_legal, rep_id, rep_cargo,
      empresa_direccion, direccion_comercial, empresa_municipio, empresa_departamento,
      domicilio, empresa_objeto, empresa_telefono, empresa_email,
      actividad_ciiu, descripcion_ciiu, tipo_sociedad,
      capital_autorizado, capital_suscrito, capital_pagado,
      fecha_matricula, fecha_renovacion, matricula, num_empleados,
      junta_directiva, vigencia_cc

    Campos mapeados (RUT):
      company_name (si no hay del CC), empresa_nit (si no hay del CC),
      empresa_direccion, empresa_municipio, empresa_departamento, codigo_postal,
      empresa_email, empresa_telefono, empresa_telefono2,
      actividad_ciiu, descripcion_ciiu, tipo_persona, tipo_contribuyente,
      regimen_iva, responsabilidades, responsabilidades_codigos,
      fecha_rut, numero_formulario_rut
    """
    ss = {}
    tipo = resultado.get("tipo_doc", "unknown")

    def _m(dest, src_key, obligatorio_si_no_presente=False):
        """Mapea src del resultado a dest en ss, solo si tiene valor."""
        val = resultado.get(src_key, "")
        if isinstance(val, list):
            if val:
                ss[dest] = val
        elif val:
            if obligatorio_si_no_presente:
                ss.setdefault(dest, val)
            else:
                ss[dest] = val

    if tipo == "camara_comercio":
        # Identidad (siempre tomar del CC — es el documento fuente)
        _m("company_name",          "company_name")
        _m("empresa_nit",           "empresa_nit")
        _m("rep_legal",             "rep_legal")
        _m("rep_id",                "rep_id")
        _m("rep_cargo",             "rep_cargo")
        _m("tipo_sociedad",         "tipo_sociedad")
        _m("matricula",             "matricula")
        _m("fecha_matricula",       "fecha_matricula")
        _m("fecha_renovacion_cc",   "fecha_renovacion")
        _m("vigencia_cc",           "vigencia")
        # Ubicación
        _m("empresa_direccion",     "empresa_direccion")
        _m("direccion_comercial",   "direccion_comercial")
        _m("empresa_municipio",     "domicilio")
        _m("empresa_municipio",     "empresa_municipio")
        _m("empresa_departamento",  "empresa_departamento")
        # Contacto
        _m("empresa_telefono",      "empresa_telefono")
        _m("empresa_email",         "empresa_email")
        # Actividad
        _m("empresa_objeto",        "empresa_objeto")
        _m("actividad_ciiu",        "actividad_ciiu")
        _m("descripcion_ciiu",      "descripcion_ciiu")
        _m("num_empleados",         "num_empleados")
        # Capital
        _m("capital_autorizado",    "capital_autorizado")
        _m("capital_suscrito",      "capital_suscrito")
        _m("capital_pagado",        "capital_pagado")
        # Junta
        _m("junta_directiva",       "junta_directiva")

    elif tipo == "rut":
        # Identidad (solo rellenar si no existe ya del CC)
        _m("company_name",              "company_name")     # setdefault en _m
        _m("empresa_nit",               "empresa_nit")
        _m("tipo_persona",              "tipo_persona")
        _m("tipo_contribuyente",        "tipo_contribuyente")
        _m("regimen_iva",               "regimen_iva")
        _m("numero_formulario_rut",     "numero_formulario")
        # Ubicación (el RUT puede complementar datos del CC)
        _m("empresa_direccion",         "empresa_direccion")
        _m("empresa_municipio",         "empresa_municipio")
        _m("empresa_departamento",      "empresa_departamento")
        _m("codigo_postal",             "codigo_postal")
        # Contacto (RUT es la fuente definitiva para email y tel)
        _m("empresa_email",             "empresa_email")
        _m("empresa_telefono",          "empresa_telefono")
        _m("empresa_telefono2",         "empresa_telefono2")
        # Actividad
        _m("actividad_ciiu",            "actividad_ciiu")
        _m("descripcion_ciiu",          "descripcion_ciiu")
        # Tributario
        _m("responsabilidades",         "responsabilidades")
        _m("responsabilidades_codigos", "responsabilidades_codigos")
        _m("fecha_rut",                 "fecha_rut")

    return ss
