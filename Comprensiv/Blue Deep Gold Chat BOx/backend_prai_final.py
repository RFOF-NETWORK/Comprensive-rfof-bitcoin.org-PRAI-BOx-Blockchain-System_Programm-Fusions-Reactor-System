# backend_prai_final.py (Google Cloud Function)

import os
import json
import hashlib
import time
from google.auth import default
import google_generativeai as genai
# from google_search import search  # Stelle sicher, dass du eine funktionierende Bibliothek hast

# --- Konfiguration ---
PROJECT_ID = "imposing-eye-446911-f4"  # Deine Google Cloud Projekt-ID
MODEL_NAME = "gemini-pro"
QUANTUM_SALT = os.environ.get("QUANTUM_SALT", "default_quantum_salt_42") # Sichere Umgebungsvariable

# --- Initialisierung von Google Cloud Clients ---
try:
    credentials, project = default()
    genai.configure(project=PROJECT_ID, credentials=credentials)
    gemini_model = genai.GenerativeModel(MODEL_NAME)
    # Wenn du eine funktionierende Google Search Intelligence Bibliothek hast:
    # from google_search import search
    # def search_with_google_intelligence(query: str) -> str:
    #     try:
    #         search_results = search(queries=[query])
    #         if search_results and search_results['results']:
    #             return "\n".join([f"[{i+1}] {res['title']}: {res['link']}\n{res['snippet']}" for i, res in enumerate(search_results['results'][:3])])
    #         else:
    #             return "Keine relevanten Suchergebnisse gefunden."
    #     except Exception as e:
    #         print(f"Fehler bei der Google Suche: {e}")
    #         return "Fehler bei der Suche."
    search_with_google_intelligence = None # Platzhalter, falls keine funktionierende Bibliothek vorhanden
except Exception as e:
    print(f"Fehler bei der Initialisierung der Google Cloud Clients: {e}")

def generate_quantum_id(user_message: str, timestamp: float) -> str:
    """Simuliert eine robuste, 'quantum-inspirierte' ID."""
    combined = f"{user_message}-{timestamp}-{QUANTUM_SALT}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]

def prai_filter(gemini_response: str, user_message: str) -> str:
    """Erweiterte ethische Filterung und Anpassung der Gemini-Antwort."""
    filtered_response = gemini_response.replace("schlecht", "nicht gut").replace("gefährlich", "bedenklich")
    # Hier würden deine komplexeren ethischen Regeln und potenziell der Aufruf von ML-Modellen zur Filterung stehen

    if search_with_google_intelligence:
        search_results = search_with_google_intelligence(user_message)
        if search_results:
            filtered_response += f"\n\nInformationen aus dem Web:\n{search_results}"

    return f"PRAI (Quantum-verifiziert: {generate_quantum_id(filtered_response, time.time())[:8]}): {filtered_response}"

def interact_with_gemini(user_message: str) -> str:
    """Interagiert mit der Gemini API."""
    try:
        response = gemini_model.generate_content(user_message)
        return response.text
    except Exception as e:
        print(f"Fehler bei der Interaktion mit Gemini: {e}")
        return "Fehler bei der Antwortgenerierung."

def main(request):
    """HTTP Cloud Function zur Verarbeitung von Nachrichten."""
    request_json = request.get_json(silent=True)
    if request_json and 'message' in request_json:
        user_message = request_json['message']
        timestamp = time.time()
        quantum_id = generate_quantum_id(user_message, timestamp)

        gemini_response = interact_with_gemini(user_message)
        prai_response = prai_filter(gemini_response, user_message)

        return json.dumps({'reply': prai_response})
    else:
        return '{"error": "Nachricht fehlt im Anfragekörper"}', 400
