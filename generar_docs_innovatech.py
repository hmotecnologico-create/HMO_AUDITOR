"""
GENERADOR DE DOCUMENTOS BASE DE INGESTA
Empresa: Innovatech Solutions SAS
Normas: SIG, ISO 9001, ISO 27001, ISO 14001
Autor: HMO Auditor Elite V13.1
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 
    "HMO_Auditor_Master_V1", "04_Arquitectura_y_Diseno", "Scripts_Generadores"))

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import datetime

COMPANY   = "Innovatech Solutions SAS"
NIT       = "901.456.789-3"
REP_LEGAL = "Carlos Eduardo Mora"
AUDITOR   = "HMO Auditor Elite"
SECTOR    = "Tecnologia de la Informacion"
CIUDAD    = "Bogota D.C."
DIR       = "Calle 100 #7-33, Torre Empresarial Norte, Piso 8"
OUT_DIR   = os.path.join(os.getcwd(), "Auditorias_HMO", "Innovatech_Solutions_SAS", "01_Documentos_Base")

TODAY = datetime.date.today().strftime("%d/%m/%Y")

NORMAS_COLOR = {
    "SIG":       (10,  30,  70),
    "CALIDAD":   (20,  80, 150),
    "SEGURIDAD": (140,  20,  20),
    "AMBIENTAL": (20, 110,  50),
    "ACADEMICO": (80,  20, 120),
}

def safe(text):
    if not isinstance(text, str): text = str(text)
    return text.encode("latin-1", "replace").decode("latin-1")

class DocPDF(FPDF):
    def __init__(self, norma="SIG"):
        super().__init__()
        self.norma = norma
        self.color = NORMAS_COLOR.get(norma, (10, 30, 70))

    def header(self):
        r, g, b = self.color
        self.set_fill_color(r, g, b)
        self.rect(0, 0, 210, 18, "F")
        self.set_font("helvetica", "B", 9)
        self.set_text_color(255, 255, 255)
        self.set_y(4)
        self.cell(0, 5, safe(f"{COMPANY}  |  NIT: {NIT}  |  {CIUDAD}"), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.cell(0, 5, safe(f"Marco Normativo: {self.norma}  |  Generado: {TODAY}  |  Auditor: {AUDITOR}"), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, safe(f"Pagina {self.page_no()}  |  HMO Auditor Elite  |  Documento de Uso Interno  |  {COMPANY}"), align="C")

    def section_header(self, text):
        r, g, b = self.color
        self.set_fill_color(r, g, b)
        self.set_font("helvetica", "B", 11)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, safe(text), fill=True, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.set_font("helvetica", "", 10)
        self.ln(2)

    def sub_header(self, text):
        self.set_font("helvetica", "B", 10)
        self.set_fill_color(220, 225, 235)
        self.cell(0, 7, safe(text), fill=True, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("helvetica", "", 10)
        self.ln(1)

    def body(self, text):
        self.multi_cell(0, 6, safe(text))
        self.ln(3)

    def firma_block(self):
        self.ln(10)
        y = self.get_y()
        self.line(self.l_margin, y, self.l_margin + 60, y)
        self.line(self.w - self.r_margin - 60, y, self.w - self.r_margin, y)
        self.ln(3)
        self.set_font("helvetica", "B", 8)
        self.cell(90, 5, "ELABORADO POR:", new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.cell(0, 5, safe(f"AUDITOR: {AUDITOR}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("helvetica", "", 8)
        self.cell(90, 5, safe(f"Rep. Legal: {REP_LEGAL}"), new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.cell(0, 5, safe(f"Fecha: {TODAY}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def write_lines(self, n=15):
        for _ in range(n):
            y_pos = self.get_y() + 8
            if y_pos < self.h - self.b_margin - 5:
                self.line(self.l_margin, y_pos, self.w - self.r_margin, y_pos)
            self.ln(9)


os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# DOCUMENTOS SIG (BASE LEGAL)
# ============================================================
docs_sig = [
    {
        "nombre": "Camara de Comercio - Existencia Legal",
        "norma": "SIG",
        "ref": "ISO 19011:6.3.1",
        "secciones": [
            ("Datos de la Empresa", 
             f"Razon Social: {COMPANY}\nNIT: {NIT}\nRepresentante Legal: {REP_LEGAL}\nDireccion: {DIR}\nCiudad: {CIUDAD}\nSector: {SECTOR}"),
            ("Objeto Social",
             "Prestacion de servicios de tecnologia de la informacion, desarrollo de software a medida, consultoria en transformacion digital y ciberseguridad para empresas del sector privado y publico en Colombia."),
            ("Estado de la Empresa",
             "La empresa se encuentra ACTIVA y al dia con sus obligaciones mercantiles segun el ultimo certificado expedido por la Camara de Comercio de Bogota.\nVigencia del certificado: 30 dias a partir de la fecha de expedicion."),
            ("Nota del Auditor",
             "INSTRUCCION: Reemplace este documento con el certificado oficial descargado de www.ccb.org.co con vigencia no mayor a 30 dias. Este es un documento de placeholder para las pruebas iniciales de ingesta."),
        ]
    },
    {
        "nombre": "RUT - Registro Unico Tributario",
        "norma": "SIG",
        "ref": "DIAN Colombia",
        "secciones": [
            ("Datos Tributarios Principales",
             f"Razon Social: {COMPANY}\nNIT: {NIT}\nTipo de Contribuyente: Persona Juridica\nResponsabilidad: Regimen Comun (Responsable de IVA)\nActividad Economica: 6201 - Actividades de desarrollo de sistemas informaticos\nDireccion Fiscal: {DIR}"),
            ("Responsabilidades Tributarias",
             "- IVA: Responsable\n- Impuesto de Renta: Declarante\n- Retencion en la Fuente: Agente retenedor\n- ICA: Declarante Ciudad de Bogota"),
            ("Nota del Auditor",
             "INSTRUCCION: Reemplace con el RUT oficial descargado desde www.dian.gov.co. Asegurese de que este actualizado con la informacion vigente de la empresa."),
        ]
    },
    {
        "nombre": "Acta de Compromiso Directivo",
        "norma": "SIG",
        "ref": "ISO 9001:5.1 / ISO 19011:6.2.2",
        "secciones": [
            ("Apertura del Acta",
             f"En la ciudad de {CIUDAD}, siendo las 9:00 a.m. del dia {TODAY}, se reunieron en las instalaciones de {COMPANY} los directivos de la organizacion para suscribir el presente Acta de Compromiso Directivo para la realizacion de la Auditoria Interna Integrada."),
            ("Participantes",
             f"- {REP_LEGAL}: Gerente General\n- [Nombre]: Coordinador de Calidad (SIG)\n- [Nombre]: Director de Operaciones\n- [Nombre]: Director Administrativo y Financiero\n- Auditor Lider: {AUDITOR}"),
            ("Declaracion de Compromiso",
             f"La Alta Direccion de {COMPANY} declara formalmente:\n\n1. El compromiso irrestricto con la implementacion y mejora del Sistema de Gestion Integrado (ISO 9001, ISO 27001).\n2. La asignacion de los recursos humanos, tecnologicos y financieros necesarios para el proceso de auditoria.\n3. La cooperacion total del personal con el equipo auditor.\n4. La aceptacion de los hallazgos como oportunidades de mejora continua."),
            ("Designacion de Responsables",
             "Proceso Calidad: [Nombre] - Cargo: Coord. SIG\nProceso TI: [Nombre] - Cargo: Dir. Tecnologia\nProceso RRHH: [Nombre] - Cargo: Dir. Talento Humano\nProceso Finanzas: [Nombre] - Cargo: Dir. Financiero\nProceso Comercial: [Nombre] - Cargo: Dir. Comercial"),
            ("Cierre",
             f"Siendo las 10:30 a.m., se da por terminada la reunion y los presentes firman en constancia de acuerdo.\n\nFecha: {TODAY}"),
        ]
    },
    {
        "nombre": "Cronograma de Preparacion Auditoria",
        "norma": "SIG",
        "ref": "ISO 19011:6.3.2",
        "secciones": [
            ("Objetivo del Cronograma",
             f"Establecer las fechas y responsables para la entrega de la informacion documentada que sera objeto de revision por parte del equipo auditor de {COMPANY}."),
            ("Actividades Programadas",
             "ACTIVIDAD                            RESPONSABLE        FECHA LIMITE    ESTADO\n" + "-"*70 + "\n"
             "Entrega Camara de Comercio           Juridico           [DD/MM/AAAA]    Pendiente\n"
             "Entrega RUT actualizado              Contabilidad       [DD/MM/AAAA]    Pendiente\n"
             "Entrega Estados Financieros          Finanzas           [DD/MM/AAAA]    Pendiente\n"
             "Entrega Manual de Procesos           Calidad            [DD/MM/AAAA]    Pendiente\n"
             "Entrega Politica de Seguridad        TI                 [DD/MM/AAAA]    Pendiente\n"
             "Revision IA de Documentos            Auditor Lider      [DD/MM/AAAA]    Pendiente\n"
             "Apertura de Auditoria de Campo       Todos              [DD/MM/AAAA]    Pendiente"),
            ("Responsable del Seguimiento",
             f"El seguimiento del cumplimiento del cronograma estara a cargo del Coordinador de Calidad de {COMPANY} en coordinacion con el Auditor Lider {AUDITOR}."),
        ]
    },
    {
        "nombre": "Mision y Vision Corporativa",
        "norma": "SIG",
        "ref": "ISO 9001:4.1",
        "secciones": [
            ("MISION",
             f"En {COMPANY}, somos una empresa colombiana dedicada a la prestacion de servicios de tecnologia de la informacion de alta calidad. Desarrollamos soluciones de software a medida, consultoria en transformacion digital y ciberseguridad, con el objetivo de impulsar la competitividad de nuestros clientes mediante la innovacion tecnologica responsable y el talento humano comprometido."),
            ("VISION",
             f"Para el ano 2030, {COMPANY} sera reconocida como la firma de consultoria tecnologica mas confiable del mercado colombiano de mediana empresa, certificada internacionalmente en ISO 9001 e ISO 27001, con presencia en los principales centros economicos del pais y un equipo de mas de 200 profesionales especializados."),
            ("VALORES CORPORATIVOS",
             "- Innovacion: Buscamos constantemente nuevas formas de agregar valor.\n- Integridad: Actuamos con transparencia y etica en todos nuestros procesos.\n- Excelencia: Nos comprometemos con la calidad superior en cada entregable.\n- Colaboracion: Construimos relaciones de largo plazo basadas en la confianza.\n- Responsabilidad: Respondemos por nuestros compromisos con clientes y colaboradores."),
            ("Aprobacion",
             f"Aprobado por la Gerencia General de {COMPANY}\nFecha de aprobacion: {TODAY}\nVersion: 3.0 | Vigencia: 2024-2030"),
        ]
    },
]

# ============================================================
# DOCUMENTOS CALIDAD (ISO 9001)
# ============================================================
docs_calidad = [
    {
        "nombre": "Contexto Organizacional - Matriz DOFA",
        "norma": "CALIDAD",
        "ref": "ISO 9001:4.1",
        "secciones": [
            ("Objetivo del Analisis",
             f"Identificar los factores internos y externos que afectan la capacidad de {COMPANY} para lograr los resultados previstos de su Sistema de Gestion de Calidad."),
            ("FORTALEZAS (Factores Internos Positivos)",
             "F1: Equipo tecnico altamente calificado con certificaciones internacionales.\nF2: Portafolio diversificado de servicios TI adaptado a PyMEs y grandes empresas.\nF3: Cultura organizacional orientada a la innovacion y mejora continua.\nF4: Relaciones solidas con clientes estrategicos en sectores financiero y salud.\nF5: Infraestructura tecnologica de ultima generacion (Cloud/On-premise)."),
            ("DEBILIDADES (Factores Internos Negativos)",
             "D1: Alta dependencia de personal clave en proyectos criticos.\nD2: Procesos documentados parcialmente, con brechas en el SGC.\nD3: Limitada estructura comercial para expansion geografica.\nD4: Rotacion media del equipo tecnico junior (22% anual).\nD5: Ausencia de certificacion ISO formal (en proceso)."),
            ("OPORTUNIDADES (Factores Externos Positivos)",
             "O1: Crecimiento del mercado de transformacion digital en Colombia (+35% 2023-2025).\nO2: Politica de Colombia Digital del Gobierno Nacional favorece la contratacion TI.\nO3: Auge del trabajo remoto genera demanda de soluciones de ciberseguridad.\nO4: Tratados de libre comercio facilitan exportacion de servicios TI.\nO5: Disponibilidad de talento STEM en universidades colombianas."),
            ("AMENAZAS (Factores Externos Negativos)",
             "A1: Intensa competencia de empresas multinacionales con mayor respaldo financiero.\nA2: Volatilidad cambiaria afecta proyectos con componente internacional.\nA3: Escasez global de especialistas en ciberseguridad eleva costos laborales.\nA4: Evolucion rapida de amenazas ciberneticas requiere inversion continua.\nA5: Cambios regulatorios en proteccion de datos (Ley 1581) exigen adaptacion constante."),
        ]
    },
    {
        "nombre": "Mapa de Procesos",
        "norma": "CALIDAD",
        "ref": "ISO 9001:4.4",
        "secciones": [
            ("Descripcion del Mapa de Procesos",
             f"El mapa de procesos de {COMPANY} representa la interaccion de todos los procesos del Sistema de Gestion de Calidad, clasificados en tres categorias segun su naturaleza estrategica y operativa."),
            ("PROCESOS ESTRATEGICOS (Direccion)",
             "PE-01: Gestion Estrategica y Direccionamiento\nPE-02: Gestion del Sistema Integrado (SIG/SGC)\nPE-03: Gestion de Innovacion y Tecnologia\nPE-04: Revision por la Direccion"),
            ("PROCESOS MISIONALES (Valor al Cliente)",
             "PM-01: Gestion Comercial y de Propuestas\nPM-02: Desarrollo de Software a Medida\nPM-03: Consultoria en Transformacion Digital\nPM-04: Soporte y Mantenimiento de Sistemas\nPM-05: Ciberseguridad y Auditoria TI"),
            ("PROCESOS DE SOPORTE (Apoyo)",
             "PS-01: Gestion de Talento Humano y Competencias\nPS-02: Gestion Financiera y Contable\nPS-03: Gestion de Compras y Proveedores\nPS-04: Gestion Documental e Informacion\nPS-05: Gestion de Infraestructura Tecnologica"),
            ("Indicadores de Desempeno del Mapa",
             "- Satisfaccion del cliente: Meta > 90% | Medicion: Trimestral\n- Cumplimiento de entrega de proyectos: Meta > 95% | Medicion: Mensual\n- Eficiencia de procesos: Meta > 85% | Medicion: Semestral"),
        ]
    },
    {
        "nombre": "Manual de Funciones y Perfiles - Cargos Clave",
        "norma": "CALIDAD",
        "ref": "ISO 9001:7.2",
        "secciones": [
            ("Gerente General",
             "MISION DEL CARGO: Dirigir estrategicamente a Innovatech Solutions SAS hacia el logro de sus objetivos corporativos.\nFUNCIONES: Aprobar la politica de calidad, asignar recursos, revisar resultados del SGC.\nPERFIL: Profesional universitario en Ingenieria o Administracion, MBA, 10+ anos de experiencia."),
            ("Coordinador del Sistema de Gestion (SIG)",
             "MISION DEL CARGO: Planificar, implementar y mantener el Sistema de Gestion Integrado de la empresa.\nFUNCIONES: Gestionar auditorias, documentar procesos, analizar hallazgos, liderar la mejora continua.\nPERFIL: Ingeniero Industrial o afines, certificacion ISO 9001 Lead Auditor, 3+ anos SGC."),
            ("Director de Tecnologia (CTO)",
             "MISION DEL CARGO: Liderar la arquitectura tecnologica y los proyectos de desarrollo de software.\nFUNCIONES: Aprobar decisiones de arquitectura, gestionar el equipo tecnico, velar por la seguridad de sistemas.\nPERFIL: Ingeniero de Sistemas, habilidades en Cloud/DevOps/Ciberseguridad, 7+ anos."),
            ("Analista de Calidad",
             "MISION DEL CARGO: Ejecutar actividades de control de calidad en los proyectos y procesos internos.\nFUNCIONES: Realizar pruebas de software, auditorias de proceso, generar informes de calidad.\nPERFIL: Tecnologo o Profesional en areas TI, conocimiento en ISTQB, ISO 9001, 2+ anos."),
        ]
    },
]

# ============================================================
# DOCUMENTOS SEGURIDAD (ISO 27001)
# ============================================================
docs_seguridad = [
    {
        "nombre": "Politica de Seguridad de la Informacion",
        "norma": "SEGURIDAD",
        "ref": "ISO 27001:5.2",
        "secciones": [
            ("Declaracion de la Politica",
             f"La Alta Direccion de {COMPANY} reconoce que la informacion es un activo critico para la continuidad del negocio y la confianza de nuestros clientes. Por tanto, declara su compromiso con la proteccion de la confidencialidad, integridad y disponibilidad (CID) de la informacion en todos los niveles de la organizacion."),
            ("Principios Fundamentales (Triada CID)",
             "CONFIDENCIALIDAD: La informacion solo es accesible para personas autorizadas. Los datos de clientes se tratan con maxima reserva y bajo acuerdos de confidencialidad firmados.\n\nINTEGRIDAD: La informacion se mantiene exacta, completa y sin alteraciones no autorizadas. Todo cambio es documentado y trazable.\n\nDISPONIBILIDAD: Los sistemas y la informacion estan disponibles cuando los usuarios autorizados los necesitan, con RTO < 4h y RPO < 1h para sistemas criticos."),
            ("Alcance del SGSI",
             f"Esta politica aplica a todos los empleados, contratistas, proveedores y terceros que acceden a los sistemas de informacion de {COMPANY}, incluyendo:\n- Infraestructura tecnologica (servidores, redes, endpoints)\n- Aplicaciones y sistemas de gestion\n- Datos de clientes y propiedad intelectual\n- Comunicaciones electronicas"),
            ("Compromisos de la Direccion",
             "1. Designar un Responsable de Seguridad (CISO) con autoridad y recursos.\n2. Proporcionar formacion anual en ciberseguridad a todo el personal.\n3. Revisar y actualizar esta politica anualmente o ante cambios significativos.\n4. Asignar presupuesto especifico para la gestion de la ciberseguridad.\n5. Reportar y gestionar incidentes de seguridad segun el procedimiento establecido."),
            ("Aprobacion",
             f"Aprueba: {REP_LEGAL} - Gerente General\nRevisa: Director de tecnologia (CISO)\nFecha de aprobacion: {TODAY}\nVersion: 2.0 | Proxima revision: {TODAY}"),
        ]
    },
    {
        "nombre": "Analisis de Riesgos de Seguridad",
        "norma": "SEGURIDAD",
        "ref": "ISO 27001:6.1",
        "secciones": [
            ("Metodologia de Valoracion",
             "Se utiliza la ecuacion:\n\nRIESGO = PROBABILIDAD x IMPACTO\n\nEscala de valoracion: 1 (Muy Bajo) a 5 (Critico)\n\nNivel de Riesgo:\n- 1-4: Bajo (Aceptar)\n- 5-9: Medio (Mitigar)\n- 10-16: Alto (Evitar/Transferir)\n- 17-25: Critico (Accion inmediata)"),
            ("Matriz de Riesgos Principales",
             "ACTIVO: Base de datos de clientes\nAMENAZA: Acceso no autorizado / Exfiltracion\nVULNERABILIDAD: Credenciales debiles / sin MFA\nPROBABILIDAD: 3 | IMPACTO: 5 | RIESGO: 15 (ALTO)\nCONTROL: Implementar MFA, cifrado AES-256, monitoreo continuo\n\n---\nACTIVO: Codigo fuente propietario\nAMENAZA: Robo de propiedad intelectual\nVULNERABILIDAD: Control de versiones sin restriccion de acceso\nPROBABILIDAD: 2 | IMPACTO: 5 | RIESGO: 10 (ALTO)\nCONTROL: Branch protection, revision de codigo, gestion de accesos\n\n---\nACTIVO: Infraestructura Cloud (AWS/Azure)\nAMENAZA: Ransomware / Denegacion de servicio\nVULNERABILIDAD: Configuracion insegura de buckets S3\nPROBABILIDAD: 3 | IMPACTO: 4 | RIESGO: 12 (ALTO)\nCONTROL: CIS Benchmarks, backups automatizados, WAF"),
            ("Plan de Tratamiento Priorizado",
             "PRIORIDAD 1 (Criticos/Altos):\n- Implementacion de MFA para todos los accesos remotos [Responsable: CTO | Plazo: 30 dias]\n- Auditoria de accesos a repositorios de codigo [Responsable: CTO | Plazo: 15 dias]\n\nPRIORIDAD 2 (Medios):\n- Capacitacion en phishing para todo el personal [Responsable: CISO | Plazo: 60 dias]\n- Revision de configuracion de infraestructura cloud [Responsable: DevOps | Plazo: 45 dias]"),
        ]
    },
]

# ============================================================
# DOCUMENTOS AMBIENTAL (ISO 14001)
# ============================================================
docs_ambiental = [
    {
        "nombre": "Matriz de Aspectos e Impactos Ambientales",
        "norma": "AMBIENTAL",
        "ref": "ISO 14001:6.1.2",
        "secciones": [
            ("Objetivo y Alcance",
             f"Identificar y valorar los aspectos ambientales significativos generados por las actividades de {COMPANY} en sus instalaciones de {CIUDAD}, con el fin de establecer controles operacionales y objetivos de mejora ambiental."),
            ("Matriz de Aspectos Ambientales",
             "ACTIVIDAD: Uso de equipos de computo (100+ workstations)\nASPECTO: Consumo de energia electrica\nIMPACTO: Agotamiento de recursos no renovables / Emisiones CO2\nFRECUENCIA: Diaria | SEVERIDAD: Media | SIGNIFICANCIA: Alta\nCONTROL: Programa de uso eficiente de energia, equipos Energy Star\n\n---\nACTIVIDAD: Gestion de residuos de oficina\nASPECTO: Generacion de papel, carton y residuos electronicos (RAEE)\nIMPACTO: Contaminacion de suelos\nFRECUENCIA: Diaria | SEVERIDAD: Baja | SIGNIFICANCIA: Media\nCONTROL: Programa de reciclaje, convenio con gestores RAEE certificados\n\n---\nACTIVIDAD: Operacion de servidores (Data Center)\nASPECTO: Emision de calor (refrigeracion)\nIMPACTO: Consumo energetico intensivo\nFRECUENCIA: Continua | SEVERIDAD: Media | SIGNIFICANCIA: Alta\nCONTROL: Migracion progresiva a cloud computing verde (AWS Green Regions)"),
            ("Indicadores de Seguimiento",
             "- Consumo mensual de energia (kWh): Meta: reduccion del 15% anual\n- Kg de residuos reciclados vs total: Meta: > 70%\n- Huella de carbono operativa: Meta: neutralidad para 2027"),
        ]
    },
    {
        "nombre": "Objetivos y Programa Ambiental",
        "norma": "AMBIENTAL",
        "ref": "ISO 14001:6.2",
        "secciones": [
            ("Objetivo 1: Reduccion del Consumo Energetico",
             f"META: Reducir el consumo de energia electrica en {COMPANY} en un 20% para el 31/12/2025.\n\nACCIONES:\n1. Instalar sensores de movimiento en areas comunes [Responsable: Infraestructura | Fecha: Q1 2025]\n2. Configurar modo de ahorro en todos los equipos [Responsable: TI | Fecha: Inmediato]\n3. Evaluar paneles solares en la terraza del edificio [Responsable: Gerencia | Fecha: Q2 2025]\n\nINDICADOR: kWh/mes | LINEA BASE: XXXX kWh | META: YYYY kWh"),
            ("Objetivo 2: Gestion de Residuos",
             "META: Lograr una tasa de reciclaje del 75% de los residuos generados en oficina.\n\nACCIONES:\n1. Instalar puntos ecologicos en cada piso [Responsable: Infraestructura | Fecha: Q1 2025]\n2. Campana de sensibilizacion ambiental trimestral [Responsable: RRHH | Fecha: Q1-Q4 2025]\n3. Convenio con gestores certificados para RAEE [Responsable: Compras | Fecha: Q1 2025]\n\nINDICADOR: Kg reciclados / Kg totales x 100"),
            ("Objetivo 3: Huella de Carbono Neutral",
             "META: Declarar operaciones de carbon neutral para el ano 2027.\n\nACCIONES:\n1. Medir huella de carbono actual (Alcance 1, 2 y 3) [Responsable: SIG | Fecha: Q2 2025]\n2. Disenar plan de compensacion con siembra de arboles [Responsable: Gerencia | Fecha: Q3 2025]\n3. Adquirir bonos de carbono certificados para compensacion [Responsable: Finanzas | Fecha: 2026]"),
        ]
    },
]

def generar_pdf(doc_data, output_dir):
    norma = doc_data["norma"]
    pdf = DocPDF(norma=norma)
    pdf.add_page()

    # Titulo principal
    r, g, b = NORMAS_COLOR.get(norma, (10, 30, 70))
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(r, g, b)
    pdf.multi_cell(0, 8, safe(doc_data["nombre"].upper()), align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", "I", 9)
    pdf.cell(0, 6, safe(f"Referencia Normativa: {doc_data['ref']}  |  Empresa: {COMPANY}"), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    pdf.set_fill_color(240, 245, 255)
    pdf.set_font("helvetica", "", 9)
    pdf.multi_cell(0, 5, safe(f"Este documento forma parte del expediente de materia prima para la auditoria interna bajo el marco normativo {norma} de {COMPANY}. Elaborado el {TODAY}."), fill=True)
    pdf.ln(5)

    for i, (titulo, contenido) in enumerate(doc_data["secciones"], 1):
        if pdf.get_y() > pdf.h - 50:
            pdf.add_page()
        pdf.section_header(f"{i}. {titulo.upper()}")
        pdf.body(contenido)

    pdf.firma_block()

    safe_name = doc_data["nombre"].replace(" ", "_").replace("/", "-")[:40].upper()
    file_name = f"{norma}_{safe_name}.pdf"
    full_path = os.path.join(output_dir, file_name)
    pdf.output(full_path)
    return full_path


# ============================================================
# EJECUCION
# ============================================================
if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  HMO AUDITOR - GENERADOR DE DOCUMENTOS BASE")
    print(f"  Empresa: {COMPANY}")
    print(f"  Directorio: {OUT_DIR}")
    print(f"{'='*60}\n")

    todos = docs_sig + docs_calidad + docs_seguridad + docs_ambiental
    generados = []
    errores = []

    for doc in todos:
        try:
            path = generar_pdf(doc, OUT_DIR)
            generados.append(path)
            print(f"  [OK] {os.path.basename(path)}")
        except Exception as e:
            errores.append((doc["nombre"], str(e)))
            print(f"  [ERR] {doc['nombre']}: {e}")

    print(f"\n{'='*60}")
    print(f"  RESUMEN: {len(generados)} documentos generados, {len(errores)} errores.")
    if errores:
        print("\n  ERRORES:")
        for n, e in errores:
            print(f"  - {n}: {e}")
    print(f"  Ubicacion: {OUT_DIR}")
    print(f"{'='*60}\n")
