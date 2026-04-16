"""
================================================================================
SMART CV FILTER - AI ANALYZER ENGINE (GROQ CLOUD)
================================================================================
Author: Tebagl
Date: April 2026
Version: 2.0 (Cloud Migration)

Description:
Core analysis module that interfaces with Groq's LPU™ infrastructure. 
This engine processes raw CV text against job descriptions using 
Llama-3.1-8b-instant to provide objective scoring and justification.

TECHNICAL SPECIFICATIONS:
- Provider: Groq Cloud API
- Model: llama-3.1-8b-instant
- Response Format: Strict JSON (score, apto, motivo)
- Temperature: 0.0 (Deterministic output for consistency)

SECURITY & PRIVACY:
- API keys are loaded via environment variables (.env) to prevent leaks.
- No local LLM overhead: Offloads processing to remote inference.
- Data handled via encrypted HTTPS requests.

DATA FLOW:
1. Load API Key -> 2. Construct Prompt -> 3. POST Request -> 4. JSON Parse
================================================================================
"""

import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Busca el archivo .env subiendo dos niveles desde donde está analyzer.py
base_path = Path(__file__).resolve().parent.parent.parent
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

class CVAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"
        
        if not self.api_key:
            print("❌ ERROR: No se encontró GROQ_API_KEY en el archivo .env")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def analyze(self, cv_text, job_description):
        # Prompt equilibrado: Estricto con intrusos, justo con el sector
        prompt = f"""
        Actúa como un experto en selección de personal. Analiza el CV para el puesto de: {job_description}.

        MÉTODO DE EVALUACIÓN:
        1. Identifica habilidades y experiencia CLAVE para el puesto.
        2. Si el CV tiene experiencia REAL y DIRECTA en el sector, valora positivamente (Score > 70).
        3. Si el CV es de un sector totalmente ajeno (ej. programación para camarera), el score DEBE ser inferior a 15.
        4. No te inventes incompatibilidades. Si menciona el sector solicitado, puntúa según esa experiencia.

        Responde exclusivamente en formato JSON:
        {{
          "score": número del 0 al 100,
          "apto": "SI" o "NO",
          "motivo": "Explicación breve y coherente"
        }}

        TEXTO DEL CV A ANALIZAR:
        {cv_text}
        """

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Eres un reclutador que solo responde en JSON puro."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }

        try:
            response = requests.post(self.url, json=payload, headers=self.headers, timeout=20)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None