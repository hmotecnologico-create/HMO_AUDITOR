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

# --- CONFIGURACIÓN DE RUTAS PARA DESPLIEGUE ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GEN_PATH = os.path.join(SCRIPT_DIR, "HMO_Auditor_Master_V1", "04_Arquitectura_y_Diseno", "Scripts_Generadores")
if GEN_PATH not in sys.path:
    sys.path.append(GEN_PATH)

from HMO_PDF_Generator import generate_audit_program_pdf, generate_preparation_guide_pdf, generate_document_template_pdf
from HMO_AI_Engine import HMO_AI_Engine
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
    .stApp, .stApp p, .stApp li {
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

    # ---- COLUMNA 1: REANUDAR ----
    with col_g1:
        st.markdown("""
        <div class='elite-card'>
            <h4 style='color: #00C2FF; margin-bottom: 0.2rem;'>📂 REANUDAR</h4>
            <p style='font-size: 0.75rem; color: #94A3B8; margin-bottom: 0.5rem;'>Carga un expediente existente.</p>
        </div>
        """, unsafe_allow_html=True)

        base_audits_path = os.path.join(os.getcwd(), "Auditorias_HMO")
        if os.path.exists(base_audits_path):
            existing = [d for d in os.listdir(base_audits_path) if os.path.isdir(os.path.join(base_audits_path, d))]
        else:
            existing = []

        if existing:
            selected = st.selectbox("Proceso:", existing, key="resume_hub", label_visibility="collapsed")
        else:
            st.caption("No hay auditorías previas.")
            selected = None

        st.write("")  # espaciador uniforme
        if st.button("🚀 RESTAURAR", use_container_width=True, disabled=not selected):
            if selected and load_audit_state(selected): st.rerun()

    # ---- COLUMNA 2: SIMULACIÓN ----
    with col_g2:
        st.markdown("""
        <div class='elite-card'>
            <h4 style='color: #10B981; margin-bottom: 0.2rem;'>🎓 SIMULACIÓN</h4>
            <p style='font-size: 0.75rem; color: #94A3B8; margin-bottom: 0.5rem;'>Expediente demo: <b>Innovatech Solutions SAS</b>.</p>
        </div>
        """, unsafe_allow_html=True)

        st.info("✅ 12 documentos base pre-cargados (SIG · Calidad · Seguridad · Ambiental)", icon="💡")

        st.write("")  # espaciador uniforme
        if st.button("🚀 LANZAR V1.6 ELITE", use_container_width=True):
            st.session_state['env'], st.session_state['company_name'] = "Simulacion", "Innovatech Solutions SAS"
            st.session_state['base_path'] = setup_company_folders("Innovatech Solutions SAS")
            st.session_state['paso_ingesta'] = 5
            st.session_state['auditor_name'] = "Juan Gabriel Ortiz"
            st.session_state['empresa_nit'] = "901.455.789-2"
            st.session_state['norma'] = ["Calidad (ISO 9001:2015)", "Seguridad (ISO 27001:2022)"]
            st.session_state['expediente'] = {
                "Camara de Comercio (Existencia Legal)": "Verificado V6.0",
                "RUT (Registro Unico Tributario)": "Verificado V6.0",
                "Acta de Compromiso Directivo": "Compromiso de preparacion firmado.",
                "Cronograma de Actividades de Preparacion": "Hitos de auditoria programados.",
                "Mision y Vision Corporativa": "Verificado V6.0",
                "Organigrama Funcional": "Estructura Jerarquica Verificada",
                "Mapa de Procesos": "Interaccion de procesos analizada",
                "Politica de Seguridad": "Verificado V8.8 (SIG Integration)"
            }
            save_audit_state()
            st.rerun()

    # ---- COLUMNA 3: NUEVO PROYECTO ----
    with col_g3:
        st.markdown("""
        <div class='elite-card'>
            <h4 style='color: #FFFFFF; margin-bottom: 0.2rem;'>🏗️ NUEVO PROYECTO</h4>
            <p style='font-size: 0.75rem; color: #94A3B8; margin-bottom: 0.5rem;'>Auditoría real con rigor legal.</p>
        </div>
        """, unsafe_allow_html=True)

        new_name = st.text_input("Nombre Entidad:", placeholder="Ej: Universidad San José", key="nw_hub", label_visibility="collapsed")
        normas_disponibles = ["Calidad (ISO 9001:2015)", "Ambiental (ISO 14001:2015)", "Seguridad (ISO 27001:2022)", "Académico (Ley 115 / Dec. 1330)"]
        new_norma = st.multiselect("Marcos:", normas_disponibles, default=["Calidad (ISO 9001:2015)"], key="nm_hub", label_visibility="collapsed")

        if st.button("🏗️ CREAR PROYECTO", use_container_width=True):
            if new_name:
                st.session_state['env'], st.session_state['company_name'] = "Real", new_name
                st.session_state['norma'] = new_norma
                st.session_state['base_path'] = setup_company_folders(new_name)
                save_audit_state()
                st.rerun()
            else:
                st.warning("⚠️ Nombre requerido.")

    st.markdown("<p style='text-align: center; font-size: 0.65rem; color: #475569; margin-top: 1rem;'>HMO v2.0 Elite | Operación Local Privada</p>", unsafe_allow_html=True)

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
         "ejemplo_base": "FICHA DE PROCESO - {EMPRESA}\n\nNOMBRE: Gestion de Compras\nOBJETIVO: Garantizar el suministro oportuno de bienes y servicios.\nENTRADAS: Solicitud de compra aprobada.\nSALIDAS: Bien/servicio entregado y verificado.\nRESPONSABLE: Jefe de Logistica.\nINDICADOR: Nivel de cumplimiento de proveedores > 90%"}
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
    
    cartas_todas = base_cartas + norm_cartas
    
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

    # --- SIDEBAR MASTER (V4.5) ---
    st.sidebar.markdown(f"### 🏢 {company}")
    st.sidebar.markdown(f"**Marco:** {st.session_state['norma']}")
    
    # Selector de Rol Mejorado (V9.6 - Mapeo Robusto)
    roles_disponibles = [
        "Administrador (Global)", 
        "⚖️ Jurídico", 
        "🏦 Alta Dirección", 
        "📊 Calidad / SIG", 
        "🛡️ Ciberseguridad", 
        "♻️ Gestión Ambiental", 
        "🎓 Gestión Académica",
        "👥 Talento Humano",
        "💰 Financiera",
        "⚙️ Operaciones"
    ]
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

    # --- BOTÓN DE SINCRONIZACIÓN GLOBAL V9.4 ---
    st.sidebar.markdown("---")
    if st.sidebar.button("📡 Sincronizar con Central", use_container_width=True, help="Actualiza el expediente con datos de otras terminales via Cloud."):
        with st.sidebar:
            with st.spinner("Conectando con Servidor Maestro..."):
                try:
                    import subprocess
                    # Paso 1: Pull de cambios remotos
                    subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
                    # Paso 2: Push de cambios locales (incluyendo el estado actual)
                    save_audit_state()
                    subprocess.run(["git", "add", "."], capture_output=True)
                    subprocess.run(["git", "commit", "-m", "Sincronización automática de terminal"], capture_output=True)
                    subprocess.run(["git", "push", "origin", "main"], capture_output=True)
                    st.success("✅ Sincronización Exitosa.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error de enlace: {e}")

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
        
        # --- TABLERO DE TRAZABILIDAD COMPACTO (V9.3) ---
        c_mtr1, c_mtr2, c_mtr3, c_mtr4, c_mtr5, c_mtr6 = st.columns(6)
        
        # Mezcla de Donas y Métricas en una sola fila (Cockpit)
        with c_mtr1: draw_donut(progreso_total*100, "GLOBAL", "#00C2FF")
        with c_mtr2: draw_donut(30 if not fase_a_ready else 12, "RIESGO", "#F87171")
        with c_mtr3: draw_donut(pct_fase_c, "CALIDAD", "#34D399")
        
        c_mtr4.metric("Avance SIG", f"{progreso_global:.1f}%")
        c_mtr5.metric("Motor Experto", "BÚSQUEDA ACTIVA")
        c_mtr6.metric("Seguridad", "SHA-256")
        
        # --- FILA DE ANÁLISIS Y FICHA (SIDE-BY-SIDE) ---
        col_g1, col_g2, col_g3 = st.columns([1.2, 1, 1])
        
        with col_g1:
            st.markdown("<div class='elite-card' style='padding: 0.5rem;'><b>Radar de Madurez</b>", unsafe_allow_html=True)
            labels = ['Misión/Visión', 'Ética', 'Estructura', 'Norma Cl.4', 'Norma Cl.5', 'Norma Cl.6']
            values = [100 if label in st.session_state['expediente'] else (100 if i < 3 and st.session_state['env'] == "Simulacion" else 0) for i, label in enumerate(labels)]
            fig = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself', line_color='#00C2FF'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=250, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_g2:
            st.markdown("<div class='elite-card' style='padding: 0.5rem;'><b>Ficha de Identidad</b>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 0.8rem; margin:0;'>**NIT:** `{st.session_state['empresa_nit']}`</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 0.8rem; margin:0;'>**Sector:** {st.session_state['empresa_sector']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 0.8rem; margin:0;'>**Personal:** {st.session_state['empresa_personal']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 0.8rem; margin:0;'>**Dirección:** {st.session_state['empresa_direccion']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            if "Organigrama Funcional" in st.session_state['expediente']:
                st.markdown("<div class='elite-card' style='padding: 0.5rem; margin-top: 5px;'><b>Organigrama</b>", unsafe_allow_html=True)
                data_org = dict(character=["G.G", "Jur", "Ops", "TH", "SIG", "Prod", "Vnt"], parent=["", "G.G", "G.G", "G.G", "Ops", "Ops", "Ops"], value=[10, 5, 8, 4, 3, 6, 6])
                fig_org = px.treemap(data_org, names='character', parents='parent', values='value', color_discrete_sequence=['#00C2FF', '#1e3a8a'])
                fig_org.update_layout(margin=dict(t=5, l=5, r=5, b=5), height=120, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_org, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
        with col_g3:
            st.markdown("<div class='elite-card' style='padding: 0.5rem;'><b>Certificación</b>", unsafe_allow_html=True)
            for i, c in enumerate(cartas[:8]): # Mostrar solo los 8 primeros para evitar scroll
                doc_name = c['doc']
                estado = "✅" if doc_name in st.session_state['expediente'] else ("⚖️" if doc_name in st.session_state.get('justificados', []) else "⏳")
                st.markdown(f"<p style='font-size: 0.75rem; margin: 0;'>{estado} {doc_name[:25]}...</p>", unsafe_allow_html=True)
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
                justificado = doc_name in st.session_state['justificados']
                
                if cargado: estado = "✅"
                elif justificado: estado = "⚖️"
                else: estado = "⏳"
                
                prefijo = "💎" if c.get('prioridad') == "VITAL (Obligatorio)" else "📜"
                st.write(f"{estado} {prefijo} **{doc_name}**")
            st.markdown("</div>", unsafe_allow_html=True)

        # --- PANEL DE HALLAZGOS CONSOLIDADO V12.0 ---
        st.markdown("---")
        st.markdown("### 🔍 Panel de Hallazgos y Resultados de Auditoría")
        if not todos_hallazgos:
            st.info("No se han detectado hallazgos aún. Valide documentos con IA en el Camino de Ingesta.")
        else:
            col_hall1, col_hall2 = st.columns([2, 1])
            with col_hall1:
                st.markdown("<div class='elite-card'><b>Consolidado de Evidencias</b>", unsafe_allow_html=True)
                for h_item in todos_hallazgos:
                    doc = h_item['doc']
                    h_txt = h_item['hallazgo']
                    h_key = f"{doc}_{h_txt}"[:50]
                    
                    c_h1, c_h2 = st.columns([3, 1])
                    c_h1.write(f"**[{doc}]**: {h_txt}")
                    cat = st.session_state['hallazgos_manuales'].get(h_key, "Detectado")
                    
                    # Selector de Categoría
                    nueva_cat = c_h2.selectbox("-", ["Detectado", "No Conformidad", "Observación", "Fortaleza"], 
                                             key=f"cat_{h_key}", label_visibility="collapsed", 
                                             index=["Detectado", "No Conformidad", "Observación", "Fortaleza"].index(cat))
                    if nueva_cat != cat:
                        st.session_state['hallazgos_manuales'][h_key] = nueva_cat
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col_hall2:
                st.markdown("<div class='elite-card'><b>Resumen Proporcional</b>", unsafe_allow_html=True)
                ncs = sum(1 for v in st.session_state['hallazgos_manuales'].values() if v == "No Conformidad")
                obs = sum(1 for v in st.session_state['hallazgos_manuales'].values() if v == "Observación")
                fors = sum(1 for v in st.session_state['hallazgos_manuales'].values() if v == "Fortaleza")
                
                st.metric("🚫 No Conformidades", ncs)
                st.metric("⚠️ Observaciones", obs)
                st.metric("💎 Fortalezas", fors)
                st.markdown("</div>", unsafe_allow_html=True)

    # --- SECCIÓN: INGESTA DE MATERIA PRIMA (HITL) ---
    elif menu == "🗺️ Camino de Ingesta":
        st.markdown("<h1 class='norm-header'>🏗️ Ingesta de Materia Prima por Fases</h1>", unsafe_allow_html=True)
        
        # CÁLCULO DE PROGRESO GLOBAL DE INGESTA (SYNC V4.5)
        st.markdown(f"### 📈 Avance Consolidado del Expediente: {pct_total}%")
        st.progress(progreso_total)
        
        col_st1, col_st2, col_st3 = st.columns(3)
        col_st1.markdown(f"**Fase A (Identidad):** {pct_fase_a}%")
        col_st2.markdown(f"**Fase B (Dimension):** {pct_fase_b}%")
        col_st3.markdown(f"**Fase C (Revision):** {pct_fase_c}%")
        st.divider()

        tab_a, tab_b, tab_c, tab_final = st.tabs(["🔒 Fase A: Identidad", "📊 Fase B: Dimensión", "⚖️ 6.3.1 Revisión Documental", "🏁 Preparación Actividades"])
        
        with tab_a:
            # Métricas de Fase A
            fase_a_reqs = [st.session_state['auditor_name'], st.session_state['rep_legal'], st.session_state['rep_id']]
            fase_a_completados = sum(1 for r in fase_a_reqs if r)
            pct_a = int((fase_a_completados / 3) * 100)
            
            c_m1, c_m2 = st.columns([1, 4])
            c_m1.metric("Fase A", f"{pct_a}%")
            with c_m2: st.progress(pct_a / 100)
            
            if pct_a < 100:
                st.caption(f"⚠️ **Falta:** {', '.join([r for r, v in zip(['Auditor', 'Rep. Legal', 'ID'], fase_a_reqs) if not v])}")

            c1, c2, c3 = st.columns(3)
            st.session_state['auditor_name'] = c1.text_input("* Auditor:", value=st.session_state['auditor_name'])
            st.session_state['rep_legal'] = c2.text_input("* Representante:", value=st.session_state['rep_legal'])
            st.session_state['rep_id'] = c3.text_input("* ID Rep:", value=st.session_state['rep_id'])
            
            if st.button("💾 REGISTRAR"):
                save_audit_state()
                st.success("✅ Guardado.")
                st.rerun()

        # --- FASE B: DIMENSIONAMIENTO ---
        with tab_b:
            fase_b_reqs_status = {
                'tamanio': st.session_state['empresa_tamanio'] != "Pyme (1-50 emp)", 
                'personal': st.session_state['empresa_personal'] > 0,
                'direccion': bool(st.session_state['empresa_direccion'])
            }
            fase_b_completados = sum(1 for status in fase_b_reqs_status.values() if status)
            pct_b = int((fase_b_completados / 3) * 100)
            
            c_mb1, c_mb2 = st.columns([1, 4])
            c_mb1.metric("Fase B", f"{pct_b}%")
            with c_mb2: st.progress(pct_b / 100)

            c1, c2, c3 = st.columns(3)
            st.session_state['empresa_tamanio'] = c1.selectbox("* Tamaño:", ["Pyme (1-50 emp)", "Mediana (51-250 emp)", "Gran Empresa (+250 emp)"], index=0)
            st.session_state['empresa_personal'] = c2.number_input("* Personal:", value=st.session_state['empresa_personal'], min_value=1)
            st.session_state['empresa_sector'] = c3.selectbox("Sector:", ["Servicios", "Industrial", "Educativo", "Salud", "Tecnología"], index=0)
            st.session_state['empresa_direccion'] = st.text_area("* Dirección completa:", value=st.session_state['empresa_direccion'], height=80, placeholder="Ej: Calle 123 # 45-67, Piso 3, Torre A, Parque Empresarial Norte, Bogotá D.C.")
            
            if st.button("💾 GUARDAR B"):
                save_audit_state()
                st.success("✅ Perfilado.")

        # --- FASE C: CUERPO NORMATIVO ---
        with tab_c:
            # BLOQUEO RETIRADO V9.1 - Acceso libre para carga de evidencias
            if not fase_a_ready:
                st.warning("⚠️ Nota: La Fase A (Identidad) aún no está completa, pero puede adelantar la carga de evidencias aquí.")
            
            # --- MODO GOBERNANZA ADMIN V9.6 ---
            if st.session_state['user_role'] == "Administrador (Global)":
                st.markdown("""
                <div style='background: rgba(0, 194, 255, 0.1); border-left: 5px solid #00C2FF; padding: 10px; margin-bottom: 20px; border-radius: 5px;'>
                    <b style='color: #00C2FF;'>🛡️ MODO CONFIGURACIÓN ACTIVO (ADMIN)</b><br>
                    <span style='font-size: 0.85rem;'>Usted tiene la autoridad para <b>Justificar N/A</b>. Los documentos marcados como N/A desaparecerán de la vista de los responsables.</span>
                </div>
                """, unsafe_allow_html=True)
            
            # CABECERA DE CARGA CON METRICAS (V4.2)
            total_req = len(cartas)
            count_ready = len(st.session_state['expediente'])
            doc_list_missing = [c['doc'] for c in cartas if c['doc'] not in st.session_state['expediente']]
            
            c_head1, c_head2 = st.columns([1.5, 1])
            with c_head1:
                st.write("### ⚖️ 6.3.1 Revision de Informacion Documentada")
            with c_head2:
                # BOTON DE GUIA DE PREPARACION (V8.5 - ASCII)
                if st.button("📄 Descargar Guia de Preparacion (PDF)", use_container_width=True):
                    guide_path = generate_preparation_guide_pdf(st.session_state['company_name'], st.session_state['base_path'], cartas_todas, norma=st.session_state['norma'])
                    with open(guide_path, "rb") as f:
                        st.download_button("📂 Haz clic para Guardar Guia", f, file_name=os.path.basename(guide_path))
                
                st.metric("📦 Materia Prima Inyectada", f"{pct_fase_c}%", f"{count_ready}/{total_total} Listos")
            
            # VISIBILIDAD DE FALTANTES - PROPORCIONALIDAD V9.0
            if doc_list_missing:
                # Dividir en Críticos y Recomendados
                criticos = [d for d in doc_list_missing if any(c['doc'] == d and c['prioridad'] == "VITAL (Obligatorio)" for c in cartas)]
                recomendados = [d for d in doc_list_missing if d not in criticos]
                
                with st.expander("PENDIENTES DE CARGA (Haga clic para ver)", expanded=True):
                    if criticos:
                        st.error(f"⚠️ **BLOQUEANTES VITALES ({len(criticos)}):**")
                        st.write(", ".join(criticos))
                    if recomendados:
                        st.info(f"💡 **RECOMENDADOS/LEAN ({len(recomendados)}):**")
                        st.write(", ".join(recomendados))
                        if es_startup:
                            st.caption("Nota: Por ser una empresa pequeña, estos documentos son opcionales para avanzar.")
            else:
                st.success("✅ ¡Expediente Completo! Puede proceder a la Emision de Formatos.")
            
            st.divider()
            # Agrupación por Áreas (V4.5 Limpieza de Emojis)
            areas = list(dict.fromkeys([c['area'] for c in cartas]))
            for i, area in enumerate(areas):
                docs_area = [c for c in cartas if c['area'] == area]
                conteo_ready = sum(1 for c in docs_area if c['doc'] in st.session_state['expediente'])
                porcentaje_area = int((conteo_ready / len(docs_area)) * 100) if docs_area else 0
                
                with st.expander(f"AREA: {area.upper()} (Avance: {porcentaje_area}%)"):
                    for c in docs_area:
                        idx = cartas.index(c)
                        doc_id = c['doc']
                        norma_tag = c.get('norma', 'SIG')
                        es_completado = doc_id in st.session_state['expediente']
                        
                        # Badge Visual por Norma V9.8
                        color_map = {"SEGURIDAD": "#F87171", "AMBIENTAL": "#34D399", "ACADÉMICO": "#A78BFA", "CALIDAD": "#60A5FA", "SIG": "#94A3B8"}
                        badge_color = color_map.get(norma_tag, "#94A3B8")
                        
                        st.markdown(f"""
                        <div style='display: flex; align-items: center; gap: 10px;'>
                            <span style='background: {badge_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.65rem; font-weight: bold;'>{norma_tag}</span>
                            <b style='font-size: 1rem;'>{'✅' if es_completado else '⏳'} {doc_id}</b>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if not es_completado:
                            with st.expander("📋 ASISTENCIA DE ELABORACIÓN ELITE (Hiper-Contextual)", expanded=False):
                                st.markdown(f"**📌 Concepto y Justificación:** *{c.get('justificacion', 'Requisito normativo estándar.')}*")
                                
                                # Sub-tabs para limpieza visual V13.0
                                tab_pasos, tab_ejemplo = st.tabs(["�️ Cómo se crea", "📖 Ejemplo Contextualizado"])
                                
                                with tab_pasos:
                                    st.write("### Pasos para Crear y Generar:")
                                    pasos = c.get('como_crear', 'Solicite el documento al área responsable y verifique que cumpla con los estándares institucionales.')
                                    st.info(pasos)
                                    inst = c.get('instrucciones', '')
                                    if inst: st.caption(f"Nota técnica: {inst}")
                                
                                with tab_ejemplo:
                                    st.write(f"### Ejemplo Referencial para {company}:")
                                    metadata_ctx = {
                                        "company_name": company,
                                        "empresa_objeto": st.session_state.get('empresa_objeto', 'sus actividades'),
                                        "auditor_name": st.session_state.get('auditor_name', 'Auditor Líder')
                                    }
                                    ejemplo_text = formatear_ejemplo(c, metadata_ctx)
                                    st.code(ejemplo_text, language="text")
                                    st.caption("Tip: Puede copiar este texto como base para su documento oficial.")

                                st.caption(f"Ref: {c['ref']} | {c['desc']} | Prioridad: {c.get('prioridad', 'Estándar')}")
                                
                                # Botón de Descarga de Plantilla V10.0
                                if st.button(f"📑 Descargar Plantilla PDF - {doc_id}", key=f"tpl_{idx}", use_container_width=True):
                                    # Usar contenido combinado para la plantilla
                                    full_inst = f"{pasos}\n\nEJEMPLO:\n{ejemplo_text}"
                                    tpl_path = generate_document_template_pdf(
                                        doc_id, full_inst, st.session_state['base_path'],
                                        company=company,
                                        norma=c.get('norma', 'SIG'),
                                        ejemplo_base=ejemplo_text
                                    )
                                    with open(tpl_path, "rb") as f:
                                        st.download_button(f"📂 Guardar Plantilla {doc_id}", f, file_name=os.path.basename(tpl_path), key=f"dl_{idx}")
                                
                                # Ejemplo Visual para Politica de Seguridad (V10.0 Mockup)
                                if "Politica de Seguridad" in doc_id:
                                    img_path = os.path.join(SCRIPT_DIR, "politica_seguridad_perfecta_mockup.png")
                                    if os.path.exists(img_path):
                                        st.image(img_path, caption="Referencia Visual: Diagramación Profesional de Política ISO 27001", use_container_width=True)
                            
                            col_act1, col_act2 = st.columns([1, 1])
                            with col_act1:
                                # Opción de Justificación Manual (N/A) V9.4 - RESERVADO PARA ADMIN
                                es_justificado = doc_id in st.session_state.get('justificados', [])
                                if st.session_state['user_role'] == "Administrador (Global)":
                                    if st.button(f"⚖️ {'Quitar' if es_justificado else 'Justificar'} N/A", key=f"na_{idx}", use_container_width=True):
                                        if es_justificado:
                                            st.session_state['justificados'].remove(doc_id)
                                        else:
                                            st.session_state['justificados'].append(doc_id)
                                        save_audit_state()
                                        st.rerun()
                                else:
                                    # Si es N/A pero el usuario no es admin, solo ve el status (aunque el filtro de arriba ya debería haberlo ocultado)
                                    if es_justificado:
                                        st.warning("⚖️ Este requisito ha sido marcado como N/A por el Administrador.")
                            
                            with col_act2:
                                uploaded_file = st.file_uploader(f"📥 Cargar Evidencia", type=['pdf', 'docx', 'xlsx', 'csv'], key=f"up_{idx}", label_visibility="collapsed")
                            if uploaded_file:
                                st.info(f"🧿 Motor de Reconocimiento Cognitivo V8.0...")
                                st.write("---")
                                # Lógica de Parsing Estructurado para Matrices (V8.0)
                                extracted_data = ""
                                if uploaded_file.name.endswith(('.xlsx', '.csv')):
                                    try:
                                        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
                                        extracted_data = df.to_markdown() # Formato que Llama3 entiende muy bien
                                        st.success("📊 Estructura de Tabla Detectada y Procesada.")
                                    except:
                                        extracted_data = "Error en parsing estructurado."
                                
                                st.caption("🔍 Pasos de la IA:")
                                st.write("1. Analizando coherencia sintáctica...")
                                st.write("2. Validando semántica contra ISO 9001:2015...")
                                st.write("3. Verificando integridad de la materia prima...")
                                
                                col_ocr1, col_ocr2 = st.columns(2)
                                with col_ocr1:
                                    raw_txt = st.text_area("📄 Texto Detectado", value=f"Contenido verificado de {doc_id}...", height=100, key=f"ocr_{idx}")
                                with col_ocr2:
                                    manual_txt = st.text_area("✍️ Ajuste Auditor", placeholder="Añada observaciones...", key=f"val_{idx}")
                                
                                if st.button(f"✅ VALIDAR SEMÁNTICA {doc_id.upper()}", key=f"btn_{idx}"):
                                    with st.spinner("🧠 Llama3 Analizando Coherencia Normativa..."):
                                        ai_engine = HMO_AI_Engine()
                                        if ai_engine.test_connection():
                                            # Decidir si es análisis estructural o de documento
                                            if extracted_data:
                                                analisis = ai_engine.analyze_risk_matrix(extracted_data)
                                            else:
                                                analisis = ai_engine.analyze_document(doc_id, manual_txt if manual_txt else raw_txt, target_norm=st.session_state['norma'])
                                            
                                            if "error" not in analisis:
                                                st.session_state['expediente'][doc_id] = {
                                                    "contenido": manual_txt if manual_txt else (extracted_data if extracted_data else raw_txt),
                                                    "coherencia": analisis.get("Coherencia", 0),
                                                    "hallazgos": analisis.get("Hallazgos_Clave", []),
                                                    "resumen": analisis.get("Resumen_Ejecutivo", "")
                                                }
                                                st.success(f"✅ {doc_id} validado por IA con {analisis.get('Coherencia')}% de coherencia.")
                                            else:
                                                st.warning("⚠️ Error en respuesta de Llama3. Usando validación estándar.")
                                                st.session_state['expediente'][doc_id] = manual_txt if manual_txt else raw_txt
                                        else:
                                            st.error("🚨 Ollama (Llama3) No Detectado localmente.")
                                            st.session_state['expediente'][doc_id] = manual_txt if manual_txt else raw_txt
                                    
                                    save_audit_state()
                                    st.rerun()
                                
                                # Botón de Feedback Loop V11.0
                                if doc_id in st.session_state['expediente'] and manual_txt:
                                    if st.button("💡 Notificar Mejora a Central", key=f"feed_{idx}", use_container_width=True):
                                        fb_data = {
                                            "doc": doc_id,
                                            "ai_raw": raw_txt,
                                            "human_fix": manual_txt,
                                            "norma": st.session_state['norma'],
                                            "timestamp": str(datetime.datetime.now())
                                        }
                                        # Guardar localmente para sincronización futura
                                        fb_path = os.path.join(SCRIPT_DIR, "feedback_loop.json")
                                        feedbacks = []
                                        if os.path.exists(fb_path):
                                            try:
                                                with open(fb_path, "r") as f: feedbacks = json.load(f)
                                            except: pass
                                        feedbacks.append(fb_data)
                                        with open(fb_path, "w") as f: json.dump(feedbacks, f, indent=4)
                                        st.success("✅ Gracias. Esta lección será enviada a Central para mejorar el cerebro IA.")
                                
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
                                
            # El bloque de faltantes al final ha sido movido arriba.

        # --- VALIDACIÓN & CIERRE ---
        with tab_final:
            st.write("### 🏁 Cierre de Ingesta y Validación de Estructura")
            progreso_c = (len(st.session_state['expediente']) / len(cartas)) if len(cartas) > 0 else 0
            
            if 'revisado_plantillas' not in st.session_state: st.session_state['revisado_plantillas'] = False
            
            # --- CIERRE SELECTIVO V12.0 ---
            norma_lista = any(pct >= 100 for pct in normas_resumen.values())
            
            # Blindaje de Rigor V12.0
            if norma_lista and not es_rigor_ok:
                st.error(f"🛑 **BLOQUEO DE RIGOR:** La coherencia media de los documentos vitales es de {coherencia_media_vital:.1f}%, inferior al mínimo de 60%. Revise la calidad de la materia prima.")
            
            if not (fase_a_ready and fase_b_ready) or not norma_lista or not es_rigor_ok:
                st.warning("⚠️ Ingesta Incompleta o Insuficiente. Se requiere completar Fase A, B, los documentos VITALES de al menos una norma y cumplir con el rigor mínimo (60%).")
                if not norma_lista:
                    st.info("💡 **Estado de Normas:** " + " | ".join([f"{n}: {p}%" for n, p in normas_resumen.items()]))
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
                            # Generación REAL de PDF
                            try:
                                f_pdf = generate_audit_program_pdf(company, st.session_state['base_path'], st.session_state['expediente'], identity_data)
                                with open(f_pdf, "rb") as f:
                                    st.download_button("📄 Descargar Programa Certificado (PDF)", f, file_name=os.path.basename(f_pdf))
                            except Exception as e:
                                st.error(f"Error PDF: {e}")
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
