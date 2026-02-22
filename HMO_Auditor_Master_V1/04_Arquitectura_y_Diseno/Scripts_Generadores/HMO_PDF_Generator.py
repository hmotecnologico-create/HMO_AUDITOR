from fpdf import FPDF
from fpdf.enums import XPos, YPos
import datetime
import os

class HMO_PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'HMO AUDITOR ELITE - SISTEMA DE GESTION DE CALIDAD', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 5, f'Codigo: GAD-PROG-01 | Version: 03 | Fecha: {datetime.date.today()}', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()} | Confidencial HMO Auditor - ISO 19011 Compliance', align='C')

def generate_audit_program_pdf(company_name, output_path, kb=None, identity_data=None):
    pdf = HMO_PDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "PROGRAMA DE AUDITORIA INTERNA", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    # 1. Datos Generales
    pdf.set_font("helvetica", "B", 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, "1. DATOS GENERALES Y ALCANCE", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "", 10)
    
    data = [
        ("Empresa Auditada", company_name),
        ("Auditor Lider", identity_data.get("auditor", "N/A")),
        ("NIT / ID Legal", identity_data.get("nit", "N/A")),
        ("Sector Economico", identity_data.get("sector", "N/A")),
        ("Norma de Referencia", "ISO 9001:2015 / ISO 19011:2018"),
    ]
    
    for key, val in data:
        pdf.cell(60, 8, f" {key}:", border=1)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 8, f" {val}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", "", 10)
    
    pdf.ln(10)
    
    # 2. Analisis Cognitivo de Evidencias
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "2. ANALISIS COGNITIVO DE EVIDENCIAS (ISO 19011:6.4)", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    if kb:
        for doc, data in kb.items():
            pdf.set_font("helvetica", "B", 10)
            status = f" [Coherencia: {data.get('coherencia')}%]" if isinstance(data, dict) else ""
            pdf.cell(0, 8, f">> {doc}{status}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("helvetica", "", 9)
            
            summary = data.get('resumen', "Verificado") if isinstance(data, dict) else "Analizado por motor estandar."
            pdf.multi_cell(0, 5, f"Resumen Semantico: {summary}")
            
            if isinstance(data, dict) and data.get('hallazgos'):
                pdf.set_font("helvetica", "I", 8)
                pdf.cell(0, 5, "   Hallazgos Detectados:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                for h in data.get('hallazgos'):
                    pdf.cell(0, 5, f"   - {h}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(3)
    
    pdf.ln(5)
    
    # 3. Conclusiones y Firmas
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "3. CONCLUSIONES Y VALIDACION LEGAL", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 6, "Tras el analisis multidimensional de la materia prima inyectada, se concluye que la organizacion cumple con los requisitos de planificacion y preparacion establecidos en la norma ISO 19011:2018.")
    
    pdf.ln(20)
    # Firmas
    pdf.line(20, pdf.get_y(), 90, pdf.get_y())
    pdf.line(120, pdf.get_y(), 190, pdf.get_y())
    pdf.set_font("helvetica", "B", 8)
    pdf.text(35, pdf.get_y() + 5, f"FIRMA AUDITOR: {identity_data.get('auditor')}")
    pdf.text(130, pdf.get_y() + 5, f"FIRMA REPRESENTANTE LEGAL")


def generate_preparation_guide_pdf(company_name, output_path, doc_requirements, norma="ISO 9001:2015"):
    """
    Genera una guia de preparacion para que el humano sepa que y como crear los documentos.
    """
    pdf = HMO_PDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "GUIA DE PREPARACION DOCUMENTAL", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 8, f"Norma de Referencia: {norma}", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    pdf.set_font("helvetica", "", 10)
    intro = (f"Esta guia ha sido generada para {company_name} con el fin de facilitar la recoleccion "
             "de evidencias necesarias para la fase de Revision de Informacion Documentada (ISO 19011:6.3.1).")
    pdf.multi_cell(0, 5, intro)
    pdf.ln(10)

    for doc_item in doc_requirements:
        pdf.set_font("helvetica", "B", 12)
        pdf.set_fill_color(220, 230, 241)
        pdf.cell(0, 10, doc_item['doc'].upper(), fill=True, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 7, "JUSTIFICACION NORMATIVA:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", "", 9)
        pdf.multi_cell(0, 5, doc_item.get('justificacion', 'Requisito estandar de auditoria.'))
        
        pdf.ln(2)
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(31, 78, 120)
        pdf.cell(0, 7, "COMO CREAR ESTE DOCUMENTO (EL HUMANO):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("helvetica", "I", 9)
        pdf.multi_cell(0, 5, doc_item.get('instrucciones', 'Consulte el manual de calidad o el archivo maestro de la entidad.'))
        pdf.ln(5)

    if not os.path.exists(output_path): os.makedirs(output_path)
    full_path = os.path.join(output_path, f"GUIA_PREPARACION_{company_name[:5].upper()}.pdf")
    pdf.output(full_path)
    return full_path

def generate_document_template_pdf(doc_name, instructions, output_path, company="LA EMPRESA", norma="SIG", ejemplo_base=""):
    """
    Genera una plantilla enriquecida con 5 secciones profesionales para el documento indicado.
    """
    # Limpiar caracteres especiales para FPDF
    def safe(text):
        return (text.encode('latin-1', 'replace').decode('latin-1') 
                if isinstance(text, str) else str(text))

    pdf = HMO_PDF()
    pdf.add_page()

    # SECCIÓN 1: PORTADA INSTITUCIONAL
    pdf.set_fill_color(10, 30, 70)
    pdf.rect(0, 25, 210, 30, 'F')
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(30)
    pdf.cell(0, 10, safe(f"PLANTILLA: {doc_name.upper()}"), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "I", 9)
    pdf.cell(0, 8, safe(f"Empresa: {company}  |  Norma: {norma}  |  Fecha: {datetime.date.today()}"), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(15)

    # SECCIÓN 2: PROPÓSITO
    pdf.set_font("helvetica", "B", 11)
    pdf.set_fill_color(220, 230, 245)
    pdf.cell(0, 8, "1. PROPOSITO DEL DOCUMENTO", fill=True, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "", 10)
    proposito = safe(
        f"Este documento es la evidencia objetiva del requerimiento '{doc_name}' "
        f"en el Sistema de Gestion de {company}. Requerido por la norma: {norma}."
    )
    pdf.multi_cell(0, 6, proposito)
    pdf.ln(5)

    # SECCIÓN 3: PASOS DE ELABORACIÓN
    pdf.set_font("helvetica", "B", 11)
    pdf.set_fill_color(220, 245, 230)
    pdf.cell(0, 8, "2. COMO SE CREA ESTE DOCUMENTO (PASO A PASO)", fill=True, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "", 10)
    clean_inst = instructions.replace("EJEMPLO:", "\n---\n")
    for line in clean_inst.split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith("---"):
            pdf.multi_cell(0, 6, safe(f"  {stripped}"))
    pdf.ln(5)

    # SECCIÓN 4: EJEMPLO CONTEXTUALIZADO
    if ejemplo_base and ejemplo_base != "No hay ejemplo disponible para este documento.":
        pdf.set_font("helvetica", "B", 11)
        pdf.set_fill_color(245, 235, 220)
        pdf.cell(0, 8, safe(f"3. EJEMPLO REFERENCIAL - {company.upper()}"), fill=True, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("courier", "", 9)
        pdf.set_fill_color(250, 248, 240)
        pdf.multi_cell(0, 6, safe(ejemplo_base), fill=True)
        pdf.ln(5)

    # SECCIÓN 5: ESPACIO DE DESARROLLO
    pdf.set_font("helvetica", "B", 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, "4. CONTENIDO OFICIAL (COMPLETAR POR EL RESPONSABLE)", fill=True, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "I", 9)
    pdf.set_text_color(150, 150, 150)
    for _ in range(16):
        y_pos = pdf.get_y() + 8
        pdf.line(pdf.l_margin, y_pos, pdf.w - pdf.r_margin, y_pos)
        pdf.ln(9)

    # FIRMAS
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    y_firma = pdf.get_y()
    pdf.line(pdf.l_margin, y_firma, 80, y_firma)
    pdf.line(130, y_firma, pdf.w - pdf.r_margin, y_firma)
    pdf.ln(3)
    pdf.set_font("helvetica", "B", 9)
    pdf.cell(90, 5, "ELABORADO POR:", new_x=XPos.RIGHT, new_y=YPos.LAST)
    pdf.cell(0, 5, "VALIDADO POR (AUDITOR):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    if not os.path.exists(output_path): os.makedirs(output_path)
    safe_name = doc_name[:15].replace(' ', '_').replace('/', '-').upper()
    file_name = f"PLANTILLA_{safe_name}.pdf"
    full_path = os.path.join(output_path, file_name)
    pdf.output(full_path)
    return full_path



if __name__ == "__main__":
    # Test session
    generate_audit_program_pdf("Innovatech", ".", kb={"Misión": "Ser la mejor"}, identity_data={"auditor": "Juan Gabriel"})
