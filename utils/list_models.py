# list_models.py
import os
from dotenv import load_dotenv

# new genai client
from google import genai

load_dotenv()  # loads .env in working dir (if present)

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")  # fallback
if not API_KEY:
    raise SystemExit("❌ Set GEMINI_API_KEY (or GOOGLE_API_KEY) in env or .env")

# Initialize client (will use API key)
client = genai.Client(api_key=API_KEY)

def list_models():
    try:
        # NOTE: models.list() is the current way to list available models
        models = client.models.list()
        print("Available models (partial info):")
        for m in models:
            # model object may be dict-like; defensively print name and raw repr
            name = getattr(m, "name", None) or (m.get("name") if isinstance(m, dict) else None)
            print("-", name or repr(m))
    except Exception as e:
        print("Failed to list models:", e)
        # debug: show client methods so you can inspect what's available
        print("\nDebug: dir(client):")
        print(sorted([x for x in dir(client) if not x.startswith("_")]))

if __name__ == "__main__":
    list_models()
