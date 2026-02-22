import requests
import json

class HMO_AI_Engine:
    def __init__(self, model="llama3:8b", url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = url

    def test_connection(self):
        try:
            response = requests.post(self.url, json={"model": self.model, "prompt": "test", "stream": False}, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def analyze_document(self, doc_name, text_content, target_norm="ISO 9001:2015"):
        """
        Análisis semántico dual: ISO 19011 (Metodología) + Norma Específica (Criterio).
        """
        prompt = f"""
        Eres un Auditor Senior Certificado. Utiliza la ISO 19011:2018 como METODOLOGÍA de auditoría 
        y la norma '{target_norm}' como CRITERIO de evaluación.
        
        Analiza el contenido del documento '{doc_name}' y responde estrictamente en JSON:
        1. Coherencia (0-100) - Que tanto cumple el documento con los requisitos integrales de: {target_norm}.
        2. Hallazgos_Clave (Lista) - Hallazgos basados en evidencias objetivas (ISO 19011:6.4.7).
        3. Riesgos_Detectados (Lista) - Riesgos asociados segun los marcos: {target_norm}.
        4. Resumen_Ejecutivo (Maximo 3 lineas) - Conclusion del auditor sobre la madurez del documento respecto al SIG (Sistema de Gestion Integrado).

        Contenido del Documento:
        {text_content[:2500]} 
        """
        
        try:
            response = requests.post(self.url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            })
            if response.status_code == 200:
                return json.loads(response.json()['response'])
            return {"error": "Fallo en comunicación con Llama3"}
        except Exception as e:
            return {"error": f"Error de motor: {str(e)}"}

    def analyze_risk_matrix(self, table_data):
        """
        Entendimiento estructural de matrices de riesgo (ISO 31000).
        Recibe un DataFrame o texto estructurado.
        """
        prompt = f"""
        Analiza esta MATRIZ DE RIESGOS estructuralmente.
        Evalúa:
        1. Identificación del Riesgo (¿Es claro?)
        2. Proporcionalidad del Control (¿Mitiga la causa?)
        3. Calificación de Riesgo Residual.
        Responde en JSON con: 'Coherencia' (0-100), 'Hallazgos_Clave' (Lista), 'Resumen_Ejecutivo' (String).

        Datos Estructurados:
        {table_data}
        """
        
        try:
            response = requests.post(self.url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            })
            if response.status_code == 200:
                return json.loads(response.json()['response'])
            return {"error": "Fallo en motor de Riesgos"}
        except Exception as e:
            return {"error": f"Error estructural: {str(e)}"}
    def calculate_corporate_health_score(self, session_state):
        """
        Calcula el HMO Corporate Health Score (CHS) basado en el Plan Elite V15.0.
        Ponderación: 
        - 60% Documentos Vitales
        - 30% Coherencia/Calidad (OCR/IA)
        - 10% Integridad de Perfil (Fase A/B)
        """
        # 1. Integridad de Perfil (10%)
        # Phase A: Auditor, Rep Legal, ID (3 fields)
        # Phase B: Tamaño, Personal, Dirección (3 fields)
        fields_a = [session_state.get('auditor_name'), session_state.get('rep_legal'), session_state.get('rep_id')]
        fields_b = [session_state.get('empresa_tamanio'), session_state.get('empresa_personal'), session_state.get('empresa_direccion')]
        integrity_score = (sum(1 for f in fields_a if f) + sum(1 for f in fields_b if f)) / 6 * 10
        
        # 2. Documentos Vitales (60%)
        # Definimos los pilares vitales para el score (Blindaje SGC V18/19)
        pilares = [
            "Camara de Comercio (Existencia Legal)",
            "RUT (Registro Unico Tributario)",
            "Mision y Vision Corporativa",
            "Mapa de Procesos",
            "Matriz de Riesgos y Oportunidades (SGC)",
            "Matriz de Comunicaciones (SGC)",
            "Plan de Capacitación y Toma de Conciencia",
            "Informe de Auditoría Interna (Ciclo Previo)",
            "Acta de Revisión por la Dirección"
        ]
        expediente = session_state.get('expediente', {})
        vital_count = sum(1 for p in pilares if p in expediente)
        vital_score = (vital_count / len(pilares)) * 60

        # 3. Coherencia IA (30%)
        # Promedio de coherencia de los documentos cargados
        coherencias = [data.get('coherencia', 0) for doc, data in expediente.items() if isinstance(data, dict)]
        if not coherencias:
            ia_score = 0
        else:
            ia_score = (sum(coherencias) / len(coherencias)) * 0.3 # 30% de la coherencia media

        total_score = integrity_score + vital_score + ia_score
        total_score = min(100, max(0, total_score))

        # Clasificación Elite
        if total_score >= 86:
            level = "PLATINUM (Excelencia)"
            color = "#E5E4E2" # Platinum
        elif total_score >= 61:
            level = "GOLD (Cumplimiento Alto)"
            color = "#FFD700" # Gold
        elif total_score >= 41:
            level = "SILVER (En Proceso)"
            color = "#C0C0C0" # Silver
        else:
            level = "BRONZE (Riesgo Crítico)"
            color = "#CD7F32" # Bronze

        return {
            "score": round(total_score, 1),
            "level": level,
            "color": color,
            "breakdown": {
                "perfil": round(integrity_score, 1),
                "vitales": round(vital_score, 1),
                "ia": round(ia_score, 1)
            }
        }

    def generate_draft_text(self, doc_name, company_name, industry, objects, extra_ctx=""):
        """
        Genera una propuesta de texto (materia prima) para un documento específico.
        """
        prompt = f"""
        Eres un Consultor Experto en Sistemas de Gestión de Calidad (SGC).
        Genera una propuesta formal y profesional para el documento: '{doc_name}'.
        
        Empresa: {company_name}
        Sector: {industry}
        Objeto Social: {objects}
        Contexto Adicional: {extra_ctx}
        
        El tono debe ser corporativo, alineado con ISO 9001:2015. 
        Si el documento es 'Mision', redacta una misión de 3 a 5 líneas.
        Si es 'Vision', proyecta a 5 años.
        Si es una 'Politica', define compromisos claros.
        
        Responde SOLO con el texto del borrador, sin introducciones ni comentarios.
        """
        try:
            response = requests.post(self.url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                return response.json()['response'].strip()
            return f"Propuesta preliminar para {doc_name} en {company_name}. (Fallo conexión IA)"
        except Exception:
            return f"Contenido borrador para {doc_name}. Por favor redactar según política de {company_name}."

    def suggest_corrective_action(self, finding, target_norm="ISO 9001:2015"):
        """
        Sugiere una acción correctiva profesional basada en un hallazgo de NC.
        """
        prompt = f"""
        Eres un Consultor Senior en Calidad. Se ha detectado la siguiente NO CONFORMIDAD:
        Hallazgo: "{finding}"
        Norma de Referencia: {target_norm}
        
        Propón una ACCIÓN CORRECTIVA concreta siguiendo el ciclo PHVA (Planear, Hacer, Verificar, Actuar).
        La propuesta debe ser accionable, profesional y enfocada en eliminar la causa raíz.
        Responde SOLO con el texto de la propuesta, sin introducciones.
        """
        try:
            response = requests.post(self.url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                return response.json()['response'].strip()
            return f"Implementar plan de mejora inmediata para: {finding}."
        except Exception:
            return f"Revisar proceso asociado al hallazgo: {finding}."
