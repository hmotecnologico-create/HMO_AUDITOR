from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import os

def generate_roadmap_pdf(output_path):
    doc = SimpleDocTemplate(os.path.join(output_path, "ROTA_CERT_001_Ruta_Certificacion_HMO.pdf"), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Ruta a la Certificación: Guía Paso a Paso", styles['Title']))
    story.append(Paragraph("Sistema HMO Auditor - Metodología Ágil", styles['Normal']))
    story.append(Spacer(1, 12))

    # Phases
    phases = [
        ("Fase 1: Cimentación (Mes 1)", "Reunión directiva, definición estratégica y mapa de procesos."),
        ("Fase 2: Documentación e Ingesta (Mes 2-3)", "Digitalización OCR y validación humana de políticas internas."),
        ("Fase 3: Auditorías Internas (Mes 4-5)", "Uso de formatos protegidos y cierre de hallazgos asistido por IA."),
        ("Fase 4: Certificación (Mes 6)", "Auditoría de certificación con entes externos.")
    ]

    for title, desc in phases:
        story.append(Paragraph(title, styles['Heading2']))
        story.append(Paragraph(desc, styles['Normal']))
        story.append(Spacer(1, 12))

    # Control Bot info
    story.append(Spacer(1, 24))
    story.append(Paragraph("Asistente de Ayuda AI", styles['Heading3']))
    story.append(Paragraph("Si en algún momento el OCR omite información, el aplicativo permite el ingreso manual de datos para garantizar la integridad del sistema.", styles['Italic']))

    doc.build(story)
    print(f"Ruta PDF generada.")

if __name__ == "__main__":
    output_dir = r"d:\HMO\SENA\Auditor_Formatos\Formatos_Profesionales_HMO"
    generate_roadmap_pdf(output_dir)
