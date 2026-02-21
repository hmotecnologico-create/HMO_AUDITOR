import openpyxl
from openpyxl.styles import Font, Border, Side, Alignment, PatternFill
import os
import datetime

def create_legal_checklist(company_name, output_path, logo_path=None):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "AUD-LIST-02 Checklist Legal"
    
    # 1. ENCABEZADO DE IDENTIFICACIÓN
    ws.merge_cells('A1:B3')
    if logo_path and os.path.exists(logo_path):
        img = openpyxl.drawing.image.Image(logo_path)
        img.width = 100
        img.height = 100
        ws.add_image(img, 'A1')
    else:
        ws['A1'] = "LOGO INSTITUCIONAL"
    
    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    
    ws.merge_cells('C1:E2')
    ws['C1'] = f"SISTEMA DE GESTIÓN DE CALIDAD\n{company_name}"
    ws['C1'].font = Font(bold=True, size=14)
    ws['C1'].alignment = center_align
    
    ws.merge_cells('C3:E3')
    ws['C3'] = "LISTA DE VERIFICACIÓN DE AUDITORÍA"
    ws['C3'].font = Font(bold=True)
    ws['C3'].alignment = center_align
    
    ws['F1'] = "Código:"
    ws['G1'] = "AUD-LIST-02"
    ws['F2'] = "Versión:"
    ws['G2'] = "02"
    ws['F3'] = "Fecha:"
    ws['G3'] = str(datetime.date.today())
    
    # 2. DATOS GENERALES
    ws.append([])
    ws.append(["DATOS GENERALES DE LA AUDITORÍA"])
    ws.merge_cells(f'A5:G5')
    ws['A5'].font = Font(bold=True)
    
    ws.append(["Tipo de Auditoría:", "Interna de Calidad", "", "Proceso Auditado:", "Gestión Operativa"])
    ws.append(["Área Auditada:", "Producción / Admin", "", "Ubicación:", "Sede Central"])
    ws.append(["Auditor Líder:", "Juan Pérez", "", "Fecha Inicio:", str(datetime.date.today())])
    
    # 7. LISTA DE VERIFICACIÓN (Columnas Obligatorias)
    ws.append([])
    headers = ["Ítem", "Requisito Normativo", "Cumple", "No cumple", "Observación", "Evidencia", "Tipo de Hallazgo"]
    ws.append(headers)
    
    header_row = 10
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = white_font
        cell.alignment = center_align
        cell.border = border
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_num)].width = 20

    # Datos de ejemplo (Innovatech)
    data = [
        ["1", "ISO 9001:2015 Cl. 4.1 - Comprensión de la organización", "X", "", "Se evidencia análisis DOFA.", "Acta_Estrategica_001.pdf", "Cumple"],
        ["2", "ISO 9001:2015 Cl. 5.2 - Política de Calidad", "X", "", "Política firmada y comunicada.", "Manual_Calidad_V1.pdf", "Cumple"],
        ["3", "ISO 9001:2015 Cl. 7.5 - Información documentada", "", "X", "Faltan firmas en el Acta de Inicio.", "Acta_Inicio.docx", "No Conformidad"],
    ]
    
    for row_data in data:
        ws.append(row_data)
        for cell in ws[ws.max_row]:
            cell.border = border
            cell.alignment = Alignment(vertical="center", wrap_text=True)

    # 11. FIRMAS (Elemento CRÍTICO)
    ws.append([])
    ws.append([])
    start_row = ws.max_row
    ws.merge_cells(f'A{start_row}:C{start_row}')
    ws[f'A{start_row}'] = "RESPONSABILIDAD LEGAL Y FIRMAS"
    ws[f'A{start_row}'].font = Font(bold=True)
    
    ws.append([])
    sig_row = ws.max_row
    ws[f'A{sig_row}'] = "Firma del Auditor:"
    ws[f'A{sig_row+2}'] = "__________________________"
    ws[f'A{sig_row+3}'] = "Nombre: Juan Pérez"
    
    ws[f'E{sig_row}'] = "Firma del Auditado:"
    ws[f'E{sig_row+2}'] = "__________________________"
    ws[f'E{sig_row+3}'] = "Nombre: Representante Legal"

    # 12. CONTROL DE VERSIONES
    ws.append([])
    ws.append(["CONTROL DE VERSIONES"])
    ver_row = ws.max_row
    ws.append(["Versión", "Fecha", "Descripción", "Responsable"])
    ws.append(["02", str(datetime.date.today()), "Actualización para cumplimiento legal ISO 19011", "HMO Auditor"])

    # Guardar
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    file_name = "GAD_LIST_02_Checklist_Auditoria_LEGAL.xlsx"
    full_path = os.path.join(output_path, file_name)
    wb.save(full_path)
    print(f"Excel LEGAL generado en: {full_path}")

if __name__ == "__main__":
    company = "Innovatech Solutions SAS"
    path = "d:\\HMO\\SENA\\Auditor_Formatos\\HMO_Auditor_Master_V1\\02_Formatos_del_Sistema"
    create_legal_checklist(company, path)
