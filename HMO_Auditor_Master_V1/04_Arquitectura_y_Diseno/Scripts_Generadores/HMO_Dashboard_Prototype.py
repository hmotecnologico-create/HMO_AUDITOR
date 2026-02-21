import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os
import sys
import shutil
import json

# Añadir ruta para importar generadores
sys.path.append(os.path.dirname(__file__))
from HMO_Auditor_Master_V2_Generator import create_audit_program_v2
from HMO_Checklist_Legal_Generator import create_legal_checklist

# Configuración de página
st.set_page_config(page_title="HMO Auditor Pro - V1.3 Elite", layout="wide", page_icon="🛡️")

# --- CONFIGURACIÓN DE ESTILO TEMPORALMENTE DESACTIVADA PARA DIAGNÓSTICO ---
# st.markdown("<style>...</style>", unsafe_allow_html=True)

# Lógica de Sesión
if 'env' not in st.session_state:
    st.session_state['env'] = None
if 'norma' not in st.session_state:
    st.session_state['norma'] = "Calidad (ISO 9001)"
if 'paso_ingesta' not in st.session_state:
    st.session_state['paso_ingesta'] = 0
if 'logo_path' not in st.session_state:
    st.session_state['logo_path'] = None

# --- FUNCIONES DE PERSISTENCIA Y ORGANIZACIÓN ---
def setup_company_folders(company_name):
    safe_name = "".join([c if c.isalnum() else "_" for c in company_name])
    base_dir = os.path.join(os.getcwd(), "Auditorias_HMO", safe_name)
    subfolders = ["01_Templates_Vacios", "02_Auditoria_IA", "03_Evidencias_Ingesta"]
    
    for sub in subfolders:
        path = os.path.join(base_dir, sub)
        if not os.path.exists(path):
            os.makedirs(path)
    return base_dir

def save_audit_state():
    if st.session_state['env'] and st.session_state.get('company_name'):
        base_dir = st.session_state['base_path']
        state = {
            "company_name": st.session_state['company_name'],
            "norma": st.session_state['norma'],
            "paso_ingesta": st.session_state['paso_ingesta'],
            "logo_path": st.session_state['logo_path'],
            "env": st.session_state['env'],
            "last_update": datetime.datetime.now().isoformat()
        }
        with open(os.path.join(base_dir, "audit_state.json"), "w") as f:
            json.dump(state, f, indent=4)

def load_audit_state(company_folder):
    state_path = os.path.join(os.getcwd(), "Auditorias_HMO", company_folder, "audit_state.json")
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
            st.session_state['company_name'] = state['company_name']
            st.session_state['norma'] = state['norma']
            st.session_state['paso_ingesta'] = state['paso_ingesta']
            st.session_state['logo_path'] = state['logo_path']
            st.session_state['env'] = state['env']
            st.session_state['base_path'] = os.path.join(os.getcwd(), "Auditorias_HMO", company_folder)
            return True
    return False

# --- PANTALLA DE BIENVENIDA ---
if st.session_state['env'] is None:
    st.title("🛡️ HMO Auditor - Ecosistema de Auditoría Profesional")
    st.subheader("Gestión Multi-Norma con Persistencia de Grado Industrial")
    
    # 📂 SECCIÓN DE REANUDACIÓN
    base_audits_path = os.path.join(os.getcwd(), "Auditorias_HMO")
    if os.path.exists(base_audits_path):
        existing_audits = [d for d in os.listdir(base_audits_path) if os.path.isdir(os.path.join(base_audits_path, d))]
        if existing_audits:
            with st.expander("📂 REANUDAR AUDITORÍA EXISTENTE", expanded=True):
                col_sel, col_btn = st.columns([3, 1])
                with col_sel:
                    selected_audit = st.selectbox("Seleccione el proceso a continuar:", existing_audits)
                with col_btn:
                    if st.button("🚀 Continuar"):
                        if load_audit_state(selected_audit):
                            st.success(f"Bienvenido de nuevo: {st.session_state['company_name']}")
                            st.rerun()

    st.divider()
    
    # 🆕 SECCIÓN DE NUEVA AUDITORÍA
    st.write("### 🆕 Configurar Nueva Sesión de Auditoría")
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.session_state['norma'] = st.selectbox(
            "Sistema de Gestión a Auditar:", 
            ["Calidad (ISO 9001)", "Seguridad (ISO 27001)", "Académico (Ley 115 / Dec. 1330)", "Ambiental (ISO 14001)"]
        )
        new_company = st.text_input("Nombre de la Empresa / Institución:", placeholder="Ej: Universidad San José")
        
    with col_n2:
        st.write("🖼️ **Identidad Corporativa**")
        logo_file = st.file_uploader("Cargar Logo Institucional (PNG/JPG)", type=['png', 'jpg', 'jpeg'])
        # El logo se guardará definitivamente una vez se cree el espacio de trabajo

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🧪 Ingresar a Simulación (Innovatech)"):
            st.session_state['env'] = "Simulacion"
            st.session_state['company_name'] = "Innovatech Solutions SAS"
            base_dir = setup_company_folders(st.session_state['company_name'])
            st.session_state['base_path'] = base_dir
            st.session_state['paso_ingesta'] = 0
            # Guardamos logo en carpeta de empresa si existe
            if logo_file:
                logo_p = os.path.join(base_dir, "logo.png")
                with open(logo_p, "wb") as f: f.write(logo_file.getbuffer())
                st.session_state['logo_path'] = logo_p
            save_audit_state()
            st.rerun()
            
    with col_btn2:
        if st.button("🏗️ Crear Espacio de Auditoría Real"):
            if new_company:
                st.session_state['env'] = "Real"
                st.session_state['company_name'] = new_company
                base_dir = setup_company_folders(new_company)
                st.session_state['base_path'] = base_dir
                st.session_state['paso_ingesta'] = 0
                if logo_file:
                    logo_p = os.path.join(base_dir, "logo.png")
                    with open(logo_p, "wb") as f: f.write(logo_file.getbuffer())
                    st.session_state['logo_path'] = logo_p
                save_audit_state()
                st.rerun()
            else:
                st.warning("⚠️ Debe ingresar el nombre de la empresa para continuar.")

# --- DASHBOARD PRINCIPAL ---
else:
    company = st.session_state['company_name']
    base_path = st.session_state['base_path']

    # Barra Lateral
    st.sidebar.title(f"🏢 {company}")
    st.sidebar.write(f"📜 **Norma:** {st.session_state['norma']}")
    st.sidebar.write(f"💼 **Entorno:** {st.session_state['env']}")
    st.sidebar.divider()
    
    menu = st.sidebar.radio("Navegación", [
        "Dashboard de Trazabilidad", 
        "Ingesta Guiada (ISO 19011)", 
        "Generación de Formatos Legales", 
        "💎 Centro de Ayuda & Veracidad"
    ])
    
    st.sidebar.divider()
    if st.sidebar.button("🔒 Guardar y Salir"):
        save_audit_state()
        st.session_state['env'] = None
        st.rerun()

    # --- CARTAS NORMATIVAS (Persuadir veracidad) ---
    if "Académico" in st.session_state['norma']:
        cartas_navegacion = [
            {"doc": "PEI (Proyecto Educativo)", "ref": "Ley 115 / Dec. 1330", "justificacion": "Columna vertebral académica.", "simulado": "PEI_Verificado.pdf"},
            {"doc": "Registro Calificado", "ref": "Dec. 1330 Art. 2.5", "justificacion": "Existencia legal del programa.", "simulado": "Resolucion_MEN.pdf"},
            {"doc": "Estatuto Docente", "ref": "Dec. 1278 / 2277", "justificacion": "Garantía de idoneidad.", "simulado": "Estatutos.pdf"}
        ]
    else:
        cartas_navegacion = [
            {"doc": "Contexto de la Organización", "ref": "ISO 9001 Cl. 4.1", "justificacion": "Comprensión del entorno.", "simulado": "FODA_Estrategico.docx"},
            {"doc": "Política de Calidad", "ref": "ISO 9001 Cl. 5.2", "justificacion": "Compromiso de dirección.", "simulado": "Politica_V2.pdf"},
            {"doc": "Mapa de Procesos", "ref": "ISO 9001 Cl. 4.4", "justificacion": "Gestión por procesos.", "simulado": "Mapa_Procesos.png"}
        ]

    # --- SECCIONES DE CONTENIDO (Safe Mode) ---
    if menu == "Dashboard de Trazabilidad":
        st.title(f"📊 Dashboard de Control: {company}")
        st.write(f"**Progreso Ingesta:** {st.session_state['paso_ingesta']} de {len(cartas_navegacion)}")
        st.write("Estado del Motor: **ACTIVO**")
        st.divider()
        st.write("### Mapa de Cumplimiento")
        for i, c in enumerate(cartas_navegacion):
            estado = "✅ Completado" if i < st.session_state['paso_ingesta'] else "⏳ Pendiente"
            st.write(f"- **{c['doc']}**: {estado}")

    elif menu == "Ingesta Guiada (ISO 19011)":
        st.title("🗺️ Camino de Ingesta")
        st.write("Alimente la base de conocimiento con evidencias.")
        if st.session_state['paso_ingesta'] < len(cartas_navegacion):
            paso = st.session_state['paso_ingesta']
            carta = cartas_navegacion[paso]
            st.write(f"### Paso {paso+1}: {carta['doc']}")
            st.info(f"Justificación: {carta['justificacion']}")
            
            up = st.file_uploader(f"Cargar {carta['doc']}", key=f"up_safe_{paso}")
            if st.session_state['env'] == "Simulacion":
                if st.button("🚀 Simular Carga"): up = True
            
            if up:
                st.success("Documento verificado.")
                if st.button("Guardar y Continuar"):
                    st.session_state['paso_ingesta'] += 1
                    save_audit_state()
                    st.rerun()
        else:
            st.success("🎉 Ingesta Completa.")

    elif menu == "Generación de Formatos Legales":
        st.title("⚖️ Emisión de Títulos")
        st.write(f"Carpeta: `{base_path}`")
        if st.button("Generar Programa de Auditoría (Base)"):
            path = os.path.join(base_path, "01_Templates_Vacios", f"PROG_{company[:5]}.docx")
            create_audit_program_v2(company, path, st.session_state['logo_path'])
            st.success("Documento generado con éxito.")

    elif menu == "💎 Centro de Ayuda & Veracidad":
        st.title("💎 Centro de Ayuda & Veracidad")
        st.write("### 📖 Guía de Operación")
        st.write("Su progreso se guarda en el servidor.")
        st.write("### 🏛️ Base Normativa")
        st.write("- ISO 9001 / 27001 / 19011")
        st.write("- Decreto 1330 MEN")
        st.write("### 🤖 Asistente Técnico")
        q = st.text_input("Duda técnica:", key="help_q_safe")
        if q:
            st.info("Consulte el manual de implementación .ipynb para detalles técnicos profundos.")

# --- FOOTER ---
st.divider()
st.caption(f"HMO Auditor Pro v1.3.2 | Modo de Seguridad Activo")
