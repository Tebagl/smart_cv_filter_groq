import os
from pathlib import Path
from dotenv import load_dotenv
import requests

base_path = Path(__file__).resolve().parent
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print('❌ ERROR: No se lee la clave del .env')
    print(f'Buscando en: {env_path}')
else:
    print(f'✅ Clave detectada (empieza por: {api_key[:6]}...)')
    url = 'https://api.groq.com/openai/v1/chat/completions'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'model': 'llama-3.1-8b-instant', 'messages': [{'role': 'user', 'content': 'test'}], 'max_tokens': 5}
    try:
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            print('🚀 CONEXIÓN EXITOSA CON GROQ')
        else:
            print(f'⚠️ Error de API: {res.status_code} - {res.text}')
    except Exception as e:
        print(f'🔥 Error de red: {e}')
