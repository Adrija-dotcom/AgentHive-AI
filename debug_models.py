import google.generativeai as genai

# Use your actual key here
genai.configure(api_key="AIzaSyB-XgQoV2XaxrX8gy_LFDCx-DEiR3WJYaU")

print("--- FETCHING SUPPORTED MODELS ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ USE THIS NAME: {m.name}")
except Exception as e:
    print(f"❌ ERROR: {e}")