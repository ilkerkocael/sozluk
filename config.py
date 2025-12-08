import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # "latest" yerine doğrudan 1.5 sürümünü yazıyoruz.
    # 1.5 Flash'ın günlük limiti çok yüksektir (1500 istek).
    PRIMARY_MODEL = "gemini-1.5-flash"
    
    # 1.5 Pro da güçlü ve kararlı bir yedektir.
    FALLBACK_MODEL = "gemini-1.5-pro"

    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY is not set in environment variables.")
