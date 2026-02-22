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
