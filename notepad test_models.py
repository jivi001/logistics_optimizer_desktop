import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
print(f"API Key: {api_key[:15]}...")

genai.configure(api_key=api_key)

print("\n=== Listing Available Models ===")
try:
    models = genai.list_models()
    print(f"Found {len(list(models))} models")
    
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"\n✓ {m.name}")
            print(f"  Display: {m.display_name}")
            print(f"  Description: {m.description[:100]}...")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing Direct Model Creation ===")
test_models = ['gemini-1.5-flash-latest', 'gemini-1.5-pro-latest', 'gemini-2.0-flash-exp']

for model_name in test_models:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say hello")
        print(f"✓ {model_name} WORKS! Response: {response.text[:50]}...")
        break
    except Exception as e:
        print(f"✗ {model_name} failed: {str(e)[:80]}...")