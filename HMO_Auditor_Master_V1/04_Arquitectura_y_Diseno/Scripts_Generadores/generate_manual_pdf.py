from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import os

def generate_manual_pdf(output_path):
    doc = SimpleDocTemplate(os.path.join(output_path, "MAN_AUD_001_Manual_Procedimientos_HMO.pdf"), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Manual de Auditoría y Procedimientos Técnicos", styles['Title']))
    story.append(Paragraph("Sistema HMO Auditor - Versión 1.0", styles['Normal']))
    story.append(Spacer(1, 12))

    # Content
    content = [
        ("1. Propósito", "Establecer las directrices para la planificación y ejecución de auditorías internas asistidas por IA local."),
        ("2. El Proceso OCR", "Digitalización de documentos con validación humana obligatoria."),
        ("3. Blindaje Documental", "Uso de protección estructural en archivos Word y Excel para asegurar la integridad de la certificación.")
    ]

    for title, text in content:
        story.append(Paragraph(title, styles['Heading2']))
        story.append(Paragraph(text, styles['Normal']))
        story.append(Spacer(1, 12))

    # Footer/Table
    story.append(Spacer(1, 24))
    story.append(Paragraph("Control de Versiones", styles['Heading3']))
    data = [['Versión', 'Fecha', 'Responsable'], ['1.0', '21/02/2026', 'HMO AI Specialist']]
    t = Table(data)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    story.append(t)

    doc.build(story)
    print(f"Manual PDF generado.")

if __name__ == "__main__":
    output_dir = r"d:\HMO\SENA\Auditor_Formatos\Formatos_Profesionales_HMO"
    generate_manual_pdf(output_dir)
