import ollama
import os
from dotenv import load_dotenv

load_dotenv()
# Tokenul tău de autentificare
auth_token = os.getenv("AUTH_TOKEN")
if not auth_token:
    raise ValueError("Lipsește AUTH_TOKEN din fișierul .env!")
# Inițializarea clientului Ollama cu autentificare
client = ollama.Client(
    host='https://chat.readerbench.com/ollama',
    headers={"Authorization": f"Bearer {auth_token}"}
)
# Promptul pe care dorești să îl trimiți modelului
cerinta = 'Ce zi este astazi?'

# Generarea răspunsului
response = client.generate(
    model='gemma3:27b',
    prompt=cerinta
)

# Afișarea răspunsului generat
print(response)