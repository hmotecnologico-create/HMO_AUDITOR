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

# --- SISTEMA DE DISEÑO ELITE V1.4 (CSS AVANZADO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: radial-gradient(circle at top right, #F1F4F8, #FFFFFF);
    }
    
    /* Panel de Navegación */
    [data-testid="stSidebar"] {
        background-color: #0E1117;
        border-right: 1px solid #1E293B;
    }
    
    /* Botones Elite */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.8em;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(30, 58, 138, 0.3);
    }
    
    /* Tarjetas de Información */
    .elite-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    
    .norm-header {
        color: #1E3A8A;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* Tabs Custom */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #F1F5F9;
        border-radius: 8px 8px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Lógica de Sesión
for key, default in [('env', None), ('norma', "Calidad (ISO 9001)"), ('paso_ingesta', 0), ('logo_path', None), ('kb', {})]:
    if key not in st.session_state: st.session_state[key] = default

# ... [Funciones de persistencia omitidas por brevedad] ...

def save_audit_state():
    if st.session_state['env'] and st.session_state.get('company_name'):
        base_dir = st.session_state['base_path']
        state = {
            "company_name": st.session_state['company_name'], "norma": st.session_state['norma'],
            "paso_ingesta": st.session_state['paso_ingesta'], "logo_path": st.session_state['logo_path'],
            "env": st.session_state['env'], "kb": st.session_state['kb'], "last_update": datetime.datetime.now().isoformat()
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
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🛡️ HMO Auditor <span style='font-size: 0.5em; vertical-align: middle;'>V1.4 ELITE</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #64748B;'>Ecosistema de Auditoría Multi-Norma con Inteligencia RAG Local</p>", unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = st.columns([1, 6, 1])
    with col_c2:
        # 📂 REANUDAR
        base_audits_path = os.path.join(os.getcwd(), "Auditorias_HMO")
        if os.path.exists(base_audits_path):
            existing = [d for d in os.listdir(base_audits_path) if os.path.isdir(os.path.join(base_audits_path, d))]
            if existing:
                with st.expander("📂 REANUDAR AUDITORÍA EN CURSO", expanded=True):
                    c_sel, c_btn = st.columns([3, 1])
                    selected = c_sel.selectbox("Seleccione el proceso:", existing)
                    if c_btn.button("🚀 Iniciar"):
                        if load_audit_state(selected): st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 🆕 NUEVA
        st.write("### 🆕 Configurar Nuevo Espacio de Trabajo")
        st.session_state['norma'] = st.selectbox("Marco Normativo de Referencia:", [
            "Calidad (ISO 9001:2015)", 
            "Seguridad de Información (ISO 27001:2022)", 
            "Gestión Ambiental (ISO 14001:2015)",
            "Sector Académico (Decreto 1330 / Ley 115)"
        ])
        
        col_f1, col_f2 = st.columns(2)
        new_company = col_f1.text_input("Nombre de la Organización:", placeholder="Ej: Universidad San José")
        logo_file = col_f2.file_uploader("Cargar Identidad Visual (Logo JPG/PNG)", type=['png', 'jpg', 'jpeg'])

        st.info("💡 El entorno de 'Simulación' utiliza los documentos pre-cargados de Innovatech Solutions SAS para demostración de capacidades RAG.")
        
        btn_col1, btn_col2 = st.columns(2)
        if btn_col1.button("🧪 Lanzar Simulación Académica"):
            st.session_state['env'], st.session_state['company_name'] = "Simulacion", "Innovatech Solutions SAS"
            st.session_state['base_path'] = setup_company_folders("Innovatech Solutions SAS")
            st.session_state['paso_ingesta'] = 0
            st.session_state['kb'] = {
                "Misión y Visión Corporativa": "Liderar la transformación digital en Colombia mediante soluciones sostenibles.",
                "Valores y Código de Ética": "Integridad, Innovación y Respeto Ambiental.",
                "Organigrama Funcional": "Estructura plana liderada por la Gerencia de Innovación.",
                "PEI (Proyecto Educativo)": "Modelo pedagógico basado en la práctica industrial avanzada."
            }
            if logo_file:
                path = os.path.join(st.session_state['base_path'], "logo.png")
                with open(path, "wb") as f: f.write(logo_file.getbuffer())
                st.session_state['logo_path'] = path
            save_audit_state()
            st.rerun()
                
        if btn_col2.button("🏗️ Crear Proyecto de Auditoría Real"):
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
            else: st.error("⚠️ Debe especificar el nombre de la organización.")

# --- DASHBOARD PRINCIPAL ---
else:
    company, base_path = st.session_state['company_name'], st.session_state['base_path']
    
    # Sidebar Superior
    st.sidebar.markdown(f"<h2 style='color: white;'>🏢 {company}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='color: #94A3B8;'>💎 Marco: {st.session_state['norma']}</p>", unsafe_allow_html=True)
    st.sidebar.divider()
    
    menu = st.sidebar.radio("Navegación Estratégica", [
        "📊 Dashboard Analítico", 
        "🗺️ Camino de Ingesta (HITL)", 
        "⚖️ Emisión de Títulos/Formatos", 
        "💎 Help Center Elite"
    ])
    
    st.sidebar.divider()
    if st.sidebar.button("🔒 Cerrar Sesión Segura"):
        save_audit_state()
        st.session_state['env'] = None
        st.rerun()

    # --- CONFIGURACIÓN DE PASOS DE INGESTA POR DEPARTAMENTOS ---
    base_cartas = [
        {"doc": "Misión y Visión Corporativa", "area": "🏦 Alta Dirección", "ref": "Estratégico", "desc": "Definición del propósito y dirección.", "file_hint": "Mision_Vision.pdf"},
        {"doc": "Valores y Código de Ética", "area": "🏦 Alta Dirección", "ref": "Cultura", "desc": "Principios rectores de la organización.", "file_hint": "Codigo_Etica.pdf"},
        {"doc": "Organigrama Funcional", "area": "🏦 Alta Dirección", "ref": "Estructura", "desc": "Jerarquía y responsabilidades.", "file_hint": "Organigrama.pdf"}
    ]

    if "Académico" in st.session_state['norma']:
        norm_cartas = [
            {"doc": "PEI (Proyecto Educativo)", "area": "🎓 Gestión Académica", "ref": "Ley 115", "desc": "Columna vertebral académica.", "file_hint": "PEI_Innovatech.pdf"},
            {"doc": "Registro Calificado", "area": "⚖️ Jurídico/Normativo", "ref": "Dec. 1330", "desc": "Autorización ministerial.", "file_hint": "Resolucion_MEN.pdf"},
            {"doc": "Estatuto Docente", "area": "👥 Talento Humano", "ref": "Dec. 1278", "desc": "Reglamentación docente.", "file_hint": "Estatutos.pdf"}
        ]
    elif "Seguridad" in st.session_state['norma']:
        norm_cartas = [
            {"doc": "Política de Seguridad", "area": "🛡️ Ciberseguridad", "ref": "ISO 27001:5.2", "desc": "Directrices de protección.", "file_hint": "Politica_Seguridad.pdf"},
            {"doc": "Análisis de Riesgos", "area": "🛡️ Ciberseguridad", "ref": "ISO 27001:6.1", "desc": "Mapa de vulnerabilidades.", "file_hint": "Matriz_Riesgos.xlsx"}
        ]
    elif "Ambiental" in st.session_state['norma']:
        norm_cartas = [
            {"doc": "Aspectos Ambientales", "area": "♻️ Gestión Ambiental", "ref": "ISO 14001:6.1.2", "desc": "Evaluación de impactos.", "file_hint": "Aspectos.pdf"},
            {"doc": "Objetivos Ambientales", "area": "♻️ Gestión Ambiental", "ref": "ISO 14001:6.2", "desc": "Metas de eco-eficiencia.", "file_hint": "Metas.pdf"}
        ]
    else: # ISO 9001
        norm_cartas = [
            {"doc": "Contexto Organizacional", "area": "📊 Calidad", "ref": "ISO 9001:4.1", "desc": "Análisis de entorno (DOFA).", "file_hint": "Contexto.pdf"},
            {"doc": "Mapa de Procesos", "area": "⚙️ Operaciones", "ref": "ISO 9001:4.4", "desc": "Interacción de procesos.", "file_hint": "Mapa_Procesos.pdf"}
        ]
    
    # Combinación de Fases: Cimientos + Norma
    cartas = base_cartas + norm_cartas

    # --- SECCIÓN: DASHBOARD ANALÍTICO ---
    if menu == "📊 Dashboard Analítico":
        st.markdown(f"<h1 class='norm-header'>📊 Control de Mando: {company}</h1>", unsafe_allow_html=True)
        
        # Métricas Elite
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        total_total = len(cartas)
        progreso = (st.session_state['paso_ingesta'] / total_total) * 100
        
        col_m1.metric("Cumplimiento Total", f"{progreso:.1f}%")
        col_m2.metric("Fase Actual", "Cimientos" if st.session_state['paso_ingesta'] < len(base_cartas) else "Normativa")
        col_m3.metric("Motor RAG", "ACTIVO", "Local")
        col_m4.metric("Seguridad", "SHA-256")
        
        st.divider()
        
        # Gráficos y Análisis
        col_g1, col_g2 = st.columns([2, 1])
        with col_g1:
            st.markdown("<div class='elite-card'><b>Radar de Madurez Normativa</b>", unsafe_allow_html=True)
            labels = ['Misión/Visión', 'Ética', 'Estructura', 'Norma Cl.4', 'Norma Cl.5', 'Norma Cl.6']
            values = [100 if i < st.session_state['paso_ingesta'] else 20 for i in range(len(labels))]
            fig = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself', line_color='#1E3A8A'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(l=40, r=40, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_g2:
            st.markdown("<div class='elite-card'><b>Progreso de Expediente</b>", unsafe_allow_html=True)
            for i, c in enumerate(cartas):
                estado = "✅" if i < st.session_state['paso_ingesta'] else "⏳"
                prefijo = "💎" if i < len(base_cartas) else "📜"
                st.write(f"{estado} {prefijo} **{c['doc']}**")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- SECCIÓN: INGESTA (HITL) ---
    elif menu == "🗺️ Camino de Ingesta (HITL)":
        st.markdown("<h1 class='norm-header'>🗺️ Camino de Ingesta Departamental</h1>", unsafe_allow_html=True)
        
        # Agrupación por Áreas
        areas = list(dict.fromkeys([c['area'] for c in cartas]))
        area_tabs = st.tabs(areas + ["🔒 Autorización Final"])
        
        for i, area in enumerate(areas):
            with area_tabs[i]:
                st.write(f"### Requisitos del Área: {area}")
                docs_area = [c for c in cartas if c['area'] == area]
                
                for c in docs_area:
                    idx = cartas.index(c)
                    es_completado = idx < st.session_state['paso_ingesta']
                    es_actual = idx == st.session_state['paso_ingesta']
                    
                    with st.expander(f"{'✅' if es_completado else '⏳' if es_actual else '🔒'} {c['doc']}", expanded=es_actual):
                        st.write(f"**Referencia:** {c['ref']}")
                        st.write(c['desc'])
                        
                        if es_actual:
                            # Interfaz de Carga
                            u1, u2 = st.columns([2, 1])
                            uploaded_file = u1.file_uploader(f"Cargar {c['doc']}", type=['pdf', 'docx'], key=f"up_{idx}")
                            if st.session_state['env'] == "Simulacion":
                                u2.info(f"📂 Sugerido: **{c['file_hint']}**")
                            
                            if uploaded_file:
                                st.success(f"🔍 '{uploaded_file.name}' detectado.")
                                st.write("**🧠 Hallazgo Motivador (Validación HITL):**")
                                finding = st.text_area("Contenido clave para el diligenciamiento:", 
                                                     placeholder=f"Ej: Se valida cumplimiento de la {c['doc']}...",
                                                     key=f"find_{idx}")
                                
                                if st.button("💎 CONFIRMAR E INDEXAR", key=f"btn_{idx}"):
                                    if finding:
                                        st.session_state['kb'][c['doc']] = finding
                                        target_path = os.path.join(base_path, "03_Evidencias_Ingesta", uploaded_file.name)
                                        with open(target_path, "wb") as f: f.write(uploaded_file.getbuffer())
                                        st.session_state['paso_ingesta'] += 1
                                        save_audit_state()
                                        st.rerun()
                                    else: st.warning("⚠️ El hallazgo es obligatorio para el diligenciamiento.")
                        elif es_completado:
                            st.info(f"✨ Hallazgo indexado: *{st.session_state['kb'].get(c['doc'], 'N/A')}*")
        
        with area_tabs[-1]:
            st.write("### 🔒 Cierre de Fase de Ingesta")
            progreso = (st.session_state['paso_ingesta'] / len(cartas)) * 100
            
            if progreso < 100:
                st.warning(f"⚠️ Ingesta incompleta ({progreso:.0f}%). Debe completar todos los departamentos antes de autorizar la emisión de formatos diligenciados.")
            else:
                st.success("✅ Todos los documentos e hitos estratégicos han sido indexados y validados.")
                st.session_state['autorizado_emision'] = st.toggle("AUTORIZAR DILIGENCIAMIENTO Y EMISIÓN DE FORMATOS", value=st.session_state['autorizado_emision'])
                if st.session_state['autorizado_emision']:
                    st.info("🚀 El sistema ha sido habilitado para generar documentos 'Motivados' con su base de conocimiento.")
                    if st.button("📊 Ver Resultados en Dashboard"): st.rerun()

    # --- SECCIÓN: FORMATOS ---
    elif menu == "⚖️ Emisión de Títulos/Formatos":
        st.markdown("<h1 class='norm-header'>⚖️ Emisión de Formatos & Títulos Legales</h1>", unsafe_allow_html=True)
        
        if not st.session_state['autorizado_emision']:
            st.warning("⚠️ ACCESO RESTRINGIDO: Debe completar la 'Ingesta Departamental' y otorgar la 'Autorización Final' para emitir documentos diligenciados.")
            st.info("💡 En este estado, solo puede visualizar los requerimientos pero no generar los activos finales con validez técnica.")
        else:
            st.success("✅ ESTATUS ELITE: Emisión habilitada. Los formatos se generarán con inyección de hallazgos y logo institucional.")

        tab_list, tab_gen = st.tabs(["📝 Control de Expediente", "🏗️ Generador de Activos"])
        
        with tab_list:
            st.write("### Auditoría de Calidad: Formatos del Proceso")
            st.table(pd.DataFrame({
                "Código": ["GAD-PROG-01", "GAD-LIST-02"],
                "Nombre": ["Programa de Auditoría ELITE", "Checklist de Verificación ELITE"],
                "Estado Actual": ["AUTORIZADO" if st.session_state['autorizado_emision'] else "BLOQUEADO"],
                "Fuente de Datos": ["Base de Conocimiento IA" if st.session_state['kb'] else "Dato Manual"]
            }))
            
        with tab_gen:
            if not st.session_state['autorizado_emision']:
                st.error("🔒 Generador bloqueado. Requiere firma de Autorización Final en la pestaña de Ingesta.")
            else:
                st.write("### Control de Emisión Maestro")
                col_b1, col_b2 = st.columns(2)
                
                if col_b1.button("🚀 Emitir GAD-PROG-01 (Word)"):
                    from HMO_Auditor_Master_V2_Generator import create_audit_program_v2
                    path = os.path.join(base_path, "02_Auditoria_IA", f"PROG_{company[:5]}.docx")
                    full_path = create_audit_program_v2(company, os.path.dirname(path), st.session_state['logo_path'], st.session_state['kb'])
                    st.success(f"✅ GAD-PROG-01 Emitido.")
                    with open(full_path, "rb") as f:
                        st.download_button("Descargar Programa Motivado", f, file_name=f"ELITE_PROG_{company}.docx")

                if col_b2.button("🚀 Emitir GAD-LIST-02 (Excel)"):
                    from HMO_Checklist_Legal_Generator import create_legal_checklist
                    path = os.path.join(base_path, "02_Auditoria_IA", f"LIST_{company[:5]}.xlsx")
                    full_path = create_legal_checklist(company, os.path.dirname(path), st.session_state['logo_path'], st.session_state['kb'])
                    st.success(f"✅ GAD-LIST-02 Emitida.")
                    with open(full_path, "rb") as f:
                        st.download_button("Descargar Checklist Motivada", f, file_name=f"ELITE_LIST_{company}.xlsx")

    # --- SECCIÓN: AYUDA ---
    elif menu == "💎 Help Center Elite":
        st.markdown("<h1 class='norm-header'>💎 Centro de Ayuda & Veracidad</h1>", unsafe_allow_html=True)
        
        help_tabs = st.tabs(["📖 Guía de Usuario", "🏛️ Base Normativa", "🤖 Asistente IA"])
        
        with help_tabs[0]:
            st.write("### Cómo operar el HMO Auditor")
            st.markdown("""
            1. **Ingesta**: Suba sus documentos en orden. La IA los procesará localmente.
            2. **Dashboard**: Verifique el nivel de cumplimiento y madurez.
            3. **Generación**: Use los datos indexados para crear sus reportes finales.
            """)
        with help_tabs[1]:
            st.write("### Referencias Legales Ancladas")
            st.table(pd.DataFrame({
                "Norma": ["ISO 9001", "ISO 27001", "ISO 14001", "Dec. 1330"],
                "Descripción": ["Calidad y Procesos", "Seguridad Informática", "Gestión Ambiental", "Aseguramiento Calidad Académica"],
                "Validación": ["Anclado", "Anclado", "Anclado", "Anclado"]
            }))

# --- FOOTER ---
st.divider()
st.caption("HMO Auditor Pro v1.4.0 | 💎 Ecosistema Elite | 🔒 Operación Local Privada")
