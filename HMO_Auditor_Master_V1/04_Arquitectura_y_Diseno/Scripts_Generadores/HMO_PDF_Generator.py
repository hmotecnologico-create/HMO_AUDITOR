from fpdf import FPDF
import datetime
import os

class HMO_PDF(FPDF):
    def header(self):
        # Logo placeholder or real logo
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'HMO AUDITOR ELITE - SISTEMA DE GESTIÓN DE CALIDAD', ln=True, align='C')
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 5, f'Generado: {datetime.date.today()} | Grado: Institucional', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} | Confidencial HMO Auditor', align='C')

def generate_audit_program_pdf(company_name, output_path, kb=None, identity_data=None):
    pdf = HMO_PDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "PROGRAMA DE AUDITORÍA INTERNA", ln=True, align='C')
    pdf.ln(10)

    # Datos Generales
    pdf.set_font("helvetica", "B", 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, "1. DATOS GENERALES", ln=True, fill=True)
    pdf.set_font("helvetica", "", 10)
    
    data = [
        ("Entidad", company_name),
        ("Auditor", identity_data.get("auditor", "N/A")),
        ("NIT", identity_data.get("nit", "N/A")),
        ("Sector", identity_data.get("sector", "N/A")),
    ]
    
    for key, val in data:
        pdf.cell(50, 8, f"{key}:", border=1)
        pdf.cell(0, 8, f" {val}", border=1, ln=True)
    
    pdf.ln(10)
    
    # Contenido Semántico
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "2. ANÁLISIS DE COHERENCIA NORMATIVA (Materia Prima)", ln=True, fill=True)
    pdf.set_font("helvetica", "", 10)
    
    if kb:
        for doc, content in kb.items():
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(0, 7, f"Documento: {doc}", ln=True)
            pdf.set_font("helvetica", "", 9)
            pdf.multi_cell(0, 5, f"Resumen Semántico: {str(content)[:300]}...")
            pdf.ln(2)
    
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "3. CRITERIOS DE CERTIFICACIÓN", ln=True, fill=True)
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 6, "Este documento certifica que la entidad ha superado la fase de ingesta documental, cumpliendo con los estándares de integridad y veracidad exigidos por el marco normativo ISO 9001:2015.")

    full_path = os.path.join(output_path, f"GA_CERT_{company_name[:5].upper()}.pdf")
    pdf.output(full_path)
    return full_path

if __name__ == "__main__":
    # Test session
    generate_audit_program_pdf("Innovatech", ".", kb={"Misión": "Ser la mejor"}, identity_data={"auditor": "Juan Gabriel"})
