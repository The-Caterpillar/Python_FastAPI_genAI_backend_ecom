import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("PERSONA_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str):
    """
    Sends prompt to Gemini 2.0 Flash and returns text output.
    """
    model = genai.GenerativeModel("gemini-flash-latest")

    response = model.generate_content(prompt)

    # Return plain text (Gemini returns markdown sometimes)
    return response.text
