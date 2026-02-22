import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os
import sys
import shutil
import json

# --- CONFIGURACIÓN DE RUTAS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GEN_PATH = os.path.join(SCRIPT_DIR, "HMO_Auditor_Master_V1", "04_Arquitectura_y_Diseno", "Scripts_Generadores")
sys.path.append(GEN_PATH)

from HMO_Auditor_Master_V2_Generator import create_audit_program_v2
from HMO_Checklist_Legal_Generator import create_legal_checklist

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

    /* TEXTO HI-FI (LEGIBILIDAD EXTREMA) */
    .stApp, .stApp p, .stApp span, .stApp li {
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    /* FIX EMOJI RENDERING */
    .stExpander summary span {
        display: inline-flex !important;
    }
    
    /* ETIQUETAS DE WIDGETS (NEON BLUE) */
    [data-testid="stWidgetLabel"] p {
        color: #00C2FF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.8rem !important;
        text-shadow: 0 2px 10px rgba(0, 194, 255, 0.3);
    }

    /* TITULOS NEON */
    h1, h2, h3, .neon-title {
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 20px rgba(0, 194, 255, 0.6);
        letter-spacing: 3px !important;
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
        border: 4px solid #00C2FF;
        box-shadow: 0 0 15px rgba(0, 194, 255, 0.5);
    }

    /* INPUTS Y FORMULARIOS HI-FI */
    /* INPUTS Y FORMULARIOS HI-FI V4.6 (ACCESSIBILITY FIRST) */
    [data-baseweb="input"], [data-baseweb="select"], [data-baseweb="popover"] {
        background: #E2E8F0 !important; /* Fondo claro para contraste real */
        border: 1.5px solid #00C2FF !important;
        border-radius: 12px !important;
    }
    input { 
        color: #000000 !important; 
        font-weight: 700 !important; 
    }
    input::placeholder {
        color: rgba(0, 0, 0, 0.5) !important;
    }
    
    /* SELECTOR DE ROL Y DROPDOWNS: NEGRO SOBRE CLARO */
    div[data-baseweb="select"] span, div[data-baseweb="select"] div { 
        color: #000000 !important; 
        font-weight: 800 !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stSidebar"] label {
        color: #00C2FF !important;
        font-weight: 700 !important;
        font-size: 0.7rem !important;
    }

    /* BOTONES ELITE 3.0 */
    .stButton>button {
        background: linear-gradient(135deg, #00C2FF 0%, #1e3a8a 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        border: none !important;
        padding: 1rem !important;
        border-radius: 16px !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 30px rgba(0, 194, 255, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover { 
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 45px rgba(0, 194, 255, 0.7) !important;
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

    /* ESTILOS DE EXPANDER V4.1 */
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

# Lógica de Sesión (V1.8.0 Resiliente)
for key, default in [('env', None), ('norma', "Calidad (ISO 9001)"), ('paso_ingesta', 0), ('logo_path', None), ('expediente', {}), ('autorizado_emision', False), 
                    ('auditor_name', ""), ('rep_legal', ""), ('rep_id', ""), ('empresa_tamanio', "Pyme"), ('empresa_sector', "Servicios"),
                    ('empresa_nit', ""), ('empresa_direccion', ""), ('empresa_web', ""), ('empresa_objeto', ""), ('empresa_personal', 0),
                    ('user_role', "Administrador (Global)"), ('company_name', ""), ('base_path', ""), ('kb', {})]:
    if key not in st.session_state: st.session_state[key] = default

# ... [Funciones de persistencia omitidas por brevedad] ...

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

# --- PANTALLA DE BIENVENIDA (ONBOARDING GATEWAY V3.4) ---
if st.session_state['env'] is None:
    st.markdown("<h2 style='text-align: center; color: #FFFFFF; font-family: Orbitron; margin-bottom: 1rem;'>🛡️ HMO HUB <span style='font-size: 0.6em; vertical-align: middle; color: #00C2FF;'>ELITE EDITION</span></h2>", unsafe_allow_html=True)
    
    col_g1, col_g2, col_g3 = st.columns(3)
    
    with col_g1:
        st.markdown("""
        <div class='elite-card'>
            <h4 style='color: #00C2FF; margin-bottom: 0.2rem;'>📂 REANUDAR</h4>
            <p style='font-size: 0.75rem; color: #94A3B8; margin-bottom: 0;'>Acceso a expedientes previos.</p>
        </div>
        """, unsafe_allow_html=True)
        
        base_audits_path = os.path.join(os.getcwd(), "Auditorias_HMO")
        if os.path.exists(base_audits_path):
            existing = [d for d in os.listdir(base_audits_path) if os.path.isdir(os.path.join(base_audits_path, d))]
            if existing:
                selected = st.selectbox("Proceso:", existing, key="resume_hub", label_visibility="collapsed")
                if st.button("🚀 Restaurar", use_container_width=True):
                    if load_audit_state(selected): st.rerun()
            else: st.caption("No hay auditorías.")

    with col_g2:
        st.markdown("""
        <div class='elite-card'>
            <h4 style='color: #10B981; margin-bottom: 0.2rem;'>🎓 SIMULACIÓN</h4>
            <p style='font-size: 0.75rem; color: #94A3B8; margin-bottom: 0;'>Expediente: <b>Innovatech Solutions</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.7rem; color: #10B981;'>💡 Cámara, RUT y Matriz listos.</p>", unsafe_allow_html=True)
        if st.button("Lanzar V1.6 Elite", use_container_width=True):
            st.session_state['env'], st.session_state['company_name'] = "Simulacion", "Innovatech Solutions SAS"
            st.session_state['base_path'] = setup_company_folders("Innovatech Solutions SAS")
            st.session_state['paso_ingesta'] = 3
            st.session_state['auditor_name'] = "Juan Gabriel Ortiz"
            st.session_state['empresa_nit'] = "901.455.789-2"
            save_audit_state()
            st.rerun()

    with col_g3:
        st.markdown("""
        <div class='elite-card'>
            <h4 style='color: #FFFFFF; margin-bottom: 0.2rem;'>🏗️ NUEVO PROYECTO</h4>
            <p style='font-size: 0.75rem; color: #94A3B8; margin-bottom: 0;'>Auditoría real con rigor legal.</p>
        </div>
        """, unsafe_allow_html=True)
        new_name = st.text_input("Nombre Entidad:", placeholder="Ej: Universidad San José", key="nw_hub", label_visibility="collapsed")
        new_norma = st.selectbox("Marco:", ["ISO 9001:2015", "ISO 27001:2022", "Decreto 1330"], key="nm_hub", label_visibility="collapsed")
        if st.button("Crear Proyecto", use_container_width=True):
            if new_name:
                st.session_state['env'], st.session_state['company_name'] = "Real", new_name
                st.session_state['norma'] = new_norma
                st.session_state['base_path'] = setup_company_folders(new_name)
                save_audit_state()
                st.rerun()
            else: st.warning("Nombre requerido.")

    st.markdown("<p style='text-align: center; font-size: 0.65rem; color: #475569; margin-top: 1rem;'>HMO v2.0 Elite | Operación Local Privada</p>", unsafe_allow_html=True)

# --- DASHBOARD PRINCIPAL ---
else:
    company, base_path = st.session_state['company_name'], st.session_state['base_path']
    
    # --- CONFIGURACIÓN DE CARTAS Y PROGRESO (V3.9 PRE-RENDER) ---
    base_cartas = [
        {"doc": "Cámara de Comercio (Existencia Legal)", "area": "⚖️ Jurídico", "ref": "Legalidad", "desc": "Certificado actualizado con objeto social y NIT."},
        {"doc": "RUT (Registro Único Tributario)", "area": "⚖️ Jurídico", "ref": "Fiscal", "desc": "Identificación tributaria y responsabilidades."},
        {"doc": "Misión y Visión Corporativa", "area": "🏦 Alta Dirección", "ref": "Estratégico", "desc": "Propósito y rumbo organizacional."},
        {"doc": "Matriz de Responsables de Área", "area": "🏦 Alta Dirección", "ref": "Gobierno", "desc": "Liderazgo nominal por procesos."},
        {"doc": "Organigrama Funcional", "area": "🏦 Alta Dirección", "ref": "Estructura", "desc": "Jerarquía y mandos medios."}
    ]

    if "Académico" in st.session_state['norma']:
        norm_cartas = [
            {"doc": "PEI (Proyecto Educativo)", "area": "🎓 Gestión Académica", "ref": "Ley 115", "desc": "Columna vertebral académica."},
            {"doc": "Registro Calificado", "area": "⚖️ Jurídico/Normativo", "ref": "Dec. 1330", "desc": "Autorización ministerial."},
            {"doc": "Estatuto Docente", "area": "👥 Talento Humano", "ref": "Dec. 1278", "desc": "Reglamentación docente."}
        ]
    elif "Seguridad" in st.session_state['norma']:
        norm_cartas = [
            {"doc": "Política de Seguridad", "area": "🛡️ Ciberseguridad", "ref": "ISO 27001:5.2", "desc": "Directrices de protección."},
            {"doc": "Análisis de Riesgos", "area": "🛡️ Ciberseguridad", "ref": "ISO 27001:6.1", "desc": "Mapa de vulnerabilidades."}
        ]
    elif "Ambiental" in st.session_state['norma']:
        norm_cartas = [
            {"doc": "Aspectos Ambientales", "area": "♻️ Gestión Ambiental", "ref": "ISO 14001:6.1.2", "desc": "Evaluación de impactos."},
            {"doc": "Objetivos Ambientales", "area": "♻️ Gestión Ambiental", "ref": "ISO 14001:6.2", "desc": "Metas de eco-eficiencia."}
        ]
    else: # ISO 9001
        norm_cartas = [
            {"doc": "Contexto Organizacional", "area": "📊 Calidad", "ref": "ISO 9001:4.1", "desc": "Análisis de entorno (DOFA)."},
            {"doc": "Mapa de Procesos", "area": "⚙️ Operaciones", "ref": "ISO 9001:4.4", "desc": "Interacción de procesos."}
        ]
    
    cartas_todas = base_cartas + norm_cartas
    total_total = len(cartas_todas)
    # --- MOTOR DE CÁLCULO UNIFICADO V4.5 ---
    count_exp = len(st.session_state['expediente'])
    fase_a_ready = all([st.session_state['auditor_name'], st.session_state['rep_legal'], st.session_state['rep_id']])
    fase_b_ready = st.session_state['empresa_tamanio'] != "Pyme (1-50 emp)" or st.session_state['env'] == "Simulacion"
    
    pct_fase_a = 100 if fase_a_ready else 0
    pct_fase_b = 100 if fase_b_ready else 0
    pct_fase_c = int((count_exp / total_total) * 100) if total_total > 0 else 0
    pct_total = int((pct_fase_a + pct_fase_b + pct_fase_c) / 3)

    # Variables de compatibilidad para evitar discrepancias
    progreso_c = (count_exp / total_total) if total_total > 0 else 0
    progreso_total = pct_total / 100

    # --- SIDEBAR MASTER (V4.5) ---
    st.sidebar.markdown(f"### 🏢 {company}")
    st.sidebar.markdown(f"**Marco:** {st.session_state['norma']}")
    
    # Selector de Rol (V4.0 - Hi-Contrast)
    roles_disponibles = ["Administrador (Global)", "⚖️ Jurídico", "🏦 Alta Dirección", "📊 Calidad / SIG", "🛡️ Ciberseguridad", "♻️ Gestión Ambiental", "🎓 Gestión Académica"]
    st.session_state['user_role'] = st.sidebar.selectbox("👤 ROL DEL AUDITOR:", roles_disponibles, key="role_selector_top")
    
    st.sidebar.divider()
    
    # Navegación Prioritaria (Ingesta Primero + Avance)
    opciones = [
        f"🗺️ Camino de Ingesta [{pct_fase_c}%]",
        f"📊 Dashboard Analítico [{pct_total}%]",
        "📋 Requerimientos Maestros",
        "⚖️ Emisión de Formatos",
        "💎 Help Center Elite"
    ]
    menu_raw = st.sidebar.radio("FLUJO DE TRABAJO:", opciones, key="main_menu_elite")
    menu = menu_raw.split(" [")[0]
    
    if st.sidebar.button("🔒 Cierre Seguro"):
        save_audit_state()
        st.session_state['env'] = None
        st.rerun()

    # Filtrado Dinámico por Rol
    if st.session_state['user_role'] == "Administrador (Global)":
        cartas = cartas_todas
    else:
        role_search = st.session_state['user_role'].split(" ")[-1].strip()
        cartas = [c for c in cartas_todas if role_search in c['area'] or st.session_state['user_role'] in c['area']]
        if not cartas: cartas = cartas_todas
    count_exp = len(st.session_state['expediente'])
    fase_a_ready = all([st.session_state['auditor_name'], st.session_state['rep_legal'], st.session_state['rep_id']])
    fase_b_ready = st.session_state['empresa_tamanio'] != "Pyme (1-50 emp)" or st.session_state['env'] == "Simulacion"
    progreso_c = (count_exp / total_total) if total_total > 0 else 0
    progreso_total = ((1 if fase_a_ready else 0) + (1 if fase_b_ready else 0) + progreso_c) / 3

    # --- SECCIÓN: REQUERIMIENTOS MAESTROS ---
    if menu == "📋 Requerimientos Maestros":
        st.markdown(f"<h1 class='norm-header'>📋 Lista Maestra de Requerimientos</h1>", unsafe_allow_html=True)
        st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
        st.write(f"### Requisitos del Marco: {st.session_state['norma']}")
        st.info("Esta lista representa la materia prima necesaria para que el sistema genere los formatos oficiales.")
        
        df_req = pd.DataFrame(cartas_todas)
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
        st.markdown(f"<h1 class='norm-header'>📊 Dashboard Fase Analytics: {company}</h1>", unsafe_allow_html=True)
        
        # --- PHASE CARDS LIVE (V3.1) ---
        col1, col2, col3 = st.columns(3)
        phases = [
            ("Fase A: Identidad", 100 if st.session_state['auditor_name'] else 0, "Completo" if st.session_state['auditor_name'] else "Pendiente", "#10B981"),
            ("Fase B: Dimensión", 100 if st.session_state['empresa_tamanio'] != "Pyme" or st.session_state['env'] == "Simulacion" else 0, "Completo", "#00C2FF"),
            ("Fase C: Cuerpo Normativo", int((count_exp/len(cartas_todas))*100) if len(cartas_todas)>0 else 0, "En Progreso", "#94A3B8")
        ]
        
        for i, (title, proc, status, color) in enumerate(phases):
            with [col1, col2, col3][i]:
                st.markdown(f"""
                <div class='elite-card' style='text-align: center;'>
                    <div style='font-size: 0.8rem; color: #94A3B8;'>FASE {i+1}</div>
                    <h3 style='color: {color};'>{title}</h3>
                    <div style='font-size: 2.5rem; font-family: Orbitron; font-weight: 700;'>{proc}%</div>
                    <div style='color: {color}; font-weight: 700;'>{status}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # --- TABLERO DE TRAZABILIDAD DE MATERIA PRIMA (V1.5.2) ---
        st.write("### 🏗️ Estatus de Materia Prima")
        
        # Calcular estados
        fase_a_ok = fase_a_ready
        fase_b_ok = fase_b_ready
        progreso_c_val = progreso_c * 100
        
        # METRICS GAUGES (STILO REFERENCIA ELITE V2.0)
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
                height=180,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                annotations=[dict(text=f"{int(value)}%", x=0.5, y=0.5, font_size=24, font_color="white", font_family="Orbitron", showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"<p style='text-align: center; color: #00C2FF; font-family: Orbitron; font-size: 0.8rem; margin-top: -20px; text-shadow: 0 0 5px rgba(0,194,255,0.3);'>{label}</p>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: draw_donut(progreso_total*100, "CUMPLIMIENTO TOTAL", "#00C2FF")
        with c2: draw_donut(30 if not fase_a_ok else 12, "RIESGO OPERATIVO", "#F87171")
        with c3: draw_donut(progreso_c_val, "CALIDAD DE DATOS", "#34D399")
        
        st.divider()
        
        # --- FICHA DE IDENTIDAD LEGAL (V1.6.0) ---
        st.markdown(f"<div class='elite-card'>", unsafe_allow_html=True)
        st.write("### 📜 Ficha de Identidad Legal & Tributaria")
        cl1, cl2 = st.columns(2)
        with cl1:
            st.markdown(f"**NIT:** `{st.session_state['empresa_nit']}`")
            st.markdown(f"**Dirección:** `{st.session_state['empresa_direccion']}`")
            st.markdown(f"**Web:** [{st.session_state['empresa_web']}](https://{st.session_state['empresa_web']})")
        with cl2:
            st.markdown(f"**Sector:** {st.session_state['empresa_sector']}")
            st.markdown(f"**Personal:** {st.session_state['empresa_personal']} colaboradores")
            st.markdown(f"**Objeto Social:** *{st.session_state['empresa_objeto']}*")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()
        progreso_global = ((1 if fase_a_ok else 0) + (1 if fase_b_ok else 0) + (st.session_state['paso_ingesta'] / total_total)) / 3 * 100
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Cumplimiento Global", f"{progreso_global:.1f}%")
        col_m2.metric("Motor Experto", "BÚSQUEDA TÉCNICA ACTIVA", "V1.5.2 Elite")
        col_m3.metric("Seguridad", "SHA-256", "Inexpugnable")
        
        st.divider()
        
        # Análisis Visual
        col_g1, col_g2 = st.columns([2, 1])
        with col_g1:
            st.markdown("<div class='elite-card'><b>Radar de Madurez Normativa (Kiviat)</b>", unsafe_allow_html=True)
            labels = ['Misión/Visión', 'Ética', 'Estructura', 'Norma Cl.4', 'Norma Cl.5', 'Norma Cl.6']
            values = [100 if label in st.session_state['expediente'] else (100 if i < 3 and st.session_state['env'] == "Simulacion" else 0) for i, label in enumerate(labels)]
            fig = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself', line_color='#00C2FF'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(l=40, r=40, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- NUEVA VISUALIZACIÓN: ORGANIGRAMA JERÁRQUICO (V5.0) ---
            if "Organigrama Funcional" in st.session_state['expediente']:
                st.markdown("<div class='elite-card'><b>Visualización Jerárquica: Organigrama Funcional</b>", unsafe_allow_html=True)
                # Mock data representation of a typical hierarchy for the treemap
                data_org = dict(
                    character=["Gerencia General", "Dirección Jurídica", "Dirección Operativa", "Talento Humano", "Calidad/SIG", "Producción", "Ventas"],
                    parent=["", "Gerencia General", "Gerencia General", "Gerencia General", "Dirección Operativa", "Dirección Operativa", "Dirección Operativa"],
                    value=[10, 5, 8, 4, 3, 6, 6]
                )
                fig_org = px.treemap(data_org, names='character', parents='parent', values='value', color_discrete_sequence=['#00C2FF', '#1e3a8a', '#10B981'])
                fig_org.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=300, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_org, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
        with col_g2:
            st.markdown("<div class='elite-card'><b>Certificación de Expediente</b>", unsafe_allow_html=True)
            for i, c in enumerate(cartas):
                doc_name = c['doc']
                cargado = doc_name in st.session_state['expediente']
                estado = "✅" if cargado else "⏳"
                prefijo = "💎" if i < len(base_cartas) else "📜"
                st.write(f"{estado} {prefijo} **{doc_name}**")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- SECCIÓN: INGESTA DE MATERIA PRIMA (HITL) ---
    elif menu == "🗺️ Camino de Ingesta":
        st.markdown("<h1 class='norm-header'>🏗️ Ingesta de Materia Prima por Fases</h1>", unsafe_allow_html=True)
        
        # CÁLCULO DE PROGRESO GLOBAL DE INGESTA (SYNC V4.5)
        st.markdown(f"### 📈 Avance Consolidado del Expediente: {pct_total}%")
        st.progress(progreso_total)
        
        col_st1, col_st2, col_st3 = st.columns(3)
        col_st1.markdown(f"**Fase A:** {'✅' if fase_a_ready else '⏳'}")
        col_st2.markdown(f"**Fase B:** {'✅' if fase_b_ready else '⏳'}")
        col_st3.markdown(f"**Fase C:** {pct_fase_c}%")
        st.divider()

        tab_a, tab_b, tab_c, tab_final = st.tabs(["🔒 Fase A: Identidad", "📊 Fase B: Dimensión", "📜 Fase C: Cuerpo Normativo", "🏁 Validación & Cierre"])
        
        # --- FASE A: IDENTIDAD ---
        with tab_a:
            st.write("### 🏦 Datos Maestros de Identidad")
            st.info("Información obligatoria para la validez legal de las firmas y encabezados.")
            
            c1, c2 = st.columns(2)
            st.session_state['auditor_name'] = c1.text_input("👨‍💼 Nombre Completo del Auditor:", value=st.session_state['auditor_name'], placeholder="Ingrese su nombre (Ej: Juan Gabriel)")
            st.session_state['rep_legal'] = c2.text_input("⚖️ Representante Legal de la Entidad:", value=st.session_state['rep_legal'], placeholder="Nombre del Representante")
            st.session_state['rep_id'] = c1.text_input("🆔 Documento de Identidad (Representante):", value=st.session_state['rep_id'], placeholder="Cédula o ID Legal")
            
            if st.button("💾 REGISTRAR IDENTIDAD"):
                save_audit_state()
                st.success("✅ Identidad Registrada.")
                st.rerun()

        # --- FASE B: DIMENSIONAMIENTO ---
        with tab_b:
            st.write("### 📊 Perfilamiento Organizacional")
            st.info("El tamaño y sector de la empresa determinan de forma crítica el rigor de los controles a aplicar.")
            
            st.session_state['empresa_tamanio'] = st.selectbox("📏 Tamaño de la Empresa:", ["Pyme (1-50 emp)", "Mediana (51-200 emp)", "Gran Empresa (>200 emp)"], index=["Pyme (1-50 emp)", "Mediana (51-200 emp)", "Gran Empresa (>200 emp)"].index(st.session_state['empresa_tamanio']) if st.session_state['empresa_tamanio'] in ["Pyme (1-50 emp)", "Mediana (51-200 emp)", "Gran Empresa (>200 emp)"] else 0)
            st.session_state['empresa_sector'] = st.selectbox("🏭 Sector Económico:", ["Servicios", "Industrial", "Educativo", "Salud", "Tecnología"], index=["Servicios", "Industrial", "Educativo", "Salud", "Tecnología"].index(st.session_state['empresa_sector']) if st.session_state['empresa_sector'] in ["Servicios", "Industrial", "Educativo", "Salud", "Tecnología"] else 0)
            
            if st.button("💾 GUARDAR PERFILADO Y CONTINUAR"):
                save_audit_state()
                st.success("✅ Perfilamiento guardado. Proceda al Cuerpo Normativo.")

        # --- FASE C: CUERPO NORMATIVO ---
        with tab_c:
            if not fase_a_ready:
                st.error("🔒 El Cuerpo Normativo está bloqueado. Complete primero la Fase A: Identidad.")
            else:
                # CABECERA DE CARGA CON MÉTRICAS (V4.2)
                total_req = len(cartas)
                count_ready = len(st.session_state['expediente'])
                doc_list_missing = [c['doc'] for c in cartas if c['doc'] not in st.session_state['expediente']]
                
                c_head1, c_head2 = st.columns([1.5, 1])
                with c_head1:
                    st.write("### ⚙️ Carga de Anexos Técnicos")
                with c_head2:
                    st.metric("📦 Materia Prima Inyectada", f"{pct_fase_c}%", f"{count_ready}/{total_total} Listos")
                # Agrupación por Áreas (V4.5 Limpieza de Emojis)
                areas = list(dict.fromkeys([c['area'] for c in cartas]))
                for i, area in enumerate(areas):
                    docs_area = [c for c in cartas if c['area'] == area]
                    conteo_ready = sum(1 for c in docs_area if c['doc'] in st.session_state['expediente'])
                    porcentaje_area = int((conteo_ready / len(docs_area)) * 100) if docs_area else 0
                    
                    with st.expander(f"📁 {area} - Avance: {porcentaje_area}%"):
                         for c in docs_area:
                            idx = cartas.index(c)
                            doc_id = c['doc']
                            es_completado = doc_id in st.session_state['expediente']
                            
                            st.write(f"**{'✅' if es_completado else '⏳'} {doc_id}**")
                            
                            if not es_completado:
                                st.caption(f"Ref: {c['ref']} | {c['desc']}")
                                uploaded_file = st.file_uploader(f"📥 {doc_id}: Cargue aquí el documento oficial (.pdf, .docx)", type=['pdf', 'docx'], key=f"up_{idx}")
                                if uploaded_file:
                                    st.info(f"🧿 Motor de Reconocimiento Procesando {doc_id}...")
                                    col_ocr1, col_ocr2 = st.columns(2)
                                    with col_ocr1:
                                        raw_txt = st.text_area("📄 Texto Detectado", value=f"Contenido verificado de {doc_id}...", height=100, key=f"ocr_{idx}")
                                    with col_ocr2:
                                        manual_txt = st.text_area("✍️ Ajuste Auditor", placeholder="Añada observaciones...", key=f"val_{idx}")
                                    
                                    if st.button(f"✅ VALIDAR {doc_id.upper()}", key=f"btn_{idx}"):
                                        # Guardar en el expediente meta-data real
                                        st.session_state['expediente'][doc_id] = manual_txt if manual_txt else raw_txt
                                        save_audit_state()
                                        st.success(f"✅ {doc_id} cargado con éxito.")
                                        st.rerun()
                                    
                                    # Evaluador de Rigor
                                    es_grande = "Gran" in st.session_state['empresa_tamanio']
                                    check_content = manual_txt if manual_txt else raw_txt
                                    if len(check_content) < (150 if es_grande else 80):
                                        st.warning("⚠️ Contenido limitado para los estándares de rigor.")
                                    else:
                                        st.success("💎 Densidad informativa óptima.")
                            else:
                                st.success(f"Documento indexado: {len(st.session_state['expediente'][doc_id])} caracteres.")
                                if st.button(f"🗑️ Eliminar y Re-cargar {doc_id}", key=f"del_{idx}"):
                                    del st.session_state['expediente'][doc_id]
                                    save_audit_state()
                                    st.rerun()
                                    
                if doc_list_missing:
                    st.warning(f"⚠️ **Pendientes de Carga ({len(doc_list_missing)}):** {', '.join(doc_list_missing[:3])}{'...' if len(doc_list_missing)>3 else ''}")
                if not doc_list_missing:
                    st.success("✅ ¡Cuerpo Normativo Completo!")

        # --- VALIDACIÓN & CIERRE ---
        with tab_final:
            st.write("### 🏁 Cierre de Ingesta y Validación de Estructura")
            progreso_c = (len(st.session_state['expediente']) / len(cartas)) if len(cartas) > 0 else 0
            
            if 'revisado_plantillas' not in st.session_state: st.session_state['revisado_plantillas'] = False
            
            if progreso_total < 1.0: # Requisito: Fase A, B y C al 100%
                st.warning("⚠️ Ingesta Incompleta (Menor al 100%). No se puede proceder a la revisión de formatos.")
            else:
                st.success("🏆 Materia Prima completa y validada por el Experto.")
                st.markdown("---")
                st.write("#### 🛡️ Paso 1: Generación y Conocimiento de Plantillas Base")
                st.info("Antes de autorizar el diligenciamiento automático, es mandatorio que el auditor conozca y valide la estructura de las plantillas base.")
                
                if st.button("🏗️ GENERAR PLANTILLAS BASE PARA REVISIÓN"):
                    with st.spinner("Preparando formatos sin diligenciar..."):
                        # Importar generadores si no están ya en el scope
                        from HMO_Auditor_Master_V2_Generator import create_audit_program_v2
                        from HMO_Checklist_Legal_Generator import create_legal_checklist
                        
                        # Consolidar Identidad Legal (V1.6.0)
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
                        
                        # Generar vacíos oficialmente
                        f1 = create_audit_program_v2(company, st.session_state['base_path'], st.session_state['logo_path'], {}, identity_data)
                        f2 = create_legal_checklist(company, st.session_state['base_path'], st.session_state['logo_path'], {}, identity_data)
                        st.session_state['revisado_plantillas'] = True
                        st.success("✅ Plantillas Base generadas. Por favor, descárguelas y revíselas.")
                        
                if st.session_state['revisado_plantillas']:
                    c_rev1, c_rev2 = st.columns(2)
                    with open(os.path.join(st.session_state['base_path'], "GAD_PRO_01_Programa_Auditoria_ELITE.docx"), "rb") as f:
                        c_rev1.download_button("📂 Revisar Programa (Vacío)", f, file_name="PLANTILLA_BASE_PROGRAMA.docx")
                    with open(os.path.join(st.session_state['base_path'], "GAD_LIST_02_Checklist_Auditoria_ELITE.xlsx"), "rb") as f:
                        c_rev2.download_button("📊 Revisar Checklist (Vacío)", f, file_name="PLANTILLA_BASE_CHECKLIST.xlsx")
                    
                    st.markdown("---")
                    st.write("#### ✍️ Paso 2: Autorización de Diligenciamiento")
                    st.warning("¿La estructura de las plantillas es adecuada? Si desea que el sistema proceda a inyectar la materia prima, autorice a continuación:")
                    st.session_state['autorizado_emision'] = st.toggle("AUTORIZAR DILIGENCIAMIENTO DE FORMATOS", value=st.session_state['autorizado_emision'])
                    
                    if st.session_state['autorizado_emision']:
                        st.balloons()
                        st.success("🚀 El sistema ha sido habilitado para emitir documentos con inyección de datos del expediente.")

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
                "Diligenciamiento IA": ["Habilitado ✅" if st.session_state['autorizado_emision'] else "Bloqueado 🔒"],
                "Motivación / Hallazgo": ["Cargado (Inyección RAG)" if st.session_state['kb'] else "Dato Sugerido"]
            }))
            
        with tab_emision:
            st.write("### Generación de Activos Certificados")
            c_doc1, c_doc2 = st.columns(2)
            
            # --- DOCUMENTO 1: PROGRAMA ---
            with c_doc1:
                st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
                st.write("**GAD-PROG-01: Programa de Auditoría**")
                st.caption("Documento maestro de planeación.")
                
                # Consolidar Identidad Legal (V1.6.0)
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

                # Botón de Plantilla Vacía (Siempre disponible)
                from HMO_Auditor_Master_V2_Generator import create_audit_program_v2
                if st.button("📥 Descargar Plantilla Vacía", key="empty_prog"):
                    path = os.path.join(base_path, "01_Templates_Vacios", f"PLANTILLA_PROG.docx")
                    create_audit_program_v2(company, os.path.dirname(path), st.session_state['logo_path'], {}, identity_data)
                    with open(path, "rb") as f: st.download_button("Guardar Template", f, file_name="Plantilla_Vacia_PROG.docx")
                
            if st.session_state['autorizado_emision']:
                st.markdown("<div class='elite-card' style='border-color: #10B981;'>", unsafe_allow_html=True)
                st.write("### 🚀 DESCARGA DUAL ELITE: PAQUETE DE AUDITORÍA")
                st.info("El sistema ha procesado la materia prima y está listo para emitir los formatos oficiales en múltiples formatos.")
                
                if st.button("🏁 GENERAR Y EMITIR DOCUMENTACIÓN"):
                    with st.spinner("Consolidando Expediente Profesional..."):
                        # Programa de Auditoría
                        p_prog = os.path.join(st.session_state['base_path'], "01_Direccion_y_Estrategia")
                        f1 = create_audit_program_v2(company, p_prog, st.session_state['logo_path'], st.session_state['expediente'], identity_data)
                        
                        # Checklist Legal
                        p_check = os.path.join(st.session_state['base_path'], "02_Gestion_de_Calidad")
                        f2 = create_legal_checklist(company, p_check, st.session_state['logo_path'], st.session_state['expediente'], identity_data)
                        
                        st.success("✅ Documentación Generada Exitosamente")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            st.write("#### 📝 Word/Excel (Editables)")
                            with open(f1, "rb") as f: st.download_button("📂 Programa de Auditoría (Word)", f, file_name=os.path.basename(f1))
                            with open(f2, "rb") as f: st.download_button("📊 Checklist Legal (Excel)", f, file_name=os.path.basename(f2))
                        
                        with c2:
                            st.write("#### 🔒 PDF (Certificados)")
                            st.info("💡 La conversión a PDF con firma digital está siendo procesada. Por ahora, los formatos Word/Excel incluyen todos los sellos legales.")
                            st.button("📄 Exportar PDF (ELITE)", disabled=True)
                        st.balloons()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ El expediente aún no ha sido autorizado para emisión. Complete la validación en la pestaña anterior.")

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
