import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # SENİN LİSTENDEN SEÇİLEN MODELLER:
    
    # Ana Model: 2.0 Flash (2.5 gibi limitli değildir, çok hızlıdır)
    PRIMARY_MODEL = "models/gemini-2.0-flash"
    
    # Yedek Model: 2.0 Flash Lite (Daha da hafiftir, kota dostudur)
    FALLBACK_MODEL = "models/gemini-2.0-flash-lite"

    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY is not set in environment variables.")
