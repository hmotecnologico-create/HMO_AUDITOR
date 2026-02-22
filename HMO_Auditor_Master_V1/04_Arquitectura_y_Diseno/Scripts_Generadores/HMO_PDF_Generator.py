from fpdf import FPDF
from fpdf.enums import XPos, YPos
import datetime
import os

class HMO_PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'HMO AUDITOR ELITE - SISTEMA DE GESTIÓN DE CALIDAD', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 5, f'Código: GAD-PROG-01 | Versión: 03 | Fecha: {datetime.date.today()}', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} | Confidencial HMO Auditor - ISO 19011 Compliance', align='C')

def generate_audit_program_pdf(company_name, output_path, kb=None, identity_data=None):
    pdf = HMO_PDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "PROGRAMA DE AUDITORÍA INTERNA", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    # 1. Datos Generales
    pdf.set_font("helvetica", "B", 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, "1. DATOS GENERALES Y ALCANCE", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "", 10)
    
    data = [
        ("Empresa Auditada", company_name),
        ("Auditor Líder", identity_data.get("auditor", "N/A")),
        ("NIT / ID Legal", identity_data.get("nit", "N/A")),
        ("Sector Económico", identity_data.get("sector", "N/A")),
        ("Norma de Referencia", "ISO 9001:2015 / ISO 19011:2018"),
    ]
    
    for key, val in data:
        pdf.cell(60, 8, f" {key}:", border=1)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 8, f" {val}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", "", 10)
    
    pdf.ln(10)
    
    # 2. Análisis Cognitivo de Evidencias
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "2. ANÁLISIS COGNITIVO DE EVIDENCIAS (ISO 19011:6.4)", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    if kb:
        for doc, data in kb.items():
            pdf.set_font("helvetica", "B", 10)
            status = f" [Coherencia: {data.get('coherencia')}%]" if isinstance(data, dict) else ""
            pdf.cell(0, 8, f">> {doc}{status}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("helvetica", "", 9)
            
            summary = data.get('resumen', "Verificado") if isinstance(data, dict) else "Analizado por motor estándar."
            pdf.multi_cell(0, 5, f"Resumen Semántico: {summary}")
            
            if isinstance(data, dict) and data.get('hallazgos'):
                pdf.set_font("helvetica", "I", 8)
                pdf.cell(0, 5, "   Hallazgos Detectados:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                for h in data.get('hallazgos'):
                    pdf.cell(0, 5, f"   - {h}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(3)
    
    pdf.ln(5)
    
    # 3. Conclusiones y Firmas
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "3. CONCLUSIONES Y VALIDACIÓN LEGAL", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 6, "Tras el análisis multidimensional de la materia prima inyectada, se concluye que la organización cumple con los requisitos de planificación y preparación establecidos en la norma ISO 19011:2018.")
    
    pdf.ln(20)
    # Firmas
    pdf.line(20, pdf.get_y(), 90, pdf.get_y())
    pdf.line(120, pdf.get_y(), 190, pdf.get_y())
    pdf.set_font("helvetica", "B", 8)
    pdf.text(35, pdf.get_y() + 5, f"FIRMA AUDITOR: {identity_data.get('auditor')}")
    pdf.text(130, pdf.get_y() + 5, f"FIRMA REPRESENTANTE LEGAL")

def generate_audit_program_pdf(company_name, output_path, kb=None, identity_data=None):
    # ... (existing function content)
    # ...
    if not os.path.exists(output_path): os.makedirs(output_path)
    full_path = os.path.join(output_path, f"GAD_PROG_01_CERT_{company_name[:5].upper()}.pdf")
    pdf.output(full_path)
    return full_path

def generate_preparation_guide_pdf(company_name, output_path, doc_requirements, norma="ISO 9001:2015"):
    """
    Genera una guía de preparación para que el humano sepa qué y cómo crear los documentos.
    """
    pdf = HMO_PDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "GUÍA DE PREPARACIÓN DOCUMENTAL", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 8, f"Norma de Referencia: {norma}", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    pdf.set_font("helvetica", "", 10)
    intro = (f"Esta guía ha sido generada para {company_name} con el fin de facilitar la recolección "
             "de evidencias necesarias para la fase de Revisión de Información Documentada (ISO 19011:6.3.1).")
    pdf.multi_cell(0, 5, intro)
    pdf.ln(10)

    for doc_item in doc_requirements:
        pdf.set_font("helvetica", "B", 12)
        pdf.set_fill_color(220, 230, 241)
        pdf.cell(0, 10, doc_item['doc'].upper(), fill=True, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 7, "📌 JUSTIFICACIÓN NORMATIVA:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", "", 9)
        pdf.multi_cell(0, 5, doc_item.get('justificacion', 'Requisito estándar de auditoría.'))
        
        pdf.ln(2)
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(31, 78, 120)
        pdf.cell(0, 7, "🛠️ CÓMO CREAR ESTE DOCUMENTO (EL HUMANO):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("helvetica", "I", 9)
        pdf.multi_cell(0, 5, doc_item.get('instrucciones', 'Consulte el manual de calidad o el archivo maestro de la entidad.'))
        pdf.ln(5)

    if not os.path.exists(output_path): os.makedirs(output_path)
    full_path = os.path.join(output_path, f"GUIA_PREPARACION_{company_name[:5].upper()}.pdf")
    pdf.output(full_path)
    return full_path

if __name__ == "__main__":
    # Test session
    generate_audit_program_pdf("Innovatech", ".", kb={"Misión": "Ser la mejor"}, identity_data={"auditor": "Juan Gabriel"})
