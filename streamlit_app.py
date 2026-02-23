import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os
import sys
import io
import shutil
import json
import zipfile

# --- CONFIGURACIÓN DE RUTAS PARA DESPLIEGUE ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GEN_PATH = os.path.join(SCRIPT_DIR, "HMO_Auditor_Master_V1", "04_Arquitectura_y_Diseno", "Scripts_Generadores")
if GEN_PATH not in sys.path:
    sys.path.append(GEN_PATH)

from HMO_PDF_Generator import generate_audit_program_pdf, generate_preparation_guide_pdf, generate_document_template_pdf, generate_maturity_report_pdf
from HMO_AI_Engine import HMO_AI_Engine
from HMO_Auditor_Master_V2_Generator import create_audit_program_v2
from HMO_Checklist_Legal_Generator import create_legal_checklist
try:
    from HMO_OCR_Extractor import procesar_documento, resultado_a_session_state
    OCR_DISPONIBLE = True
except Exception:
    OCR_DISPONIBLE = False

try:
    from HMO_Auth import check_login, can, get_rol_label, get_all_users, create_user, \
                         toggle_user_active, delete_user, change_password, load_users
    AUTH_DISPONIBLE = True
except Exception as _ae:
    AUTH_DISPONIBLE = False


# Configuración de página
st.set_page_config(page_title="HMO Auditor Pro - V1.4 Elite", layout="wide", page_icon="🛡️")

# --- SISTEMA DE DISEÑO ELITE V3.0 (HI-FI PROFESSIONAL MOCKUP) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* FONDO BASE PROFESIONAL */
    .stApp {
        background: #0B0E14 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 194, 255, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.08) 0px, transparent 50%) !important;
        background-attachment: fixed !important;
    }

    /* GLASSMORPHISM PROFUNDO (TARJETAS) */
    .elite-card {
        background: rgba(14, 20, 31, 0.75) !important;
        backdrop-filter: blur(25px) saturate(210%) !important;
        border: 1.5px solid rgba(0, 194, 255, 0.3) !important;
        border-radius: 16px !important;
        padding: 1rem !important; /* Ultra-compacto */
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    /* COMPACTACIÓN GLOBAL STREAMLIT */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 95% !important;
    }
    .elite-card:hover { 
        border-color: #00C2FF !important; 
        box-shadow: 0 0 40px rgba(0, 194, 255, 0.25) !important; 
    }

    /* MINI DOC CARD (V19.5 ELITE TECH) */
    .doc-card-mini {
        background: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(12px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        padding: 0.7rem !important;
        margin-bottom: 0.5rem !important;
        height: 155px !important;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease;
    }
    .doc-card-mini:hover { 
        background: rgba(15, 23, 42, 0.6) !important;
        border-color: rgba(0, 194, 255, 0.5) !important;
        transform: translateY(-2px);
    }
    
    .status-badge {
        font-size: 0.55rem;
        background: rgba(255, 255, 255, 0.08);
        padding: 2px 6px;
        border-radius: 5px;
        text-transform: uppercase;
        color: #94A3B8;
    }

    /* TEXTO HI-FI (LEGIBILIDAD EXTREMA) */
    .stApp, .stApp p, .stApp li {
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* ETIQUETAS DE WIDGETS — BLANCO SUAVE (LEGIBLE) */
    [data-testid="stWidgetLabel"] p {
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        font-size: 0.80rem !important;
        margin-bottom: 0.6rem !important;
        text-shadow: 0 1px 6px rgba(0, 194, 255, 0.2);
    }

    /* TITULOS NEON — REFINADOS V16 */
    h1 { font-size: 1.8rem !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 1.4rem !important; }
    h3 { font-size: 1.1rem !important; }
    
    h1, h2, h3, .neon-title {
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 15px rgba(0, 194, 255, 0.4);
        letter-spacing: 2px !important;
        font-weight: 700 !important;
        text-align: center;
    }

    /* INDICADORES CIRCULARES (PHASES) */
    .phase-circle {
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-family: 'Orbitron';
        border: 3px solid #00C2FF;
        box-shadow: 0 0 10px rgba(0, 194, 255, 0.3);
    }

    /* INPUTS Y FORMULARIOS HI-FI */
    /* INPUTS Y FORMULARIOS HI-FI V4.6 (ACCESSIBILITY FIRST) */
    [data-baseweb="input"], [data-baseweb="select"], [data-baseweb="popover"] {
        background: #F8FAFC !important; /* Más claro aún */
        border: 1px solid rgba(0, 194, 255, 0.4) !important;
        border-radius: 8px !important;
    }
    input { 
        color: #0F172A !important; 
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    /* BOTONES ELITE 3.0 — SOBRIOS V16 */
    .stButton>button {
        background: linear-gradient(135deg, #00C2FF 0%, #172554 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        border: none !important;
        padding: 0.5rem 1rem !important; /* Más compacto */
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important; /* Fuente más pequeña */
        box-shadow: 0 4px 15px rgba(0, 194, 255, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover { 
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 194, 255, 0.5) !important;
    }

    /* SIDEBAR GLASS */
    [data-testid="stSidebar"] {
        background: rgba(14, 20, 31, 0.95) !important;
        border-right: 1px solid rgba(0, 194, 255, 0.3) !important;
    }

    /* DASHBOARD GAUGES */
    .stPlotlyChart {
        background: transparent !important;
        border-radius: 24px;
    }
    /* BOTÓN DE AYUDA FLOTANTE */
    .floating-help {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 60px;
        height: 60px;
        background: rgba(0, 194, 255, 0.2) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid #00C2FF !important;
        border-radius: 50% !important;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #00C2FF !important;
        font-size: 24px !important;
        z-index: 1001;
        box-shadow: 0 0 20px rgba(0, 194, 255, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none !important;
    }
    .floating-help:hover {
        transform: scale(1.1) rotate(15deg);
        background: rgba(0, 194, 255, 0.4) !important;
        box-shadow: 0 0 30px rgba(0, 194, 255, 0.6);
    }
    
    /* COMPACTACIÓN EXTREMA SIDEBAR */
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebar"] .block-container { padding-top: 1rem !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2, [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        font-size: 0.8rem !important;
        margin-bottom: 2px !important;
        margin-top: 5px !important;
    }
    [data-testid="stSidebar"] .stRadio > label { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        font-size: 0.75rem !important;
        padding: 2px 0px !important;
        min-height: 20px !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 0px !important;
    }
    [data-testid="stSidebar"] hr { margin: 0.5rem 0 !important; }

    /* COMPACTACIÓN QUIRÚRGICA V21.10 (ZERO-SCROLL) */
    [data-testid="stFileUploader"] {
        padding: 0.3rem !important;
        background: rgba(0, 194, 255, 0.04) !important;
        border: 1px solid rgba(0, 194, 255, 0.2) !important;
        border-radius: 8px !important;
        margin-bottom: 0.5rem !important;
    }
    [data-testid="stFileUploader"] section {
        min-height: 60px !important;
    }
    [data-testid="stFileUploader"] button {
        font-weight: 900 !important;
        font-size: 0.85rem !important;
        color: #FFFFFF !important;
        background-color: #0080FF !important;
        padding: 0.2rem 0.6rem !important;
        text-transform: uppercase !important;
    }
    [data-testid="stFileUploader"] label {
        color: #00C2FF !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        margin-bottom: 4px !important;
    }
    [data-testid="stFileUploaderDropzone"] div {
        display: none !important; /* Ocultar texto decorativo para ahorrar espacio */
    }
    
    /* HARD RESET FASE C V21.13 (CLEAN-ULTRA-ELITE) */
    .fase-c-card {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(0, 194, 255, 0.2) !important;
        border-radius: 12px !important;
        margin-bottom: 0.8rem !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
        box-shadow: none !important;
        transition: border 0.3s ease !important;
    }
    .fase-c-card:hover {
        border-color: rgba(0, 194, 255, 0.5) !important;
    }
    .fase-c-cabecera {
        padding: 0.6rem !important;
        background: rgba(0, 194, 255, 0.08) !important;
        border-bottom: 1px solid rgba(0, 194, 255, 0.2) !important;
        min-height: 55px !important;
    }
    /* BLINDAJE DE COMPONENTES INTERNOS (STREAMLIT RESET) */
    .fase-c-card [data-testid="stFileUploader"], 
    .fase-c-card [data-testid="stFileUploader"] section, 
    .fase-c-card [data-testid="stFileUploaderDropzone"],
    .fase-c-card [data-testid="stBaseButton-secondary"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    .fase-c-card [data-testid="stFileUploader"] section {
        min-height: 40px !important;
        justify-content: center !important;
        align-items: center !important;
    }
    .fase-c-card [data-testid="stFileUploaderDropzone"] div {
        display: none !important;
    }
    /* BOTONERA TIPO HARDWARE (FOOTER) */
    .fase-c-footer {
        background: rgba(0, 194, 255, 0.05) !important;
        border-top: 1px solid rgba(0, 194, 255, 0.1) !important;
        padding: 0.2rem !important;
    }
    .fase-c-card button {
        background: rgba(0, 194, 255, 0.1) !important;
        border: 1px solid rgba(0, 194, 255, 0.2) !important;
        color: #00C2FF !important;
        height: 32px !important;
        font-size: 1rem !important;
        border-radius: 4px !important;
    }
    .fase-c-card button:hover {
        background: rgba(0, 194, 255, 0.3) !important;
        border-color: #00C2FF !important;
    }
    
    [data-testid="stExpander"] {
        background: rgba(14, 20, 31, 0.4) !important;
        border: 1.5px solid rgba(0, 194, 255, 0.2) !important;
        border-radius: 12px !important;
        margin-bottom: 1rem !important;
        padding: 0.2rem !important;
    }
    [data-testid="stExpander"] summary {
        color: #00C2FF !important;
        font-weight: 700 !important;
    }

    @media (max-width: 768px) { .floating-help { display: none; } }
</style>
""", unsafe_allow_html=True)

# --- BOTÓN DE AYUDA UNIVERSAL (V3.5) ---
st.markdown("""
<a href='#' class='floating-help' title='Soporte Experto Elite'>
    🛡️
</a>
""", unsafe_allow_html=True)

# Lógica de Sesión (V1.9.0 Auth)
for key, default in [('env', None), ('norma', "Calidad (ISO 9001)"), ('paso_ingesta', 0), ('logo_path', None), ('expediente', {}), ('autorizado_emision', False), 
                    ('auditor_name', ""), ('rep_legal', ""), ('rep_id', ""), ('empresa_tamanio', "Pyme"), ('empresa_sector', "Servicios"),
                    ('empresa_nit', ""), ('empresa_direccion', ""), ('empresa_web', ""), ('empresa_objeto', ""), ('empresa_personal', 0),
                    ('user_role', "Administrador (Global)"), ('company_name', ""), ('base_path', ""), ('kb', {}),
                    ('landing_mode', None), ('auth', None), ('plan_accion', {}), ('history_chs', [])]:  # auth=None → no logueado
    if key not in st.session_state: st.session_state[key] = default




# ... [Funciones de persistencia omitidas por brevedad] ...

# ═════════════════════════════════════════════════════════════════
# PANTALLA DE LOGIN (V1.0) — Bloquea el resto de la app si no hay sesión
# ═════════════════════════════════════════════════════════════════
if AUTH_DISPONIBLE and st.session_state['auth'] is None:
    # — Cabecera login —
    st.markdown("""
    <div style='max-width:440px;margin:4rem auto 0;'>
    <h2 style='text-align:center;color:#FFFFFF;font-family:Orbitron,sans-serif;
               letter-spacing:3px;margin-bottom:0.2rem;'>
        🛡️ HMO Auditor
    </h2>
    <p style='text-align:center;color:#475569;font-size:0.8rem;margin-bottom:2rem;'>
        Sistema de Gestión de Auditorías Elite
    </p>
    </div>
    """, unsafe_allow_html=True)

    _lc, _lmid, _lc2 = st.columns([1, 2, 1])
    with _lmid:
        st.markdown("""
        <div style='background:rgba(14,20,31,0.8);border:1px solid rgba(0,194,255,0.25);
                    border-radius:16px;padding:2rem;'>
            <p style='color:#94A3B8;font-size:0.75rem;letter-spacing:1px;
                      margin-bottom:1.5rem;text-align:center;'>ACCESO AL SISTEMA</p>
        </div>
        """, unsafe_allow_html=True)

        # Cargar lista de usuarios activos para el selector
        try:
            _all_users = get_all_users()
            _user_options = [u['user'] for u in _all_users if u.get('activo', True)]
        except Exception:
            _user_options = ["admin", "auditor", "visitante"]

        _login_user = st.selectbox(
            "👤 Selecciona tu ROL de Acceso",
            options=_user_options,
            key="login_user",
            help="El nombre de usuario coincide con tu rol en el sistema."
        )
        _login_pass = st.text_input("🔑 Contraseña", type="password", placeholder="••••••••", key="login_pass")

        if st.button("🚀 Ingresar al Sistema", use_container_width=True, type="primary"):
            if _login_user and _login_pass:
                _user_data = check_login(_login_user, _login_pass)
                if _user_data:
                    st.session_state['auth'] = _user_data
                    st.session_state['user_role'] = _user_data['rol']
                    st.session_state['auditor_name'] = _user_data.get('nombre', '')
                    st.rerun()
                else:
                    st.error("❌ Contraseña incorrecta.")
            else:
                st.warning("⚠️ Ingresa tu contraseña.")

        st.markdown("<p style='text-align:center;color:#334155;font-size:0.65rem;margin-top:1rem;'>"
                    "HMO v2.0 · Operación local privada</p>", unsafe_allow_html=True)
    st.stop()  # ← Nada más se ejecuta si no hay sesión


# ── CAMBIO OBLIGATORIO DE CLAVE (primer login) ────────────────────────────
if AUTH_DISPONIBLE and st.session_state.get('auth') and st.session_state['auth'].get('primer_login', False):
    _user = st.session_state['auth']['user']
    st.warning("🔒 **Primer acceso detectado** — Debes cambiar la contraseña temporal antes de continuar.")
    _c1, _cm, _c2 = st.columns([1, 2, 1])
    with _cm:
        _np1 = st.text_input("Nueva contraseña", type="password", key="cp_new1")
        _np2 = st.text_input("Confirmar contraseña", type="password", key="cp_new2")
        if st.button("💾 Guardar nueva contraseña", type="primary", use_container_width=True):
            if _np1 and _np1 == _np2 and len(_np1) >= 6:
                change_password(_user, _np1)
                st.session_state['auth']['primer_login'] = False
                st.success("✅ Contraseña actualizada. Continuando...")
                st.rerun()
            elif _np1 != _np2:
                st.error("❌ Las contraseñas no coinciden.")
            else:
                st.error("❌ Mínimo 6 caracteres.")
    st.stop()



def setup_company_folders(company_name):
    """Crea la estructura de carpetas para una nueva auditoría."""
    safe_name = "".join([c if c.isalnum() else "_" for c in company_name])
    base_path = os.path.join(os.getcwd(), "Auditorias_HMO", safe_name)
    os.makedirs(base_path, exist_ok=True)
    
    # Estructura Estándar (V1.6.0 Rigor Legal)
    folders = [
        "01_Direccion_y_Estrategia", "02_Gestion_de_Calidad", 
        "03_Operaciones", "04_Recursos_Humanos", 
        "05_TI_y_Seguridad", "06_Anexos_Tecnicos",
        "01_Templates_Vacios", "02_Auditoria_IA"
    ]
    for f in folders:
        os.makedirs(os.path.join(base_path, f), exist_ok=True)
    return base_path


def formatear_ejemplo(doc_item, metadata):
    """Inyecta datos reales de la empresa en el ejemplo base del documento."""
    ejemplo = doc_item.get('ejemplo_base', 'No hay ejemplo disponible para este documento.')
    ejemplo = ejemplo.replace("{EMPRESA}", metadata.get('company_name', 'LA EMPRESA'))
    ejemplo = ejemplo.replace("{OBJETO}", metadata.get('empresa_objeto', 'sus actividades comerciales'))
    ejemplo = ejemplo.replace("{AUDITOR}", metadata.get('auditor_name', 'El Auditor'))
    return ejemplo

def save_audit_state():
    if st.session_state['env'] and st.session_state.get('company_name'):
        base_dir = st.session_state['base_path']
        if not os.path.exists(base_dir): os.makedirs(base_dir, exist_ok=True)
        
        state = {
            "company_name": st.session_state['company_name'], "norma": st.session_state['norma'],
            "paso_ingesta": st.session_state['paso_ingesta'], "logo_path": st.session_state['logo_path'],
            "env": st.session_state['env'], "expediente": st.session_state['expediente'], 
            "autorizado_emision": st.session_state['autorizado_emision'],
            "auditor_name": st.session_state['auditor_name'], "rep_legal": st.session_state['rep_legal'],
            "rep_id": st.session_state['rep_id'], "empresa_tamanio": st.session_state['empresa_tamanio'],
            "empresa_sector": st.session_state['empresa_sector'],
            "empresa_nit": st.session_state['empresa_nit'], "empresa_direccion": st.session_state['empresa_direccion'],
            "empresa_web": st.session_state['empresa_web'], "empresa_objeto": st.session_state['empresa_objeto'],
            "empresa_personal": st.session_state['empresa_personal'],
            "plan_accion": st.session_state.get('plan_accion', {}),
            "history_chs": st.session_state.get('history_chs', []),
            "last_update": datetime.datetime.now().isoformat()
        }
        with open(os.path.join(base_dir, "audit_state.json"), "w") as f: json.dump(state, f, indent=4)

def load_audit_state(company_folder):
    # Intentar cargar desde la nueva ruta unificada
    base_audits = os.path.join(os.getcwd(), "Auditorias_HMO")
    state_path = os.path.join(base_audits, company_folder, "audit_state.json")
    
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
            for k, v in state.items(): st.session_state[k] = v
            st.session_state['base_path'] = os.path.join(base_audits, company_folder)
            return True
    return False

# --- MIGRACIÓN DE LEGACY (V1.7.5) ---
def migrate_legacy_audits():
    base_audits = os.path.join(os.getcwd(), "Auditorias_HMO")
    os.makedirs(base_audits, exist_ok=True)
    
    # Buscar carpetas sospechosas en la raíz (ej: Innovatech_Solutions)
    for item in os.listdir(os.getcwd()):
        if os.path.isdir(item) and item not in [".git", "HMO_Auditor_Master_V1", "Auditorias_HMO", "Formatos_Profesionales_HMO", ".streamlit"]:
            # Si tiene estructura de auditoría, moverla
            if os.path.exists(os.path.join(item, "01_Direccion_y_Estrategia")) or os.path.exists(os.path.join(item, "audit_state.json")):
                try:
                    dest = os.path.join(base_audits, item)
                    if not os.path.exists(dest):
                        shutil.move(item, dest)
                        st.sidebar.success(f"📦 Auditoría '{item}' migrada a zona segura.")
                except: pass

migrate_legacy_audits()

# --- PANTALLA DE BIENVENIDA (ONBOARDING GATEWAY V3.5) ---
if st.session_state['env'] is None:

    # ══════════════════════════════════════════════════════════════════
    #  CABECERA COMÚN
    # ══════════════════════════════════════════════════════════════════
    st.markdown("""
    <h2 style='text-align:center;color:#FFFFFF;font-family:Orbitron,sans-serif;
               letter-spacing:3px;margin-bottom:0.2rem;'>
        🛡️ HMO HUB <span style='font-size:0.55em;color:#00C2FF;'>ELITE EDITION</span>
    </h2>
    <p style='text-align:center;color:#475569;font-size:0.8rem;margin-bottom:1.8rem;'>
        Sistema de Auditoría e Implementación de Sistemas de Gestión • v2.0
    </p>
    """, unsafe_allow_html=True)

    _lmode = st.session_state.get('landing_mode', None)

    # ══════════════════════════════════════════════════════════════════
    #  NIVEL 0 — MENÚ PRINCIPAL (Tarjetas Clickables Elite V15)
    # ══════════════════════════════════════════════════════════════════
    if _lmode is None:
        st.markdown("""
        <style>
        div.stButton > button {
            height: 180px !important;
            border-radius: 16px !important;
            border: 1.5px solid rgba(255,255,255,0.1) !important;
            background: rgba(255,255,255,0.03) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            border-color: #00C2FF !important;
            background: rgba(0,194,255,0.08) !important;
            transform: translateY(-5px) !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
        }
        </style>
        """, unsafe_allow_html=True)

        _mc1, _mc2, _mc3 = st.columns(3, gap="medium")

        with _mc1:
            if st.button("📂\n\n**REANUDAR**\n\nContinúa auditoría\nguardada en local", 
                         use_container_width=True, key="btn_home_resume"):
                st.session_state['landing_mode'] = 'reanudar_v15'
                st.rerun()

        with _mc2:
            if st.button("🎓\n\n**SIMULACIÓN**\n\nLanzar demo de\nInnovatech SAS", 
                         use_container_width=True, key="btn_home_sim"):
                with st.spinner("Inyectando Inteligencia de Negocio..."):
                    _bp = setup_company_folders("Innovatech Solutions SAS")
                    st.session_state.update({
                        'env': "Simulacion", 'company_name': "Innovatech Solutions SAS",
                        'base_path': _bp, 'paso_ingesta': 5, 'auditor_name': "Juan Gabriel Ortiz",
                        'empresa_nit': "901.455.789-2", 'norma': ["Calidad (ISO 9001)", "Seguridad (ISO 27001)"],
                        'expediente': {}, 'empresa_objeto': "Desarrollo de IA y Auditoria Digital"
                    })
                    from HMO_Simulation_Engine import HMOSimulationEngine
                    sim = HMOSimulationEngine(_bp)
                    # Inyectar Calidad y Seguridad para Innovatech
                    sim.simulate_norm_ecosystem("CALIDAD", "Innovatech Solutions SAS", "Tecnologia")
                    _, log_s = sim.simulate_norm_ecosystem("SEGURIDAD", "Innovatech Solutions SAS", "Tecnologia")
                    for entry in log_s:
                        st.session_state['expediente'][entry['doc']] = {"score": 95, "file_path": entry['path'], "validado": True}
                    
                    save_audit_state(); st.rerun()

        with _mc3:
            if st.button("🏗️\n\n**NUEVO PROYECTO**\n\nCrear auditoría real\ncon rigor legal", 
                         use_container_width=True, key="btn_home_new"):
                st.session_state['landing_mode'] = 'nuevo'
                st.rerun()

        st.markdown("<p style='text-align:center;font-size:0.65rem;color:#475569;margin-top:2rem;'>"
                    "HMO Auditor V15 Elite · UI Ergonómica · Clickable Cards Enabled</p>",
                    unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    #  MODO REANUDAR (Compacto)
    # ══════════════════════════════════════════════════════════════════
    elif _lmode == 'reanudar_v15':
        if st.button("← Volver", key="back_resume_v15"):
            st.session_state['landing_mode'] = None; st.rerun()
        
        st.markdown("<h3 style='text-align:center;'>📂 Seleccionar Expediente</h3>", unsafe_allow_html=True)
        base_audits_path = os.path.join(os.getcwd(), "Auditorias_HMO")
        existing = [d for d in os.listdir(base_audits_path) if os.path.isdir(os.path.join(base_audits_path, d))] if os.path.exists(base_audits_path) else []
        
        if existing:
            # COMPACTACIÓN DE INPUTS (V19.3)
            _, col_sel, _ = st.columns([1, 2, 1])
            with col_sel:
                selected = st.selectbox("Expedientes en este equipo:", existing, key="sel_resume_v15")
                if st.button("🚀 ABRIR AUDITORÍA", type="primary", use_container_width=True):
                    if load_audit_state(selected): 
                        st.session_state['landing_mode'] = None
                        st.rerun()
        else:
            st.warning("No se encontraron auditorías guardadas.")

    # ══════════════════════════════════════════════════════════════════
    #  NIVEL 1 — NUEVO PROYECTO (ZERO-SCROLL COMPACT V15)
    # ══════════════════════════════════════════════════════════════════
    elif _lmode == 'nuevo':
        st.markdown("""
        <div style='margin:-1rem 0 1rem;display:flex;align-items:center;gap:1rem;'>
            <button onclick="window.location.reload();" style='background:none;border:none;color:#94A3B8;cursor:pointer;'>← Volver</button>
            <div style='flex:1;height:1px;background:rgba(16,185,129,0.2);'></div>
            <span style='color:#10B981;font-family:Orbitron;font-size:0.65rem;letter-spacing:2px;'>NUEVA CONFIGURACIÓN</span>
            <div style='flex:1;height:1px;background:rgba(16,185,129,0.2);'></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Volver al Hub Principal", key="back_new_v15"): st.session_state['landing_mode'] = None; st.rerun()

        # Layout Triple Columna para Zero-Scroll
        c_ocr, c_data, c_act = st.columns([1.2, 1, 0.8], gap="medium")

        with c_ocr:
            st.markdown("##### 🤖 ① Pre-Carga OCR")
            _up_cc = st.file_uploader("CC (PDF/Img)", type=["pdf","jpg","png"], key="up_cc_v15")
            _up_rut = st.file_uploader("RUT (PDF/Img)", type=["pdf","jpg","png"], key="up_rut_v15")
            
            if _up_cc and OCR_DISPONIBLE:
                with st.spinner("Leyendo CC..."):
                    _r = procesar_documento(_up_cc.read(), _up_cc.name)
                    if _r.get("tipo_doc") == "camara_comercio":
                        for _k, _v in resultado_a_session_state(_r).items(): st.session_state[_k] = _v
                        st.success(f"CC: {_r.get('company_name','')}")

        with c_data:
            st.markdown("##### 📝 ② Datos Entidad")
            _nombre_ocr = st.session_state.get('company_name', '').strip()
            new_name = st.text_input("Nombre Entidad", value=_nombre_ocr, placeholder="Ej: Universidad San José")
            
            normas_disponibles = ["Calidad (ISO 9001)", "Ambiental (ISO 14001)", "Seguridad (ISO 27001)", "Académico"]
            new_norma = st.multiselect("Normas", normas_disponibles, default=["Calidad (ISO 9001)"])

        with c_act:
            st.markdown("##### 🏗️ ③ Finalizar")
            st.write("")
            if st.button("🏗️ CREAR PROYECTO", type="primary", use_container_width=True):
                if new_name:
                    _base_path = setup_company_folders(new_name)
                    # Checklist Automático
                    _docs_req = [{"doc": "Camara de Comercio", "justificacion": "6.3.1 - Legal", "instrucciones": "Descargar CC"}]
                    try:
                        _pdf_out = os.path.join(_base_path, "01_Direccion_y_Estrategia")
                        generate_preparation_guide_pdf(new_name, _pdf_out, _docs_req, norma=", ".join(new_norma))
                    except: pass

                    st.session_state.update({
                        'env': "Real", 'company_name': new_name,
                        'norma': new_norma, 'base_path': _base_path, 'landing_mode': None
                    })
                    save_audit_state(); st.rerun()
                else:
                    st.warning("Nombre requerido")
            
            st.caption("Al crear, se habilita el Dashboard y se genera la Guía PDF.")
        with _col_tip:
            st.caption("💡 Si subiste documentos en el paso ①, el nombre se auto-completa. "
                       "Puedes editarlo antes de crear el proyecto.")


# --- DASHBOARD PRINCIPAL ---
else:
    company, base_path = st.session_state['company_name'], st.session_state['base_path']
    
    # --- CONFIGURACIÓN DE CARTAS Y PROGRESO (V3.9 PRE-RENDER) ---
    base_cartas = [
        {"doc": "Camara de Comercio (Existencia Legal)", "area": "Juridico", "ref": "Legalidad", "norma": "SIG", "prioridad": "VITAL (Obligatorio)", "desc": "Certificado actualizado con objeto social y NIT.", "justificacion": "ISO 19011:6.3.1 - Necesario para verificar la base legal y representacion de la entidad auditada.",
         "instrucciones": "Solicite en la Camara de Comercio o descargue del portal con vigencia no mayor a 30 dias.",
         "como_crear": "1. Ingrese al portal de la Camara de Comercio de su ciudad.\n2. Busque su empresa por NIT o Razon Social.\n3. Solicite el certificado de existencia y representacion legal.\n4. Asegurese de que tenga fecha reciente (max 30 dias).",
         "ejemplo_base": "CERTIFICADO DE EXISTENCIA Y REPRESENTACION LEGAL\n\nEmpresa: {EMPRESA}\nNIT: 900.XXX.XXX-X\nObjeto Social: Prestacion de servicios de...\nRepresentante Legal: [Nombre y CC]\nVigente a: {HOY}"},

        {"doc": "RUT (Registro Unico Tributario)", "area": "Juridico", "ref": "Fiscal", "norma": "SIG", "desc": "Identificacion tributaria y responsabilidades.", "justificacion": "Requisito legal/fiscal para la identificacion de la persona juridica segun normativa nacional.",
         "instrucciones": "Descargue el PDF actualizado desde el portal de la DIAN.",
         "como_crear": "1. Ingrese a www.dian.gov.co\n2. Seleccione 'Servicios en Linea'.\n3. Consulte o actualice el RUT de {EMPRESA}.\n4. Descargue el PDF oficial.",
         "ejemplo_base": "RUT - {EMPRESA}\n\nNIT: 900.XXX.XXX-X\nRazon Social: {EMPRESA} S.A.S\nResponsabilidad: Regimen Comun / Gran Contribuyente\nActividad CIIU: XXXX - [Descripcion de la actividad]"},

        {"doc": "Acta de Compromiso Directivo", "area": "Alta Direccion", "ref": "Gobierno", "norma": "SIG", "prioridad": "VITAL (Obligatorio)", "desc": "Acuerdo de preparacion, asignacion de recursos y roles.", "justificacion": "ISO 9001:5.1 e ISO 19011:6.2.2 - El compromiso de la direccion es vital.",
         "instrucciones": "Redacte un acta firmada por la gerencia declarando la intencion de auditoria.",
         "como_crear": "1. Convoque una reunion de alta direccion.\n2. Redacte el acta declarando el objetivo de la auditoria.\n3. Designe los responsables de cada area.\n4. El Gerente General y el Auditor firman el acta.",
         "ejemplo_base": "ACTA DE COMPROMISO DIRECTIVO No. 001\n\nEn la ciudad de Bogota, siendo las 9:00am, reunidos los directivos de {EMPRESA}...\n\nCOMPROMISOS:\n- La gerencia provee los recursos necesarios para la auditoria.\n- El proceso de auditoria iniciara el [FECHA].\n\nFIRMAS: [Gerente] / [Auditor Lider: {AUDITOR}]"},

        {"doc": "Cronograma de Actividades de Preparacion", "area": "Alta Direccion", "ref": "Planeacion", "norma": "SIG", "desc": "Calendario con hitos de entrega de evidencias (Inicio-Fin).", "justificacion": "ISO 19011:6.3.2 - Base para la planificacion detallada de las actividades de auditoria.",
         "instrucciones": "Disene un calendario (Excel o Gantt) con fechas limite de entrega.",
         "como_crear": "1. Liste todos los documentos requeridos.\n2. Asigne un responsable por cada documento.\n3. Defina fechas limite de entrega.\n4. Exporte como PDF o imagen.",
         "ejemplo_base": "CRONOGRAMA - {EMPRESA}\n\nACTIVIDAD                    RESPONSABLE        FECHA LIMITE\nEntrega Camara de Comercio   [Juridico]         DD/MM/AAAA\nEntrega Estados Financieros  [Contabilidad]     DD/MM/AAAA\nRevision IA de Documentos    {AUDITOR}          DD/MM/AAAA"},

        {"doc": "Mision y Vision Corporativa", "area": "Alta Direccion", "ref": "Estrategico", "norma": "SIG", "prioridad": "VITAL (Obligatorio)", "desc": "Proposito y rumbo organizacional.", "justificacion": "ISO 9001:4.1 - Fundamental para entender el contexto organizacional.",
         "instrucciones": "Extraiga los textos oficiales del manual estrategico o la pagina web de la empresa.",
         "como_crear": "1. Reunase con el comite directivo.\n2. Defina el 'Para que existimos' (Mision).\n3. Defina el 'Hacia donde vamos' en 5 anos (Vision).\n4. Plasmelo en un documento Word con membrete oficial.",
         "ejemplo_base": "MISION: En {EMPRESA}, nos dedicamos a prestar servicios de alta calidad a nuestros clientes, garantizando su satisfaccion plena.\n\nVISION: Para el 2030, {EMPRESA} sera reconocida como empresa lider en su sector en la region, destacando por la innovacion y compromiso con la calidad."},

        {"doc": "Matriz de Responsables de Area", "area": "Alta Direccion", "ref": "Gobierno", "norma": "SIG", "desc": "Liderazgo nominal por procesos.", "justificacion": "ISO 9001:5.3 - Define las responsabilidades y autoridades dentro de los procesos.",
         "instrucciones": "Cree un cuadro que relacione cada proceso con su responsable.",
         "como_crear": "1. Identifique todos los procesos del mapa.\n2. Asigne un lider nominal (nombre y cargo).\n3. Defina su rol en el SGC.\n4. Elabore una tabla en Excel o Word.",
         "ejemplo_base": "MATRIZ DE RESPONSABLES - {EMPRESA}\n\nPROCESO           LIDER              CARGO          ROL EN SGC\nGestion Calidad   [Nombre]           Coord. SIG     Coordinar auditoria interna\nCompras           [Nombre]           Jefe Logist.   Validar proveedores calificados\nTalento Humano    [Nombre]           Dir. RRHH      Gestionar competencia del personal"},

        {"doc": "Organigrama Funcional", "area": "Alta Direccion", "ref": "Estructura", "norma": "SIG", "desc": "Jerarquia y mandos medios.", "justificacion": "ISO 19011:6.3.1 - Requerido para mapear la cadena de mando.",
         "como_crear": "1. Dibuje los niveles jerarquicos de arriba hacia abajo.\n2. Use herramientas como Visio, LucidChart o PowerPoint.\n3. Asegurese de que Calidad/SIG reporte a la Gerencia.\n4. Guarde como PDF con fecha de vigencia.",
         "ejemplo_base": "ORGANIGRAMA - {EMPRESA}\n\n[GERENCIA GENERAL]\n    |\n    +--- [Direccion Comercial]\n    +--- [Direccion de Operaciones]\n    |        +--- [Equipo Tecnico]\n    +--- [SIG / Calidad] (Reporte directo a Gerencia)\n    +--- [Talento Humano]"},

        # EXPANSION V8.9
        {"doc": "Estados Financieros (Ultimo Trimestre)", "area": "Financiera", "ref": "Sostenibilidad", "norma": "CALIDAD", "desc": "Balance y P&G actualizado.", "justificacion": "ISO 9001:7.1.1 - Asegura que la organizacion cuenta con los recursos necesarios para el SGC.",
         "instrucciones": "Solicite al area contable el balance general y estado de resultados firmado.",
         "como_crear": "1. Solicite al contador o area financiera los estados del ultimo trimestre.\n2. El documento debe estar firmado por el contador certificado.\n3. Adjunte Balance General y Estado de Resultados.",
         "ejemplo_base": "ESTADOS FINANCIEROS - {EMPRESA} | Q: [Trimestre/Ano]\n\nACTIVO TOTAL: $XXX.XXX.XXX\nPASIVO TOTAL: $XXX.XXX.XXX\nPATRIMONIO: $XXX.XXX.XXX\nUTILIDAD NETA: $XX.XXX.XXX\n\nFirmado: [Contador] CC/TP: XXXXX"},

        {"doc": "Manual de Funciones y Perfiles", "area": "Talento Humano", "ref": "Competencia", "norma": "CALIDAD", "desc": "Responsabilidades por cargo.", "justificacion": "ISO 9001:7.2 - Base para evaluar la competencia del personal.",
         "instrucciones": "Adjunte el documento institucional que define los perfiles de cargo.",
         "como_crear": "1. Liste todos los cargos de {EMPRESA}.\n2. Para cada cargo defina: Mision del cargo, Funciones, Perfil (educacion/experiencia).\n3. El jefe de RRHH y la Gerencia aprueban el documento.",
         "ejemplo_base": "PERFIL DE CARGO - {EMPRESA}\n\nCARGO: Coordinador de Calidad\nMISION: Planificar y coordinar el SGC de {EMPRESA}.\nFUNCIONES:\n1. Mantener actualizado el sistema documental.\n2. Planificar y ejecutar auditorias internas.\nPERFIL: Profesional en Ingenieria Industrial o afines, 2 anos de experiencia en SGC."},

        {"doc": "Manual de Procesos Institucional", "area": "Operaciones", "ref": "SGC", "norma": "CALIDAD", "desc": "Documentacion de la operacion.", "justificacion": "ISO 9001:4.4.2 - Informacion documentada para apoyar la operacion.",
         "instrucciones": "Suba el manual maestro de procesos o listado maestro de procedimientos.",
         "como_crear": "1. Levante los procesos existentes conversando con cada area.\n2. Documente el flujo (Inicio-Proceso-Fin) de cada proceso clave.\n3. Defina entradas, salidas, recursos y controles.\n4. El Gerente y el responsable de cada proceso firman.",
         "ejemplo_base": "FICHA DE PROCESO - {EMPRESA}\n\nNOMBRE: Gestion de Compras\nOBJETIVO: Garantizar el suministro oportuno de bienes y servicios.\nENTRADAS: Solicitud de compra aprobada.\nSALIDAS: Bien/servicio entregado y verificado.\nRESPONSABLE: Jefe de Logistica.\nINDICADOR: Nivel de cumplimiento de proveedores > 90%"},
        
        # EXPANSIÓN V18.0: BLINDAJE SGC TOTAL
        {"doc": "Matriz de Riesgos y Oportunidades (SGC)", "area": "Calidad", "ref": "ISO 9001:6.1", "norma": "CALIDAD", "desc": "Mapa de amenazas y oportunidades del sistema.", "justificacion": "ISO 9001:6.1 - Abordar riesgos y oportunidades para asegurar que el SGC logre sus resultados."},
        {"doc": "Matriz de Comunicaciones (SGC)", "area": "Calidad", "ref": "ISO 9001:7.4", "norma": "CALIDAD", "desc": "Que, cuando, a quien y como comunicar.", "justificacion": "ISO 9001:7.4 - La organizacion debe determinar las comunicaciones internas y externas pertinentes."},
        {"doc": "Plan de Capacitación y Toma de Conciencia", "area": "Talento Humano", "ref": "ISO 9001:7.3", "norma": "CALIDAD", "desc": "Cronograma de formacion del personal.", "justificacion": "ISO 9001:7.3 - Asegurar que las personas que realizan el trabajo bajo el control de la organizacion tomen conciencia."},
        {"doc": "Informe de Auditoría Interna (Ciclo Previo)", "area": "Calidad", "ref": "ISO 9001:9.2", "norma": "CALIDAD", "desc": "Resultados de la ultima revision interna.", "justificacion": "ISO 9001:9.2 - La organizacion debe llevar a cabo auditorias internas a intervalos planificados."},
        {"doc": "Acta de Revisión por la Dirección", "area": "Alta Direccion", "ref": "ISO 9001:9.3", "norma": "CALIDAD", "desc": "Revision formal del SGC por la Gerencia.", "justificacion": "ISO 9001:9.3 - La alta direccion debe revisar el SGC para asegurar su conveniencia y eficacia."}
    ]

    norm_cartas = []
    normas_activas = st.session_state['norma'] if isinstance(st.session_state['norma'], list) else [st.session_state['norma']]
    
    if "Académico" in str(normas_activas):
        norm_cartas += [
            {"doc": "PEI (Proyecto Educativo)", "area": "Gestion Academica", "ref": "Ley 115", "norma": "ACADÉMICO", "desc": "Columna vertebral academica.", "justificacion": "Ley 115 de 1994 - Documento maestro que define la identidad y el modelo pedagogico de la institucion.", "instrucciones": "Recopile el documento PEI vigente del consejo directivo. Debe incluir el Horizonte Institucional y el Plan de Estudios."},
            {"doc": "Registro Calificado", "area": "Juridico", "ref": "Dec. 1330", "norma": "ACADÉMICO", "desc": "Autorizacion ministerial.", "justificacion": "Decreto 1330 de 2019 - Habilitacion legal para la oferta y desarrollo de programas academicos.", "instrucciones": "Adjunte la resolucion ministerial vigente que autoriza el programa."},
            {"doc": "Estatuto Docente", "area": "Talento Humano", "ref": "Dec. 1278", "norma": "ACADÉMICO", "desc": "Reglamentacion docente.", "justificacion": "Decreto 1278/2277 - Marco normativo para la gestion del personal docente y su escalafon.", "instrucciones": "Extraiga el reglamento de escalafon y deberes docentes aprobado por la institucion."},
            {"doc": "Manual de Convivencia", "area": "Gestion Academica", "ref": "Ley 115", "norma": "ACADÉMICO", "desc": "Acuerdos preventivos y correctivos.", "justificacion": "ISO 9001:S3 - Define las normas de interaccion y justicia escolar.", "instrucciones": "Estructura: 1. Horizonte (Misión/Visión), 2. Derechos y Deberes, 3. Debido Proceso (Escala de faltas), 4. Estímulos, 5. Ruta de Atención Integral. Tip: Debe estar firmado por el Consejo Directivo."},
            {"doc": "Plan de Estudios por Competencias", "area": "Gestion Academica", "ref": "Dec. 1330", "norma": "ACADÉMICO", "desc": "Disenio curricular.", "justificacion": "Aseguramiento de la Calidad Academica s/ Dec. 1330.", "instrucciones": "Estructura: 1. Malla Curricular por Grados, 2. Estándares/DBA (Derechos Básicos), 3. Criterios de Evaluación, 4. Metodologías (Aulas), 5. Plan de Nivelación. Tip: Verifique que sea coherente con el PEI."},
            {"doc": "Informe de Autoevaluacion Institucional", "area": "Alta Direccion", "ref": "Calidad Academica", "norma": "ACADÉMICO", "desc": "Corte de madurez educativa.", "justificacion": "Requisito para renovacion de registros calificados.", "instrucciones": "Estructura: 1. Gestión Directiva, 2. Gestión Académica, 3. Gestión Administrativa/Financiera, 4. Gestión de Comunidad, 5. Análisis de Indicadores (Deserción, Pruebas Saber)."},
            {"doc": "Plan de Mejoramiento Institucional (PMI)", "area": "Calidad", "ref": "Estrategico", "norma": "ACADÉMICO", "desc": "Acciones de mejora continua.", "justificacion": "ISO 9001:10.3 - Asegura la evolucion constante de la institucion.", "instrucciones": "Estructura: 1. Objetivos, 2. Metas Anuales, 3. Responsables, 4. Presupuesto, 5. Cronograma (Gantt). Tip: Cada hallazgo de la autoevaluación debe tener una acción aquí."}
        ]
    if "Seguridad" in str(normas_activas):
        norm_cartas += [
            {"doc": "Politica de Seguridad", "area": "Ciberseguridad", "ref": "ISO 27001:5.2", "norma": "SEGURIDAD", "desc": "Directrices de proteccion.", "justificacion": "ISO 27001:5.2 - La direccion debe establecer una politica de seguridad que sea apropiada.", 
             "como_crear": "1. Defina los principios de CID (Confidencialidad, Integridad, Disponibilidad).\n2. Establezca el alcance del SGSI.\n3. Declare el compromiso de la dirección con el cumplimiento legal.\n4. Firme y comunique a todo el personal.",
             "ejemplo_base": "POLÍTICA DE SEGURIDAD - {EMPRESA}\n\nEn nuestra empresa, dedicada a {OBJETO}, nos comprometemos a proteger la confidencialidad de los datos de nuestros clientes mediante controles técnicos y organizativos avanzados..."},
            {"doc": "Analisis de Riesgos", "area": "Ciberseguridad", "ref": "ISO 27001:6.1", "norma": "SEGURIDAD", "desc": "Mapa de vulnerabilidades.", "justificacion": "ISO 27001:6.1 - Base para el tratamiento planificado de los riesgos de seguridad de la informacion.", 
             "como_crear": "1. Identifique los activos críticos.\n2. Valore probabilidad e impacto.\n3. Defina el riesgo inherente y residual.\n4. Establezca el plan de tratamiento (Evitar, Mitigar, Transferir, Aceptar).",
             "ejemplo_base": "MATRIZ DE RIESGOS - {EMPRESA}\n\nACTIVO: Base de Datos de Clientes | AMENAZA: Acceso no autorizado | IMPACTO: Crítico | CONTROL: Cifrado AES-256."},
            {"doc": "Declaracion de Aplicabilidad (SoA)", "area": "Ciberseguridad", "ref": "ISO 27001:6.1.3", "norma": "SEGURIDAD", "desc": "Inventario de controles aplicables.", "justificacion": "ISO 27001:6.1.3 d) - Documento obligatorio que resume los controles de seguridad seleccionados.", 
             "como_crear": "1. Tome los 93 controles del Anexo A.\n2. Para cada uno, defina si aplica o no.\n3. Si no aplica, justifique detalladamente.\n4. Indique el estado actual de implementación.",
             "ejemplo_base": "SOA V2022 - {EMPRESA}\n\nControl A.5.1: Políticas de Seguridad -> APLICA (Implementado mediante manual corporativo).\nControl A.7.1: Seguridad Física -> NO APLICA (Somos una empresa 100% remota)."},
            {"doc": "Inventario de Activos de Informacion", "area": "Ciberseguridad", "ref": "ISO 27001:A.5.9", "norma": "SEGURIDAD", "desc": "Activos criticos de la entidad.", "justificacion": "ISO 27001:A.5.9 - Los activos asociados con informacion deben ser identificados.", "instrucciones": "Columnas: ID, Activo, Tipo (Software/Hardware/Datos), Dueño, Clasificación (Público/Privado)."},
            {"doc": "Plan de Continuidad de Negocio (BCP)", "area": "Operaciones", "ref": "ISO 27001:A.5.30", "norma": "SEGURIDAD", "desc": "Capacidad de recuperacion.", "justificacion": "ISO 27001:A.5.30 - Asegura la disponibilidad de la informacion ante incidentes graves.", "instrucciones": "Fases: 1. Análisis de Impacto (BIA), 2. Estrategia de Recuperación, 3. Roles en Emergencia, 4. Plan de Pruebas. Tip: Debe responder ¿qué pasa si se cae el servidor?"},
            {"doc": "Politica de Control de Acceso", "area": "Ciberseguridad", "ref": "ISO 27001:A.8.1", "norma": "SEGURIDAD", "desc": "Restriccion de privilegios.", "justificacion": "ISO 27001:A.8.1 - Reglas y derechos de acceso al sistema.", "instrucciones": "Reglas: 1. Registro de usuarios, 2. Gestión de contraseñas, 3. Privilegios mínimos, 4. Revocación inmediata. Tip: Especifique que los accesos son personales e intransferibles."}
        ]
    if "Ambiental" in str(normas_activas):
        norm_cartas += [
            {"doc": "Aspectos Ambientales", "area": "Gestion Ambiental", "ref": "ISO 14001:6.1.2", "norma": "AMBIENTAL", "desc": "Evaluacion de impactos.", "justificacion": "ISO 14001:6.1.2 - Determinacion de aspectos ambientales y sus impactos asociados.", 
             "como_crear": "1. Identifique las actividades de {EMPRESA}.\n2. Categorice las salidas (Residuo, Emisión, Vertimiento).\n3. Califique la severidad del impacto ambiental.\n4. Priorice los impactos significativos.",
             "ejemplo_base": "MATRIZ DE ASPECTOS - {EMPRESA}\n\nACTIVIDAD: Generación de residuos de oficina | ASPECTO: Papel y cartón | IMPACTO: Agotamiento de recursos naturales | SEVERIDAD: Baja."},
            {"doc": "Objetivos Ambientales", "area": "Gestion Ambiental", "ref": "ISO 14001:6.2", "norma": "AMBIENTAL", "desc": "Metas de eco-eficiencia.", "justificacion": "ISO 14001:6.2 - La organizacion debe establecer objetivos ambientales en las funciones relevantes.", "instrucciones": "Defina metas medibles para el año en curso."},
            {"doc": "Matriz de Requisitos Legales Ambientales", "area": "Juridico", "ref": "ISO 14001:6.1.3", "norma": "AMBIENTAL", "desc": "Cumplimiento normativo verde.", "justificacion": "ISO 14001:6.1.3 - Identificacion de obligaciones de cumplimiento ambiental.", 
             "como_crear": "1. Liste las leyes ambientales nacionales.\n2. Cruce con las actividades de {EMPRESA}.\n3. Verifique el estado de cumplimiento (Cumple/No Cumple).\n4. Establezca planes de acción para brechas.",
             "ejemplo_base": "REQUISITOS LEGALES - {EMPRESA}\n\nNORMA: Ley 99 de 1993 -> ARTÍCULO: Manejo de Residuos -> CUMPLIMIENTO: Sí (Certificado por gestor externo)."},
            {"doc": "Plan de Gestion de Residuos Solidos (PGIRS)", "area": "Gestion Ambiental", "ref": "Ley Ambiental", "norma": "AMBIENTAL", "desc": "Manejo de residuos.", "justificacion": "ISO 14001:8.1 - Control operacional del proceso de residuos.", "instrucciones": "Manual de separacion en la fuente y disposicion final de residuos."},
            {"doc": "Programa de Uso Eficiente de Agua y Energia", "area": "Operaciones", "ref": "Sostenibilidad", "norma": "AMBIENTAL", "desc": "Ahorro de recursos.", "justificacion": "ISO 14001:8.1 - Gestion del consumo de recursos naturales.", "instrucciones": "Plan de reduccion de consumos con indicadores mensuales."},
            {"doc": "Plan de Respuesta a Emergencias Ambientales", "area": "Operaciones", "ref": "ISO 14001:8.2", "norma": "AMBIENTAL", "desc": "Mitigacion de derrames.", "justificacion": "ISO 14001:8.2 - Preparacion y respuesta ante emergencias.", "instrucciones": "Procedimiento de actuacion ante posibles accidentes ambientales."}
        ]
    if "Calidad" in str(normas_activas):
        norm_cartas += [
            {"doc": "Contexto Organizacional", "area": "Calidad", "ref": "ISO 9001:4.1", "norma": "CALIDAD", "desc": "Analisis de entorno (DOFA).", "justificacion": "ISO 9001:4.1 - Requisito fundamental para entender las cuestiones externas e internas que afectan al SGC.", "instrucciones": "Realice una matriz DOFA que analice Debilidades, Oportunidades, Fortalezas y Amenazas de la empresa."},
            {"doc": "Mapa de Procesos", "area": "Operaciones", "ref": "ISO 9001:4.4", "norma": "CALIDAD", "desc": "Interaccion de procesos.", "justificacion": "ISO 9001:4.4 - Exigido para demostrar el enfoque basado en procesos y su interaccion.", "instrucciones": "Grafique los procesos estrategicos, misionales y de soporte de la entidad."}
        ]
    
    cartas_todas = norm_cartas if norm_cartas else base_cartas
    
    # Si la norma es calidad, mezclamos con base. Si no, prevalece el marco específico.
    if "Calidad" in str(normas_activas) and norm_cartas:
        # Evitar duplicados si Calidad ya añadió algo
        existentes = [c['doc'] for c in norm_cartas]
        base_extra = [c for c in base_cartas if c['doc'] not in existentes]
        cartas_todas = norm_cartas + base_extra
    
    # --- LOGICA DE PROPORCIONALIDAD V9.0 (LEAN AUDIT) ---
    # Una empresa es 'Startup/Micro' si tiene <=10 empleados (independientemente del label de tamaño)
    es_startup = st.session_state['empresa_personal'] <= 10
    
    # Clasificación de Documentos Vitales (Soportan el 100% en modo Lean)
    docs_vitales = [
        "Camara de Comercio (Existencia Legal)", "RUT (Registro Unico Tributario)", 
        "Acta de Compromiso Directivo", "Mision y Vision Corporativa", 
        "Contexto Organizacional", "Mapa de Procesos", "Politica de Seguridad", 
        "PEI (Proyecto Educativo)", "Aspectos Ambientales",
        "Declaracion de Aplicabilidad (SoA)", "Matriz de Requisitos Legales Ambientales",
        "Manual de Convivencia", "Informe de Autoevaluacion Institucional"
    ]
    
    for c in cartas_todas:
        if c['doc'] in docs_vitales:
            c['prioridad'] = "VITAL (Obligatorio)"
        else:
            c['prioridad'] = "SOPORTE (Recomendado)" if not es_startup else "LEAN (Opcional)"

    total_total = len(cartas_todas)
    
    # --- FUNCIONES VISUALES DASHBOARD (V9.3) ---
    def draw_donut(value, label, color):
        fig = go.Figure(go.Pie(
            values=[value, 100-value if value <= 100 else 0],
            labels=["", ""],
            hole=0.75,
            marker_colors=[color, "rgba(255,255,255,0.05)"],
            sort=False
        ))
        fig.update_traces(textinfo='none', hoverinfo='none')
        fig.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=10, r=10),
            height=120, # Compacto para Zero-Scroll
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[dict(text=f"{int(value)}%", x=0.5, y=0.5, font_size=18, font_color="white", font_family="Orbitron", showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"<p style='text-align: center; color: #94A3B8; font-family: Orbitron; font-size: 0.6rem; margin-top: -15px;'>{label}</p>", unsafe_allow_html=True)

    # --- MOTOR DE CÁLCULO UNIFICADO V9.0 (JUSTIFICACIONES N/A) ---
    if 'justificados' not in st.session_state: st.session_state['justificados'] = []
    
    # Métricas Globales para Fase A y B
    fase_a_reqs_g = [st.session_state.get('auditor_name'), st.session_state.get('rep_legal'), st.session_state.get('rep_id')]
    pct_fase_a = int((sum(1 for r in fase_a_reqs_g if r) / 3) * 100)
    
    fase_b_reqs_g = [
        st.session_state.get('empresa_tamanio') != "Pyme (1-50 emp)",
        st.session_state.get('empresa_personal', 0) > 0,
        bool(st.session_state.get('empresa_direccion', ""))
    ]
    pct_fase_b = int((sum(1 for r in fase_b_reqs_g if r) / 3) * 100)

    docs_en_expediente = list(st.session_state['expediente'].keys())
    docs_validados = list(set(docs_en_expediente + st.session_state['justificados']))
    
    count_exp = len([d for d in docs_validados if any(c['doc'] == d for c in cartas_todas)])
    
    # --- PROGRESO SEGMENTADO POR NORMA V12.0 ---
    normas_resumen = {}
    _normas_iter = normas_activas if normas_activas else [st.session_state.get('norma', 'ISO 9001:2015')]
    for n in _normas_iter:
        n_tag = n.upper().replace("ISO 9001:2015", "CALIDAD").replace("ISO 27001", "SEGURIDAD").replace("ISO 14001", "AMBIENTAL")
        docs_n = [c for c in cartas_todas if c.get('norma') == n_tag]
        if not docs_n: docs_n = [c for c in cartas_todas if c.get('norma') == 'SIG']  # Fallback a base
        
        vitales_n = [c for c in docs_n if c.get('prioridad') == "VITAL (Obligatorio)"]
        count_vitales_n = len([d for d in docs_validados if any(c['doc'] == d for c in vitales_n)])
        pct_n = int((count_vitales_n / len(vitales_n)) * 100) if vitales_n else 100
        normas_resumen[n] = pct_n

    # En modo Startup, solo los vitales cuentan para el progreso del 100% de la fase
    if es_startup:
        vitales_en_cartas = [c for c in cartas_todas if c['prioridad'] == "VITAL (Obligatorio)"]
        total_a_evaluar = len(vitales_en_cartas) if vitales_en_cartas else 1
        cargados_vitales = len([d for d in docs_validados if any(c['doc'] == d and c['prioridad'] == "VITAL (Obligatorio)" for c in cartas_todas)])
        pct_fase_c = int((cargados_vitales / total_a_evaluar) * 100)
    else:
        pct_fase_c = int((count_exp / total_total) * 100) if total_total > 0 else 0
    pct_total = int((pct_fase_a + pct_fase_b + pct_fase_c) / 3)

    # Variables de compatibilidad Unificadas (V9.3)
    progreso_total = pct_total / 100
    progreso_global = float(pct_total)
    progreso_c = (count_exp / total_total) if total_total > 0 else 0
    fase_a_ready = (pct_fase_a == 100)
    fase_b_ready = (pct_fase_b == 100)

    # --- MOTOR DE HALLAZGOS Y COHERENCIA V12.0 ---
    if 'hallazgos_manuales' not in st.session_state: st.session_state['hallazgos_manuales'] = {}
    todos_hallazgos = []
    coherencias_vitales = []
    for doc, data in st.session_state['expediente'].items():
        if isinstance(data, dict):
            # Coherencia para blindaje
            if any(c['doc'] == doc and c['prioridad'] == "VITAL (Obligatorio)" for c in cartas_todas):
                coherencias_vitales.append(data.get('coherencia', 0))
            
            # Hallazgos consolidado
            for h in data.get('hallazgos', []):
                todos_hallazgos.append({"doc": doc, "hallazgo": h})
    
    coherencia_media_vital = (sum(coherencias_vitales) / len(coherencias_vitales)) if coherencias_vitales else 0
    es_rigor_ok = coherencia_media_vital >= 60

    # --- SIDEBAR MASTER (V4.5 ELITE) ---
    with st.sidebar:
        # LOGO Y DATOS EMPRESA
        _logo = st.session_state.get('logo_path')
        logo_disp = _logo if _logo and os.path.exists(_logo) else None
        if logo_disp: st.image(logo_disp, width=150)
        else: st.markdown(f"<h2 style='text-shadow: 0 0 10px #00C2FF;'>{company[:15]}</h2>", unsafe_allow_html=True)
        
        st.markdown(f"**Marco:** <span style='color:#00C2FF;'>{st.session_state['norma']}</span>", unsafe_allow_html=True)
        st.divider()

        # NAVEGACIÓN BASADA EN ROL
        is_colab = st.session_state['user_role'] in ["responsable", "juridica", "finanzas"]
        
        if is_colab:
            opciones = ["📋 Portal de Entrega", "💎 Help Center Elite"]
            menu = st.radio("MI TRABAJO:", opciones, key="main_menu_colab")
        else:
            opciones = [
                f"🗺️ Camino de Ingesta [{pct_fase_c}%]",
                f"📊 Dashboard Analítico [{pct_total}%]",
                "📋 Requerimientos Maestros",
                "⚖️ Emisión de Formatos",
                "💎 Help Center Elite"
            ]
            menu_raw = st.radio("FLUJO DE TRABAJO:", opciones, key="main_menu_auditor")
            menu = menu_raw.split(" [")[0]
            
            # Selector de Rol del Auditor (Counselor)
            roles_disponibles = ["Administrador (Global)", "⚖️ Jurídico", "🏦 Alta Dirección", "📊 Calidad / SIG", "🛡️ Ciberseguridad", "♻️ Gestión Ambiental", "🎓 Gestión Académica", "👥 Talento Humano", "💰 Financiera", "⚙️ Operaciones"]
            st.session_state['user_role_active'] = st.selectbox("👤 PERFIL DE CONSULTA:", roles_disponibles, index=0)

        st.divider()
        
        # USUARIO Y SESIÓN
        _auth = st.session_state.get('auth', {})
        if _auth:
            st.markdown(f"""
            <div style='background:rgba(0,194,255,0.05);border:1px solid rgba(0,194,255,0.1);
                        border-radius:12px;padding:0.75rem;margin-bottom:1rem;'>
                <span style='color:#94A3B8;font-size:0.65rem;letter-spacing:1.5px;'>LOGUEADO COMO</span><br>
                <span style='color:#00C2FF;font-weight:700;font-size:0.9rem;'>{_auth.get('nombre','User')}</span><br>
                <span style='color:#475569;font-size:0.7rem;'>ROL: {_auth.get('rol','visitante').upper()}</span>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🚪 CERRAR SESIÓN", use_container_width=True, type="secondary"):
            st.session_state['auth'] = None
            st.session_state['env'] = None
            st.session_state['company_name'] = ""
            st.rerun()

        # HUB DE SIMULACIÓN ADMIN (V19.1)
        if st.session_state['user_role'] == "Administrador (Global)":
            st.markdown("---")
            with st.expander("🏰 HUB DE SIMULACIÓN Multi-Norma"):
                st.caption("Poblamiento determinístico para Demos de Venta.")
                sim_norm = st.selectbox("Norma a Simular", ["CALIDAD", "SEGURIDAD", "AMBIENTAL", "ACADEMICO"], key="sim_norm_sel")
                if st.button("🚀 INYECTAR ECOSISTEMA REALISTA", use_container_width=True):
                    from HMO_Simulation_Engine import HMOSimulationEngine
                    sim_engine = HMOSimulationEngine(st.session_state['base_path'])
                    with st.spinner(f"Simulando {sim_norm}..."):
                        success, log = sim_engine.simulate_norm_ecosystem(sim_norm, company, st.session_state['empresa_objeto'])
                        if success:
                            for entry in log:
                                st.session_state['expediente'][entry['doc']] = {"score": 100, "file_path": entry['path'], "validado": True}
                            save_audit_state()
                            st.success(f"{sim_norm} Inyectado.")
                            st.rerun()
                        else:
                            st.error(log)

        # ACCIONES RÁPIDAS
        if not is_colab:
            if st.button("🔄 Actualizar Datos", use_container_width=True):
                save_audit_state(); st.rerun()

    # --- MOTOR DE GENERACIÓN IA (Borradores V16-V17) ---
    def ui_generar_borrador_ia(doc_name, area, justificacion):
        st.markdown(f"<div style='background:rgba(0,194,255,0.05); padding:0.8rem; border-radius:10px; border:1px dashed rgba(0,194,255,0.4);'>", unsafe_allow_html=True)
        st.caption(f"🤖 **Asistente IA:** Redacción automática para {doc_name}")
        
        info_doc = st.session_state['expediente'].get(doc_name, {})
        is_signed = info_doc.get('signed', False)
        
        c_i1, c_i2 = st.columns(2)
        with c_i1:
            if st.button(f"🪄 PROPUESTA IA", key=f"btn_draft_{doc_name}", use_container_width=True, disabled=is_signed):
                with st.spinner("Generando borrador normativo..."):
                    engine = HMO_AI_Engine()
                    draft_text = engine.generate_draft_text(doc_name, company, st.session_state['empresa_sector'], st.session_state['empresa_objeto'])
                    from HMO_PDF_Generator import generate_ai_draft_pdf
                    pdf_path = generate_ai_draft_pdf(doc_name, draft_text, st.session_state['base_path'], company=company, justification=justificacion)
                    st.session_state['expediente'][doc_name] = {"score": 85, "validado": True, "ia_draft": True, "draft_text": draft_text}
                    save_audit_state()
                    st.success(f"✅ Borrador generado")
                    st.rerun()
        
        with c_i2:
            if info_doc.get('ia_draft') and not is_signed:
                if st.button("✍️ NORMALIZAR Y FIRMAR", key=f"btn_sign_{doc_name}", use_container_width=True, type="primary"):
                    with st.spinner("Normalizando documento SGC..."):
                        from HMO_PDF_Generator import generate_ai_draft_pdf
                        signer = {"user": st.session_state['auth'].get('nombre', 'Responsable'), "role": st.session_state['user_role']}
                        pdf_path = generate_ai_draft_pdf(
                            doc_name, info_doc['draft_text'], st.session_state['base_path'], 
                            company=company, justification=justificacion, signer_data=signer
                        )
                        st.session_state['expediente'][doc_name]['signed'] = True
                        st.session_state['expediente'][doc_name]['file_path'] = pdf_path
                        save_audit_state()
                        st.success("✅ Documento Firmado")
                        st.rerun()
            elif is_signed:
                st.info("✅ Firmado y Validado")
                if st.session_state['expediente'][doc_name].get('file_path'):
                    with open(st.session_state['expediente'][doc_name]['file_path'], "rb") as f:
                        st.download_button("📂 Descargar Certificado", f, file_name=os.path.basename(st.session_state['expediente'][doc_name]['file_path']), use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # --- BOTÓN ACTUALIZAR APP V10.0 ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <style>
    /* Fuerza texto visible en botón sidebar siempre */
    section[data-testid="stSidebar"] button {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background: rgba(0,194,255,0.15) !important;
        border-color: rgba(0,194,255,0.5) !important;
        color: #00C2FF !important;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.sidebar.button("🔄 Actualizar App", use_container_width=True,
                         help="Descarga la última versión desde el repositorio central."):
        with st.sidebar:
            with st.spinner("Actualizando desde repositorio..."):
                try:
                    import subprocess
                    _pull = subprocess.run(
                        ["git", "fetch", "--all"],
                        capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__))
                    )
                    _reset = subprocess.run(
                        ["git", "reset", "--hard", "origin/main"],
                        capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__))
                    )
                    if "Already up to date" in _pull.stdout:
                        st.success("✅ Ya tienes la última versión.")
                    elif _pull.returncode == 0:
                        st.success("✅ App actualizada. Recarga la página (F5).")
                    else:
                        st.warning(f"⚠️ Git: {_pull.stderr[:120]}")
                except Exception as _ge:
                    st.error(f"Error: {_ge}")

    # Filtrado Dinámico por Rol & Gobernanza V9.6
    ROLE_AREA_MAP = {
        "⚖️ Jurídico": "Juridico",
        "🏦 Alta Dirección": "Alta Direccion",
        "📊 Calidad / SIG": "Calidad",
        "🛡️ Ciberseguridad": "Ciberseguridad",
        "♻️ Gestión Ambiental": "Gestion Ambiental",
        "🎓 Gestión Académica": "Gestion Academica",
        "👥 Talento Humano": "Talento Humano",
        "💰 Financiera": "Financiera",
        "⚙️ Operaciones": "Operaciones"
    }

    if st.session_state['user_role'] == "Administrador (Global)":
        cartas = cartas_todas
    else:
        target_area = ROLE_AREA_MAP.get(st.session_state['user_role'], "")
        # Filtro 1: Segmentación por Área (Búsqueda flexible)
        cartas_base = [c for c in cartas_todas if target_area.lower() in str(c['area']).lower()]
        if not cartas_base: cartas_base = cartas_todas
        
        # Filtro 2: Exclusión de documentos N/A (Justificados por Admin)
        cartas = [c for c in cartas_base if c['doc'] not in st.session_state.get('justificados', [])]

    # Eliminación de redundancias de cálculo para evitar NameErrors (Corte V9.3)

    # --- SECCIÓN: REQUERIMIENTOS MAESTROS ---
    if menu == "📋 Requerimientos Maestros":
        st.markdown(f"<h1 class='norm-header'>📋 Lista Maestra de Requerimientos</h1>", unsafe_allow_html=True)
        st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
        st.write(f"### Requisitos del Marco: {st.session_state['norma']}")
        st.info("Esta lista representa la materia prima necesaria para que el sistema genere los formatos oficiales.")
        
        df_req = pd.DataFrame(cartas_todas)[["doc", "area", "prioridad", "instrucciones"]]
        df_req.columns = ["📚 Documento Requerido", "🏢 Área Responsable", "🔗 Ref. Normativa", "📝 Descripción del Control"]
        st.dataframe(df_req, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
        st.write("### 🔑 Guía de Acción Directa")
        st.markdown("""
        - **Paso 1**: Identifique el área responsable en su organización.
        - **Paso 2**: Recupere el documento en formato PDF o Word.
        - **Paso 3**: Diríjase al **Camino de Ingesta (HITL)** para cargar la evidencia.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif menu == "📊 Dashboard Analítico":
        # --- CÁLCULO V15 ---
        engine = HMO_AI_Engine()
        chs = engine.calculate_corporate_health_score(st.session_state)
        
        # Definición global de estados para Radar V21.1
        fase_a_ready = st.session_state.get('expediente', {}).get("Camara de Comercio (Existencia Legal)") and \
                       st.session_state.get('expediente', {}).get("RUT (Registro Unico Tributario)")
        
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;'>
            <h2 style='margin:0; font-family:Orbitron;'>📊 DASHBOARD ANALYTICS V17</h2>
            <div style='background:rgba(255,255,255,0.05); border:1px solid {chs['color']}44; border-radius:10px; padding:0.4rem 1rem;'>
                <span style='color:{chs['color']}; font-weight:700; font-family:Orbitron;'>{chs['score']}% - {chs['level']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # TABLERO DE SUPERVISIÓN (V17.0 - Solo Admin)
        if st.session_state['user_role'] == "Administrador (Global)":
            with st.expander("🏰 TABLERO DE SUPERVISIÓN ELITE (MAESTRO)", expanded=False):
                st.write("### Avance en tiempo real por área")
                _areas = list(set([c.get('area') for c in cartas_todas if c.get('area')]))
                _cols_sup = st.columns(len(_areas))
                for _idx, _ar in enumerate(_areas):
                    _docs_ar = [c for c in cartas_todas if c.get('area') == _ar]
                    _ok_ar = len([d for d in _docs_ar if d['doc'] in st.session_state['expediente']])
                    _pct_ar = int((_ok_ar / len(_docs_ar)) * 100) if _docs_ar else 100
                    with _cols_sup[_idx]:
                        st.markdown(f"<div style='text-align:center; font-size:0.7rem;'><b>{_ar.upper()}</b></div>", unsafe_allow_html=True)
                        draw_donut(_pct_ar, f"{_ok_ar}/{len(_docs_ar)}", "#10B981" if _pct_ar == 100 else "#00C2FF")
                st.divider()
        
        # --- COMMAND CENTER KIPs (V20.0) ---
        c1, c2, c3, c4 = st.columns(4)
        
        # Calcular Días para Cierre
        dias_restantes = 0
        if st.session_state.get('fecha_compromiso'):
            try:
                target_date = datetime.datetime.strptime(st.session_state['fecha_compromiso'], "%Y-%m-%d").date()
                dias_restantes = (target_date - datetime.date.today()).days
            except: pass
            
        # Calcular Deltas de Progreso (Comparativa con último Snapshot si existe)
        prev_score = st.session_state['history_chs'][-1]['score'] if st.session_state.get('history_chs') else chs['score']
        delta_score = chs['score'] - prev_score
        
        def kpi_card(label, value, delta=None, color="#00C2FF", unit=""):
            delta_html = ""
            if delta is not None:
                d_color = "#10B981" if delta >= 0 else "#F87171"
                d_icon = "▴" if delta >= 0 else "▾"
                delta_html = f"<span style='color:{d_color}; font-size:0.75rem; margin-left:5px;'>{d_icon} {abs(delta)}{unit}</span>"
            
            st.markdown(f"""
            <div class='elite-card' style='text-align:center; padding:0.6rem !important;'>
                <p style='font-size:0.65rem; color:#94A3B8; margin-bottom:0px; font-weight:700;'>{label.upper()}</p>
                <div style='display:flex; justify-content:center; align-items:baseline;'>
                    <span style='font-size:1.6rem; font-weight:700; color:{color}; font-family:Orbitron;'>{value}</span>{delta_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c1: kpi_card("Corporate Health", f"{chs['score']}%", delta=delta_score, color=chs['color'], unit="%")
        with c2: kpi_card("Docs Validados", len(st.session_state['expediente']), delta=len(st.session_state['expediente']), color="#10B981")
        with c3: kpi_card("Días p/ Cierre", max(0, dias_restantes), delta=-1 if dias_restantes > 0 else 0, color="#F59E0B")
        with c4:
            if st.button("📊 REPORTE ELITE", use_container_width=True):
                _path = generate_maturity_report_pdf(company, st.session_state['base_path'], chs['score'], chs['level'])
                st.toast(f"Reporte Generado: {os.path.basename(_path)}")
            if st.button("💾 SNAPSHOT", use_container_width=True, type="primary"):
                snapshot = {"fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "score": chs['score'], "level": chs['level']}
                st.session_state['history_chs'].append(snapshot)
                save_audit_state(); st.rerun()

        st.divider()
        
        # --- ANALÍTICA AVANZADA (SIDE-BY-SIDE) ---
        col_g1, col_g2 = st.columns([1.5, 1])
        
        with col_g1:
            st.markdown("<div class='elite-card' style='padding: 0.8rem;'><b>📈 Tendencia de Madurez Corporativa</b>", unsafe_allow_html=True)
            if st.session_state.get('history_chs'):
                df_hist = pd.DataFrame(st.session_state['history_chs'])
                fig_hist = px.area(df_hist, x="fecha", y="score", markers=True, color_discrete_sequence=['#00C2FF'])
                fig_hist.update_layout(
                    height=200, margin=dict(t=10, b=0, l=0, r=0), 
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, color="#94A3B8", tickfont=dict(size=9)), 
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color="#94A3B8", tickfont=dict(size=9), range=[0, 105])
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.info("No hay registros históricos para graficar tendencia.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_g2:
            st.markdown("<div class='elite-card' style='padding: 0.8rem;'><b>🛡️ Radar de Madurez SGC</b>", unsafe_allow_html=True)
            labels_rad = ['Identidad', 'Estrategia', 'Operación', 'Jurídico', 'Financiero', 'Calidad']
            # Valores reales basados en el expediente
            val_id = 100 if fase_a_ready else 0
            val_est = 100 if "Mision y Vision Corporativa" in st.session_state['expediente'] else 0
            val_ops = 100 if "Mapa de Procesos" in st.session_state['expediente'] else 0
            val_jur = 100 if "Camara de Comercio (Existencia Legal)" in st.session_state['expediente'] else 0
            val_fin = 100 if "RUT (Registro Unico Tributario)" in st.session_state['expediente'] else 0
            val_cal = pct_fase_c
            
            values_rad = [val_id, val_est, val_ops, val_jur, val_fin, val_cal]
            fig_rad = go.Figure(data=go.Scatterpolar(r=values_rad, theta=labels_rad, fill='toself', line_color='#A855F7', fillcolor='rgba(168, 85, 247, 0.2)'))
            fig_rad.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)", tickfont=dict(size=8)), angularaxis=dict(tickfont=dict(size=8))), 
                showlegend=False, height=200, margin=dict(l=30, r=30, t=20, b=10), paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_rad, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_h2:
            st.write("### 📸 Punto de Control")
            if st.button("💾 GUARDAR SNAPSHOT ACTUAL", use_container_width=True, type="primary"):
                snapshot = {
                    "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "score": chs['score'],
                    "level": chs['level']
                }
                st.session_state['history_chs'].append(snapshot)
                save_audit_state()
                st.success("Snapshot guardado exitosamente.")
                st.rerun()
            
            # Auto-Certificación Platinum
            if chs['score'] >= 86:
                st.markdown("<div style='background:linear-gradient(135deg, #E5E4E2 0%, #94A3B8 100%); padding:1rem; border-radius:10px; color:#0F172A; text-align:center;'>", unsafe_allow_html=True)
                st.write("🏆 **EXCELENCIA PLATINUM**")
                st.caption("Su organización cumple con los más altos estándares SGC.")
                if st.button("🎓 DESCARGAR DIPLOMA", use_container_width=True):
                    st.toast("Generando Diploma de Excelencia...")
                st.markdown("</div>", unsafe_allow_html=True)
        
        # --- LOG DE TRAZABILIDAD Y VERSIONES (V17.0) ---
        st.markdown("---")
        with st.expander("📝 LOG DE TRAZABILIDAD Y VERSIONAMIENTO (CONTROL DE CAMBIOS)", expanded=True):
            st.write("Historial de aprobación y normalización de documentos institucionales.")
            
            signed_docs = []
            for d_name, d_val in st.session_state['expediente'].items():
                if isinstance(d_val, dict) and d_val.get('signed'):
                    signed_docs.append({
                        "Documento": d_name,
                        "Versión": "1.0",
                        "Estatus": "APROBADO",
                        "Verificación": "NORMALIZADO SGC"
                    })
            
            if signed_docs:
                st.table(pd.DataFrame(signed_docs))
            else:
                st.info("No hay documentos normalizados con firma digital en este ciclo.")

        # --- FICHA TÉCNICA Y ESTATUS (GRID COMPACTO) ---
        cf1, cf2, cf3 = st.columns([1, 1, 1.2])
        
        with cf1:
            st.markdown("<div class='elite-card' style='padding: 0.6rem;'><b>📊 Estatus por Áreas</b>", unsafe_allow_html=True)
            _areas = ["Jurídico", "Financiera", "Talento Humano", "Operaciones"]
            for _ar in _areas:
                _docs_ar = [c for c in cartas_todas if c.get('area') == _ar]
                _ok_ar = len([d for d in _docs_ar if d['doc'] in st.session_state['expediente']])
                _pct_ar = int((_ok_ar / len(_docs_ar)) * 100) if _docs_ar else 100
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.2rem;'>
                    <span style='font-size:0.7rem;'>{_ar}</span>
                    <span style='font-size:0.7rem; color:#00C2FF; font-weight:700;'>{_pct_ar}%</span>
                </div>
                <div style='width:100%; background:rgba(255,255,255,0.05); height:4px; border-radius:2px;'>
                    <div style='width:{_pct_ar}%; background:#10B981; height:4px; border-radius:2px;'></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with cf2:
            st.markdown("<div class='elite-card' style='padding: 0.6rem;'><b>🏢 Ficha Corporativa</b>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='font-size:0.75rem; line-height:1.4;'>
                <b>Nit:</b> {st.session_state['empresa_nit']}<br>
                <b>Sector:</b> {st.session_state['empresa_sector']}<br>
                <b>Personal:</b> {st.session_state['empresa_personal']}<br>
                <b>Ubicación:</b> {st.session_state['empresa_direccion'][:30]}...
            </div>
            """, unsafe_allow_html=True)
            if "Organigrama Funcional" in st.session_state['expediente']:
                data_org = dict(character=["G.G", "Ops", "SIG"], parent=["", "G.G", "Ops"], value=[10, 8, 3])
                fig_org = px.treemap(data_org, names='character', parents='parent', values='value', color_discrete_sequence=['#A855F7', '#1e3a8a'])
                fig_org.update_layout(margin=dict(t=5, l=5, r=5, b=5), height=65, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_org, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with cf3:
            st.markdown("<div class='elite-card' style='padding: 0.6rem;'><b>💎 Requerimientos Vitales</b>", unsafe_allow_html=True)
            vitales = [c for c in cartas_todas if c.get('prioridad') == "VITAL (Obligatorio)"][:5]
            for v in vitales:
                cargado = v['doc'] in st.session_state['expediente']
                icon = "✅" if cargado else "⏳"
                st.markdown(f"<p style='font-size:0.7rem; margin:0;'>{icon} {v['doc'][:30]}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- PANEL DE HALLAZGOS CONSOLIDADO V12.0 ---
        st.markdown("---")
        # --- PANEL DE HALLAZGOS ELITE (V20.0) ---
        st.markdown("<div class='elite-card' style='padding:0.8rem;'><b>🔍 Centro de Hallazgos y Resultados de Auditoría</b>", unsafe_allow_html=True)
        if not todos_hallazgos:
            st.info("Sin anomalías detectadas. Continúe con la validación documental.")
        else:
            ch_col1, ch_col2 = st.columns([1.8, 1])
            with ch_col1:
                for h_item in todos_hallazgos[:5]: # Top 5 prioritarios
                    doc = h_item['doc']
                    h_txt = h_item['hallazgo']
                    h_key = f"{doc}_{h_txt}"[:50]
                    cat = st.session_state['hallazgos_manuales'].get(h_key, "Detectado")
                    h_color = "#F87171" if cat == "No Conformidad" else ("#F59E0B" if cat == "Observación" else "#10B981")
                    
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.02); border-left:3px solid {h_color}; padding:0.4rem; border-radius:4px; margin-bottom:0.3rem;'>
                        <p style='font-size:0.75rem; color:#FFFFFF; margin:0;'><b>[{doc[:15]}]</b>: {h_txt[:80]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with ch_col2:
                ncs = sum(1 for v in st.session_state['hallazgos_manuales'].values() if v == "No Conformidad")
                obs = sum(1 for v in st.session_state['hallazgos_manuales'].values() if v == "Observación")
                fors = sum(1 for v in st.session_state['hallazgos_manuales'].values() if v == "Fortaleza")
                
                st.markdown(f"""
                <div style='display:flex; justify-content:space-around; text-align:center;'>
                    <div><b style='color:#F87171;'>{ncs}</b><br><span style='font-size:0.6rem;'>NC</span></div>
                    <div><b style='color:#F59E0B;'>{obs}</b><br><span style='font-size:0.6rem;'>OBS</span></div>
                    <div><b style='color:#10B981;'>{fors}</b><br><span style='font-size:0.6rem;'>FOR</span></div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🔧 GESTIONAR TODO", use_container_width=True):
                    st.toast("Abriendo Panel Maestro de Hallazgos...")
        st.markdown("</div>", unsafe_allow_html=True)

        # --- MÓDULO DE PLANES DE ACCIÓN (V17.0 - MEJORA CONTINUA) ---
        st.markdown("---")
        with st.expander("🛠️ GESTIÓN DE PLANES DE ACCIÓN (MEJORA CONTINUA)", expanded=False):
            st.write("Convierta sus Hallazgos / No Conformidades en tareas preventivas y correctivas.")
            
            hallazgos_nc = [h for h, cat in st.session_state.get('hallazgos_manuales', {}).items() if cat == "No Conformidad"]
            
            if not hallazgos_nc:
                st.success("✨ No se han categorizado No Conformidades. El sistema está en equilibrio operativo.")
            else:
                for h_key in hallazgos_nc:
                    st.markdown(f"<div style='border-left: 4px solid #F87171; padding-left: 1rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)
                    st.write(f"**Hallazgo de Origen:** {h_key}")
                    
                    p_data = st.session_state['plan_accion'].get(h_key, {"accion": "", "resp": "Calidad", "fecha": datetime.date.today()})
                    
                    c_p1, c_p2, c_p3 = st.columns([2, 1, 1])
                    
                    # Botón IA de Sugerencia
                    if c_p1.button("🤖 Sugerir con IA", key=f"ai_sugg_{h_key}"):
                        with st.spinner("IA analizando No Conformidad..."):
                            ia_engine = HMO_AI_Engine()
                            p_data['accion'] = ia_engine.suggest_corrective_action(h_key, st.session_state['norma'])
                            st.session_state['plan_accion'][h_key] = p_data
                            save_audit_state()
                            st.rerun()

                    accion = c_p1.text_input("Acción Correctiva Propuesta", value=p_data['accion'], placeholder="Ej: Capacitación en proceso...", key=f"plan_input_{h_key}")
                    resp_plan = c_p2.selectbox("Cierre Responsable", ["Calidad", "Líder Proceso", "Gerencia"], index=["Calidad", "Líder Proceso", "Gerencia"].index(p_data['resp']), key=f"resp_plan_input_{h_key}")
                    fecha_plan = c_p3.date_input("Compromiso Cierre", value=p_data['fecha'], key=f"date_plan_input_{h_key}")
                    
                    if accion != p_data['accion'] or resp_plan != p_data['resp'] or fecha_plan != p_data['fecha']:
                        st.session_state['plan_accion'][h_key] = {"accion": accion, "resp": resp_plan, "fecha": fecha_plan}
                        save_audit_state()
                        st.toast("Mejora guardada")
                    
                    if accion:
                        st.caption(f"🚀 Tarea programada para: {fecha_plan.strftime('%Y-%m-%d')} | Responsable: {resp_plan}")
                    st.markdown("</div>", unsafe_allow_html=True)

    # --- SECCIÓN: INGESTA DE MATERIA PRIMA (HITL) ---
    elif menu == "🗺️ Camino de Ingesta":
        st.markdown("<h2 style='text-align:center;'>🗺️ CAMINO DE INGESTA V21.13 ELITE</h2>", unsafe_allow_html=True)
        
        # Selector de Fases V15
        if 'ing_f' not in st.session_state: st.session_state['ing_f'] = 'A'
        f = st.session_state['ing_f']
        
        c1, c2, c3, c4 = st.columns(4)
        
        # Estilos Dinámicos Wizard Elite
        def phase_btn(label, target, current, pct):
            is_active = current == target
            is_done = pct == 100
            
            # Emoji de estado
            prefix = "✅ " if is_done else ("🔵 " if is_active else "⚪ ")
            btn_label = f"{prefix}{label}\n{pct}%"
            
            btn_type = "primary" if is_active else "secondary"
            if st.button(btn_label, use_container_width=True, type=btn_type, key=f"btn_fase_{target}"):
                st.session_state['ing_f'] = target
                st.rerun()

        with c1: phase_btn("FASE A\nIdentidad", 'A', f, pct_fase_a)
        with c2: phase_btn("FASE B\nDimensión", 'B', f, pct_fase_b)
        with c3: phase_btn("FASE C\nRevisión", 'C', f, pct_fase_c)
        with c4: phase_btn("FINAL\nCierre", 'FINAL', f, 100 if st.session_state.get('revisado_plantillas') else 0)

        if f == 'A':
            # Estado de validación (V21.3)
            cc_ready = st.session_state.get('expediente', {}).get("Camara de Comercio (Existencia Legal)") is not None
            rut_ready = st.session_state.get('expediente', {}).get("RUT (Registro Unico Tributario)") is not None

            st.markdown("<div class='elite-card' style='border-top: 3px solid #00C2FF; padding: 0.5rem;'>", unsafe_allow_html=True)
            st.markdown("##### 🏢 FASE A: IDENTIFICACIÓN CORPORATIVA")
            st.caption("Validación Documental Obligatoria (CC y RUT)")
            
            c_doc_a, c_doc_b = st.columns(2)
            with c_doc_a:
                uploaded_cc = st.file_uploader("📂 SUBIR CÁMARA DE COMERCIO", type=["pdf", "jpg", "jpeg", "png"], key="smart_cc_v21.10")
                if uploaded_cc and not cc_ready:
                    with st.spinner("Validando CC..."):
                        res = procesar_documento(uploaded_cc.read(), uploaded_cc.name) if OCR_DISPONIBLE else {"tipo_doc":"unknown"}
                    if res.get("tipo_doc") == "camara_comercio":
                        for k,v in resultado_a_session_state(res).items(): st.session_state[k] = v
                        st.session_state['expediente']["Camara de Comercio (Existencia Legal)"] = {"validado":True}
                        save_audit_state(); st.rerun()
                elif cc_ready: st.success("✅ CC OK")

            with c_doc_b:
                uploaded_rut = st.file_uploader("📂 SUBIR RUT DIAN", type=["pdf", "jpg", "jpeg", "png"], key="smart_rut_v21.10")
                if uploaded_rut and not rut_ready:
                    with st.spinner("Validando RUT..."):
                        res_r = procesar_documento(uploaded_rut.read(), uploaded_rut.name) if OCR_DISPONIBLE else {"tipo_doc":"unknown"}
                    if res_r.get("tipo_doc") == "rut":
                        for k,v in resultado_a_session_state(res_r).items(): st.session_state[k] = v
                        st.session_state['expediente']["RUT (Registro Unico Tributario)"] = {"validado":True}
                        save_audit_state(); st.rerun()
                elif rut_ready: st.success("✅ RUT OK")
            st.markdown("</div>", unsafe_allow_html=True)

            # --- CAMPOS DE IDENTIDAD (RESTRICCIÓN ESTRICTA V21.2) ---
            if cc_ready and rut_ready:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<div class='elite-card' style='background:rgba(0,194,255,0.03); border: 1.5px dashed rgba(0,194,255,0.3);'>", unsafe_allow_html=True)
                st.markdown("##### 📝 Perfil de Auditoría (Edición Manual/HITL)")
                
                ci1, ci2 = st.columns(2)
                st.session_state['empresa_nombre'] = ci1.text_input("Nombre de la Empresa (Auto-poblado)", value=st.session_state.get('empresa_nombre',''), key="smart_name")
                # El campo auditor se inicializa vacío si no existe previamente
                if 'auditor_name' not in st.session_state: st.session_state['auditor_name'] = ""
                st.session_state['auditor_name'] = ci2.text_input("Auditor Líder (MANUAL OBLIGATORIO)", value=st.session_state.get('auditor_name',''), key="smart_aud", placeholder="Nombre completo del auditor")
                
                ci3, ci4 = st.columns(2)
                st.session_state['rep_legal'] = ci3.text_input("Representante Legal", value=st.session_state.get('rep_legal',''), key="smart_rep")
                st.session_state['rep_id'] = ci4.text_input("N° Identificación Representante", value=st.session_state.get('rep_id',''), key="smart_id")
                
                # Checkbox de re-carga
                if st.checkbox("🔄 Re-subir documentos base"):
                    st.session_state['expediente'].pop("Camara de Comercio (Existencia Legal)", None)
                    st.session_state['expediente'].pop("RUT (Registro Unico Tributario)", None)
                    save_audit_state(); st.rerun()

                # Botón de Avance habilitado solo con ambos documentos
                if cc_ready and rut_ready:
                    if st.button("💾 GUARDAR IDENTIDAD Y CONTINUAR", use_container_width=True, type="primary"):
                        if not st.session_state['auditor_name']:
                            st.error("Por favor, ingrese el nombre del Auditor Líder para continuar.")
                        else:
                            save_audit_state(); st.success("Identidad Guardada.")
                            st.session_state['ing_f'] = 'B'
                            st.rerun()
                else:
                    st.warning("⚠️ Se requieren AMBOS documentos (CC y RUT) cargados para avanzar a la Fase B.")
                    st.button("💾 GUARDAR IDENTIDAD Y CONTINUAR", disabled=True, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            # --- FASE B: DIMENSIÓN ---
        elif f == 'B':
            # --- FASE B: DIMENSIÓN (VERSION ZERO-SCROLL V19.2) ---
            st.markdown("##### 📊 Dimensión Organizacional & Contexto")
            col_b1, col_b2 = st.columns([1, 4])
            with col_b1:
                draw_donut(pct_fase_b, "AVANCE B", "#10B981")
            with col_b2:
                # Una sola fila para todos los descriptores
                cb1, cb2, cb3 = st.columns(3)
                st.session_state['empresa_tamanio'] = cb1.selectbox("Clasificación", ["Pyme (1-50 emp)", "Mediana (51-250 emp)", "Gran Empresa (+250 emp)"], index=0, key="b_size")
                st.session_state['empresa_personal'] = cb2.number_input("Total Personal", value=st.session_state['empresa_personal'], min_value=1, key="b_pers")
                st.session_state['empresa_sector'] = cb3.selectbox("Sector", ["Servicios", "Industrial", "Educativo", "Salud", "Tecnología"], index=0, key="b_sect")
                
                # Dirección compacta
                st.session_state['empresa_direccion'] = st.text_input("Dirección Domicilio Principal", value=st.session_state['empresa_direccion'], placeholder="Ej: Calle 123 # 45-67, Bogotá", key="b_dir")
            
            if st.button("💾 GUARDAR DIMENSIÓN Y CONTINUAR", use_container_width=True, type="primary"):
                save_audit_state(); st.success("Perfilado exitoso.")
                st.session_state['ing_f'] = 'C'
                st.rerun()

        elif f == 'C':
            st.markdown("##### ⚖️ Revisión Documental (ULTRA-DENSE V19.5)")
            
            # Resumen Compacto
            docs_cargados = len(st.session_state['expediente'])
            st.markdown(f"""
            <div style='background:rgba(0,194,255,0.03); border-radius:8px; padding:0.4rem 1rem; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:0.75rem;'><b>Avance:</b> {pct_fase_c}% ({docs_cargados}/{total_total})</span>
                <div style='width:50%; background:rgba(255,255,255,0.05); border-radius:10px; height:6px;'>
                    <div style='width:{pct_fase_c}%; background:#00C2FF; border-radius:10px; height:6px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Malla de Documentos 4 Columnas (Estilo Mockup)
            cols = st.columns(4)
            for i, doc in enumerate(cartas_todas):
                with cols[i % 4]:
                    doc_ready = doc['doc'] in st.session_state['expediente']
                    is_vital = doc.get('prioridad') == "VITAL (Obligatorio)"
                    
                    status_icon = "✅" if doc_ready else ("⏳" if is_vital else "📁")
                    status_color = "#10B981" if doc_ready else ("#00C2FF" if is_vital else "#475569")
                    
                    # Construcción Quirúrgica Tarjeta Fase C (V21.13)
                    st.markdown("<div class='fase-c-card'>", unsafe_allow_html=True)
                    
                    # 1. Cabecera Blindada
                    st.markdown(f"""
                    <div class='fase-c-cabecera' style='display:flex; align-items:center; gap:10px;'>
                        <span style='font-size:1.4rem; filter: drop-shadow(0 0 8px {status_color}); flex-shrink:0;'>{status_icon}</span>
                        <div style='display:flex; flex-direction:column; min-width:0;'>
                            <span style='font-size:0.6rem; color:#00C2FF; font-weight:900; text-transform:uppercase; letter-spacing:1.2px;'>{doc.get('area','GENERAL')}</span>
                            <span style='font-size:0.75rem; font-weight:700; color:#FFFFFF; line-height:1.2; overflow-wrap: break-word;'>{doc['doc']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not doc_ready:
                        # 2. Zona de Carga (Totalmente Transparente)
                        st.markdown("<div style='padding:0.4rem; background:transparent;'>", unsafe_allow_html=True)
                        _f = st.file_uploader("UP", key=f"up_v21.13_{i}", label_visibility="collapsed")
                        if _f:
                            with st.spinner(""):
                                st.session_state['expediente'][doc['doc']] = {"score": 90, "validado": True}
                                save_audit_state(); st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # 3. Footer Integrado (Toolbar)
                        st.markdown("<div class='fase-c-footer'>", unsafe_allow_html=True)
                        ca1, ca2, ca3 = st.columns(3)
                        with ca1: st.button("🤖", key=f"ia_v21.13_{i}", help="IA Suggest: Generar borrador", use_container_width=True)
                        with ca2: st.button("⚖️", key=f"jus_v21.13_{i}", help="Justificar: Nota narrativa", use_container_width=True)
                        with ca3: st.button("⏳", key=f"wait_v21.13_{i}", disabled=True, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        # Estado Validado: Interfaz de Gestión
                        st.markdown("<div style='padding:0.6rem; text-align:center; color:#10B981; font-weight:900; font-size:0.7rem; letter-spacing:1px;'>✅ VALIDADO</div>", unsafe_allow_html=True)
                        st.markdown("<div class='fase-c-footer'>", unsafe_allow_html=True)
                        ca1, ca2, ca3 = st.columns(3)
                        with ca1: st.button("🔍", key=f"view_v21.13_{i}", help="Visualizar", use_container_width=True)
                        with ca2:
                            is_jus = doc['doc'] in st.session_state['justificados']
                            if st.button("⚖️" if is_jus else "📜", key=f"jus_st_v21.13_{i}", help="Cambiar justificación", use_container_width=True):
                                if is_jus: st.session_state['justificados'].remove(doc['doc'])
                                else: st.session_state['justificados'].append(doc['doc'])
                                save_audit_state(); st.rerun()
                        with ca3:
                            if st.button("🗑️", key=f"del_v21.13_{i}", help="Resetear carga", use_container_width=True):
                                del st.session_state['expediente'][doc['doc']]
                                save_audit_state(); st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

        elif f == 'FINAL':
            st.markdown("##### 🏁 Cierre de Ingesta & Validación de Suficiencia")
            
            # Panel de Validación
            st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
            st.write("### 🔍 Checklist de Suficiencia SGC")
            
            docs_v_total = [c for c in cartas_todas if c.get('prioridad') == "VITAL (Obligatorio)"]
            docs_v_ok = [c for c in docs_v_total if c['doc'] in st.session_state['expediente']]
            docs_v_missing = [c for c in docs_v_total if c['doc'] not in st.session_state['expediente']]
            
            c_s1, c_s2 = st.columns([1, 2])
            with c_s1:
                draw_donut(int((len(docs_v_ok)/len(docs_v_total))*100), "VITALES", "#10B981")
            
            with c_s2:
                if not docs_v_missing:
                    st.success("✅ **Blindaje SGC Completo:** Todos los documentos vitales han sido cargados.")
                else:
                    st.warning(f"⚠️ **Pendiente:** Faltan {len(docs_v_missing)} documentos vitales para el blindaje reglamentario.")
                    with st.expander("Ver documentos faltantes"):
                        for m in docs_v_missing:
                            st.write(f"❌ {m['doc']}")
            
            st.divider()
            
            st.markdown("##### ⚖️ Autorización de Emisión")
            st.caption("Al habilitar esta opción, el sistema realizará el diligenciamiento IA de los formatos maestros.")
            st.session_state['autorizado_emision'] = st.toggle("HABILITAR EMISIÓN DE FORMATOS IA", value=st.session_state.get('autorizado_emision', False))
            
            if st.session_state['autorizado_emision']:
                if not docs_v_missing:
                    st.success("🚀 ESTATUS ELITE: Listo para emisión.")
                else:
                    st.info("💡 Puedes emitir, pero el cumplimiento se marcará como parcial.")
                
                if st.button("🏗️ IR A REVISIÓN DE FORMATOS", use_container_width=True, type="primary"):
                    st.session_state['main_menu_auditor'] = "⚖️ Emisión de Formatos [0%]" # Hack para navegar
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # --- SECCIÓN: FORMATOS ---

    # --- SECCIÓN: FORMATOS ---
    elif menu == "⚖️ Emisión de Formatos":
        st.markdown("<h1 class='norm-header'>⚖️ Emisión de Formatos & Títulos Legales</h1>", unsafe_allow_html=True)
        
        # Estado de Autorización
        if not st.session_state['autorizado_emision']:
            st.warning("🔒 ACCESO RESTRINGIDO A DILIGENCIAMIENTO ALTO: Los formatos motivados por IA están bloqueados hasta completar la 'Autorización Final' en Ingesta.")
        else:
            st.success("💎 ESTATUS ELITE ACTIVO: El sistema está autorizado para diligenciar y motivar documentos automáticamente.")

        tab_lista, tab_emision = st.tabs(["📝 Control de Expediente", "🏗️ Centro de Emisión Digital"])
        
        with tab_lista:
            st.write("### Auditoría de Calidad: Estado de Documentos")
            # Trazabilidad de documentos motivados
            progreso_kb = (len(st.session_state['kb']) / len(cartas)) * 100
            st.progress(progreso_kb / 100)
            st.markdown(f"**Integridad de la Base de Conocimiento:** {progreso_kb:.0f}%")
            
            st.table(pd.DataFrame({
                "Código": ["GAD-PROG-01", "GAD-LIST-02"],
                "Nombre": ["Programa de Auditoría ELITE", "Checklist de Verificación ELITE"],
                "Diligenciamiento IA": ["Habilitado ✅" if st.session_state['autorizado_emision'] else "Bloqueado 🔒"] * 2,
                "Motivación / Hallazgo": ["Cargado (Inyección RAG)" if st.session_state['kb'] else "Dato Sugerido"] * 2
            }))
            
        with tab_emision:
            st.markdown("<div class='elite-card' style='padding:0.8rem;'><b>🏗️ Centro de Emisión Digital: Selección de Activos</b>", unsafe_allow_html=True)
            
            # --- RESUMEN DE IDENTIDAD (PARA LOS GENERADORES) ---
            identity_data = {
                "auditor": st.session_state['auditor_name'],
                "rep_legal": st.session_state['rep_legal'],
                "rep_id": st.session_state['rep_id'],
                "tamanio": st.session_state['empresa_tamanio'],
                "sector": st.session_state['empresa_sector'],
                "nit": st.session_state['empresa_nit'],
                "direccion": st.session_state['empresa_direccion'],
                "web": st.session_state['empresa_web'],
                "objeto_social": st.session_state['empresa_objeto']
            }

            # --- REJILLA DE EMISIÓN ALTA DENSIDAD ---
            em_col1, em_col2, em_col3, em_col4 = st.columns(4)
            
            with em_col1:
                st.markdown("<div class='elite-card' style='text-align:center;'>", unsafe_allow_html=True)
                st.write("**PROG-01**")
                st.caption("Programa de Auditoría")
                if st.button("📥 WORD", key="em_prog_w", use_container_width=True):
                    p_prog = os.path.join(st.session_state['base_path'], "01_Direccion_y_Estrategia")
                    f = create_audit_program_v2(company, p_prog, st.session_state['logo_path'], st.session_state['expediente'], identity_data)
                    st.toast("Word Generado")
                st.markdown("</div>", unsafe_allow_html=True)

            with em_col2:
                st.markdown("<div class='elite-card' style='text-align:center;'>", unsafe_allow_html=True)
                st.write("**LIST-02**")
                st.caption("Checklist Legal")
                if st.button("📥 EXCEL", key="em_list_e", use_container_width=True):
                    p_check = os.path.join(st.session_state['base_path'], "02_Gestion_de_Calidad")
                    f = create_legal_checklist(company, p_check, st.session_state['logo_path'], st.session_state['expediente'], identity_data)
                    st.toast("Excel Generado")
                st.markdown("</div>", unsafe_allow_html=True)

            with em_col3:
                st.markdown("<div class='elite-card' style='text-align:center;'>", unsafe_allow_html=True)
                st.write("**REP-V20**")
                st.caption("Reporte Madurez")
                if st.button("📥 PDF", key="em_rep_p", use_container_width=True):
                    f = generate_maturity_report_pdf(company, st.session_state['base_path'], chs['score'], chs['level'])
                    st.toast("PDF Generado")
                st.markdown("</div>", unsafe_allow_html=True)

            with em_col4:
                st.markdown("<div class='elite-card' style='text-align:center; border: 1px solid #10B981;'>", unsafe_allow_html=True)
                st.write("**💎 ZIP**")
                st.caption("Master Pack Elite")
                if st.button("🏗️ COMPILAR", key="em_zip_all", use_container_width=True, type="primary"):
                    with st.spinner("Empaquetando..."):
                        # Generar todos los archivos
                        p_prog = os.path.join(st.session_state['base_path'], "01_Direccion_y_Estrategia")
                        f1 = create_audit_program_v2(company, p_prog, st.session_state['logo_path'], st.session_state['expediente'], identity_data)
                        p_check = os.path.join(st.session_state['base_path'], "02_Gestion_de_Calidad")
                        f2 = create_legal_checklist(company, p_check, st.session_state['logo_path'], st.session_state['expediente'], identity_data)
                        f3 = generate_maturity_report_pdf(company, st.session_state['base_path'], chs['score'], chs['level'])
                        
                        # Crear ZIP en memoria
                        buf = io.BytesIO()
                        with zipfile.ZipFile(buf, "x") as csv_zip:
                            csv_zip.write(f1, arcname=os.path.basename(f1))
                            csv_zip.write(f2, arcname=os.path.basename(f2))
                            csv_zip.write(f3, arcname=os.path.basename(f3))
                        
                        st.download_button(
                            label="📂 DESCARGAR EXPEDIENTE .ZIP",
                            data=buf.getvalue(),
                            file_name=f"EXPEDIENTE_ELITE_{company}.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                        st.balloons()
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    # --- SECCIÓN: PORTAL DE COLABORADOR (V16.0) ---
    elif menu == "📋 Portal de Entrega":
        st.markdown(f"<h1 class='norm-header'>📋 Portal de Colaboración: {st.session_state['user_role'].upper()}</h1>", unsafe_allow_html=True)
        st.info(f"Bienvenido. Aquí podrá gestionar los documentos requeridos para el área de **{st.session_state['user_role']}**.")
        
        # Filtrar documentos por el área del usuario
        area_map = {"juridica": "Juridico", "finanzas": "Financiera", "responsable": "Talento Humano"}
        mi_area = area_map.get(st.session_state['user_role'], "Operaciones")
        mis_docs = [c for c in cartas_todas if c.get('area') == mi_area or c.get('prioridad') == "VITAL (Obligatorio)"]
        
        c_p1, c_p2 = st.columns([2, 1])
        with c_p1:
            # Malla para Colaborador (V19.5 Unificada)
            st.write("### Mis Pendientes de Entrega")
            if not mis_docs:
                st.info("No tienes requerimientos pendientes para tu área.")
            else:
                cols_colab = st.columns(4)
                for i, d in enumerate(mis_docs):
                    with cols_colab[i % 4]:
                        doc_ready = d['doc'] in st.session_state['expediente']
                        status_icon = "✅" if doc_ready else "⏳"
                        status_color = "#10B981" if doc_ready else "#00C2FF"
                        
                        st.markdown(f"""
                        <div class="doc-card-mini" style="border-left: 4px solid {status_color};">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.5rem;">
                                <span style="font-size:1.1rem; filter: drop-shadow(0 0 5px {status_color}80);">{status_icon}</span>
                                <span class="status-badge">VITAL</span>
                            </div>
                            <p style="font-size:0.8rem; font-weight:700; color:#FFFFFF; margin:0; line-height:1.2; height: 2.4rem; overflow:hidden;">{d['doc']}</p>
                            <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.05); margin: 0.5rem 0;">
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<div style='margin-top:-3.8rem; padding: 0 0.5rem;'>", unsafe_allow_html=True)
                        ca1, ca2 = st.columns(2)
                        if not doc_ready:
                            with ca1:
                                _f = st.file_uploader("📥", key=f"up_colab_{i}", label_visibility="collapsed")
                                if _f:
                                    st.session_state['expediente'][d['doc']] = {"validado": True, "hitl": True}
                                    save_audit_state(); st.rerun()
                            with ca2:
                                if st.button("🤖", key=f"ia_colab_{i}", help="Draft IA", use_container_width=True):
                                    ui_generar_borrador_ia(d['doc'], d['area'], d['justificacion'])
                        else:
                            st.markdown("<p style='font-size:0.6rem; color:#10B981; text-align:center;'>LISTO</p>", unsafe_allow_html=True)
                        st.markdown("</div><br>", unsafe_allow_html=True)
        
        with c_p2:
            st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
            st.write("### Estatus de Cumplimiento")
            pct_area = int((len([d for d in mis_docs if d['doc'] in st.session_state['expediente']]) / len(mis_docs)) * 100) if mis_docs else 100
            draw_donut(pct_area, "MI PROGRESO", "#00C2FF")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- SECCIÓN: AYUDA ---
    elif menu == "💎 Help Center Elite":
        st.markdown("<h1 class='norm-header'>💎 Centro de Ayuda & Veracidad</h1>", unsafe_allow_html=True)
        
        help_tabs = st.tabs(["📖 Guía de Usuario", "🏛️ Base Normativa", "🤖 Asistente IA"])
        
        with help_tabs[0]:
            st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
            st.write("### Cómo operar el HMO Auditor")
            st.markdown("""
1. **Ingesta**: Suba sus documentos en orden. La IA los procesará localmente.
2. **Dashboard**: Verifique el nivel de cumplimiento y madurez en la central de mando.
3. **Generación**: Use los datos indexados para crear sus reportes finales certificados.
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with help_tabs[1]:
            st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
            st.write("### Referencias Legales Ancladas")
            st.table(pd.DataFrame({
                "Norma": ["ISO 9001", "ISO 27001", "ISO 14001", "Dec. 1330"],
                "Descripción": ["Calidad y Procesos", "Seguridad Informática", "Gestión Ambiental", "Aseguramiento Calidad Académica"],
                "Validación": ["Anclado", "Anclado", "Anclado", "Anclado"]
            }))
            st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
st.markdown("<p style='text-align: center; color: #FFFFFF; font-family: Orbitron; font-size: 0.8rem;'>HMO Auditor Pro v2.0.0 | 💎 Ecosistema Elite | 🔒 Operación Local Privada</p>", unsafe_allow_html=True)
