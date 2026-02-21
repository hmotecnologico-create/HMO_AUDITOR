# Guía de Inicio Rápido: HMO Auditor V1.0

Bienvenido al ecosistema profesional de **HMO Auditor**. Siga estos pasos para ejecutar el prototipo y generar la documentación legal blindada.

## 1. Instalación de Requisitos (Una sola vez)
Abra una terminal en el directorio raíz del proyecto y ejecute:
```powershell
pip install streamlit pandas matplotlib plotly openpyxl python-docx
```

## 2. Ejecución del Dashboard Profesional
Para ver el funcionamiento del aplicativo, el mapa de nodos y la interfaz de ingesta:
```powershell
streamlit run HMO_Auditor_Master_V1\04_Arquitectura_y_Diseno\Scripts_Generadores\HMO_Dashboard_Prototype.py
```
*El sistema se abrirá en su navegador predeterminado. Puede elegir el **Modo Simulación** para ver los datos de Innovatech.*

## 3. Generación de Formatos Legales (Manual)
Si desea generar los archivos Word y Excel blindados manualmente sin usar el Dashboard:
- **Word (Programa de Auditoría)**: 
  `python HMO_Auditor_Master_V1\04_Arquitectura_y_Diseno\Scripts_Generadores\HMO_Auditor_Master_V2_Generator.py`
- **Excel (Checklist de Verificación)**: 
  `python HMO_Auditor_Master_V1\04_Arquitectura_y_Diseno\Scripts_Generadores\HMO_Checklist_Legal_Generator.py`

## 4. Estructura de Documentación
- **Normativa y Justificación**: Localizada en `HMO_Auditor_Master_V1\01_Normativa_y_Metodologia\`.
- **Manuales**: Localizados en `HMO_Auditor_Master_V1\05_Manuales_y_Documentacion\`.
- **Ingeniería de Software**: Localizada en `HMO_Auditor_Master_V1\04_Arquitectura_y_Diseno\`.

---

### HMO Auditor: "Calidad que se nota, legalidad que se firma." 🛡️
Este paquete contiene todo el blindaje necesario para superar cualquier auditoría externa bajo la norma ISO 19011.
