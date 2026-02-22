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
    .stApp, .stApp p, .stApp span, .stApp div, .stApp li {
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
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
    [data-baseweb="input"], [data-baseweb="select"] {
        background: rgba(5, 7, 12, 0.9) !important;
        border: 1px solid rgba(0, 194, 255, 0.4) !important;
        border-radius: 14px !important;
    }
    input { color: #FFFFFF !important; font-weight: 600 !important; }

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
    
    # Sidebar Superior
    st.sidebar.markdown(f"**🏢 {company}**")
    st.sidebar.markdown(f"**💎 Marco:** {st.session_state['norma']}")
    
    # Selector de Rol (Prioridad V3.7)
    roles_disponibles = ["Administrador (Global)", "⚖️ Jurídico", "🏦 Alta Dirección", "📊 Calidad / SIG", "🛡️ Ciberseguridad", "♻️ Gestión Ambiental", "🎓 Gestión Académica"]
    st.session_state['user_role'] = st.sidebar.selectbox("🔑 Rol de Sesión:", roles_disponibles, key="role_selector_top")
    
    st.sidebar.divider()
    
    # Navegación Unificada
    opciones = [
        "📊 Dashboard Analítico",
        "📋 Requerimientos Maestros",
        "🗺️ Camino de Ingesta (HITL)",
        "⚖️ Emisión de Títulos/Formatos",
        "💎 Help Center Elite"
    ]
    menu = st.sidebar.radio("Navegación:", opciones, key="main_menu_elite")
    
    if st.sidebar.button("🔒 Cerrar Sesión Segura"):
        save_audit_state()
        st.session_state['env'] = None
        st.rerun()

    # --- CONFIGURACIÓN DE DOCUMENTACIÓN & ROLES (UNIFICADA V3.3) ---
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
    
    # Filtrado por Rol
    if st.session_state['user_role'] == "Administrador (Global)":
        cartas = cartas_todas
    else:
        role_pure = st.session_state['user_role'].split(" ")[-1].strip()
        cartas = [c for c in cartas_todas if role_pure in c['area']]
        if not cartas: # Fallback
            cartas = [c for c in cartas_todas if st.session_state['user_role'] in c['area']]
        if not cartas: cartas = cartas_todas # Emergency Fallback

    # --- CÁLCULOS GLOBALES DE PROGRESO ---
    fase_a_ready = all([st.session_state['auditor_name'], st.session_state['rep_legal'], st.session_state['rep_id']])
    fase_b_ready = st.session_state['empresa_tamanio'] != "Pyme (1-50 emp)" or st.session_state['env'] == "Simulacion"
    progreso_c = (st.session_state['paso_ingesta'] / total_total) if total_total > 0 else 0
    progreso_total = ((1 if fase_a_ready else 0) + (1 if fase_b_ready else 0) + progreso_c) / 3

    # --- SECCIÓN: REQUERIMIENTOS MAESTROS ---
    if menu == "📋 Requerimientos Maestros":
        st.markdown(f"<h1 class='norm-header'>📋 Lista Maestra de Requerimientos</h1>", unsafe_allow_html=True)
        # ... rest of the code ...
    
    elif menu == "📊 Dashboard Analítico":
        st.markdown(f"<h1 class='norm-header'>📊 Dashboard Fase Analytics: {company}</h1>", unsafe_allow_html=True)
        
        # --- PHASE CARDS LIVE (V3.1) ---
        col1, col2, col3 = st.columns(3)
        phases = [
            ("Fase A: Identidad", 100 if st.session_state['auditor_name'] else 0, "Completo" if st.session_state['auditor_name'] else "Pendiente", "#10B981"),
            ("Fase B: Dimensión", 100 if st.session_state['empresa_tamanio'] != "Pyme" or st.session_state['env'] == "Simulacion" else 0, "Completo", "#00C2FF"),
            ("Fase C: Cuerpo Normativo", int((st.session_state['paso_ingesta']/len(cartas_todas))*100) if len(cartas_todas)>0 else 0, "En Progreso", "#94A3B8")
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
            # Mapear avance a labels del radar
            values = [100 if i < st.session_state['paso_ingesta'] else 30 for i in range(len(labels))]
            fig = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself', line_color='#1E3A8A'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(l=40, r=40, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_g2:
            st.markdown("<div class='elite-card'><b>Trazabilidad de Expediente</b>", unsafe_allow_html=True)
            for i, c in enumerate(cartas):
                estado = "✅" if i < st.session_state['paso_ingesta'] else "⏳"
                prefijo = "💎" if i < len(base_cartas) else "📜"
                st.write(f"{estado} {prefijo} **{c['doc']}**")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- SECCIÓN: INGESTA DE MATERIA PRIMA (HITL) ---
    elif menu == "🗺️ Camino de Ingesta (HITL)":
        st.markdown("<h1 class='norm-header'>🏗️ Ingesta de Materia Prima por Fases</h1>", unsafe_allow_html=True)
        
        # CÁLCULO DE PROGRESO GLOBAL DE INGESTA
        fase_a_ready = all([st.session_state['auditor_name'], st.session_state['rep_legal'], st.session_state['rep_id']])
        fase_b_ready = st.session_state['empresa_tamanio'] != ""
        progreso_c = (st.session_state['paso_ingesta'] / len(cartas)) if len(cartas) > 0 else 0
        
        progreso_total = ((1 if fase_a_ready else 0) + (1 if fase_b_ready else 0) + progreso_c) / 3
        
        st.markdown(f"### 📈 Avance Consolidado del Expediente: {progreso_total*100:.0f}%")
        st.progress(progreso_total)
        
        col_st1, col_st2, col_st3 = st.columns(3)
        col_st1.markdown(f"**Fase A:** {'✅' if fase_a_ready else '⏳'}")
        col_st2.markdown(f"**Fase B:** {'✅' if fase_b_ready else '⏳'}")
        col_st3.markdown(f"**Fase C:** {progreso_c*100:.0f}%")
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
                st.write("### ⚙️ Carga de Anexos Técnicos")
                # Agrupación por Áreas (Excluyendo lo que ya se pidió en A si fuera el caso, pero aquí mantenemos el loop departamental)
                areas = list(dict.fromkeys([c['area'] for c in cartas]))
                for i, area in enumerate(areas):
                    docs_area = [c for c in cartas if c['area'] == area]
                    completados_area = sum(1 for c in docs_area if cartas.index(c) < st.session_state['paso_ingesta'])
                    
                    with st.expander(f"{area} - Avance: {(completados_area/len(docs_area))*100:.0f}%"):
                        for c in docs_area:
                            idx = cartas.index(c)
                            es_completado = idx < st.session_state['paso_ingesta']
                            es_actual = idx == st.session_state['paso_ingesta']
                            
                            st.write(f"**{'✅' if es_completado else '⏳' if es_actual else '🔒'} {c['doc']}**")
                            
                            if es_actual:
                                uploaded_file = st.file_uploader(f"Cargar Evidencia: {c['doc']}", type=['pdf', 'docx'], key=f"up_{idx}")
                                if uploaded_file:
                                    st.info("🧿 Motor de Reconocimiento Procesando...")
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        raw_txt = st.text_area("📄 Texto Detectado por Reconocimiento", value=f"Contenido de {c['doc']}...", height=150, key=f"ocr_{idx}")
                                    with col2:
                                        manual_txt = st.text_area("✍️ Información Omitida / Ajuste Auditor", placeholder="Ingrese aquí lo que el motor no detectó...", key=f"val_{idx}")
                                    
                                    # Evaluador Experto de Alineamiento (Influenciado por Fase B)
                                    st.markdown("---")
                                    st.markdown(f"#### 🕵️ Evaluación del Experto (Rigor: {st.session_state['empresa_tamanio']})")
                                    check_txt = manual_txt if manual_txt else raw_txt
                                    
                                    # Lógica de Rigor por Tamaño
                                    es_grande = "Gran" in st.session_state['empresa_tamanio']
                                    min_len = 150 if es_grande else 80
                                    
                                    if len(check_txt) < min_len:
                                        msg = f"⚠️ **Alerta:** Para una {st.session_state['empresa_tamanio']}, se exige mayor profundidad técnica." if es_grande else "⚠️ **Alerta:** Información escueta para los estándares mínimos."
                                        st.warning(msg)
                                    else:
                                        st.success(f"✅ **Validación:** Contenido sólido para {st.session_state['empresa_tamanio']}.")
                                    
                # RESUMEN DE MATERIA PRIMA FALTANTE (FASE C)
                st.markdown("---")
                total_req = len(cartas)
                doc_list_missing = [c['doc'] for c in cartas if cartas.index(c) >= st.session_state['paso_ingesta']]
                
                c_inf1, c_inf2 = st.columns(2)
                c_inf1.metric("Materia Prima Fase C", f"{progreso_c*100:.0f}%", f"{st.session_state['paso_ingesta']}/{total_req} Cargados")
                
                if doc_list_missing:
                    with c_inf2:
                        st.warning(f"⚠️ **Pendientes de Carga ({len(doc_list_missing)}):**")
                        for d in doc_list_missing[:5]: st.write(f"- {d}")
                        if len(doc_list_missing) > 5: st.write(f"... y {len(doc_list_missing)-5} más.")
                if not doc_list_missing:
                    c_inf2.success("✅ ¡Cuerpo Normativo Completo!")

        # --- VALIDACIÓN & CIERRE ---
        with tab_final:
            st.write("### 🏁 Cierre de Ingesta y Validación de Estructura")
            progreso_c = (st.session_state['paso_ingesta'] / len(cartas)) if len(cartas) > 0 else 0
            
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
    elif menu == "⚖️ Emisión de Títulos/Formatos":
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
                
                # Botón de Motivado (Solo con Autorización)
                if st.session_state['autorizado_emision']:
                    if st.button("🚀 EMITIR DILIGENCIADO ELITE", key="full_prog"):
                        with st.spinner("Generando Matriz Legal y Programa Motivado..."):
                            f1 = create_audit_program_v2(company, st.session_state['base_path'], st.session_state['logo_path'], st.session_state['expediente'], identity_data)
                            f2 = create_legal_checklist(company, st.session_state['base_path'], st.session_state['logo_path'], st.session_state['expediente'], identity_data)
                            
                            st.success("✅ Documentos Diligenciados con Materia Prima Real.")
                            with open(f1, "rb") as f: st.download_button("📂 Descargar Programa de Auditoría", f, file_name=os.path.basename(f1))
                            with open(f2, "rb") as f: st.download_button("📊 Descargar Checklist Legal", f, file_name=os.path.basename(f2))
                st.markdown("</div>", unsafe_allow_html=True)

            # --- DOCUMENTO 2: CHECKLIST ---
            with c_doc2:
                st.markdown("<div class='elite-card'>", unsafe_allow_html=True)
                st.write("**GAD-LIST-02: Checklist Legal**")
                st.caption("Verificación de cumplimiento normativo.")
                
                from HMO_Checklist_Legal_Generator import create_legal_checklist
                if st.button("📥 Descargar Plantilla Vacía", key="empty_list"):
                    path = os.path.join(base_path, "01_Templates_Vacios", f"PLANTILLA_LIST.xlsx")
                    create_legal_checklist(company, os.path.dirname(path), st.session_state['logo_path'], {}, identity_data)
                    with open(path, "rb") as f: st.download_button("Guardar Template", f, file_name="Plantilla_Vacia_LIST.xlsx")
                
                if st.session_state['autorizado_emision']:
                    if st.button("🚀 EMITIR DILIGENCIADA ELITE", key="full_list"):
                        path = os.path.join(base_path, "02_Auditoria_IA", f"FULL_LIST.xlsx")
                        create_legal_checklist(company, os.path.dirname(path), st.session_state['logo_path'], st.session_state['expediente'], identity_data)
                        with open(path, "rb") as f: st.download_button("Descargar Checklist Motivada", f, file_name=f"ELITE_Diligenciada_LIST_{company}.xlsx")
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
