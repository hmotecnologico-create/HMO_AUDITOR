"""
HMO_OCR_Extractor.py  —  V14.0 Document Intelligence
=======================================================
Extrae datos estructurados de documentos oficiales colombianos:
  - Cámara de Comercio (Certificado de Existencia y Representación)
  - RUT (Formulario del Registro Único Tributario - DIAN)

Estrategia:
  1. Extracción de texto con pdfplumber (PDFs digitales/texto nativo)
  2. Fallback OCR con pytesseract + pdf2image (PDFs escaneados)
  3. Extracción de campos con regex sin NLP (estructura fija de dctos. colombianos)

Autor: HMO Auditor Elite V14.0
"""

import re
import io
import os

# ── IMPORTS OPCIONALES (pueden no estar instalados) ─────────────────────────
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

# ── CONSTANTES DE VALIDACIÓN ────────────────────────────────────────────────
# Patrones que identifican inequívocamente cada tipo de documento

CAMARA_SIGNALS = [
    "CERTIFICADO DE EXISTENCIA",
    "REPRESENTACION LEGAL",
    "CAMARA DE COMERCIO",
    "CAMARA DE COMERCIO DE",
    "SECRETARIO DE LA CAMARA",
    "REGISTRO MERCANTIL",
    "MATRICULA",
    "OBJETO SOCIAL",
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
]


# ── EXTRACCIÓN DE TEXTO ─────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extrae texto de un PDF.
    Intenta pdfplumber primero (más preciso para PDFs digitales).
    Si no extrae suficiente texto, usa pytesseract (OCR para escaneados).
    """
    text = ""

    # Intento 1: pdfplumber (texto nativo)
    if PDFPLUMBER_OK:
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
        except Exception:
            pass

    # Si pdfplumber extrajo suficiente texto, lo usamos
    if len(text.strip()) > 100:
        return text

    # Intento 2: OCR con pytesseract (PDFs escaneados como los del usuario)
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
    """Extrae texto de una imagen (JPG, PNG, etc.)"""
    if not OCR_OK:
        return ""
    try:
        img = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(img, lang="spa+eng")
    except Exception:
        return ""


# ── DETECCIÓN DE TIPO DE DOCUMENTO ──────────────────────────────────────────

def detect_document_type(text: str) -> str:
    """
    Detecta si el texto corresponde a:
      - 'camara_comercio'
      - 'rut'
      - 'unknown'
    """
    text_upper = text.upper().replace("\n", " ")

    score_cc  = sum(1 for s in CAMARA_SIGNALS if s in text_upper)
    score_rut = sum(1 for s in RUT_SIGNALS if s in text_upper)

    if score_cc >= 2 and score_cc >= score_rut:
        return "camara_comercio"
    if score_rut >= 2:
        return "rut"
    # Heurística adicional: presencia de "CERTIFICA" múltiples veces → CC
    if text_upper.count("CERTIFICA") >= 3:
        return "camara_comercio"
    return "unknown"


# ── HELPERS DE REGEX ────────────────────────────────────────────────────────

def _search(pattern: str, text: str, flags=re.IGNORECASE) -> str:
    """Busca un patrón y devuelve el primer grupo capturado, o ''."""
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else ""


def _clean_nit(raw: str) -> str:
    """Normaliza un NIT: 900539051-5 o 900.539.051-5"""
    # Elimina espacios internos y puntos extra
    clean = re.sub(r"[^\d\-]", "", raw.replace(" ", ""))
    # Asegura formato con dígito de verificación
    if "-" not in clean and len(clean) > 1:
        clean = clean[:-1] + "-" + clean[-1]
    return clean


# ── EXTRACTOR: CÁMARA DE COMERCIO ───────────────────────────────────────────

def extract_camara_comercio(text: str) -> dict:
    """
    Extrae campos clave del Certificado de Existencia y Representación.

    Estructura esperada (Cámara de Comercio colombiana):
    NOMBRE:          [Razón Social]
    MATRICULA:       [Número de matrícula]
    DOMICILIO:       [Ciudad]
    NIT              [número]-[DV]
    OBJETO SOCIAL:   [Texto libre]
    REPRESENTANTE LEGAL  [Nombre]  [C.C.]
    CAPITAL AUTORIZADO / SUSCRITO / PAGADO
    Fecha de Renovación: [Fecha]
    """
    data = {
        "tipo_doc": "camara_comercio",
        "company_name": "",
        "empresa_nit": "",
        "domicilio": "",
        "matricula": "",
        "empresa_objeto": "",
        "rep_legal": "",
        "rep_id": "",
        "empresa_direccion": "",
        "capital_autorizado": "",
        "capital_suscrito": "",
        "capital_pagado": "",
        "fecha_renovacion": "",
        "tipo_sociedad": "",
        "vigencia": "",
        "confianza": 0,   # 0-100
        "campos_encontrados": [],
    }

    # -- Nombre / Razón Social --
    # Varias variantes: "NOMBRE: HEYMOL..." o texto destacado después de cabecera
    nombre = _search(r"NOMBRE[\s:]+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]+(?:SAS|SA|LTDA|EU|SRL|AND CIA|S\.A\.S|S\.A|LTDA\.)?)", text)
    if not nombre:
        # Buscar en las primeras apariciones del nombre en el doc
        nombre = _search(r"denominada[\s:]*\n?\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]+(?:SAS|SA|LTDA|EU))", text, re.IGNORECASE)
    data["company_name"] = nombre
    if nombre:
        data["campos_encontrados"].append("company_name")

    # -- NIT --
    nit_raw = _search(r"NIT[\s:]*([0-9][0-9\.\s]+[\-]?\s*\d)", text)
    if not nit_raw:
        nit_raw = _search(r"(\d{9,10}[\-]\d)", text)
    data["empresa_nit"] = _clean_nit(nit_raw)
    if data["empresa_nit"]:
        data["campos_encontrados"].append("empresa_nit")

    # -- Matrícula --
    mat = _search(r"MATRICULA[\s:]+([0-9\-]+)", text)
    data["matricula"] = mat
    if mat:
        data["campos_encontrados"].append("matricula")

    # -- Domicilio --
    dom = _search(r"DOMICILIO[\s:]+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑa-záéíóúñ\s]+?)[\n\r]", text)
    data["domicilio"] = dom.strip()
    if dom:
        data["campos_encontrados"].append("domicilio")

    # -- Objeto Social --
    objeto_m = re.search(
        r"OBJETO\s+SOCIAL[\s:]+(.+?)(?:CERTIFICA|CAPITAL|REPRESENTACION|$)",
        text, re.IGNORECASE | re.DOTALL
    )
    if objeto_m:
        raw_obj = objeto_m.group(1).strip()
        # Limpiar saltos de línea y espacios múltiples
        data["empresa_objeto"] = re.sub(r"\s+", " ", raw_obj)[:600]
        data["campos_encontrados"].append("empresa_objeto")

    # -- Representante Legal --
    # Patrón: "REPRESENTANTE LEGAL    HEYDER MEDRANO OLIER    C    3.809..."
    rep_m = re.search(
        r"REPRESENTANTE\s+LEGAL\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]+?)\s+C\s+([\d\.]+)",
        text, re.IGNORECASE
    )
    if rep_m:
        data["rep_legal"] = rep_m.group(1).strip()
        data["rep_id"] = rep_m.group(2).strip()
        data["campos_encontrados"].extend(["rep_legal", "rep_id"])
    else:
        # Fallback: buscar solo el nombre del representante
        rep_alt = _search(r"REPRESENTANTE\s+LEGAL\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{5,50})", text)
        if rep_alt:
            data["rep_legal"] = rep_alt.split("\n")[0].strip()
            data["campos_encontrados"].append("rep_legal")

    # -- Dirección para notificación --
    dir_m = _search(
        r"DIRECCI[OÓ]N[\w\s]*JUDICIAL\s*([A-ZÁÉÍÓÚÑ0-9][^\n]+)",
        text
    )
    if dir_m:
        data["empresa_direccion"] = dir_m.strip()
        data["campos_encontrados"].append("empresa_direccion")

    # -- Capital --
    for campo in ["AUTORIZADO", "SUSCRITO", "PAGADO"]:
        val = _search(rf"{campo}\s+\$([\d\.,]+)", text)
        if val:
            key = f"capital_{campo.lower()}"
            data[key] = f"${val}"
            data["campos_encontrados"].append(key)

    # -- Fecha de renovación --
    fecha = _search(r"Fecha de Renovaci[oó]n[\s:]+([A-Za-záéíóúñ0-9\s]+\d{4})", text)
    data["fecha_renovacion"] = fecha.strip()
    if fecha:
        data["campos_encontrados"].append("fecha_renovacion")

    # -- Tipo de sociedad --
    for tipo in ["sociedad por acciones simplificadas", "SAS", "sociedad anonima",
                 "responsabilidad limitada", "empresa unipersonal"]:
        if tipo.upper() in text.upper():
            data["tipo_sociedad"] = tipo.upper().replace(
                "SOCIEDAD POR ACCIONES SIMPLIFICADAS", "SAS")
            break

    # -- Confianza --
    data["confianza"] = min(100, len(data["campos_encontrados"]) * 14)
    return data


# ── EXTRACTOR: RUT ──────────────────────────────────────────────────────────

def extract_rut(text: str) -> dict:
    """
    Extrae campos del RUT (Formulario DIAN).

    Campos del formulario:
      5.  NIT
      35. Razón Social
      41. Dirección
      42. Correo electrónico
      44. Teléfono 1
      46. Actividad económica principal (CIIU)
      53. Responsabilidades
    """
    data = {
        "tipo_doc": "rut",
        "company_name": "",
        "empresa_nit": "",
        "empresa_direccion": "",
        "email": "",
        "telefono": "",
        "ciudad": "",
        "departamento": "",
        "actividad_ciiu": "",
        "responsabilidades": [],
        "fecha_rut": "",
        "confianza": 0,
        "campos_encontrados": [],
    }

    # -- NIT (Campo 5) --
    # Formato en RUT: "9 0 0 5 3 9 0 5 1" con espacios entre dígitos
    nit_rut = _search(r"(?:NIT|N[º°.]?\s*de\s*Identificaci[oó]n)[^\d]*([\d\s\.]{8,15}[\-]?\d?)", text)
    if not nit_rut:
        # Buscar secuencia numérica separada por espacios estilo DIAN
        nit_rut = _search(r"(\d\s+\d\s+\d\s+\d\s+\d\s+\d\s+\d\s+\d\s+\d)", text)
        if nit_rut:
            nit_rut = nit_rut.replace(" ", "")
    data["empresa_nit"] = _clean_nit(nit_rut) if nit_rut else ""
    if data["empresa_nit"]:
        data["campos_encontrados"].append("empresa_nit")

    # -- Razón Social (Campo 35) --
    razon = _search(r"Raz[oó]n\s+[Ss]ocial[\s:]*\n?([A-ZÁÉÍÓÚÑ][^\n]{3,60})", text)
    if not razon:
        # Buscar por posición: la línea después del label en el formulario
        razon = _search(r"35[\.:]?\s*Raz[oó]n\s+social[\s\n]+([A-ZÁÉÍÓÚÑ][^\n]{3,60})", text)
    data["company_name"] = razon.strip()
    if razon:
        data["campos_encontrados"].append("company_name")

    # -- Dirección (Campo 41) --
    direccion = _search(r"(?:41[\.:]?\s*Direcci[oó]n|Direcci[oó]n[\s:]+)([A-Z0-9][^\n]{5,80})", text)
    data["empresa_direccion"] = direccion.strip()
    if direccion:
        data["campos_encontrados"].append("empresa_direccion")

    # -- Email (Campo 42) --
    email = _search(r"([a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z]{2,})", text)
    data["email"] = email
    if email:
        data["campos_encontrados"].append("email")

    # -- Teléfono (Campo 44) --
    tel = _search(r"(?:Tel[eé]fono\s*1?[\s:]+|44[\.:\s]+)(\d[\d\s]{5,12})", text)
    data["telefono"] = tel.replace(" ", "").strip() if tel else ""
    if data["telefono"]:
        data["campos_encontrados"].append("telefono")

    # -- Ciudad (Campo 40) --
    ciudad = _search(r"(?:Ciudad[\s/]Municipio|40[\.:])[^\n]*?([A-ZÁÉÍÓÚÑ]{3,20})\s+0+1\b", text)
    if not ciudad:
        ciudad = _search(r"(?:Ciudad[\s/]Municipio|Ciudad)[\s:]+([A-ZÁÉÍÓÚÑ][a-záéíóúñA-Z\s]{2,20})", text)
    data["ciudad"] = ciudad.strip()
    if ciudad:
        data["campos_encontrados"].append("ciudad")

    # -- Departamento (Campo 39) --
    dep = _search(r"(?:Departamento|39[\.:])[^\n]*?([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]{3,20})", text)
    data["departamento"] = dep.strip()
    if dep:
        data["campos_encontrados"].append("departamento")

    # -- Actividad CIIU (Campo 46) --
    ciiu = _search(r"(?:46[\.:]|C[oó]digo[\s:]+Actividad\s+(?:principal)?)\s*(\d{4})", text)
    data["actividad_ciiu"] = ciiu
    if ciiu:
        data["campos_encontrados"].append("actividad_ciiu")

    # -- Responsabilidades tributarias (Campo 53) --
    # En el RUT aparecen como series de números pequeños (05,07,11,14,35...)
    resp_section = re.search(r"Responsabilidades.{0,300}", text, re.IGNORECASE | re.DOTALL)
    if resp_section:
        codigos = re.findall(r"\b(0[1-9]|[1-9]\d)\b", resp_section.group())
        mapa = {
            "05": "Renta y complementarios (régimen ordinario)",
            "07": "Retención en la fuente",
            "11": "IVA - Ventas régimen común",
            "14": "Informante de exógena",
            "35": "CREE",
            "42": "IVA - Gran contribuyente",
        }
        data["responsabilidades"] = [mapa.get(c, f"Código {c}") for c in set(codigos) if c in mapa]
        if data["responsabilidades"]:
            data["campos_encontrados"].append("responsabilidades")

    # -- Fecha RUT (Campo 61) --
    fecha = _search(r"(?:61[\.:\s]+Fecha|Fecha.*?generaci[oó]n)[^\d]*(\d{4}[\-/\.]\d{2}[\-/\.]\d{2})", text)
    data["fecha_rut"] = fecha
    if fecha:
        data["campos_encontrados"].append("fecha_rut")

    # -- Confianza --
    data["confianza"] = min(100, len(data["campos_encontrados"]) * 15)
    return data


# ── FUNCIÓN PRINCIPAL ────────────────────────────────────────────────────────

def procesar_documento(file_bytes: bytes, filename: str = "") -> dict:
    """
    Función principal. Recibe los bytes de un PDF o imagen,
    detecta su tipo y extrae todos los campos disponibles.

    Returns:
        dict con claves:
          - tipo_doc: 'camara_comercio' | 'rut' | 'unknown'
          - confianza: 0-100
          - (campos específicos del documento)
    """
    ext = os.path.splitext(filename.lower())[1]

    if ext in (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"):
        text = extract_text_from_image(file_bytes)
    else:
        text = extract_text_from_pdf(file_bytes)

    if not text or len(text.strip()) < 30:
        return {"tipo_doc": "unknown", "confianza": 0, "error": "No se pudo extraer texto del archivo."}

    tipo = detect_document_type(text)

    if tipo == "camara_comercio":
        result = extract_camara_comercio(text)
    elif tipo == "rut":
        result = extract_rut(text)
    else:
        result = {
            "tipo_doc": "unknown",
            "confianza": 0,
            "texto_bruto": text[:500],
            "error": "No se reconoció el tipo de documento. ¿Es una Cámara de Comercio o RUT?"
        }

    result["texto_completo"] = text  # Para debug / auditoría
    return result


def resultado_a_session_state(resultado: dict) -> dict:
    """
    Convierte el resultado del extractor OCR al formato de session_state
    del aplicativo HMO Auditor Elite.

    Returns: dict listo para actualizar st.session_state
    """
    ss = {}
    tipo = resultado.get("tipo_doc", "unknown")

    if tipo == "camara_comercio":
        if resultado.get("company_name"):
            ss["company_name"] = resultado["company_name"]
        if resultado.get("empresa_nit"):
            ss["empresa_nit"] = resultado["empresa_nit"]
        if resultado.get("rep_legal"):
            ss["rep_legal"] = resultado["rep_legal"]
        if resultado.get("rep_id"):
            ss["rep_id"] = resultado["rep_id"]
        if resultado.get("empresa_direccion"):
            ss["empresa_direccion"] = resultado["empresa_direccion"]
        if resultado.get("domicilio"):
            ss.setdefault("empresa_ciudad", resultado["domicilio"])
        if resultado.get("empresa_objeto"):
            ss["empresa_objeto"] = resultado["empresa_objeto"]

    elif tipo == "rut":
        if resultado.get("company_name") and not ss.get("company_name"):
            ss["company_name"] = resultado["company_name"]
        if resultado.get("empresa_nit") and not ss.get("empresa_nit"):
            ss["empresa_nit"] = resultado["empresa_nit"]
        if resultado.get("empresa_direccion") and not ss.get("empresa_direccion"):
            ss["empresa_direccion"] = resultado["empresa_direccion"]
        if resultado.get("email"):
            ss["empresa_email"] = resultado["email"]
        if resultado.get("telefono"):
            ss["empresa_telefono"] = resultado["telefono"]
        if resultado.get("ciudad"):
            ss.setdefault("empresa_ciudad", resultado["ciudad"])
        if resultado.get("actividad_ciiu"):
            ss["empresa_ciiu"] = resultado["actividad_ciiu"]

    return ss
