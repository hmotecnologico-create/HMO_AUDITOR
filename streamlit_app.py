import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os
import sys
import shutil
import json

# --- CONFIGURACIÓN DE RUTAS (Importante para despliegue raíz) ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GEN_PATH = os.path.join(SCRIPT_DIR, "HMO_Auditor_Master_V1", "04_Arquitectura_y_Diseno", "Scripts_Generadores")
sys.path.append(GEN_PATH)

from HMO_Auditor_Master_V2_Generator import create_audit_program_v2
from HMO_Checklist_Legal_Generator import create_legal_checklist

# Configuración de página
st.set_page_config(page_title="HMO Auditor Pro - V1.3 Elite", layout="wide", page_icon="🛡️")

# Estilo personalizado Elite (Optimizado y Estable)
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; color: #212529; }
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        background: linear-gradient(135deg, #1F4E78 0%, #2E6B9E 100%); 
        color: white; font-weight: 600; border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    [data-testid="stMetricValue"] { color: #1F4E78 !important; }
</style>
""", unsafe_allow_html=True)

# Lógica de Sesión
for key, default in [('env', None), ('norma', "Calidad (ISO 9001)"), ('paso_ingesta', 0), ('logo_path', None)]:
    if key not in st.session_state: st.session_state[key] = default

# --- FUNCIONES DE PERSISTENCIA ---
def setup_company_folders(company_name):
    safe_name = "".join([c if c.isalnum() else "_" for c in company_name])
    base_dir = os.path.join(os.getcwd(), "Auditorias_HMO", safe_name)
    for sub in ["01_Templates_Vacios", "02_Auditoria_IA", "03_Evidencias_Ingesta"]:
        path = os.path.join(base_dir, sub)
        if not os.path.exists(path): os.makedirs(path)
    return base_dir

def save_audit_state():
    if st.session_state['env'] and st.session_state.get('company_name'):
        base_dir = st.session_state['base_path']
        state = {
            "company_name": st.session_state['company_name'], "norma": st.session_state['norma'],
            "paso_ingesta": st.session_state['paso_ingesta'], "logo_path": st.session_state['logo_path'],
            "env": st.session_state['env'], "last_update": datetime.datetime.now().isoformat()
        }
        with open(os.path.join(base_dir, "audit_state.json"), "w") as f: json.dump(state, f, indent=4)

def load_audit_state(company_folder):
    state_path = os.path.join(os.getcwd(), "Auditorias_HMO", company_folder, "audit_state.json")
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
            for k, v in state.items(): st.session_state[k] = v
            st.session_state['base_path'] = os.path.join(os.getcwd(), "Auditorias_HMO", company_folder)
            return True
    return False

# --- PANTALLA DE BIENVENIDA ---
if st.session_state['env'] is None:
    st.title("🛡️ HMO Auditor - Ecosistema Pro")
    st.subheader("Gestión Multi-Norma con Persistencia Industrial")
    
    base_audits_path = os.path.join(os.getcwd(), "Auditorias_HMO")
    if os.path.exists(base_audits_path):
        existing = [d for d in os.listdir(base_audits_path) if os.path.isdir(os.path.join(base_audits_path, d))]
        if existing:
            with st.expander("📂 REANUDAR AUDITORÍA", expanded=True):
                c_sel, c_btn = st.columns([3, 1])
                selected = c_sel.selectbox("Proceso:", existing)
                if c_btn.button("🚀 Continuar"):
                    if load_audit_state(selected): st.rerun()

    st.divider()
    st.write("### 🆕 Nueva Auditoría")
    col1, col2 = st.columns(2)
    st.session_state['norma'] = col1.selectbox("Norma:", [
        "Calidad (ISO 9001)", 
        "Seguridad (ISO 27001)", 
        "Ambiental (ISO 14001)",
        "Académico (Ley 115 / Dec. 1330)"
    ])
    new_company = col1.text_input("Empresa:", placeholder="Ej: Universidad San José")
    logo_file = col2.file_uploader("Logo (PNG/JPG)", type=['png', 'jpg', 'jpeg'])

    b1, b2 = st.columns(2)
    if b1.button("🧪 Simulación"):
        st.session_state['env'], st.session_state['company_name'] = "Simulacion", "Innovatech Solutions SAS"
        st.session_state['base_path'] = setup_company_folders("Innovatech Solutions SAS")
        st.session_state['paso_ingesta'] = 0
        if logo_file:
            path = os.path.join(st.session_state['base_path'], "logo.png")
            with open(path, "wb") as f: f.write(logo_file.getbuffer())
            st.session_state['logo_path'] = path
        save_audit_state()
        st.rerun()
            
    if b2.button("🏗️ Crear"):
        if new_company:
            st.session_state['env'], st.session_state['company_name'] = "Real", new_company
            st.session_state['base_path'] = setup_company_folders(new_company)
            st.session_state['paso_ingesta'] = 0
            if logo_file:
                path = os.path.join(st.session_state['base_path'], "logo.png")
                with open(path, "wb") as f: f.write(logo_file.getbuffer())
                st.session_state['logo_path'] = path
            save_audit_state()
            st.rerun()
        else: st.warning("Ingrese nombre.")

# --- DASHBOARD ---
else:
    company, base_path = st.session_state['company_name'], st.session_state['base_path']
    st.sidebar.title(f"🏢 {company}")
    st.sidebar.write(f"📜 **Norma:** {st.session_state['norma']}")
    st.sidebar.divider()
    menu = st.sidebar.radio("Navegación", ["Dashboard", "Ingesta", "Formatos", "💎 Ayuda"])
    
    if st.sidebar.button("🔒 Salir"):
        save_audit_state()
        st.session_state['env'] = None
        st.rerun()

    if "Académico" in st.session_state['norma']:
        cartas = [
            {"doc": "PEI (Proyecto Educativo)", "ref": "Ley 115", "just": "Columna vertebral académica."},
            {"doc": "Registro Calificado", "ref": "Dec. 1330", "just": "Existencia legal del programa."},
            {"doc": "Estatuto Docente", "ref": "Dec. 1278", "just": "Garantía de idoneidad."}
        ]
    elif "Seguridad" in st.session_state['norma']:
        cartas = [
            {"doc": "Política de Seguridad", "ref": "ISO 27001 Cl. 5.2", "just": "Compromiso de protección."},
            {"doc": "Análisis de Riesgos", "ref": "ISO 27001 Cl. 6.1", "just": "Identificación de amenazas."},
            {"doc": "Inventario de Activos", "ref": "ISO 27001 Cl. 5.9", "just": "Control de recursos."}
        ]
    elif "Ambiental" in st.session_state['norma']:
        cartas = [
            {"doc": "Aspectos Ambientales", "ref": "ISO 14001 Cl. 6.1.2", "just": "Impactos significativos."},
            {"doc": "Objetivos Ambientales", "ref": "ISO 14001 Cl. 6.2", "just": "Metas de sostenibilidad."},
            {"doc": "Control Operacional", "ref": "ISO 14001 Cl. 8.1", "just": "Gestión de residuos/energía."}
        ]
    else: # Calidad ISO 9001
        cartas = [
            {"doc": "Contexto de la Organización", "ref": "ISO 9001 Cl. 4.1", "just": "Comprensión del entorno."},
            {"doc": "Política de Calidad", "ref": "ISO 9001 Cl. 5.2", "just": "Compromiso de dirección."},
            {"doc": "Mapa de Procesos", "ref": "ISO 9001 Cl. 4.4", "just": "Gestión por procesos."}
        ]

    if menu == "Dashboard":
        st.title(f"📊 Dashboard: {company}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Ingesta", f"{(st.session_state['paso_ingesta']/len(cartas))*100:.0f}%")
        m2.metric("Motor RAG", "ACTIVO")
        m3.metric("Seguridad", "SHA-256")
        
    elif menu == "Ingesta":
        st.title("🗺️ Ingesta Guiada")
        st.info("Suba evidencias PDF/Word para alimentar la IA.")
        if st.button("Simular Carga de Documento"):
            st.session_state['paso_ingesta'] += 1
            save_audit_state()
            st.success("Documento procesado.")

    elif menu == "Formatos":
        st.title("⚖️ Formatos Legales")
        if st.button("Generar Programa Base"):
            path = os.path.join(base_path, "01_Templates_Vacios", f"PROG_{company[:5]}.docx")
            create_audit_program_v2(company, path, st.session_state['logo_path'])
            st.success(f"Guardado en: {path}")

    elif menu == "💎 Ayuda":
        st.title("💎 Centro de Ayuda & Veracidad")
        tab1, tab2 = st.tabs(["📖 Guía", "🏛️ Normas"])
        tab1.write("Manual interactivo de operación local.")
        tab2.table(pd.DataFrame({
            "Norma": ["ISO 9001", "ISO 27001", "ISO 14001", "Dec. 1330"],
            "Especialidad": ["Calidad", "Seguridad", "Ambiental", "Académico"],
            "Estado": ["Anclado", "Anclado", "Anclado", "Anclado"]
        }))

st.divider()
st.caption("HMO Auditor Pro v1.3.4 | 🔒 Biblioteca Multi-Norma Expandida")
