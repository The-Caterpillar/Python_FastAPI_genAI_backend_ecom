import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("PERSONA_API_KEY"))

def get_embedding(text: str):
    embedding = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
    )
    return embedding["embedding"]
