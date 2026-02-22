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
        except:
            return False

    def analyze_document(self, doc_name, text_content):
        """
        Análisis semántico real bajo ISO 9001/19011.
        """
        prompt = f"""
        Eres un Auditor Senior Certificado en ISO 9001:2015 e ISO 19011:2018.
        Analiza el siguiente contenido del documento '{doc_name}' y responde en formato JSON:
        1. Coherencia (0-100)
        2. Hallazgos_Clave (Lista)
        3. Riesgos_Detectados (Lista)
        4. Resumen_Ejecutivo (Máximo 3 líneas)

        Contenido:
        {text_content[:2000]} # Limitamos por contexto local
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
