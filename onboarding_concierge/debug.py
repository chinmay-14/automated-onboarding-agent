# File: debug.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: No API Key found in .env file!")
else:
    print(f"✅ API Key found: {api_key[:5]}...")
    print("Attempting to list available models...")
    
    try:
        genai.configure(api_key=api_key)
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                available_models.append(m.name)
        
        if not available_models:
            print("⚠️ No text-generation models found. Check your API Key permissions.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")