# File: parser.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def parse_user_request(text_input: str):
    # --- UPDATED: Using a model specifically from your list ---
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    Extract details from: "{text_input}".
    Guess GitHub username from email if missing.
    RETURN RAW JSON ONLY. NO MARKDOWN.
    Keys: candidate_email, github_username, role
    """
    
    try:
        result = model.generate_content(prompt)
        # Clean up any formatting Gemini might add
        clean_text = result.text.replace("```json", "").replace("```", "").strip()
        return clean_text
    except Exception as e:
        # Fallback for debugging
        return json.dumps({"error": str(e)})